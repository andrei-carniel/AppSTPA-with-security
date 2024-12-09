import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Objects.security.Stride_Requirement import Stride_Requirement_imported


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
    sql_query = "CREATE TABLE sec_stride_requirement_import (id INTEGER PRIMARY KEY AUTOINCREMENT, id_link INTEGER NOT NULL, id_req_imported INTEGER NOT NULL, " \
                "FOREIGN KEY(id_link) REFERENCES components_links(id), " \
                "FOREIGN KEY(id_req_imported) REFERENCES sec_stride_requirement(id))"

    return sql_query

def insert(id_link, id_req_imp):
    # create a database connection
    try:
        conn = create_connection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM sec_stride_requirement_import WHERE id_link = ? AND id_req_imported = ?", (id_link, id_req_imp,))
            row_l = cur.fetchone()
            if row_l != None:
                return -1

            sql = "INSERT OR REPLACE INTO sec_stride_requirement_import(id_link, id_req_imported) VALUES(?, ?)"
            cur.execute(sql, (id_link, id_req_imp))
            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)

def delete(id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM sec_stride_requirement_import WHERE id = ?", (id,))
        conn.commit()
        return cur.lastrowid

def delete_link_req(id_link, id_req_imp):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM sec_stride_requirement_import WHERE id_link = ? AND id_req_imported = ?", (id_link, id_req_imp,))
        conn.commit()
        return cur.lastrowid

# select action name
def select_by_id_req(id_req):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id, id_link, id_req_imported FROM sec_stride_requirement_import")

        rows = cur.fetchall()

        for row in rows:
            result_list.append(Stride_Requirement_imported(row[0], row[1], row[2]))

    return result_list

def select_links_with_id_req(id_req):
    # create a database connection
    result = ""
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT si.id_link, cs.name, cd.name FROM sec_stride_requirement_import AS si "
                    "JOIN components_links AS cl ON si.id_link = cl.id "
                    "JOIN components AS cs ON cl.id_component_src = cs.id "
                    "JOIN components AS cd ON cl.id_component_dst = cd.id "
                    "WHERE id_req_imported = ?", (id_req,))

        rows = cur.fetchall()

        for row in rows:
            if result != "":
                result += "\n"
            result += row[1] + " -> " + row[2]

    if result == "":
        result = "None link"

    return result

def select_links_with_id_req_except(id_req, id_current_link):
    # create a database connection
    result = ""
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT si.id_link, cs.name, cd.name FROM sec_stride_requirement_import AS si "
                    "JOIN components_links AS cl ON si.id_link = cl.id "
                    "JOIN components AS cs ON cl.id_component_src = cs.id "
                    "JOIN components AS cd ON cl.id_component_dst = cd.id "
                    "WHERE id_req_imported = ? AND si.id_link <> ?", (id_req, id_current_link,))

        rows = cur.fetchall()

        for row in rows:
            if result != "":
                result += "\n"
            result += row[1] + " -> " + row[2]

    if result == "":
        result = "None link"

    return result
