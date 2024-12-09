import datetime
from os import link

from owlready2 import IRIS

import Constant
from Objects.Requirement import Requirement
from Objects.Sec_Hierarchy import Sec_Hierarchy
from Tools import General_tools, Dictionary


# present the analysis of safety requirements
def print_space_line(analysis_file):
    analysis_file.write("\n--------------------------------\n\n")


def get_security_requirement_analysis(onto):
    date_now = datetime.datetime.now()
    analysis_file = open(Constant.ANALYSIS_PATH + "security_analysis_" + str(date_now.year) + "-" + str(date_now.month) + "-" + str(date_now.day) + ".txt", "w")
    requirements_obj_list = []

    requirements_obj_list.extend(sec_requirement_creation(onto, False, Constant.SEC_SPOOFING_CAUSAL_FACTOR, Constant.SEC_SPOOFING, Constant.SEC_SPOOFING_CONTROL, analysis_file, len(requirements_obj_list)))
    print_space_line(analysis_file)

    requirements_obj_list.extend(sec_requirement_creation(onto, False, Constant.SEC_TAMPERING_CAUSAL_FACTOR, Constant.SEC_TAMPERING, Constant.SEC_TAMPERING_CONTROL, analysis_file, len(requirements_obj_list)))
    print_space_line(analysis_file)

    requirements_obj_list.extend(sec_requirement_creation(onto, False, Constant.SEC_REPUDIATION_CAUSAL_FACTOR, Constant.SEC_REPUDIATION, Constant.SEC_REPUDIATION_CONTROL, analysis_file, len(requirements_obj_list)))
    print_space_line(analysis_file)

    requirements_obj_list.extend(sec_requirement_creation(onto, False, Constant.SEC_INFORMATION_DISCLOSURE_CAUSAL_FACTOR, Constant.SEC_INFORMATION_DISCLOSURE, Constant.SEC_INFORMATION_DISCLOSURE_CONTROL, analysis_file, len(requirements_obj_list)))
    print_space_line(analysis_file)

    requirements_obj_list.extend(sec_requirement_creation(onto, False, Constant.SEC_DENIAL_OF_SERVICE_CAUSAL_FACTOR, Constant.SEC_DENIAL_OF_SERVICE, Constant.SEC_DENIAL_OF_SERVICE_CONTROL, analysis_file, len(requirements_obj_list)))
    print_space_line(analysis_file)

    requirements_obj_list.extend(sec_requirement_creation(onto, False, Constant.SEC_ELEVATION_OF_PRIVILEGE_CAUSAL_FACTOR, Constant.SEC_ELEVATION_OF_PRIVILEGE, Constant.SEC_ELEVATION_OF_PRIVILEGE_CONTROL, analysis_file, len(requirements_obj_list)))
    print_space_line(analysis_file)

    analysis_file.close()
    return requirements_obj_list


def sec_requirement_creation(onto, is_B_side, sample_threat, sample_attack, sample_control, analysis_file, counter):
    sec_requirements = General_tools.find_individuals_of_class(onto, sample_threat)
    action_to_remove_list = []
    sec_requirements_list = []
    analysis_file.write("Name: " + sec_requirements.class_parent.name + "\n\n")
    result_list = []

    individual_list = sec_requirements.name_list
    individual_list.remove(sample_attack)

    for individual in sec_requirements.individual_list:
        if "Link_" in individual.name:
            aux_object = get_link_information_sec_requirement(onto, individual, sample_attack, sample_control)
            if not aux_object.is_to_delete:
                sec_requirements_list.append(aux_object)

            action_to_remove_list.append(individual.name)
            if aux_object.action_name != "":
                action_to_remove_list.append(aux_object.action_name)
                if is_B_side:
                    action_to_remove_list.append(aux_object.source)

    for remove in action_to_remove_list:
        if remove in individual_list:
            individual_list.remove(remove)

    for individual in individual_list:
        aux_object = get_element_information_sec_requirement(individual, sample_attack, sample_control)
        if not aux_object.is_to_delete:
            sec_requirements_list.append(aux_object)

    for item_list in sec_requirements_list:
        counter+=1
        result_list.append(print_sec_requirement(item_list, analysis_file, counter))

    return result_list


