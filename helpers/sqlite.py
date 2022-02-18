import sqlite3
from helpers import bgsapi


def monitoredsystems():
    """this method returns the current list of monitored systems"""
    # Replace this with sql logic to get monitored systems later
    monitored = ['Arque', 'Zaonce', 'Teorge', 'Tianve', 'Tionisla', 'Neganhot', 'Orrere', 'Oguninksmii']
    return monitored


def create_conn(location):
    try:
        conn = sqlite3.connect(location)
        c = conn.cursor()
        return conn, c
    except sqlite3.OperationalError:
        return None, None


def initialize_tables(c):
    try:
        c.execute("""CREATE TABLE monitoredsystems (
                        system_id text,
                        eddb_id integer,
                        system_name text,
                        x real,
                        y real,
                        z real
                        )""")
    except sqlite3.OperationalError:
        print("ERROR IN initialize_tables()")
        pass


def add_system(c, name):
    query = "INSERT INTO monitoredsystems VALUES ({})".format(name)
    try:
        c.execute(query)
    except sqlite3.OperationalError:
        print("ERROR IN add_system()")
        pass


def get_data(c):
    try:
        c.execute("SELECT * FROM monitoredsystems")
        print(c.fetchall())
    except sqlite3.OperationalError:
        print("ERROR IN get_data()")
        pass
