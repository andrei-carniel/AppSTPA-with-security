from PyQt5.QtCore import QRect

from Database.business import DB_Bus_Requirement
from Database.performance import DB_Saf_Pef_Requirement, DB_Pef_Performance_Resource, DB_Sec_Pef_Requirement, \
    DB_Bus_Pef_Requirement, DB_Pef_Res_Requirement
from Database.security import DB_Sec_Stride_Priority, DB_Sec_Stride_Requirement, DB_Sec_Stride_DFD, \
    DB_Sec_Stride_Requirement_Import
from Objects.Responsibility import Responsibility, Responsibility_ssc
from owlready2 import *
import os

from PyQt5 import QtWidgets, QtGui

import Constant
import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QMessageBox, QWidget, QComboBox, QAbstractItemView, QLabel, \
    QMainWindow, QTableWidgetItem, QPushButton, QVBoxLayout, QDialog, QHBoxLayout, QDialogButtonBox, QAction, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QFont

from Objects.Action import Action_Component
from Objects.Assumptions import Assumptions
from Objects.Component import Component
from Objects.Loss_Scenario_Req import Loss_Scenario_Req
from Objects.Project import Project
from Objects.Var_Values_Aux import Var_Values_Aux
from Objects.Variable_Values import Variable_Values
from Objects.Variables import Variables
from Tools.PdfTools import Generate_PDF, Generate_PDF_STRIDE, Generate_PDF_Performance
from ui_mainwindow import Ui_MainWindow

from datetime import datetime

# define the object to access the ontology
from Database import DB
from Database.safety import DB_Loss_Scenario_Req, DB_Hazards, DB_Components_Links, DB_Components, DB_Losses, \
    DB_Safety_Constraints, DB_Variables, DB_Variables_Values, DB_Projects, DB_Goals, DB_Actions_Components, \
    DB_Assumptions, DB_UCA, DB_Project_Files, DB_Responsibility
from Objects.Goal import Goal
from Objects.Hazard import Hazard, Hazard_Loss
from Objects.Loss import Loss
from Objects.Safety_Constraint import Safety_Constraint, Safety_Constraint_Hazard
from Tools import Dictionary, General_tools, Safety_tools_new, Security_tools_new

from shutil import copyfile

Dictionary.init_default_elements_dictionary()
# Dictionary.init_elements_dictionary()
Dictionary.init_safety_elements_dictionary()

# Compile the interface:
# pip install pyuic5-tool
# pyuic5 -x mainwindow.ui -o ui_mainwindow.py

# Generate installer
# pip install pyinstaller
# pyinstaller app.py
# pyinstaller --paths .\venv\Lib\site-packages\ app.py
# pyinstaller --onefile --paths .\venv\Lib\site-packages\ app.py

# MAIN VARS
# owlready2.JAVA_EXE = Constant.JAVA_PATH
onto = owlready2.get_ontology(Constant.BIN_PATH).load(reload=True)

id_project = -1

# FIRST STEP VARS
list_projects = []
list_goals = []
list_assumptions = []
list_losses = []
list_hazards = []
list_constraints = []

# SECOND STEP VARS
list_component_controller = []
list_component_controller_variables = []
list_component_controller_variables_values = []
list_component_exti = []
list_component_actuator = []
list_component_sensor = []
list_component_exts = []
list_component_controlled_process = []
list_component_controlled_process_variables = []
list_component_controlled_process_variables_values = []
list_controlled_process_envd = []
list_controlled_process_input = []
list_controlled_process_output = []
list_controlled_process_env_dist = []
list_controlled_process_envd_variables = []
list_controlled_process_input_variables = []
list_controlled_process_envd_variables_values = []
list_controlled_process_input_variables_values = []
list_controlled_process_output_variables = []
list_controlled_process_output_variables_values = []
list_control_actions = []
list_links_controller = []
list_links_exts = []
list_links_actuator = []
list_links_sensor = []
list_links_controlled_process = []
list_connection_controller = []
list_connection_exts = []
list_connection_actuator = []
list_connection_sensor = []
list_connection_controlled_process = []
list_links_variable_controller = []
list_links_actions_controller = []
list_controller_hlcs = []
list_controller_hlcs_links = []
list_second_responsibility = []
list_second_responsibility_ssc = []

# THIRD STEP VARS
list_three_controller = []
list_three_control_action = []
list_third_var_comp = []
list_third_uca = []
list_third_uca_cell = []
list_third_uca_safe = []
list_third_context = []
list_third_uca_type = []
list_third_uca_type_description = []
list_third_hazard = []
listwidget_third_hazard = None
list_third_uca_warning = []
third_uca_description = ""

# FOURTH STEP VARS
list_four_controller = []
list_four_control_action = []
list_four_uca = []
list_four_loss_causal = []
list_four_requirements = []

# STRIDE ANALYSIS
list_stride_controller = []
list_stride_links = []
list_stride_threats = []
list_stride_threat_priority = []
list_stride_requirements = []
# list_stride_requirements_to_import = []

# DFD analysis
list_dfd_elements = []
list_dfd_links = []
list_dfd_category = []


# Business analysis
list_business_controller = []
list_business_requirement = []

# Performance saf analysis
list_saf_pef_controller = []
list_saf_pef_uca = []
list_saf_pef_resource = []
list_saf_pef_requirement = []
list_saf_pef_res_requirement = []

# Pef sec analysis
list_sec_pef_controller = []
list_sec_pef_priority = []
list_sec_pef_resource = []
list_sec_pef_requirement = []
list_sec_pef_res_requirement = []

# Pef bus analysis
list_bus_pef_controller = []
list_bus_pef_requirement = []
list_bus_pef_resource = []
list_bus_pef_res_requirement = []

# Pef conflict analysis
list_conflict_pef_controller = []
list_conflict_pef_resource = []
list_saf_conflict = []
list_sec_conflict = []
list_bus_conflict = []
list_conflict_pef_resource_requirement = []


qss_black = """
                QGroupBox {
                    border: 2px solid black;
                    border-radius: 5px;
                    margin-top: 0.5em;
                    color : black;
                    font-size: 11pt;
                }

                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                """
# font-size: 15px;
qss_red = """
                QGroupBox {
                    border: 2px solid red;
                    border-radius: 5px;
                    margin-top: 0.5em;
                    color : red;
                    font-size: 11pt;
                }

                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                """
need_update_stride_link = False
need_update_stride_dfd = False


def clear_var_step_one():
    # FIRST STEP VARS
    global list_projects, list_goals, list_assumptions, list_losses, list_hazards, list_constraints

    list_projects = []
    list_goals = []
    list_assumptions = []
    list_losses = []
    list_hazards = []
    list_constraints = []

def clear_var_step_two():
    # SECOND STEP VARS
    global list_component_controller, list_component_controller_variables, list_component_controller_variables_values, list_component_exti, \
        list_component_actuator, list_component_sensor, list_component_exts, list_component_controlled_process, list_component_controlled_process_variables, \
        list_component_controlled_process_variables_values, list_controlled_process_envd, list_controlled_process_input, list_controlled_process_output, \
        list_controlled_process_env_dist, list_controlled_process_envd_variables, list_controlled_process_input_variables, list_controlled_process_envd_variables_values, \
        list_controlled_process_input_variables_values, list_controlled_process_output_variables, list_controlled_process_output_variables_values, list_control_actions, \
        list_links_controller, list_links_exts, list_links_actuator, list_links_sensor, list_links_controlled_process, list_connection_controller, list_connection_exts, \
        list_connection_actuator, list_connection_sensor, list_connection_controlled_process, list_links_variable_controller, list_links_actions_controller, \
        list_controller_hlcs, list_controller_hlcs_links

    list_component_controller = []
    list_component_controller_variables = []
    list_component_controller_variables_values = []
    list_component_exti = []
    list_component_actuator = []
    list_component_sensor = []
    list_component_exts = []
    list_component_controlled_process = []
    list_component_controlled_process_variables = []
    list_component_controlled_process_variables_values = []
    list_controlled_process_envd = []
    list_controlled_process_input = []
    list_controlled_process_output = []
    list_controlled_process_env_dist = []
    list_controlled_process_envd_variables = []
    list_controlled_process_input_variables = []
    list_controlled_process_envd_variables_values = []
    list_controlled_process_input_variables_values = []
    list_controlled_process_output_variables = []
    list_controlled_process_output_variables_values = []
    list_control_actions = []
    list_links_controller = []
    list_links_exts = []
    list_links_actuator = []
    list_links_sensor = []
    list_links_controlled_process = []
    list_connection_controller = []
    list_connection_exts = []
    list_connection_actuator = []
    list_connection_sensor = []
    list_connection_controlled_process = []
    list_links_variable_controller = []
    list_links_actions_controller = []
    list_controller_hlcs = []
    list_controller_hlcs_links = []

def clear_var_step_three():
    # THIRD STEP VARS
    global list_three_controller, list_three_control_action, list_third_var_comp, list_third_uca, list_third_uca_cell, list_third_uca_safe, list_third_context,\
            list_third_uca_type, list_third_uca_type_description, list_third_hazard, listwidget_third_hazard, list_third_uca_warning

    list_three_controller = []
    list_three_control_action = []
    list_third_var_comp = []
    list_third_uca = []
    list_third_uca_cell = []
    list_third_uca_safe = []
    list_third_context = []
    list_third_uca_type = []
    list_third_uca_type_description = []
    list_third_hazard = []
    listwidget_third_hazard = None
    list_third_uca_warning = []

def clear_var_step_four():
    # FOURTH STEP VARS
    global list_four_controller, list_four_control_action, list_four_uca, list_four_loss_causal, list_four_requirements

    list_four_controller = []
    list_four_control_action = []
    list_four_uca = []
    list_four_loss_causal = []
    list_four_requirements = []

class LoadingScreen(QWidget):
    def __init__(self):
        super(LoadingScreen, self).__init__()
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)
        self.movie = QMovie(Constant.GIF_LOADING_PATH)
        self.label_animation.setMovie(self.movie)

        self.startAnimation()
        # timer = QTimer(self)
        # timer.singleShot(3000, self.stopAnimation)
        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()

class OpDialog(QDialog):
    "A Dialog to set input and output ranges for an optimization."

    def __init__(self, *args, **kwargs):
        "Create a new dialogue instance."
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Create new UCA by the cell")
        self.gui_init()

    def gui_init(self):
        global list_third_hazard

        row_1 = QVBoxLayout()
        row_1.addWidget(QLabel("Select at least one hazard:"))
        row_1.addStretch()
        self.listWidget = QListWidget()

        for haz in list_third_hazard:
            self.listWidget.addItem("H-" + str(haz.id_hazard) + ": " + haz.description)

        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        row_1.addWidget(self.listWidget)
        self.resize(1050, 250)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

class ProjectDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Adding new project")
        self.gui_init()

    def gui_init(self):
        global list_third_hazard

        row_1 = QVBoxLayout()
        row_1.addWidget(QLabel("Fill all the fields to create a new project"))
        row_1.addStretch()

        # Add label
        self.ln = QLabel(self)
        self.ln.move(30, 62)
        self.ln.setText("Name of project")
        self.ln.resize(400, 22)

        # Add lineedit
        self.name = QtWidgets.QLineEdit(self)
        self.name.resize(400, 22)

        # Add label
        self.ld = QLabel(self)
        self.ld.move(30, 62)
        self.ld.setText("Description of project")
        self.ld.resize(400, 22)

        # Add lineedit
        self.description = QtWidgets.QLineEdit(self)
        self.description.resize(400, 22)

        row_1.addWidget(self.ln)
        row_1.addWidget(self.name)
        row_1.addWidget(self.ld)
        row_1.addWidget(self.description)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        self.resize(800, 150)

class CausalFactorDialog(QDialog):

    d_cause = ""
    d_recommendation = ""
    d_mechanism = ""
    d_source = ""
    d_destiny = ""
    d_comp_cause = ""
    d_show_pef_req = False
    d_pef_req = ""

    def __init__(self, cause, recommendation, mechanism, source, destiny, comp_cause, show_pef_requirement, pef_requirement):
        super().__init__()
        self.setWindowTitle("Adding new recommendation")
        self.d_cause = cause
        self.d_recommendation = recommendation
        self.d_mechanism = mechanism
        self.d_source = source
        self.d_destiny = destiny
        self.d_comp_cause = comp_cause
        self.d_show_pef_req = show_pef_requirement
        self.d_pef_req = pef_requirement
        self.gui_init()

    def gui_init(self):
        global list_third_hazard
        default_font = QFont('Arial', 11)

        instructions = "Fill all the fields to create a new recommendation\n"

        if self.d_source != "" or self.d_destiny != "": #or self.d_comp_cause != "":
            if self.d_source == self.d_destiny:
                instructions += "\nElement: " + self.d_source + "\n" #+ "\nCause: " + self.d_comp_cause
            else:
                instructions += "\nInteraction: " + self.d_source + " -> " + self.d_destiny + "\n" #+ "\nCause: " + self.d_comp_cause

        row_1 = QVBoxLayout()
        row_1.addStretch()

        # Add label
        self.li = QLabel(self)
        self.li.move(30, 62)
        self.li.setFont(default_font)
        self.li.setText(instructions)
        self.li.resize(400, 22)

        # Add label
        self.ln = QLabel(self)
        self.ln.move(30, 62)
        self.ln.setFont(default_font)
        self.ln.setText("Cause")
        self.ln.resize(400, 22)

        # Add lineedit
        self.cause = QtWidgets.QTextEdit(self)
        self.cause.setWordWrapMode(True)
        self.cause.setFont(default_font)
        self.cause.setText(self.d_cause)
        self.cause.resize(400, 22)

        # Add label
        self.ld = QLabel(self)
        self.ld.move(30, 62)
        self.ld.setFont(default_font)
        self.ld.setText("Recommendation (use the following structure):")
        self.ld.resize(400, 22)

        # self.lne = QLabel(self)
        # self.lne.move(30, 62)
        # self.lne.setFont(default_font)
        # self.lne.setText("ELEMENT + MODAL VERB + RECOMMENDATION + SUBORDINATING CONJUNCTION + CONDITION \n")
        # self.lne.setAlignment(Qt.AlignCenter)
        # self.lne.resize(400, 22)
        #
        # self.lnr = QLabel(self)
        # self.lnr.move(30, 62)
        # self.lnr.setFont(default_font)
        # self.lnr.setText("ELEMENT: controller / control action / actuator / ...\n"
        #                  "MODAL VERBS: must / shall \n"
        #                  "RECOMMENDATION: have / be + something to do or be\n"
        #                  "SUBORDINATING CONJUNCTION: when / before / after / while\n"
        #                  "CONDITION: or restriction\n")
        # self.lnr.resize(400, 22)

        # Add lineedit
        self.requirement = QtWidgets.QTextEdit(self)
        self.requirement.setWordWrapMode(True)
        self.requirement.setFont(default_font)
        self.requirement.setText(self.d_recommendation)
        self.requirement.resize(400, 22)

        self.lnm = QLabel(self)
        self.lnm.move(30, 62)
        self.lnm.setFont(default_font)
        self.lnm.setText("Mechanism")
        self.lnm.resize(400, 22)

        # Add lineedit
        self.mechanism = QtWidgets.QTextEdit(self)
        self.mechanism.setWordWrapMode(True)
        self.mechanism.setFont(default_font)
        self.mechanism.setText(self.d_mechanism)
        self.mechanism.resize(400, 22)

        row_1.addWidget(self.li)
        row_1.addWidget(self.ln)
        row_1.addWidget(self.cause)
        row_1.addWidget(self.ld)
        row_1.addWidget(self.requirement)
        row_1.addWidget(self.lnm)
        row_1.addWidget(self.mechanism)

        if self.d_show_pef_req:
            self.lpr = QLabel(self)
            self.lpr.move(30, 62)
            self.lpr.setFont(default_font)
            self.lpr.setText("Safety Performance Requirement")
            self.lpr.resize(400, 22)

            # Add lineedit
            self.pef_req = QtWidgets.QTextEdit(self)
            self.pef_req.setWordWrapMode(True)
            self.pef_req.setFont(default_font)
            self.pef_req.setText(self.d_pef_req)
            self.pef_req.resize(400, 22)

            row_1.addWidget(self.lpr)
            row_1.addWidget(self.pef_req)


        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        self.resize(800, 150)

class UcaDescriptionDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Change UCA description")
        self.gui_init()

    def gui_init(self):
        global third_uca_description
        row_1 = QVBoxLayout()
        row_1.addWidget(QLabel("Fill all the fields to create a new recommendation"))
        row_1.addStretch()

        # Add label
        self.ln = QLabel(self)
        self.ln.move(30, 62)
        self.ln.setText("Description")
        self.ln.resize(400, 22)

        # Add lineedit
        # self.description = QtWidgets.QLineEdit(self)
        self.description = QtWidgets.QTextEdit(self)
        self.description.setWordWrapMode(True)
        self.description.setText(third_uca_description)
        self.description.resize(400, 22)

        row_1.addWidget(self.ln)
        row_1.addWidget(self.description)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        self.resize(800, 150)

class StrideDialog(QDialog):

    t_title = ""
    t_category = ""
    t_interaction = ""
    t_description = ""
    t_justification = ""
    t_priority = ""
    t_mechanism = ""
    t_son_list = []
    d_show_pef_req = False
    d_pef_req = ""

    def __init__(self, tit, cat, intr, desc, just, prior, mec, son_list, show_pef_requirement, pef_requirement):
        super().__init__()
        # super().__init__(*args, **kwargs)
        self.setWindowTitle("Create STRIDE recommendation")
        self.t_title = tit
        self.t_category = cat
        self.t_interaction = intr
        self.t_description = desc
        self.t_justification = just
        self.t_priority = prior
        self.t_mechanism = mec
        self.t_son_list = son_list
        self.d_show_pef_req = show_pef_requirement
        self.d_pef_req = pef_requirement
        self.gui_init()

    def gui_init(self):
        global list_stride_threat_priority
        default_font = QFont('Arial', 11)

        row_1 = QVBoxLayout()

        # Add category
        self.lnc = QLabel(self)
        self.lnc.setFont(default_font)
        self.lnc.move(30, 62)
        self.lnc.setText("Category: " + self.t_category)
        self.lnc.resize(400, 22)
        row_1.addWidget(self.lnc)

        # Add interaction
        self.lni = QLabel(self)
        self.lni.setFont(default_font)
        self.lni.move(30, 62)
        self.lni.setText("Interaction: " + self.t_interaction)
        self.lni.resize(400, 22)
        row_1.addWidget(self.lni)

        # Add title
        self.lnt = QLabel(self)
        self.lnt.setFont(default_font)
        self.lnt.move(30, 62)
        self.lnt.setText("Title:")
        self.lnt.resize(400, 22)
        self.title = QtWidgets.QLineEdit(self)
        # self.title.setWordWrapMode(True)
        self.title.setText(self.t_title)
        self.title.setFont(default_font)
        self.title.resize(400, 22)
        row_1.addWidget(self.lnt)
        row_1.addWidget(self.title)

        # Add description
        self.lnd = QLabel(self)
        self.lnd.setFont(default_font)
        self.lnd.move(30, 62)
        self.lnd.setText("Description:")
        self.lnd.resize(400, 22)
        self.description = QtWidgets.QTextEdit(self)
        self.description.setWordWrapMode(True)
        self.description.setText(self.t_description)
        self.description.setFont(default_font)
        self.description.resize(400, 22)
        row_1.addWidget(self.lnd)
        row_1.addWidget(self.description)

        # Add justification
        self.lnj = QLabel(self)
        self.lnj.setFont(default_font)
        self.lnj.move(30, 62)
        self.lnj.setText("Recommendation:")
        self.lnj.resize(400, 22)

        self.justification = QtWidgets.QTextEdit(self)
        self.justification.setText(self.t_justification)
        self.justification.setFont(default_font)
        self.justification.resize(400, 22)
        self.justification.setWordWrapMode(True)

        row_1.addWidget(self.lnj)
        # row_1.addWidget(self.lne)
        # row_1.addWidget(self.lnr)
        row_1.addWidget(self.justification)

        # Add mechanism
        self.lnm = QLabel(self)
        self.lnm.setFont(default_font)
        self.lnm.move(30, 62)
        self.lnm.setText("Mechanism: ")
        self.lnm.resize(400, 22)

        self.mechanism = QtWidgets.QTextEdit(self)
        self.mechanism.setWordWrapMode(True)
        self.mechanism.setText(self.t_mechanism)
        self.mechanism.setFont(default_font)
        self.mechanism.resize(400, 22)

        row_1.addWidget(self.lnm)
        row_1.addWidget(self.mechanism)

        if self.d_show_pef_req:
            self.lpr = QLabel(self)
            self.lpr.move(30, 62)
            self.lpr.setFont(default_font)
            self.lpr.setText("Security Performance Requirement")
            self.lpr.resize(400, 22)

            # Add lineedit
            self.pef_req = QtWidgets.QTextEdit(self)
            self.pef_req.setWordWrapMode(True)
            self.pef_req.setFont(default_font)
            self.pef_req.setText(self.d_pef_req)
            self.pef_req.resize(400, 22)

            row_1.addWidget(self.lpr)
            row_1.addWidget(self.pef_req)

        # Add priority
        self.lnp = QLabel(self)
        self.lnp.setFont(default_font)
        self.lnp.move(30, 62)
        self.lnp.setText("Priority:")
        self.lnp.resize(400, 22)
        row_1.addWidget(self.lnp)

        self.comboBox = QComboBox(self)
        self.comboBox.setFont(default_font)
        list_stride_threat_priority = DB_Sec_Stride_Priority.select_all()
        for tp in list_stride_threat_priority:
            self.comboBox.addItem(tp.name)

        self.comboBox.setCurrentIndex(self.t_priority)
        row_1.addWidget(self.comboBox)


        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        self.resize(800, 600)

class Performance_Saf_Sec_Bus(QDialog):

    t_controller = ""
    t_requirement = ""
    t_mechanism = ""
    d_show_pef_req = False
    d_pef_req = ""

    def __init__(self, ctrl, req, mech, show_pef_requirement, pef_requirement):
        super().__init__()
        # super().__init__(*args, **kwargs)
        self.setWindowTitle("Create Performance recommendation")
        self.t_controller = ctrl
        self.t_requirement = req
        self.t_mechanism = mech
        self.d_show_pef_req = show_pef_requirement
        self.d_pef_req = pef_requirement
        self.gui_init()

    def gui_init(self):
        global list_stride_threat_priority
        default_font = QFont('Arial', 11)

        row_1 = QVBoxLayout()

        # Add Controller
        self.lnc = QLabel(self)
        self.lnc.setFont(default_font)
        self.lnc.move(30, 62)
        self.lnc.setText("Controller: " + self.t_controller)
        self.lnc.resize(400, 22)
        row_1.addWidget(self.lnc)

        # Add description
        self.lnr = QLabel(self)
        self.lnr.setFont(default_font)
        self.lnr.move(30, 62)
        self.lnr.setText("Requirement:")
        self.lnr.resize(400, 22)
        self.requirement = QtWidgets.QTextEdit(self)
        self.requirement.setWordWrapMode(True)
        self.requirement.setText(self.t_requirement)
        self.requirement.setFont(default_font)
        self.requirement.resize(400, 22)
        row_1.addWidget(self.lnr)
        row_1.addWidget(self.requirement)

        # Add description
        # self.lnm = QLabel(self)
        # self.lnm.setFont(default_font)
        # self.lnm.move(30, 62)
        # self.lnm.setText("Mechanism:")
        # self.lnm.resize(400, 22)
        # self.mechanism = QtWidgets.QTextEdit(self)
        # self.mechanism.setWordWrapMode(True)
        # self.mechanism.setText(self.t_requirement)
        # self.mechanism.setFont(default_font)
        # self.mechanism.resize(400, 22)
        # row_1.addWidget(self.lnm)
        # row_1.addWidget(self.mechanism)

        if self.d_show_pef_req:
            self.lpr = QLabel(self)
            self.lpr.move(30, 62)
            self.lpr.setFont(default_font)
            self.lpr.setText("Business Performance Requirement")
            self.lpr.resize(400, 22)

            # Add lineedit
            self.pef_req = QtWidgets.QTextEdit(self)
            self.pef_req.setWordWrapMode(True)
            self.pef_req.setFont(default_font)
            self.pef_req.setText(self.d_pef_req)
            self.pef_req.resize(400, 22)

            row_1.addWidget(self.lpr)
            row_1.addWidget(self.pef_req)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        # self.setGeometry(300, 300, 800, 150)
        self.resize(800, 400)

