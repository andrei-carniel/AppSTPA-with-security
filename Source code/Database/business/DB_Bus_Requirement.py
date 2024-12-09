import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Database.performance import DB_Bus_Pef_Requirement
from Objects.Business.Business import Business


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
    sql_query = "CREATE TABLE bus_requirement (id INTEGER PRIMARY KEY AUTOINCREMENT, requirement TEXT, mechanism TEXT, id_component INTEGER, id_project INTEGER, performance_req TEXT, " \
                "FOREIGN KEY(id_component) REFERENCES components(id), " \
                "FOREIGN KEY(id_project) REFERENCES project(id))"

    return sql_query

# insert many registers to Table Things
def insert_to_db(requirement, mechanism, id_component, id_project, performance_req):
    # create a database connection
    try:
        conn = create_connection()
        with conn:
            cur = conn.cursor()

            sql = "INSERT OR REPLACE INTO bus_requirement(requirement, mechanism, id_component, id_project, performance_req) VALUES(?, ?, ?, ?, ?)"
            cur.execute(sql, (requirement, mechanism, id_component, id_project, performance_req))

            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)

def update(id, requirement, mechanism, performance_req):
    conn = create_connection()
    with conn:
        sql = "UPDATE bus_requirement SET requirement = ?, mechanism = ?, performance_req = ? WHERE id = ?"
        cur = conn.cursor()
        task = (requirement, mechanism, performance_req, id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def delete(id):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM pef_bus_res_requirement WHERE id_bus_requirement = ?", (id,))
        cur.execute("DELETE FROM bus_requirement WHERE id = ?", (id,))
        conn.commit()
        return cur.lastrowid

def load_business_requirement(id_component, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT DISTINCT br.id, br.requirement, br.mechanism, br.id_project, br.id_component, c.name, br.performance_req " \
              "FROM bus_requirement AS br " \
			  "JOIN components AS c ON c.id = br.id_component " \
              "WHERE br.id_component = ? AND br.id_project = ?"
        cur.execute(sql, (id_component, id_project,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Business(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return result_list

def load_business_requirement_by_resource(id_component, id_project, id_resource):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT DISTINCT br.id, br.requirement, br.mechanism, br.id_project, br.id_component, c.name, br.performance_req " \
              "FROM bus_requirement AS br " \
			  "JOIN components AS c ON c.id = br.id_component " \
              "WHERE br.id_component = ? AND br.id_project = ?"
        cur.execute(sql, (id_component, id_project,))
        rows = cur.fetchall()

        for row in rows:
            cur.execute("SELECT count(id) FROM pef_bus_res_requirement WHERE id_bus_requirement = ? AND id_resource = ?", (row[0], id_resource))
            row_count = cur.fetchone()

            if row_count != None:
                if row_count[0] > 0:
                    result_list.append(Business(row[0], row[1], row[2], row[3], row[4], row[5], row[6], DB_Bus_Pef_Requirement.select_by_requirement_without_connection(cur, row[0], id_resource)))

    return result_list