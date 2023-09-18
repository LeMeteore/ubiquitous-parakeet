import re
import streamlit as st

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