# Function to organize the information in a objet - Data type: LINK
def get_link_information_sec_requirement(onto, individual, attack, control):
    result_object = Sec_Hierarchy()
    result_object.name = individual.name
    result_object.name_trust_boundary = get_trust_boundary(individual)
    result_object.attack_name = attack
    result_object.attacks_list = Dictionary.elements[attack]
    result_object.control_name = control
    result_object.controls_list = Dictionary.elements[control]
    result_object.is_link = True

    link_list = General_tools.find_individuals_of_class(onto, individual.name)

    if Dictionary.elements[Constant.HIGH_LEVEL_CONTROLLER] == "" and Constant.HIGH_LEVEL_CONTROLLER in link_list.name_list:
        result_object.is_to_delete = True

    list_names_link = individual.name.split("_")
    list_names_link.pop(0)
    link_list.name_list.remove(individual.name)
    link_list.individual_list.remove(individual)

    result_object.action_name = find_action_in_list(link_list.name_list)

    if result_object.action_name != "":
        result_object.actions_list = Dictionary.elements[result_object.action_name]

    result_object.source = find_name_in_list(link_list.name_list, list_names_link[0].lower())
    result_object.source_trust_boundary = find_trust_boundary_in_list(link_list.individual_list, list_names_link[0].lower())
    list_names_link.pop(0)
    result_object.destiny = find_name_in_list(link_list.name_list, list_names_link[0].lower())
    result_object.destiny_trust_boundary = find_trust_boundary_in_list(link_list.individual_list, list_names_link[0].lower())
    list_names_link.pop(0)

    return result_object


# Function to organize the information in a objet - Data type: ELEMENT
def get_element_information_sec_requirement(name, attack, control):
    result_object = Sec_Hierarchy()
    result_object.name = name
    result_object.attack_name = attack
    result_object.attacks_list = Dictionary.elements[attack]
    result_object.control_name = control
    result_object.controls_list = Dictionary.elements[control]
    result_object.is_link = False
    result_object.action_name = ""
    result_object.actions_list = []

    aux_source = Dictionary.elements[name]

    if isinstance(aux_source, str):
        result_object.source = aux_source
        result_object.sources_list = []

        if Dictionary.elements[Constant.HIGH_LEVEL_CONTROLLER] == "" and Constant.HIGH_LEVEL_CONTROLLER == name:
            result_object.is_to_delete = True
    else:
        result_object.source = ""
        result_object.sources_list = aux_source

    result_object.destiny = ""

    return result_object

# find the action based in the name of ontology
def find_action_in_list(list):
    name_found = ""

    for name_in_list in list:
        if "control_action_" in name_in_list.lower() or "feedback_of_" in name_in_list.lower():
            name_found = name_in_list
            list.remove(name_in_list)
            return name_found

    return name_found


# find the names on ontology
def find_name_in_list(list, name_wanted):
    name_found = ""

    for name_in_list in list:
        if name_wanted in name_in_list.lower():
            name_found =  name_in_list
            return name_found


    return  name_found


def get_trust_boundary(individual):
    try:
        trust_boundary = individual.sec_trusted_boundary[0]
    except Exception as e: # work on python 3.x
        # logger.error('Failed to upload to ftp: '+ str(e))
        print('Failed to upload to ftp: '+ str(e))
        trust_boundary = -1

    return trust_boundary


def find_trust_boundary_in_list(individual_list, name_wanted):
    trust_boundary = -1

    for individual in individual_list:
        if name_wanted == individual.name.lower():
            trust_boundary = get_trust_boundary(individual)
            return trust_boundary

    return trust_boundary

