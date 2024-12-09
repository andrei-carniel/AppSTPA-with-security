import Constant
from Objects.security.Stride_control import Stride_control
from Tools import General_tools


def fix_name(name_comp):

    if name_comp == "CP":
        return Constant.CONTROLLED_PROCESS_full_name

    return name_comp

def fix_name_link(name_comp, id_src, id_dst):
    if name_comp == "Link_":
        if id_src == 1 and id_dst == 2:
            return Constant.LINK_CONTROLLER_ACTUATOR
        elif id_src == 1 and id_dst == 3:
            return Constant.LINK_CONTROLLER_CP
        elif id_src == 1 and id_dst == 7:
            return Constant.LINK_CONTROLLER_EXT_INF
        elif id_src == 1 and id_dst == 11:
            return Constant.LINK_CONTROLLER_HLC
        elif id_src == 2 and id_dst == 3:
            return Constant.LINK_ACTUATOR_CP
        elif id_src == 3 and id_dst == 1:
            return Constant.LINK_CP_CONTROLLER
        elif id_src == 3 and id_dst == 4:
            return Constant.LINK_CP_SENSOR
        elif id_src == 3 and id_dst == 11:
            return Constant.LINK_CP_HLC
        elif id_src == 4 and id_dst == 1:
            return Constant.LINK_SENSOR_CONTROLLER
        elif id_src == 4 and id_dst == 11:
            return Constant.LINK_SENSOR_HLC
        elif id_src == 7 and id_dst == 1:
            return Constant.LINK_EXT_INF_CONTROLLER
        elif id_src == 11 and id_dst == 1:
            return Constant.LINK_HLC_CONTROLLER
        elif id_src == 11 and id_dst == 3:
            return Constant.LINK_HLC_CP

    return name_comp

def get_dfd_element(onto, name_comp, id_src, id_dst):
    result_list = []

    name_comp = fix_name_link(name_comp, id_src, id_dst)

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_DATA_FLOW),
                              name_comp, Constant.SEC_IS_DATA_FLOW, Constant.SEC_IS_DATA_FLOW_OBJECT):
        result_list.append(Constant.SEC_IS_DATA_FLOW_NAME)

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_DATA_STORE),
                              name_comp, Constant.SEC_IS_DATA_STORE, Constant.SEC_IS_DATA_STORE_OBJECT):
        result_list.append(Constant.SEC_IS_DATA_STORE_NAME)

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_EXTERNAL_ENTITY),
                              name_comp, Constant.SEC_IS_EXTERNAL_ENTITY, Constant.SEC_IS_EXTERNAL_ENTITY_OBJECT):
        result_list.append(Constant.SEC_IS_EXTERNAL_ENTITY_NAME)

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_PROCESS),
                              name_comp, Constant.SEC_IS_PROCESS, Constant.SEC_IS_PROCESS_OBJECT):
        result_list.append(Constant.SEC_IS_PROCESS_NAME)

    return result_list

def get_dfd_element_only(onto, name_comp):
    result_list = []

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_DATA_FLOW),
                              name_comp, Constant.SEC_IS_DATA_FLOW, Constant.SEC_IS_DATA_FLOW_OBJECT):
        result_list.append(Constant.SEC_IS_DATA_FLOW_NAME)

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_DATA_STORE),
                              name_comp, Constant.SEC_IS_DATA_STORE, Constant.SEC_IS_DATA_STORE_OBJECT):
        result_list.append(Constant.SEC_IS_DATA_STORE_NAME)

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_EXTERNAL_ENTITY),
                              name_comp, Constant.SEC_IS_EXTERNAL_ENTITY, Constant.SEC_IS_EXTERNAL_ENTITY_OBJECT):
        result_list.append(Constant.SEC_IS_EXTERNAL_ENTITY_NAME)

    if find_threats_general(onto, General_tools.find_individuals_of_class(onto, Constant.SEC_IS_PROCESS),
                              name_comp, Constant.SEC_IS_PROCESS, Constant.SEC_IS_PROCESS_OBJECT):
        result_list.append(Constant.SEC_IS_PROCESS_NAME)

    return result_list

