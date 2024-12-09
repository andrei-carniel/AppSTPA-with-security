import sqlite3
from sqlite3 import Error

import Constant



# make a connection
from Objects.Loss_Scenario_Req import Loss_Scenario_Req
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

# count requirements
def select_count_conflict_safety_security(list_onto, id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    if list_onto == None:
        return []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        for pos in range(len(list_onto)):
            saf_string = "%" + list_onto[pos].word + "%"
            cur.execute("SELECT count(requirement) FROM saf_loss_scenario_req WHERE requirement LIKE ? AND id_project = ?", (saf_string, id_project,))
            row_saf = cur.fetchone()

            sec_count = 0
            for sec_confl in list_onto[pos].list_of_conflicts:
                sec_string = "%" + sec_confl + "%"
                cur.execute("SELECT count(justification) FROM sec_stride_requirement WHERE justification LIKE ? AND id_project = ?", (sec_string, id_project,))
                row_sec = cur.fetchone()
                if row_sec != None:
                    sec_count += row_sec[0]

            if row_saf != None:
                if row_saf[0] > 0 and sec_count > 0:
                    list_onto[pos].is_conflict = True

    return list_onto

#select recommendation by conflict
def select_recommendation_by_count_conflict_safety_security(onto_conflict, id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    saf_result_list = []
    sec_result_list = []

    if onto_conflict == None:
        return saf_result_list, sec_result_list

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        saf_string = "%" + onto_conflict.word + "%"

        cur.execute("SELECT lsr.id, lsr.id_controller, lsr.id_uca, lsr.id_project, lsr.id_comp_cause, lsr.id_comp_src, lsr.id_comp_dst, lsr.requirement, "
                    "lsr.cause, lsr.mechanism, cs.name, cd.name, cc.name FROM saf_loss_scenario_req AS lsr "
                    "JOIN components AS cs ON cs.id = lsr.id_comp_src "
                    "JOIN components AS cd ON cd.id = lsr.id_comp_dst "
                    "JOIN components AS cc ON cc.id = lsr.id_comp_dst "
                    "WHERE lsr.requirement like ? AND lsr.id_project = ?", (saf_string, id_project))
        row_safs = cur.fetchall()

        for row_saf in row_safs:
            saf_result_list.append(Loss_Scenario_Req(row_saf[0], row_saf[1], row_saf[2], row_saf[3], row_saf[4], row_saf[5],
                                  row_saf[6], row_saf[7], row_saf[8], row_saf[9], row_saf[10], row_saf[11], row_saf[12]))

        sql_sec = "SELECT DISTINCT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.mechanism, ssr.id_priority, ssp.name, ssr.id_component, ssr.id_link, ssr.id_dfd, " \
                  "ssd.name, ssr.id_stride, ss.name, cs.name, cd.name, ssr.id_project " \
                  "FROM sec_stride_requirement AS ssr " \
                  "JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id " \
                  "JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id " \
                  "JOIN sec_stride AS ss ON ssr.id_stride = ss.id " \
                  "JOIN components_links AS cl ON ssr.id_link = cl.id " \
                  "JOIN components AS cs ON cl.id_component_src = cs.id " \
                  "JOIN components AS cd ON cl.id_component_dst = cd.id " \
                  "WHERE ssr.justification LIKE ? AND ssr.id_project = ?"
        for sec_confl in onto_conflict.list_of_conflicts:
            sec_string = "%" + sec_confl + "%"
            cur.execute(sql_sec, (sec_string, id_project))
            row_sec = cur.fetchall()

            for row in row_sec:
                name_link = row[13] + " -> " + row[14]
                sec_result_list.append(Stride_Requirement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], name_link, row[7],
                                                          row[8], row[9], row[10], row[11], row[12], False, True, row[15]))

    return saf_result_list, sec_result_list

def select_distinct_safety_recommendation(id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    list_result = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT(requirement) FROM saf_loss_scenario_req WHERE id_project = ?", (id_project,))
        row_saf = cur.fetchall()

        for row in row_saf:
            list_result.append(clean_safety_recommendation(row[0]))

    return list_result

def clean_safety_recommendation(aux_string):
    splited_string = []
    string_formated = ""
    aux_string = aux_string.lower().strip()

    if aux_string.__contains__(Constant.MUST_HAVE):
        splited_string = aux_string.split(Constant.MUST_HAVE, 2)
    elif aux_string.__contains__(Constant.MUST):
        splited_string = aux_string.split(Constant.MUST, 2)
    elif aux_string.__contains__(Constant.SHALL_HAVE):
        splited_string = aux_string.split(Constant.SHALL_HAVE, 2)
    elif aux_string.__contains__(Constant.SHALL):
        splited_string = aux_string.split(Constant.SHALL, 2)

    if len(splited_string) >= 2:
        string_formated = splited_string[1]
    else:
        string_formated = aux_string

    splited_string = []
    if string_formated.__contains__(Constant.WHEN):
        splited_string = string_formated.split(Constant.WHEN, 2)
    elif string_formated.__contains__(Constant.BEFORE):
        splited_string = string_formated.split(Constant.BEFORE, 2)
    elif string_formated.__contains__(Constant.AFTER):
        splited_string = string_formated.split(Constant.AFTER, 2)
    elif string_formated.__contains__(Constant.WHILE):
        splited_string = string_formated.split(Constant.WHILE, 2)

    if len(splited_string) >= 2:
        string_formated = splited_string[0]

    return string_formated

def select_distinct_security_recommendation(id_project):
    """
    Query tasks by all rows
    :return: List of Losses
    """
    list_result = []

    # create a database connection
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT justification FROM sec_stride_requirement WHERE id_project = ?", (id_project,))
        row_saf = cur.fetchall()

        for row in row_saf:
            list_result.append(clean_security_recommendation(row[0]))

    return list_result

def clean_security_recommendation(aux_string):
    splited_string = []
    string_formated = ""
    aux_string = aux_string.lower().strip()

    if aux_string.__contains__(Constant.MUST_HAVE):
        splited_string = aux_string.split(Constant.MUST_HAVE, 2)
    elif aux_string.__contains__(Constant.MUST):
        splited_string = aux_string.split(Constant.MUST, 2)
    elif aux_string.__contains__(Constant.SHALL_HAVE):
        splited_string = aux_string.split(Constant.SHALL_HAVE, 2)
    elif aux_string.__contains__(Constant.SHALL):
        splited_string = aux_string.split(Constant.SHALL, 2)

    if len(splited_string) >= 2:
        string_formated = splited_string[1]
    else:
        string_formated = aux_string

    splited_string = []
    if string_formated.__contains__(Constant.FOR):
        splited_string = string_formated.split(Constant.FOR, 2)

    if len(splited_string) >= 2:
        string_formated = splited_string[0]

    return string_formated