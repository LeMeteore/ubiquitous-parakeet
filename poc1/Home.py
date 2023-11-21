import streamlit as st
from database import init_connection, database_path

st.set_page_config(
    page_title="Home page",
    layout="wide",
    menu_items=None,
)

if "con" not in st.session_state:
    con = init_connection(database_path)
    st.sesstion_state = con

def run():
    st.write("# Welcome :scientist:")

    multi = '''
This is a proof of concept built _specifically_ for the scientists at the immunology lab to help them for the management of their [PCR plate plans](#).

The primary objective is, for each performed test, map **the results** returned by the spectrophotometer, to **the samples** contained inside the PCR plate plans.

Keep in mind, the software is :red[still a work in progress], the software should not be released to the public yet.

To find more informations, please, follow this [link](#)
    '''
    st.markdown(multi)

if __name__ == "__main__":
    run()