# Print the security requirement
def print_sec_requirement(obj_sec_hierarchy, analysis_file, counter):
    requirement = ""
    key_control_action = "The value "
    key_link = "The link between: "
    key_can_suffer = ", can suffer the following attack(s): "
    key_consider = ".\nConsider the following mitigation(s): "
    key_to = ", to:  "
    aux_things_list = []
    aux_requirement = ""

    if obj_sec_hierarchy.is_link :
        if obj_sec_hierarchy.action_name != "":
            requirement += key_control_action + "\"" + str(obj_sec_hierarchy.actions_list) + "\" from: \"" + obj_sec_hierarchy.source + "\" (trust boundary " + str(obj_sec_hierarchy.source_trust_boundary) + ")" + key_to + "\"" + obj_sec_hierarchy.destiny + \
                           "\"(trust boundary " + str(obj_sec_hierarchy.destiny_trust_boundary) + ")" + key_can_suffer + "\"" + str(obj_sec_hierarchy.attacks_list) + "\"" + key_consider + "\"" + str(obj_sec_hierarchy.controls_list) + "\".\n\n"
            aux_things_list.extend(obj_sec_hierarchy.actions_list)
        else:
            requirement += key_link + "\"" + obj_sec_hierarchy.source + "\" (trust boundary " + str(obj_sec_hierarchy.source_trust_boundary) + ")" + key_to + "\"" + obj_sec_hierarchy.destiny + \
                           "\" (trust boundary " + str(obj_sec_hierarchy.destiny_trust_boundary) + ")" + key_can_suffer + "\"" + str(obj_sec_hierarchy.attacks_list) + "\"" + key_consider + "\"" + str(obj_sec_hierarchy.controls_list) + "\".\n\n"
            aux_things_list.append(obj_sec_hierarchy.destiny)

        aux_requirement = requirement
        requirement = str(counter) + " ->> " + obj_sec_hierarchy.name + " (trust boundary " + str(obj_sec_hierarchy.name_trust_boundary) + "): " + requirement
    else:

        if obj_sec_hierarchy.source != "":
            requirement += str(counter) + " >> " + obj_sec_hierarchy.source + "(trust boundary " + str(obj_sec_hierarchy.source_trust_boundary) + ")"
            aux_things_list.append(obj_sec_hierarchy.source)
        else:
            requirement += str(counter) + " >> " + str(obj_sec_hierarchy.sources_list) + "(trust boundary " + str(obj_sec_hierarchy.destiny_trust_boundary) + ")"
            aux_things_list.extend(obj_sec_hierarchy.sources_list)

        requirement += key_can_suffer + "\"" + str(obj_sec_hierarchy.attacks_list) + "\"" + key_consider + "\"" + str(obj_sec_hierarchy.controls_list) + "\".\n\n"
        aux_requirement = requirement


    analysis_file.write(requirement)

    req_obj = Requirement(counter, Constant.SECURITY, aux_requirement, aux_things_list)
    return req_obj


# to delete
def get_causal_factor_list(causal_factor_name):
    new_line = False
    result = ""

    if causal_factor_name == Constant.ALGORITHM:
        return Dictionary.elements[causal_factor_name] + " is an inadequate control algorithm."

    if causal_factor_name == Constant.CONTROL_ACTION_ACTUATOR:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is an inappropriate or missing control action to " + Dictionary.elements[Constant.ACTUATOR] + "."
        return result

    if causal_factor_name == Constant.CONTROL_ACTION_CP:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is an inappropriate or missing control action to " + Dictionary.elements[Constant.CONTROLLED_PROCESS] + "."
        return result

    if causal_factor_name == Constant.CONTROL_ACTION_HLC_CONTROLLER:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is a conflicting control action to " + Dictionary.elements[Constant.CONTROLLER] + "."
        return result

    if causal_factor_name == Constant.CONTROL_ACTION_HLC_CP:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is a conflicting Control Action."
        return result

    if causal_factor_name == Constant.EXTERNAL_INFORMATION:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is a wrong or missing External Information."
        return result

    if causal_factor_name == Constant.ENVIRONMENTAL_DISTURBANCES:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is an unidentified disturbance."
        return result

    if causal_factor_name == Constant.FEEDBACK_OF_CP:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is as inadequate or missing feedback of " + Dictionary.elements[Constant.SENSOR] + "."
        return result

    if causal_factor_name == Constant.PROCESS_MODEL:
        return Dictionary.elements[causal_factor_name] + " is a wrong process model."

    if causal_factor_name == Constant.INPUT:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " is a missing or wrong input."
        return result

    if causal_factor_name == Constant.OUTPUT:
        for action in Dictionary.elements[causal_factor_name]:
            if new_line:
                result += "\n"
            new_line = True
            result += action + " causes delay."
        return result


