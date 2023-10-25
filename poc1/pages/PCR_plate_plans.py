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
from forms import plate_type_form, plate_form


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
    tab1, tab2 = st.tabs(["Types", "Plates"])
    con = st.session_state.con
    with tab1:
        st.markdown("#### This page will help you create and list _types_ of PCR plates")
        with st.expander("Form to create types of plates"):
            with st.form("plate_type_form", clear_on_submit=True):
                type_, nb_cols, nb_rows, names_cols, names_rows, \
                    nb_whites, nb_pos, nb_negs, \
                    wells_whites, wells_pos, wells_negs = plate_type_form()
                submit = st.form_submit_button("Submit")
                if submit and type_ != "": # what are all the mandatory fields ?
                    created = datetime.datetime.now().strftime("%Y/%m/%d")
                    params = (type_, nb_cols, nb_rows, names_cols, names_rows,
                              nb_whites, nb_pos, nb_negs,
                              " ".join(wells_whites), " ".join(wells_pos), " ".join(wells_negs),
                              created)
                    insert_plate_type(con, params)

        with st.expander("Available types of plates"):
            df = pd.read_sql("select * from plate_types;", con)
            st.dataframe(df)

    with tab2:
        st.markdown("#### This page will help you create & list PCR plates")
        con = st.session_state.con
        with st.expander("Create a plate"):
            with st.form("plate_form", clear_on_submit=True):
                type_ = plate_form()
                submit = st.form_submit_button("Submit")
                if submit and type_:
                    created = datetime.datetime.now().strftime("%Y/%m/%d")
                    status = "empty"
                    params = (type_, status, created)
                    insert_plate(con, params)

        with st.expander("Add patients inside plate "):
            with st.form("patients_form", clear_on_submit=True):

                submit = st.form_submit_button("Submit")
                if submit and type_ != "":
                    st.write("")

        with st.expander("List plates"):
            df = pd.read_sql("select * from plates;", con)
            st.dataframe(df)


if __name__ == "__main__":
    run()
