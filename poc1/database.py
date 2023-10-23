import streamlit as st
import sqlite3
import pathlib
import contextlib

basedir = pathlib.Path(__file__).parent.parent
datadir = basedir / "data"
database_path = basedir / "database.sqlite"


@st.cache_resource
def init_connection(database_path):
    con = sqlite3.connect(database_path, check_same_thread=False)
    # con.row_factory = dict_factory
    if "con" not in st.session_state:
        st.session_state.con = con
    return con

@st.cache_resource
def create_plate_types_table():
    con = st.session_state.con
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("""
        create table if not exists plate_types(
        eid integer primary key,
        type varchar(50) not null,
        nb_cols integer not null,
        col_names varchar(50) not null, -- letters of numbers
        nb_rows integer not null,
        row_names varchar(50) not null, -- letters of numbers
        nb_whites integer not null,
        nb_pos integer not null,
        nb_negs integer not null,
        nb_wells integer GENERATED ALWAYS AS (nb_cols * nb_rows),
        nb_patient_wells integer GENERATED ALWAYS AS ((nb_cols * nb_rows) - (nb_pos+nb_negs+nb_whites)),
        created varchar(50) not null
        );
        """)
        con.commit()

@st.cache_resource
def create_plates_table():
    con = st.session_state.con
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("""
        create table if not exists plates(
        eid integer primary key,
        type integer not null,
        status text check(status IN ('empty','filled','processed')) NOT NULL DEFAULT 'empty',
        wells_for_whites text not null,
        wells_for_pos text not null,
        wells_for_negs text not null
        );
        """)
        con.commit()


def insert_plate_type(con, params):
    query = """
    insert into plate_types (type, nb_cols, col_names, nb_rows, row_names, nb_whites, nb_pos, nb_negs, created)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with contextlib.closing(con.cursor()) as cur:
        cur.execute(query, params)
        con.commit()

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def list_plate_types(row_factory=None):
    con = st.session_state.con
    if row_factory:
        con.row_factory = row_factory
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("select eid, type from plate_types")
        return cur.fetchall()
