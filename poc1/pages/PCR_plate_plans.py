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
        ncols integer not null,
        nrows integer not null,
        nwhites integer not null,
        npos integer not null,
        nnegs integer not null,
        created varchar(50) not null
        );
        """)
        con.commit()


def run():
    st.write("### PCR plate plans management")

    tab1, tab2, tab3 = st.tabs(["PCR plates", "foo", "bar"])

    with tab1:
        with st.expander("Form to create different types of plates"):
            with st.form("plate_type_form", clear_on_submit=True):
                type_ = st.text_input("Type of the plate")
                col1, col2 = st.columns(2)
                with col1:
                    ncols = st.number_input("Number of columns", step=1, min_value=1)
                with col2:
                    nrows = st.number_input("Number of rows", step=1, min_value=1)
                col4, col5, col6 = st.columns(3)
                with col4:
                    nwhites = st.number_input("Number of whites", step=1, min_value=1)
                with col5:
                    npos = st.number_input("Number of positives", step=1, min_value=1)
                with col6:
                    nnegs = st.number_input("Number of negatives", step=1, min_value=1)

                submit = st.form_submit_button("Submit")
                if submit:
                    # retrieve all the fields and store them inside the database
                    con = st.session_state.con
                    query = """
                    insert into plate_types (type, ncols, nrows, nwhites, npos, nnegs, created)
                    values (?, ?, ?, ?, ?, ?, ?)
                    """
                    created = datetime.datetime.now().strftime("%Y/%m/%d")
                    params = (type_, ncols, nrows, nwhites, npos, nnegs, created)
                    with contextlib.closing(con.cursor()) as cur:
                        cur.execute(query, params)
                        con.commit()

        with st.expander("Available types of plate"):
            df = pd.read_sql("select * from plate_types;", st.session_state.con)
            st.dataframe(df)

    with tab2:
        st.header("foo")

    with tab3:
        st.header("bar")


if __name__ == "__main__":
    create_plate_types_table()
    run()
