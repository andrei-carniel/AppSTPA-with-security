import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Objects.security.Stride import Stride


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


# return the sql query for components
def create_table():
    sql_query = "CREATE TABLE IF NOT EXISTS sec_stride (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);"

    return sql_query


# insert the default data on stride
def insert_stride(conn):
    sql = "INSERT OR REPLACE INTO sec_stride(id, name) VALUES(?, ?)"

    rsql1 = insert_to_db(conn, sql, (Constant.DB_ID_SPOOFING, Constant.DB_NAME_SPOOFING))
    rsql2 = insert_to_db(conn, sql, (Constant.DB_ID_TAMPERING, Constant.DB_NAME_TAMPERING))
    rsql3 = insert_to_db(conn, sql, (Constant.DB_ID_REPUDIATION, Constant.DB_NAME_REPUDIATION))
    rsql4 = insert_to_db(conn, sql, (Constant.DB_ID_INFORMATION_DISCLOSURE, Constant.DB_NAME_INFORMATION_DISCLOSURE))
    rsql5 = insert_to_db(conn, sql, (Constant.DB_ID_DENIAL_OF_SERVICE, Constant.DB_NAME_DENIAL_OF_SERVICE))
    rsql6 = insert_to_db(conn, sql, (Constant.DB_ID_ELEVATION_OF_PRIVILEGE, Constant.DB_NAME_ELEVATION_OF_PRIVILEGE))


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
        cur.execute("SELECT id, name FROM sec_stride")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Stride(row[0], row[1]))

    return result_list
