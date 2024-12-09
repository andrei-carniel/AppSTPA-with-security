from owlready2 import *
import types

import Constant
from Database.conflict import DB_Conflict
from Tools import General_tools


def add_conflict_safety_security(onto, name_saf, name_sec, conf_reinf):
    # name_saf_formated = name_saf.lower()
    # name_sec_formated = name_sec.lower()
    try:
        name_saf_formated = " ".join(name_saf.split()).replace(" ", "_").lower()
        name_sec_formated = " ".join(name_sec.split()).replace(" ", "_").lower()

        with onto:
            # class Saf_conflict_recommendation(Thing): pass
            # class Sec_conflict_mechanism(Thing): pass
            Saf_conflict_recommendation = types.new_class(Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION, (Thing,))
            Sec_conflict_mechanism = types.new_class(Constant.SEC_CONFLICT_REINFORCEMENT_RECOMMENDATION, (Thing,))

            saf_class = types.new_class(name_saf_formated, (Saf_conflict_recommendation,))
            sec_class = types.new_class(name_sec_formated, (Sec_conflict_mechanism,))

            if conf_reinf == "C":
                list_of_conflict = General_tools.find_class_for_object_property_of_class(onto, name_saf_formated, Constant.IS_SAF_SEC_CONFLICT)
            elif conf_reinf == "R":
                list_of_conflict = General_tools.find_class_for_object_property_of_class(onto, name_saf_formated, Constant.IS_SAF_SEC_REINFORCEMENT)

            list_of_conflict.append(sec_class)
            if conf_reinf == "C":
                saf_class.is_saf_sec_conflict = list_of_conflict
            elif conf_reinf == "R":
                saf_class.is_saf_sec_reinforcement = list_of_conflict
        onto.save(file = Constant.BIN_PATH, format = "rdfxml")
    except:
        print("Erro to add " + name_saf + " and " + name_sec)
        result = False
    return True

def remove_conflict_safety(onto, name_saf):
    result = True
    try:
        name_saf_formated = " ".join(name_saf.split()).replace(" ", "_").lower()
        with onto:
            # class Saf_conflict_recommendation(Thing): pass
            Saf_conflict_recommendation = types.new_class(Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION, (Thing,))
            saf_class = types.new_class(name_saf_formated, (Saf_conflict_recommendation,))
            destroy_entity(saf_class)
        onto.save(file=Constant.BIN_PATH, format="rdfxml")
    except:
        print("Erro to delete " + name_saf)
        result = False
    return result

def update_conflict_safety(onto, name_old, name_new):
    try:
        name_old_formated = " ".join(name_old.split()).replace(" ", "_").lower()
        name_new_formated = " ".join(name_new.split()).replace(" ", "_").lower()
        list_conflicts_old = General_tools.find_class_for_object_property_of_class(onto, name_old_formated, Constant.IS_SAF_SEC_CONFLICT)
        with onto:
            # class Saf_conflict_recommendation(Thing): pass
            Saf_conflict_recommendation = types.new_class(Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION, (Thing,))

            old_class = types.new_class(name_old_formated, (Saf_conflict_recommendation,))
            destroy_entity(old_class)
            new_class = types.new_class(name_new_formated, (Saf_conflict_recommendation,))
            if len(list_conflicts_old) > 0:
                new_class.is_saf_sec_conflict = list_conflicts_old
        onto.save(file=Constant.BIN_PATH, format="rdfxml")
    except:
        print("Erro to update " + name_old)
        return False
    return True

def remove_conflict_security(onto, name_sec):
    result = True
    try:
        name_sec_formated = " ".join(name_sec.split()).replace(" ", "_").lower()

        with onto:
            # class Sec_conflict_mechanism(Thing): pass
            Sec_conflict_mechanism = types.new_class(Constant.SEC_CONFLICT_REINFORCEMENT_RECOMMENDATION, (Thing,))

            sec_class = types.new_class(name_sec_formated, (Sec_conflict_mechanism,))
            destroy_entity(sec_class)
        onto.save(file=Constant.BIN_PATH, format="rdfxml")
    except:
        print("Erro to delete " + name_sec)
        result = False
    return result

