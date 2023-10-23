import sqlite3
import pandas as pd
import streamlit as st
import datetime
import contextlib
from database import init_connection, database_path
from utils import convert_to_excel

try:
    from streamlit import rerun as rerun
except ImportError:
    from streamlit import experimental_rerun as rerun

st.set_page_config(
    page_title="Patients page",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

if "con" not in st.session_state:
    init_connection(database_path)
    st.session_state.con = con

def patients():
    # patient form insertion
    with st.expander("Import from Excel file"):
        con = st.session_state.con
        st.write("## Import")
        with st.form("my_patients_upload_form", clear_on_submit=True):
            input_file = st.file_uploader(
                "Input file",
                type=["xls", "xlsx"],
                help="Enter an Excel file containing patients list"
            )
            submit_button_form = st.form_submit_button("Submit file")
            if submit_button_form:
                columns = ["firstname", "lastname", "age", "sex"]
                dfp = pd.read_excel(input_file, sheet_name="Patients", header=None, names=columns)
                now = datetime.datetime.now().strftime("%Y/%m/%d")
                dfp["created"] = pd.Series([now] * dfp.shape[0])
                # insert inside table
                dfp.to_sql('patients', con, if_exists='append', index=False)

    with st.expander("Add with form"):
        st.write("## Patient creation")
        with st.form("creation_form", clear_on_submit=True):
            # patient form
            c1, c2 = st.columns(2)
            with c2:
                firstname = st.text_input("Firstname",
                                      placeholder="Firstname",
                                      label_visibility="collapsed")
                lastname = st.text_input("Lastname",
                                      placeholder="Lastname",
                                      label_visibility="collapsed")

            with c1:
                age = st.number_input("Age",
                                      step=1, min_value=1,
                                      value=None,
                                      placeholder="Patient age",
                                      label_visibility="collapsed")
                sex = st.selectbox("Patient sex",
                                   ("Male", "Female"),
                                   index=None,
                                   placeholder="Patient sex",
                                   label_visibility="collapsed")

            submit_button_form = st.form_submit_button("Submit")
            if submit_button_form:
                con = st.session_state.con
                now = datetime.datetime.now().strftime("%Y/%m/%d")
                query = """
                insert into patients(firstname, lastname, age, sex, created) values (?, ?, ?, ?, ?)
                """
                with contextlib.closing(con.cursor()) as cur:
                    cur.execute(query, (firstname, lastname, age, sex, now))
                    con.commit()

    # patient list
    with st.expander("List"):
        con = st.session_state.con
        df = pd.read_sql("SELECT * from patients", st.session_state.con)
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
            ids_to_rm = edited_df[edited_df["Delete"]]["eid"]
            ids_to_rm = [(i,) for i in ids_to_rm]
            delete = st.form_submit_button("Delete")
            if delete and len(ids_to_rm) != 0:
                con = st.session_state.con
                query = "delete from patients where eid = ?"
                with contextlib.closing(con.cursor()) as cur:
                    cur.executemany(query, ids_to_rm)
                    con.commit()
                # https://docs.streamlit.io/library/api-reference/control-flow/st.rerun
                rerun()
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        con = st.session_state.con
        dfr = pd.read_sql("SELECT * from patients", con)
        download = st.download_button(
            label="Download patients",
            data=convert_to_excel(dfr),
            file_name=f"patients_list_{now}.xlsx",
            mime="application/vnd.ms-excel",
            key='download-csv'
        )

if __name__ == "__main__":
    patients()
