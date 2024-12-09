import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Objects.Performance.Pef_Requirement import Saf_Pef_UCA, Pef_Saf_Resource, Pef_Bus_Resource


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
    sql_query = "CREATE TABLE pef_bus_res_requirement (id INTEGER PRIMARY KEY AUTOINCREMENT, requirement TEXT, id_bus_requirement INTEGER, id_component INTEGER, " \
                "id_resource INTEGER, id_project INTEGER, " \
                "FOREIGN KEY(id_bus_requirement) REFERENCES bus_requirement(id), " \
                "FOREIGN KEY(id_component) REFERENCES components(id), " \
                "FOREIGN KEY(id_resource) REFERENCES pef_resource(id), " \
                "FOREIGN KEY(id_project) REFERENCES project(id))"

    return sql_query

# insert many registers to Table Things
def insert_to_db(requirement, id_bus_requirement, id_resource, id_project, id_component):
    # create a database connection
    try:
        conn = create_connection()
        with conn:
            cur = conn.cursor()

            sql = "INSERT OR REPLACE INTO pef_bus_res_requirement(requirement, id_bus_requirement, id_resource, id_project, id_component) VALUES(?, ?, ?, ?, ?)"
            cur.execute(sql, (requirement, id_bus_requirement, id_resource, id_project, id_component))

            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)

def update(id, requirement):
    conn = create_connection()
    with conn:
        sql = "UPDATE pef_bus_res_requirement SET requirement = ? WHERE id = ?"
        cur = conn.cursor()
        task = (requirement, id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def delete(id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM pef_bus_res_requirement WHERE id = ?", (id,))
        conn.commit()
        return cur.lastrowid

def select_by_requirement(id_bus_requirement):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT srr.id, srr.requirement, srr.id_bus_requirement, srr.id_component, srr.id_resource, srr.id_project, c.name, r.name " \
              "FROM pef_bus_res_requirement AS srr " \
              "JOIN components AS c ON c.id = srr.id_component " \
              "JOIN pef_resource AS r ON r.id = srr.id_resource " \
              "WHERE srr.id_bus_requirement = ?"
        cur.execute(sql, (id_bus_requirement,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Pef_Bus_Resource(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return result_list

def select_by_requirement_without_connection(cur, id_bus_requirement, id_resource):
    result_list = []

    try:
        sql = "SELECT srr.id, srr.requirement, srr.id_bus_requirement, srr.id_component, srr.id_resource, srr.id_project, c.name, r.name " \
              "FROM pef_bus_res_requirement AS srr " \
              "JOIN components AS c ON c.id = srr.id_component " \
              "JOIN pef_resource AS r ON r.id = srr.id_resource " \
              "WHERE srr.id_bus_requirement = ? AND srr.id_resource = ?"
        cur.execute(sql, (id_bus_requirement, id_resource,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Pef_Bus_Resource(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return result_list
    except Exception as e:
        return result_list