import re
import io
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import pathlib
import datetime
import contextlib
from database import init_connection, database_path
from database import list_plate_types, list_patients
from database import insert_plate_type, insert_plate
from forms import plate_type_form, plate_form, plate_patients_form

try:
    from streamlit import rerun as rerun
except ImportError:
    from streamlit import experimental_rerun as rerun


st.set_page_config(
    page_title="PCR plate plans page",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

if "con" not in st.session_state:
    con = init_connection(database_path)
    st.session_state.con = con

def run():
    st.write("### PCR plate plans management")
    con = st.session_state.con
    st.markdown("#### This page will help you create & list PCR plates")
    con = st.session_state.con
    with st.expander("Create a plate"):
        with st.form("plate_form", clear_on_submit=True):
            type_, description = plate_form()
            submit = st.form_submit_button("Submit")
            if submit and type_ and description:
                created = datetime.datetime.now().strftime("%Y/%m/%d")
                status = "empty"
                params = (type_, description, status, created)
                insert_plate(con, params)

    with st.expander("Add patients inside plate "):
        with st.form("patients_form", clear_on_submit=True):
            plate_eid, patients = plate_patients_form()
            submit = st.form_submit_button("Submit")
            if submit and plate_eid and patients:
                st.write(plate_eid)
                st.write(patients)

    with st.expander("List plates"):
        df = pd.read_sql("select * from plates;", con)
        df["List patients"] = pd.Series([False] * df.shape[0], dtype=bool)
        with st.form("plate_patient_edit_form", clear_on_submit=True):
             edited_df = st.data_editor(
                 df,
                 use_container_width=True,
                 hide_index=True,
                 column_config={
                     "List patients": st.column_config.CheckboxColumn(
                         "List patients?",
                         help="Display plate patients",
                         default=False,
                     )
                 },
             )

             plate_eid = edited_df[edited_df["List patients"]]["eid"]
             plate_desc = edited_df[edited_df["List patients"]]["description"]
             show = st.form_submit_button("Show plate patients")
             if show and len(plate_eid) == 1:
                 st.write(f"List of patients for plate name: {plate_desc}")
                 st.write(plate_eid)
                 # select all patients where plate eid equalts plate_eid

if __name__ == "__main__":
    run()