class Pef_Resource_Requiremnt(QDialog):

    t_text = ""
    t_requirement = ""

    def __init__(self, text, req):
        super().__init__()
        # super().__init__(*args, **kwargs)
        self.setWindowTitle("Create Performance recommendation")
        self.t_text = text
        self.t_requirement = req
        self.gui_init()

    def gui_init(self):
        global list_stride_threat_priority
        default_font = QFont('Arial', 11)

        row_1 = QVBoxLayout()

        # Add Controller
        self.lnc = QLabel(self)
        self.lnc.setFont(default_font)
        self.lnc.move(30, 62)
        self.lnc.setText("Description: " + self.t_text)
        self.lnc.setWordWrap(True)
        self.lnc.resize(400, 22)
        row_1.addWidget(self.lnc)

        # Add description
        self.lnr = QLabel(self)
        self.lnr.setFont(default_font)
        self.lnr.move(30, 62)
        self.lnr.setText("Requirement:")
        self.lnr.resize(400, 22)
        self.requirement = QtWidgets.QTextEdit(self)
        self.requirement.setWordWrapMode(True)
        self.requirement.setText(self.t_requirement)
        self.requirement.setFont(default_font)
        self.requirement.resize(400, 22)
        row_1.addWidget(self.lnr)
        row_1.addWidget(self.requirement)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        # self.setGeometry(300, 300, 800, 150)
        self.resize(800, 400)

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class MainWindow:

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.label_version.setText("Version: " + Constant.VERSION)
        # self.ui.tabWidget_main.setTabEnabled(9, False)

        self.helpContentOntology = QAction("Full STPA ontology")
        self.helpContentOntology.triggered.connect(self.load_image)

        self.stpaOne = QAction("STPA Step 1 - Purpose of the analysis")
        self.stpaOne.triggered.connect(self.load_image_step_one)
        self.stpaTwo = QAction("STPA Step 2 - Control structure")
        self.stpaTwo.triggered.connect(self.load_image_step_two)
        self.stpaThree = QAction("STPA Step 3 - Unsafe Control Actions")
        self.stpaThree.triggered.connect(self.load_image_step_three)
        self.stpaFour = QAction("STPA Step 4 - Loss scenarios")
        self.stpaFour.triggered.connect(self.load_image_step_four)
        self.ui.menu_ontology_stpa.addAction(self.stpaOne)
        self.ui.menu_ontology_stpa.addAction(self.stpaTwo)
        self.ui.menu_ontology_stpa.addAction(self.stpaThree)
        self.ui.menu_ontology_stpa.addAction(self.stpaFour)
        self.ui.menu_ontology_stpa.addSeparator()
        self.ui.menu_ontology_stpa.addAction(self.helpContentOntology)


        self.strideDfd = QAction("STRIDE - DFD Mapping")
        self.strideDfd.triggered.connect(self.load_image_stride_dfd_map)
        self.strideSecurity = QAction("STRIDE - Security")
        self.strideSecurity.triggered.connect(self.load_image_stride_security)
        self.strideOntology = QAction("Full STRIDE ontology")
        self.strideOntology.triggered.connect(self.load_image_stride)
        self.ui.menu_ontology_stride.addAction(self.strideDfd)
        self.ui.menu_ontology_stride.addAction(self.strideSecurity)
        self.ui.menu_ontology_stride.addSeparator()
        self.ui.menu_ontology_stride.addAction(self.strideOntology)


        self.helpContentAbout = QAction("Information")
        self.helpContentAbout.triggered.connect(self.load_about)
        self.ui.menu_ontology_help.addAction(self.helpContentAbout)

        # self.load_projects()
        self.ui.combobox_projects.currentIndexChanged.connect(self.selection_change_project)
        self.ui.combobox_projects.wheelEvent = lambda event: None
        self.ui.button_add_projects.clicked.connect(self.on_button_add_project_clicked)
        self.ui.button_del_projects.clicked.connect(self.on_button_del_project_clicked)

        self.ui.tabWidget_main.currentChanged.connect(self.onChange_main)
        self.ui.tabWidget_safety.currentChanged.connect(self.onChange_safety)
        self.ui.tabWidget_security.currentChanged.connect(self.onChange_security)
        self.ui.tabWidget_performance.currentChanged.connect(self.onChange_performance)

        # ----- TAB Fisrt Step -----
        self.ui.list_saf_goals.clicked.connect(self.on_list_saf_goals_clicked)
        self.ui.button_saf_new_goal.clicked.connect(self.on_button_saf_new_goal_clicked)
        self.ui.button_saf_update_goal.clicked.connect(self.on_button_saf_update_goal_clicked)
        self.ui.button_saf_delete_goal.clicked.connect(self.on_button_saf_delete_goal_clicked)
        self.ui.button_saf_cancel_goal.clicked.connect(self.on_button_saf_cancel_goal_clicked)

        self.ui.list_saf_assumptions.clicked.connect(self.on_list_saf_assumptions_clicked)
        self.ui.button_saf_new_assumption.clicked.connect(self.on_button_saf_new_assumption_clicked)
        self.ui.button_saf_update_assumption.clicked.connect(self.on_button_saf_update_assumption_clicked)
        self.ui.button_saf_delete_assumption.clicked.connect(self.on_button_saf_delete_assumption_clicked)
        self.ui.button_saf_cancel_assumption.clicked.connect(self.on_button_saf_cancel_assumption_clicked)

        self.ui.list_saf_losses.clicked.connect(self.on_list_saf_losses_clicked)
        self.ui.button_saf_new_loss.clicked.connect(self.on_button_saf_new_loss_clicked)
        self.ui.button_saf_update_loss.clicked.connect(self.on_button_saf_update_loss_clicked)
        self.ui.button_saf_delete_loss.clicked.connect(self.on_button_saf_delete_loss_clicked)
        self.ui.button_saf_cancel_loss.clicked.connect(self.on_button_saf_cancel_loss_clicked)

        self.ui.list_saf_hazards.currentRowChanged.connect(self.on_list_saf_hazards_clicked)
        self.ui.button_saf_new_hazard.clicked.connect(self.on_button_saf_new_hazard_clicked)
        self.ui.button_saf_update_hazard.clicked.connect(self.on_button_saf_update_hazard_clicked)
        self.ui.button_saf_delete_hazard.clicked.connect(self.on_button_saf_delete_hazard_clicked)
        self.ui.button_saf_cancel_hazard.clicked.connect(self.on_button_saf_cancel_hazard_clicked)

        self.ui.list_saf_constraints.currentRowChanged.connect(self.on_list_saf_constraints_clicked)
        self.ui.button_saf_new_constraint.clicked.connect(self.on_button_saf_new_constraint_clicked)
        self.ui.button_saf_update_constraint.clicked.connect(self.on_button_saf_update_constraint_clicked)
        self.ui.button_saf_delete_constraint.clicked.connect(self.on_button_saf_delete_constraint_clicked)
        self.ui.button_saf_cancel_constraint.clicked.connect(self.on_button_saf_cancel_constraint_clicked)

        self.load_goals()
        self.load_assumptions()
        self.load_losses()
        self.load_hazards()
        self.load_constraints()
        # ----- TAB Fisrt Step -----

        # ----- TAB Second Step -----
        self.ui.button_add_controller.clicked.connect(self.on_button_add_controller_clicked)
        self.ui.button_update_controller.clicked.connect(self.on_button_update_controller_clicked)
        self.ui.button_delete_controller.clicked.connect(self.on_button_delete_controller_clicked)
        self.ui.button_cancel_controller.clicked.connect(self.on_button_cancel_controller_clicked)
        self.ui.listwidget_controllers.currentRowChanged.connect(self.on_listwidget_controllers_clicked)
        self.ui.button_add_controller_connection.clicked.connect(self.on_button_add_controller_connection_clicked)
        self.ui.listwidget_controller_connection.currentRowChanged.connect(self.on_listwidget_controller_connection_clicked)
        self.ui.button_delete_controller_connection.clicked.connect(self.on_button_delete_controller_connection_clicked)

        self.ui.button_add_exts.clicked.connect(self.on_button_add_exts_clicked)
        self.ui.button_update_exts.clicked.connect(self.on_button_update_exts_clicked)
        self.ui.button_delete_exts.clicked.connect(self.on_button_delete_exts_clicked)
        self.ui.button_cancel_exts.clicked.connect(self.on_button_cancel_exts_clicked)
        self.ui.listwidget_exts.currentRowChanged.connect(self.on_listwidget_exts_clicked)
        self.ui.button_add_exts_connection.clicked.connect(self.on_button_add_exts_connection_clicked)
        self.ui.listwidget_exts_connection.currentRowChanged.connect(self.on_listwidget_exts_connection_clicked)
        self.ui.button_delete_exts_connection.clicked.connect(self.on_button_delete_exts_connection_clicked)

        self.ui.button_add_actuator.clicked.connect(self.on_button_add_actuator_clicked)
        self.ui.button_update_actuator.clicked.connect(self.on_button_update_actuator_clicked)
        self.ui.button_delete_actuator.clicked.connect(self.on_button_delete_actuator_clicked)
        self.ui.button_cancel_actuator.clicked.connect(self.on_button_cancel_actuator_clicked)
        self.ui.listwidget_actuator.currentRowChanged.connect(self.on_listwidget_actuators_clicked)
        self.ui.button_add_actuator_connection.clicked.connect(self.on_button_add_actuator_connection_clicked)
        self.ui.listwidget_actuator_connection.currentRowChanged.connect(self.on_listwidget_actuator_connection_clicked)
        self.ui.button_delete_actuator_connection.clicked.connect(self.on_button_delete_actuator_connection_clicked)

        self.ui.button_add_sensor.clicked.connect(self.on_button_add_sensor_clicked)
        self.ui.button_update_sensor.clicked.connect(self.on_button_update_sensor_clicked)
        self.ui.button_delete_sensor.clicked.connect(self.on_button_delete_sensor_clicked)
        self.ui.button_cancel_sensor.clicked.connect(self.on_button_cancel_sensor_clicked)
        self.ui.listwidget_sensor.currentRowChanged.connect(self.on_listwidget_sensors_clicked)
        self.ui.button_add_sensor_connection.clicked.connect(self.on_button_add_sensor_connection_clicked)
        self.ui.listwidget_sensor_connection.currentRowChanged.connect(self.on_listwidget_sensor_connection_clicked)
        self.ui.button_delete_sensor_connection.clicked.connect(self.on_button_delete_sensor_connection_clicked)

        self.ui.button_save_controlled_process.clicked.connect(self.on_button_save_controlled_process_clicked)
        self.ui.button_edit_controlled_process.clicked.connect(self.on_button_edit_controlled_process_clicked)
        self.ui.button_delete_controlled_process.clicked.connect(self.on_button_delete_controlled_process_clicked)
        self.ui.button_cancel_controlled_process.clicked.connect(self.on_button_cancel_controlled_process_clicked)
        self.ui.button_add_controlled_process_connection.clicked.connect(self.on_button_add_controlled_process_connection_clicked)
        self.ui.listwidget_controlled_process_connection.currentRowChanged.connect(self.on_listwidget_controlled_process_connection_clicked)
        self.ui.button_delete_controlled_process_connection.clicked.connect(self.on_button_delete_controlled_process_connection_clicked)
        self.ui.listwidget_controlled_process_envd.currentRowChanged.connect(self.on_listwidget_controlled_process_envd_clicked)
        self.ui.button_add_controlled_process_envd.clicked.connect(self.on_button_add_controlled_process_envd_clicked)
        self.ui.button_update_controlled_process_envd.clicked.connect(self.on_button_update_controlled_process_envd_clicked)
        self.ui.button_delete_controlled_process_envd.clicked.connect(self.on_button_delete_controlled_process_envd_clicked)
        self.ui.button_cancel_controlled_process_envd.clicked.connect(self.on_button_cancel_controlled_process_envd_clicked)
        self.ui.listwidget_controlled_process_input.currentRowChanged.connect(self.on_listwidget_controlled_process_input_clicked)
        self.ui.button_add_controlled_process_input.clicked.connect(self.on_button_add_controlled_process_input_clicked)
        self.ui.button_update_controlled_process_input.clicked.connect(self.on_button_update_controlled_process_input_clicked)
        self.ui.button_delete_controlled_process_input.clicked.connect(self.on_button_delete_controlled_process_input_clicked)
        self.ui.button_cancel_controlled_process_input.clicked.connect(self.on_button_cancel_controlled_process_input_clicked)
        self.ui.listwidget_controlled_process_output.currentRowChanged.connect(self.on_listwidget_controlled_process_output_clicked)
        self.ui.button_add_controlled_process_output.clicked.connect(self.on_button_add_controlled_process_output_clicked)
        self.ui.button_update_controlled_process_output.clicked.connect(self.on_button_update_controlled_process_output_clicked)
        self.ui.button_delete_controlled_process_output.clicked.connect(self.on_button_delete_controlled_process_output_clicked)
        self.ui.button_cancel_controlled_process_output.clicked.connect(self.on_button_cancel_controlled_process_output_clicked)

        self.ui.combobox_second_controller.currentIndexChanged.connect(self.selection_change_controller_connection)
        self.ui.combobox_second_controller.wheelEvent = lambda event: None


        self.ui.button_saf_new_responsibility.clicked.connect(self.on_button_saf_new_responsibility_clicked)
        self.ui.button_saf_update_responsibility.clicked.connect(self.on_button_saf_update_reponsability_clicked)
        self.ui.button_saf_delete_responsibility.clicked.connect(self.on_button_saf_delete_reponsability_clicked)
        self.ui.button_saf_cancel_responsibility.clicked.connect(self.on_button_saf_cancel_responsibility_clicked)

        self.ui.list_second_responsibility.currentRowChanged.connect(self.on_list_responsibility_clicked)
        self.ui.list_second_responsibility.wheelEvent = lambda event: None

        self.ui.button_add_control_action.clicked.connect(self.on_button_add_control_action_clicked)
        self.ui.button_update_control_action.clicked.connect(self.on_button_update_control_action_clicked)
        self.ui.button_delete_control_action.clicked.connect(self.on_button_delete_control_action_clicked)
        self.ui.button_cancel_control_action.clicked.connect(self.on_button_cancel_control_action_clicked)
        self.ui.listwidget_control_actions.currentRowChanged.connect(self.on_listwidget_control_action_clicked)
        self.ui.button_add_controller_variable.clicked.connect(self.on_button_add_controller_variable_clicked)
        self.ui.button_update_controller_variable.clicked.connect(self.on_button_update_controller_variable_clicked)
        self.ui.button_delete_controller_variable.clicked.connect(self.on_button_delete_controller_variable_clicked)
        self.ui.button_cancel_controller_variable.clicked.connect(self.on_button_cancel_controller_variable_clicked)
        self.ui.listwidget_controller_variable.currentRowChanged.connect(self.on_listwidget_controller_variable_clicked)
        self.ui.button_add_controller_variable_values.clicked.connect(self.on_button_add_controller_variable_values_clicked)
        self.ui.button_update_controller_variable_values.clicked.connect(self.on_button_update_controller_variable_values_clicked)
        self.ui.button_delete_controller_variable_values.clicked.connect(self.on_button_delete_controller_variable_values_clicked)
        self.ui.button_cancel_controller_variable_values.clicked.connect(self.on_button_cancel_controller_variable_values_clicked)
        self.ui.listwidget_controller_variable_values.currentRowChanged.connect(self.on_listwidget_controller_variable_values_clicked)

        self.ui.button_structure_check.clicked.connect(self.check_control_structure)
        # ----- TAB Second Step -----

        # ----- TAB Third Step -----
        self.ui.combobox_third_controller.currentIndexChanged.connect(self.selection_change_controller_third)
        self.ui.combobox_third_controller.wheelEvent = lambda event: None
        self.ui.combobox_third_control_action.currentIndexChanged.connect(self.selection_change_control_action_third)
        self.ui.combobox_third_control_action.wheelEvent = lambda event: None
        self.ui.button_third_save_uca.clicked.connect(self.on_button_button_third_save_uca_clicked)
        self.ui.button_third_delete_uca_rule.clicked.connect(self.on_button_button_third_delete_uca_rule_clicked)
        self.ui.button_third_delete_uca_cell.clicked.connect(self.on_button_button_third_delete_uca_cell_clicked)
        self.ui.button_third_delete_uca_safe.clicked.connect(self.on_button_button_third_delete_uca_safe_clicked)


        self.ui.tablewidget_third_context.cellClicked.connect(self.cell_was_clicked)
        self.ui.listwidget_third_uca_rule.currentRowChanged.connect(self.on_listwidget_uca_rule_clicked)
        self.ui.listwidget_third_uca_cell.currentRowChanged.connect(self.on_listwidget_uca_cell_clicked)
        self.ui.listwidget_third_uca_safe.currentRowChanged.connect(self.on_listwidget_uca_safe_clicked)
        self.ui.button_third_description_uca_rule.clicked.connect(self.on_button_third_update_description_uca_rule)
        self.ui.button_third_description_uca_cell.clicked.connect(self.on_button_third_update_description_uca_cell)
        self.ui.button_third_description_uca_safe.clicked.connect(self.on_button_third_update_description_uca_safe)
        # ----- TAB Third Step -----

        # ----- TAB Fourth Step -----
        self.ui.combobox_fourth_controller.currentIndexChanged.connect(self.selection_change_controller_fourth)
        self.ui.combobox_fourth_controller.wheelEvent = lambda event: None
        self.ui.combobox_fourth_control_action.currentIndexChanged.connect(self.selection_change_control_action_fourth)
        self.ui.combobox_fourth_control_action.wheelEvent = lambda event: None
        self.ui.listwidget_fourth_uca.currentRowChanged.connect(self.selection_change_uca_fourth)
        self.ui.listwidget_fourth_uca.wheelEvent = lambda event: None
        self.ui.listwidget_fourth_requirement.itemClicked.connect(self.selection_change_requirement_fourth)
        self.ui.listwidget_fourth_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_fourth_causal_factor.currentRowChanged.connect(self.selection_change_causal_factor_fourth)
        self.ui.listwidget_fourth_causal_factor.wheelEvent = lambda event: None
        self.ui.button_fourth_add_causal_factor.clicked.connect(self.on_button_fourth_add_causal_factor_clicked)
        self.ui.button_fourth_create_causal_factor.clicked.connect(self.on_button_fourth_create_causal_factor_clicked)
        # ----- TAB Fourth Step -----

        # ----- TAB DFD elements -----
        self.ui.combobox_dfd_elements.currentIndexChanged.connect(self.selection_change_dfd_elements)
        self.ui.combobox_dfd_elements.wheelEvent = lambda event: None
        self.ui.combobox_dfd_link.currentIndexChanged.connect(self.selection_change_dfd_links)
        self.ui.combobox_dfd_link.wheelEvent = lambda event: None
        self.ui.combobox_dfd_bound_trust.wheelEvent = lambda event: None
        self.ui.button_dfd_update.clicked.connect(self.on_button_update_element_dfd_category)
        self.ui.button_dfd_update_bound_trust.clicked.connect(self.on_button_update_dfd_bound_trust)
        self.ui.button_dfd_hidden_links.clicked.connect(self.on_button_hidden_links_clicked)
        self.ui.button_dfd_link_info.clicked.connect(self.on_button_dfd_link_info_clicked)
        # ----- TAB DFD elements -----

        # ----- Functions STRIDE analysis -----
        self.ui.combobox_stride_controller.currentIndexChanged.connect(self.selection_change_controller_stride)
        self.ui.combobox_stride_controller.wheelEvent = lambda event: None
        self.ui.combobox_stride_link.currentIndexChanged.connect(self.selection_change_link_stride_board)
        self.ui.combobox_stride_link.wheelEvent = lambda event: None
        self.ui.radiobutton_stride_src.toggled.connect(self.selection_change_stride_analysis)
        self.ui.radiobutton_stride_link.toggled.connect(self.selection_change_stride_analysis)
        self.ui.radiobutton_stride_dst.toggled.connect(self.selection_change_stride_analysis)
        self.ui.button_stride_add.clicked.connect(self.add_stride_requirement)
        self.ui.listwidget_stride_threats.currentRowChanged.connect(self.on_listwidget_stride_threats_clicked)
        self.ui.listwidget_stride_threats.wheelEvent = lambda event: None
        self.ui.listwidget_stride_requirements.itemClicked.connect(self.on_listwidget_stride_requirements_clicked)
        self.ui.listwidget_stride_requirements.wheelEvent = lambda event: None
        # self.ui.listwidget_stride_requirements_import.itemClicked.connect(self.on_listwidget_stride_requirements_import_clicked)
        # self.ui.listwidget_stride_requirements_import.wheelEvent = lambda event: None
        self.ui.listwidget_stride_act.wheelEvent = lambda event: None
        self.ui.listwidget_stride_var.wheelEvent = lambda event: None
        self.ui.listwidget_stride_uca.wheelEvent = lambda event: None
        # ----- Functions STRIDE analysis -----

        # ----- Functions Business analysis -----
        self.ui.button_bus_add.clicked.connect(self.on_button_bus_add_clicked)
        # ----- Functions Business analysis -----

        # ----- TAB STPA Report -----
        self.ui.button_stpa_report_pdf.clicked.connect(self.on_button_fifith_stpa_report_clicked)
        # ----- TAB Sixth Step -----

        # ----- TAB Seventh Step -----
        self.ui.button_stride_report_pdf.clicked.connect(self.on_button_stride_report_clicked)
        # ----- TAB Seventh Step -----

        # ----- TAB Control Structure Image -----
        self.ui.button_open_file_one.clicked.connect(self.on_button_select_file_one_clicked)
        self.ui.button_open_file_two.clicked.connect(self.on_button_select_file_two_clicked)
        self.ui.button_open_file_three.clicked.connect(self.on_button_select_file_three_clicked)
        self.ui.button_delete_file_one.clicked.connect(self.on_button_delete_file_one_clicked)
        self.ui.button_delete_file_two.clicked.connect(self.on_button_delete_file_two_clicked)
        self.ui.button_delete_file_three.clicked.connect(self.on_button_delete_file_three_clicked)
        # ----- TAB Control Structure Image -----

        # ----- TAB Business Analysis -----
        self.ui.combobox_bus_controller.currentIndexChanged.connect(self.load_business_requirements)
        self.ui.combobox_bus_controller.wheelEvent = lambda event: None
        self.ui.listwidget_bus_requirements.itemClicked.connect(self.on_listwidget_bus_requirements_clicked)
        self.ui.listwidget_bus_requirements.wheelEvent = lambda event: None
        # ----- TAB Business Analysis -----

        # ----- TAB Safety Performance -----
        self.ui.combobox_saf_pef_controller.currentIndexChanged.connect(self.load_saf_pef_requirements)
        self.ui.combobox_saf_pef_controller.wheelEvent = lambda event: None
        self.ui.combobox_saf_pef_uca_type.currentIndexChanged.connect(self.load_saf_pef_requirements)
        self.ui.combobox_saf_pef_uca_type.wheelEvent = lambda event: None
        self.ui.listwidget_saf_pef_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_saf_pef_resource.wheelEvent = lambda event: None
        self.ui.listwidget_saf_pef_requirement.currentRowChanged.connect(self.load_saf_pef_res_requirement)
        self.ui.listwidget_saf_pef_resource.currentRowChanged.connect(self.load_req_saf_pef)
        self.ui.button_saf_pef_add.clicked.connect(self.add_saf_pef_res_requirement)
        self.ui.button_saf_pef_change.clicked.connect(self.change_saf_pef_res_requirement)
        self.ui.listwidget_saf_pef_res_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_saf_pef_res_requirement.itemClicked.connect(self.load_req_saf_pef_resource)
        # ----- TAB Safety Performance -----

        # ----- TAB Security Performance -----
        self.ui.combobox_sec_pef_controller.currentIndexChanged.connect(self.load_sec_pef_requirements)
        self.ui.combobox_sec_pef_controller.wheelEvent = lambda event: None
        self.ui.combobox_sec_pef_priority.currentIndexChanged.connect(self.load_sec_pef_requirements)
        self.ui.combobox_sec_pef_priority.wheelEvent = lambda event: None
        self.ui.listwidget_sec_pef_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_sec_pef_resource.wheelEvent = lambda event: None
        self.ui.listwidget_sec_pef_requirement.currentRowChanged.connect(self.load_sec_pef_res_requirement)
        self.ui.listwidget_sec_pef_resource.currentRowChanged.connect(self.load_req_sec_pef)
        self.ui.button_sec_pef_add.clicked.connect(self.add_sec_pef_res_requirement)
        self.ui.button_sec_pef_change.clicked.connect(self.change_sec_pef_res_requirement)
        self.ui.listwidget_sec_pef_res_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_sec_pef_res_requirement.itemClicked.connect(self.load_req_sec_pef_resource)
        # ----- TAB Security Performance -----

        # ----- TAB Business Performance -----
        self.ui.combobox_bus_pef_controller.currentIndexChanged.connect(self.load_bus_pef_requirement)
        self.ui.combobox_bus_pef_controller.wheelEvent = lambda event: None
        self.ui.listwidget_bus_pef_res_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_bus_pef_requirement.currentRowChanged.connect(self.load_bus_pef_res_requirement)
        self.ui.listwidget_bus_pef_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_bus_pef_resource.currentRowChanged.connect(self.load_req_bus_pef)
        self.ui.listwidget_bus_pef_resource.wheelEvent = lambda event: None
        self.ui.button_bus_pef_add.clicked.connect(self.add_bus_pef_res_requirement)
        self.ui.button_bus_pef_change.clicked.connect(self.change_bus_pef_requirement)
        self.ui.listwidget_bus_pef_res_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_bus_pef_res_requirement.currentRowChanged.connect(self.load_req_bus_pef_resource)
        # ----- TAB Business Performance -----

        # ----- TAB Conflict Performance -----
        self.ui.combobox_conflict_controller.currentIndexChanged.connect(self.load_conflict_requirement_controller)
        self.ui.combobox_conflict_controller.wheelEvent = lambda event: None
        self.ui.combobox_conflict_resource.currentIndexChanged.connect(self.load_conflict_requirement)
        self.ui.combobox_conflict_resource.wheelEvent = lambda event: None

        self.ui.listwidget_saf_conflict_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_sec_conflict_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_bus_conflict_requirement.wheelEvent = lambda event: None


        self.ui.button_conflict_saf_req.clicked.connect(self.on_button_change_saf_req)
        self.ui.button_conflict_saf_res.clicked.connect(self.on_button_change_saf_res)
        self.ui.button_conflict_sec_req.clicked.connect(self.on_button_change_sec_req)
        self.ui.button_conflict_sec_res.clicked.connect(self.on_button_change_sec_res)
        self.ui.button_conflict_bus_req.clicked.connect(self.on_button_change_bus_req)
        self.ui.button_conflict_bus_res.clicked.connect(self.on_button_change_bus_res)

        self.ui.checkbox_conflict_requirement.stateChanged.connect(self.checkbox_state_changed)
        self.ui.checkbox_conflict_mechanism.stateChanged.connect(self.checkbox_state_changed)
        self.ui.checkbox_conflict_pef_requirement.stateChanged.connect(self.checkbox_state_changed)
        self.ui.checkbox_conflict_resource.stateChanged.connect(self.checkbox_state_changed)

        self.ui.combobox_conflict_resource_performance.wheelEvent = lambda event: None
        self.ui.listwidget_conflict_resource_requirement.wheelEvent = lambda event: None
        self.ui.button_conflict_res_create.clicked.connect(self.on_button_conflict_res_create)
        self.ui.button_conflict_res_change.clicked.connect(self.on_button_conflict_res_change)
        self.ui.button_conflict_res_print_report.clicked.connect(self.on_button_conflict_res_print_report)

        # ----- TAB Conflict Performance -----


        # print("---------------------")
        # a6 = General_tools.list_subclass_with_property(onto, "Pef_DoS_performance_recommendation", "pef_identify_dos_performance_recommendation")
        # print("---------------------")

        # self.load_start_advice()

    def get_component_by_ID(self, id_comp):
        if (id_comp == Constant.DB_ID_CONTROLLER):
            return  Constant.CONTROLLER
        elif (id_comp == Constant.DB_ID_ACTUATOR):
            return Constant.ACTUATOR
        elif (id_comp == Constant.DB_ID_CP):
            return Constant.CONTROLLED_PROCESS
        elif (id_comp == Constant.DB_ID_SENSOR):
            return Constant.SENSOR
        elif (id_comp == Constant.DB_ID_INPUT):
            return Constant.INPUT
        elif (id_comp == Constant.DB_ID_OUTPUT):
            return Constant.OUTPUT
        elif (id_comp == Constant.DB_ID_EXT_INFORMATION):
            return Constant.EXTERNAL_INFORMATION
        elif (id_comp == Constant.DB_ID_ALGORITHM):
            return Constant.ALGORITHM
        elif (id_comp == Constant.DB_ID_PROCESS_MODEL):
            return Constant.PROCESS_MODEL
        elif (id_comp == Constant.DB_ID_ENV_DISTURBANCES):
            return Constant.ENVIRONMENTAL_DISTURBANCES
        elif (id_comp == Constant.DB_ID_HLC):
            return Constant.HIGH_LEVEL_CONTROLLER
        return ""

    def show(self):
        self.main_win.show()

    def load_tabwidget_main(self, tab_index):
        if tab_index == 0:
            tab_saf = self.ui.tabWidget_safety.currentIndex()
            self.load_tabwidget_safety(tab_saf)
        elif tab_index == 1:
            tab_sec = self.ui.tabWidget_security.currentIndex()
            self.load_tabwidget_security(tab_sec)
        elif tab_index == 2:
            self.load_controller_business()
        elif tab_index == 3:
            tab_pef = self.ui.tabWidget_performance.currentIndex()
            self.load_tabwidget_performance(tab_pef)

    def load_tabwidget_safety(self, tab_index):
        if tab_index == 0:
            self.load_goals()
            self.load_assumptions()
            self.load_losses()
            self.load_hazards()
            self.load_constraints()
        elif tab_index == 1:
            self.disable_controller_connections()
            self.disable_exts_connections()
            self.disable_actuator_connections()
            self.disable_sensor_connections()
            self.disable_controlled_process_connections()
            self.disable_controller_actions_variables()

            self.load_component_controller()
            self.load_component_exts()
            self.load_component_actuator()
            self.load_component_sensor()
            self.load_component_controlled_proccess()

            self.load_second_responsibility_ssc()

            self.check_control_structure()
        elif tab_index == 2:
            clear_var_step_three()
            self.load_combobox_third_controller()
            self.load_variables_dynamically()
            self.load_uca_third()
        elif tab_index == 3:
            clear_var_step_four()
            self.load_combobox_fourth_controller()
            self.load_fourth_loss_img()
        elif tab_index == 4:
            self.load_control_structure_image()
        elif tab_index == 5:
            self.load_stpa_report()

    def load_tabwidget_security(self, tab_index):
        if tab_index == 0:
            self.load_dfd_initialize()
            self.load_dfd_link_initialize()
            self.load_dfd_links()
        elif tab_index == 1:
            self.load_controller_stride()
        elif tab_index == 2:
            self.load_stride_report()

    def load_tabwidget_performance(self, tab_index):
        if tab_index == 0:
            self.load_controller_saf_pef_controller()
            self.load_controller_saf_pef_uca()
            self.load_saf_pef_requirements()
            self.load_saf_pef_resource()
        elif tab_index == 1:
            self.load_controller_sec_pef_controller()
            self.load_controller_sec_pef_priority()
            self.load_sec_pef_requirements()
            self.load_sec_pef_resource()
        elif tab_index == 2:
            self.load_controller_business_pef()
            self.load_bus_pef_resource()
        elif tab_index == 3:
            self.load_controller_conflict_pef()
            self.load_resource_conflict_pef()
            self.load_conflict_requirement()

    def onChange_main(self, i):  # changed!
        tab_index = i
        self.load_tabwidget_main(tab_index)

    def onChange_safety(self, i):  # changed!
        tab_index = i
        self.load_tabwidget_safety(tab_index)

    def onChange_security(self, i):  # changed!
        tab_index = i
        self.load_tabwidget_security(tab_index)

    def onChange_performance(self, i):  # changed!
        tab_index = i
        self.load_tabwidget_performance(tab_index)

    def load_projects(self):
        global list_projects, id_project

        list_projects = DB_Projects.select_all_projects()
        pos_selected = self.ui.combobox_projects.currentIndex()

        self.ui.combobox_projects.clear()

        if id_project < 0:
            is_first = True
        else:
            is_first = False

        for pos in range(len(list_projects)):
            self.ui.combobox_projects.addItem(list_projects[pos].name)
            if is_first:
                is_first = False
                id_project = list_projects[pos].id

        if len(list_projects) == 0:
            self.ui.tabWidget_main.setEnabled(False)
            return

        if self.ui.tabWidget_main.isEnabled() == False:
            self.ui.tabWidget_main.setEnabled(True)
            self.ui.tabWidget_safety.setEnabled(True)

        if pos_selected > 0 and pos_selected < len(list_projects):
            self.ui.combobox_projects.setCurrentIndex(pos_selected)
        else:
            self.ui.combobox_projects.setCurrentIndex(0)

    def selection_change_project(self):
        global id_project, list_projects

        pos = self.ui.combobox_projects.currentIndex()
        tab_index = self.ui.tabWidget_main.currentIndex()

        if len(list_projects) == 0:
            self.ui.tabWidget_main.setEnabled(False)
            return

        if pos >= len(list_projects):
            pos = 0

        id_project = list_projects[pos].id
        self.load_tabwidget_main(tab_index)

    def active_tab(self):
        self.ui.groupbox_project.setEnabled(True)
        self.ui.combobox_projects.setEnabled(True)
        self.ui.button_add_projects.setEnabled(True)
        self.ui.button_del_projects.setEnabled(True)
        # self.ui.tabWidget_main.setEnabled(True)

    def load_image(self):

        # img = Image.open(Constant.IMAGE_PATH)
        # img.show()
        try:
            os.startfile(Constant.IMAGE_STPA_FULL_PATH)
        except Exception as e:
            print(e)

    def load_image_step_one(self):
        try:
            os.startfile(Constant.IMAGE_STPA_ONE_PATH)
        except Exception as e:
            print(e)

    def load_image_step_two(self):
        try:
            os.startfile(Constant.IMAGE_STPA_TWO_PATH)
        except Exception as e:
            print(e)

    def load_image_step_three(self):
        try:
            os.startfile(Constant.IMAGE_STPA_THREE_PATH)
        except Exception as e:
            print(e)

    def load_image_step_four(self):
        try:
            os.startfile(Constant.IMAGE_STPA_FOUR_PATH)
        except Exception as e:
            print(e)

    def load_image_stride_dfd_map(self):
        try:
            os.startfile(Constant.IMAGE_STRIDE_DFD_MAP_PATH)
        except Exception as e:
            print(e)

    def load_image_stride_security(self):
        try:
            os.startfile(Constant.IMAGE_STRIDE_SECURITY_PATH)
        except Exception as e:
            print(e)

    def load_image_stride(self):
        try:
            os.startfile(Constant.IMAGE_STRIDE_FULL_PATH)
        except Exception as e:
            print(e)

    def load_start_advice(self):
        title = "Attention"

        msg = "This is a doctoral work by Andrei Carniel, under the supervision of Prof. Celso Hirata, at Instituto Tecnológico de Aeronáutica - ITA." \
              "\n\nYou are not authorized to share this software. After using the software, delete it." \
              "\n\nFor more information, please send an e-mail to andrei.carniel@ga.ita.br and hirata@ita.br." \
              "\n\n\nSoftware version " + Constant.VERSION

        showdialog(title, msg)

    def load_about(self):
        title = "Attention"

        msg = "This is a doctoral work by Andrei Carniel, under the supervision of Prof. Celso Hirata, at Instituto Tecnológico de Aeronáutica - ITA." \
              "\n\nYou are not authorized to share this software. After using the software, delete it." \
              "\n\nFor more information, please send an e-mail to andrei.carniel@ga.ita.br and hirata@ita.br." \
              "\n\nSupport material: STPA Handbook, by the authors: Nancy G. Leveson and John P. Thomas." \
              "\n\n\nSoftware version " + Constant.VERSION

        showdialog(title, msg)

    def on_button_add_project_clicked(self):
        pd = ProjectDialog()
        result = pd.exec_()

        if result == 1:
            name = pd.name.text()
            description = pd.description.text()

            if len(name) == 0 or len(description) == 0:
                showdialog("Error to create a new project", "You must fill all the fields to create a new project.")
                return

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            project = Project(0, name, description, current_date, "")
            id_proj = DB_Projects.insert_to_projects(project)

            if id_proj > 0:
                showdialog("Success", "New project created.")
                if self.ui.tabWidget_main.isEnabled() == False:
                    self.ui.tabWidget_main.setEnabled(True)
                    self.ui.tabWidget_safety.setEnabled(True)

                self.load_projects()
                return

            showdialog("Error", "It is not possible to create a new project at this time, please try again.")

    def on_button_del_project_clicked(self):
        global list_projects
        pos = self.ui.combobox_projects.currentIndex()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete the project " + list_projects[pos].name + "?\nThis operation cannot be undone")
        msgBox.setWindowTitle("Delete project?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Projects.delete(list_projects[pos].id)
            self.load_projects()

    # ----- Function Conflict Performance Analysis ----
    def load_controller_conflict_pef(self):
        global list_conflict_pef_controller, id_project

        self.ui.combobox_conflict_controller.clear()

        list_conflict_pef_controller = DB_Components.select_controller_not_external_not_human(id_project)
        for conn in list_conflict_pef_controller:
            self.ui.combobox_conflict_controller.addItem(conn.name)

    def load_resource_conflict_pef(self):
        global list_conflict_pef_resource

        self.ui.combobox_conflict_resource.clear()
        self.ui.combobox_conflict_resource_performance.clear()

        list_conflict_pef_resource = DB_Pef_Performance_Resource.select_all()
        for res in list_conflict_pef_resource:
            self.ui.combobox_conflict_resource.addItem(res.name)
            self.ui.combobox_conflict_resource_performance.addItem(res.name)

    def load_resource_pef_req(self):
        global list_conflict_pef_controller, list_conflict_pef_resource_requirement

        self.ui.listwidget_conflict_resource_requirement.clear()
        pos_c = self.ui.combobox_conflict_controller.currentIndex()

        if pos_c == -1:
            return

        list_conflict_pef_resource_requirement = DB_Pef_Res_Requirement.select_by_controller(list_conflict_pef_controller[pos_c].id)

        count = 1
        for req in list_conflict_pef_resource_requirement:
            self.ui.listwidget_conflict_resource_requirement.addItem("RQ-" + str(count) + ". " + req.res_name + " resource: " + req.requirement)
            count += 1

    def on_button_conflict_res_create(self):
        global list_conflict_pef_controller, list_conflict_pef_resource, id_project
        pos_c = self.ui.combobox_conflict_controller.currentIndex()
        pos_rs = self.ui.combobox_conflict_resource_performance.currentIndex()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return

        if pos_rs == -1:
            showdialog("No resource selected", "Select the resource")
            return

        # for aux in list_conflict_pef_resource_requirement:
        #     if list_conflict_pef_resource[pos_rs].id == aux.id_resource:
        #         showdialog("Existing requirement","There is a resource requirement for this resource. Please, edit it or choose another resource.")
        #         return

        req_dialog = Pef_Resource_Requiremnt("Creating a " + list_conflict_pef_resource[pos_rs].name + " requirement for " + list_conflict_pef_controller[pos_c].name, "")
        result = req_dialog.exec_()

        if result == 1:
            requirement = req_dialog.requirement.toPlainText()
            DB_Pef_Res_Requirement.insert_to_db(requirement, list_conflict_pef_resource[pos_rs].id, id_project, list_conflict_pef_controller[pos_c].id)
            self.load_resource_pef_req()

    def on_button_conflict_res_change(self):
        global list_conflict_pef_resource_requirement

        pos = self.ui.listwidget_conflict_resource_requirement.currentRow()

        if pos == -1:
            showdialog("No performance resource requirement selected", "Select the performance resource requirement")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this requirement?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_conflict_pef_resource_requirement[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Pef_Resource_Requiremnt(edt_req.comp_name, edt_req.requirement)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()

                DB_Pef_Res_Requirement.update(edt_req.id, requirement)
                self.load_resource_pef_req()
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the requirement RQ-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Pef_Res_Requirement.delete(edt_req.id)
                self.load_resource_pef_req()

    def on_button_conflict_res_print_report(self):
        global list_conflict_pef_controller
        try:
            result = Generate_PDF_Performance(id_project)
            if result == "Error":
                showdialog("Error to create PDF", "If the file is open, close and try again...")
            else:
                showdialog("New STRIDE Report", result)
        except Exception as e:
            showdialog("Error to create PDF", "If the file is open, close and try again...\n\n" + str(e))
            print(e)

    def load_conflict_requirement_controller(self):
        self.load_conflict_requirement()
        self.load_resource_pef_req()

    def load_conflict_requirement(self):
        global list_conflict_pef_controller, list_conflict_pef_resource, list_saf_conflict, list_sec_conflict, list_bus_conflict, id_project

        self.load_conflict_saf_requirement()
        self.load_conflict_sec_requirement()
        self.load_conflict_bus_requirement()

        self.ui.lbl_req_conflict.setText(str(len(list_saf_conflict)) + " saferty requirements x " + str(len(list_sec_conflict)) +
                                         " security requirements x " + str(len(list_bus_conflict)) + " business requirements")

    def checkbox_state_changed(self):
        self.load_conflict_saf_requirement()
        self.load_conflict_sec_requirement()
        self.load_conflict_bus_requirement()

    def load_conflict_saf_requirement(self):
        global list_conflict_pef_controller, list_conflict_pef_resource, list_saf_conflict, list_sec_conflict, list_bus_conflict, id_project

        pos_c = self.ui.combobox_conflict_controller.currentIndex()
        pos_rs = self.ui.combobox_conflict_resource.currentIndex()

        self.ui.listwidget_saf_conflict_requirement.clear()

        if pos_c == -1 or pos_rs == -1:
            return

        list_saf_conflict = DB_Loss_Scenario_Req.select_requirements_by_controller_resource(list_conflict_pef_controller[pos_c].id, list_conflict_pef_resource[pos_rs].id)

        self.ui.lbl_saf_conflict.setText("Number of requirements: " + str(len(list_saf_conflict)))
        count = 1
        for sf_rq in list_saf_conflict:
            text = "R_Saf - " + str(count) + ", causal factor originating element " + sf_rq.name_cause
            if self.ui.checkbox_conflict_requirement.isChecked():
                text += "\nCause: " + sf_rq.cause + "\nRequirement: " + sf_rq.requirement
            if self.ui.checkbox_conflict_mechanism.isChecked():
                text += "\nMechanism: " + sf_rq.mechanism
            if self.ui.checkbox_conflict_pef_requirement.isChecked():
                text += "\nPerformance Requirement: " + sf_rq.performance_req
            if self.ui.checkbox_conflict_resource.isChecked():
                for rq in sf_rq.list_res:
                    text += "\n" + rq.res_name + ": " + rq.requirement
            self.ui.listwidget_saf_conflict_requirement.addItem(text)
            count += 1

    def load_conflict_sec_requirement(self):
        global list_conflict_pef_controller, list_conflict_pef_resource, list_saf_conflict, list_sec_conflict, list_bus_conflict, id_project

        pos_c = self.ui.combobox_conflict_controller.currentIndex()
        pos_rs = self.ui.combobox_conflict_resource.currentIndex()

        self.ui.listwidget_sec_conflict_requirement.clear()

        if pos_c == -1 or pos_rs == -1:
            return

        list_sec_conflict = DB_Sec_Pef_Requirement.select_by_controller_resource(list_conflict_pef_controller[pos_c].id, list_conflict_pef_resource[pos_rs].id)
        self.ui.lbl_sec_conflict.setText("Number of requirements: " + str(len(list_sec_conflict)))
        count = 1
        for sc_rq in list_sec_conflict:
            text = "R_Sec - " + str(count) + ", threat class " + sc_rq.name_stride + " (Priority: " + sc_rq.name_priority + ")"

            if self.ui.checkbox_conflict_requirement.isChecked():
                text += "\nCause: " + sc_rq.description
                text += "\nRequirement: " + sc_rq.justification
            if self.ui.checkbox_conflict_mechanism.isChecked():
                text += "\nMechanism: " + sc_rq.mechanism
            if self.ui.checkbox_conflict_pef_requirement.isChecked():
                text += "\nPerformance Requirement: " + sc_rq.performance_req
            if self.ui.checkbox_conflict_resource.isChecked():
                for rq in sc_rq.list_res:
                    text += "\n" + rq.res_name + ": " + rq.requirement

            self.ui.listwidget_sec_conflict_requirement.addItem(text)
            count += 1

    def load_conflict_bus_requirement(self):
        global list_conflict_pef_controller, list_conflict_pef_resource, list_saf_conflict, list_sec_conflict, list_bus_conflict, id_project

        pos_c = self.ui.combobox_conflict_controller.currentIndex()
        pos_rs = self.ui.combobox_conflict_resource.currentIndex()

        self.ui.listwidget_bus_conflict_requirement.clear()

        if pos_c == -1 or pos_rs == -1:
            return

        list_bus_conflict = DB_Bus_Requirement.load_business_requirement_by_resource(list_conflict_pef_controller[pos_c].id, id_project, list_conflict_pef_resource[pos_rs].id)
        self.ui.lbl_bus_conflict.setText("Number of requirements: " + str(len(list_bus_conflict)))
        count = 1
        for bus_rq in list_bus_conflict:
            text = "R_Bus - " + str(count) + ", business element " + bus_rq.name_component

            if self.ui.checkbox_conflict_requirement.isChecked():
                text += "\nRequirement: " + bus_rq.requirement
            # if self.ui.checkbox_conflict_mechanism.isChecked():
            #     text += "\nMechanism: " + bus_rq.mechanism
            if self.ui.checkbox_conflict_pef_requirement.isChecked():
                text += "\nPerformance Requirement: " + bus_rq.performance_req
            if self.ui.checkbox_conflict_resource.isChecked():
                for bus in bus_rq.list_res:
                    text += "\n" + bus.res_name + ": " + bus.requirement

            self.ui.listwidget_bus_conflict_requirement.addItem(text)
            count += 1

    def on_button_change_saf_req(self):
        global list_saf_conflict

        pos = self.ui.listwidget_saf_conflict_requirement.currentRow()

        if pos == -1:
            showdialog("No requirement selected", "Select the requirement")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_saf_conflict[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            # priority = edt_req.id_priority - 1
            cf = CausalFactorDialog(edt_req.cause, edt_req.requirement, edt_req.mechanism, edt_req.name_src,
                                    edt_req.name_dst, edt_req.name_cause, True, edt_req.performance_req)
            result = cf.exec_()

            if result == 1:
                cause = cf.cause.toPlainText()
                recommendation = cf.requirement.toPlainText()
                mechanism = cf.mechanism.toPlainText()

                try:
                    pef_req = cf.pef_req.toPlainText()
                except Exception as e:
                    pef_req = edt_req.performance_req

                DB_Loss_Scenario_Req.update(edt_req.id, cause, recommendation, mechanism, pef_req)
                self.load_conflict_saf_requirement()
                return
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Loss_Scenario_Req.delete_by_id(edt_req.id)
                self.load_conflict_saf_requirement()

    def on_button_change_saf_res(self):
        global list_saf_conflict
        update = True

        pos = self.ui.listwidget_saf_conflict_requirement.currentRow()

        if pos == -1:
            showdialog("No requirement resource selected", "Select the requirement resource")
            return

        if len(list_saf_conflict[pos].list_res) == 0:
            showdialog("No requirement resource", "Create the resource before edit.")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_saf_conflict[pos].list_res[0]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Pef_Resource_Requiremnt(edt_req.comp_name, edt_req.requirement)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()

                DB_Saf_Pef_Requirement.update(edt_req.id, requirement)
                self.load_conflict_saf_requirement()
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Saf_Pef_Requirement.delete(edt_req.id)
                self.load_conflict_saf_requirement()

    def on_button_change_sec_req(self):
        global list_sec_conflict

        pos = self.ui.listwidget_sec_conflict_requirement.currentRow()

        if pos == -1:
            showdialog("No requirement selected", "Select the requirement")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_sec_conflict[pos]

        text = "Do you want to update or delete this  recommendation?"

        if edt_req.is_imported:
            text += "\n\nWARNING: you are updating an imported recommendation and this implies:" \
                    "\n- UPDATE will edit the original recommendation and the following links: "
            # text += "\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req_except(edt_req.id, list_stride_links[pos_link].id)
        else:
            text += "\n\nThis recommendation is used in the following links:\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req(
                edt_req.id)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Change  recommendation")
        msgBox.setText(text)

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            link = DB_Components_Links.get_by_id(edt_req.id_link)
            l_text = ""
            if link != None:
                l_text = link.name_src + " -> " + link.name_dst

            controls_text, controls_list = Security_tools_new.get_subclass_of_countermeasure_class(onto,
                                                                                                   edt_req.name_stride)
            for ctrl_req in edt_req.list_of_controls:
                is_in = False
                for ctrl in controls_list:
                    if ctrl.name == ctrl_req.name:
                        is_in = True
                        ctrl.selected = True

                if is_in == False:
                    controls_list.append(ctrl_req)

            priority = edt_req.id_priority - 1
            req = StrideDialog(edt_req.title, edt_req.name_stride, l_text, edt_req.description, edt_req.justification,
                               priority, edt_req.mechanism, controls_list, True, edt_req.performance_req)
            result = req.exec_()

            if result == 1:
                title = req.title.text()
                description = req.description.toPlainText()
                justification = req.justification.toPlainText()
                mechanism = req.mechanism.toPlainText()
                priority = req.comboBox.currentIndex() + 1

                try:
                    performance_req = req.pef_req.toPlainText()
                except Exception as e:
                    performance_req = edt_req.performance_req

                DB_Sec_Stride_Requirement.update(edt_req.id, title, description, justification, mechanism, priority, "", performance_req)
                self.load_conflict_sec_requirement()
                return
        elif returnValue == 1:
            text_delete = "You want to delete the recommendation: " + edt_req.title + "\n\nAre you sure?"

            if edt_req.is_imported:
                text_delete += "\n\nWARNING: This is a imported recommendation, and deleting here will NOT affects the original recommendation and other link analysis."
            else:
                text_delete += "\n\nWARNING. Deleting this recommendation will affect the following links:\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req(
                    edt_req.id)

            msgBoxDel = QMessageBox()
            msgBoxDel.setIcon(QMessageBox.Information)

            msgBoxDel.setWindowTitle("Delete recommendation")
            msgBoxDel.setText(text_delete)

            msgBoxDel.addButton(QPushButton("Delete"), QMessageBox.YesRole)
            msgBoxDel.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

            returnValue = msgBoxDel.exec()
            if returnValue == 0:
                if edt_req.is_imported:
                    pos_link = self.ui.combobox_stride_link.currentIndex()
                    if pos_link < 0:
                        return

                    DB_Sec_Stride_Requirement_Import.delete_link_req(list_stride_links[pos_link].id, edt_req.id)
                else:
                    DB_Sec_Stride_Requirement.delete(edt_req.id)

                self.load_conflict_sec_requirement()
                return

    def on_button_change_sec_res(self):
        global list_sec_conflict
        update = True

        pos = self.ui.listwidget_sec_conflict_requirement.currentRow()

        if pos == -1:
            showdialog("No requirement resource selected", "Select the requirement resource")
            return

        if len(list_sec_conflict[pos].list_res) == 0:
            showdialog("No requirement resource", "Create the resource before edit.")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_sec_conflict[pos].list_res[0]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Pef_Resource_Requiremnt(edt_req.comp_name, edt_req.requirement)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()

                DB_Sec_Pef_Requirement.update(edt_req.id, requirement)
                self.load_conflict_sec_requirement()
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Sec_Pef_Requirement.delete(edt_req.id)
                self.load_conflict_sec_requirement()

    def on_button_change_bus_req(self):
        global list_bus_conflict

        pos = self.ui.listwidget_bus_conflict_requirement.currentRow()

        if pos < 0:
            showdialog("Attention", "Before continue you must select a requirement.")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_bus_conflict[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Performance_Saf_Sec_Bus(edt_req.name_component, edt_req.requirement, edt_req.mechanism, True, edt_req.performance_req)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()
                mechanism = "" #req_dialog.mechanism.toPlainText()
                performance_req = req_dialog.pef_req.toPlainText()

                DB_Bus_Requirement.update(edt_req.id, requirement, mechanism, performance_req)
                self.load_conflict_bus_requirement()
        elif returnValue == 1:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Bus_Requirement.delete(edt_req.id)
                self.load_conflict_bus_requirement()

    def on_button_change_bus_res(self):
        global list_bus_conflict
        update = True

        pos = self.ui.listwidget_bus_conflict_requirement.currentRow()

        if pos == -1:
            showdialog("No requirement resource selected", "Select the requirement resource")
            return

        if len(list_bus_conflict[pos].list_res) == 0:
            showdialog("No requirement resource", "Create the resource before edit.")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_bus_conflict[pos].list_res[0]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Pef_Resource_Requiremnt(edt_req.comp_name, edt_req.requirement)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()

                DB_Bus_Pef_Requirement.update(edt_req.id, requirement)
                self.load_conflict_bus_requirement()
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Bus_Pef_Requirement.delete(edt_req.id)
                self.load_conflict_bus_requirement()
    # ----- Function Conflict Performance Analysis ----

    # ----- Function Business Performance Analysis ----
    def load_controller_business_pef(self):
        global list_bus_pef_controller, id_project

        self.ui.combobox_bus_pef_controller.clear()

        list_bus_pef_controller = DB_Components.select_controller_not_external_not_human(id_project)
        for conn in list_bus_pef_controller:
            self.ui.combobox_bus_pef_controller.addItem(conn.name)

        self.load_bus_pef_requirement()

    def load_bus_pef_requirement(self, selected_Position = -1):
        global list_bus_pef_controller, list_bus_pef_requirement, id_project

        pos_c = self.ui.combobox_bus_pef_controller.currentIndex()
        self.ui.listwidget_bus_pef_requirement.clear()
        self.ui.listwidget_bus_pef_res_requirement.clear()
        self.ui.lbl_bus_pef_res_requirement_count.setText("0")

        if pos_c == -1:
            # showdialog("No controller selected", "Select the controller")
            return

        req = list_bus_pef_controller[pos_c]
        list_bus_pef_requirement = DB_Bus_Requirement.load_business_requirement(req.id, id_project)

        self.ui.lbl_bus_pef_req.setText("2° Select the business requirement (total " + str(len(list_bus_pef_requirement)) + "):")
        count = 1
        for bus_rq in list_bus_pef_requirement:
            text = "R- " + str(count) + ". Requirement: " + bus_rq.requirement + "\nBusiness Performance Requirement: " + bus_rq.performance_req #"\nMechanism: " + bus_rq.mechanism +
            self.ui.listwidget_bus_pef_requirement.addItem(text)
            count += 1

        if selected_Position > -1:
            self.ui.listwidget_bus_pef_requirement.setCurrentRow(selected_Position)
        else:
            self.load_req_bus_pef()

    def load_req_bus_pef(self):
        global list_bus_pef_controller, list_bus_pef_requirement, list_bus_pef_resource, id_project

        pos_c = self.ui.combobox_bus_pef_controller.currentIndex()
        pos_rq = self.ui.listwidget_bus_pef_requirement.currentRow()
        pos_rs = self.ui.listwidget_bus_pef_resource.currentRow()

        text = ""

        if pos_c > -1:
            text += "Controller: " + list_bus_pef_controller[pos_c].name
        else:
            text += "Controller: -"

        if pos_rq > -1:
            text += "\nRequirement: " + list_bus_pef_requirement[pos_rq].requirement + \
                    "\nBusiness Performance Requirement: " + list_bus_pef_requirement[pos_rq].performance_req
        else:
            text += "\nRequirement: -"#\nMechanism: -"

        if pos_rs > -1:
            text += "\nResource: " + list_bus_pef_resource[pos_rs].name
        else:
            text += "\nResource: -"

        self.ui.lbl_bus_pef_res_req.setText(text)

    def load_bus_pef_resource(self):
        global list_bus_pef_resource

        self.ui.listwidget_bus_pef_resource.clear()

        list_bus_pef_resource = DB_Pef_Performance_Resource.select_all()
        for res in list_bus_pef_resource:
            self.ui.listwidget_bus_pef_resource.addItem(res.name)

    def load_bus_pef_res_requirement(self):
        global list_bus_pef_requirement, list_bus_pef_res_requirement

        pos_rq = self.ui.listwidget_bus_pef_requirement.currentRow()
        self.ui.listwidget_bus_pef_res_requirement.clear()
        self.ui.lbl_bus_pef_res_requirement_count.setText("0")

        if pos_rq == -1:
            return

        list_bus_pef_res_requirement = DB_Bus_Pef_Requirement.select_by_requirement(list_bus_pef_requirement[pos_rq].id)

        self.ui.lbl_bus_pef_res_requirement_count.setText(str(len(list_bus_pef_res_requirement)))
        count = 1
        for rq in list_bus_pef_res_requirement:
            self.ui.listwidget_bus_pef_res_requirement.addItem("R - " + str(count) + ", name: " + rq.res_name + "\nRequirement: " + rq.requirement)
            count += 1

        self.load_req_bus_pef()

    def add_bus_pef_res_requirement(self):
        global list_bus_pef_controller, list_bus_pef_requirement, list_bus_pef_resource, list_bus_pef_res_requirement
        pos_c = self.ui.combobox_bus_pef_controller.currentIndex()
        pos_rq = self.ui.listwidget_bus_pef_requirement.currentRow()
        pos_rs = self.ui.listwidget_bus_pef_resource.currentRow()

        text = ""

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        else:
            text += "Controller: " + list_bus_pef_controller[pos_c].name

        if pos_rq == -1:
            showdialog("No requirement selected", "Select the requirement")
            return
        else:
            text += "\nRequirement: " + list_bus_pef_requirement[pos_rq].requirement #+"\nMechanism: " + list_bus_pef_requirement[pos_rq].mechanism

        if pos_rs == -1:
            showdialog("No resource selected", "Select the resource")
            return
        else:
            text += "\nResource: " + list_bus_pef_resource[pos_rs].name

        # for aux in list_bus_pef_res_requirement:
        #     if list_bus_pef_resource[pos_rs].id == aux.id_resource:
        #         showdialog("Existing requirement",
        #                    "There is a resource requirement for this resource. Please, edit it or choose another resource.")
        #         return

        req_dialog = Pef_Resource_Requiremnt(text, "")
        result = req_dialog.exec_()

        if result == 1:
            requirement = req_dialog.requirement.toPlainText()

            DB_Bus_Pef_Requirement.insert_to_db(requirement, list_bus_pef_requirement[pos_rq].id, list_bus_pef_resource[pos_rs].id, id_project, list_bus_pef_controller[pos_c].id)
            self.load_bus_pef_res_requirement()

    def change_bus_pef_requirement(self):
        global list_bus_pef_requirement, id_project

        pos = self.ui.listwidget_bus_pef_requirement.currentRow()

        if pos < 0:
            showdialog("Attention", "Before continue you must select a requirement.")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_bus_pef_requirement[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Performance_Saf_Sec_Bus(edt_req.name_component, edt_req.requirement, edt_req.mechanism, True, edt_req.performance_req)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()
                mechanism = "" #req_dialog.mechanism.toPlainText()
                performance_req = req_dialog.pef_req.toPlainText()

                DB_Bus_Requirement.update(edt_req.id, requirement, mechanism, performance_req)
                self.load_bus_pef_requirement(pos)
        elif returnValue == 1:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Bus_Requirement.delete(edt_req.id)
                self.load_bus_pef_requirement()

    def load_req_bus_pef_resource(self):
        global list_bus_pef_res_requirement

        pos = self.ui.listwidget_bus_pef_res_requirement.currentRow()

        if pos == -1:
            # showdialog("No requirement resource selected", "Select the requirement resource")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_bus_pef_res_requirement[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Pef_Resource_Requiremnt(edt_req.comp_name, edt_req.requirement)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()

                DB_Bus_Pef_Requirement.update(edt_req.id, requirement)
                self.load_bus_pef_res_requirement()
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Bus_Pef_Requirement.delete(edt_req.id)
                self.load_bus_pef_res_requirement()
    # ----- Function Business Performance Analysis ----

    # ----- Function Security Performance Analysis ----
    def load_controller_sec_pef_controller(self):
        global list_sec_pef_controller, id_project

        self.ui.combobox_sec_pef_controller.clear()

        list_sec_pef_controller = DB_Components.select_controller_not_external_not_human(id_project)
        for conn in list_sec_pef_controller:
            self.ui.combobox_sec_pef_controller.addItem(conn.name)

        self.load_req_sec_pef()
        self.load_controller_sec_pef_priority()

    def load_controller_sec_pef_priority(self):
        global list_sec_pef_priority, id_project

        self.ui.combobox_sec_pef_priority.clear()

        list_sec_pef_priority = DB_Sec_Pef_Requirement.load_sec_pef_priority()
        for conn in list_sec_pef_priority:
            self.ui.combobox_sec_pef_priority.addItem(conn.name)

        self.load_req_sec_pef()
        self.load_sec_pef_requirements()

    def load_sec_pef_requirements(self, selected_Position = -1):
        global list_sec_pef_controller, list_sec_pef_priority, list_sec_pef_requirement, id_project

        pos_c = self.ui.combobox_sec_pef_controller.currentIndex()
        pos_p = self.ui.combobox_sec_pef_priority.currentIndex()
        self.ui.listwidget_sec_pef_requirement.clear()
        self.ui.listwidget_sec_pef_res_requirement.clear()
        self.ui.lbl_sec_pef_res_requirement_count.setText("0")

        if pos_c == -1 or pos_p == -1:
            # showdialog("No controller selected", "Select the controller")
            return

        list_sec_pef_requirement = DB_Sec_Pef_Requirement.select_by_controller(list_sec_pef_controller[pos_c].id, list_sec_pef_priority[pos_p].id)


        self.ui.lbl_sec_pef_req.setText("3° Select the security requirement (total " + str(len(list_sec_pef_requirement)) + "):")
        count = 1
        for req in list_sec_pef_requirement:
            text = "R - " + str(count) + ". Requirement: " + req.justification + "\nMechanism: " + req.mechanism + "\nSecurity Performance Requirement: " + req.performance_req
            count += 1
            self.ui.listwidget_sec_pef_requirement.addItem(text)

        if selected_Position > -1:
            self.ui.listwidget_sec_pef_requirement.setCurrentRow(selected_Position)
        else:
            self.load_req_sec_pef()

    def load_sec_pef_resource(self):
        global list_sec_pef_resource

        self.ui.listwidget_sec_pef_resource.clear()

        list_sec_pef_resource = DB_Pef_Performance_Resource.select_all()
        for res in list_sec_pef_resource:
            self.ui.listwidget_sec_pef_resource.addItem(res.name)

    def load_req_sec_pef(self):
        global list_sec_pef_controller, list_sec_pef_requirement, list_sec_pef_resource, id_project

        pos_c = self.ui.combobox_sec_pef_controller.currentIndex()
        pos_rq = self.ui.listwidget_sec_pef_requirement.currentRow()
        pos_rs = self.ui.listwidget_sec_pef_resource.currentRow()

        text = ""

        if pos_c > -1:
            text += "Controller: " + list_sec_pef_controller[pos_c].name
        else:
            text += "Controller: -"

        if pos_rq > -1:
            text += "\nRequirement: " + list_sec_pef_requirement[pos_rq].justification + \
                    "\nMechanism: " + list_sec_pef_requirement[pos_rq].mechanism +\
                    "\nSecurity Performance Requirement: " + list_sec_pef_requirement[pos_rq].performance_req
        else:
            text += "\nRequirement: -\nMechanism: -\nSecurity Performance Requirement: -"

        if pos_rs > -1:
            text += "\nResource: " + list_sec_pef_resource[pos_rs].name
        else:
            text += "\nResource: -"

        self.ui.lbl_sec_pef_res_req.setText(text)

    def load_sec_pef_res_requirement(self):
        global list_sec_pef_requirement, list_sec_pef_res_requirement

        pos_rq = self.ui.listwidget_sec_pef_requirement.currentRow()
        self.ui.listwidget_sec_pef_res_requirement.clear()

        if pos_rq == -1:
            return

        list_sec_pef_res_requirement = DB_Sec_Pef_Requirement.select_by_requirement(list_sec_pef_requirement[pos_rq].id)

        self.ui.lbl_sec_pef_res_requirement_count.setText(str(len(list_sec_pef_res_requirement)))
        count = 1
        for rq in list_sec_pef_res_requirement:
            self.ui.listwidget_sec_pef_res_requirement.addItem("R - " + str(count) + ", " + rq.res_name + "\nRequirement: " + rq.requirement)
            count += 1
        self.load_req_sec_pef()

    def add_sec_pef_res_requirement(self):
        global list_sec_pef_controller, list_sec_pef_requirement, list_sec_pef_resource, list_sec_pef_res_requirement
        pos_c = self.ui.combobox_sec_pef_controller.currentIndex()
        pos_rq = self.ui.listwidget_sec_pef_requirement.currentRow()
        pos_rs = self.ui.listwidget_sec_pef_resource.currentRow()

        text = ""

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        else:
            text += "Controller: " + list_sec_pef_controller[pos_c].name

        if pos_rq == -1:
            showdialog("No requirement selected", "Select the requirement")
            return
        else:
            text += "\nRequirement: " + list_sec_pef_requirement[pos_rq].justification + \
                    "\nMechanism: " + list_sec_pef_requirement[pos_rq].mechanism

        if pos_rs == -1:
            showdialog("No resource selected", "Select the resource")
            return
        else:
            text += "\nResource: " + list_sec_pef_resource[pos_rs].name

        # for aux in list_sec_pef_res_requirement:
        #     if list_sec_pef_resource[pos_rs].id == aux.id_resource:
        #         showdialog("Existing requirement", "There is a resource requirement for this resource. Please, edit it or choose another resource.")
        #         return

        req_dialog = Pef_Resource_Requiremnt(text, "")
        result = req_dialog.exec_()

        if result == 1:
            requirement = req_dialog.requirement.toPlainText()

            DB_Sec_Pef_Requirement.insert_to_db(requirement, list_sec_pef_requirement[pos_rq].id, list_sec_pef_resource[pos_rs].id, id_project, list_sec_pef_controller[pos_c].id)
            self.load_sec_pef_res_requirement()

    def change_sec_pef_res_requirement(self):
        global list_sec_pef_requirement
        pos_rq = self.ui.listwidget_sec_pef_requirement.currentRow()

        if pos_rq == -1:
            showdialog("No requirement selected", "Select the requirement")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_sec_pef_requirement[pos_rq]


        text = "Do you want to update or delete this  recommendation?"

        if edt_req.is_imported:
            text += "\n\nWARNING: you are updating an imported recommendation and this implies:" \
                    "\n- UPDATE will edit the original recommendation and the following links: "
            # text += "\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req_except(edt_req.id, list_stride_links[pos_link].id)
        else:
            text += "\n\nThis recommendation is used in the following links:\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req(edt_req.id)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Change  recommendation")
        msgBox.setText(text)

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            link = DB_Components_Links.get_by_id(edt_req.id_link)
            l_text = ""
            if link != None:
                l_text = link.name_src + " -> " + link.name_dst

            controls_text, controls_list = Security_tools_new.get_subclass_of_countermeasure_class(onto,
                                                                                                   edt_req.name_stride)
            for ctrl_req in edt_req.list_of_controls:
                is_in = False
                for ctrl in controls_list:
                    if ctrl.name == ctrl_req.name:
                        is_in = True
                        ctrl.selected = True

                if is_in == False:
                    controls_list.append(ctrl_req)

            priority = edt_req.id_priority - 1
            req = StrideDialog(edt_req.title, edt_req.name_stride, l_text, edt_req.description, edt_req.justification,
                               priority, edt_req.mechanism, controls_list, True, edt_req.performance_req)
            result = req.exec_()

            if result == 1:
                title = req.title.text()
                description = req.description.toPlainText()
                justification = req.justification.toPlainText()
                mechanism = req.mechanism.toPlainText()
                priority = req.comboBox.currentIndex() + 1

                try:
                    performance_req = req.pef_req.toPlainText()
                except Exception as e:
                    performance_req = edt_req.performance_req

                DB_Sec_Stride_Requirement.update(edt_req.id, title, description, justification, mechanism, priority, "", performance_req)
                self.load_sec_pef_requirements(pos_rq)
                return
        elif returnValue == 1:
            text_delete = "You want to delete the recommendation: " + edt_req.title + "\n\nAre you sure?"

            if edt_req.is_imported:
                text_delete += "\n\nWARNING: This is a imported recommendation, and deleting here will NOT affects the original recommendation and other link analysis."
            else:
                text_delete += "\n\nWARNING. Deleting this recommendation will affect the following links:\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req(edt_req.id)

            msgBoxDel = QMessageBox()
            msgBoxDel.setIcon(QMessageBox.Information)

            msgBoxDel.setWindowTitle("Delete recommendation")
            msgBoxDel.setText(text_delete)

            msgBoxDel.addButton(QPushButton("Delete"), QMessageBox.YesRole)
            msgBoxDel.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

            returnValue = msgBoxDel.exec()
            if returnValue == 0:
                if edt_req.is_imported:
                    pos_link = self.ui.combobox_stride_link.currentIndex()
                    if pos_link < 0:
                        return

                    DB_Sec_Stride_Requirement_Import.delete_link_req(list_stride_links[pos_link].id, edt_req.id)
                else:
                    DB_Sec_Stride_Requirement.delete(edt_req.id)

                self.load_sec_pef_requirements()
                return

    def load_req_sec_pef_resource(self):
        global list_sec_pef_res_requirement

        pos = self.ui.listwidget_sec_pef_res_requirement.currentRow()

        if pos == -1:
            showdialog("No requirement resource selected", "Select the requirement resource")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_sec_pef_res_requirement[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Pef_Resource_Requiremnt(edt_req.comp_name, edt_req.requirement)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()

                DB_Sec_Pef_Requirement.update(edt_req.id, requirement)
                self.load_sec_pef_res_requirement()
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Sec_Pef_Requirement.delete(edt_req.id)
                self.load_sec_pef_res_requirement()
    # ----- Function Security Performance Analysis ----

    # ----- Function Safety Performance Analysis ----
    def load_controller_saf_pef_controller(self):
        global list_saf_pef_controller, id_project

        self.ui.combobox_saf_pef_controller.clear()

        list_saf_pef_controller = DB_Components.select_controller_not_external_not_human(id_project)
        for conn in list_saf_pef_controller:
            self.ui.combobox_saf_pef_controller.addItem(conn.name)

        self.load_req_saf_pef()
        self.load_controller_saf_pef_uca()

    def load_controller_saf_pef_uca(self):
        global list_saf_pef_uca, id_project

        self.ui.combobox_saf_pef_uca_type.clear()

        list_saf_pef_uca = DB_Saf_Pef_Requirement.load_saf_pef_uca_type()
        for conn in list_saf_pef_uca:
            self.ui.combobox_saf_pef_uca_type.addItem(conn.description)

        self.load_req_saf_pef()
        self.load_saf_pef_requirements()

    def load_saf_pef_requirements(self, selected_Position = -1):
        global list_saf_pef_controller, list_saf_pef_uca,  list_saf_pef_requirement, id_project

        pos_c = self.ui.combobox_saf_pef_controller.currentIndex()
        pos_u = self.ui.combobox_saf_pef_uca_type.currentIndex()
        self.ui.listwidget_saf_pef_requirement.clear()
        self.ui.listwidget_saf_pef_res_requirement.clear()
        self.ui.lbl_saf_pef_res_requirement_count.setText("0")

        if pos_c == -1 or pos_u == -1:
            # showdialog("No controller selected", "Select the controller")
            return

        list_saf_pef_requirement = DB_Loss_Scenario_Req.select_requirements_by_controller_uca(list_saf_pef_controller[pos_c].id, list_saf_pef_uca[pos_u].id)
        self.ui.lbl_saf_pef_req.setText("3° Select the safety requirement (total " + str(len(list_saf_pef_requirement)) + "):")
        count = 1
        for req in list_saf_pef_requirement:
            text = "R - " + str(count) + ", " + req.name_cause + \
                   "\nCause: " + req.cause + \
                   "\nRequirement: " + req.requirement + \
                   "\nMechanism: " + req.mechanism + \
                   "\nSafety Performance Requirement: " + req.performance_req

            count += 1
            self.ui.listwidget_saf_pef_requirement.addItem(text)

        if selected_Position > -1:
            self.ui.listwidget_saf_pef_requirement.setCurrentRow(selected_Position)
        else:
            self.load_req_saf_pef()

    def load_saf_pef_resource(self):
        global list_saf_pef_resource

        self.ui.listwidget_saf_pef_resource.clear()

        list_saf_pef_resource = DB_Pef_Performance_Resource.select_all()
        for res in list_saf_pef_resource:
            self.ui.listwidget_saf_pef_resource.addItem(res.name)

    def load_req_saf_pef(self):
        global list_saf_pef_controller, list_saf_pef_requirement, list_saf_pef_resource, id_project

        pos_c = self.ui.combobox_saf_pef_controller.currentIndex()
        pos_rq = self.ui.listwidget_saf_pef_requirement.currentRow()
        pos_rs = self.ui.listwidget_saf_pef_resource.currentRow()

        text = ""

        if pos_c > -1:
            text += "Controller: " + list_saf_pef_controller[pos_c].name
        else:
            text += "Controller: -"

        if pos_rq > -1:
            uca_text = DB_UCA.select_string_uca_by_id(list_saf_pef_requirement[pos_rq].id_uca)
            text += "\nUCA: " + uca_text + \
                    "\nCause: " + list_saf_pef_requirement[pos_rq].cause +\
                    "\nRequirement: " + list_saf_pef_requirement[pos_rq].requirement +\
                    "\nMechanism: " + list_saf_pef_requirement[pos_rq].mechanism +\
                    "\nSafety Performance Requirement: " + list_saf_pef_requirement[pos_rq].performance_req
        else:
            text += "\nRequirement: -\nMechanism: -\nSafety Performance Requirement: -"

        if pos_rs > -1:
            text += "\nResource: " + list_saf_pef_resource[pos_rs].name
        else:
            text += "\nResource: -"

        self.ui.lbl_saf_pef_res_req.setText(text)

    def load_saf_pef_res_requirement(self):
        global list_saf_pef_requirement, list_saf_pef_res_requirement

        pos_rq = self.ui.listwidget_saf_pef_requirement.currentRow()
        self.ui.listwidget_saf_pef_res_requirement.clear()

        if pos_rq == -1:
            return

        list_saf_pef_res_requirement = DB_Saf_Pef_Requirement.select_by_requirement(list_saf_pef_requirement[pos_rq].id)

        self.ui.lbl_saf_pef_res_requirement_count.setText(str(len(list_saf_pef_res_requirement)))
        count = 1
        for rq in list_saf_pef_res_requirement:
            self.ui.listwidget_saf_pef_res_requirement.addItem("R - " + str(count) + ", name: " + rq.res_name + "\nRequirement: " + rq.requirement)
            count += 1
        self.load_req_saf_pef()

    def add_saf_pef_res_requirement(self):
        global list_saf_pef_controller, list_saf_pef_requirement, list_saf_pef_resource, list_saf_pef_res_requirement
        pos_c = self.ui.combobox_saf_pef_controller.currentIndex()
        pos_rq = self.ui.listwidget_saf_pef_requirement.currentRow()
        pos_rs = self.ui.listwidget_saf_pef_resource.currentRow()

        text = ""

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        else:
            text += "Controller: " + list_saf_pef_controller[pos_c].name

        if pos_rq == -1:
            showdialog("No requirement selected", "Select the requirement")
            return
        else:
            text += "\nRequirement: " + list_saf_pef_requirement[pos_rq].requirement + \
                    "\nMechanism: " + list_saf_pef_requirement[pos_rq].mechanism

        if pos_rs == -1:
            showdialog("No resource selected", "Select the resource")
            return
        else:
            text += "\nResource: " + list_saf_pef_resource[pos_rs].name

        # for aux in list_saf_pef_res_requirement:
        #     if list_saf_pef_resource[pos_rs].id == aux.id_resource:
        #         showdialog("Existing requirement", "There is a resource requirement for this resource. Please, edit it or choose another resource.")
        #         return

        req_dialog = Pef_Resource_Requiremnt(text, "")
        result = req_dialog.exec_()

        if result == 1:
            requirement = req_dialog.requirement.toPlainText()

            DB_Saf_Pef_Requirement.insert_to_db(requirement, list_saf_pef_requirement[pos_rq].id, list_saf_pef_resource[pos_rs].id, id_project, list_saf_pef_controller[pos_c].id)
            self.load_saf_pef_res_requirement()

    def change_saf_pef_res_requirement(self):
        global list_saf_pef_requirement
        pos_rq = self.ui.listwidget_saf_pef_requirement.currentRow()

        if pos_rq == -1:
            showdialog("No requirement selected", "Select the requirement")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_saf_pef_requirement[pos_rq]

        returnValue = msgBox.exec()
        if returnValue == 0:
            # priority = edt_req.id_priority - 1
            cf = CausalFactorDialog(edt_req.cause, edt_req.requirement, edt_req.mechanism, edt_req.name_src,
                                    edt_req.name_dst, edt_req.name_cause, True, edt_req.performance_req)
            result = cf.exec_()

            if result == 1:
                cause = cf.cause.toPlainText()
                recommendation = cf.requirement.toPlainText()
                mechanism = cf.mechanism.toPlainText()

                try:
                    performance_req = cf.pef_req.toPlainText()
                except Exception as e:
                    performance_req = ""

                DB_Loss_Scenario_Req.update(edt_req.id, cause, recommendation, mechanism, performance_req)
                self.load_saf_pef_requirements(pos_rq)
                return
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos_rq + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Loss_Scenario_Req.delete_by_id(edt_req.id)
                self.load_saf_pef_requirements()

    def load_req_saf_pef_resource(self):
        global list_saf_pef_res_requirement

        pos = self.ui.listwidget_saf_pef_res_requirement.currentRow()

        if pos == -1:
            showdialog("No requirement resource selected", "Select the requirement resource")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_saf_pef_res_requirement[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Pef_Resource_Requiremnt(edt_req.comp_name, edt_req.requirement)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()

                DB_Saf_Pef_Requirement.update(edt_req.id, requirement)
                self.load_saf_pef_res_requirement()
        elif returnValue == 1:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Saf_Pef_Requirement.delete(edt_req.id)
                self.load_saf_pef_res_requirement()
    # ----- Function Safety Performance Analysis ----

    # ----- Function Business Analysis ----
    def load_controller_business(self):
        global list_business_controller, id_project

        self.ui.combobox_bus_controller.clear()

        list_business_controller = DB_Components.select_controller_not_external_not_human(id_project)
        for conn in list_business_controller:
            self.ui.combobox_bus_controller.addItem(conn.name)

        self.load_business_requirements()

    def load_business_requirements(self):
        global list_business_controller, list_business_requirement, id_project

        pos_c = self.ui.combobox_bus_controller.currentIndex()
        self.ui.listwidget_bus_requirements.clear()

        if pos_c == -1:
            # showdialog("No controller selected", "Select the controller")
            return

        req = list_business_controller[pos_c]
        list_business_requirement = DB_Bus_Requirement.load_business_requirement(req.id, id_project)

        self.ui.lbl_pef_recommendation_count.setText(str(len(list_business_requirement)))
        count = 1
        for bus_rq in list_business_requirement:
            text = "R - " + str(count) + "\nRequirement: " + bus_rq.requirement + "\nBusiness Performance Requirement: " + bus_rq.performance_req # "\nMechanism: " + bus_rq.mechanism +
            self.ui.listwidget_bus_requirements.addItem(text)
            count += 1

    def on_button_bus_add_clicked(self):
        global list_business_controller, id_project

        pos_c = self.ui.combobox_bus_controller.currentIndex()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return

        req = list_business_controller[pos_c]
        req_dialog = Performance_Saf_Sec_Bus(req.name, "", "", True, "")
        result = req_dialog.exec_()

        if result == 1:
            requirement = req_dialog.requirement.toPlainText()
            mechanism = "" #req_dialog.mechanism.toPlainText()
            performance_req = req_dialog.pef_req.toPlainText()

            DB_Bus_Requirement.insert_to_db(requirement, mechanism, req.id, id_project, performance_req)
            self.load_business_requirements()

    def on_listwidget_bus_requirements_clicked(self):
        global list_business_requirement, id_project

        pos = self.ui.listwidget_bus_requirements.currentRow()

        if pos < 0:
            showdialog("Attention", "Before continue you must select a requirement.")
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)
        edt_req = list_business_requirement[pos]

        returnValue = msgBox.exec()
        if returnValue == 0:
            req_dialog = Performance_Saf_Sec_Bus(edt_req.name_component, edt_req.requirement, edt_req.mechanism, True, edt_req.performance_req)
            result = req_dialog.exec_()

            if result == 1:
                requirement = req_dialog.requirement.toPlainText()
                mechanism = "" #req_dialog.mechanism.toPlainText()
                performance_req = req_dialog.pef_req.toPlainText()

                DB_Bus_Requirement.update(edt_req.id, requirement, mechanism, performance_req)
                self.load_business_requirements()
        elif returnValue == 1:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Bus_Requirement.delete(edt_req.id)
                self.load_business_requirements()
    # ----- Function Business Analysis ----

    # ----- Functions STRIDE report Step -----
    def load_stride_report(self):
        global id_project

        list_controllers = DB_Components.select_controller_not_external_not_human(id_project)
        list_omitted_links = DB_Components_Links.select_omitted_links(id_project)

        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout()
        group_box = QtWidgets.QGroupBox()
        group_box.setTitle("")
        group_box.setFont(QFont('Arial', 11))
        layout = QtWidgets.QVBoxLayout(group_box)

        project = DB_Projects.select_project_by_id(id_project)
        layout.addWidget(self.get_label_14_title("STRIDE analysis of " + project.name))
        layout.addWidget(self.get_label_12_text(project.description))
        layout.addWidget(self.get_label_12_text("Begin date: " + project.begin_date))

        # Show omitted links
        layout.addWidget(self.get_label_12_bold_subtitle("\nPhysical and empty links: "))
        text_omt = ""
        for omt in list_omitted_links:
            if text_omt != "":
                text_omt += "\n"
            text_omt += "\t" + omt
        layout.addWidget(self.get_label_11_text(text_omt))

        # Show recomendations by controller and link
        for conn in list_controllers:
            layout.addWidget(self.get_label_12_bold_subtitle("\n" + conn.name))

            list_stride_links = DB_Components_Links.select_links_stride(conn.id)

            for link in list_stride_links:
                text = ""

                if link.is_hlc and len(link.list_var) > 0:
                    text = " - from Controller"
                elif link.is_hlc and len(link.list_act) > 0:
                    text = " - to Controller"

                if len(link.list_act) > 0 and link.is_ext == True:
                    layout.addWidget(self.get_label_12_text("(External Communication) " + link.name_src + " -> " + link.name_dst))

                if len(link.list_act) > 0 and link.is_ext == False:
                    layout.addWidget(self.get_label_12_text("(Control Action" + text + ") " + link.name_src + " -> " + link.name_dst))

                if len(link.list_var) > 0 and link.is_ext == True:
                    layout.addWidget(self.get_label_12_text("(External Communication) " + link.name_src + " -> " + link.name_dst))

                if len(link.list_var) > 0 and link.is_ext == False:
                    layout.addWidget(self.get_label_12_text("(Feedback" + text + ") " + link.name_src + " -> " + link.name_dst))


                if link.is_bound_trust == 1:
                    layout.addWidget(self.get_label_12_text("Is in a boundary trust: YES"))
                else:
                    layout.addWidget(self.get_label_12_text("Is in a boundary trust: NO"))

                list_stride_requirements = DB.DB_Sec_Stride_Requirement.select_by_id_link(link.id)
                count = 1
                layout.addWidget(self.get_label_11_text("\tNumber of recommendations: " + str(len(list_stride_requirements)) + "\n"))
                for req in list_stride_requirements:
                    text = "\t"
                    if req.is_imported == True:
                        text += "(IMPORTED) "
                    text += "Rec " + str(count) + ": Priority " + req.name_priority + "\n"
                    text += "\tComponent/Link: " + req.name_comp_link + "\n"
                    text += "\tSTRIDE Element: " + req.name_stride + "\n"
                    text += "\tAnalysed as DFD Element: " + req.name_dfd + "\n"
                    text += "\tTitle: " + req.title + "\n"
                    text += "\tDescription: " + req.description + "\n"
                    text += "\tRecommendation: " + req.justification + "\n"
                    text += "\tMechanism: " + req.mechanism + "\n"

                    #controls = ""
                    #for ctrl in req.list_of_controls:
                    #    if controls != "":
                    #        controls += "; "
                    #    controls += ctrl.name
                    #text += "\tSelected controls: " + controls + "\n"

                    count += 1
                    layout.addWidget(self.get_label_11_text(text))

        top_layout.addWidget(group_box)
        top_widget.setLayout(top_layout)
        self.ui.scrollArea_stride_report.setWidget(top_widget)

    def on_button_stride_report_clicked(self):
        try:
            result = Generate_PDF_STRIDE(id_project)
            if result == "Error":
                showdialog("Error to create PDF", "If the file is open, close and try again...")
            else:
                showdialog("New STRIDE Report", result)
        except Exception as e:
            showdialog("Error to create PDF", "If the file is open, close and try again...\n\n" + str(e))
            print(e)
    # ----- Functions STRIDE report Step -----

    # ----- Functions STRIDE analysis -----
    def load_controller_stride(self):
        global list_stride_controller, id_project, need_update_stride_link

        need_update_stride_link = False
        self.ui.combobox_stride_controller.clear()

        list_stride_controller = DB_Components.select_controller_not_external_not_human(id_project)
        for conn in list_stride_controller:
            self.ui.combobox_stride_controller.addItem(conn.name)

        need_update_stride_link = True

    def selection_change_controller_stride(self):
        global list_stride_controller

        self.ui.listwidget_stride_act.clear()
        self.ui.listwidget_stride_var.clear()
        self.ui.listwidget_stride_uca.clear()
        self.ui.lbl_stride_act.setText("Controller control actions (total = 0):")
        self.ui.lbl_stride_var.setText("Controller feedback (total = 0):")
        self.ui.lbl_stride_uca.setText("Unsafe Control Actions for controller (total = 0):")

        pos = self.ui.combobox_stride_controller.currentIndex()
        if pos < 0:
            return

        act_list = DB_Actions_Components.select_name_actions_by_controller(list_stride_controller[pos].id)
        for act in act_list:
            self.ui.listwidget_stride_act.addItem(act)
        self.ui.lbl_stride_act.setText("Controller control actions (total = " + str(len(act_list)) + "):")

        var_list = DB_Variables.select_name_variables_by_controller(list_stride_controller[pos].id)
        for var in var_list:
            self.ui.listwidget_stride_var.addItem(var)
        self.ui.lbl_stride_var.setText("Controller feedback (total = " + str(len(var_list)) + "):")

        self.load_stride_uca(list_stride_controller[pos].id)
        self.load_stride_links()

    def load_stride_uca(self, id_controller):
        list_stride_uca = DB_UCA.select_all_saf_uca_by_controller_filtering(id_controller, Constant.UCA_RULE, True)
        list_stride_uca.extend(
            DB_UCA.select_all_saf_uca_by_controller_filtering(id_controller, Constant.UCA_CELL, True))

        self.ui.lbl_stride_uca.setText(
            "Unsafe Control Actions for controller (total = " + str(len(list_stride_uca)) + "):")

        count_r = 0
        count_c = 0
        for uca in list_stride_uca:
            text = "UCA"
            if uca.uca_origin == Constant.UCA_RULE:
                count_r += 1
                text += "_R-" + str(count_r)
            else:
                count_c += 1
                text += "_C-" + str(count_c)

            text += " " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action

            text_context = ""
            for context in uca.context_list:
                if text_context != "":
                    text_context += ", "
                text_context += context.variable_name + " is " + context.variable_value

            if text_context == "":
                text += " in any context. "
            else:
                text += " when " + text_context + ". "

            # text += text_context + ". "
            for haz in uca.hazard_list:
                text += "[H-" + str(haz.hazard_order) + "]"

            self.ui.listwidget_stride_uca.addItem(text)

    def load_stride_links(self):
        global list_stride_links, list_stride_controller, id_project

        self.ui.combobox_stride_link.clear()

        pos = self.ui.combobox_stride_controller.currentIndex()
        if pos < 0:
            return

        self.ui.radiobutton_stride_src.setEnabled(True)
        self.ui.radiobutton_stride_link.setEnabled(True)
        self.ui.radiobutton_stride_dst.setEnabled(True)

        list_stride_links = DB_Components_Links.select_links_stride(list_stride_controller[pos].id)

        for link in list_stride_links:
            text = ""

            if link.is_hlc and len(link.list_var) > 0:
                text = " - from Controller"
            elif link.is_hlc and len(link.list_act) > 0:
                text = " - to Controller"

            if len(link.list_act) > 0 and link.is_ext == False:
                self.ui.combobox_stride_link.addItem(
                    "(Control Action" + text + ") " + link.name_src + " -> " + link.name_dst)

            if len(link.list_var) > 0 and link.is_ext == False:
                self.ui.combobox_stride_link.addItem(
                    "(Feedback" + text + ") " + link.name_src + " -> " + link.name_dst)

            if len(link.list_act) > 0 and link.is_ext == True:
                self.ui.combobox_stride_link.addItem(
                    "(External Communication) " + link.name_src + " -> " + link.name_dst)

            if len(link.list_var) > 0 and link.is_ext == True:
                self.ui.combobox_stride_link.addItem(
                    "(External Communication) " + link.name_src + " -> " + link.name_dst)

    def selection_change_link_stride_board(self):
        global list_stride_links

        self.ui.label_stride_src_name.setText("")
        self.ui.label_stride_link_name.setText("")
        self.ui.label_stride_dst_name.setText("")

        pos_link = self.ui.combobox_stride_link.currentIndex()
        if pos_link < 0:
            return

        self.ui.label_stride_src_name.setText(list_stride_links[pos_link].name_src)

        act_len = len(list_stride_links[pos_link].list_act)
        var_len = len(list_stride_links[pos_link].list_var)

        text = ""
        if act_len > 0:
            for act in list_stride_links[pos_link].list_act:
                if text != "":
                    text += "\n"
                text += act

        elif var_len > 0:
            for var in list_stride_links[pos_link].list_var:
                if text != "":
                    text += "\n"
                text += var

        self.ui.label_stride_link_name.setText(text)
        self.ui.label_stride_dst_name.setText(list_stride_links[pos_link].name_dst)

        if list_stride_links[pos_link].is_bound_trust == 1:
            qss = qss_red
            self.ui.label_stride_bound_trust.setStyleSheet("QLabel { font-size: 11pt; color : red; }")
        else:
            qss = qss_black
            self.ui.label_stride_bound_trust.setStyleSheet("QLabel { font-size: 11pt; color : black; }")


        self.ui.gbx_stride_link.setStyleSheet(qss)
        self.selection_change_stride_analysis()
        self.load_stride_requirements()

    def selection_change_stride_analysis(self):
        if self.ui.radiobutton_stride_src.isChecked():
            self.ui.label_stride_element.setText(self.ui.label_stride_src_name.text())
            self.on_security_elements_clicked()
        elif self.ui.radiobutton_stride_link.isChecked():
            self.ui.label_stride_element.setText(self.ui.label_stride_link_name.text())
            self.on_security_elements_clicked()
        elif self.ui.radiobutton_stride_dst.isChecked():
            self.ui.label_stride_element.setText(self.ui.label_stride_dst_name.text())
            self.on_security_elements_clicked()

    def on_security_elements_clicked(self):
        global onto, list_stride_links, list_stride_threats

        comp_type = ""
        self.ui.listwidget_stride_threats.clear()

        pos_link = self.ui.combobox_stride_link.currentIndex()
        if pos_link < 0:
            return

        type_src = list_stride_links[pos_link].type_src
        type_dst = list_stride_links[pos_link].type_dst
        dfd_id = -1

        if self.ui.radiobutton_stride_src.isChecked():
            dfd_id = list_stride_links[pos_link].id_dfd_src
        elif self.ui.radiobutton_stride_link.isChecked():
            dfd_id = list_stride_links[pos_link].id_dfd_link
        elif self.ui.radiobutton_stride_dst.isChecked():
            dfd_id = list_stride_links[pos_link].id_dfd_dst

        list_stride_threats = Security_tools_new.get_threats(onto, Security_tools_new.get_dfd_name(dfd_id))

        self.ui.listwidget_stride_threats.clear()
        self.ui.label_stride_threat.setText("")
        self.ui.label_stride_description.setText("")
        self.ui.label_stride_justification.setText("")
        for threat in list_stride_threats:
            self.ui.listwidget_stride_threats.addItem(threat)

    def on_listwidget_stride_threats_clicked(self):
        global list_stride_threats, list_stride_links, onto

        pos = self.ui.listwidget_stride_threats.currentRow()
        if pos < 0:
            return

        self.ui.label_stride_threat.setText(list_stride_threats[pos])

        pos_link = self.ui.combobox_stride_link.currentIndex()
        if pos_link < 0:
            return

        pos_threat = self.ui.listwidget_stride_threats.currentRow()
        if pos_threat < 0:
            return

        link = list_stride_links[pos_link].name_src + " -> " + list_stride_links[pos_link].name_dst
        context = ""
        for ca in list_stride_links[pos_link].list_act:
            if context != "":
                context += ", "
            context += ca

        for fb in list_stride_links[pos_link].list_var:
            if context != "":
                context += ", "
            context += fb


        if self.ui.radiobutton_stride_src.isChecked():
            desc, just, mec, son_list = Security_tools_new.generate_description_source(onto, list_stride_links[pos_link].name_src, list_stride_links[pos_link].name_dst, context, list_stride_threats[pos_threat])
        elif self.ui.radiobutton_stride_link.isChecked():
            desc, just, mec, son_list = Security_tools_new.generate_description_link(onto, link, context, list_stride_threats[pos_threat])
        elif self.ui.radiobutton_stride_dst.isChecked():
            desc, just, mec, son_list = Security_tools_new.generate_description_destiny(onto, list_stride_links[pos_link].name_dst, list_stride_links[pos_link].name_src, context, list_stride_threats[pos_threat])
        self.ui.label_stride_description.setText(desc)
        self.ui.label_stride_justification.setText(just)
        self.ui.label_stride_mechanism.setText(mec)

    def unselect_stride_analysis(self):
        self.ui.label_stride_src_name.setText("")
        self.ui.label_stride_link_name.setText("")
        self.ui.label_stride_dst_name.setText("")
        self.ui.radiobutton_stride_src.setEnabled(False)
        self.ui.radiobutton_stride_link.setEnabled(False)
        self.ui.radiobutton_stride_dst.setEnabled(False)

        self.ui.label_stride_element.setText("")
        self.ui.label_stride_threat.setText("")
        self.ui.label_stride_description.setText("")
        self.ui.label_stride_justification.setText("")

    def add_stride_requirement(self):
        global list_stride_uca_variable, list_stride_links, list_stride_uca, list_stride_threats, list_stride_requirements, onto, id_project

        pos_link = self.ui.combobox_stride_link.currentIndex()
        if pos_link < 0:
            showdialog("Attention", "Before continue you must select a link.")
            return

        pos_threat = self.ui.listwidget_stride_threats.currentRow()
        if pos_threat < 0:
            showdialog("Attention", "Before continue you must select a threat.")
            return

        link = list_stride_links[pos_link].name_src + " -> " + list_stride_links[pos_link].name_dst

        context = ""
        for ca in list_stride_links[pos_link].list_act:
            if context != "":
                context += ", "
            context += ca

        for cf in list_stride_links[pos_link].list_var:
            if context != "":
                context += ", "
            context += cf

        title = ""
        desc = ""
        just = ""
        id_component = -1
        if self.ui.radiobutton_stride_src.isChecked():
            title = list_stride_threats[pos_threat] + " attack to " + list_stride_links[pos_link].name_src + "."
            id_component = list_stride_links[pos_link].id_component_src
            desc, just, mec, son_list = Security_tools_new.generate_description_source(onto, list_stride_links[pos_link].name_src, list_stride_links[pos_link].name_dst, context, list_stride_threats[pos_threat])
        elif self.ui.radiobutton_stride_link.isChecked():
            title = list_stride_threats[pos_threat] + " attack to link " + link + "."
            desc, just, mec, son_list = Security_tools_new.generate_description_link(onto, link, context, list_stride_threats[pos_threat])
        elif self.ui.radiobutton_stride_dst.isChecked():
            title = list_stride_threats[pos_threat] + " attack to " + list_stride_links[pos_link].name_dst + "."
            id_component = list_stride_links[pos_link].id_component_dst
            desc, just, mec, son_list = Security_tools_new.generate_description_destiny(onto, list_stride_links[pos_link].name_dst, list_stride_links[pos_link].name_src, context, list_stride_threats[pos_threat])

        req = StrideDialog(title, list_stride_threats[pos_threat], link, desc, just, 0, mec, son_list, False, "")
        result = req.exec_()

        if result == 1:
            title = req.title.text()
            description = req.description.toPlainText()
            justification = req.justification.toPlainText()
            mechanism = req.mechanism.toPlainText()
            priority = req.comboBox.currentIndex() + 1
            link_id = list_stride_links[pos_link].id

            # print([item.text() for item in req.list_widget.selectedItems()])
            control_text = ""

            count = 0
            for c_req in list_stride_requirements:
                count += 1
                if c_req.description == description and c_req.justification == justification and c_req.title == title and c_req.mechanism == mechanism:
                    showdialog("Error", "This recommendation is alread created as R-" + str(count))
                    return

            stride_id = Constant.DB_ID_SPOOFING
            if list_stride_threats[pos_threat] == Constant.DB_NAME_TAMPERING:
                stride_id = Constant.DB_ID_TAMPERING
            elif list_stride_threats[pos_threat] == Constant.DB_NAME_REPUDIATION:
                stride_id = Constant.DB_ID_REPUDIATION
            elif list_stride_threats[pos_threat] == Constant.DB_NAME_INFORMATION_DISCLOSURE:
                stride_id = Constant.DB_ID_INFORMATION_DISCLOSURE
            elif list_stride_threats[pos_threat] == Constant.DB_NAME_DENIAL_OF_SERVICE:
                stride_id = Constant.DB_ID_DENIAL_OF_SERVICE
            elif list_stride_threats[pos_threat] == Constant.DB_NAME_ELEVATION_OF_PRIVILEGE:
                stride_id = Constant.DB_ID_ELEVATION_OF_PRIVILEGE

            dfd_id = Constant.DB_ID_PROCESS
            if self.ui.radiobutton_stride_src.isChecked():
                dfd_id = list_stride_links[pos_link].id_dfd_src
            elif self.ui.radiobutton_stride_link.isChecked():
                dfd_id = list_stride_links[pos_link].id_dfd_link
            elif self.ui.radiobutton_stride_dst.isChecked():
                dfd_id = list_stride_links[pos_link].id_dfd_dst


            DB_Sec_Stride_Requirement.insert_to_db(title, description, justification, mechanism, priority, id_component, link_id, dfd_id, stride_id, id_project, control_text)
            self.load_stride_requirements()
            return

    def load_stride_requirements(self):
        global list_stride_requirements, list_stride_links

        list_stride_requirements = []
        self.ui.listwidget_stride_requirements.clear()

        pos = self.ui.combobox_stride_link.currentIndex()
        if pos < 0:
            return
        list_stride_requirements = DB_Sec_Stride_Requirement.select_by_id_link(list_stride_links[pos].id)

        count = 1
        self.ui.lbl_stride_recommendations.setText("Number of recommendations: " + str(len(list_stride_requirements)))
        for req in list_stride_requirements:
            text = ""
            if req.is_imported == True:
                text += "(IMPORTED) "
            text += "R-" + str(count) + ": Priority " + req.name_priority + " [" + req.name_stride +"]\n"

            if req.id_component != None:
                text += "-> Component: " + req.name_comp_link + "\n"
            else:
                text += "-> Link: " + req.name_comp_link + "\n"

            # text += "STRIDE Element: " + req.name_stride + "\n"
            text += "Analysed as DFD Element: " + req.name_dfd + "\n"
            text += "Title: " + req.title + "\n"
            text += "Description: " + req.description + "\n"
            text += "Recommendation: " + req.justification + "\n"
            text += "Mechanism: " + req.mechanism + "\n"

            #controls = ""
            #for ctrl in req.list_of_controls:
            #    if controls != "":
            #        controls += "; "
            #    controls += ctrl.name
            #text += "Selected controls: " + controls + "\n"

            count += 1
            self.ui.listwidget_stride_requirements.addItem(text)

    def on_listwidget_stride_requirements_clicked(self):
        global list_stride_requirements, list_stride_links, onto

        pos = self.ui.listwidget_stride_requirements.currentRow()
        if pos < 0:
            showdialog("Attention", "Before continue you must select a recommendation.")
            return

        pos_link = self.ui.combobox_stride_link.currentIndex()
        if pos_link < 0:
            showdialog("Attention", "Before continue you must select a recommendation.")
            return

        # Copy line on click
        # cb = QApplication.clipboard()
        # cb.clear(mode=cb.Clipboard)
        # cb.setText(self.ui.listwidget_stride_requirements.currentItem().text(), mode=cb.Clipboard)

        edt_req = list_stride_requirements[pos]

        text = "Do you want to update or delete this  recommendation?"

        if edt_req.is_imported:
            text += "\n\nWARNING: you are updating an imported recommendation and this implies:" \
                    "\n- UPDATE will edit the original recommendation and the following links: "
            text += "\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req_except(edt_req.id, list_stride_links[pos_link].id)
        else:
            text += "\n\nThis recommendation is used in the following links:\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req(edt_req.id)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Change  recommendation")
        msgBox.setText(text)

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            link = DB_Components_Links.get_by_id(edt_req.id_link)
            l_text = ""
            if link != None:
                l_text = link.name_src + " -> " + link.name_dst


            controls_text, controls_list = Security_tools_new.get_subclass_of_countermeasure_class(onto, edt_req.name_stride)
            for ctrl_req in edt_req.list_of_controls:
                is_in = False
                for ctrl in controls_list:
                    if ctrl.name == ctrl_req.name:
                        is_in = True
                        ctrl.selected = True

                if is_in == False:
                    controls_list.append(ctrl_req)

            priority = edt_req.id_priority - 1
            req = StrideDialog(edt_req.title, edt_req.name_stride, l_text, edt_req.description, edt_req.justification, priority, edt_req.mechanism, controls_list, False, "")
            result = req.exec_()

            if result == 1:
                title = req.title.text()
                description = req.description.toPlainText()
                justification = req.justification.toPlainText()
                mechanism = req.mechanism.toPlainText()
                priority = req.comboBox.currentIndex() + 1

                performance_req = edt_req.performance_req

                DB_Sec_Stride_Requirement.update(edt_req.id, title, description, justification, mechanism, priority, "", performance_req)
                self.load_stride_requirements()
                return
        elif returnValue == 1:
            text_delete = "You want to delete the recommendation: " + edt_req.title + "\n\nAre you sure?"

            if edt_req.is_imported:
                text_delete += "\n\nWARNING: This is a imported recommendation, and deleting here will NOT affects the original recommendation and other link analysis."
            else:
                text_delete += "\n\nWARNING. Deleting this recommendation will affect the following links:\n" + DB_Sec_Stride_Requirement_Import.select_links_with_id_req(edt_req.id)

            msgBoxDel = QMessageBox()
            msgBoxDel.setIcon(QMessageBox.Information)

            msgBoxDel.setWindowTitle("Delete recommendation")
            msgBoxDel.setText(text_delete)

            msgBoxDel.addButton(QPushButton("Delete"), QMessageBox.YesRole)
            msgBoxDel.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

            returnValue = msgBoxDel.exec()
            if returnValue == 0:
                if edt_req.is_imported:
                    pos_link = self.ui.combobox_stride_link.currentIndex()
                    if pos_link < 0:
                        return

                    DB_Sec_Stride_Requirement_Import.delete_link_req(list_stride_links[pos_link].id, edt_req.id)
                else:
                    DB_Sec_Stride_Requirement.delete(edt_req.id)

                self.load_stride_requirements()
                return
    # ----- Functions Functions STRIDE analysis -----

    # ----- Functions DFD Elements -----
    def load_dfd_link_initialize(self):
        self.ui.combobox_dfd_bound_trust.clear()
        self.ui.combobox_dfd_bound_trust.addItem("No")
        self.ui.combobox_dfd_bound_trust.addItem("Yes")

    def load_dfd_initialize(self):
        global id_project, list_dfd_elements

        self.ui.combobox_dfd_elements.clear()
        list_dfd_elements = DB_Components.select_dfd_elements(id_project)

        text = ""
        for elm in list_dfd_elements:
            self.ui.combobox_dfd_elements.addItem(elm.name)

            if text != "":
                text += "\n"
            text += elm.name + " (" + self.get_component_by_ID(elm.id_thing) + " analyzed as " + Security_tools_new.get_dfd_name(
                elm.id_stride_dfd) + ")"

        self.ui.label_dfd_elements.setText(text)

    def load_dfd_links(self):
        global list_dfd_links

        self.ui.combobox_dfd_link.clear()
        list_dfd_links = DB_Components_Links.select_dfd_links(id_project)

        text_out_bt = "Link out of Boundary Trust:"
        text_in_bt = "Link in a Boundary Trust:"
        for link in list_dfd_links:
            if link.is_bound_trust == 0:
                text_i = ""
                if link.is_hlc and len(link.list_var) > 0:
                    text_i = " - from Controller"
                elif link.is_hlc and len(link.list_act) > 0:
                    text_i = " - to Controller"

                if len(link.list_act) > 0 and link.is_ext == False:
                    self.ui.combobox_dfd_link.addItem("(Control Action" + text_i + ") " + link.name_src + " -> " + link.name_dst)
                    text_out_bt += "\n\t(Control Action" + text_i + ") " + link.name_src + " -> " + link.name_dst

                if len(link.list_var) > 0 and link.is_ext == False:
                    self.ui.combobox_dfd_link.addItem("(Feedback" + text_i + ") " + link.name_src + " -> " + link.name_dst)
                    text_out_bt += "\n\t(Feedback" + text_i + ") " + link.name_src + " -> " + link.name_dst

                if len(link.list_act) > 0 and link.is_ext == True:
                    self.ui.combobox_dfd_link.addItem("(External Communication) " + link.name_src + " -> " + link.name_dst)
                    text_out_bt += "\n\t(External Communication) " + link.name_src + " -> " + link.name_dst

                if len(link.list_var) > 0 and link.is_ext == True:
                    self.ui.combobox_dfd_link.addItem("(External Communication) " + link.name_src + " -> " + link.name_dst)
                    text_out_bt += "\n\t(External Communication) " + link.name_src + " -> " + link.name_dst
            else:
                text_o = ""
                if link.is_hlc and len(link.list_var) > 0:
                    text_o = " - from Controller"
                elif link.is_hlc and len(link.list_act) > 0:
                    text_o = " - to Controller"

                if len(link.list_act) > 0 and link.is_ext == False:
                    self.ui.combobox_dfd_link.addItem("(Control Action" + text_o + ") " + link.name_src + " -> " + link.name_dst)
                    text_in_bt += "\n\t(Control Action" + text_o + ") " + link.name_src + " -> " + link.name_dst

                if len(link.list_var) > 0 and link.is_ext == False:
                    self.ui.combobox_dfd_link.addItem("(Feedback" + text_o + ") " + link.name_src + " -> " + link.name_dst)
                    text_in_bt += "\n\t(Feedback" + text_o + ") " + link.name_src + " -> " + link.name_dst

                if len(link.list_act) > 0 and link.is_ext == True:
                    self.ui.combobox_dfd_link.addItem("(External Communication) " + link.name_src + " -> " + link.name_dst)
                    text_in_bt += "\n\t(External Communication) " + link.name_src + " -> " + link.name_dst

                if len(link.list_var) > 0 and link.is_ext == True:
                    self.ui.combobox_dfd_link.addItem("(External Communication) " + link.name_src + " -> " + link.name_dst)
                    text_in_bt += "\n\t(External Communication) " + link.name_src + " -> " + link.name_dst

        self.ui.label_dfd_out_bt.setText(text_out_bt)
        self.ui.label_dfd_in_bt.setText(text_in_bt)

    def selection_change_dfd_elements(self):
        global list_dfd_elements, list_dfd_category

        self.ui.combobox_dfd_category.clear()
        pos = self.ui.combobox_dfd_elements.currentIndex()
        if pos < 0:
            return

        dfd_id = list_dfd_elements[pos].id_stride_dfd
        name_comp = self.get_component_by_ID(list_dfd_elements[pos].id_thing)
        list_dfd_category = Security_tools_new.get_dfd_element_only(onto, name_comp)

        dfd_list = DB_Sec_Stride_DFD.select_all()
        dfd_name = ""
        for dfd_db in dfd_list:
            if dfd_db.id == dfd_id:
                dfd_name = dfd_db.name

        count = 0
        select = 0 if len(list_dfd_category) > 0 else -1
        for dfd in list_dfd_category:
            self.ui.combobox_dfd_category.addItem(dfd)
            if dfd == dfd_name:
                select = count
            count += 1

        if select >= 0:
            self.ui.combobox_dfd_category.setCurrentIndex(select)

    def on_button_update_element_dfd_category(self):
        global list_dfd_elements, list_dfd_category

        pos_e = self.ui.combobox_dfd_elements.currentIndex()
        pos_c = self.ui.combobox_dfd_category.currentIndex()
        if pos_e < 0 or pos_c < 0:
            return

        DB_Components.update_component_dfd(list_dfd_elements[pos_e].id, list_dfd_category[pos_c])
        self.load_dfd_initialize()
        self.ui.combobox_dfd_elements.setCurrentIndex(pos_e)

    def on_button_hidden_links_clicked(self):
        global id_project
        title = "Physical links"
        text = "This is a list of Physical links. This links will be not analyzed.\n\n"

        list_omitted_links = DB_Components_Links.select_omitted_links(id_project)
        for omt in list_omitted_links:
            text += omt + "\n"

        showdialog(title, text)

    def selection_change_dfd_links(self):
        global list_dfd_links

        pos_link = self.ui.combobox_dfd_link.currentIndex()
        if pos_link < 0:
            return

        self.ui.combobox_dfd_bound_trust.setCurrentIndex(list_dfd_links[pos_link].is_bound_trust)

    def on_button_dfd_link_info_clicked(self):
        global list_dfd_links

        pos_link = self.ui.combobox_dfd_link.currentIndex()
        if pos_link < 0:
            return

        act_len = len(list_dfd_links[pos_link].list_act)
        var_len = len(list_dfd_links[pos_link].list_var)

        text = ""
        if act_len > 0:
            for act in list_dfd_links[pos_link].list_act:
                if text != "":
                    text += "\n"
                text += act

        elif var_len > 0:
            for var in list_dfd_links[pos_link].list_var:
                if text != "":
                    text += "\n"
                text += var

        title = list_dfd_links[pos_link].name_src + " -> " + list_dfd_links[pos_link].name_dst
        showdialog(title, text)

    def on_button_update_dfd_bound_trust(self):
        global list_dfd_links

        pos = self.ui.combobox_dfd_bound_trust.currentIndex()
        if pos < 0:
            return

        pos_link = self.ui.combobox_dfd_link.currentIndex()
        if pos_link < 0:
            return

        DB_Components_Links.update(list_dfd_links[pos_link].id, pos)
        self.load_dfd_links()
        self.ui.combobox_dfd_link.setCurrentIndex(pos_link)

    # ----- Functions DFD Elements -----

    # ----- Functions STPA report Step -----
    def on_button_fifith_stpa_report_clicked(self):
        global stpa_pdf_report_list

        try:
            result = Generate_PDF(id_project)
            if result == "Error":
                showdialog("Error to create PDF", "If the file is open, close and try again...")
            else:
                showdialog("New Report", result)
        except Exception as e:
            showdialog("Error to create PDF", "If the file is open, close and try again...\n\n" + str(e))
            print(e)

    def get_label_14_title(self, text):
        global stpa_pdf_report_list

        font_14 = QFont('Arial', 14)

        self.label = QLabel()
        self.label.setFont(font_14)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setText(text)
        return self.label

    def get_label_image(self, path):
        global stpa_pdf_report_list

        self.label = QLabel()

        pixmap = QtGui.QPixmap(path)
        width = 1000
        iw = pixmap.width()
        ih = pixmap.height()
        aspect = ih / float(iw)
        height = int(width * aspect)
        self.label.setPixmap(pixmap.scaled(width, height, Qt.KeepAspectRatio))

        return self.label

    def get_label_12_bold_subtitle(self, text):
        font_12_b = QFont('Arial', 12)
        font_12_b.setBold(True)

        self.label = QLabel()
        self.label.setFont(font_12_b)
        self.label.setWordWrap(True)
        self.label.setText(text)

        return self.label

    def get_label_12_text(self, text):
        global stpa_pdf_report_list

        font_12_b = QFont('Arial', 12)

        self.label = QLabel()
        self.label.setFont(font_12_b)
        self.label.setWordWrap(True)
        self.label.setText("  " + text)

        return self.label

    def get_label_11_text(self, text):
        global stpa_pdf_report_list

        font_11 = QFont('Arial', 11)
        self.label = QLabel()
        self.label.setFont(font_11)
        self.label.setWordWrap(True)
        self.label.setText("  " + text)

        return self.label

    def load_stpa_report(self):
        global id_project, stpa_pdf_report_list

        stpa_pdf_report_list = []

        list_goals_fifth = DB_Goals.select_all_goals_by_project(id_project)
        list_assumptions_fifth = DB_Assumptions.select_all_assumptions_by_project(id_project)
        list_losses_fifth = DB_Losses.select_all_losses_by_project(id_project)
        list_hazards_fifth = DB_Hazards.select_all_hazards_by_project(id_project)
        list_constraints_fifth = DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project)

        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout()
        group_box = QtWidgets.QGroupBox()
        group_box.setTitle("")
        group_box.setFont(QFont('Arial', 11))
        layout = QtWidgets.QVBoxLayout(group_box)

        project = DB_Projects.select_project_by_id(id_project)
        layout.addWidget(self.get_label_14_title("STPA analysis of " + project.name))
        layout.addWidget(self.get_label_12_text(project.description))
        layout.addWidget(self.get_label_12_text("Begin date: " + project.begin_date))
        # layout.addWidget(self.get_label_12_text("Last update: " + project.edited_date))

        # step one
        layout.addWidget(self.get_label_14_title("\n\nStep One - Purpose of the Analysis"))
        layout.addWidget(self.get_label_12_bold_subtitle("Goals"))
        for pos in range(len(list_goals_fifth)):
            layout.addWidget(self.get_label_11_text(
                "G-" + str(list_goals_fifth[pos].id_goal) + ": " + list_goals_fifth[pos].description))

        layout.addWidget(self.get_label_12_bold_subtitle("Assumptions"))
        for pos in range(len(list_assumptions_fifth)):
            layout.addWidget(self.get_label_11_text(
                "A-" + str(list_assumptions_fifth[pos].id_assumption) + ": " + list_assumptions_fifth[
                    pos].description))

        layout.addWidget(self.get_label_12_bold_subtitle("Losses"))
        for pos in range(len(list_losses_fifth)):
            layout.addWidget(self.get_label_11_text(
                "L-" + str(list_losses_fifth[pos].id_loss) + ": " + list_losses_fifth[pos].description))

        layout.addWidget(self.get_label_12_bold_subtitle("System-level Hazards"))
        for pos in range(len(list_hazards_fifth)):
            text = ""
            for loss in list_hazards_fifth[pos].list_of_loss:
                text += "[L-" + str(loss.id_loss_screen) + "] "

            layout.addWidget(self.get_label_11_text(
                "H-" + str(list_hazards_fifth[pos].id_hazard) + ": " + list_hazards_fifth[
                    pos].description + " " + text))

        layout.addWidget(self.get_label_12_bold_subtitle("Systel-level Safety Constraints"))
        for pos in range(len(list_constraints_fifth)):
            text = ""
            for haz in list_constraints_fifth[pos].list_of_hazards:
                text += "[H-" + str(haz.id_haz_screen) + "] "

            layout.addWidget(self.get_label_11_text(
                "SSC-" + str(list_constraints_fifth[pos].id_safety_constraint) + ": " + list_constraints_fifth[
                    pos].description + " " + text))

        # step 2
        layout.addWidget(self.get_label_14_title("\n\nStep Two - Control Structure"))
        self.get_component_report(layout, DB_Components.select_component_by_thing_project_analysis(
            Constant.DB_ID_CONTROLLER, id_project), Constant.DB_ID_CONTROLLER)
        self.get_component_report(layout,
                                  DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_ACTUATOR,
                                                                                           id_project),
                                  Constant.DB_ID_ACTUATOR)
        self.get_component_report(layout, DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_SENSOR,
                                                                                           id_project),
                                  Constant.DB_ID_SENSOR)
        self.get_component_report(layout, DB_Components.select_component_by_thing_project_analysis(
            Constant.DB_ID_EXT_INFORMATION, id_project), Constant.DB_ID_EXT_INFORMATION)
        self.get_component_report(layout,
                                  DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP,
                                                                                           id_project),
                                  Constant.DB_ID_CP)

        # step 3
        layout.addWidget(self.get_label_14_title("\nStep Three - Unsafe Control Actions"))
        layout.addWidget(self.get_label_12_bold_subtitle("Unsafe Control Actions (UCA) and Safety Constraints (SC)"))
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

            item_uca_r = "Constraint " + str(count_usc) + ": (Controller: " + uca.name_controller + " - Control Action: " + uca.name_action + ")"
            layout.addWidget(self.get_label_11_text(item_uca_r))

            item_uca_u = "UCA-" + str(
                count_usc) + ": " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action
            if text_context == "":
                item_uca_u += " in any context."
            else:
                item_uca_u += " when " + text_context + ". "
            item_uca_u += " " + text_haz
            layout.addWidget(self.get_label_11_text(item_uca_u))

            item_uca_u_desc = "Description: "
            if uca.description != None:
                item_uca_u_desc += uca.description
            layout.addWidget(self.get_label_11_text(item_uca_u_desc))

            item_uca_s = "SC-" + str(count_usc) + ": " + uca.name_controller + " shall " + self.get_opposite_uca(
                uca.id_uca_type) + " " + uca.name_action
            if text_context == "":
                item_uca_s += " in any context."
            else:
                item_uca_s += " when " + text_context + ". "

            item_uca_s += "\n"
            layout.addWidget(self.get_label_11_text(item_uca_s))

        # step 4
        layout.addWidget(self.get_label_14_title("\nStep Four - Loss Scenarios and Recommendations"))
        count_ls = 0
        for rec in DB_Loss_Scenario_Req.select_all(id_project):
            count_ls += 1
            spacer = " -> "
            if Constant.ALGORITHM in rec.name_src or Constant.PROCESS_MODEL_full_name in rec.name_src:
                spacer = " in "

            layout.addWidget(self.get_label_11_text(
                "R-" + str(count_ls) + " (" + rec.name_src + spacer + rec.name_dst + "): UCA-" + str(self.get_number_uca(rec.id_uca, list_aux_uca))))
            layout.addWidget(self.get_label_11_text("Type: " + rec.classification))
            layout.addWidget(self.get_label_11_text("Cause: " + rec.cause))
            layout.addWidget(self.get_label_11_text("Recommendation: " + rec.requirement))
            layout.addWidget(self.get_label_11_text("Mechanism: " + rec.mechanism + "\n"))

        top_layout.addWidget(group_box)
        top_widget.setLayout(top_layout)
        self.ui.scrollArea_fifith_report.setWidget(top_widget)

        # report
        layout.addWidget(self.get_label_14_title("\nLink with energy"))
        list_omitted_links = DB_Components_Links.select_omitted_links(id_project)
        for omt in list_omitted_links:
            layout.addWidget(self.get_label_11_text(omt))

        # show control structure images
        layout.addWidget(self.get_label_14_title("\nShow control structure images"))
        has_image = False

        try:
            path_one = DB_Project_Files.select_images_by_project(id_project, 1)
            if path_one != "":
                layout.addWidget(self.get_label_image(path_one))
                has_image = True
        except NameError as e:
            print(e)

        try:
            path_two = DB_Project_Files.select_images_by_project(id_project, 2)
            if path_two != "":
                layout.addWidget(self.get_label_image(path_two))
                has_image = True
        except NameError as e:
            print(e)

        try:
            path_three = DB_Project_Files.select_images_by_project(id_project, 3)
            if path_three != "":
                layout.addWidget(self.get_label_image(path_three))
                has_image = True
        except NameError as e:
            print(e)

        if not has_image:
            layout.addWidget(self.get_label_12_text("No control structure images found."))

    def get_number_uca(self, id_uca, list_aux_uca):
        count = 1
        for uca in list_aux_uca:
            if uca.id == id_uca:
                return count
            count += 1
        return 0

    def get_component_report(self, layout, list_of_components, id_comp):
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

            layout.addWidget(self.get_label_12_bold_subtitle(aux_name))

            if (id_comp == Constant.DB_ID_CONTROLLER):
                layout.addWidget(self.get_label_12_text("responsibilities: "))

                list_responsibility = DB_Responsibility.select_all_responsibilities_by_controller(comp.id)

                for pos in range(len(list_responsibility)):

                    text = ""
                    for ssc in list_responsibility[pos].list_of_ssc:
                        text += "[SSC-" + str(ssc.id_constraint_screen) + "] "

                    layout.addWidget(self.get_label_11_text(
                        "    R-" + str(list_responsibility[pos].id_screen) + ": " + str(
                            list_responsibility[pos].description + ". " + text)))


            layout.addWidget(self.get_label_12_text("Outgoing connections"))
            for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, True):
                layout.addWidget(self.get_label_11_text("    " + link.name_src + " -> " + link.name_dst))
                # if id_comp == Constant.DB_ID_CONTROLLER or id_comp == Constant.DB_ID_CP or id_comp == Constant.DB_ID_SENSOR:
                if id_comp == Constant.DB_ID_CONTROLLER:
                    self.get_component_report_actions(layout, comp.id, id_project, link.id)
                    self.get_component_report_feedback(layout, comp.id, id_project, link.id)

            layout.addWidget(self.get_label_12_text("Incoming connections"))
            for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, False):
                layout.addWidget(self.get_label_11_text("    " + link.name_src + " -> " + link.name_dst))
                if id_comp == Constant.DB_ID_CONTROLLER:
                    self.get_component_report_actions(layout, comp.id, id_project, link.id)
                    self.get_component_report_feedback(layout, comp.id, id_project, link.id)

            if (id_comp == Constant.DB_ID_CP):
                self.get_report_cp(layout, id_project, comp.id)

            layout.addWidget(self.get_label_11_text(" "))

    def get_component_report_actions(self, layout, id_comp, id_project, id_link):
        list_a = DB_Actions_Components.select_actions_by_component_project_link(id_comp, id_project, id_link)
        if len(list_a) > 0:
            aux_a = ""
            for act in list_a:
                if aux_a != "":
                    aux_a += ", "
                aux_a += act.name
            layout.addWidget(self.get_label_11_text("\tControl actions: " + aux_a))

    def get_component_report_feedback(self, layout, id_comp, id_project, id_link):
        list_v = DB_Variables.select_variables_with_value_by_controller_project_link(id_comp, id_project, id_link)
        if len(list_v) > 0:
            layout.addWidget(self.get_label_11_text("\tFeedbacks (variables and values):"))
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
                layout.addWidget(self.get_label_11_text("\t    " + aux_v))

    def get_report_cp(self, layout, id_project, id_father):
        text_inp = ""
        for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_INPUT):
            if text_inp != "":
                text_inp += ", "
            text_inp += comp_i

        if text_inp != "":
            layout.addWidget(self.get_label_11_text("Input: " + text_inp))

        text_out = ""
        for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_OUTPUT):
            if text_out != "":
                text_out += ", "
            text_out += comp_i

        if text_out != "":
            layout.addWidget(self.get_label_11_text("Output: " + text_out))

        text_env = ""
        for comp_i in DB_Components.select_controlled_process_values(id_project, id_father,
                                                                     Constant.DB_ID_ENV_DISTURBANCES):
            if text_env != "":
                text_env += ", "
            text_env += comp_i

        if text_env != "":
            layout.addWidget(self.get_label_11_text("Environmental Disturbances: " + text_env))

    def get_opposite_uca(self, id):
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
    # ----- Functions STPA report Step -----

    # ----- Functions Graphical Structure image -----
    def get_file_extension(self, src, current_date):
        dst = "0"
        if ".png" in src.lower():
            dst = Constant.FILES_REPO + "\\" + str(id_project) + "_" + current_date + ".png"
        elif ".jpg" in src.lower():
            dst = Constant.FILES_REPO + "\\" + str(id_project) + "_" + current_date + ".jpg"
        elif ".jpeg" in src.lower():
            dst = Constant.FILES_REPO + "\\" + str(id_project) + "_" + current_date + ".jpeg"
        else:
            showdialog("Wrong format", "Please select only image files (PNG or JPG)")

        return dst

    def on_button_select_file_one_clicked(self):
        global id_project

        try:
            fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.jpeg *.jpg)')
            # fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.png *.jpeg *.jpg)')
            src = fname[0]

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK_FILE_COPY)

            if os.path.exists(src):
                dst = self.get_file_extension(src, current_date)
                if dst == "0":
                    return

                to_delete = DB_Project_Files.select_images_by_project(id_project, 1)
                if to_delete != "" and os.path.exists(to_delete):
                    os.remove(to_delete)

                copyfile(src, dst)
                id = DB_Project_Files.insert_control_srtucture_file(id_project, dst, current_date, 1)

                if id > 0:
                    showdialog("Success", "Image imported")
                    self.ui.label_image_pic_one.setPixmap(QtGui.QPixmap(dst))
                    self.ui.label_image_pic_one.show()

                else:
                    showdialog("Error", "ry again, Try to import only files PNG or JPG")
        except NameError as e:
            print(e)

    def on_button_select_file_two_clicked(self):
        global id_project

        try:
            fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.jpeg *.jpg)')
            # fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.png *.jpeg *.jpg)')
            src = fname[0]

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK_FILE_COPY)

            if os.path.exists(src):
                dst = self.get_file_extension(src, current_date)
                if dst == "0":
                    return

                to_delete = DB_Project_Files.select_images_by_project(id_project, 2)
                if to_delete != "" and os.path.exists(to_delete):
                    os.remove(to_delete)

                copyfile(src, dst)
                id = DB_Project_Files.insert_control_srtucture_file(id_project, dst, current_date, 2)

                if id > 0:
                    showdialog("Success", "Image imported")
                    self.ui.label_image_pic_two.setPixmap(QtGui.QPixmap(dst))
                    self.ui.label_image_pic_two.show()

                else:
                    showdialog("Error", "ry again, Try to import only files PNG or JPG")
        except NameError as e:
            print(e)

    def on_button_select_file_three_clicked(self):
        global id_project

        try:
            fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.jpeg *.jpg)')
            # fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.png *.jpeg *.jpg)')
            src = fname[0]

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK_FILE_COPY)

            if os.path.exists(src):
                dst = self.get_file_extension(src, current_date)
                if dst == "0":
                    return

                to_delete = DB_Project_Files.select_images_by_project(id_project, 3)
                if to_delete != "" and os.path.exists(to_delete):
                    os.remove(to_delete)

                copyfile(src, dst)
                id = DB_Project_Files.insert_control_srtucture_file(id_project, dst, current_date, 3)

                if id > 0:
                    showdialog("Success", "Image imported")
                    self.ui.label_image_pic_three.setPixmap(QtGui.QPixmap(dst))
                    self.ui.label_image_pic_three.show()

                else:
                    showdialog("Error", "ry again, Try to import only files PNG or JPG")
        except NameError as e:
            print(e)

    def on_button_delete_file_one_clicked(self):
        global id_project

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Delete first image")
        msgBox.setText("Are you sure that you to delete the first image?")

        msgBox.addButton(QPushButton("Delete"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            to_delete = DB_Project_Files.select_images_by_project(id_project, 1)
            DB_Project_Files.delete_file(id_project, 1)
            if to_delete != "" and os.path.exists(to_delete):
                os.remove(to_delete)

            self.load_control_structure_image()

    def on_button_delete_file_two_clicked(self):
        global id_project

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Delete second image")
        msgBox.setText("Are you sure that you to delete the second image?")

        msgBox.addButton(QPushButton("Delete"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            to_delete = DB_Project_Files.select_images_by_project(id_project, 2)
            DB_Project_Files.delete_file(id_project, 2)
            if to_delete != "" and os.path.exists(to_delete):
                os.remove(to_delete)

            self.load_control_structure_image()

    def on_button_delete_file_three_clicked(self):
        global id_project

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Delete third image")
        msgBox.setText("Are you sure that you to delete the third image?")

        msgBox.addButton(QPushButton("Delete"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            to_delete = DB_Project_Files.select_images_by_project(id_project, 3)
            DB_Project_Files.delete_file(id_project, 3)
            if to_delete != "" and os.path.exists(to_delete):
                os.remove(to_delete)

            self.load_control_structure_image()

    def load_control_structure_image(self):
        global id_project

        self.ui.label_image_pic_one.setPixmap(QtGui.QPixmap(Constant.DEFAULT_IMAGE_PATH))
        self.ui.label_image_pic_two.setPixmap(QtGui.QPixmap(Constant.DEFAULT_IMAGE_PATH))
        self.ui.label_image_pic_three.setPixmap(QtGui.QPixmap(Constant.DEFAULT_IMAGE_PATH))

        try:
            self.ui.label_image_pic_one.show()
            path_one = DB_Project_Files.select_images_by_project(id_project, 1)
            if path_one != "":
                self.ui.label_image_pic_one.setPixmap(QtGui.QPixmap(path_one))
            self.ui.label_image_pic_one.show()
        except NameError as e:
            print(e)


        try:
            self.ui.label_image_pic_two.show()
            path_two = DB_Project_Files.select_images_by_project(id_project, 2)
            if path_two != "":
                self.ui.label_image_pic_two.setPixmap(QtGui.QPixmap(path_two))
            self.ui.label_image_pic_two.show()
        except NameError as e:
            print(e)

        try:
            self.ui.label_image_pic_three.show()
            path_three = DB_Project_Files.select_images_by_project(id_project, 3)
            if path_three != "":
                self.ui.label_image_pic_three.setPixmap(QtGui.QPixmap(path_three))
            self.ui.label_image_pic_three.show()
        except NameError as e:
            print(e)

    # ----- Functions Graphical Structure image -----

    # ----- Functions STPA 4 Step -----
    def selection_change_controller_fourth(self, i):
        self.load_combobox_fourth_control_action()

    def selection_change_control_action_fourth(self, i):
        self.load_uca_fourth()

    def selection_change_uca_fourth(self, i):
        self.load_loss_scenarios_requirements()

    def load_combobox_fourth_controller(self):
        global list_four_controller, id_project

        list_four_controller = DB_Components.select_controller_not_external_project_analysis(id_project)
        self.ui.combobox_fourth_controller.setEnabled(True)
        self.ui.combobox_fourth_controller.clear()

        for conn in list_four_controller:
            self.ui.combobox_fourth_controller.addItem(conn.name)

        if len(list_four_controller) == 0:
            self.ui.combobox_fourth_control_action.clear()
            self.ui.listwidget_fourth_uca.clear()
            self.ui.listwidget_fourth_causal_factor.clear()
            self.ui.listwidget_fourth_requirement.clear()
        elif len(list_four_controller) > 0:
            self.load_combobox_fourth_control_action()

    def load_fourth_loss_img(self):
        try:
            self.ui.label_fourth_loss_img.setPixmap(QtGui.QPixmap(Constant.DEFAULT_IMAGE_PATH))
        except NameError as e:
            print(e)

        try:
            # pixmap = QtGui.QPixmap(Constant.IMAGE_STPA_LOSS).scaledToWidth(700)
            # self.ui.label_fourth_loss_img.setPixmap(pixmap)
            self.ui.label_fourth_loss_img.setPixmap(QtGui.QPixmap(Constant.IMAGE_STPA_LOSS))
        except NameError as e:
            print(e)

    def load_combobox_fourth_control_action(self):
        global list_four_control_action, id_project

        pos = self.ui.combobox_fourth_controller.currentIndex()

        if pos < 0:
            return

        list_four_control_action = DB_Actions_Components.select_actions_by_component_and_project(
            list_four_controller[pos].id, id_project)

        self.ui.combobox_fourth_control_action.clear()
        self.ui.combobox_fourth_control_action.setEnabled(True)

        for pos in range(len(list_four_control_action)):
            self.ui.combobox_fourth_control_action.addItem(list_four_control_action[pos].name)

        if len(list_four_control_action) > 0:
            self.load_uca_fourth()
        else:
            self.ui.listwidget_fourth_uca.clear()
            self.ui.listwidget_fourth_causal_factor.clear()
            self.ui.listwidget_fourth_requirement.clear()

    def load_uca_fourth(self):
        global list_fourth_uca
        pos = self.ui.combobox_fourth_control_action.currentIndex()
        if len(list_four_control_action) > 0:
            list_fourth_uca = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_four_control_action[pos].id,
                                                                                    Constant.UCA_RULE, True)
            list_fourth_uca.extend(
                DB_UCA.select_all_saf_uca_by_control_action_filtering(list_four_control_action[pos].id,
                                                                      Constant.UCA_CELL, True))
            self.ui.listwidget_fourth_uca.clear()
            self.ui.listwidget_fourth_uca.setEnabled(True)

            count_r = 0
            count_c = 0
            for uca in list_fourth_uca:
                text = "UCA"
                if uca.uca_origin == Constant.UCA_RULE:
                    count_r += 1
                    text += "_R-" + str(count_r)
                else:
                    count_c += 1
                    text += "_C-" + str(count_c)

                text += " " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action

                text_context = ""
                for context in uca.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value

                if text_context == "":
                    text += " in any context. "
                else:
                    text += " when " + text_context + ". "

                # text += text_context + ". "
                for haz in uca.hazard_list:
                    text += "[H-" + str(haz.hazard_order) + "]"

                self.ui.listwidget_fourth_uca.addItem(text)

            self.load_loss_scenarios()
            self.load_loss_scenarios_requirements()
        else:
            self.ui.listwidget_fourth_uca.setEnabled(False)

    def load_loss_scenarios(self):
        global list_four_control_action, list_fourth_uca, list_four_controller, list_four_loss_causal

        if len(list_fourth_uca) == 0 or len(list_four_controller) == 0:
            self.ui.listwidget_fourth_causal_factor.clear()
            self.ui.listwidget_fourth_requirement.clear()
            return

        pos_c = self.ui.combobox_fourth_controller.currentIndex()
        list_four_loss_causal = Safety_tools_new.get_step_four(onto, id_project, list_four_controller[pos_c])
        self.ui.listwidget_fourth_causal_factor.clear()

        for loss in list_four_loss_causal:
            # item = color.BOLD + "Side: " + loss.side + color.END + " - " + loss.onto_name + "\n"
            # item += color.BOLD + "Cause: " + loss.causes + color.END + " - " + loss.onto_name
            # side = "Right"
            # if loss.side == "B":
            #     side = "Left"

            item = ">> " + loss.classification + "\n"
            item += "Element: " + loss.onto_name + "\n"
            item += "Causal Factor: " + loss.causes + "\n"
            item += "Recommendation: " + loss.requirement + "\n"

            self.ui.listwidget_fourth_causal_factor.addItem(item)

        # result_list.append(color.BOLD + "Left: " + color.END + r_text)

    def selection_change_causal_factor_fourth(self):
        global list_four_loss_causal
        pos = self.ui.listwidget_fourth_causal_factor.currentRow()

        self.clear_recommendation_fields()

        if pos == -1:
            # showdialog("No causal factor selected", "Select at least one causal factor")
            return

        lc = list_four_loss_causal[pos]
        text = lc.name_src + " -> " + lc.name_dst
        desc = "Interaction:"

        if lc.name_src == lc.name_dst or lc.name_src.lower().__contains__("process model") or lc.name_src.lower().__contains__("algorithm"):
            desc = "Element:"
            text = lc.name_src

        self.ui.label_fourth_interaction.setText(desc)
        self.ui.label_fourth_interaction_desc.setText(text)
        self.ui.label_fourth_cause.setText(lc.causes)
        self.ui.label_fourth_recommendation.setText(lc.requirement)

    def load_loss_scenarios_requirements(self):
        global list_four_requirements, id_project, list_fourth_uca

        self.ui.listwidget_fourth_requirement.clear()

        if len(list_fourth_uca) == 0:
            return

        pos_u = self.ui.listwidget_fourth_uca.currentRow()
        if pos_u > -1:
            list_four_requirements = DB_Loss_Scenario_Req.select_all_requirements_by_project_uca(id_project, list_fourth_uca[pos_u].id)
            count = 0
            for req in list_four_requirements:
                count += 1
                spacer = " -> "
                if Constant.ALGORITHM in req.name_src or Constant.PROCESS_MODEL_full_name in req.name_src:
                    spacer = " in "

                src_dst = req.name_src
                if req.name_src != req.name_dst:
                    src_dst = req.name_src + spacer + req.name_dst

                item = "R-" + str(count) + " (" + src_dst + "): \n"
                item += "Type: " + req.classification + "\n"
                item += "Cause: " + req.cause + "\n"
                item += "Recommendation: " + req.requirement + "\n"
                item += "Mechanism: " + req.mechanism + "\n"
                self.ui.listwidget_fourth_requirement.addItem(item)

    def on_button_fourth_add_causal_factor_clicked(self):
        global list_fourth_uca, list_four_controller, list_four_control_action, id_project, list_four_loss_causal

        pos_c = self.ui.combobox_fourth_controller.currentIndex()
        pos_a = self.ui.combobox_fourth_control_action.currentIndex()
        pos_u = self.ui.listwidget_fourth_uca.currentRow()
        pos_cause = self.ui.listwidget_fourth_causal_factor.currentRow()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        elif pos_a == -1:
            showdialog("No control action selected", "Select the control action")
            return
        elif pos_u == -1:
            showdialog("No UCA selected", "Select the UCA")
            return
        elif pos_cause == -1:
            showdialog("No causal factor selected", "Select at least one causal factor")
            return

        lc = list_four_loss_causal[pos_cause]
        req_id_saved = self.is_requirement_cause_saved(lc.requirement, lc.causes, lc.mechanism)
        if req_id_saved > 0:
            showdialog("No need to save", "The current recommendation is saved as Recommendation " + str(req_id_saved))
            return

        req = Loss_Scenario_Req(0,
                                list_four_controller[pos_c].id,
                                list_fourth_uca[pos_u].id,
                                id_project,
                                lc.id_component,
                                lc.id_component_src,
                                lc.id_component_dst,
                                lc.requirement,
                                lc.causes,
                                lc.mechanism,
                                "", "", "", "", lc.classification)

        id_req = DB_Loss_Scenario_Req.insert(req)

        if id_req > 0:
            showdialog("Success", "Recommendation created!")
            self.load_loss_scenarios_requirements()
        else:
            showdialog("Error", "Cannot save recommendation now, try again!")

    def on_button_fourth_create_causal_factor_clicked(self):
        global list_fourth_uca, list_four_controller, list_four_control_action, id_project, list_four_loss_causal

        pos_c = self.ui.combobox_fourth_controller.currentIndex()
        pos_a = self.ui.combobox_fourth_control_action.currentIndex()
        pos_u = self.ui.listwidget_fourth_uca.currentRow()
        pos_cause = self.ui.listwidget_fourth_causal_factor.currentRow()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        elif pos_a == -1:
            showdialog("No control action selected", "Select the control action")
            return
        elif pos_u == -1:
            showdialog("No UCA selected", "Select the UCA")
            return
        elif pos_cause == -1:
            showdialog("No causal factor selected", "Select at least one causal factor")
            return

        lc = list_four_loss_causal[pos_cause]
        cf = CausalFactorDialog(lc.causes, lc.requirement, lc.mechanism, lc.name_src, lc.name_dst, "", False, "")
        result = cf.exec_()

        if result == 1:
            cause = cf.cause.toPlainText()
            requirement = cf.requirement.toPlainText()
            mechanism = cf.mechanism.toPlainText()
            # priority = cf.comboBox.currentIndex() + 1

            if len(cause) == 0 or len(requirement) == 0:
                showdialog("Error to create a new recommendation",
                           "You must fill all the fields to create a new recommendation.")
                return

            req_id_saved = self.is_requirement_cause_saved(requirement, cause, mechanism)
            if req_id_saved > 0:
                showdialog("No need to save",
                           "The current recommendation is saved as Recommendation " + str(req_id_saved))
                return

            lc = list_four_loss_causal[pos_cause]
            req = Loss_Scenario_Req(0,
                                    list_four_controller[pos_c].id,
                                    list_fourth_uca[pos_u].id,
                                    id_project,
                                    lc.id_component,
                                    lc.id_component_src,
                                    lc.id_component_dst,
                                    requirement,
                                    cause,
                                    mechanism,
                                    "", "", "", "", lc.classification)

            id_req = DB_Loss_Scenario_Req.insert(req)

            if id_req > 0:
                # showdialog("Success", "Recommendation created!")
                self.load_loss_scenarios_requirements()
            else:
                showdialog("Error", "Cannot save Recommendation now, try again!")

    def selection_change_requirement_fourth(self):
        global list_four_requirements

        pos = self.ui.listwidget_fourth_requirement.currentRow()
        if pos == -1:
            showdialog("No recommendation selected", "Select one recommendation to delete")
            return

        # cb = QApplication.clipboard()
        # cb.clear(mode=cb.Clipboard)
        # cb.setText(self.ui.listwidget_fourth_requirement.currentItem().text(), mode=cb.Clipboard)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            edt_req = list_four_requirements[pos]
            # priority = edt_req.id_priority - 1
            cf = CausalFactorDialog(edt_req.cause, edt_req.requirement, edt_req.mechanism, edt_req.name_src, edt_req.name_dst, edt_req.name_cause, False, "")
            result = cf.exec_()

            if result == 1:
                cause = cf.cause.toPlainText()
                recommendation = cf.requirement.toPlainText()
                mechanism = cf.mechanism.toPlainText()
                # priority = cf.comboBox.currentIndex() + 1

                performance_req = edt_req.performance_req

                DB_Loss_Scenario_Req.update(edt_req.id, cause, recommendation, mechanism, performance_req)
                self.load_loss_scenarios_requirements()
                return
        elif returnValue == 1:
            pos = self.ui.listwidget_fourth_requirement.currentRow()

            if pos == -1:
                showdialog("No recommendation selected", "Select one recommendation to delete")
                return

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Loss_Scenario_Req.delete_by_id(list_four_requirements[pos].id)
                self.load_loss_scenarios_requirements()

    def is_requirement_cause_saved(self, requirement, cause, mechanism):
        global list_four_requirements

        count = 0
        for item in list_four_requirements:
            count += 1
            if item.cause == cause and item.requirement == requirement and item.mechanism == mechanism:
                return count

        return 0

    def clear_recommendation_fields(self):
        self.ui.label_fourth_interaction_desc.setText("")
        self.ui.label_fourth_cause.setText("")
        self.ui.label_fourth_recommendation.setText("")
        self.ui.label_fourth_mechanism.setText("")
    # ----- Functions STPA 4 Step -----

    # ----- Functions STPA 3 Step -----

    def selection_change_controller_third(self, i):
        self.load_combobox_third_control_action()

    def selection_change_control_action_third(self, i):
        self.load_variables_dynamically()
        self.load_uca_third()

    def load_combobox_third_controller(self):
        global list_three_controller, id_project

        list_three_controller = DB_Components.select_controller_not_external_project_analysis(id_project)
        self.ui.combobox_third_controller.clear()

        for conn in list_three_controller:
            self.ui.combobox_third_controller.addItem(conn.name)

        if len(list_three_controller) == 0:
            list_three_control_action = []
            self.ui.combobox_third_control_action.clear()
            self.ui.combobox_third_control_action.setEnabled(False)
            self.ui.listwidget_third_uca_rule.clear()
            self.ui.listwidget_third_uca_cell.clear()
            self.ui.listwidget_third_uca_safe.clear()
            self.ui.tablewidget_third_context.clear()
            self.ui.tablewidget_third_context.setRowCount(0)
            self.ui.tablewidget_third_context.setColumnCount(0)
        elif len(list_three_controller) > 0:
            self.load_combobox_third_control_action()

    def load_combobox_third_control_action(self):
        global list_three_control_action, list_three_controller, id_project, list_third_uca_type, list_third_var_comp

        pos = self.ui.combobox_third_controller.currentIndex()
        if pos < 0:
            return

        list_three_control_action = DB_Actions_Components.select_actions_by_component_and_project(list_three_controller[pos].id, id_project)

        self.ui.combobox_third_control_action.clear()
        self.ui.combobox_third_control_action.setEnabled(True)

        for pos in range(len(list_three_control_action)):
            self.ui.combobox_third_control_action.addItem(list_three_control_action[pos].name)

        self.load_variables_dynamically()

    # def find_hazardous_UCA(self, row, column, context_list):
    #     global list_third_uca
    #     pos = 0
    #     for uca in list_third_uca:
    #         pos +=1
    #         for ctx in uca.context_list:
    #             for var in context_list:
    #                 col = column + uca.id_uca_type - 1
    #
    #                 if ctx.id_variable == var.var_id and ctx.id_value == var.val_id:
    #                     cell = self.ui.tablewidget_third_context.item(row, col).text()
    #                     text = " UR-" + str(pos)
    #                     if not text in cell:
    #                         self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(cell + text))

    def find_hazardous_UCA(self, row, column, context_list):
        global list_third_uca
        pos = 0
        for uca in list_third_uca:
            pos += 1
            print_uca = True
            for ctx in uca.context_list:
                for var in context_list:
                    if ctx.id_variable == var.var_id:
                        if ctx.id_value != var.val_id:
                            print_uca = False

            if print_uca:
                col = column + uca.id_uca_type - 1
                cell = self.ui.tablewidget_third_context.item(row, col).text()
                text = " UR-" + str(pos)
                if not text in cell:
                    self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(cell + text))

    def find_hazardous_UCA_Cell(self, row, column, context_list):
        global list_third_uca_cell
        pos = 0
        for uca in list_third_uca_cell:
            pos += 1
            print_uca = True
            for ctx in uca.context_list:
                for var in context_list:
                    if ctx.id_variable == var.var_id:
                        if ctx.id_value != var.val_id:
                            print_uca = False

            if print_uca:
                col = column + uca.id_uca_type - 1
                cell = self.ui.tablewidget_third_context.item(row, col).text()
                text = " UC-" + str(pos)
                if not text in cell:
                    self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(cell + text))

    def find_hazardous_UCA_Safe(self, row, column, context_list):
        global list_third_uca_safe
        pos = 0
        for uca in list_third_uca_safe:
            pos += 1
            print_uca = True
            for ctx in uca.context_list:
                for var in context_list:
                    if ctx.id_variable == var.var_id:
                        if ctx.id_value != var.val_id:
                            print_uca = False

            if print_uca:
                col = column + uca.id_uca_type - 1
                cell = self.ui.tablewidget_third_context.item(row, col).text()
                text = " NH " + str(pos)
                if not text in cell:
                    self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(text + cell))
                    if cell != "":
                        self.ui.tablewidget_third_context.item(row, col).setBackground(
                            QtGui.QColor("#efc6c6"))  # color = "#C6EFCE"

    def load_variables_dynamically(self):
        global list_third_uca_type, list_third_var_comp, list_third_hazard, list_third_haz, list_three_controller, listwidget_third_hazard

        pos = self.ui.combobox_third_controller.currentIndex()
        if pos < 0:
            scrollArea = self.ui.scrollArea_4
            top_widget = QtWidgets.QWidget()
            top_layout = QtWidgets.QHBoxLayout()
            top_widget.setLayout(top_layout)
            scrollArea.setWidget(top_widget)
            return

        list_third_var_comp = DB_Variables.select_variables_with_value_by_project_controller_FOR_UCA(id_project, list_three_controller[pos].id)
        list_third_uca_type = DB_UCA.select_all_saf_uca_type_COMP()

        scrollArea = self.ui.scrollArea_4
        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QHBoxLayout()

        for uca in list_third_uca_type:
            group_box = QtWidgets.QGroupBox()
            group_box.setTitle(uca.name)
            layout = QtWidgets.QHBoxLayout(group_box)

            self.comboBox = QComboBox()
            self.comboBox.setObjectName("combo_" + uca.name)
            self.comboBox.setGeometry(QRect(40, 40, 491, 31))

            for type in uca.list_types:
                self.comboBox.addItem(type.description)

            layout.addWidget(self.comboBox)
            uca.component = self.comboBox
            top_layout.addWidget(group_box)

        for var in list_third_var_comp:
            group_box = QtWidgets.QGroupBox()
            group_box.setTitle(var.var_name)
            layout = QtWidgets.QHBoxLayout(group_box)

            self.comboBox = QComboBox()
            self.comboBox.setObjectName("combo_" + var.var_name)
            self.comboBox.setGeometry(QRect(40, 40, 491, 31))

            self.comboBox.addItem("Any")
            for val in var.values_list:
                self.comboBox.addItem(val.value)

            layout.addWidget(self.comboBox)
            var.component = self.comboBox
            top_layout.addWidget(group_box)

        list_third_hazard = DB_Hazards.select_all_hazards_by_project(id_project)

        group_box = QtWidgets.QGroupBox()
        group_box.setTitle("Hazards")
        layout = QtWidgets.QHBoxLayout(group_box)

        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listwidget_hazard")
        self.listWidget.setGeometry(40, 40, 200, 200)
        self.listWidget.setMinimumWidth(600)

        for haz in list_third_hazard:
            self.listWidget.addItem("H-" + str(haz.id_hazard) + ": " + haz.description)

        layout.addWidget(self.listWidget)
        listwidget_third_hazard = self.listWidget
        top_layout.addWidget(group_box)

        top_widget.setLayout(top_layout)
        scrollArea.setWidget(top_widget)

    def load_uca_third(self):
        global list_third_uca, list_third_uca_cell, list_third_uca_safe, list_third_context, list_third_uca_type, list_third_uca_type_description, \
            list_third_uca_warning, list_three_control_action

        pos = self.ui.combobox_third_control_action.currentIndex()
        self.ui.listwidget_third_uca_rule.clear()
        self.ui.listwidget_third_uca_cell.clear()
        self.ui.listwidget_third_uca_safe.clear()
        self.ui.tablewidget_third_context.clear()
        self.ui.tablewidget_third_context.setRowCount(0)
        self.ui.tablewidget_third_context.setColumnCount(0)
        self.ui.label_third_description_rule.setText("")
        self.ui.label_third_description_cell.setText("")
        self.ui.label_third_description_safe.setText("")

        if pos < 0:
            return


        if len(list_three_control_action) > 0:
            list_third_uca = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos].id, Constant.UCA_RULE, True)
            list_third_uca_cell = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos].id, Constant.UCA_CELL, True)
            list_third_uca_safe = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos].id, Constant.UCA_CELL, False)
            list_third_uca_warning = []

            count = 0
            for uca in list_third_uca:
                is_war = False
                count += 1
                text = "UCA_R-" + str(count) + " --> " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action

                text_context = ""
                for context in uca.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value
                    if (context.variable_name == Constant.VAR_ERR or context.variable_value == Constant.VAL_ERR):
                        is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA_R-" + str(count) + " (variables and values)")

                if text_context == "":
                    text += " in any context."
                else:
                    text += " when " + text_context + ". "

                for haz in uca.hazard_list:
                    text += "[H-" + str(haz.hazard_order) + "]"

                is_war = False
                if len(uca.hazard_list) == 0:
                    is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA_R-" + str(count) + " (hazards)")

                self.ui.listwidget_third_uca_rule.addItem(text)

            # count = 0
            for uca_c in list_third_uca_cell:
                is_war = False
                count += 1
                text = "UCA_C-"  + str(count) + " --> " + uca_c.name_controller + " " + uca_c.description_uca_type + " " + uca_c.name_action

                text_context = ""
                for context in uca_c.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value
                    if (context.variable_name == Constant.VAR_ERR or context.variable_value == Constant.VAL_ERR):
                        is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA-C" + str(count) + " (variables and values)")

                if text_context == "":
                    text += " in any context."
                else:
                    text += " when " + text_context + ". "
                for haz in uca_c.hazard_list:
                    text += "[H-" + str(haz.hazard_order) + "]"

                is_war = False
                if len(uca_c.hazard_list) == 0:
                    is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA-C" + str(count) + " (hazards)")

                self.ui.listwidget_third_uca_cell.addItem(text)

            # count = 0
            for uca_s in list_third_uca_safe:
                is_war = False
                count += 1
                text = "NH-" + str(count) + " - " + uca_s.name_controller + " " + uca_s.description_uca_type + " " + uca_s.name_action

                text_context = ""
                for context in uca_s.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value
                    if (context.variable_name == Constant.VAR_ERR or context.variable_value == Constant.VAL_ERR):
                        is_war = True

                if is_war:
                    list_third_uca_warning.append("NH-" + str(count))

                if text_context == "":
                    text += " in any context."
                else:
                    text += " when " + text_context + ". "
                self.ui.listwidget_third_uca_safe.addItem(text)

            top_widget_uca = QtWidgets.QWidget()
            top_layout_uca = QtWidgets.QVBoxLayout()
            group_box_uca = QtWidgets.QGroupBox()
            group_box_uca.setTitle("Warnings")
            layout_uca = QtWidgets.QVBoxLayout(group_box_uca)
            layout_uca.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            for uca_err in list_third_uca_warning:
                self.label_uca = QLabel()
                self.label_uca.setFont(QFont('Arial', 11))
                self.label_uca.setText(uca_err)
                layout_uca.addWidget(self.label_uca)

            top_layout_uca.addWidget(group_box_uca)
            top_widget_uca.setLayout(top_layout_uca)
            self.ui.scrollarea_third_warnings.setWidget(top_widget_uca)

            list_var_with_values = []
            for var in list_third_var_comp:
                if len(var.values_list) > 0:
                    list_var_with_values.append(var)

            list_third_context = []
            list_third_uca_type_description = DB_UCA.select_all_saf_uca_type()

            if len(list_var_with_values) > 0:
                Safety_tools_new.get_context_a(list_var_with_values, 0, [], list_third_context, True)

            if len(list_third_context) > 0:
                m_columns = len(list_third_context[0].list) + len(list_third_uca_type_description)
                m_rows = len(list_third_context)

                table = self.ui.tablewidget_third_context
                table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                table.setColumnCount(m_columns)  # Set three columns
                table.setRowCount(m_rows)  # and one row

                list_header = []
                for label in list_third_context[0].list:
                    list_header.append(label.var_name)

                for uca in list_third_uca_type:
                    for type in uca.list_types:
                        list_header.append(type.description)

                table.setHorizontalHeaderLabels(list_header)  # Set the table headers

                for r in range(len(list_third_context)):
                    row = list_third_context[r]
                    for c in range(m_columns):
                        if c < len(row.list):
                            col = row.list[c]
                            table.setItem(r, c, QTableWidgetItem(col.val_value))
                        else:
                            table.setItem(r, c, QTableWidgetItem(""))

                for r2 in range(len(list_third_context)):
                    row2 = list_third_context[r2]
                    self.find_hazardous_UCA(r2, len(row2.list), row2.list)
                    self.find_hazardous_UCA_Cell(r2, len(row2.list), row2.list)
                    self.find_hazardous_UCA_Safe(r2, len(row2.list), row2.list)

                table.resizeColumnsToContents()

    def on_button_button_third_save_uca_clicked(self):
        global listwidget_third_hazard, list_third_var_comp, list_third_uca, list_third_uca_type, list_third_hazard, list_three_controller, list_three_control_action

        hazard_list = []
        for haz in listwidget_third_hazard.selectedIndexes():
            hazard_list.append(list_third_hazard[haz.row()])

        context_list = self.get_context_selected()
        uca_type_id = self.get_context_selected_uca_type()

        pos_c = self.ui.combobox_third_controller.currentIndex()
        pos_a = self.ui.combobox_third_control_action.currentIndex()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        elif pos_a == -1:
            showdialog("No control action selected", "Select the control action")
            return
        # elif len(context_list) == 0:
        #     showdialog("No value selected", "Select at least one variable value")
        #     return
        elif listwidget_third_hazard == None:
            showdialog("No hazard selected", "Select at least one Hazard")
            return
        elif len(hazard_list) == 0:
            showdialog("No hazard selected", "Select at least one Hazard")
            return

        id_result = DB_UCA.insert(list_three_controller[pos_c].id, uca_type_id, list_three_control_action[pos_a].id,
                                  context_list, hazard_list, "rule", True)
        if id_result > 0:
            showdialog("Success", "UCA created!")
            self.load_uca_third()
        else:
            showdialog("Error", "Cannot save UCA now, try again!")

    def get_context_selected(self):
        global list_third_var_comp

        result_list = []

        for var in list_third_var_comp:
            values = []
            if var.component.currentIndex() != 0:
                values.append(var.values_list[var.component.currentIndex() - 1])
                result_list.append(Var_Values_Aux(var.var_name, var.variable, values))

        return result_list

    def get_context_selected_uca_type(self):
        global list_third_uca_type

        for type in list_third_uca_type:
            return type.list_types[type.component.currentIndex()].id
        return 0

    def on_button_button_third_delete_uca_rule_clicked(self):
        global list_third_uca
        pos = self.ui.listwidget_third_uca_rule.currentRow()

        if pos == -1:
            showdialog("No UCA_R selected", "Select one UCA_R to be deleted")
            return

        uca = list_third_uca[pos]
        list_req = DB_Loss_Scenario_Req.select_id_requirement_by_uca(uca.id)
        text = "Are you sure that you want delete UCA_R-" + str(pos + 1) + "?"
        if len(list_req) > 0:
            text += "\nIf you delete this UCA_R, you will lost " + str(len(list_req)) + " recommendations."

        text += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Delete UCA_R?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_UCA.delete(uca.id)
            self.load_uca_third()

    def on_button_button_third_delete_uca_cell_clicked(self):
        global list_third_uca_cell
        pos = self.ui.listwidget_third_uca_cell.currentRow()

        if pos == -1:
            showdialog("No UCA_C selected", "Select one UCA_C to be deleted")
            return

        uca = list_third_uca_cell[pos]
        list_req = DB_Loss_Scenario_Req.select_id_requirement_by_uca(uca.id)
        text = "Are you sure that you want delete UCA_C-" + str(pos + 1) + "?"
        if len(list_req) > 0:
            text += "\nIf you delete this UCA_R, you will lost " + str(len(list_req)) + " recommendations."

        text += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Delete UCA_C?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_UCA.delete(uca.id)
            self.load_uca_third()

    def on_button_button_third_delete_uca_safe_clicked(self):
        global list_third_uca_safe
        pos = self.ui.listwidget_third_uca_safe.currentRow()

        if pos == -1:
            showdialog("No NH selected", "Select one NH to be deleted")
            return

        uca = list_third_uca_safe[pos]
        text = "Are you sure that you want delete NH-" + str(pos + 1) + "?"
        text += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Delete NH?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_UCA.delete(uca.id)
            self.load_uca_third()

    def cell_was_clicked(self, row, column):
        global list_third_context, list_three_controller, list_third_uca_type, list_third_hazard, list_third_uca_type_description

        if len(list_third_context) == 0:
            return

        if column < len(list_third_context[row].list):
            return

        text = self.ui.tablewidget_third_context.item(row, column).text()

        if text == "":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)

            msgBox.setWindowTitle("Rule creation")
            msgBox.setText("Do you want to create a rule for this cell?")

            msgBox.addButton(QPushButton("Hazardous cell rule"), QMessageBox.YesRole)
            msgBox.addButton(QPushButton("NOT hazardous cell rule"), QMessageBox.NoRole)
            msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

            returnValue = msgBox.exec()
            if returnValue == 0:
                context_list = list_third_context[row]
                uca_type = list_third_uca_type[0].list_types[column - len(context_list.list)]

                pos_c = self.ui.combobox_third_controller.currentIndex()
                pos_a = self.ui.combobox_third_control_action.currentIndex()

                if pos_c == -1:
                    showdialog("No controller selected", "Select the controller")
                    return
                elif pos_a == -1:
                    showdialog("No control action selected", "Select the control action")
                    return
                elif listwidget_third_hazard == None:
                    showdialog("No hazard selected", "Select at least one Hazard")
                    return

                msgBox2 = OpDialog()
                result = msgBox2.exec_()

                if result == 1:
                    hazard_list = []
                    for haz in msgBox2.listWidget.selectedIndexes():
                        hazard_list.append(list_third_hazard[haz.row()])

                    if len(hazard_list) == 0:
                        showdialog("No hazard selected", "Select at least one Hazard")
                        return

                    try:
                        id_result = DB_UCA.insert_from_cell(list_three_controller[pos_c].id, uca_type.id,
                                                            list_three_control_action[pos_a].id, context_list.list,
                                                            hazard_list, "cell", True)
                    except NameError as e:
                        print(e)
                        id_result = 0

                    if id_result > 0:
                        # showdialog("Success", "Rule for Cell created!")
                        self.ui.tablewidget_third_context.clearSelection()
                        self.load_uca_third()
                    else:
                        showdialog("Error", "Cannot save UCA now, try again!")
            elif returnValue == 1:
                context_list = list_third_context[row]
                uca_type = list_third_uca_type[0].list_types[column - len(context_list.list)]

                pos_c = self.ui.combobox_third_controller.currentIndex()
                pos_a = self.ui.combobox_third_control_action.currentIndex()

                if pos_c == -1:
                    showdialog("No controller selected", "Select the controller")
                    return
                elif pos_a == -1:
                    showdialog("No control action selected", "Select the control action")
                    return
                elif listwidget_third_hazard == None:
                    showdialog("No hazard selected", "Select at least one Hazard")
                    return

                try:
                    id_result = DB_UCA.insert_from_cell(list_three_controller[pos_c].id, uca_type.id,
                                                        list_three_control_action[pos_a].id,
                                                        context_list.list, [], "cell", False)
                except NameError as e:
                    print(e)
                    id_result = 0

                if id_result > 0:
                    # showdialog("Success", "Cell marked as Not Hazardous!")
                    self.ui.tablewidget_third_context.clearSelection()
                    self.load_uca_third()
                else:
                    showdialog("Error", "Cannot save UCA now, try again!")
        elif " NH " in text:
            context_list = list_third_context[row]
            col = column - len(context_list.list)
            uca_aux = list_third_uca_type_description[col]

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Do you want to remove the Not Hazardous marking from cell at row " + str(
                row + 1) + " and column " + uca_aux.description + "?")
            msgBox.setWindowTitle("Delete Not Hazardous Cell")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            returnValue = msgBox.exec()

            if returnValue == QMessageBox.Yes:
                uca_id_delete = self.find_uca_safe(context_list, uca_aux.id)
                if uca_id_delete > 0:
                    DB_UCA.delete(uca_id_delete)
                    self.ui.tablewidget_third_context.clearSelection()
                    self.load_uca_third()
                else:
                    showdialog("Error", "Error to process the action to delete, try again.")

    def find_uca_safe(self, context_list, uca_type_id):
        global list_third_uca_safe

        for uca in list_third_uca_safe:
            if uca.id_uca_type == uca_type_id:
                found_uca = True
                for ctx in uca.context_list:
                    for var in context_list.list:
                        if ctx.id_variable == var.var_id:
                            if ctx.id_value != var.val_id:
                                found_uca = False
                if found_uca:
                    return uca.id

        return 0

    def on_listwidget_uca_rule_clicked(self):
        global list_third_uca

        pos = self.ui.listwidget_third_uca_rule.currentRow()

        if len(list_third_uca) == 0 or pos < 0:
            return

        if list_third_uca[pos].description == None:
            self.ui.label_third_description_rule.setText("")
        else:
            self.ui.label_third_description_rule.setText(list_third_uca[pos].description)

    def on_listwidget_uca_cell_clicked(self):
        global list_third_uca_cell
        pos = self.ui.listwidget_third_uca_cell.currentRow()

        if len(list_third_uca_cell) == 0 or pos < 0:
            return

        if list_third_uca_cell[pos].description == None:
            self.ui.label_third_description_cell.setText("")
        else:
            self.ui.label_third_description_cell.setText(list_third_uca_cell[pos].description)

    def on_listwidget_uca_safe_clicked(self):
        global list_third_uca_safe

        pos = self.ui.listwidget_third_uca_safe.currentRow()

        if len(list_third_uca_safe) == 0 or pos < 0:
            return

        if list_third_uca_safe[pos].description == None:
            self.ui.label_third_description_safe.setText("")
        else:
            self.ui.label_third_description_safe.setText(list_third_uca_safe[pos].description)

    def on_button_third_update_description_uca_rule(self):
        global list_third_uca, list_three_control_action

        pos = self.ui.listwidget_third_uca_rule.currentRow()

        if len(list_third_uca) == 0 or pos < 0:
            return

        result = self.update_description_uca(list_third_uca[pos])

        if result < 0:
            return

        pos_act = self.ui.combobox_third_control_action.currentIndex()
        if len(list_three_control_action) <= 0:
            return

        list_third_uca = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos_act].id, Constant.UCA_RULE, True)
        self.on_listwidget_uca_rule_clicked()

    def on_button_third_update_description_uca_cell(self):
        global list_third_uca_cell, list_three_control_action
        pos = self.ui.listwidget_third_uca_cell.currentRow()

        if len(list_third_uca_cell) == 0 or pos < 0:
            return

        result = self.update_description_uca(list_third_uca_cell[pos])

        if result < 0:
            return

        pos_act = self.ui.combobox_third_control_action.currentIndex()
        if len(list_three_control_action) <= 0:
            return

        list_third_uca_cell = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos_act].id, Constant.UCA_CELL, True)
        self.on_listwidget_uca_cell_clicked()

    def on_button_third_update_description_uca_safe(self):
        global list_third_uca_safe, list_three_control_action

        pos = self.ui.listwidget_third_uca_safe.currentRow()

        if len(list_third_uca_safe) == 0 or pos < 0:
            return

        result = self.update_description_uca(list_third_uca_safe[pos])

        if result < 0:
            return

        pos_act = self.ui.combobox_third_control_action.currentIndex()
        if len(list_three_control_action) <= 0:
            return

        list_third_uca_safe = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos_act].id, Constant.UCA_CELL, False)
        self.on_listwidget_uca_safe_clicked()

    def update_description_uca(self, obj_uca):
        global third_uca_description

        third_uca_description = ""
        if obj_uca.description != None:
            third_uca_description = obj_uca.description

        cf = UcaDescriptionDialog()
        result = cf.exec_()

        if result == 1:
            # description = cf.description.text()
            description = cf.description.toPlainText()
            return DB_UCA.update(obj_uca.id, description)

        return -1

    # ----- Functions STPA 3 Step -----

    # ----- Functions STPA 2 Step -----
    def on_button_delete_controller_connection_clicked(self):
        global list_connection_controller, list_links_controller
        pos = self.ui.listwidget_controller_connection.currentRow()
        item = self.ui.listwidget_controller_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Controller?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_controller[pos])
            self.load_controller_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_exts_connection_clicked(self):
        global list_connection_exts, list_links_exts
        pos = self.ui.listwidget_exts_connection.currentRow()
        item = self.ui.listwidget_exts_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link External System?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_exts[pos])
            self.load_exts_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_actuator_connection_clicked(self):
        global list_connection_actuator, list_links_actuator
        pos = self.ui.listwidget_actuator_connection.currentRow()
        item = self.ui.listwidget_actuator_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_actuator[pos])
            self.load_actuator_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_sensor_connection_clicked(self):
        global list_connection_sensor, list_links_sensor
        pos = self.ui.listwidget_sensor_connection.currentRow()
        item = self.ui.listwidget_sensor_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Sensor?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_sensor[pos])
            self.load_sensor_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_controlled_process_connection_clicked(self):
        global list_connection_controlled_process, list_links_controlled_process
        pos = self.ui.listwidget_controlled_process_connection.currentRow()
        item = self.ui.listwidget_controlled_process_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Controlled Process?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_controlled_process[pos])
            self.load_controlled_process_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_listwidget_controller_connection_clicked(self):
        self.ui.button_delete_controller_connection.setEnabled(True)

    def on_listwidget_exts_connection_clicked(self):
        self.ui.button_delete_exts_connection.setEnabled(True)

    def on_listwidget_actuator_connection_clicked(self):
        self.ui.button_delete_actuator_connection.setEnabled(True)

    def on_listwidget_sensor_connection_clicked(self):
        self.ui.button_delete_sensor_connection.setEnabled(True)

    def on_listwidget_controlled_process_connection_clicked(self):
        self.ui.button_delete_controlled_process_connection.setEnabled(True)

    def on_button_add_controller_connection_clicked(self):
        global list_component_controller, list_connection_controller, list_links_controller

        index = self.ui.combobox_controller_connection.currentIndex()
        pos = self.ui.listwidget_controllers.currentRow()

        for link in list_links_controller:
            if link.id_component_src == list_component_controller[pos].id and link.id_component_dst == \
                    list_connection_controller[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_controller[pos].id, list_connection_controller[index].id)
        self.load_controller_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_exts_connection_clicked(self):
        global list_component_exts, list_connection_exts, list_links_exts

        index = self.ui.combobox_exts_connection.currentIndex()
        pos = self.ui.listwidget_exts.currentRow()

        for link in list_links_exts:
            if link.id_component_src == list_component_exts[pos].id and link.id_component_dst == list_connection_exts[
                index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_exts[pos].id, list_connection_exts[index].id)
        self.load_exts_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_actuator_connection_clicked(self):
        global list_component_actuator, list_connection_actuator, list_links_actuator

        index = self.ui.combobox_actuator_connection.currentIndex()
        pos = self.ui.listwidget_actuator.currentRow()

        for link in list_links_actuator:
            if link.id_component_src == list_component_actuator[pos].id and link.id_component_dst == \
                    list_connection_actuator[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_actuator[pos].id, list_connection_actuator[index].id)
        self.load_actuator_connections()

        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_sensor_connection_clicked(self):
        global list_component_sensor, list_connection_sensor, list_links_sensor

        index = self.ui.combobox_sensor_connection.currentIndex()
        pos = self.ui.listwidget_sensor.currentRow()

        for link in list_links_sensor:
            if link.id_component_src == list_component_sensor[pos].id and link.id_component_dst == \
                    list_connection_sensor[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_sensor[pos].id, list_connection_sensor[index].id)
        self.load_sensor_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_controlled_process_connection_clicked(self):
        global list_component_controlled_process, list_connection_controlled_process, list_links_controlled_process

        index = self.ui.combobox_controlled_process_connection.currentIndex()

        for link in list_links_controlled_process:
            if link.id_component_src == list_component_controlled_process[0].id and link.id_component_dst == \
                    list_connection_controlled_process[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_controlled_process[0].id,
                                   list_connection_controlled_process[index].id)
        self.load_controlled_process_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def load_component_controller(self):
        global list_component_controller, id_project
        list_component_controller = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CONTROLLER, id_project)

        self.ui.listwidget_controllers.clear()
        self.ui.combobox_second_controller.clear()
        self.ui.checkbox_controller_ext_of_analysis.setChecked(False)
        self.ui.checkbox_controller_human.setChecked(False)

        for pos in range(len(list_component_controller)):
            self.ui.listwidget_controllers.addItem(list_component_controller[pos].name)
            self.ui.combobox_second_controller.addItem(list_component_controller[pos].name)

        if len(list_component_controller) == 0:
            self.clean_control_action()
            self.clean_variables_values()
        else:
            self.selection_change_controller_connection()

        self.load_responsibilities()
        self.clear_new_responsibility()

    def disable_edit_controller(self):
        self.ui.button_add_controller.setEnabled(True)
        self.ui.button_update_controller.setEnabled(False)
        self.ui.button_delete_controller.setEnabled(False)
        self.ui.button_cancel_controller.setEnabled(False)
        self.ui.checkbox_controller_ext_of_analysis.setChecked(False)
        self.ui.checkbox_controller_human.setChecked(False)
        self.ui.lineedit_name_controller.setText("")

    def disable_new_controller(self):
        self.ui.button_add_controller.setEnabled(False)
        self.ui.button_update_controller.setEnabled(True)
        self.ui.button_delete_controller.setEnabled(True)
        self.ui.button_cancel_controller.setEnabled(True)

    def on_button_add_controller_clicked(self):
        global id_project, list_component_controller

        description = self.ui.lineedit_name_controller.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            if self.ui.checkbox_controller_ext_of_analysis.isChecked():
                is_ext_anl = 1
            else:
                is_ext_anl = 0

            if self.ui.checkbox_controller_human.isChecked():
                is_human = 1
            else:
                is_human = 0

            comp = Component(0, Constant.DB_ID_CONTROLLER, id_project, description, current_date, current_date, 0, is_ext_anl, is_human)
            DB_Components.insert_controller(comp)

            if self.ui.listwidget_sensor_connection.isEnabled():
                self.load_sensor_connections()

            if self.ui.listwidget_exts_connection.isEnabled():
                self.load_exts_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

            self.load_component_controller()
            self.ui.lineedit_name_controller.setText("")

    def on_button_update_controller_clicked(self):
        global id_project, list_component_controller

        name = self.ui.lineedit_name_controller.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_controllers.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_controller[pos]
            comp.name = name
            comp.edited_date = current_date

            if self.ui.checkbox_controller_ext_of_analysis.isChecked():
                comp.is_external_component = 1
            else:
                comp.is_external_component = 0

            if self.ui.checkbox_controller_human.isChecked():
                comp.is_human = 1
            else:
                comp.is_human = 0

            DB_Components.update_component_controller(comp)

            self.disable_edit_controller()
            self.load_component_controller()
            self.disable_edit_controller()
            self.disable_controller_connections()

            if self.ui.listwidget_sensor_connection.isEnabled():
                self.load_sensor_connections()

            if self.ui.listwidget_exts_connection.isEnabled():
                self.load_exts_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

    def on_button_delete_controller_clicked(self):
        global list_component_controller
        pos = self.ui.listwidget_controllers.currentRow()
        comp = list_component_controller[pos]

        delete_report = DB_Components.delete_report(comp.id)
        message = "Are you sure that you want delete the controller: " + comp.name + "?"

        if len(delete_report) > 0:
            message += "\nThis controller is related to: "
            for text in delete_report:
                message += "\n" + text

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle("Delete Controller?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete_controller(comp)
            self.load_component_controller()
            self.ui.lineedit_name_controller.setText("")
            self.disable_edit_controller()
            self.disable_controller_connections()

            if self.ui.listwidget_sensor_connection.isEnabled():
                self.load_sensor_connections()

            if self.ui.listwidget_exts_connection.isEnabled():
                self.load_exts_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

            self.load_controller_connections()

    def on_button_cancel_controller_clicked(self):
        self.disable_edit_controller()
        self.ui.lineedit_name_controller.setText("")
        self.disable_controller_connections()
        # self.disable_controller_actions_variables()
        self.ui.listwidget_controllers.clearSelection()
        self.ui.listwidget_controllers.selectionModel().clear()
        self.ui.checkbox_controller_ext_of_analysis.setChecked(False)
        self.ui.checkbox_controller_human.setChecked(False)

    def load_controller_connections(self):
        global list_component_controller, list_connection_controller, list_links_controller, id_project
        pos = self.ui.listwidget_controllers.currentRow()

        if pos < 0:
            return

        list_links_controller = DB_Components_Links.select_component_links_by_project_and_component(
            list_component_controller[pos].id, True)
        self.ui.listwidget_controller_connection.clear()
        self.disable_edit_controller_connections()

        for link in list_links_controller:
            self.ui.listwidget_controller_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_controller_")
        list_connection_controller = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                             list_component_controller[
                                                                                                 pos].id,
                                                                                             list_of_things)
        self.ui.combobox_controller_connection.clear()
        for conn in list_connection_controller:
            self.ui.combobox_controller_connection.addItem(conn.name)

    def load_exts_connections(self):
        global list_component_exts, list_connection_exts, list_links_exts
        pos = self.ui.listwidget_exts.currentRow()

        if pos < 0:
            return

        list_links_exts = DB_Components_Links.select_component_links_by_project_and_component(
            list_component_exts[pos].id, True)
        self.ui.listwidget_exts_connection.clear()
        self.disable_edit_exts_connections()

        for link in list_links_exts:
            self.ui.listwidget_exts_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK,
                                                                                "Link_External-information_")
        list_connection_exts = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                       list_component_exts[pos].id,
                                                                                       list_of_things)
        self.ui.combobox_exts_connection.clear()
        for conn in list_connection_exts:
            self.ui.combobox_exts_connection.addItem(conn.name)

    def load_actuator_connections(self):
        global list_component_actuator, list_connection_actuator, list_links_actuator

        pos = self.ui.listwidget_actuator.currentRow()

        if pos < 0:
            return

        list_links_actuator = DB_Components_Links.select_component_links_by_project_and_component(
            list_component_actuator[pos].id, True)
        self.ui.listwidget_actuator_connection.clear()
        self.disable_edit_actuator_connections()

        for link in list_links_actuator:
            self.ui.listwidget_actuator_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_actuator_")
        list_connection_actuator = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                           list_component_actuator[
                                                                                               pos].id, list_of_things)
        self.ui.combobox_actuator_connection.clear()
        for conn in list_connection_actuator:
            self.ui.combobox_actuator_connection.addItem(conn.name)

    def load_sensor_connections(self):
        global list_component_sensor, list_connection_sensor, list_links_sensor
        pos = self.ui.listwidget_sensor.currentRow()

        if pos < 0:
            return

        list_links_sensor = DB_Components_Links.select_component_links_by_project_and_component(
            list_component_sensor[pos].id, True)
        self.ui.listwidget_sensor_connection.clear()
        self.disable_edit_sensor_connections()

        for link in list_links_sensor:
            self.ui.listwidget_sensor_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_sensor_")
        list_connection_sensor = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                         list_component_sensor[pos].id,
                                                                                         list_of_things)
        self.ui.combobox_sensor_connection.clear()
        for conn in list_connection_sensor:
            self.ui.combobox_sensor_connection.addItem(conn.name)

    def load_controlled_process_connections(self):
        global list_component_controlled_process, list_connection_controlled_process, list_links_controlled_process

        if len(list_component_controlled_process) == 0:
            return

        list_links_controlled_process = DB_Components_Links.select_component_links_by_project_and_component(list_component_controlled_process[0].id, True)
        self.ui.listwidget_controlled_process_connection.clear()
        self.disable_edit_controlled_process_connections()

        for link in list_links_controlled_process:
            self.ui.listwidget_controlled_process_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_CP_")
        list_connection_controlled_process = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                                     list_component_controlled_process[
                                                                                                         0].id,
                                                                                                     list_of_things)
        self.ui.combobox_controlled_process_connection.clear()
        for conn in list_connection_controlled_process:
            self.ui.combobox_controlled_process_connection.addItem(conn.name)

    def disable_edit_controller_connections(self):
        self.ui.combobox_controller_connection.setEnabled(True)
        self.ui.button_add_controller_connection.setEnabled(True)
        self.ui.button_delete_controller_connection.setEnabled(False)
        self.ui.listwidget_controller_connection.setEnabled(True)

    def disable_edit_exts_connections(self):
        self.ui.combobox_exts_connection.setEnabled(True)
        self.ui.button_add_exts_connection.setEnabled(True)
        self.ui.button_delete_exts_connection.setEnabled(False)
        self.ui.listwidget_exts_connection.setEnabled(True)

    def disable_edit_actuator_connections(self):
        self.ui.combobox_actuator_connection.setEnabled(True)
        self.ui.button_add_actuator_connection.setEnabled(True)
        self.ui.button_delete_actuator_connection.setEnabled(False)
        self.ui.listwidget_actuator_connection.setEnabled(True)

    def disable_edit_sensor_connections(self):
        self.ui.combobox_sensor_connection.setEnabled(True)
        self.ui.button_add_sensor_connection.setEnabled(True)
        self.ui.button_delete_sensor_connection.setEnabled(False)
        self.ui.listwidget_sensor_connection.setEnabled(True)

    def disable_edit_controlled_process_connections(self):
        print()
        self.ui.combobox_controlled_process_connection.setEnabled(True)
        self.ui.button_add_controlled_process_connection.setEnabled(True)
        self.ui.button_delete_controlled_process_connection.setEnabled(False)
        self.ui.listwidget_controlled_process_connection.setEnabled(True)

    def on_listwidget_controllers_clicked(self):
        global list_component_controller, id_project
        item = self.ui.listwidget_controllers.currentItem()
        pos = self.ui.listwidget_controllers.currentRow()

        if pos >= 0:
            item.setSelected(True)
            self.disable_new_controller()
            self.ui.lineedit_name_controller.setText(list_component_controller[pos].name)

            if list_component_controller[pos].is_external_component == 1:
                self.ui.checkbox_controller_ext_of_analysis.setChecked(True)
            else:
                self.ui.checkbox_controller_ext_of_analysis.setChecked(False)

            if list_component_controller[pos].is_human == 1:
                self.ui.checkbox_controller_human.setChecked(True)
            else:
                self.ui.checkbox_controller_human.setChecked(False)

            self.load_controller_connections()

    def load_second_responsibility_ssc(self):
        global list_second_responsibility_ssc, id_project
        list_second_responsibility_ssc = []
        self.ui.list_second_safety_constraints.clear()

        list_second_responsibility_ssc = DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project)
        for pos in range(len(list_second_responsibility_ssc)):
            text = ""
            for haz in list_second_responsibility_ssc[pos].list_of_hazards:
                text += "[H-" + str(haz.id_haz_screen) + "] "

            self.ui.list_second_safety_constraints.addItem("SSC-" + str(list_second_responsibility_ssc[pos].id_safety_constraint) + ": " + list_second_responsibility_ssc[pos].description + " " + text)
        self.clear_new_responsibility()

    def on_button_saf_new_responsibility_clicked(self):
        global id_project, list_second_responsibility, list_second_responsibility_ssc, list_component_controller

        description = self.ui.lineedit_second_responsibility.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
            return

        pos_c = self.ui.combobox_second_controller.currentIndex()
        if pos_c < 0:
            return

        responsibility = Responsibility(0, description, id_project, len(list_second_responsibility) + 1, list_component_controller[pos_c].id, [])

        selected_ssc = []
        for item in self.ui.list_second_safety_constraints.selectedItems():
            ssc_id = list_second_responsibility_ssc[self.ui.list_second_safety_constraints.row(item)].id
            selected_ssc.append(Responsibility_ssc(0, 0, ssc_id))

        responsibility.list_of_ssc = selected_ssc
        DB_Responsibility.insert_to_responsibility(responsibility)

        self.clear_new_responsibility()
        self.load_responsibilities()

    def load_responsibilities(self):
        global id_project, list_second_responsibility, list_component_controller
        # pos = self.ui.list_second_responsibility.currentRow()
        list_second_responsibility = []
        self.ui.list_second_responsibility.clear()

        pos_c = self.ui.combobox_second_controller.currentIndex()
        if pos_c < 0:
            return

        list_second_responsibility = DB_Responsibility.select_all_responsibilities_by_controller(list_component_controller[pos_c].id)

        for pos in range(len(list_second_responsibility)):

            text = ""
            for ssc in list_second_responsibility[pos].list_of_ssc:
                text += "[SSC-" + str(ssc.id_constraint_screen) + "] "

            self.ui.list_second_responsibility.addItem("R-" + str(list_second_responsibility[pos].id_screen) + ": " + str(list_second_responsibility[pos].description + ". " + text))

    def on_list_responsibility_clicked(self):
        global list_second_responsibility, list_second_responsibility_ssc
        pos_resp = self.ui.list_second_responsibility.currentRow()

        if pos_resp < 0:
            return

        self.ui.button_saf_new_responsibility.setEnabled(False)
        self.ui.button_saf_update_responsibility.setEnabled(True)
        self.ui.button_saf_delete_responsibility.setEnabled(True)
        self.ui.button_saf_cancel_responsibility.setEnabled(True)

        self.ui.lineedit_second_responsibility.setText(list_second_responsibility[pos_resp].description)
        self.ui.list_second_safety_constraints.clear()

        for pos in range(len(list_second_responsibility_ssc)):
            text = ""
            for haz in list_second_responsibility_ssc[pos].list_of_hazards:
                text += "[H-" + str(haz.id_haz_screen) + "] "

            item = QtWidgets.QListWidgetItem("SSC-" + str(list_second_responsibility_ssc[pos].id_safety_constraint) + ": " + list_second_responsibility_ssc[pos].description + " " + text)
            self.ui.list_second_safety_constraints.addItem(item)

            for ssc in list_second_responsibility[pos_resp].list_of_ssc:
                if ssc.id_constraint == list_second_responsibility_ssc[pos].id:
                    self.ui.list_second_safety_constraints.item(pos).setSelected(True)

    def clear_new_responsibility(self):
        self.ui.lineedit_second_responsibility.setText("")
        self.ui.list_second_safety_constraints.clearSelection()
        self.ui.list_second_safety_constraints.selectionModel().clear()
        self.ui.list_second_responsibility.clearSelection()
        self.ui.list_second_responsibility.selectionModel().clear()

        self.ui.button_saf_new_responsibility.setEnabled(True)
        self.ui.button_saf_update_responsibility.setEnabled(False)
        self.ui.button_saf_delete_responsibility.setEnabled(False)
        self.ui.button_saf_cancel_responsibility.setEnabled(False)

    def on_button_saf_cancel_responsibility_clicked(self):
        self.ui.button_saf_new_responsibility.setEnabled(True)
        self.ui.button_saf_update_responsibility.setEnabled(False)
        self.ui.button_saf_delete_responsibility.setEnabled(False)
        self.ui.button_saf_cancel_responsibility.setEnabled(False)

        self.ui.lineedit_second_responsibility.setText("")
        self.ui.list_second_responsibility.clearSelection()
        self.ui.list_second_responsibility.selectionModel().clear()
        self.ui.list_second_safety_constraints.clearSelection()
        self.ui.list_second_safety_constraints.selectionModel().clear()

        self.load_responsibilities()

    def on_button_saf_update_reponsability_clicked(self):
        global id_project, list_second_responsbility

        description = self.ui.lineedit_second_responsibility.text()
        if len(description) <= 0:
            showdialog("Error on save", "Fill the field with description")
        # elif len(self.ui.list_second_safety_constraints.selectedItems()) == 0:
        #     showdialog("Error on save", "Select at least one Hazard")
        else:
            pos = self.ui.list_second_responsibility.currentRow()

            resp = list_second_responsibility[pos]
            resp.description = description

            selected_ssc = []
            for item in self.ui.list_second_safety_constraints.selectedItems():
                ssc_id = list_second_responsibility_ssc[self.ui.list_second_safety_constraints.row(item)].id
                selected_ssc.append(Responsibility_ssc(0, 0, ssc_id))

            resp.list_of_ssc = selected_ssc
            DB_Responsibility.update_responsibility(resp)

            self.clear_new_responsibility()
            self.load_responsibilities()
            self.clear_new_responsibility()

    def on_button_saf_delete_reponsability_clicked(self):
        global id_project, list_second_responsibility

        pos = self.ui.list_second_responsibility.currentRow()
        if pos < 0:
            return

        resp = list_second_responsibility[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete the responsibility: " + str(resp.description) + "?")
        msgBox.setWindowTitle("Delete Responsibility")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Responsibility.delete_responsibility(resp)
            self.clear_new_responsibility()
            self.load_responsibilities()
            self.clear_new_responsibility()

    def disable_new_control_action(self):
        self.ui.button_add_control_action.setEnabled(False)
        self.ui.button_update_control_action.setEnabled(True)
        self.ui.button_delete_control_action.setEnabled(True)
        self.ui.button_cancel_control_action.setEnabled(True)

    def disable_edit_control_action(self):
        self.ui.lineedit_name_control_action.setText("")
        self.ui.button_add_control_action.setEnabled(True)
        self.ui.button_update_control_action.setEnabled(False)
        self.ui.button_delete_control_action.setEnabled(False)
        self.ui.button_cancel_control_action.setEnabled(False)
        self.ui.lineedit_name_control_action.setEnabled(True)
        self.ui.listwidget_control_actions.setEnabled(True)
        self.ui.listwidget_second_links_act.setEnabled(True)

    def disable_new_controller_variable(self):
        self.ui.button_add_controller_variable.setEnabled(False)
        self.ui.button_update_controller_variable.setEnabled(True)
        self.ui.button_delete_controller_variable.setEnabled(True)
        self.ui.button_cancel_controller_variable.setEnabled(True)
        self.ui.lineedit_name_control_action.setEnabled(True)
        self.ui.listwidget_control_actions.setEnabled(True)
        self.ui.listwidget_second_links_var.setEnabled(True)

    def disable_edit_controller_variable(self):
        self.ui.lineedit_name_controller_variable.setText("")
        self.ui.button_add_controller_variable.setEnabled(True)
        self.ui.button_update_controller_variable.setEnabled(False)
        self.ui.button_delete_controller_variable.setEnabled(False)
        self.ui.button_cancel_controller_variable.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setEnabled(True)
        self.ui.listwidget_controller_variable.setEnabled(True)
        self.ui.listwidget_second_links_var.setEnabled(True)

    def clean_control_action(self):
        self.ui.button_add_control_action.setEnabled(False)
        self.ui.button_update_control_action.setEnabled(False)
        self.ui.button_delete_control_action.setEnabled(False)
        self.ui.button_cancel_control_action.setEnabled(False)
        self.ui.listwidget_control_actions.clear()
        self.ui.listwidget_control_actions.setEnabled(False)
        self.ui.lineedit_name_control_action.setEnabled(False)
        self.ui.lineedit_name_control_action.setText("")

    def selection_change_controller_connection(self):
        self.load_controller_control_actions()
        self.load_component_controller_variables()
        self.disable_edit_controller_variable()
        self.disable_edit_control_action()
        self.load_responsibilities()

    def on_button_add_control_action_clicked(self):
        global id_project, list_control_actions, list_component_controller, list_links_actions_controller

        description = self.ui.lineedit_name_control_action.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
            return

        pos_c = self.ui.combobox_second_controller.currentIndex()
        if pos_c < 0:
            return

        list_link_to_verify = []
        for item in self.ui.listwidget_second_links_act.selectedItems():
            pos = self.ui.listwidget_second_links_act.row(item)
            list_link_to_verify.append(list_links_actions_controller[pos])

        list_feedback = DB_Components_Links.select_all_control_actions_in_link(list_link_to_verify);
        if len(list_feedback) > 0:
            if len(list_feedback) == 1:
                msg = "There is a conflict that must be solved before do this action: \n"
            else:
                msg = "There some conflicts that must be solved before do this action: \n"

            for m_a in list_feedback:
                msg += m_a + "\n"

            showdialog("Action not allowed!", msg)
            return

        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK)

        act = Action_Component(0, list_component_controller[pos_c].id, description, current_date, current_date,
                               id_project)
        id_last_var = DB_Actions_Components.insert_to_table(act)

        if id_last_var > 0:
            for item in self.ui.listwidget_second_links_act.selectedItems():
                pos = self.ui.listwidget_second_links_act.row(item)
                link_id = list_links_actions_controller[pos].id
                DB_Components_Links.insert_link_act(id_last_var, link_id)

        self.load_controller_control_actions()
        self.ui.lineedit_name_control_action.setText("")

    def on_button_update_control_action_clicked(self):
        global id_project, list_control_actions, list_links_actions_controller

        description = self.ui.lineedit_name_control_action.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
            return

        list_link_to_verify = []
        for item in self.ui.listwidget_second_links_act.selectedItems():
            pos = self.ui.listwidget_second_links_act.row(item)
            list_link_to_verify.append(list_links_actions_controller[pos])

        list_feedback = DB_Components_Links.select_all_control_actions_in_link(list_link_to_verify);
        if len(list_feedback) > 0:
            if len(list_feedback) == 1:
                msg = "There is a conflict that must be solved before do this action: \n"
            else:
                msg = "There some conflicts that must be solved before do this action: \n"

            for m_a in list_feedback:
                msg += "- " + m_a + "\n"

            showdialog("Action not allowed!", msg)
            return

        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK)
        pos = self.ui.listwidget_control_actions.currentRow()

        act = list_control_actions[pos]
        act.name = description
        act.edite_date = current_date
        DB_Actions_Components.update(act)

        index_list = self.ui.listwidget_second_links_act.selectedItems()
        DB_Components_Links.delete_link_act(act.id)

        for item in index_list:
            pos = self.ui.listwidget_second_links_act.row(item)
            link_id = list_links_actions_controller[pos].id
            DB_Components_Links.insert_link_act(act.id, link_id)

        self.load_controller_control_actions()
        self.ui.lineedit_name_control_action.setText("")

    def on_button_delete_control_action_clicked(self):
        global list_control_actions
        pos = self.ui.listwidget_control_actions.currentRow()
        act = list_control_actions[pos]

        list_id_uca = DB_UCA.select_id_uca_by_control_action(act.id)

        text_delete = "You are deleting " + act.name + "?"

        if len(list_id_uca) > 0:
            cout_req = 0
            for uca_id in list_id_uca:
                cout_req += len(DB_Loss_Scenario_Req.select_id_requirement_by_uca(uca_id))

            text_delete += "\nIf you delete this Control Action, you will lost " + str(
                len(list_id_uca)) + " related UCA."
            text_delete += "\nThis Control Action is related with " + str(cout_req) + " requirements."

        text_delete += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_delete)
        msgBox.setWindowTitle("Delete Control Action")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Actions_Components.delete(act)
            self.load_controller_control_actions()
            self.ui.lineedit_name_control_action.setText("")
            self.disable_edit_control_action()

    def on_button_cancel_control_action_clicked(self):
        self.disable_edit_control_action()
        self.ui.lineedit_name_control_action.setText("")
        self.ui.listwidget_control_actions.selectionModel().clear()
        self.ui.listwidget_control_actions.clearSelection()
        self.ui.listwidget_second_links_act.selectionModel().clear()
        self.ui.listwidget_second_links_act.clearSelection()

    def on_listwidget_control_action_clicked(self):
        global list_control_actions, id_project
        item = self.ui.listwidget_control_actions.currentItem()
        pos = self.ui.listwidget_control_actions.currentRow()

        if pos >= 0:
            item.setSelected(True)
            self.disable_new_control_action()
            self.ui.lineedit_name_control_action.setText(list_control_actions[pos].name)
            self.load_controller_actions_connections()

    def clean_variables(self):
        self.ui.button_add_controller_variable.setEnabled(False)
        self.ui.button_update_controller_variable.setEnabled(False)
        self.ui.button_delete_controller_variable.setEnabled(False)
        self.ui.button_cancel_controller_variable.setEnabled(False)
        self.ui.listwidget_controller_variable.clear()
        self.ui.listwidget_controller_variable.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setEnabled(False)
        self.ui.listwidget_second_links_act.clear()
        self.ui.listwidget_second_links_var.clear()
        self.ui.listwidget_second_links_act.setEnabled(False)
        self.ui.listwidget_second_links_var.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setText("")

    def clean_variables_values(self):
        self.ui.button_add_controller_variable_values.setEnabled(False)
        self.ui.button_update_controller_variable_values.setEnabled(False)
        self.ui.button_delete_controller_variable_values.setEnabled(False)
        self.ui.button_cancel_controller_variable_values.setEnabled(False)
        self.ui.listwidget_controller_variable_values.clear()
        self.ui.listwidget_controller_variable_values.setEnabled(False)
        self.ui.lineedit_name_controller_variable_values.setEnabled(False)
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.listwidget_second_links_act.clearSelection()
        self.ui.listwidget_second_links_act.selectionModel().clear()
        self.ui.listwidget_second_links_var.clearSelection()
        self.ui.listwidget_second_links_var.selectionModel().clear()

    def disable_new_controller_variable_values(self):
        self.ui.button_add_controller_variable_values.setEnabled(False)
        self.ui.button_update_controller_variable_values.setEnabled(True)
        self.ui.button_delete_controller_variable_values.setEnabled(True)
        self.ui.button_cancel_controller_variable_values.setEnabled(True)

    def disable_edit_controller_variable_values(self):
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.lineedit_name_controller_variable_values.setEnabled(True)
        self.ui.listwidget_controller_variable_values.setEnabled(True)
        self.ui.button_add_controller_variable_values.setEnabled(True)
        self.ui.button_update_controller_variable_values.setEnabled(False)
        self.ui.button_delete_controller_variable_values.setEnabled(False)
        self.ui.button_cancel_controller_variable_values.setEnabled(False)

    def on_button_add_controller_variable_clicked(self):
        global id_project, list_component_controller_variables, list_component_controller

        description = self.ui.lineedit_name_controller_variable.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos_c = self.ui.combobox_second_controller.currentIndex()

            var = Variables(0, list_component_controller[pos_c].id, id_project, description, current_date, current_date)
            id_last_var = DB_Variables.insert(var)

            for item in self.ui.listwidget_second_links_var.selectedItems():
                pos = self.ui.listwidget_second_links_var.row(item)
                link_id = list_links_variable_controller[pos].id
                DB_Components_Links.insert_link_var(id_last_var, link_id)

            self.ui.lineedit_name_controller_variable.setText("")
            self.load_component_controller_variables()

    def on_button_update_controller_variable_clicked(self):
        global id_project, list_component_controller_variables, list_component_controller, list_links_variable_controller

        description = self.ui.lineedit_name_controller_variable.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controller_variable.currentRow()

            var = list_component_controller_variables[pos]
            var.name = description
            var.edited_date = current_date
            DB_Variables.update(var)

            index_list = self.ui.listwidget_second_links_var.selectedItems()
            DB_Components_Links.delete_link_var(var.id)

            for item in index_list:
                pos = self.ui.listwidget_second_links_var.row(item)
                link_id = list_links_variable_controller[pos].id
                DB_Components_Links.insert_link_var(var.id, link_id)

            # self.ui.lineedit_name_controller_variable.setText("")
            # self.disable_edit_controller_variable()
            self.load_component_controller_variables()

    def on_button_delete_controller_variable_clicked(self):
        global list_component_controller_variables
        pos = self.ui.listwidget_controller_variable.currentRow()
        var = list_component_controller_variables[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete variable: " + var.name + "?")
        msgBox.setWindowTitle("Delete Variable?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables.delete(var)
            DB_Components_Links.delete_link_var(var.id)
            self.ui.lineedit_name_controller_variable.setText("")
            self.disable_edit_controller_variable()
            self.load_component_controller_variables()
        self.clean_variables_values()

    def on_button_cancel_controller_variable_clicked(self):
        self.disable_edit_controller_variable()
        self.ui.lineedit_name_controller_variable.setText("")
        self.ui.listwidget_controller_variable.selectionModel().clear()
        self.ui.listwidget_controller_variable.clearSelection()
        self.clean_variables_values()

    def on_listwidget_controller_variable_clicked(self):
        global list_component_controller_variables, id_project, list_links_variable_controller
        pos_var = self.ui.listwidget_controller_variable.currentRow()
        self.ui.listwidget_second_links_var.clearSelection()
        self.ui.listwidget_second_links_var.selectionModel().clear()
        item = self.ui.listwidget_controller_variable.currentItem()

        if pos_var >= 0:
            item.setSelected(True)
            self.disable_new_controller_variable()
            self.ui.lineedit_name_controller_variable.setText(list_component_controller_variables[pos_var].name)
            self.load_component_controller_variables_values()
            self.load_controller_variable_connections()

    def load_controller_variable_connections(self):
        global list_component_controller, list_links_variable_controller, id_project, list_component_controller_variables
        pos = self.ui.combobox_second_controller.currentIndex()
        self.ui.listwidget_second_links_var.clear()

        if len(list_component_controller) == 0:
            return

        list_links_variable_controller = DB_Components_Links.select_all_component_links_feedback_by_component(list_component_controller[pos].id)

        for link in list_links_variable_controller:
            self.ui.listwidget_second_links_var.addItem(link.name_src + " -> " + link.name_dst)

        pos_var = self.ui.listwidget_controller_variable.currentRow()
        if pos_var >= 0:
            list_var_link = DB_Components_Links.select_var_link(list_component_controller_variables[pos_var].id)
            count = 0

            for link in list_links_variable_controller:
                for vl in list_var_link:
                    if link.id == vl.id_link:
                        self.ui.listwidget_second_links_var.item(count).setSelected(True)
                count += 1

    def load_controller_actions_connections(self):
        global list_component_controller, list_links_actions_controller, id_project, list_control_actions
        pos = self.ui.combobox_second_controller.currentIndex()
        list_links_actions_controller = DB_Components_Links.select_all_component_links_actions_by_component(
            list_component_controller[pos].id)
        self.ui.listwidget_second_links_act.clear()

        for link in list_links_actions_controller:
            self.ui.listwidget_second_links_act.addItem(link.name_src + " -> " + link.name_dst)

        pos_var = self.ui.listwidget_control_actions.currentRow()
        if pos_var >= 0:
            list_act_link = DB_Components_Links.select_act_link(list_control_actions[pos_var].id)
            count = 0

            for link in list_links_actions_controller:
                for vl in list_act_link:
                    if link.id == vl.id_link:
                        self.ui.listwidget_second_links_act.item(count).setSelected(True)
                count += 1

    def load_component_controller_variables_values(self):
        global list_component_controller_variables, list_component_controller_variables_values, id_project
        pos_var = self.ui.listwidget_controller_variable.currentRow()

        list_component_controller_variables_values = DB_Variables_Values.select_values_by_variable(
            list_component_controller_variables[pos_var].id)

        self.ui.listwidget_controller_variable_values.clear()
        for val in list_component_controller_variables_values:
            self.ui.listwidget_controller_variable_values.addItem(val.value)
        self.disable_edit_controller_variable_values()

    def on_button_add_controller_variable_values_clicked(self):
        global id_project, list_component_controller_variables_values, list_component_controller_variables, list_component_controller

        description = self.ui.lineedit_name_controller_variable_values.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos_var = self.ui.listwidget_controller_variable.currentRow()

            var = Variable_Values(0, list_component_controller_variables[pos_var].id, description, current_date,
                                  current_date)

            DB_Variables_Values.insert(var)

            self.load_component_controller_variables_values()
            self.ui.lineedit_name_controller_variable_values.setText("")

    def on_button_update_controller_variable_values_clicked(self):
        global id_project, list_component_controller_variables_values, list_component_controller

        description = self.ui.lineedit_name_controller_variable_values.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controller_variable_values.currentRow()

            val = list_component_controller_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controller_variables_values()
            self.ui.lineedit_name_controller_variable_values.setText("")
            self.disable_edit_controller_variable_values()
            self.ui.listwidget_controller_variable_values.selectionModel().clear()
            self.ui.listwidget_controller_variable_values.clearSelection()

    def on_button_delete_controller_variable_values_clicked(self):
        global list_component_controller_variables_values
        pos = self.ui.listwidget_controller_variable_values.currentRow()
        val = list_component_controller_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controller_variables_values()
            self.ui.lineedit_name_controller_variable_values.setText("")
            self.disable_edit_controller_variable_values()
            self.ui.listwidget_controller_variable_values.clearSelection()
            self.ui.listwidget_controller_variable_values.selectionModel().clear()

    def on_button_cancel_controller_variable_values_clicked(self):
        self.disable_edit_controller_variable_values()
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.listwidget_controller_variable_values.selectionModel().clear()
        self.ui.listwidget_controller_variable_values.clearSelection()

    def on_listwidget_controller_variable_values_clicked(self):
        global list_component_controller_variables_values, id_project
        pos_var = self.ui.listwidget_controller_variable_values.currentRow()
        item = self.ui.listwidget_controller_variable_values.currentItem()

        if pos_var >= 0:
            item.setSelected(True)
            self.disable_new_controller_variable_values()
            self.ui.lineedit_name_controller_variable_values.setText(
                list_component_controller_variables_values[pos_var].value)

    def disable_controller_connections(self):
        self.ui.combobox_controller_connection.setEnabled(False)
        self.ui.button_add_controller_connection.setEnabled(False)
        self.ui.button_delete_controller_connection.setEnabled(False)
        self.ui.listwidget_controller_connection.setEnabled(False)
        self.ui.listwidget_controller_connection.clear()
        self.ui.combobox_controller_connection.clear()

    def disable_exts_connections(self):
        self.ui.combobox_exts_connection.setEnabled(False)
        self.ui.button_add_exts_connection.setEnabled(False)
        self.ui.button_delete_exts_connection.setEnabled(False)
        self.ui.listwidget_exts_connection.setEnabled(False)

        self.ui.combobox_exts_connection.clear()
        self.ui.listwidget_exts_connection.clear()

    def disable_actuator_connections(self):
        self.ui.combobox_actuator_connection.setEnabled(False)
        self.ui.button_add_actuator_connection.setEnabled(False)
        self.ui.button_delete_actuator_connection.setEnabled(False)
        self.ui.listwidget_actuator_connection.setEnabled(False)

        self.ui.combobox_actuator_connection.clear()
        self.ui.listwidget_actuator_connection.clear()

    def disable_sensor_connections(self):
        self.ui.combobox_sensor_connection.setEnabled(False)
        self.ui.button_add_sensor_connection.setEnabled(False)
        self.ui.button_delete_sensor_connection.setEnabled(False)
        self.ui.listwidget_sensor_connection.setEnabled(False)

        self.ui.combobox_sensor_connection.clear()
        self.ui.listwidget_sensor_connection.clear()

    def disable_controlled_process_connections(self):
        self.ui.combobox_controlled_process_connection.setEnabled(False)
        self.ui.button_add_controlled_process_connection.setEnabled(False)
        self.ui.button_delete_controlled_process_connection.setEnabled(False)
        self.ui.listwidget_controlled_process_connection.setEnabled(False)

        self.ui.combobox_controlled_process_connection.clear()
        self.ui.listwidget_controlled_process_connection.clear()

    def disable_controller_actions_variables(self):
        self.ui.lineedit_name_control_action.setEnabled(False)
        self.ui.lineedit_name_control_action.setText("")
        self.ui.button_add_control_action.setEnabled(False)
        self.ui.button_update_control_action.setEnabled(False)
        self.ui.button_delete_control_action.setEnabled(False)
        self.ui.button_cancel_control_action.setEnabled(False)
        self.ui.listwidget_control_actions.setEnabled(False)
        self.ui.listwidget_control_actions.clear()
        self.ui.lineedit_name_controller_variable.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setText("")
        self.ui.button_add_controller_variable.setEnabled(False)
        self.ui.button_update_controller_variable.setEnabled(False)
        self.ui.button_delete_controller_variable.setEnabled(False)
        self.ui.button_cancel_controller_variable.setEnabled(False)
        self.ui.listwidget_controller_variable.setEnabled(False)
        self.ui.listwidget_controller_variable.clear()
        self.ui.lineedit_name_controller_variable_values.setEnabled(False)
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.button_add_controller_variable_values.setEnabled(False)
        self.ui.button_update_controller_variable_values.setEnabled(False)
        self.ui.button_delete_controller_variable_values.setEnabled(False)
        self.ui.button_cancel_controller_variable_values.setEnabled(False)
        self.ui.listwidget_controller_variable_values.setEnabled(False)
        self.ui.listwidget_controller_variable_values.clear()
        self.ui.listwidget_second_links_act.setEnabled(False)
        self.ui.listwidget_second_links_act.clear()
        self.ui.listwidget_second_links_var.setEnabled(False)
        self.ui.listwidget_second_links_var.clear()

    def load_component_actuator(self):
        global list_component_actuator, id_project
        list_component_actuator = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_ACTUATOR,
                                                                                           id_project)

        self.ui.listwidget_actuator.clear()
        for pos in range(len(list_component_actuator)):
            self.ui.listwidget_actuator.addItem(list_component_actuator[pos].name)

    def disable_edit_actuator(self):
        self.ui.button_add_actuator.setEnabled(True)
        self.ui.button_update_actuator.setEnabled(False)
        self.ui.button_delete_actuator.setEnabled(False)
        self.ui.button_cancel_actuator.setEnabled(False)
        self.ui.lineedit_name_actuator.setText("")

    def disable_new_actuator(self):
        self.ui.button_add_actuator.setEnabled(False)
        self.ui.button_update_actuator.setEnabled(True)
        self.ui.button_delete_actuator.setEnabled(True)
        self.ui.button_cancel_actuator.setEnabled(True)

    def on_button_add_actuator_clicked(self):
        global id_project, list_component_actuator

        description = self.ui.lineedit_name_actuator.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = Component(0, Constant.DB_ID_ACTUATOR, id_project, description, current_date, current_date)
            DB_Components.insert_to_table(comp)

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

            self.load_component_actuator()
            self.ui.lineedit_name_actuator.setText("")

    def on_button_update_actuator_clicked(self):
        global list_component_actuator

        name = self.ui.lineedit_name_actuator.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_actuator.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_actuator[pos]
            comp.name = name
            comp.edited_date = current_date

            DB_Components.update_component(comp)

            self.disable_edit_actuator()
            self.load_component_actuator()
            self.disable_edit_actuator()
            self.disable_actuator_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_delete_actuator_clicked(self):
        global list_component_actuator
        pos = self.ui.listwidget_actuator.currentRow()
        act = list_component_actuator[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + act.name + "?")
        msgBox.setWindowTitle("Delete Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete(act)

            self.disable_edit_actuator()
            self.load_component_actuator()
            self.ui.lineedit_name_actuator.setText("")
            self.ui.listwidget_actuator.clearSelection()
            self.ui.listwidget_actuator.selectionModel().clear()
            self.disable_edit_actuator()
            self.disable_actuator_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_cancel_actuator_clicked(self):
        self.disable_edit_actuator()
        self.ui.lineedit_name_actuator.setText("")
        self.ui.listwidget_actuator.selectionModel().clear()
        self.ui.listwidget_actuator.clearSelection()
        self.disable_actuator_connections()
        self.disable_edit_actuator()

    def on_listwidget_actuators_clicked(self):
        global list_component_actuator
        item = self.ui.listwidget_actuator.currentItem()
        pos = self.ui.listwidget_actuator.currentRow()

        self.disable_new_actuator()

        if pos >= 0:
            item.setSelected(True)
            self.ui.lineedit_name_actuator.setText(list_component_actuator[pos].name)
            self.load_actuator_connections()

    def load_component_exts(self):
        global list_component_exts, id_project
        list_component_exts = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_EXT_INFORMATION,
                                                                                       id_project)

        self.ui.listwidget_exts.clear()
        for pos in range(len(list_component_exts)):
            self.ui.listwidget_exts.addItem(list_component_exts[pos].name)

    def disable_edit_exts(self):
        self.ui.button_add_exts.setEnabled(True)
        self.ui.button_update_exts.setEnabled(False)
        self.ui.button_delete_exts.setEnabled(False)
        self.ui.button_cancel_exts.setEnabled(False)
        self.ui.lineedit_name_exts.setText("")

    def disable_new_exts(self):
        self.ui.button_add_exts.setEnabled(False)
        self.ui.button_update_exts.setEnabled(True)
        self.ui.button_delete_exts.setEnabled(True)
        self.ui.button_cancel_exts.setEnabled(True)

    def on_button_add_exts_clicked(self):
        global id_project, list_component_exts

        description = self.ui.lineedit_name_exts.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
            return

        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK)

        comp = Component(0, Constant.DB_ID_EXT_INFORMATION, id_project, description, current_date, current_date)
        result = DB_Components.insert_to_table(comp)

        if result > 0:
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()
            self.load_component_exts()
            self.ui.lineedit_name_exts.setText("")

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

        else:
            showdialog("Error to create External System",
                       "Something goes wrong during the creation of External System. Try again...")

    def on_button_update_exts_clicked(self):
        global list_component_exts

        name = self.ui.lineedit_name_exts.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_exts.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_exts[pos]
            comp.name = name
            comp.edited_date = current_date

            DB_Components.update_component(comp)

            self.disable_edit_exts()
            self.load_component_exts()
            self.ui.lineedit_name_exts.setText("")
            self.ui.listwidget_exts.clearSelection()
            self.ui.listwidget_exts.selectionModel().clear()
            self.disable_edit_exts()
            self.disable_exts_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_delete_exts_clicked(self):
        global list_component_exts
        pos = self.ui.listwidget_exts.currentRow()
        act = list_component_exts[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + act.name + "?")
        msgBox.setWindowTitle("Delete Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete(act)
            self.disable_edit_exts()
            self.load_component_exts()
            self.ui.lineedit_name_exts.setText("")
            self.load_component_exts()
            self.ui.listwidget_exts.clearSelection()
            self.ui.listwidget_exts.selectionModel().clear()
            self.disable_edit_exts()
            self.disable_exts_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_cancel_exts_clicked(self):
        self.disable_edit_exts()
        self.ui.lineedit_name_exts.setText("")
        self.ui.listwidget_exts.selectionModel().clear()
        self.ui.listwidget_exts.clearSelection()
        self.disable_exts_connections()

    def on_listwidget_exts_clicked(self):
        global list_component_exts
        pos = self.ui.listwidget_exts.currentRow()
        item = self.ui.listwidget_exts.currentItem()

        if pos >= 0:
            self.disable_new_exts()
            item.setSelected(True)
            self.ui.lineedit_name_exts.setText(list_component_exts[pos].name)
            self.load_exts_connections()

    def load_component_sensor(self):
        global list_component_sensor, id_project
        list_component_sensor = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_SENSOR, id_project)

        self.ui.listwidget_sensor.clear()
        for pos in range(len(list_component_sensor)):
            self.ui.listwidget_sensor.addItem(list_component_sensor[pos].name)

    def disable_edit_sensor(self):
        self.ui.button_add_sensor.setEnabled(True)
        self.ui.button_update_sensor.setEnabled(False)
        self.ui.button_delete_sensor.setEnabled(False)
        self.ui.button_cancel_sensor.setEnabled(False)
        self.ui.lineedit_name_sensor.setText("")

    def disable_new_sensor(self):
        self.ui.button_add_sensor.setEnabled(False)
        self.ui.button_update_sensor.setEnabled(True)
        self.ui.button_delete_sensor.setEnabled(True)
        self.ui.button_cancel_sensor.setEnabled(True)

    def on_button_add_sensor_clicked(self):
        global id_project, list_component_sensor

        description = self.ui.lineedit_name_sensor.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = Component(0, Constant.DB_ID_SENSOR, id_project, description, current_date, current_date)
            DB_Components.insert_to_table(comp)

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

            self.load_component_sensor()
            self.ui.lineedit_name_sensor.setText("")

    def on_button_update_sensor_clicked(self):
        global list_component_sensor

        name = self.ui.lineedit_name_sensor.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_sensor.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_sensor[pos]
            comp.name = name
            comp.edited_date = current_date

            DB_Components.update_component(comp)

            self.disable_edit_sensor()
            self.load_component_sensor()
            self.ui.lineedit_name_sensor.setText("")
            self.ui.listwidget_sensor.clearSelection()
            self.ui.listwidget_sensor.selectionModel().clear()
            self.disable_edit_sensor()
            self.disable_sensor_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

    def on_button_delete_sensor_clicked(self):
        global list_component_sensor
        pos = self.ui.listwidget_sensor.currentRow()
        act = list_component_sensor[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + act.name + "?")
        msgBox.setWindowTitle("Delete Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete(act)
            self.disable_edit_sensor()
            self.load_component_sensor()
            self.ui.lineedit_name_sensor.setText("")
            self.load_component_sensor()
            self.ui.listwidget_sensor.clearSelection()
            self.ui.listwidget_sensor.selectionModel().clear()
            self.disable_edit_sensor()
            self.disable_sensor_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

    def on_button_cancel_sensor_clicked(self):
        self.disable_edit_sensor()
        self.ui.lineedit_name_sensor.setText("")
        self.ui.listwidget_sensor.selectionModel().clear()
        self.ui.listwidget_sensor.clearSelection()
        self.disable_sensor_connections()

    def on_listwidget_sensors_clicked(self):
        global list_component_sensor
        pos = self.ui.listwidget_sensor.currentRow()
        item = self.ui.listwidget_sensor.currentItem()

        if pos >= 0:
            self.disable_new_sensor()
            item.setSelected(True)
            self.ui.lineedit_name_sensor.setText(list_component_sensor[pos].name)
            self.load_sensor_connections()

    def load_component_controlled_proccess(self):
        global list_component_controlled_process, id_project
        list_component_controlled_process = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP,
                                                                                                     id_project)

        if len(list_component_controlled_process) > 0:
            self.ui.lineedit_name_controlled_process.setEnabled(False)
            self.ui.lineedit_name_controlled_process.setText(list_component_controlled_process[0].name)
            self.disable_new_controlled_proccess()
            self.load_controlled_process_connections()
            self.load_component_controlled_process_input()
            self.load_component_controlled_process_output()
            self.load_component_controlled_process_envd()

        else:
            self.ui.lineedit_name_controlled_process.setText("")
            self.ui.lineedit_name_controlled_process.setEnabled(True)
            self.disable_edit_controlled_proccess()
            self.clean_cp_envd_inputs_outputs()

    def disable_edit_controlled_proccess(self):
        self.ui.button_save_controlled_process.setEnabled(True)
        self.ui.button_edit_controlled_process.setEnabled(False)
        self.ui.button_delete_controlled_process.setEnabled(False)
        self.ui.button_cancel_controlled_process.setEnabled(False)

    def disable_new_controlled_proccess(self):
        self.ui.button_save_controlled_process.setEnabled(False)
        self.ui.button_edit_controlled_process.setEnabled(True)
        self.ui.button_delete_controlled_process.setEnabled(True)
        self.ui.button_cancel_controlled_process.setEnabled(False)

    def on_button_save_controlled_process_clicked(self):
        global id_project, list_component_controlled_process, list_controlled_process_output, list_controlled_process_input, list_controlled_process_env_dist

        description = self.ui.lineedit_name_controlled_process.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            if len(list_component_controlled_process) == 0:
                comp = Component(0, Constant.DB_ID_CP, id_project, description, current_date, current_date)
                DB_Components.insert_controlled_process(comp)

            else:
                comp = list_component_controlled_process[0]
                comp.name = description
                comp.edited_date = current_date
                DB_Components.update_component(comp)

                comp_in = list_controlled_process_input[0]
                comp_in.name = description + " " + Constant.INPUT
                comp_in.edited_date = current_date
                DB_Components.update_component(comp_in)

                comp_out = list_controlled_process_output[0]
                comp_out.name = description + " " + Constant.OUTPUT
                comp_out.edited_date = current_date
                DB_Components.update_component(comp_out)

                comp_env = list_controlled_process_env_dist[0]
                comp_env.name = description + " " + Constant.ENVIRONMENTAL_DISTURBANCES
                comp_env.edited_date = current_date
                DB_Components.update_component(comp_env)

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

            if self.ui.listwidget_actuator.isEnabled():
                self.load_actuator_connections()

            self.load_component_controlled_proccess()

    def on_button_edit_controlled_process_clicked(self):
        global list_component_controlled_process

        self.ui.lineedit_name_controlled_process.setEnabled(True)
        self.ui.button_edit_controlled_process.setEnabled(False)
        self.ui.button_save_controlled_process.setEnabled(True)
        self.ui.button_delete_controlled_process.setEnabled(True)
        self.ui.button_cancel_controlled_process.setEnabled(True)

    def on_button_delete_controlled_process_clicked(self):
        global list_component_controlled_process
        if len(list_component_controlled_process) > 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete: " + list_component_controlled_process[0].name + "?")
            msgBox.setWindowTitle("Delete Controlled Procces?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Components.delete_controlled_procces(list_component_controlled_process[0])

                if self.ui.listwidget_controller_connection.isEnabled():
                    self.load_controller_connections()

                if self.ui.listwidget_actuator.isEnabled():
                    self.load_actuator_connections()

                # self.load_controlled_process_connections()
                self.disable_controlled_process_connections()

        self.load_component_controlled_proccess()

    def on_button_cancel_controlled_process_clicked(self):
        self.load_component_controlled_proccess()

    def clean_cp_envd_inputs_outputs(self):
        self.ui.button_add_controlled_process_envd.setEnabled(False)
        self.ui.button_update_controlled_process_envd.setEnabled(False)
        self.ui.button_delete_controlled_process_envd.setEnabled(False)
        self.ui.button_cancel_controlled_process_envd.setEnabled(False)
        self.ui.listwidget_controlled_process_envd.clear()
        self.ui.listwidget_controlled_process_envd.setEnabled(False)
        self.ui.lineedit_name_controlled_process_envd.setEnabled(False)
        self.ui.lineedit_name_controlled_process_envd.setText("")

        self.ui.button_add_controlled_process_input.setEnabled(False)
        self.ui.button_update_controlled_process_input.setEnabled(False)
        self.ui.button_delete_controlled_process_input.setEnabled(False)
        self.ui.button_cancel_controlled_process_input.setEnabled(False)
        self.ui.listwidget_controlled_process_input.clear()
        self.ui.listwidget_controlled_process_input.setEnabled(False)
        self.ui.lineedit_name_controlled_process_input.setEnabled(False)
        self.ui.lineedit_name_controlled_process_input.setText("")

        self.ui.button_add_controlled_process_output.setEnabled(False)
        self.ui.button_update_controlled_process_output.setEnabled(False)
        self.ui.button_delete_controlled_process_output.setEnabled(False)
        self.ui.button_cancel_controlled_process_output.setEnabled(False)
        self.ui.listwidget_controlled_process_output.clear()
        self.ui.listwidget_controlled_process_output.setEnabled(False)
        self.ui.lineedit_name_controlled_process_output.setEnabled(False)
        self.ui.lineedit_name_controlled_process_output.setText("")

    def load_component_controlled_process_input(self):
        global list_component_controlled_process, id_project, list_controlled_process_input, list_controlled_process_env_dist, \
            list_controlled_process_input_variables, list_controlled_process_input_variables_values

        self.ui.listwidget_controlled_process_input.clear()

        if len(list_component_controlled_process) > 0:

            list_controlled_process_input = DB_Components.select_component_by_project_father_thing(id_project, list_component_controlled_process[0].id, Constant.DB_ID_INPUT)
            list_controlled_process_env_dist = DB_Components.select_component_by_project_father_thing(id_project, list_component_controlled_process[0].id, Constant.DB_ID_ENV_DISTURBANCES)

            if len(list_controlled_process_input) > 0:
                list_controlled_process_input_variables = DB_Variables.select_variables_by_component_project(list_controlled_process_input[0].id, id_project)

                if len(list_controlled_process_input_variables) > 0:
                    self.ui.listwidget_controlled_process_input.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_input.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_input.setText("")

                    list_controlled_process_input_variables_values = DB_Variables_Values.select_values_by_variable(
                        list_controlled_process_input_variables[0].id)

                    self.ui.listwidget_controlled_process_input.clear()

                    for val in list_controlled_process_input_variables_values:
                        self.ui.listwidget_controlled_process_input.addItem(val.value)
                    self.disable_edit_controlled_process_input()

    def load_component_controlled_process_output(self):
        global list_component_controlled_process, id_project, list_controlled_process_output, list_controlled_process_env_dist, \
            list_controlled_process_output_variables, list_controlled_process_output_variables_values

        self.ui.listwidget_controlled_process_output.clear()

        if len(list_component_controlled_process) > 0:
            list_controlled_process_output = DB_Components.select_component_by_project_father_thing(id_project,
                                                                                                    list_component_controlled_process[
                                                                                                        0].id,
                                                                                                    Constant.DB_ID_OUTPUT)

            if len(list_controlled_process_output) > 0:
                list_controlled_process_output_variables = DB_Variables.select_variables_by_component_project(
                    list_controlled_process_output[0].id, id_project)

                if len(list_controlled_process_output_variables) > 0:
                    self.ui.listwidget_controlled_process_output.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_output.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_output.setText("")

                    list_controlled_process_output_variables_values = DB_Variables_Values.select_values_by_variable(
                        list_controlled_process_output_variables[0].id)

                    self.ui.listwidget_controlled_process_output.clear()

                    for val in list_controlled_process_output_variables_values:
                        self.ui.listwidget_controlled_process_output.addItem(val.value)
                    self.disable_edit_controlled_process_output()

    def load_component_controlled_process_envd(self):
        global list_component_controlled_process, id_project, list_controlled_process_envd, list_controlled_process_env_dist, list_controlled_process_envd_variables, list_controlled_process_envd_variables_values

        self.ui.listwidget_controlled_process_envd.clear()

        if len(list_component_controlled_process) > 0:
            list_controlled_process_envd = DB_Components.select_component_by_project_father_thing(id_project,
                                                                                                  list_component_controlled_process[
                                                                                                      0].id,
                                                                                                  Constant.DB_ID_ENV_DISTURBANCES)

            if len(list_controlled_process_envd) > 0:
                list_controlled_process_envd_variables = DB_Variables.select_variables_by_component_project(
                    list_controlled_process_envd[0].id, id_project)

                if len(list_controlled_process_envd_variables) > 0:
                    self.ui.listwidget_controlled_process_envd.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_envd.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_envd.setText("")

                    list_controlled_process_envd_variables_values = DB_Variables_Values.select_values_by_variable(
                        list_controlled_process_envd_variables[0].id)

                    self.ui.listwidget_controlled_process_envd.clear()

                    for val in list_controlled_process_envd_variables_values:
                        self.ui.listwidget_controlled_process_envd.addItem(val.value)
                    self.disable_edit_controlled_process_envd()

    def on_listwidget_controlled_process_envd_clicked(self):
        global list_controlled_process_envd_variables_values, id_project
        pos_var = self.ui.listwidget_controlled_process_envd.currentRow()

        if pos_var >= 0:
            item = self.ui.listwidget_controlled_process_envd.currentItem()
            item.setSelected(True)
            self.disable_new_controlled_process_envd()
            self.ui.lineedit_name_controlled_process_envd.setText(
                list_controlled_process_envd_variables_values[pos_var].value)

    def on_button_add_controlled_process_envd_clicked(self):
        global id_project, list_controlled_process_envd_variables

        description = self.ui.lineedit_name_controlled_process_envd.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # pos_var = self.ui.listwidget_controlled_process_variable.currentRow()

            if len(list_controlled_process_envd_variables) > 0:
                var = Variable_Values(0, list_controlled_process_envd_variables[0].id, description, current_date,
                                      current_date)
                DB_Variables_Values.insert(var)

                self.load_component_controlled_process_input()
                self.load_component_controlled_process_envd()
                self.load_component_controlled_process_envd()
                self.ui.lineedit_name_controlled_process_envd.setText("")

    def on_button_update_controlled_process_envd_clicked(self):
        global id_project, list_controlled_process_envd_variables_values

        description = self.ui.lineedit_name_controlled_process_envd.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controlled_process_envd.currentRow()

            val = list_controlled_process_envd_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controlled_process_envd()
            self.ui.lineedit_name_controlled_process_envd.setText("")
            self.ui.listwidget_controlled_process_envd.clearSelection()
            self.ui.listwidget_controlled_process_envd.selectionModel().clear()
            self.disable_edit_controlled_process_envd()

    def on_button_delete_controlled_process_envd_clicked(self):
        global list_controlled_process_envd_variables_values
        pos = self.ui.listwidget_controlled_process_envd.currentRow()
        val = list_controlled_process_envd_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controlled_process_envd()
            self.ui.lineedit_name_controlled_process_envd.setText("")
            self.disable_edit_controlled_process_envd()
            self.ui.listwidget_controlled_process_envd.selectionModel().clear()
            self.ui.listwidget_controlled_process_envd.clearSelection()

    def on_button_cancel_controlled_process_envd_clicked(self):
        self.disable_edit_controlled_process_envd()
        self.ui.lineedit_name_controlled_process_envd.setText("")
        self.ui.listwidget_controlled_process_envd.clearSelection()
        self.ui.listwidget_controlled_process_envd.selectionModel().clear()

    def on_button_add_controlled_process_input_clicked(self):
        global id_project, list_controlled_process_input_variables

        description = self.ui.lineedit_name_controlled_process_input.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # pos_var = self.ui.listwidget_controlled_process_variable.currentRow()

            if len(list_controlled_process_input_variables) > 0:
                var = Variable_Values(0, list_controlled_process_input_variables[0].id, description, current_date,
                                      current_date)
                DB_Variables_Values.insert(var)

                self.load_component_controlled_process_input()
                self.ui.lineedit_name_controlled_process_input.setText("")

    def on_button_update_controlled_process_input_clicked(self):
        global id_project, list_controlled_process_input_variables_values

        description = self.ui.lineedit_name_controlled_process_input.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controlled_process_input.currentRow()

            val = list_controlled_process_input_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controlled_process_input()
            self.ui.lineedit_name_controlled_process_input.setText("")
            self.ui.listwidget_controlled_process_input.clearSelection()
            self.ui.listwidget_controlled_process_input.selectionModel().clear()
            self.disable_edit_controlled_process_input()

    def on_button_delete_controlled_process_input_clicked(self):
        global list_controlled_process_input_variables_values
        pos = self.ui.listwidget_controlled_process_input.currentRow()
        val = list_controlled_process_input_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controlled_process_input()
            self.load_component_controlled_process_output()
            self.ui.lineedit_name_controlled_process_input.setText("")
            self.disable_edit_controlled_process_input()
            self.ui.listwidget_controlled_process_input.selectionModel().clear()
            self.ui.listwidget_controlled_process_input.clearSelection()

    def on_button_cancel_controlled_process_input_clicked(self):
        self.disable_edit_controlled_process_input()
        self.ui.lineedit_name_controlled_process_input.setText("")
        self.ui.listwidget_controlled_process_input.clearSelection()
        self.ui.listwidget_controlled_process_input.selectionModel().clear()

    def on_listwidget_controlled_process_input_clicked(self):
        global list_controlled_process_input_variables_values, id_project
        pos_var = self.ui.listwidget_controlled_process_input.currentRow()

        if pos_var >= 0:
            item = self.ui.listwidget_controlled_process_input.currentItem()
            item.setSelected(True)
            self.disable_new_controlled_process_input()
            self.ui.lineedit_name_controlled_process_input.setText(
                list_controlled_process_input_variables_values[pos_var].value)

    def on_button_add_controlled_process_output_clicked(self):
        global id_project, list_controlled_process_output_variables

        description = self.ui.lineedit_name_controlled_process_output.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # pos_var = self.ui.listwidget_controlled_process_variable.currentRow()

            if len(list_controlled_process_output_variables) > 0:
                var = Variable_Values(0, list_controlled_process_output_variables[0].id, description, current_date,
                                      current_date)
                DB_Variables_Values.insert(var)

                self.load_component_controlled_process_input()
                self.load_component_controlled_process_output()
                self.ui.lineedit_name_controlled_process_output.setText("")

    def on_button_update_controlled_process_output_clicked(self):
        global id_project, list_controlled_process_output_variables_values

        description = self.ui.lineedit_name_controlled_process_output.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controlled_process_output.currentRow()

            val = list_controlled_process_output_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controlled_process_output()
            self.ui.lineedit_name_controlled_process_output.setText("")
            self.ui.listwidget_controlled_process_output.clearSelection()
            self.ui.listwidget_controlled_process_output.selectionModel().clear()
            self.disable_edit_controlled_process_output()

    def on_button_delete_controlled_process_output_clicked(self):
        global list_controlled_process_output_variables_values
        pos = self.ui.listwidget_controlled_process_output.currentRow()
        val = list_controlled_process_output_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controlled_process_output()
            self.ui.lineedit_name_controlled_process_output.setText("")
            self.disable_edit_controlled_process_output()
            self.ui.listwidget_controlled_process_output.selectionModel().clear()
            self.ui.listwidget_controlled_process_output.clearSelection()

    def on_button_cancel_controlled_process_output_clicked(self):
        self.disable_edit_controlled_process_output()
        self.ui.lineedit_name_controlled_process_output.setText("")
        self.ui.listwidget_controlled_process_output.clearSelection()
        self.ui.listwidget_controlled_process_output.selectionModel().clear()

    def on_listwidget_controlled_process_output_clicked(self):
        global list_controlled_process_output_variables_values, id_project
        pos_var = self.ui.listwidget_controlled_process_output.currentRow()

        if pos_var >= 0:
            item = self.ui.listwidget_controlled_process_output.currentItem()
            item.setSelected(True)
            self.disable_new_controlled_process_output()
            self.ui.lineedit_name_controlled_process_output.setText(
                list_controlled_process_output_variables_values[pos_var].value)

    def disable_new_controlled_process_envd(self):
        self.ui.button_add_controlled_process_envd.setEnabled(False)
        self.ui.button_update_controlled_process_envd.setEnabled(True)
        self.ui.button_delete_controlled_process_envd.setEnabled(True)
        self.ui.button_cancel_controlled_process_envd.setEnabled(True)

    def disable_edit_controlled_process_envd(self):
        self.ui.lineedit_name_controlled_process_envd.setText("")
        self.ui.lineedit_name_controlled_process_envd.setEnabled(True)
        self.ui.listwidget_controlled_process_envd.setEnabled(True)
        self.ui.button_add_controlled_process_envd.setEnabled(True)
        self.ui.button_update_controlled_process_envd.setEnabled(False)
        self.ui.button_delete_controlled_process_envd.setEnabled(False)
        self.ui.button_cancel_controlled_process_envd.setEnabled(False)

    def disable_new_controlled_process_input(self):
        self.ui.button_add_controlled_process_input.setEnabled(False)
        self.ui.button_update_controlled_process_input.setEnabled(True)
        self.ui.button_delete_controlled_process_input.setEnabled(True)
        self.ui.button_cancel_controlled_process_input.setEnabled(True)

    def disable_edit_controlled_process_input(self):
        self.ui.lineedit_name_controlled_process_input.setText("")
        self.ui.lineedit_name_controlled_process_input.setEnabled(True)
        self.ui.listwidget_controlled_process_input.setEnabled(True)
        self.ui.button_add_controlled_process_input.setEnabled(True)
        self.ui.button_update_controlled_process_input.setEnabled(False)
        self.ui.button_delete_controlled_process_input.setEnabled(False)
        self.ui.button_cancel_controlled_process_input.setEnabled(False)

    def disable_new_controlled_process_output(self):
        self.ui.button_add_controlled_process_output.setEnabled(False)
        self.ui.button_update_controlled_process_output.setEnabled(True)
        self.ui.button_delete_controlled_process_output.setEnabled(True)
        self.ui.button_cancel_controlled_process_output.setEnabled(True)

    def disable_edit_controlled_process_output(self):
        self.ui.lineedit_name_controlled_process_output.setText("")
        self.ui.lineedit_name_controlled_process_output.setEnabled(True)
        self.ui.listwidget_controlled_process_output.setEnabled(True)
        self.ui.button_add_controlled_process_output.setEnabled(True)
        self.ui.button_update_controlled_process_output.setEnabled(False)
        self.ui.button_delete_controlled_process_output.setEnabled(False)
        self.ui.button_cancel_controlled_process_output.setEnabled(False)

    def load_controller_control_actions(self):
        global list_component_controller, list_control_actions, id_project
        pos_controller = self.ui.combobox_second_controller.currentIndex()

        self.ui.listwidget_control_actions.clear()
        self.disable_edit_control_action()

        if len(list_component_controller) == 0:
            return

        list_control_actions = DB_Actions_Components.select_actions_by_component_and_project(
            list_component_controller[pos_controller].id, id_project)
        for pos in range(len(list_control_actions)):
            self.ui.listwidget_control_actions.addItem(list_control_actions[pos].name)

        self.load_controller_actions_connections()

    def load_component_controller_variables(self):
        global list_component_controller, list_component_controller_variables, id_project
        pos_controller = self.ui.combobox_second_controller.currentIndex()

        if pos_controller >= 0:
            list_component_controller_variables = DB_Variables.select_variables_by_component_project(
                list_component_controller[pos_controller].id, id_project)

            self.ui.listwidget_controller_variable.clear()
            self.ui.listwidget_controller_variable_values.clear()
            self.disable_edit_controller_variable()
            self.clean_variables_values()

            for pos in range(len(list_component_controller_variables)):
                self.ui.listwidget_controller_variable.addItem(list_component_controller_variables[pos].name)
        self.load_controller_variable_connections()

    def check_control_structure(self):
        global id_project
        warning = ""

        warning += DB_Components.find_component_warnings(id_project)
        empty_links = DB_Components_Links.select_empty_links(id_project)
        if warning != "" and empty_links != "":
            warning += "\n"
        warning += empty_links

        w_var = DB_Variables.select_variables_warning(id_project)
        if warning != "" and w_var != "":
            warning += "\n"
        warning += w_var

        list_responsibilities_without_ssc = DB_Responsibility.check_control_structure(id_project)

        if len(list_responsibilities_without_ssc) > 0:
            warning += "Responsibilities without SSC\n"

            for resp in list_responsibilities_without_ssc:
                warning += "\t" + resp + "\n"

        if warning == "":
            self.ui.label_structure_warnings.setText("No warnings detected")
        else:
            self.ui.label_structure_warnings.setText(warning)

    #
    # feedback at least 2 values
    #
    # confirm, controller with variable


    # ----- Functions STPA 2 Step -----

    # ----- Functions STPA 1 Step -----
    def load_goals(self):
        # Goals information
        global list_goals, id_project
        self.ui.list_saf_goals.clear()
        list_goals = DB_Goals.select_all_goals_by_project(id_project)
        for pos in range(len(list_goals)):
            self.ui.list_saf_goals.addItem("G-" + str(list_goals[pos].id_goal) + ": " + list_goals[pos].description)

    def on_list_saf_goals_clicked(self):
        item = self.ui.list_saf_goals.currentItem()
        pos = self.ui.list_saf_goals.currentRow()

        self.ui.button_saf_new_goal.setEnabled(False)
        self.ui.button_saf_update_goal.setEnabled(True)
        self.ui.button_saf_delete_goal.setEnabled(True)
        self.ui.button_saf_cancel_goal.setEnabled(True)

        global list_goals
        self.ui.label_saf_goal_position.setText("G-" + str(list_goals[pos].id_goal))
        self.ui.lineedit_saf_goal.setText(list_goals[pos].description)

    def on_button_saf_new_goal_clicked(self):
        global id_project, list_goals

        description = self.ui.lineedit_saf_goal.text()
        if len(description) > 0:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_goal = len(list_goals) + 1
            goal = Goal(0, id_project, pos_goal, description, current_date, current_date)
            DB_Goals.insert_to_goals(goal)

            self.load_goals()
            self.ui.lineedit_saf_goal.setText("")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_update_goal_clicked(self):
        global id_project, list_goals

        description = self.ui.lineedit_saf_goal.text()
        if len(description) > 0:
            pos = self.ui.list_saf_goals.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            goal = list_goals[pos]
            goal.description = description
            goal.edited_date = current_date
            DB_Goals.update_goal(goal)

            self.load_goals()
            self.ui.lineedit_saf_goal.setText("")
            self.ui.button_saf_new_goal.setEnabled(True)
            self.ui.button_saf_update_goal.setEnabled(False)
            self.ui.button_saf_delete_goal.setEnabled(False)
            self.ui.button_saf_cancel_goal.setEnabled(False)
            self.ui.label_saf_goal_position.setText("G-")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_delete_goal_clicked(self):
        pos = self.ui.list_saf_goals.currentRow()
        goal = list_goals[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register G-" + str(goal.id_goal) + "?")
        msgBox.setWindowTitle("Delete Goal")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Goals.delete_goal(goal)
            self.load_goals()
            self.ui.lineedit_saf_goal.setText("")
            self.ui.button_saf_new_goal.setEnabled(True)
            self.ui.button_saf_update_goal.setEnabled(False)
            self.ui.button_saf_delete_goal.setEnabled(False)
            self.ui.button_saf_cancel_goal.setEnabled(False)
            self.ui.label_saf_goal_position.setText("G-")

    def on_button_saf_cancel_goal_clicked(self):
        self.ui.button_saf_new_goal.setEnabled(True)
        self.ui.button_saf_update_goal.setEnabled(False)
        self.ui.button_saf_delete_goal.setEnabled(False)
        self.ui.button_saf_cancel_goal.setEnabled(False)
        self.ui.label_saf_goal_position.setText("G-")
        self.ui.lineedit_saf_goal.setText("")
        item = self.ui.list_saf_goals.currentItem()
        item.setSelected(False)

    def load_assumptions(self):
        # Assumptions information
        global list_assumptions, id_project
        self.ui.list_saf_assumptions.clear()
        list_assumptions = DB_Assumptions.select_all_assumptions_by_project(id_project)
        for pos in range(len(list_assumptions)):
            self.ui.list_saf_assumptions.addItem(
                "A-" + str(list_assumptions[pos].id_assumption) + ": " + list_assumptions[pos].description)

    def on_list_saf_assumptions_clicked(self):
        item = self.ui.list_saf_assumptions.currentItem()
        pos = self.ui.list_saf_assumptions.currentRow()

        self.ui.button_saf_new_assumption.setEnabled(False)
        self.ui.button_saf_update_assumption.setEnabled(True)
        self.ui.button_saf_delete_assumption.setEnabled(True)
        self.ui.button_saf_cancel_assumption.setEnabled(True)

        global list_assumptions
        self.ui.label_saf_assumption_position.setText("A-" + str(list_assumptions[pos].id_assumption))
        self.ui.lineedit_saf_assumption.setText(list_assumptions[pos].description)

    def on_button_saf_new_assumption_clicked(self):
        global id_project, list_assumptions

        description = self.ui.lineedit_saf_assumption.text()
        if len(description) > 0:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_assumption = len(list_assumptions) + 1
            assump = Assumptions(0, id_project, pos_assumption, description, current_date, current_date)
            DB_Assumptions.insert_to_assumptions(assump)

            self.load_assumptions()
            self.ui.lineedit_saf_assumption.setText("")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_update_assumption_clicked(self):
        global id_project, list_assumptions

        description = self.ui.lineedit_saf_assumption.text()
        if len(description) > 0:
            pos = self.ui.list_saf_assumptions.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            assumption = list_assumptions[pos]
            assumption.description = description
            assumption.edited_date = current_date
            DB_Assumptions.update_assumption(assumption)

            self.load_assumptions()
            self.ui.lineedit_saf_assumption.setText("")
            self.ui.button_saf_new_assumption.setEnabled(True)
            self.ui.button_saf_update_assumption.setEnabled(False)
            self.ui.button_saf_delete_assumption.setEnabled(False)
            self.ui.button_saf_cancel_assumption.setEnabled(False)
            self.ui.label_saf_assumption_position.setText("A-")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_delete_assumption_clicked(self):
        pos = self.ui.list_saf_assumptions.currentRow()
        assumption = list_assumptions[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register A-" + str(assumption.id_assumption) + "?")
        msgBox.setWindowTitle("Delete Assumption")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Assumptions.delete_assumption(assumption)
            self.load_assumptions()
            self.ui.lineedit_saf_assumption.setText("")
            self.ui.button_saf_new_assumption.setEnabled(True)
            self.ui.button_saf_update_assumption.setEnabled(False)
            self.ui.button_saf_delete_assumption.setEnabled(False)
            self.ui.button_saf_cancel_assumption.setEnabled(False)
            self.ui.label_saf_assumption_position.setText("A-")

    def on_button_saf_cancel_assumption_clicked(self):
        self.ui.button_saf_new_assumption.setEnabled(True)
        self.ui.button_saf_update_assumption.setEnabled(False)
        self.ui.button_saf_delete_assumption.setEnabled(False)
        self.ui.button_saf_cancel_assumption.setEnabled(False)
        self.ui.label_saf_assumption_position.setText("A-")
        self.ui.lineedit_saf_assumption.setText("")
        item = self.ui.list_saf_assumptions.currentItem()
        item.setSelected(False)
        self.ui.lineedit_saf_assumption.setFocusPolicy(Qt.StrongFocus)

    def load_losses(self):
        # Losses information
        global list_losses, id_project
        self.ui.list_saf_losses.clear()
        list_losses = DB_Losses.select_all_losses_by_project(id_project)
        for pos in range(len(list_losses)):
            self.ui.list_saf_losses.addItem("L-" + str(list_losses[pos].id_loss) + ": " + list_losses[pos].description)

        self.load_hazards_losses()

    def on_list_saf_losses_clicked(self):
        item = self.ui.list_saf_losses.currentItem()
        pos = self.ui.list_saf_losses.currentRow()

        self.ui.button_saf_new_loss.setEnabled(False)
        self.ui.button_saf_update_loss.setEnabled(True)
        self.ui.button_saf_delete_loss.setEnabled(True)
        self.ui.button_saf_cancel_loss.setEnabled(True)

        global list_losses
        self.ui.label_saf_loss_position.setText("L-" + str(list_losses[pos].id_loss))
        self.ui.lineedit_saf_loss.setText(list_losses[pos].description)

    def on_button_saf_new_loss_clicked(self):
        global id_project, list_losses

        description = self.ui.lineedit_saf_loss.text()
        if len(description) > 0:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_loss = len(list_losses) + 1
            loss = Loss(0, id_project, pos_loss, description, current_date, current_date)
            DB_Losses.insert_to_losses(loss)

            self.load_losses()
            self.ui.lineedit_saf_loss.setText("")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_update_loss_clicked(self):
        global id_project, list_losses

        description = self.ui.lineedit_saf_loss.text()
        if len(description) > 0:
            pos = self.ui.list_saf_losses.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            loss = list_losses[pos]
            loss.description = description
            loss.edited_date = current_date
            DB_Losses.update_loss(loss)

            self.load_losses()
            self.ui.lineedit_saf_loss.setText("")
            self.ui.button_saf_new_loss.setEnabled(True)
            self.ui.button_saf_update_loss.setEnabled(False)
            self.ui.button_saf_delete_loss.setEnabled(False)
            self.ui.button_saf_cancel_loss.setEnabled(False)
            self.ui.label_saf_loss_position.setText("L-")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_delete_loss_clicked(self):
        pos = self.ui.list_saf_losses.currentRow()
        loss = list_losses[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register L-" + str(loss.id_loss) + "?")
        msgBox.setWindowTitle("Delete Loss")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Losses.delete_loss(loss)
            self.load_losses()
            self.ui.lineedit_saf_loss.setText("")
            self.ui.button_saf_new_loss.setEnabled(True)
            self.ui.button_saf_update_loss.setEnabled(False)
            self.ui.button_saf_delete_loss.setEnabled(False)
            self.ui.button_saf_cancel_loss.setEnabled(False)
            self.ui.label_saf_loss_position.setText("L-")

    def on_button_saf_cancel_loss_clicked(self):
        self.ui.button_saf_new_loss.setEnabled(True)
        self.ui.button_saf_update_loss.setEnabled(False)
        self.ui.button_saf_delete_loss.setEnabled(False)
        self.ui.button_saf_cancel_loss.setEnabled(False)
        self.ui.label_saf_loss_position.setText("L-")
        self.ui.lineedit_saf_loss.setText("")
        item = self.ui.list_saf_losses.currentItem()
        item.setSelected(False)

    def load_hazards(self):
        # Hazards information
        global list_hazards, id_project
        self.ui.list_saf_hazards.clear()
        list_hazards = DB_Hazards.select_all_hazards_by_project(id_project)

        count = 1
        for pos in range(len(list_hazards)):
            text = ""
            for loss in list_hazards[pos].list_of_loss:
                text += "[L-" + str(loss.id_loss_screen) + "] "

            self.ui.list_saf_hazards.addItem("H-" + str(list_hazards[pos].id_hazard) + ": " + list_hazards[pos].description + " " + text)

        self.load_hazards_losses()
        self.load_constraints_hazards()

    def load_hazards_losses(self):
        global list_losses, list_hazards
        self.ui.list_hazards_losses.clear()
        pos = self.ui.list_saf_hazards.currentRow()

        for pos_los in range(len(list_losses)):
            self.ui.list_hazards_losses.addItem(
                "L-" + str(list_losses[pos_los].id_loss) + ": " + list_losses[pos_los].description)

            if pos > 0:
                for l in list_hazards[pos].list_of_loss:
                    if l.id_loss == list_losses[pos_los].id:
                        self.ui.list_hazards_losses.item(pos_los).setSelected(True)

    def on_list_saf_hazards_clicked(self):
        global list_hazards, list_losses, id_project
        pos = self.ui.list_saf_hazards.currentRow()

        if pos < 0:
            return

        self.ui.button_saf_new_hazard.setEnabled(False)
        self.ui.button_saf_update_hazard.setEnabled(True)
        self.ui.button_saf_delete_hazard.setEnabled(True)
        self.ui.button_saf_cancel_hazard.setEnabled(True)

        self.ui.label_saf_hazard_position.setText("H-" + str(list_hazards[pos].id_hazard))
        self.ui.lineedit_saf_hazard.setText(list_hazards[pos].description)
        self.ui.list_hazards_losses.clear()

        for pos_los in range(len(list_losses)):
            item = QtWidgets.QListWidgetItem(
                "L-" + str(list_losses[pos_los].id_loss) + ": " + list_losses[pos_los].description)
            self.ui.list_hazards_losses.addItem(item)
            for l in list_hazards[pos].list_of_loss:
                if l.id_loss == list_losses[pos_los].id:
                    self.ui.list_hazards_losses.item(pos_los).setSelected(True)

    def on_button_saf_new_hazard_clicked(self):
        global id_project, list_hazards

        description = self.ui.lineedit_saf_hazard.text()

        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_hazards_losses.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Loss")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_hazard = len(list_hazards) + 1
            hazard = Hazard(0, id_project, pos_hazard, description, current_date, current_date)
            selected_losses = []
            for item in self.ui.list_hazards_losses.selectedItems():
                loss_id = list_losses[self.ui.list_hazards_losses.row(item)].id
                selected_losses.append(Hazard_Loss(0, id_project, 0, loss_id))

            hazard.list_of_loss = selected_losses
            DB_Hazards.insert_to_hazards(hazard)

            self.load_hazards()
            self.ui.lineedit_saf_hazard.setText("")

    def on_button_saf_update_hazard_clicked(self):
        global id_project, list_hazards

        description = self.ui.lineedit_saf_hazard.text()
        if len(description) <= 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_hazards_losses.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Loss")
        else:
            pos = self.ui.list_saf_hazards.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            hazard = list_hazards[pos]
            hazard.description = description
            hazard.edited_date = current_date

            selected_losses = []
            for item in self.ui.list_hazards_losses.selectedItems():
                loss_id = list_losses[self.ui.list_hazards_losses.row(item)].id
                selected_losses.append(Hazard_Loss(hazard.id, hazard.id_project, hazard.id, loss_id))

            hazard.list_of_loss = selected_losses
            DB_Hazards.update_hazard(hazard)

            self.clear_haz()

            self.load_hazards()
            self.load_hazards_losses()

            self.clear_haz()

    def clear_haz(self):
        self.ui.lineedit_saf_hazard.setText("")
        self.ui.list_saf_hazards.clearSelection()
        self.ui.list_saf_hazards.selectionModel().clear()
        self.ui.list_hazards_losses.clearSelection()
        self.ui.list_hazards_losses.selectionModel().clear()
        self.ui.label_saf_hazard_position.setText("H-")

        self.ui.button_saf_new_hazard.setEnabled(True)
        self.ui.button_saf_update_hazard.setEnabled(False)
        self.ui.button_saf_delete_hazard.setEnabled(False)
        self.ui.button_saf_cancel_hazard.setEnabled(False)

    def on_button_saf_delete_hazard_clicked(self):
        pos = self.ui.list_saf_hazards.currentRow()
        hazard = list_hazards[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register H-" + str(hazard.id_hazard) + "?")
        msgBox.setWindowTitle("Delete Hazard")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Hazards.delete_hazard(hazard)
            self.clear_haz()
            self.load_hazards()
            self.clear_haz()

    def on_button_saf_cancel_hazard_clicked(self):
        self.ui.button_saf_new_hazard.setEnabled(True)
        self.ui.button_saf_update_hazard.setEnabled(False)
        self.ui.button_saf_delete_hazard.setEnabled(False)
        self.ui.button_saf_cancel_hazard.setEnabled(False)
        self.ui.label_saf_hazard_position.setText("H-")
        self.ui.lineedit_saf_hazard.setText("")
        self.ui.list_saf_hazards.selectionModel().clear()
        self.ui.list_saf_hazards.clearSelection()
        self.load_hazards_losses()

    def load_constraints(self):
        # Constraints information
        global list_constraints, id_project
        self.ui.list_saf_constraints.clear()
        list_constraints = DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project)
        for pos in range(len(list_constraints)):
            text = ""
            for haz in list_constraints[pos].list_of_hazards:
                text += "[H-" + str(haz.id_haz_screen) + "] "

            self.ui.list_saf_constraints.addItem(
                "SSC-" + str(list_constraints[pos].id_safety_constraint) + ": " + list_constraints[
                    pos].description + " " + text)

        self.load_constraints_hazards()

    def load_constraints_hazards(self):
        global list_hazards, list_constraints
        pos = self.ui.list_saf_constraints.currentRow()
        self.ui.list_constraints_hazards.clear()
        for pos_cons in range(len(list_hazards)):
            self.ui.list_constraints_hazards.addItem(
                "H-" + str(list_hazards[pos_cons].id_hazard) + ": " + list_hazards[pos_cons].description)
            if pos > 0:
                for haz in list_constraints[pos].list_of_hazards:
                    if haz.id_hazard == list_hazards[pos_cons].id:
                        self.ui.list_constraints_hazards.item(pos_cons).setSelected(True)

    def on_list_saf_constraints_clicked(self):
        pos = self.ui.list_saf_constraints.currentRow()

        if pos < 0:
            return

        self.ui.button_saf_new_constraint.setEnabled(False)
        self.ui.button_saf_update_constraint.setEnabled(True)
        self.ui.button_saf_delete_constraint.setEnabled(True)
        self.ui.button_saf_cancel_constraint.setEnabled(True)

        global list_constraints, list_hazards
        self.ui.label_saf_constraint_position.setText("SSC-" + str(list_constraints[pos].id_safety_constraint))
        self.ui.lineedit_saf_constraint.setText(list_constraints[pos].description)
        self.ui.list_constraints_hazards.clear()

        for pos_cons in range(len(list_hazards)):
            item = QtWidgets.QListWidgetItem(
                "H-" + str(list_hazards[pos_cons].id_hazard) + ": " + list_hazards[pos_cons].description)
            self.ui.list_constraints_hazards.addItem(item)
            for haz in list_constraints[pos].list_of_hazards:
                if haz.id_hazard == list_hazards[pos_cons].id:
                    self.ui.list_constraints_hazards.item(pos_cons).setSelected(True)

    def on_button_saf_new_constraint_clicked(self):
        global id_project, list_constraints, list_hazards

        description = self.ui.lineedit_saf_constraint.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_constraints_hazards.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Hazard")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_constraint = len(list_constraints) + 1
            constraint = Safety_Constraint(0, id_project, pos_constraint, description, current_date, current_date)

            selected_haz = []
            for item in self.ui.list_constraints_hazards.selectedItems():
                haz_id = list_hazards[self.ui.list_constraints_hazards.row(item)].id
                selected_haz.append(Safety_Constraint_Hazard(0, id_project, constraint.id, haz_id))

            constraint.list_of_hazards = selected_haz
            DB_Safety_Constraints.insert_to_safety_constraints(constraint)

            self.load_constraints()
            self.ui.lineedit_saf_constraint.setText("")

    def on_button_saf_update_constraint_clicked(self):
        global id_project, list_constraints

        description = self.ui.lineedit_saf_constraint.text()
        if len(description) <= 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_constraints_hazards.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Hazard")
        else:
            pos = self.ui.list_saf_constraints.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            constraint = list_constraints[pos]
            constraint.description = description
            constraint.edited_date = current_date

            selected_haz = []
            for item in self.ui.list_constraints_hazards.selectedItems():
                haz_id = list_hazards[self.ui.list_constraints_hazards.row(item)].id
                selected_haz.append(Safety_Constraint_Hazard(0, id_project, constraint.id, haz_id))

            constraint.list_of_hazards = selected_haz

            DB_Safety_Constraints.update_safety_constraints(constraint)

            self.clear_sc()
            self.load_constraints()
            self.clear_sc()

    def clear_sc(self):
        self.ui.lineedit_saf_constraint.setText("")
        self.ui.list_saf_constraints.clearSelection()
        self.ui.list_saf_constraints.selectionModel().clear()
        self.ui.list_constraints_hazards.clearSelection()
        self.ui.list_constraints_hazards.selectionModel().clear()
        self.ui.label_saf_constraint_position.setText("SSC-")

        self.ui.button_saf_new_constraint.setEnabled(True)
        self.ui.button_saf_update_constraint.setEnabled(False)
        self.ui.button_saf_delete_constraint.setEnabled(False)
        self.ui.button_saf_cancel_constraint.setEnabled(False)

    def on_button_saf_delete_constraint_clicked(self):
        pos = self.ui.list_saf_constraints.currentRow()
        constraint = list_constraints[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register SSC-" + str(constraint.id_safety_constraint) + "?")
        msgBox.setWindowTitle("Delete Safety Constraint")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Safety_Constraints.delete_safety_constraints(constraint)
            self.clear_sc()
            self.load_constraints()
            self.clear_sc()

    def on_button_saf_cancel_constraint_clicked(self):
        self.ui.button_saf_new_constraint.setEnabled(True)
        self.ui.button_saf_update_constraint.setEnabled(False)
        self.ui.button_saf_delete_constraint.setEnabled(False)
        self.ui.button_saf_cancel_constraint.setEnabled(False)
        self.ui.label_saf_constraint_position.setText("SSC-")
        self.ui.lineedit_saf_constraint.setText("")
        self.ui.list_saf_constraints.selectionModel().clear()
        self.ui.list_saf_constraints.clearSelection()
        self.ui.list_constraints_hazards.selectionModel().clear()
        self.ui.list_constraints_hazards.clearSelection()
        self.load_constraints_hazards()
    # ----- Functions STPA 1 Step -----

def showdialog(title, message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok)

    returnValue = msgBox.exec()
    # if returnValue == QMessageBox.Ok:
    #     print('OK clicked')

def thread_function():
    # start reasoner
    # print(onto.base_iri)
    # time.sleep(1)
    sync_reasoner(infer_property_values=True)
    loadind_screen.stopAnimation()
    main_win.active_tab()
    main_win.load_projects()
# def get_d_day():
#     import datetime
#     return datetime.datetime(2021, 6, 29, 0, 0, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    DB.create_all_tables()
    main_win = MainWindow()
    main_win.show()
    loadind_screen = LoadingScreen()
    x = threading.Thread(target=thread_function)
    x.start()

    sys.exit(app.exec_())

    # try:
    #     app = QApplication(sys.argv)
    #
    #     today = datetime.now()
    #     d_day = get_d_day()
    #     t_day = d_day - today
    #
    #     days = t_day.days
    #
    #     if days > 15 or days < -15:
    #         if os.path.exists(Constant.IMAGE_PATH):
    #             os.remove(Constant.IMAGE_PATH)
    #         if os.path.exists(Constant.BIN_PATH):
    #             os.remove(Constant.BIN_PATH)
    #     else:
    #         DB.create_all_tables()
    #         main_win = MainWindow()
    #         main_win.show()
    #         loadind_screen = LoadingScreen()
    #         x = threading.Thread(target=thread_function)
    #         x.start()
    #
    #     sys.exit(app.exec_())
    # except NameError as e:
    #     print(e)

# -------------------------------------------------------
# owlready2.JAVA_EXE = Constant.JAVA_PATH
# onto = get_ontology(Constant.ONTOLOGY_PATH).load(reload = True)
# print(onto.base_iri)
#
# # start reasoner
# print("Syncing Reasoner... Wait...")
# start_r_time = time.time()
# sync_reasoner(infer_property_values = True)
# print("Reasoner synced (" + str(time.time() - start_r_time) + " seconds)... Start Ontology analysis...")
#
#
# Safety_tools_new.get_safety_analysis(onto, 1, 1)
#
#
# print("Reading ontology... Wait...")
# start_o_time = time.time()
# safety_requirements_list = Safety_tools.get_safety_requirement_analysis(onto, 1)
# security_requirements_list = Security_tools.get_security_requirement_analysis(onto)
# print("Ontology read (" + str(time.time() - start_o_time) + " seconds)... Start Safety and Security analysis...")
#
# print("Comparing results... Wait...")
# start_c_time = time.time()
# General_tools.compare_and_generate_safety_security(safety_requirements_list, security_requirements_list)
# print("Results compared (" + str(time.time() - start_c_time) + " seconds)... Finish!")
# -------------------------------------------------------


# -------------------------------------------------------
# name = General_tools.find_individuals_of_class(onto, "Saf_UCA")
#
# for obj in name.class_parent.is_a:
#     if isinstance(obj, Restriction):
#         print(obj.property.name)
#         print(obj.value.name)
# -------------------------------------------------------
