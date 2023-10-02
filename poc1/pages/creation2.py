import re
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from utils import clear_session_state
import pathlib

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"

st.set_page_config(
    page_title="Creation again",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


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


with st.form("my_form"):
    input_file = st.file_uploader("Choose input file", type=["csv", "xls", "xlsx"])
    output_file = st.file_uploader("Choose output file", type=["csv", "xls", "xlsx"])
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
        blanc, pos, neg = absorbance[-3:]
        # then remove them
        absorbance = absorbance[:-3]
        negative_control = [neg for _ in patients]
        positive_control = [pos for _ in patients]
        # to do
        ratio = [np.nan for _ in patients]
        positivity = [np.nan for _ in patients]
        df_result = pd.DataFrame({
            "Patients": patients,
            "Absorbance": absorbance,
            "Contrôle négatif": negative_control,
            "Contrôle positif": positive_control,
            "Ratio": ratio,
            "Positivity_IDVet": positivity,
        })
        # change O to 0 ??? ask them to take care of this ???
        df_result.replace('O','0', regex=True, inplace=True)
        df_result.astype(np.float64)
        st.session_state.df_result = df_result

if "df_result" in st.session_state:
    st.success("Results processed successfully!")
    st.dataframe(
        st.session_state.df_result,
        column_config={
        "Patients": st.column_config.NumberColumn(
            "Patients",
            help="Patients IDs",
            format="%d",
        )},
    hide_index=True,
    )
    csv = convert_df(st.session_state.df_result)

    st.download_button(
        "Press to Download",
        csv,
        "result.csv",
        "text/csv",
        key='download-csv'
    )
