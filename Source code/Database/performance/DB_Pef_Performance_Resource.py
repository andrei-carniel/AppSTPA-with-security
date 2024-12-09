import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Objects.Performance.Pef_Requirement import Pef_Resource


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(Constant.DB_FILE)
    except Error as e:
        print(e)

    return conn

def create_table():
    sql_query = "CREATE TABLE IF NOT EXISTS pef_resource (id INTEGER NOT NULL, name TEXT NOT NULL, onto_name TEXT NOT NULL, PRIMARY KEY(id));"
    return sql_query

# insert the default data on stride
def insert_into(conn):
    sql = "INSERT OR REPLACE INTO pef_resource (id, name, onto_name) VALUES(?, ?, ?)"

    rsql1 = insert_to_db(conn, sql, (Constant.DB_ID_APPLICATION, Constant.DB_NAME_APPLICATION, Constant.PEF_APPLICATION))
    rsql2 = insert_to_db(conn, sql, (Constant.DB_ID_INTERFACE_I_O, Constant.DB_NAME_INTERFACE_I_O, Constant.PEF_INTERFACE_I_O))
    rsql3 = insert_to_db(conn, sql, (Constant.DB_ID_MEMORY, Constant.DB_NAME_MEMORY, Constant.PEF_MEMORY))
    rsql4 = insert_to_db(conn, sql, (Constant.DB_ID_OPERATING_SYSTEM, Constant.DB_NAME_OPERATING_SYSTEM, Constant.PEF_OPERATING_SYSTEM))
    rsql5 = insert_to_db(conn, sql, (Constant.DB_ID_PHYSICAL_LINK, Constant.DB_NAME_PHYSICAL_LINK, Constant.PEF_PHYSICAL_LINK))
    rsql6 = insert_to_db(conn, sql, (Constant.DB_ID_PROCESSOR, Constant.DB_NAME_PROCESSOR, Constant.PEF_PROCESSOR))
    rsql7 = insert_to_db(conn, sql, (Constant.DB_ID_STORAGE, Constant.DB_NAME_STORAGE, Constant.PEF_STORAGE))

# insert many registers to Table Things
def insert_to_db(conn, sql, task):
    # create a database connection
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(sql, task)
            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)


# select action name
def select_all():
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, onto_name FROM pef_resource")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Pef_Resource(row[0], row[1]))

    return result_list

# select action name
def select_onto_name(id_element):
    result = ""

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT onto_name FROM pef_resource WHERE id = ?", (id_element))

        row = cur.fetchone()

        if row != None:
            result = row[0]

    return result
