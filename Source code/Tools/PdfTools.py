from datetime import datetime

import Constant
from Database import DB
from Database.business import DB_Bus_Requirement
from Database.performance import DB_Pef_Performance_Resource, DB_Sec_Pef_Requirement, DB_Pef_Res_Requirement
from Database.safety import DB_Loss_Scenario_Req, DB_Hazards, DB_Components_Links, DB_Components, DB_Losses, \
    DB_Safety_Constraints, DB_Variables, DB_Projects, DB_Goals, DB_Actions_Components, DB_Assumptions, DB_UCA, \
    DB_Responsibility, DB_Project_Files
# from dist.app.reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Image
from reportlab.lib import utils
# from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph

pdf_report_list = []

def Generate_PDF(id_project):
    global pdf_report_list

    try:
        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK_FILE)

        path_report = Constant.PATH_REPORT + "STPA_report_" + current_date + ".pdf"

        load_STPA_report(id_project, now.strftime(Constant.DATETIME_MASK))

        SimpleDocTemplate(path_report, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18).build(pdf_report_list)

        return "New STPA report created.\n\nYou can se the report at " + path_report + "."
    except Exception as e:
        print(e)
        return "Error" + str(e)

def Generate_PDF_STRIDE(id_project):
    global pdf_report_list

    try:
        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK_FILE)

        path_report = Constant.PATH_REPORT + "STRIDE_report_" + current_date + ".pdf"

        load_STRIDE_report(id_project, now.strftime(Constant.DATETIME_MASK))

        SimpleDocTemplate(path_report, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18).build(pdf_report_list)

        return "New STRIDE report created.\n\nYou can se the report at " + path_report + "."
    except Exception as e:
        print(e)
        return "Error" + str(e)

def Generate_PDF_Performance(id_project):
    global pdf_report_list

    try:
        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK_FILE)

        path_report = Constant.PATH_REPORT + "Performance_report_" + current_date + ".pdf"

        load_performance_report(id_project, now.strftime(Constant.DATETIME_MASK))

        SimpleDocTemplate(path_report, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18).build(pdf_report_list)

        return "New Performance report created.\n\nYou can se the report at " + path_report + "."
    except Exception as e:
        print(e)
        return "Error" + str(e)

def get_label_14_title(text):
    global pdf_report_list
    ptext = '<font size="14"><br/><br/><strong>' + text + '</strong></font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 12))

def get_label_12_bold_subtitle(text):
    global pdf_report_list
    ptext = '<font size="12"><strong>' + text + '</strong></font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 12))

def get_label_12_text(text):
    global pdf_report_list
    ptext = '<font size="12">  ' + text + '</font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 24))

def get_label_11_text(text):
    global pdf_report_list
    ptext = '<font size="11">&nbsp;&nbsp;&nbsp;' + text + '</font>'
    pdf_report_list.append(Paragraph(ptext))
    pdf_report_list.append(Spacer(1, 12))

def get_image(path):
    global pdf_report_list
    width = 400

    try:
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        f_image = Image(path, width=width, height=(width * aspect))
        pdf_report_list.append(f_image)
        pdf_report_list.append(Spacer(1, 12))
    except Exception as e:
        print(e)
        ptext = '<font size="11">&nbsp;&nbsp;&nbsp; Error to load image</font>'
        pdf_report_list.append(Paragraph(ptext))
        pdf_report_list.append(Spacer(1, 12))

