import re
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from utils import clear_session_state, create_plaque
import pathlib
import datetime

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"
database_path = basedir / "database.sqlite"

if "conn" not in st.session_state:
    st.session_state.conn = sqlite3.connect(database_path)
    st.session_state.c = st.session_state.conn.cursor()

st.session_state.c.execute("""
 create table if not exists patients(
  eid primary key,
  firstname varchar(50) not null,
  lastname varchar(50) not null,
  age integer not null,
  sex varchar(50) not null,
  created varchar(50) not null
  );
""")

# Perform query.
df = pd.read_sql("SELECT * from patients", st.session_state.conn)


st.set_page_config(
    page_title="Patients",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

with st.form("my_form", clear_on_submit=True):
    eid = st.number_input('Patient number')
    firstname = st.text_input("Firstname")
    lastname = st.text_input("Lastname")
    age = st.text_input('Patient age', placeholder='00')
    if age != '':
        try:
            number = int(age)  # try to convert the variable to an integer
        except ValueError:  # if it's not convertible, catch the ValueError exception
            st.markdown(f"**:red[{age}]** is NOT a number")
    sex = st.selectbox(
        'Sex',
        ('Male', 'Female')
    )
    submit_button_form = st.form_submit_button("Submit form")
    if submit_button_form:
        c = st.session_state.c
        conn = st.session_state.conn
        query = """
        insert into patients(eid, firstname, lastname, age, sex, created) values (?, ?, ?, ?, ?, ?)
        """
        c.execute(query, (eid, firstname, lastname, age, sex, datetime.datetime.now().strftime("%Y/%m/%d")))
        conn.commit()
        df = pd.read_sql("SELECT * from patients", conn)

st.dataframe(df, use_container_width=True)
