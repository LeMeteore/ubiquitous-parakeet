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
    page_title="PCR plate types page",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

if "con" not in st.session_state:
    con = init_connection(database_path)
    st.session_state.con = con

def run():
    st.write("### PCR plate types management")
    con = st.session_state.con
    st.markdown("#### This page will help you create and list _types_ of PCR plates")
    with st.expander("Form to create types of plates"):
        with st.form("plate_type_form", clear_on_submit=True):
            type_, nb_cols, nb_rows, names_cols, names_rows, \
                nb_whites, nb_pos, nb_negs, \
                wells_whites, wells_pos, wells_negs = plate_type_form()
            submit = st.form_submit_button("Submit")
            if False: # what are all the mandatory fields ?
                if type_ != "":
                    created = datetime.datetime.now().strftime("%Y/%m/%d")
                    params = (type_, nb_cols, nb_rows, names_cols, names_rows,
                              nb_whites, nb_pos, nb_negs,
                              " ".join(wells_whites), " ".join(wells_pos), " ".join(wells_negs),
                              created)
                    insert_plate_type(con, params)
                else:
                    st.error("The field 'Type of the plate' should be non empty.")
                    st.stop()

    with st.expander("Available types of plates"):
        df = pd.read_sql("select * from plate_types;", con)
        st.dataframe(df)

if __name__ == "__main__":
    run()