def load_STPA_report(id_project, current_date):
    global pdf_report_list

    pdf_report_list = []

    list_goals_fifth = DB_Goals.select_all_goals_by_project(id_project)
    list_assumptions_fifth = DB_Assumptions.select_all_assumptions_by_project(id_project)
    list_losses_fifth = DB_Losses.select_all_losses_by_project(id_project)
    list_hazards_fifth = DB_Hazards.select_all_hazards_by_project(id_project)
    list_constraints_fifth = DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project)

    project = DB_Projects.select_project_by_id(id_project)
    get_label_14_title("STPA analysis of " + project.name)
    get_label_12_text(project.description)
    get_label_12_text("Begin date: " + project.begin_date)
    get_label_12_text("Report created at: " + current_date)
    # get_label_12_text("Last update: " + project.edited_date))

    # step one
    get_label_14_title("<br/><br/>Step One - Purpose of the Analysis")
    get_label_12_bold_subtitle("Goals")
    for pos in range(len(list_goals_fifth)):
        get_label_11_text(
            "G-" + str(list_goals_fifth[pos].id_goal) + ": " + list_goals_fifth[pos].description)

    get_label_12_bold_subtitle("Assumptions")
    for pos in range(len(list_assumptions_fifth)):
        get_label_11_text("A-" + str(list_assumptions_fifth[pos].id_assumption) + ": " + list_assumptions_fifth[pos].description)

    get_label_12_bold_subtitle("Losses")
    for pos in range(len(list_losses_fifth)):
        get_label_11_text("L-" + str(list_losses_fifth[pos].id_loss) + ": " + list_losses_fifth[pos].description)

    get_label_12_bold_subtitle("System-level Hazards")
    for pos in range(len(list_hazards_fifth)):
        text = ""
        for loss in list_hazards_fifth[pos].list_of_loss:
            text += "[L-" + str(loss.id_loss_screen) + "] "

        get_label_11_text(
            "H-" + str(list_hazards_fifth[pos].id_hazard) + ": " + list_hazards_fifth[pos].description + " " + text)

    get_label_12_bold_subtitle("Systel-level Safety Constraints")
    for pos in range(len(list_constraints_fifth)):
        text = ""
        for haz in list_constraints_fifth[pos].list_of_hazards:
            text += "[H-" + str(haz.id_haz_screen) + "] "

        get_label_11_text(
            "SSC-" + str(list_constraints_fifth[pos].id_safety_constraint) + ": " + list_constraints_fifth[pos].description + " " + text)

    # step 2
    get_label_14_title("<br/><br/>Step Two - Control Structure")
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CONTROLLER, id_project), Constant.DB_ID_CONTROLLER)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_ACTUATOR, id_project), Constant.DB_ID_ACTUATOR)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_SENSOR, id_project), Constant.DB_ID_SENSOR)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_EXT_INFORMATION, id_project), Constant.DB_ID_EXT_INFORMATION)
    get_component_report(id_project, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP, id_project), Constant.DB_ID_CP)

    # step 3
    get_label_14_title("<br/>Step Three - Unsafe Control Actions")
    get_label_12_bold_subtitle("Unsafe Control Actions (UCA) and Safety Constraints (SC)")
    count_usc = 0
    list_aux_uca = DB_UCA.select_all(id_project)
    for uca in list_aux_uca:
        count_usc += 1

        text_context = ""
        for context in uca.context_list:
            if text_context != "":
                text_context += ", "
            text_context += context.variable_name + " is " + context.variable_value

        text_haz = ""
        for haz in uca.hazard_list:
            text_haz += "[H-"
            id_hz = 1

            for pos in range(len(list_hazards_fifth)):
                if list_hazards_fifth[pos].id == haz.id_hazard:
                    break
                id_hz += 1
            text_haz += str(id_hz) + "]"

        item_uca_r = "Recommendation " + str(
            count_usc) + ": (Controller: " + uca.name_controller + " - Control Action: " + uca.name_action + ")"
        get_label_11_text(item_uca_r)

        item_uca_u = "UCA-" + str(count_usc) + ": " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action
        if text_context == "":
            item_uca_u += " in any context."
        else:
            item_uca_u += " when " + text_context + ". "
        item_uca_u += " " + text_haz
        get_label_11_text(item_uca_u)

        item_uca_u_desc = "Description: "
        if uca.description != None:
            item_uca_u_desc += uca.description
        get_label_11_text(item_uca_u_desc)

        item_uca_s = "SC-" + str(count_usc) + ": " + uca.name_controller + " shall " + get_opposite_uca(
            uca.id_uca_type) + " " + uca.name_action
        if text_context == "":
            item_uca_s += " in any context."
        else:
            item_uca_s += " when " + text_context + ". "

        get_label_11_text(item_uca_s)
        get_label_11_text("")

    # step 4
    get_label_14_title("Step Four - Loss Scenarios and Recommendations")
    count_ls = 0
    for rec in DB_Loss_Scenario_Req.select_all(id_project):
        count_ls += 1
        spacer = " -> "
        if Constant.ALGORITHM in rec.name_src or Constant.PROCESS_MODEL_full_name in rec.name_src:
            spacer = " in "

        get_label_11_text("R-" + str(count_ls) + " (" + rec.name_src + spacer + rec.name_dst + "): UCA-" + str(get_number_uca(rec.id_uca, list_aux_uca)))
        get_label_11_text("Type: " + rec.classification)
        get_label_11_text("Cause: " + rec.cause)
        get_label_11_text("Recommendation: " + rec.requirement)
        get_label_11_text("Mechanism: " + rec.mechanism)
        get_label_11_text("")

    # report
    get_label_14_title("\nLink with energy")
    list_omitted_links = DB_Components_Links.select_omitted_links(id_project)
    for omt in list_omitted_links:
        get_label_11_text(omt)

    get_label_14_title("\nShow control structure images")
    has_image = False

    try:
        path_one = DB_Project_Files.select_images_by_project(id_project, 1)
        if path_one != "":
            get_image(path_one)
            has_image = True
    except NameError as e:
        print(e)

    try:
        path_two = DB_Project_Files.select_images_by_project(id_project, 2)
        if path_two != "":
            get_image(path_two)
            has_image = True
    except NameError as e:
        print(e)

    try:
        path_three = DB_Project_Files.select_images_by_project(id_project, 3)
        if path_three != "":
            get_image(path_three)
            has_image = True
    except NameError as e:
        print(e)

    if not has_image:
        get_label_12_text("No control structure images found.")

