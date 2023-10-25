import streamlit as st
from database import list_patients, list_plate_types

# I should probably define the same thing but for other types of plates plan
well_names = [
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12",
    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12",
    "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11", "H12",
]

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
        names_cols = st.selectbox("Columns naming scheme",
                                  ("Letters", "Numbers"),
                                  index=None,
                                  placeholder="How to name the columns?",
                                  label_visibility="collapsed")
        names_rows = st.selectbox("Rows naming scheme",
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
            wells_whites = st.multiselect("Location for whites",
                                          options=well_names,
                                          placeholder="Locations for whites",
                                          max_selections=nb_whites,
                                          label_visibility="collapsed")

            wells_pos = st.multiselect("Location for positives",
                                       options=well_names,
                                       placeholder="Locations for positives",
                                       max_selections=nb_pos,
                                       label_visibility="collapsed")
            wells_negs = st.multiselect("Location for negatives",
                                        options=well_names,
                                        placeholder="Location for for negatives",
                                        max_selections=nb_negs,
                                        label_visibility="collapsed")
    return (type_, nb_cols, nb_rows,
            names_cols, names_rows,
            nb_whites, nb_pos, nb_negs,
            wells_whites, wells_pos, wells_negs)

def plate_form():
    plate_types = dict(list_plate_types())
    type_ = st.selectbox("Type of the plate",
                         options=plate_types,
                         format_func=lambda key: plate_types[key],
                         index=None,
                         placeholder="The type for your plate ?",
                         label_visibility="collapsed")
    # # I should retrieve the max_nb_patients the plan can take
    # # info available with the type of plate
    # patients = st.multiselect("Patients",
    #                           options=patients,
    #                           format_func=lambda key:patients[key],
    #                           placeholder="Add patients",
    #                           label_visibility="collapsed")
    return type_
