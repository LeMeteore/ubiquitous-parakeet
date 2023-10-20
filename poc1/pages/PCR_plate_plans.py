import re
import io
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import pathlib
import datetime
import contextlib

try:
    from streamlit import rerun as rerun
except ImportError:
    from streamlit import experimental_rerun as rerun

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"
database_path = basedir / "database.sqlite"

st.set_page_config(
    page_title="PCR plate plans page",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

@st.cache_resource
def init_connection():
    return sqlite3.connect(database_path, check_same_thread=False)

if "con" not in st.session_state:
    con = init_connection()
    st.session_state.con = con

@st.cache_resource
def create_plate_types_table():
    con = st.session_state.con
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("""
        create table if not exists plate_types(
        eid integer primary key,
        type varchar(50) not null,
        nb_cols integer not null,
        col_names varchar(50) not null, -- letters of numbers
        nb_rows integer not null,
        row_names varchar(50) not null, -- letters of numbers
        nb_whites integer not null,
        nb_pos integer not null,
        nb_negs integer not null,
        created varchar(50) not null
        );
        """)
        con.commit()


def run():
    st.write("### PCR plate plans management")

    tab1, tab2, tab3 = st.tabs(["Types", "Plates", "bar"])

    with tab1:
        st.markdown("#### This page will help you create and list _types_ of PCR plates")
        with st.expander("Form to create types of plates"):
            with st.form("plate_type_form", clear_on_submit=True):
                type_ = st.text_input("Type of the plate",
                                      placeholder="Type of the plate",
                                      label_visibility="collapsed")
                col1, col2 = st.columns(2)
                with col1:
                    nb_cols = st.number_input("Number of columns",
                                            step=1, min_value=1,
                                            value=None,
                                            placeholder="Number of columns",
                                            label_visibility="collapsed")
                    nb_rows = st.number_input("Number of rows",
                                            step=1, min_value=1,
                                            value=None,
                                            placeholder="Number of rows",
                                            label_visibility="collapsed")
                with col2:
                    col_names = st.selectbox("Columns naming scheme",
                                                      ("Letters", "Numbers"),
                                                      index=None,
                                                      placeholder="How to name the columns?",
                                                      label_visibility="collapsed")
                    row_names = st.selectbox("Rows naming scheme",
                                                      ("Letters", "Numbers"),
                                                      index=None,
                                                      placeholder="How to name the rows?",
                                                      label_visibility="collapsed")


                col4, col5, col6 = st.columns(3)
                with col4:
                    nb_whites = st.number_input("Number of whites",
                                              step=1, min_value=1,
                                              value=None,
                                              placeholder="Number of whites",
                                              label_visibility="collapsed")
                with col5:
                    nb_pos = st.number_input("Number of positives",
                                           step=1, min_value=1,
                                           value=None,
                                           placeholder="Number of positives",
                                           label_visibility="collapsed")

                with col6:
                    nb_negs = st.number_input("Number of negatives",
                                            step=1, min_value=1,
                                            value=None,
                                            placeholder="Number of negatives",
                                            label_visibility="collapsed")


                submit = st.form_submit_button("Submit")
                if submit and type_ != "":
                    # retrieve all the fields and store them inside the database
                    con = st.session_state.con
                    query = """
                    insert into plate_types (type, nb_cols, col_names, nb_rows, row_names, nb_whites, nb_pos, nb_negs, created)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    created = datetime.datetime.now().strftime("%Y/%m/%d")
                    params = (type_, nb_cols, col_names, nb_rows, row_names,
                              nb_whites, nb_pos, nb_negs, created)
                    with contextlib.closing(con.cursor()) as cur:
                        cur.execute(query, params)
                        con.commit()

        with st.expander("Available types of plates"):
            df = pd.read_sql("select * from plate_types;", st.session_state.con)
            st.dataframe(df)

    with tab2:
        st.markdown("#### This page will help you create & list PCR plates")
        with st.expander("Create a plate"):
            with st.form("plate_form", clear_on_submit=True):
                st.write("form")
                submit = st.form_submit_button("Submit")
        with st.expander("List plates"):
            # df = pd.read_sql("select * from plate_types;", st.session_state.con)
            df = pd.DataFrame({})
            st.dataframe(df)


    with tab3:
        st.markdown("#### This page will help you for nothing")


if __name__ == "__main__":
    create_plate_types_table()
    run()