def get_number_uca(id_uca, list_aux_uca):
    count = 1
    for uca in list_aux_uca:
        if uca.id == id_uca:
            return count
        count += 1
    return 0

def get_component_report(id_project, list_of_components, id_comp):
    general_name = "Component "

    if (id_comp == Constant.DB_ID_CONTROLLER):
        general_name = "Controller "
    elif (id_comp == Constant.DB_ID_ACTUATOR):
        general_name = "Actuator "
    elif (id_comp == Constant.DB_ID_SENSOR):
        general_name = "Sensor "
    elif (id_comp == Constant.DB_ID_EXT_INFORMATION):
        general_name = "External System "
    elif (id_comp == Constant.DB_ID_CP):
        general_name = "Controlled Process "

    for comp in list_of_components:
        aux_name = general_name + comp.name

        if comp.is_external_component == 1:
            aux_name += " (external of analysis)"

        get_label_12_bold_subtitle(aux_name)

        if (id_comp == Constant.DB_ID_CONTROLLER):
            get_label_12_text("Responsibilities: ")

            list_responsibility = DB_Responsibility.select_all_responsibilities_by_controller(comp.id)

            for pos in range(len(list_responsibility)):

                text = ""
                for ssc in list_responsibility[pos].list_of_ssc:
                    text += "[SSC-" + str(ssc.id_constraint_screen) + "] "

                get_label_11_text(
                    "    R-" + str(list_responsibility[pos].id_screen) + ": " + str(
                        list_responsibility[pos].description + ". " + text))

        get_label_12_text("Outgoing connections")
        for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, True):
            get_label_11_text("    " + link.name_src + " -> " + link.name_dst)
            if id_comp == Constant.DB_ID_CONTROLLER:
                get_component_report_actions(comp.id, id_project, link.id)
                get_component_report_feedback(comp.id, id_project, link.id)

        get_label_12_text("Incoming connections")
        for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, False):
            get_label_11_text("    " + link.name_src + " -> " + link.name_dst)
            if id_comp == Constant.DB_ID_CONTROLLER:
                get_component_report_actions(comp.id, id_project, link.id)
                get_component_report_feedback(comp.id, id_project, link.id)

        if (id_comp == Constant.DB_ID_CP):
            get_report_cp(id_project, comp.id)

        get_label_11_text(" ")

def get_component_report_actions(id_comp, id_project, id_link):
    list_a = DB_Actions_Components.select_actions_by_component_project_link(id_comp, id_project, id_link)
    if len(list_a) > 0:
        aux_a = ""
        for act in list_a:
            if aux_a != "":
                aux_a += ", "
            aux_a += act.name
        get_label_11_text("\tControl actions: " + aux_a)

def get_component_report_feedback(id_comp, id_project, id_link):
    list_v = DB_Variables.select_variables_with_value_by_controller_project_link(id_comp, id_project, id_link)
    if len(list_v) > 0:
        get_label_11_text("\tFeedbacks (variables and values):")
        aux_v = ""
        for var in list_v:
            aux_v = var.var_name + " ("
            add_comma = False
            for val in var.values_list:
                if add_comma:
                    aux_v += ", " + val.value
                else:
                    aux_v += val.value
                add_comma = True
            aux_v += ")"
            get_label_11_text("\t    " + aux_v)

