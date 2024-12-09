import Constant
from Database.performance import DB_Pef_Performance_Recommendation, DB_Pef_Conflict
from Tools import General_tools


def get_pef_performace_metrics(onto):
    list_of_results = []

    list_original = General_tools.get_subclass_first_level(onto, Constant.PEF_PERFORMANCE_RECOMMENDATION)

    for name in list_original:
        list_of_results.append(name.replace("Pef_", "").replace("Pef ", "").replace("_", " ").replace("recommendation", ""))

    return list_of_results, list_original

def get_pef_performace_elements(onto, name_class, id_thing):
    list_of_results = []
    list_original_results = []
    list_verification = []

    if id_thing == Constant.DB_ID_CONTROLLER:
        list_verification = General_tools.find_for_object_property_of_class(onto, Constant.CONTROLLER, Constant.PEF_COMPOSED_BY)
    elif id_thing == Constant.DB_ID_ALGORITHM:
        list_verification = General_tools.find_for_object_property_of_class(onto, Constant.ALGORITHM, Constant.PEF_PRESENT_IN)
    elif id_thing == Constant.DB_ID_PROCESS_MODEL:
        list_verification = General_tools.find_for_object_property_of_class(onto, Constant.PROCESS_MODEL, Constant.PEF_PRESENT_IN)

    list_original = General_tools.get_subclass_first_level(onto, name_class)
    name_clean = name_class.replace("_recommendation","")

    for name in list_original:
        if name != name_clean:
            if name in list_verification:
                list_original_results.append(name)
                list_of_results.append(name.replace("Pef_", "").replace("Pef ", "").replace("_", " "))

    return list_of_results, list_original_results

def get_pef_composed_by(onto, id_comp):
    list_of_results = []
    find_for = ""
    if id_comp == Constant.DB_ID_CONTROLLER:
        find_for = Constant.CONTROLLER
    elif id_comp == Constant.DB_ID_ALGORITHM:
        find_for = Constant.ALGORITHM
    elif id_comp == Constant.DB_ID_PROCESS_MODEL:
        find_for = Constant.PROCESS_MODEL

    list = General_tools.find_for_object_property_of_class(onto, find_for, Constant.PEF_COMPOSED_BY)

    for name in list:
        list_of_results.append(name.replace("Pef_", "").replace("Pef ", "").replace("_", " "))

    return list_of_results

def get_description_by_performance(desc):
    description = ""

    if desc == Constant.PEF_PHYSICAL_LINK:
        description = "Is any network used to establish communication, the physical links connects to an interface, that can be wired or Wi-Fi. You shall describe what are the physichal link needs for the system?"
    elif desc == Constant.PEF_APPLICATION:
        description = "Some systems has the logic to carry out a specific task on an application. Every application needs an Operating System to run."
    elif desc == Constant.PEF_OPERATING_SYSTEM:
        description = "Is the software that manages the computer hardware, software resources, and common services for applications. This option considers that your software is Operating System that has the system logic."
    elif desc == Constant.PEF_PROCESSOR:
        description = "Consider the number of instructions or tasks that your system shall be able to accomplish. This component responsible for doing operations that will accomplish tasks."
    elif desc == Constant.PEF_INTERFACE_I_O:
        description = "Is any network used to establish communication, the physical links connects to an interface, that can be wired or Wi-Fi. You shall describe what the physichal link needs are for the system and the interfaces."
    elif desc == Constant.PEF_MEMORY:
        description = "Consider only Ram memory, which is used for short or runtimes."
    elif desc == Constant.PEF_STORAGE:
        description = "It refers to the memory used to store data for long time."

    return description

def get_metric_by_name(metric):
    if metric == Constant.PEF_COMMUNICATION_TIME:
        return Constant.DB_ID_COMMUNICATION_TIME
    elif metric == Constant.PEF_LATENCY:
        return Constant.DB_ID_LATENCY
    elif metric == Constant.PEF_RESOURCE_UTILIZATION:
        return Constant.DB_ID_RESOURCE_UTILIZATION
    elif metric == Constant.PEF_RESPONSE_TIME:
        return Constant.DB_ID_RESPONSE_TIME
    elif metric == Constant.PEF_SCALABILITY:
        return Constant.DB_ID_SCALABILITY
    elif metric == Constant.PEF_THROUGHPUT:
        return Constant.DB_ID_THROUGHPUT
    elif metric == Constant.PEF_WORKLOAD:
        return Constant.DB_ID_WORKLOAD
    return -1

def get_element_by_name(element):
    if element == Constant.PEF_APPLICATION:
        return Constant.DB_ID_APPLICATION
    elif element == Constant.PEF_INTERFACE_I_O:
        return Constant.DB_ID_INTERFACE_I_O
    elif element == Constant.PEF_MEMORY:
        return Constant.DB_ID_MEMORY
    elif element == Constant.PEF_OPERATING_SYSTEM:
        return Constant.DB_ID_OPERATING_SYSTEM
    elif element == Constant.PEF_PHYSICAL_LINK:
        return Constant.DB_ID_PHYSICAL_LINK
    elif element == Constant.PEF_PROCESSOR:
        return Constant.DB_ID_PROCESSOR
    elif element == Constant.PEF_STORAGE:
        return Constant.DB_ID_STORAGE
    return -1

def get_safety_STRIDE_conflicts(onto, element, id_component, id_project, is_source):
    list_safety_results = []
    list_security_results = []

    # SAFETY
    list_safety_results = DB_Pef_Conflict.select_safety_recommendation_by_controller(id_project, id_component, is_source)

    # STRIDE
    list_controls = get_stride_mechanism_conflicts(onto, element)
    list_security_results = DB_Pef_Conflict.select_recommendation_by_count_conflict_safety_security(id_project, id_component, list_controls)

    return list_safety_results, list_security_results

def get_stride_mechanism_conflicts(onto, onto_name_element):
    spoofing_class = General_tools.get_subclass_first_level(onto, Constant.SEC_SPOOFING_CONTROL)
    tampering_class = General_tools.get_subclass_first_level(onto, Constant.SEC_TAMPERING_CONTROL)
    rc_class = General_tools.get_subclass_first_level(onto, Constant.SEC_REPUDIATION_CONTROL)
    id_class = General_tools.get_subclass_first_level(onto, Constant.SEC_INFORMATION_DISCLOSURE_CONTROL)
    dos_class = General_tools.get_subclass_first_level(onto, Constant.SEC_DENIAL_OF_SERVICE_CONTROL)
    eop_class = General_tools.get_subclass_first_level(onto, Constant.SEC_ELEVATION_OF_PRIVILEGE_CONTROL)

    list_result = []
    list_result.extend(find_element_in_control(onto, spoofing_class, onto_name_element, list_result))
    list_result.extend(find_element_in_control(onto, tampering_class, onto_name_element, list_result))
    list_result.extend(find_element_in_control(onto, rc_class, onto_name_element, list_result))
    list_result.extend(find_element_in_control(onto, id_class, onto_name_element, list_result))
    list_result.extend(find_element_in_control(onto, dos_class, onto_name_element, list_result))
    list_result.extend(find_element_in_control(onto, eop_class, onto_name_element, list_result))

    return list_result

def find_element_in_control(onto, list, onto_name_element, current_list):
    result_list = []
    for name in list:
        sons = General_tools.get_subclass_first_level(onto, name)

        if onto_name_element in sons:
            aux = name.replace("Sec_mechanism_", "")
            save = aux.replace("_", " ")
            if (save in current_list) == False:
                result_list.append(save)

    return result_list