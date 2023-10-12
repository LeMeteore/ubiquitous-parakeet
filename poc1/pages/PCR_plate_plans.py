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

st.write("### PCR plate plans management")

create_tab, list_tab = st.tabs(["Create", "List"])

with create_tab:
    st.header("PCR plate plan creation")

with list_tab:
    st.header("PCR plate plan list")