# def find_conflict_safet_security(onto, string_to_find):
#     string_cleaned = " ".join(string_to_find.split())
#     string_formated = string_cleaned.replace(" ", "_").lower()
#     list_of_conflicts = General_tools.find_for_object_property_of_class(onto, string_formated, Constant.IS_SAF_SEC_CONFLICT)
#     list_of_conflicts.sort(key=lambda x: x.word)
#     return list_of_conflicts

def find_only_subclass_safet_security(onto, is_saf_sec):
    option = Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION
    if is_saf_sec == Constant.SECURITY:
        option = Constant.SEC_CONFLICT_REINFORCEMENT_RECOMMENDATION

    list_result = General_tools.find_safety_security_only_subclass(onto, option)
    list_result.sort(key=lambda x: x.word)
    return list_result

def find_conflict_relations_safet_security(onto, id_project):
    list_onto_conflicts = General_tools.find_safety_security_conflicts_subclass(onto)
    list_onto_conflicts = DB_Conflict.select_count_conflict_safety_security(list_onto_conflicts, id_project)
    list_onto_conflicts.sort(key=lambda x: x.word)
    return list_onto_conflicts

def find_reinforcement_relations_safet_security(onto, id_project):
    list_onto_reinforcement = General_tools.find_safety_security_reinforcements_subclass(onto)
    list_onto_reinforcement = DB_Conflict.select_count_conflict_safety_security(list_onto_reinforcement, id_project)
    list_onto_reinforcement.sort(key=lambda x: x.word)
    return list_onto_reinforcement

def find_safety_suggestions(id_project):
    list_saf_aux = DB_Conflict.select_distinct_safety_recommendation(id_project)
    list_saf_sugg = list(dict.fromkeys(list_saf_aux))

    list_sec_aux = DB_Conflict.select_distinct_security_recommendation(id_project)
    list_sec_sugg = list(dict.fromkeys(list_sec_aux))

    return list_saf_sugg, list_sec_sugg

def verify_property_between_two_classes(onto, f_class, s_class):
    f_class = " ".join(f_class.split()).replace(" ", "_").lower()
    s_class = " ".join(s_class.split()).replace(" ", "_").lower()

    c = General_tools.find_object_property_between_two_class(onto, f_class, s_class, Constant.IS_SAF_SEC_CONFLICT)
    r = General_tools.find_object_property_between_two_class(onto, f_class, s_class, Constant.IS_SAF_SEC_REINFORCEMENT)

    return c, r

def inverse_concept_exist(onto, name_saf, name_sec):
    saf_result = False
    sec_result = False
    try:
        name_saf_formated = " ".join(name_saf.split()).replace(" ", "_").lower()
        name_sec_formated = " ".join(name_sec.split()).replace(" ", "_").lower()

        saf_result = General_tools.string_is_in_subclass(onto, Constant.SEC_CONFLICT_REINFORCEMENT_RECOMMENDATION, name_saf_formated)
        sec_result = General_tools.string_is_in_subclass(onto, Constant.SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION, name_sec_formated)
    except:
        print("Erro to update")
    return saf_result, sec_result

def update_properties_conflict_safety_security(onto, name_saf, name_sec, opt):
    try:
        option = Constant.IS_SAF_SEC_CONFLICT
        if opt == "R":
            option = Constant.IS_SAF_SEC_REINFORCEMENT

        name_saf_formated = " ".join(name_saf.split()).replace(" ", "_").lower()
        name_sec_formated = " ".join(name_sec.split()).replace(" ", "_").lower()

        list_of_conflict = General_tools.find_safety_security_conflicts_subclass_EXCEPTION(onto, name_saf_formated, name_sec_formated, option)

        with onto:
            for concept in list_of_conflict:
                if opt == "C":
                    concept.onto_class.is_saf_sec_conflict = concept.list_of_conflicts
                elif opt == "R":
                    concept.onto_class.is_saf_sec_reinforcement = concept.list_of_conflicts
        onto.save(file=Constant.BIN_PATH, format="rdfxml")

    except:
        print("Erro to update")
        return False

    return True

