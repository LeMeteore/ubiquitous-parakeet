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
    con.execute("PRAGMA foreign_keys = 1")
    # con.row_factory = dict_factory

    # create one table plate_types
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("""
        create table if not exists plate_types(
        eid integer primary key,
        type varchar(50) not null,
        nb_cols integer not null,
        nb_rows integer not null,

        names_cols varchar(50) not null, -- letters of numbers
        names_rows varchar(50) not null, -- letters of numbers

        nb_whites integer not null,
        nb_pos integer not null,
        nb_negs integer not null,

        wells_whites text not null,
        wells_pos text not null,
        wells_negs text not null,

        nb_wells integer GENERATED ALWAYS AS (nb_cols * nb_rows),
        nb_patient_wells integer GENERATED ALWAYS AS ((nb_cols * nb_rows) - (nb_pos+nb_negs+nb_whites)),


        created varchar(50) not null
        );
        """)
        con.commit()

    # create second table plate plans
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("""
        create table if not exists plates(
        eid integer primary key,
        type_eid integer not null,
        description text not null, -- a little description to help recognize the plate
        status text check(status IN ('empty','filled','processed')) NOT NULL DEFAULT 'empty',
        created varchar(50) not null,
        FOREIGN KEY(type_eid) REFERENCES plate_types(eid)
        );
        """)
        con.commit()

    # create patients table
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("""
        create table if not exists patients(
        eid integer primary key,
        firstname varchar(50) not null,
        lastname varchar(50) not null,
        age integer not null,
        sex varchar(50) not null,
        created varchar(50) not null
        );
        """)
        con.commit()

    # create patients table
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("""
        create table if not exists plate_patients(
        eid integer primary key,
        plate_eid integer not null,
        patient_eid integer not null,
        FOREIGN KEY(plate_eid) REFERENCES plates(eid),
        FOREIGN KEY(patient_eid) REFERENCES patients(eid)
        );
        """)
        con.commit()

    return con

def insert_plate_type(con, params):
    query = """
    insert into plate_types (
    type, nb_cols, nb_rows,
    names_cols, names_rows,
    nb_whites, nb_pos, nb_negs,
    wells_whites, wells_pos, wells_negs,
    created)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

def list_patients(row_factory=None):
    con = st.session_state.con
    if row_factory:
        con.row_factory = row_factory
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("select eid, firstname || ' ' || lastname as fullname from patients")
        return cur.fetchall()

def list_empty_plates(row_factory=None):
    con = st.session_state.con
    if row_factory:
        con.row_factory = row_factory
    with contextlib.closing(con.cursor()) as cur:
        cur.execute("select eid, description from plates where status is 'empty'")
        return cur.fetchall()

def insert_plate(con, params):
    first_query = """
    insert into plates(
    type_eid,
    description,
    status,
    created)
    values (?, ?, ?, ?)
    """
    with contextlib.closing(con.cursor()) as cur:
        cur.execute(first_query, params)
        con.commit()

if __name__ == "__main__":
    init_connection(database_path)