def get_report_cp(id_project, id_father):
    text_inp = ""
    for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_INPUT):
        if text_inp != "":
            text_inp += ", "
        text_inp += comp_i

    if text_inp != "":
        get_label_11_text("Input: " + text_inp)

    text_out = ""
    for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_OUTPUT):
        if text_out != "":
            text_out += ", "
        text_out += comp_i

    if text_out != "":
        get_label_11_text("Output: " + text_out)

    text_env = ""
    for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_ENV_DISTURBANCES):
        if text_env != "":
            text_env += ", "
        text_env += comp_i

    if text_env != "":
        get_label_11_text("Environmental Disturbances: " + text_env)

def get_opposite_uca(id):
    result = ""

    if id == Constant.provided_in_wrong_order:
        result = "not provide in wrong order"
    elif id == Constant.provided_too_early:
        result = "not provide too early"
    elif id == Constant.provided_too_late:
        result = "not provide too late"
    elif id == Constant.not_provided:
        result = "provide"
    elif id == Constant.provided:
        result = "not provide"
    elif id == Constant.applied_too_long:
        result = "not provide too long"
    elif id == Constant.stopped_too_son:
        result = "not provide to soon"

    return result

def load_STRIDE_report(id_project, current_date):
    global pdf_report_list

    pdf_report_list = []

    project = DB_Projects.select_project_by_id(id_project)
    get_label_14_title("STRIDE analysis of " + project.name)
    get_label_12_text(project.description)
    get_label_12_text("Project begin date: " + project.begin_date)
    get_label_12_text("Report created at: " + current_date)
    # get_label_12_text("Last update: " + project.edited_date))

    list_controllers = DB_Components.select_controller_not_external_not_human(id_project)
    list_omitted_links = DB_Components_Links.select_omitted_links(id_project)

    # Show omitted links
    get_label_12_bold_subtitle("<br/>Physical and empty links: ")
    for omt in list_omitted_links:
        get_label_11_text(omt)

    # Show recomendations by controller and link
    for conn in list_controllers:
        get_label_12_bold_subtitle("<br/>" + conn.name)

        list_stride_links = DB_Components_Links.select_links_stride(conn.id)

        for link in list_stride_links:
            text = ""

            if link.is_hlc and len(link.list_var) > 0:
                text = " - from Controller"
            elif link.is_hlc and len(link.list_act) > 0:
                text = " - to Controller"


            if len(link.list_act) > 0 and link.is_ext == True:
                get_label_12_text("<br/>(External Communication) " + link.name_src + " -> " + link.name_dst)

            if len(link.list_act) > 0 and link.is_ext == False:
                get_label_12_text("<br/>(Control Action" + text + ") " + link.name_src + " -> " + link.name_dst)

            if len(link.list_var) > 0 and link.is_ext == True:
                get_label_12_text("<br/>(External Communication) " + link.name_src + " -> " + link.name_dst)

            if len(link.list_var) > 0 and link.is_ext == False:
                get_label_12_text("<br/>(Feedback" + text + ") " + link.name_src + " -> " + link.name_dst)


            if link.is_bound_trust == 1:
                get_label_12_text("Is in a boundary trust: YES")
            else:
                get_label_12_text("Is in a boundary trust: NO")

            list_stride_requirements = DB.DB_Sec_Stride_Requirement.select_by_id_link(link.id)
            count = 1
            get_label_11_text("\tNumber of recommendations: " + str(len(list_stride_requirements)) + "<br/>")
            for req in list_stride_requirements:
                text = ""
                if req.is_imported == True:
                    text += "(IMPORTED) "
                text += "Requirement " + str(count) + ": Priority " + req.name_priority + "<br/>"
                text += "\tComponent/Link: " + req.name_comp_link + "<br/>"
                text += "\tSTRIDE Element: " + req.name_stride + "<br/>"
                text += "\tAnalysed as DFD Element: " + req.name_dfd + "<br/>"
                text += "\tTitle: " + req.title + "<br/>"
                text += "\tDescription: " + req.description + "<br/>"
                text += "\tRecommendation: " + req.justification + "<br/>"
                text += "\tMechanism: " + req.mechanism + "<br/>"

                #controls = ""
                #for ctrl in req.list_of_controls:
                #    if controls != "":
                #        controls += "; "
                #    controls += ctrl.name
                #text += "\tSelected controls: " + controls + "<br/>"

                count += 1
                get_label_11_text(text)

