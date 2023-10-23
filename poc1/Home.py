import streamlit as st
from database import init_connection, database_path

st.set_page_config(
    page_title="Home page",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

if "con" not in st.session_state:
    con = init_connection(database_path)
    st.sesstion_state = con

def run():
    st.write("# Welcome :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

    multi = '''This is a proof of concept built to help for the management of [PCR plate plans](#).


Keep in mind, this is a :red[pre-alpha version], the software is :red[still being designed and built], the software should not be released to the public yet.

To find more informations, please, follow this [link](#)
    '''
    st.markdown(multi)

if __name__ == "__main__":
    run()
