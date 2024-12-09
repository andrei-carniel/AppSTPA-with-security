import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Objects.Performance.Pef_Requirement import Saf_Pef_UCA, Pef_Saf_Resource, Sec_Pef_UCA, Pef_Sec_Resource
from Objects.security.Stride_Requirement import Stride_Requirement


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
    sql_query = "CREATE TABLE pef_sec_res_requirement (id INTEGER PRIMARY KEY AUTOINCREMENT, requirement TEXT, id_sec_requirement INTEGER, id_component INTEGER, " \
                "id_resource INTEGER, id_project INTEGER, " \
                "FOREIGN KEY(id_sec_requirement) REFERENCES sec_stride_requirement(id), " \
                "FOREIGN KEY(id_component) REFERENCES components(id), " \
                "FOREIGN KEY(id_resource) REFERENCES pef_resource(id), " \
                "FOREIGN KEY(id_project) REFERENCES project(id))"

    return sql_query

# insert many registers to Table Things
def insert_to_db(requirement, id_sec_requirement, id_resource, id_project, id_component):
    # create a database connection
    try:
        conn = create_connection()
        with conn:
            cur = conn.cursor()

            sql = "INSERT OR REPLACE INTO pef_sec_res_requirement(requirement, id_sec_requirement, id_resource, id_project, id_component) VALUES(?, ?, ?, ?, ?)"
            cur.execute(sql, (requirement, id_sec_requirement, id_resource, id_project, id_component))

            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)

def update(id, requirement):
    conn = create_connection()
    with conn:
        sql = "UPDATE pef_sec_res_requirement SET requirement = ? WHERE id = ?"
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
        cur.execute("DELETE FROM pef_sec_res_requirement WHERE id = ?", (id,))
        conn.commit()
        return cur.lastrowid

def load_sec_pef_priority():
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT id, name FROM sec_stride_priority"
        cur.execute(sql, ())
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Sec_Pef_UCA(row[0], row[1]))

    return result_list

def select_by_controller(id_controller, id_priority):
        result_list = []

        # create a database connection
        conn = create_connection()
        with conn:
            cur = conn.cursor()
            sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, c.name, ssr.id_link, " \
                  "ssr.id_dfd, ssd.name, ssr.id_stride, ss.name, ssr.performance_req " \
                  "FROM sec_stride_requirement AS ssr " \
                  "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
                  "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
                  "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
                  "JOIN components AS c ON ssr.id_component = c.id " \
                  "JOIN components_links AS cl ON cl.id = ssr.id_link " \
                  "WHERE ssr.id_component = ? AND ssr.id_priority = ?"
            cur.execute(sql, (id_controller, id_priority,))
            rows = cur.fetchall()

            for row in rows:
                result_list.append(Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                       row[10], row[11], row[12], row[13], False, True, [], row[14]))

            sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, ssr.id_link, ssr.id_dfd, " \
                  "ssd.name, ssr.id_stride, ss.name, ssr.performance_req " \
                  "FROM sec_stride_requirement AS ssr " \
                  "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
                  "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
                  "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
                  "JOIN components_links AS cl ON cl.id = ssr.id_link " \
                  "WHERE (cl.id_component_dst = ? OR cl.id_component_src = ?) AND ssr.id_component IS NULL AND ssr.id_priority = ?"
            cur.execute(sql, (id_controller, id_controller, id_priority,))
            rows = cur.fetchall()

            sql_link_name = "SELECT DISTINCT cs.name, cd.name FROM components_links AS cl " \
                            "JOIN components AS cs ON cl.id_component_src = cs.id " \
                            "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                            "WHERE cl.id = ?"
            for row in rows:
                name_link = ""
                cur.execute(sql_link_name, (row[8],))
                row_l = cur.fetchone()
                if row_l != None:
                    name_link = row_l[0] + " -> " + row_l[1]

                result_list.append(Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], name_link,
                                       row[8], row[9], row[10], row[11], row[12], False, False, [], row[13]))

        return result_list


