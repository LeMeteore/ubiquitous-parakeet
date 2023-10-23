import streamlit as st

def plate_type_form():
    type_ = st.text_input("Type of the plate",
                          placeholder="Type of the plate",
                          label_visibility="collapsed")
    col1, col2 = st.columns(2)
    with col1:
        nb_cols = st.number_input("Number of columns",
                                step=1, min_value=1,
                                value=None,
                                placeholder="Number of columns",
                                label_visibility="collapsed")
        nb_rows = st.number_input("Number of rows",
                                step=1, min_value=1,
                                value=None,
                                placeholder="Number of rows",
                                label_visibility="collapsed")
    with col2:
        col_names = st.selectbox("Columns naming scheme",
                                          ("Letters", "Numbers"),
                                          index=None,
                                          placeholder="How to name the columns?",
                                          label_visibility="collapsed")
        row_names = st.selectbox("Rows naming scheme",
                                          ("Letters", "Numbers"),
                                          index=None,
                                          placeholder="How to name the rows?",
                                          label_visibility="collapsed")


    col4, col5 = st.columns([1,3])
    with col4:
        nb_whites = st.number_input("Number of whites",
                                  step=1, min_value=1,
                                  value=None,
                                  placeholder="Number of whites",
                                  label_visibility="collapsed")
        nb_pos = st.number_input("Number of positives",
                               step=1, min_value=1,
                               value=None,
                               placeholder="Number of positives",
                               label_visibility="collapsed")
        nb_negs = st.number_input("Number of negatives",
                                step=1, min_value=1,
                                value=None,
                                placeholder="Number of negatives",
                                label_visibility="collapsed")
        with col5:
            options = ["foo", "bar", "baz", "corge"]
            white_wells = st.multiselect("Location for whites",
                                         options=options,
                                         placeholder="Locations for whites",
                                         max_selections=nb_whites,
                                         label_visibility="collapsed")

            pos_wells = st.multiselect("Location for positives",
                                      options=options,
                                      placeholder="Locations for positives",
                                      max_selections=nb_pos,
                                      label_visibility="collapsed")
            neg_wells = st.multiselect("Location for negatives",
                                      options=options,
                                      placeholder="Location for for negatives",
                                      max_selections=nb_negs,
                                      label_visibility="collapsed")
    return type_, nb_cols, col_names, nb_rows, row_names, nb_whites, nb_pos, nb_negs
