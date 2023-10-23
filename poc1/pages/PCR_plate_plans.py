import re
import io
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import pathlib
import datetime
import contextlib
from database import init_connection, database_path, insert_plate_type, list_plate_types
from forms import plate_type_form

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
                if submit and type_ != "":
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

        with st.expander("Create a plate"):
            options = dict(list_plate_types())
            with st.form("plate_form", clear_on_submit=True):
                type_ = st.selectbox("Type of the plate",
                                     options=options,
                                     format_func=lambda key: options[key],
                                     index=None,
                                     placeholder="The type for your plate ?",
                                     label_visibility="collapsed")


                submit = st.form_submit_button("Submit")
        with st.expander("List plates"):
            # df = pd.read_sql("select * from plate_types;", st.session_state.con)
            df = pd.DataFrame({})
            st.dataframe(df)


if __name__ == "__main__":
    run()
