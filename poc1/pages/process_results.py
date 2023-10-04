import re
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from utils import clear_session_state
import pathlib
import io

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"

st.set_page_config(
   page_title="Creation again",
   layout="wide",
   initial_sidebar_state="collapsed",
   menu_items=None,
)

@st.cache_data
def convert_to_csv(df):
   # IMPORTANT: Cache the conversion to prevent computation on every rerun
   return df.to_csv(index=False).encode('utf-8')

# UnhashableParamError: Cannot hash argument 'df' (of type pandas.io.formats.style.Styler) in 'convert_df'.
# To address this, you can tell Streamlit not to hash this argument by adding a leading underscore to
# the argument's name in the function signature:
@st.cache_data
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
blanc = 0.047
neg = 0.052
pos = 1.442
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
          type=["csv", "xls", "xlsx"],
          help="Enter an Excel file containing your plaque"
       )
   with col2:
       output_file = st.file_uploader(
          "Output file",
          type=["csv", "xls", "xlsx"],
          help="Enter an Excel file containing results returned by the Spectrometer"
       )
   submit_button_form = st.form_submit_button("Submit file")
   if submit_button_form:
      # transform input file to a list of patients
      dfi = pd.read_excel(input_file, sheet_name="Plan de plaque")
      # ideal world, there is no empty cells inside the excel file
      # clean empty lines
      dfi.dropna(axis = 0, how = 'all', inplace=True)
      # clean empty cols
      dfi.dropna(axis = 1, how = 'all', inplace=True)
      dfi = dfi.iloc[1:,1:]
      # retrieve patients
      patients = []
      for column in dfi.columns:
         patients.extend(dfi[column].tolist())
         # remove the last 3 elts of the list
      patients = patients[:-3]

      # open all the sheets
      output_xls = pd.ExcelFile(output_file)
      # retrieve each sheets
      df_absorbance = pd.read_excel(output_xls, "Résultats d'absorbance")
      df_données_brutes_450nm = pd.read_excel(output_xls, "Données brutes 450 nm")
      df_info_gen = pd.read_excel(output_xls, "Informations générales")
      df_journal_exec = pd.read_excel(output_xls, "Journal d'exécution")

      # retrieve wave length from 1st sheet
      wave_length = df_absorbance.iloc[3,1] # no need to .extract('(\d+)') ???
      # extract actual absorbance data
      absorbance_data = df_absorbance.iloc[5:,1:]
      # transform the df to a list
      absorbance = []
      for column in absorbance_data.columns:
         absorbance.extend(absorbance_data[column].tolist())

      # extract blanc, pos, neg
      blanc, neg, pos = absorbance[-3:]
      # then remove them
      absorbance = absorbance[:-3]
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
      # df_result.astype(np.float64)
      df_result["Patients"] = df_result["Patients"].astype(str)

      # color positivity col
      # df_result.style.apply(apply_formatting) # axis = 0
      df_styled = df_result.style.map(color_positivity, subset=["Positivity_IDVet"])
      st.session_state.df_result = df_result
      st.session_state.df_styled = df_styled

if "df_result" in st.session_state:
   with st.expander("See plot"):
      df = st.session_state.df_result
      # dataviz ?
      st.scatter_chart(data=df, x="Patients", y="Ratio", size="Absorbance")

   with st.expander("See Tabular datas"):
      st.success("Results processed successfully!")
      st.dataframe(
         st.session_state.df_styled,
         column_config={
            "Patients": st.column_config.NumberColumn(
               "Patients",
               help="Patients IDs",
               format="%d",
            )},
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
