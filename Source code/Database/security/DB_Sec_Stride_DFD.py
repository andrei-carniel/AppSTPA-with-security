import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Objects.security.Stride_DFD import Stride_DFD


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
    sql_query = "CREATE TABLE IF NOT EXISTS sec_stride_dfd (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);"

    return sql_query

# insert the default data on stride
def insert_stride(conn):
    sql = "INSERT OR REPLACE INTO sec_stride_dfd(id, name) VALUES(?, ?)"

    rsql1 = insert_to_db(conn, sql, (Constant.DB_ID_EXTERNAL_ENTITY, Constant.SEC_IS_EXTERNAL_ENTITY_NAME))
    rsql2 = insert_to_db(conn, sql, (Constant.DB_ID_DATA_FLOW, Constant.SEC_IS_DATA_FLOW_NAME))
    rsql3 = insert_to_db(conn, sql, (Constant.DB_ID_DATA_STORE, Constant.SEC_IS_DATA_STORE_NAME))
    rsql4 = insert_to_db(conn, sql, (Constant.DB_ID_PROCESS, Constant.SEC_IS_PROCESS_NAME))

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
        cur.execute("SELECT id, name FROM sec_stride_dfd")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Stride_DFD(row[0], row[1]))

    return result_list
