import pandas as pd
import streamlit as st
import pathlib
import io
import altair as alt
import math
import string, random

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

st.set_page_config(
   page_title="Process Waitan results",
   layout="wide",
   initial_sidebar_state="collapsed",
   menu_items=None,
)

multi = '''## Processing of Waitan tests results

First, upload an Excel file containing your PCR plate plan. Next, upload the Excel file containing the results. The files should respect the following formats:


'''
st.markdown(multi)

if "files_uploaded" not in st.session_state:
   st.session_state["files_uploaded"] = False


with st.form("my_form", clear_on_submit=True):
   col1, col2 = st.columns(2)
   with col1:
       input_file = st.file_uploader(
          "Input file",
          type=["xls", "xlsx"],
          help="Enter an Excel file containing your plate, the file should have a worksheet named 'Plan de plaque'."
       )
   with col2:
       output_file = st.file_uploader(
          "Output file",
          type=["xls", "xlsx"],
          help="Enter an Excel file containing results returned by the Spectrometer, the file should have a worksheet named '???'."
       )
   submit_button_form = st.form_submit_button("Submit file")
   if submit_button_form:
       pass


with st.expander("See plot"):
    pass

with st.expander("See Tabular datas"):
    pass
