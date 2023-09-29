import streamlit as st

def run():
    st.set_page_config(
        page_title="Home page",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items=None,
    )
    st.write("# Welcome to IPD")

if __name__ == "__main__":
    run()