def get_dfd_connection(dfd_name):
    if dfd_name == Constant.SEC_IS_DATA_FLOW_NAME:
        return Constant.SEC_IS_DATA_FLOW
    elif dfd_name == Constant.SEC_IS_DATA_STORE_NAME:
        return Constant.SEC_IS_DATA_STORE
    elif dfd_name == Constant.SEC_IS_EXTERNAL_ENTITY_NAME:
        return Constant.SEC_IS_EXTERNAL_ENTITY
    elif dfd_name == Constant.SEC_IS_PROCESS_NAME:
        return Constant.SEC_IS_PROCESS
    return ""

def get_dfd_name(dfd_id):
    if dfd_id == Constant.DB_ID_EXTERNAL_ENTITY:
        return Constant.SEC_IS_EXTERNAL_ENTITY_NAME
    elif dfd_id == Constant.DB_ID_DATA_FLOW:
        return Constant.SEC_IS_DATA_FLOW_NAME
    elif dfd_id == Constant.DB_ID_DATA_STORE:
        return Constant.SEC_IS_DATA_STORE_NAME
    elif dfd_id == Constant.DB_ID_PROCESS:
        return Constant.SEC_IS_PROCESS_NAME
    return ""

def get_dfd_id(dfd_name):
    if dfd_name == Constant.SEC_IS_EXTERNAL_ENTITY_NAME:
        return Constant.DB_ID_EXTERNAL_ENTITY
    elif dfd_name == Constant.SEC_IS_DATA_FLOW_NAME:
        return Constant.DB_ID_DATA_FLOW
    elif dfd_name == Constant.SEC_IS_DATA_STORE_NAME:
        return Constant.DB_ID_DATA_STORE
    elif dfd_name == Constant.SEC_IS_PROCESS_NAME:
        return Constant.DB_ID_PROCESS
    return 0

def get_threats(onto, name_comp):
    result_list = []

    name_comp = get_dfd_connection(name_comp)

    if General_tools.find_property_by_name_object(onto, name_comp, Constant.SEC_SPOOFING_CAUSAL_FACTOR, Constant.SEC_SPOOFING_OBJECT):
        result_list.append(Constant.DB_NAME_SPOOFING)

    if General_tools.find_property_by_name_object(onto, name_comp, Constant.SEC_TAMPERING_CAUSAL_FACTOR, Constant.SEC_TAMPERING_OBJECT):
        result_list.append(Constant.DB_NAME_TAMPERING)

    if General_tools.find_property_by_name_object(onto, name_comp, Constant.SEC_REPUDIATION_CAUSAL_FACTOR, Constant.SEC_REPUDIATION_OBJECT):
        result_list.append(Constant.DB_NAME_REPUDIATION)

    if General_tools.find_property_by_name_object(onto, name_comp, Constant.SEC_INFORMATION_DISCLOSURE_CAUSAL_FACTOR, Constant.SEC_INFORMATION_DISCLOSURE_OBJECT):
        result_list.append(Constant.DB_NAME_INFORMATION_DISCLOSURE)

    if General_tools.find_property_by_name_object(onto, name_comp, Constant.SEC_DENIAL_OF_SERVICE_CAUSAL_FACTOR, Constant.SEC_DENIAL_OF_SERVICE_OBJECT):
        result_list.append(Constant.DB_NAME_DENIAL_OF_SERVICE)

    if General_tools.find_property_by_name_object(onto, name_comp, Constant.SEC_ELEVATION_OF_PRIVILEGE_CAUSAL_FACTOR, Constant.SEC_ELEVATION_OF_PRIVILEGE_OBJECT):
        result_list.append(Constant.DB_NAME_ELEVATION_OF_PRIVILEGE)

    return result_list

def find_threats_general(onto, sons_list, name_comp, name_class_dst, name_property):
    for son in sons_list.individual_list:
        if son.name.lower() == name_comp.lower():
            name_comp = fix_name(name_comp)
            if General_tools.find_property_by_name_object(onto, name_comp, name_class_dst, name_property):
                return True
    return False

