import re
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import pathlib
import datetime

try:
    from streamlit import rerun as rerun
except ImportError:
    from streamlit import experimental_rerun as rerun

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"
database_path = basedir / "database.sqlite"

st.set_page_config(
    page_title="Patients page",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

st.write("# Patients management")

if "con" not in st.session_state:
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    st.session_state.con = con
    st.session_state.cur = cur


def create_patients_table():
    st.session_state.cur.execute("""
    create table if not exists patients(
    eid integer primary key,
    firstname varchar(50) not null,
    lastname varchar(50) not null,
    age integer not null,
    sex varchar(50) not null,
    created varchar(50) not null
    );
    """)

def patients():
    con = st.session_state.con

    # patient form insertion
    with st.expander("Add"):
        st.write("## Patient creation")
        with st.form("creation_form", clear_on_submit=True):
            # patient form
            c1, c2 = st.columns(2)
            with c2:
                firstname = st.text_input("Firstname")
                lastname = st.text_input("Lastname")

            with c1:
                age = st.text_input('Age', placeholder='00')
                sex = st.selectbox(
                    'Sex',
                    ('Male', 'Female')
                )

            if age != '':
                try:
                    number = int(age)  # try to convert the variable to an integer
                except ValueError:  # if it's not convertible, catch the ValueError exception
                    st.markdown(f"**:red[{age}]** is NOT a number")

            submit_button_form = st.form_submit_button("Submit")
            if submit_button_form:
                cur = st.session_state.cur
                con = st.session_state.con
                now = datetime.datetime.now().strftime("%Y/%m/%d")
                query = """
                insert into patients(firstname, lastname, age, sex, created) values (?, ?, ?, ?, ?)
                """
                cur.execute(query, (firstname, lastname, age, sex, now))
                con.commit()

    # patient list
    with st.expander("List"):
        df = pd.read_sql("SELECT * from patients", con)
        df["Delete"] = pd.Series([False] * df.shape[0], dtype=bool)

        st.write("## Patients list")
        with st.form("deletion_form", clear_on_submit=True):
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                disabled=["eid", "firstname", "lastname", "age", "sex", "created"],
                column_config={
                    "Delete": st.column_config.CheckboxColumn(
                        "Delete?",
                        help="Select patients you want to delete",
                        default=False,
                    )
                },
            )
            #
            delete = st.form_submit_button("Delete")
            if delete:
                cur = st.session_state.cur
                con = st.session_state.con
                # selected_rows = edited_df[edited_df.Select]
                ids_to_delete = tuple(edited_df[edited_df["Delete"]]["eid"])
                # delete from patients where ids in
                query = "delete from patients where eid = ?"
                cur.executemany(query, (ids_to_delete,))
                con.commit()
                # https://docs.streamlit.io/library/api-reference/control-flow/st.rerun
                rerun()

    # the menu inside the sidebar
    # with st.sidebar.form("menu_form", clear_on_submit=True):
    #     option = st.selectbox("Actions", ["Update"])
    #     button = st.form_submit_button()


if __name__ == "__main__":
    create_patients_table()
    patients()
