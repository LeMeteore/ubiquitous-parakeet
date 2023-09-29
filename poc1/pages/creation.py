import re
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from utils import clear_session_state, create_plaque
import pathlib

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"
database_path = basedir / "database.sqlite"
conn = sqlite3.connect(database_path)
c = conn.cursor()
c.execute("""
 create table if not exists plaques(
  eid primary key,
  name varchar(50) not null,
  filepath varchar(50) not null,
  created varchar(50) not null
  );
""")

st.set_page_config(
    page_title="Creation",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)


# Initialize session state
if "first_form_completed" not in st.session_state:
   st.session_state["first_form_completed"] = False
   st.session_state["input_file_uploaded"] = False
   st.session_state["form_filled"] = False

if "input_file_uploaded" in st.session_state and st.session_state.input_file_uploaded:
    st.success("Input file uploaded successfully!")

if "input_file_saved" in st.session_state and st.session_state.input_file_saved:
    st.success("Input file saved successfully!")

with st.form("my_form"):
    source = st.radio(label="source", options=["file", "form"])
    if st.form_submit_button("Submit"):
        st.session_state["first_form_completed"] = True
        st.session_state.source = source

if st.session_state["first_form_completed"]:
    source = st.session_state.source
    with st.form("my_form2"):
        name = st.text_input("Name", "Name of the plaque")
        type_ = st.text_input("Type", "Type of the plaque")
        wave_length = st.number_input("Wave length")
        date = st.date_input("Date")
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xls", "xlsx"])
        submit_button_form2 = st.form_submit_button("Submit file")
        if submit_button_form2:
            if uploaded_file is not None:
                st.session_state["input_file_uploaded"] = True
                st.session_state["input_file"] = uploaded_file
                st.session_state["name"] = name
                st.session_state["type"] = type_
                st.session_state["wave_length"] = wave_length
                st.session_state["date"] = date

if st.session_state["input_file_uploaded"]:
    with st.form("my_form4"):
       df = create_plaque(st.session_state.input_file)
       # display the uploaded file just for confirmation
       edited_df = st.data_editor(df, disabled=True)
       submit_button_form4 = st.form_submit_button("Submit dataframe")
       if submit_button_form4:
           name = st.session_state["name"]
           type_ = st.session_state["type"]
           wave_length = st.session_state["wave_length"]
           date = st.session_state["date"]

           datadir = datadir / pathlib.Path(date.strftime("%Y/%m/%d"))
           datadir.mkdir(parents=True, exist_ok=True)
           filepath = datadir / f"{name}.parquet.gzip"
           print(filepath)
           # replace blanc -> 0, neg -> -1, pos -> 1
           df = df.replace('BLANC','0', regex=True)
           df = df.replace('NEG','-1', regex=True)
           df = df.replace('POS','1', regex=True)
           # replace O with 0
           df = df.replace('O','0', regex=True)
           # change everything to float
           df = df.astype(np.float64)
           # save to parquet
           df.to_parquet(filepath, compression="gzip")
           # save to database
           c.execute("insert into plaques(name, filepath, created) values (?, ?, ?)",
                     (name, filepath.as_posix(), date))
           conn.commit()
           st.session_state["input_file_saved"] = True

st.button("Reset Page", on_click=clear_session_state)
# https://docs.streamlit.io/library/api-reference/data/st.column_config