def get_subclass_of_countermeasure_class(onto, attack):
    find_for = ""
    clean = ""
    if attack == Constant.DB_NAME_SPOOFING:
        find_for = Constant.SEC_SPOOFING_CONTROL
        clean = "S_"
    elif attack == Constant.DB_NAME_TAMPERING:
        find_for = Constant.SEC_TAMPERING_CONTROL
        clean = "T_"
    elif attack == Constant.DB_NAME_REPUDIATION:
        find_for = Constant.SEC_REPUDIATION_CONTROL
        clean = "R_"
    elif attack == Constant.DB_NAME_INFORMATION_DISCLOSURE:
        find_for = Constant.SEC_INFORMATION_DISCLOSURE_CONTROL
        clean = "ID_"
    elif attack == Constant.DB_NAME_DENIAL_OF_SERVICE:
        find_for = Constant.SEC_DENIAL_OF_SERVICE_CONTROL
        clean = "DOS_"
    elif attack == Constant.DB_NAME_ELEVATION_OF_PRIVILEGE:
        find_for = Constant.SEC_ELEVATION_OF_PRIVILEGE_CONTROL
        clean = "EOP_"

    # list = General_tools.get_subclass_first_level(onto, find_for)
    list_h = General_tools.find_individuals_of_class(onto, find_for)
    son_text = ""
    son_list = []
    count = 0
    for son in list_h.name_list:
        if clean in son:
            if son_text != "":
                son_text += " OR "
            son_text += son.replace(clean, "").replace("_", " ")
            son_list.append(Stride_control(son.replace(clean, "").replace("_", " "), False))
            count += 1
    return son_text, son_list

def generate_description_source(onto, source, destiny, context, attack):
    mechanism = ""

    if attack == Constant.DB_NAME_SPOOFING:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_SPOOFING)
        consider = source + " must/shall have " + son_text + " for data sent."
        return source + " may be spoofed by an attacker and this may lead to unauthorized access to " + destiny + ".", consider, mechanism, son_list
    if attack == Constant.DB_NAME_TAMPERING:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_TAMPERING)
        consider = source + " must/shall have " + son_text + " for data sent."
        return "Data flowing across " + context + " may be tampered with by an attacker. This may lead to a denial of service attack against " + source + \
                        " or an elevation of privilege attack against " + source + " or an information disclosure by " + source + ". Failure to verify " \
                        "that input is as expected is a root cause of a very large number of exploitable issues.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_REPUDIATION:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_REPUDIATION)
        consider = source + " must/shall have " + son_text + " for data sent."
        return source + " claims that it did not sends data (" + context + ").", consider, mechanism, son_list
    if attack == Constant.DB_NAME_INFORMATION_DISCLOSURE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_INFORMATION_DISCLOSURE)
        consider = source + " must/shall have " + son_text + " for data sent."
        return "Data flowing across " + context + " from " + source + " may be sniffed by an attacker. Depending on what type of data an attacker can read, it may be used to attack other " \
                        "parts of the system or simply be a disclosure of information leading to compliance violations.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_DENIAL_OF_SERVICE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_DENIAL_OF_SERVICE)
        consider = source + " must/shall have " + son_text + " for data sent."
        return source + " crashes, halts, stops or runs slowly; in all cases violating an availability metric. " \
                        "An external agent interrupts data flowing across a trust boundary in either direction.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_ELEVATION_OF_PRIVILEGE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_ELEVATION_OF_PRIVILEGE)
        consider = source + " must/shall have " + son_text + " for data sent."
        return source + " may be able to impersonate the context of " + context + " in order to gain additional privilege. " \
                        "An attacker may pass data into " + source + " in order to change the flow of program execution within " + destiny + " to the attacker's choosing. " \
                        + source + " may be able to remotely execute code for " + destiny + ".", consider, mechanism, son_list
    return "", "", "", []