def select_by_controller_resource(id_controller, id_resource):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, c.name, ssr.id_link, " \
              "ssr.id_dfd, ssd.name, ssr.id_stride, ss.name, ssr.performance_req " \
              "FROM sec_stride_requirement AS ssr " \
              "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
              "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
              "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
              "JOIN components AS c ON ssr.id_component = c.id " \
              "JOIN components_links AS cl ON cl.id = ssr.id_link " \
              "WHERE cl.id_component_dst = ? AND ssr.id_component = ?"
        cur.execute(sql, (id_controller, id_controller,))
        rows = cur.fetchall()

        for row in rows:
            cur.execute("SELECT count(id) FROM pef_sec_res_requirement WHERE id_sec_requirement = ? AND id_resource = ?", (row[0], id_resource))
            row_count = cur.fetchone()

            if row_count != None:
                if row_count[0] > 0:
                    obj = Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                                          row[10], row[11], row[12], row[13], False, True, [], row[14])
                    obj.list_res = select_by_requirement_without_connection(cur, row[0], id_resource)
                    result_list.append(obj)

        sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, ssr.id_link, ssr.id_dfd, " \
              "ssd.name, ssr.id_stride, ss.name, ssr.performance_req " \
              "FROM sec_stride_requirement AS ssr " \
              "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
              "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
              "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
              "JOIN components_links AS cl ON cl.id = ssr.id_link " \
              "WHERE (cl.id_component_dst = ? OR cl.id_component_src = ?) AND ssr.id_component IS NULL "
        cur.execute(sql, (id_controller, id_controller,))
        rows = cur.fetchall()

        sql_link_name = "SELECT DISTINCT cs.name, cd.name FROM components_links AS cl " \
                        "JOIN components AS cs ON cl.id_component_src = cs.id " \
                        "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                        "WHERE cl.id = ?"
        for row in rows:
            cur.execute("SELECT count(id) FROM pef_sec_res_requirement WHERE id_sec_requirement = ? AND id_resource = ?", (row[0], id_resource))
            row_count = cur.fetchone()

            if row_count != None:
                if row_count[0] > 0:
                    name_link = ""
                    cur.execute(sql_link_name, (row[8],))
                    row_l = cur.fetchone()
                    if row_l != None:
                        name_link = row_l[0] + " -> " + row_l[1]

                    obj = Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], name_link, row[8], row[9],
                                                          row[10], row[11], row[12], False, False, [], row[13])
                    obj.list_res = select_by_requirement_without_connection(cur, row[0], id_resource)
                    result_list.append(obj)

    return result_list

def select_by_requirement(id_sec_requirement):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT srr.id, srr.requirement, srr.id_sec_requirement, srr.id_component, srr.id_resource, srr.id_project, c.name, r.name " \
              "FROM pef_sec_res_requirement AS srr " \
              "JOIN components AS c ON c.id = srr.id_component " \
              "JOIN pef_resource AS r ON r.id = srr.id_resource " \
              "WHERE srr.id_sec_requirement = ?"
        cur.execute(sql, (id_sec_requirement,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Pef_Sec_Resource(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return result_list

def select_by_requirement_without_connection(cur, id_sec_requirement, id_resource):
    result_list = []

    try:
        sql = "SELECT srr.id, srr.requirement, srr.id_sec_requirement, srr.id_component, srr.id_resource, srr.id_project, c.name, r.name " \
              "FROM pef_sec_res_requirement AS srr " \
              "JOIN components AS c ON c.id = srr.id_component " \
              "JOIN pef_resource AS r ON r.id = srr.id_resource " \
              "WHERE srr.id_sec_requirement = ? AND srr.id_resource = ?"
        cur.execute(sql, (id_sec_requirement, id_resource,))
        rows = cur.fetchall()

        for row in rows:
            result_list.append(Pef_Sec_Resource(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return result_list
    except Exception as e:
        return result_list