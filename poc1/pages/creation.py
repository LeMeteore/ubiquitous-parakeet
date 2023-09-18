import pathlib
import streamlit as st
import pandas as pd
import numpy as np
import string
from enum import Enum
import re
from utils import *

class Types(Enum):
    Alpha = string.ascii_uppercase
    Numeric = string.digits

options = [Types.Alpha.name, Types.Numeric.name]


st.set_page_config(page_title="Creation page")
st.sidebar.header("Create")

st.markdown("# Creation page")


if 'stage' not in st.session_state:
    st.session_state.stage = 0

with st.form(key='my_form'):
    name = st.text_input('Name', 'Name of the plaque')
    number = st.select_slider('Number of columns/rows', options=[6, 8, 9])
    col1, col2 = st.columns(2)
    with col1:
        ctype = st.radio(
            "Name type for columns",
            options=options,
        )
    with col2:
        rtype = st.radio(
            "Name type for rows",
            options=options,
        )
    add_initial_fields_inside_session(name, number, ctype, rtype)
    submitted = st.form_submit_button(label="Submit", on_click=set_stage, args=(1,))



if st.session_state.stage == 1:
    name, number, ctype, rtype = get_initial_fields_inside_session(name, number, ctype, rtype)
    columns = list(Types[ctype].value[:number])
    indexes = list(Types[rtype].value[:number])
    # add the new dataframe inside the session
    df = pd.DataFrame(columns=columns, index=indexes)
    st.session_state.df_name = name
    edited_df = st.data_editor(df)
    st.session_state.edited_df = edited_df
    st.button('Submit', on_click=backup_df)

st.button('Reset Form', on_click=clear_session_state)
st.write(st.session_state)