def generate_description_destiny(onto, destiny, source, context, attack):
    mechanism = ""

    if attack == Constant.DB_NAME_SPOOFING:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_SPOOFING)
        consider = destiny + " must/shall have " + son_text + " for data received."
        return destiny + " may be spoofed by an attacker and this may lead to information disclosure by " + source + ".", consider, mechanism, son_list
    if attack == Constant.DB_NAME_TAMPERING:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_TAMPERING)
        consider = destiny + " must/shall have " + son_text + " for data received."
        return "Data flowing across " + context + " may be tampered with by an attacker. This may lead to a denial of service attack against " + destiny + \
                        " or an elevation of privilege attack against " + destiny + " or an information disclosure by " + destiny + ". Failure to verify " \
                        "that input is as expected is a root cause of a very large number of exploitable issues.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_REPUDIATION:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_REPUDIATION)
        consider = destiny + " must/shall have " + son_text + " for data received."
        return destiny + " claims that it did not receive data (" + context + ").", consider, mechanism, son_list
    if attack == Constant.DB_NAME_INFORMATION_DISCLOSURE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_INFORMATION_DISCLOSURE)
        consider = destiny + " must/shall have " + son_text + " for data received."
        return "Data flowing across " + context + " to " + destiny + " may be sniffed by an attacker. Depending on what type of data an attacker can read, it may be used to attack other " \
                        "parts of the system or simply be a disclosure of information leading to compliance violations.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_DENIAL_OF_SERVICE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_DENIAL_OF_SERVICE)
        consider = destiny + " must/shall have " + son_text + " for data received."
        return destiny + " crashes, halts, stops or runs slowly; in all cases violating an availability metric. " \
                        "An external agent interrupts data flowing across a trust boundary in either direction.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_ELEVATION_OF_PRIVILEGE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_ELEVATION_OF_PRIVILEGE)
        consider = destiny + " must/shall have " + son_text + " for data received."
        return destiny + " may be able to impersonate the context of " + destiny + " in order to gain additional privilege. " \
                        "An attacker may pass data into " + source + " in order to change the flow of program execution within " + destiny + " to the attacker's choosing. " \
                        + source + " may be able to remotely execute code for " + destiny + ".", consider, mechanism, son_list
    return "", "", "", []

def generate_description_link(onto, link, context, attack):
    mechanism = ""

    if attack == Constant.DB_NAME_SPOOFING:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_SPOOFING)
        consider = "Link " + link + " must/shall have " + son_text + " for data flow."
        return link + " may be spoofed by an attacker and this may lead to unauthorized access to an attacker.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_TAMPERING:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_TAMPERING)
        consider = "Link " + link + " must/shall have " + son_text + " for data flow."
        return "Data flowing across " + context + " may be tampered with by an attacker. This may lead to a denial of service attack or an elevation" \
                        " of privilege attack against " + link + ", or an information disclosure by " + link + ". Failure to verify " \
                        "that input is as expected is a root cause of a very large number of exploitable issues.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_REPUDIATION:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_REPUDIATION)
        consider = "Link " + link + " must/shall have " + son_text + " for data flow."
        return link + " claims that it did not sends data (" + context + ").", consider, mechanism, son_list
    if attack == Constant.DB_NAME_INFORMATION_DISCLOSURE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_INFORMATION_DISCLOSURE)
        consider = "Link " + link + " must/shall have " + son_text + " for data flow."
        return "Data flowing across " + context + " may be sniffed by an attacker. Depending on what type of data an attacker can read, it may be used to attack other " \
                        "parts of the system or simply be a disclosure of information leading to compliance violations.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_DENIAL_OF_SERVICE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_DENIAL_OF_SERVICE)
        consider = "Link " + link + " must/shall have " + son_text + " for data flow."
        return link + " crashes, halts, stops or runs slowly; in all cases violating an availability metric. " \
                        "An external agent interrupts data flowing across a trust boundary in either direction.", consider, mechanism, son_list
    if attack == Constant.DB_NAME_ELEVATION_OF_PRIVILEGE:
        son_text, son_list = get_subclass_of_countermeasure_class(onto, Constant.DB_NAME_ELEVATION_OF_PRIVILEGE)
        consider = "Link " + link + " must/shall have " + son_text + " for data flow."
        return link + " may be able to impersonate the context of " + context + " in order to gain additional privilege.", consider, mechanism, son_list

    return "", "", "", []