def load_performance_report(id_project, current_date):
    global pdf_report_list

    pdf_report_list = []
    space = "    "
    spaceBR = "<br/>    "

    project = DB_Projects.select_project_by_id(id_project)
    get_label_14_title("Performance analysis of " + project.name)
    get_label_12_text(project.description)
    get_label_12_text("Project begin date: " + project.begin_date)
    get_label_12_text("Report created at: " + current_date)

    list_controllers = DB_Components.select_controller_not_external_not_human(id_project)
    list_resource = DB_Pef_Performance_Resource.select_all()

    project = DB_Projects.select_project_by_id(id_project)
    get_label_14_title(project.name)
    get_label_12_text(project.description)
    get_label_12_text("Begin date: " + project.begin_date)

    # Safety
    get_label_14_title("Safety")
    count = 1
    for c in list_controllers:
        get_label_12_bold_subtitle("<br/>" + c.name)

        for res in list_resource:
            list_saf_conflict = DB_Loss_Scenario_Req.select_requirements_by_controller_resource(c.id, res.id)
            get_label_12_text(space + res.name)

            for sf_rq in list_saf_conflict:
                text = "R_Saf - " + str(count) + " >> " + sf_rq.name_cause
                text += spaceBR + "Cause: " + sf_rq.cause + spaceBR + "Requirement: " + sf_rq.requirement
                text += spaceBR + "Mechanism: " + sf_rq.mechanism
                text += spaceBR + "Performance Requirement: " + sf_rq.performance_req
                for rq in sf_rq.list_res:
                    text += spaceBR + rq.res_name + ": " + rq.requirement
                get_label_11_text(text + "<br/>")
                count += 1

    # Security
    get_label_14_title("Security")
    count = 1
    for c in list_controllers:
        get_label_12_bold_subtitle(spaceBR + c.name)

        for res in list_resource:
            get_label_12_text(spaceBR + res.name)
            list_sec_conflict = DB_Sec_Pef_Requirement.select_by_controller_resource(c.id, res.id)

            for sc_rq in list_sec_conflict:
                text = "R_Sec - " + str(count) + " >> " + sc_rq.name_stride + " (Priority: " + sc_rq.name_priority + ")"
                text += spaceBR + "Cause: " + sc_rq.description
                text += spaceBR + "Requirement: " + sc_rq.justification
                text += spaceBR + "Mechanism: " + sc_rq.mechanism
                text += spaceBR + "Performance Requirement: " + sc_rq.performance_req
                for rq in sc_rq.list_res:
                    text += spaceBR + rq.res_name + ": " + rq.requirement

                get_label_11_text(text + "<br/>")
                count += 1

    # Business
    get_label_14_title("Business")
    count = 1
    for c in list_controllers:
        get_label_12_bold_subtitle(spaceBR + c.name)

        for res in list_resource:
            get_label_12_text(spaceBR + res.name)
            list_bus_conflict = DB_Bus_Requirement.load_business_requirement_by_resource(c.id, id_project, res.id)

            for bus_rq in list_bus_conflict:
                text = "R_Bus - " + str(count) + " >> " + bus_rq.name_component
                text += spaceBR + "Requirement: " + bus_rq.requirement
                text += spaceBR + "Performance Requirement: " + bus_rq.performance_req
                for bus in bus_rq.list_res:
                    text += spaceBR + bus.res_name + ": " + bus.requirement

                get_label_11_text(text + "<br/>")
                count += 1

    # Performance
    get_label_14_title("Performance")
    count = 1
    for c in list_controllers:
        get_label_12_bold_subtitle(spaceBR + c.name)
        list_conflict_pef_resource_requirement = DB_Pef_Res_Requirement.select_by_controller(c.id)

        for req in list_conflict_pef_resource_requirement:
            text = "RQ-" + str(count) + ": " + req.res_name + " >> " + req.requirement
            get_label_11_text(text + "<br/>")
            count += 1