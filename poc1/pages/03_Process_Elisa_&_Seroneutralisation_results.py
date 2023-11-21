import pandas as pd
import streamlit as st
import pathlib
import io
import altair as alt
import math
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

basedir = pathlib.Path(__file__).parent.parent.parent
datadir = basedir / "data"

st.set_page_config(
   page_title="Process ELISA & seroneutralisation results",
   layout="wide",
   initial_sidebar_state="collapsed",
   menu_items=None,
)

multi = '''## Processing of ELISA & seroneutralisation tests results

First, upload an Excel file containing your PCR plate plan. Next, upload the Excel file containing the results. The files should respect the following formats:
'''
st.markdown(multi)

# example_input = pd.DataFrame(
#     data = [[id_generator() for _ in range(12)] for _ in range(8)],
#     columns=range(1,13),
#     index=[x for x in string.ascii_uppercase[:8]]
# )

# st.dataframe(example_input)
# Initialize session state
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
