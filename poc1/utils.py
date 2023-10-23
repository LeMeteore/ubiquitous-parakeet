import re
import io
import string
import streamlit as st
import pandas as pd
import numpy as np

def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '_', s)
    return s

def set_stage(stage):
    st.session_state.stage = stage

def clear_session_state():
    # Delete all the items in Session state
    for key in st.session_state.keys():
        del st.session_state[key]

def backup_df():
    df = st.session_state.edited_df
    df.to_pickle(f"./{urlify(str(st.session_state.name)).lower()}.pkl")
    # clear_session_state()

def add_initial_fields_inside_session(name, number, ctype, rtype):
    st.session_state.name = name
    st.session_state.number = number
    st.session_state.ctype = ctype
    st.session_state.rtype = rtype

def get_initial_fields_inside_session(name, number, ctype, rtype):
    name = st.session_state.name
    number = st.session_state.number
    ctype = st.session_state.ctype
    rtype = st.session_state.rtype
    return name, number, ctype, rtype

def create_plaque0(file):
    df = pd.read_excel(file)
    name = df.iloc[1,0]
    date = df.iloc[0,0]
    wave_length = df.iloc[2,0]
    new_df = df.iloc[5:,1:]
    nrows = new_df.shape[0]
    ncols = new_df.shape[1]
    new_df.index = list(string.ascii_uppercase[:nrows])
    new_df.columns = list(range(1, ncols+1))
    return (name, date, wave_length, new_df)

def create_plaque(file):
    df = pd.read_excel(file, sheet_name="Plan de plaque")
    df.dropna(axis = 0, how = 'all', inplace=True)
    df.dropna(axis = 1, how = 'all', inplace=True)
    df = df.iloc[1:,1:]
    nrows = df.shape[0]
    ncols = df.shape[1]
    df.index = list(string.ascii_uppercase[:nrows])
    df.columns = list(range(1, ncols+1))

    return df

def save_dataframe(df, filepath):
    # replace blanc -> 0, neg -> -1, pos -> 1
    df = df.replace('BLANC','0', regex=True)
    df = df.replace('NEG','-1', regex=True)
    df = df.replace('POS','1', regex=True)
    # replace O with 0
    df = df.replace('O','0', regex=True)
    # change everything to float
    df = df.astype(np.float64)
    df.to_parquet(filepath)


def convert_to_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
       df.to_excel(writer)
    return buffer
