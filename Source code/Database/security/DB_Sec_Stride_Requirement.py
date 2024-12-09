import sqlite3
from sqlite3 import Error
import Constant


# make a connection
from Objects.security.Stride import Stride
from Objects.security.Stride_Requirement import Stride_Requirement
from Objects.security.Stride_control import Stride_control


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
    sql_query = "CREATE TABLE sec_stride_requirement (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, justification TEXT, " \
                "id_priority INTEGER NOT NULL, id_component INTEGER, id_link INTEGER NOT NULL, id_dfd INTEGER NOT NULL, id_stride INTEGER NOT NULL, " \
                "id_project INTEGER NOT NULL, " \
                "FOREIGN KEY(id_project) REFERENCES projects(id) " \
                "FOREIGN KEY(id_dfd) REFERENCES sec_stride_dfd(id), " \
                "FOREIGN KEY(id_link) REFERENCES components_links(id), " \
                "FOREIGN KEY(id_component) REFERENCES components(id), " \
                "FOREIGN KEY(id_priority) REFERENCES sec_stride_priority(id), " \
                "FOREIGN KEY(id_stride) REFERENCES sec_stride(id))"

    return sql_query

# insert many registers to Table Things
def insert_to_db(title, description, justification, mechanism, id_priority, id_component, id_link, id_dfd, id_stride, id_project, control_text):
    # create a database connection
    try:
        conn = create_connection()
        with conn:
            cur = conn.cursor()

            if id_component == -1:
                sql = "INSERT OR REPLACE INTO sec_stride_requirement(title, description, justification, id_priority, id_link, id_dfd, id_stride, id_project, mechanism, control) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(sql, (title, description, justification, id_priority, id_link, id_dfd, id_stride, id_project, mechanism, control_text))
            else:
                sql = "INSERT OR REPLACE INTO sec_stride_requirement(title, description, justification, id_priority, id_component, id_link, id_dfd, id_stride, id_project, mechanism, control) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(sql, (title, description, justification, id_priority, id_component, id_link, id_dfd, id_stride, id_project, mechanism, control_text))
            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(e)

def update(id, title, description, justification, mechanism, priority, control_text, performance_req):
    conn = create_connection()
    with conn:
        sql = "UPDATE sec_stride_requirement SET title = ?, description = ?, justification = ?, mechanism = ?, id_priority = ?, control = ?, performance_req = ? WHERE id = ?"
        cur = conn.cursor()
        task = (title, description, justification, mechanism, priority, control_text, performance_req, id)
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

def delete(id_rec):
    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM sec_stride_requirement_import WHERE id_req_imported = ?", (id_rec,))
        cur.execute("DELETE FROM pef_sec_res_requirement WHERE id_sec_requirement = ?", (id_rec,))
        cur.execute("DELETE FROM sec_stride_requirement WHERE id = ?", (id_rec,))
        conn.commit()
        return cur.lastrowid

def list_control_organizer(control_text):
    list_of_controls = []

    if len(control_text) < 2:
        return list_of_controls

    for ctrl in control_text.split(";"):
        list_of_controls.append(Stride_control(ctrl, True))
    return list_of_controls

def select_by_id_link(id_link):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, c.name, ssr.id_link, " \
              "ssr.id_dfd, ssd.name, ssr.id_stride, ss.name, ssr.control, ssr.performance_req " \
              "FROM sec_stride_requirement AS ssr " \
              "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
              "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
              "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
              "JOIN components AS c ON ssr.id_component = c.id " \
              "WHERE ssr.id_link = ? ORDER BY ssr.id_stride"
        cur.execute(sql, (id_link,))
        rows = cur.fetchall()

        for row in rows:
            list_of_controls = list_control_organizer(row[14])
            result_list.append(Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], False, True, list_of_controls, row[15]))


        sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, ssr.id_link, ssr.id_dfd, " \
              "ssd.name, ssr.id_stride, ss.name, ssr.control, ssr.performance_req " \
              "FROM sec_stride_requirement AS ssr " \
              "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
              "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
              "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
              "WHERE ssr.id_link = ? AND ssr.id_component IS NULL ORDER BY ssr.id_stride"
        cur.execute(sql, (id_link,))
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

            list_of_controls = list_control_organizer(row[13])
            result_list.append(Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], name_link, row[8], row[9], row[10], row[11], row[12], False, False, list_of_controls, row[14]))

    return result_list

def select_by_id_component(id_comp, id_link):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, ssr.id_link, ssr.id_dfd, " \
              "ssd.name, ssr.id_stride, ss.name, cs.name, cd.name, ssr.control, ssr.performance_req " \
              "FROM sec_stride_requirement AS ssr " \
              "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
              "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
              "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
              "JOIN components_links AS cl ON ssr.id_link = cl.id " \
              "JOIN components AS cs ON cl.id_component_src = cs.id " \
              "JOIN components AS cd ON cl.id_component_dst = cd.id " \
              "WHERE (cl.id_component_src = ? OR cl.id_component_dst = ?) AND ssr.id_link != ? AND cs.is_human = 0 AND cd.is_human = 0 ORDER BY ssr.id_stride"
        cur.execute(sql, (id_comp, id_comp, id_link))
        rows = cur.fetchall()

        for row in rows:
            name_link = row[13] + " -> " + row[14]
            list_of_controls = list_control_organizer(row[15])
            result_list.append(Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], name_link, row[8], row[9], row[10], row[11], row[12], False, True, list_of_controls, row[16]))

    return result_list

def select_by_link(id_link, id_project):
    result_list = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, ssr.id_link, ssr.id_dfd, " \
              "ssd.name, ssr.id_stride, ss.name, cs.name, cd.name, ssr.control, ssr.performance_req " \
              "FROM sec_stride_requirement AS ssr " \
              "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
              "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
              "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
              "JOIN components_links AS cl ON ssr.id_link = cl.id " \
              "JOIN components AS cs ON cl.id_component_src = cs.id " \
              "JOIN components AS cd ON cl.id_component_dst = cd.id " \
              "WHERE ssr.id_component IS NULL AND ssr.id_link != ? AND cs.is_human = 0 AND cd.is_human = 0 AND cs.id_project == ? AND cd.id_project == ? " \
              "ORDER BY ssr.id_stride"
        cur.execute(sql, (id_link, id_project, id_project,))
        rows = cur.fetchall()

        for row in rows:
            name_link = row[13] + " -> " + row[14]
            list_of_controls = list_control_organizer(row[15])
            result_list.append(Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], name_link, row[8], row[9], row[10], row[11], row[12], False, True, list_of_controls, row[16]))

    return result_list