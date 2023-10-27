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
from database import insert_plate_type, insert_plate, insert_plate_patients, list_plate_patients
from forms import plate_type_form, plate_form, plate_patients_form

try:
    from streamlit import rerun as rerun
except ImportError:
    from streamlit import experimental_rerun as rerun


st.set_page_config(
    page_title="PCR plate plans page",
    layout="wide",
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
    # TODO, create a plate from excel file
    with st.expander("Create a plate from an Excel file"):
        with st.form("plate_form_excel", clear_on_submit=True):
            input_file = st.file_uploader(
                "Input file",
                type=["csv", "xls", "xlsx"],
                help="Enter an Excel file containing your plate"
            )
            col1, col2 = st.columns(2)
            with col1:
                type_ = st.selectbox("Type of the plate",
                                     # TODO, dynamically select available type of plates
                                     options=["Type001", "Type002", "Type...."],
                                     index=None,
                                     placeholder="The type for your plate ?",
                                     label_visibility="collapsed")
            with col2:
                description = st.text_input("Plate description",
                                            placeholder="Plate description",
                                            label_visibility="collapsed")
            submit = st.form_submit_button("Submit")
            if submit and type_ and description:
                # TODO, check that the excel file respect the shape specified in the type
                # TODO, save plate, then extract patients from excel file and store them too
                st.write("Foobar \o/")

    with st.expander("Create a plate using a form"):
        with st.form("plate_form", clear_on_submit=True):
            type_, description = plate_form()
            submit = st.form_submit_button("Submit")
            if submit and type_ and description:
                created = datetime.datetime.now().strftime("%Y/%m/%d")
                status = "empty"
                params = (type_, description, status, created)
                insert_plate(con, params)

    # TODO, find a way to tell in which well add a patient
    # TODO, find a way to select X patients and add them inside X wells
    # TODO, make sure to add the correct number of patients inside the plate
    with st.expander("Add patients inside plate "):
        with st.form("patients_form", clear_on_submit=True):
            plate_eid, patients = plate_patients_form()
            submit = st.form_submit_button("Submit")
            if submit and plate_eid and patients:
                params = tuple([(plate_eid, p) for p in patients])
                insert_plate_patients(con, params)

    with st.expander("List plates"):
        df = pd.read_sql("select * from plates;", con)
        df["Action"] = pd.Series([False] * df.shape[0], dtype=bool)

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Action": st.column_config.CheckboxColumn(
                    "Action",
                    help="Display plate patients",
                    default=False,
                )
            },
        )

        plate_eid = edited_df[edited_df["Action"]]["eid"] # this is a Serie object
        plate_desc = edited_df[edited_df["Action"]]["description"]

        c1, c2 = st.columns([1, 3])
        with c1:
            option = st.selectbox(
                'Available actions on plates list',
                ('Show', 'Download', 'Delete', 'Map'),
                index=None,
                placeholder="Select one action...",
            )

        if len(plate_eid) != 0 and option:
            st.write('You selected the following action:', option)
            st.write("Action will be applied on the following plates:", list(plate_eid))
            # TODO, if display, make sure only one plate is selected
            # TODO, if display, display a reprensentation of the plate

if __name__ == "__main__":
    run()
