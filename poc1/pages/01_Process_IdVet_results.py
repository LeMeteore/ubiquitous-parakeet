import pandas as pd
import streamlit as st
import pathlib
import io
import altair as alt
import math
import string, random

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

st.set_page_config(
   page_title="Process IdVet results",
   layout="wide",
   initial_sidebar_state="collapsed",
   menu_items=None,
)

multi = '''## Processing of IdVet tests results

First, upload an Excel file containing your PCR plate plan. Next, upload the Excel file containing the results. The files should respect the following formats:


'''
st.markdown(multi)

@st.cache_data
def convert_to_csv(df):
   # IMPORTANT: Cache the conversion to prevent computation on every rerun
   return df.to_csv(index=False).encode('utf-8')

# UnhashableParamError: Cannot hash argument 'df' (of type pandas.io.formats.style.Styler) in 'convert_df'.
# To address this, you can tell Streamlit not to hash this argument by adding a leading underscore to
# the argument's name in the function signature:
def convert_to_excel(_df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
       _df.to_excel(writer)
    return buffer

def categorize_ratio(ratio):
   if ratio < 30:
      return 0
   elif ratio >= 30 and ratio <= 40:
      return 2
   else:
      return 1

def color_positivity(val):
   if val == 0:
      color = "red"
   elif val == 1:
      color = "green"
   else:
      color = 'yellow'
   return f'background-color: {color}'


def apply_formatting(col):
   if col.name == 'Positivity_IDVet':
      return [color_positivity(v) for v in col.values]

# for this type of plaque, blanc, neg, pos doesn't need to be in the DF
# for this type of plaque, blanc, neg, pos are the last elts of the last column
# blanc = 0.047
# neg = 0.052
# pos = 1.442
# souds like 96 puits & wave_length are attributes for this type of plaque (or this type of exam)
model = 96
wave_length = 450
# what is idvet ?

# Initialize session state
if "files_uploaded" not in st.session_state:
   st.session_state["files_uploaded"] = False


with st.form("my_form", clear_on_submit=True):
   col1, col2 = st.columns(2)
   with col1:
       input_file = st.file_uploader(
          "Input file",
          type=["xls", "xlsx"],
          help="Enter an Excel file containing your plate, the file should have a worksheet named 'Plan de plaque'."
       )
   with col2:
       output_file = st.file_uploader(
          "Output file",
          type=["xls", "xlsx"],
          help="Enter an Excel file containing results returned by the Spectrometer, the file should have a worksheet named 'Résultats d'absorbance'."
       )
   submit_button_form = st.form_submit_button("Submit file")
   if submit_button_form:
      # transform input file to a list of patients
      try:
         # read patients number as strings
         dfi = pd.read_excel(input_file, sheet_name="Plan de plaque", dtype=str)
      except ValueError as err:
         if str(err) == "Worksheet named 'Plan de plaque' not found":
            st.error("Please, reload page then as input file, upload Excel file containing a worksheet named 'Plan de plaque'")
            s.stop()

      # ideal world, there is no empty cells inside the excel file
      # clean empty lines
      dfi.dropna(axis = 0, how = 'all', inplace=True)
      # clean empty cols
      dfi.dropna(axis = 1, how = 'all', inplace=True)
      # this is the actual dataframe, rows and cols with something in it
      dfi = dfi.iloc[1:,1:]
      # clean NaN cols again
      dfi.dropna(axis = 1, how = 'all', inplace=True)
      # retrieve patients
      patients = []
      for column in dfi.columns:
         # take element after element, column after column
         patients.extend(dfi[column].tolist())

      # patients are everything until I find BLANC or keep everything except the nan values
      # patients = [x for x in takewhile(lambda x: x!="BLANC", patients)]
      # patients = [item for item in patients if not(math.isnan(item)) == True]
      patients = [item for item in patients if isinstance(item, str) == True]

      # blanc, neg, pos are the last 3
      controls_identifiers = patients[-3:]

      # samples are everything except the last 3
      patients = patients[:-3]

      # open all the sheets from the output file
      output_xls = pd.ExcelFile(output_file)
      # retrieve each sheets
      try:
         df_absorbance = pd.read_excel(output_xls, "Résultats d'absorbance")
      except ValueError as err:
         if str(err) == "Worksheet named 'Résultats d'absorbance' not found":
            st.error("Please, reload page and for the output file, upload an Excel file containing a worksheet named 'Résultats d'absorbance'")
            st.stop()

      df_données_brutes_450nm = pd.read_excel(output_xls, "Données brutes 450 nm")
      df_info_gen = pd.read_excel(output_xls, "Informations générales")
      df_journal_exec = pd.read_excel(output_xls, "Journal d'exécution")

      # retrieve wave length from 1st sheet
      wave_length = df_absorbance.iloc[3,1] # no need to .extract('(\d+)') ???
      some_date_and_hour = df_absorbance.iloc[1,1]
      # extract actual absorbance data
      absorbance_data = df_absorbance.iloc[5:,1:]
      # clean NaN cols again
      absorbance_data.dropna(axis = 1, how = 'all', inplace=True)

      # transform the df to a list
      absorbance = []
      for column in absorbance_data.columns:
         absorbance.extend(absorbance_data[column].tolist())

      # keep everything except the nan values
      absorbance = [item for item in absorbance if not(math.isnan(item)) == True]

      # extract controls, the last 3 of the column
      controls_values = absorbance[-3:]

      # define which one is white ? which one is neg ? which one is pos ?
      controls_dict = dict(zip(controls_identifiers, controls_values))
      blanc = controls_dict.get("BLANC")
      neg = controls_dict.get("NEG")
      pos = controls_dict.get("POS")

      # then remove them
      absorbance = absorbance[:-3]

      # length of absorbance should be equal to length of patients
      if len(absorbance) != len(patients):
         st.error(f"The number of patients ({len(patients)}) does not equal the number of results ({len(absorbance)}). Call the police.")
         st.stop()
      negative_control = [neg for _ in patients]
      positive_control = [pos for _ in patients]
      df_result = pd.DataFrame({
         "Patients": patients,
         "Absorbance": absorbance,
         "Contrôle négatif": negative_control,
         "Contrôle positif": positive_control,
      })
      # to do
      # add ration & positivity cols
      df_result["Ratio"] = (df_result["Absorbance"] - df_result["Contrôle négatif"]) / (df_result["Contrôle positif"] - df_result["Contrôle négatif"]) * 100
      df_result["Positivity_IDVet"] = df_result["Ratio"].apply(categorize_ratio)

      # change O to 0 ??? ask them to take care of this ???
      # df_result.replace('O','0', regex=True, inplace=True)
      df_result["Patients"] = df_result["Patients"].astype(str)

      # color positivity col
      # df_result.style.apply(apply_formatting) # axis = 0
      df_styled = df_result.style.map(color_positivity, subset=["Positivity_IDVet"])
      st.session_state.df_result = df_result
      st.session_state.df_styled = df_styled

if "df_result" in st.session_state:
   with st.expander("See plot"):
      df = st.session_state.df_result
      # dataviz ? this is how to make a chart with last version of streamlit
      # st.scatter_chart(data=df, x="Patients", y="Ratio", size="Absorbance")

      # alternative way of scatter plotting (when st.scatter_chart is not available)
      chart = alt.Chart(df).mark_point().encode(
         x='Patients',
         y='Ratio',
         size='Absorbance',
         tooltip=['Patients', 'Absorbance', 'Ratio']
      ).interactive()
      st.altair_chart(chart, use_container_width=True)

   with st.expander("See Tabular datas"):
      st.success("Results processed successfully!")
      st.dataframe(
         st.session_state.df_styled,
         # column_config={
         #    "Patients": st.column_config.NumberColumn(
         #       "Patients",
         #       help="Patients IDs",
         #       format="%d",
         #    )},
         hide_index=True,
      )

      # st.download_button(
      #    label="Download CSV",
      #    data=convert_df(st.session_state.df_result),
      #    file_name="results.csv",
      #    mime="text/csv",
      #    key='download-csv'
      # )

      st.download_button(
         label="Download Excel",
         data=convert_to_excel(st.session_state.df_styled),
         file_name="results.xlsx",
         mime="application/vnd.ms-excel",
         key='download-csv'
      )



# https://www.youtube.com/watch?v=_-xxMeUl6i0
# https://stackoverflow.com/a/60178107
