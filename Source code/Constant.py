# Ontology complete path
# BIN_PATH = "PyQt5\\Qt5\\bin\\libOSA-5.bin"
# BIN_PATH = "Ontologies\\safety_security_10.owl"
BIN_PATH = "Ontologies\\safety_security_10_dev_only.owl"
ANALYSIS_PATH = ".\\analysis\\"


IMAGE_STPA_FULL_PATH = ".\Ontologies\safety_ontology.png"


IMAGE_STPA_ONE_PATH = ".\Ontologies\step_one_stpa.png"
IMAGE_STPA_TWO_PATH = ".\Ontologies\step_two_stpa.png"
IMAGE_STPA_THREE_PATH = ".\Ontologies\step_three_stpa.png"
IMAGE_STPA_FOUR_PATH = ".\Ontologies\step_four_stpa.png"
IMAGE_STRIDE_FULL_PATH = ".\Ontologies\security_ontology.png"
IMAGE_STRIDE_DFD_MAP_PATH = ".\Ontologies\security_dfd_map.png"
IMAGE_STRIDE_SECURITY_PATH = ".\Ontologies\security_stride.png"
FILES_REPO = "Files"
DB_FILE = "Database/Ontology_DB.db"  # Database path
GIF_LOADING_PATH = "Images/Loading_Gear_400px.gif"
DEFAULT_IMAGE_PATH = "Images/image.png"
IMAGE_STPA_LOSS = "Images/new_loss_scenarios_division.png"
PATH_REPORT = "Reports\\"
VERSION = "2.0.2"

# Java complete path
#JAVA_PATH = "C:\\Program Files\\Java\\jre1.8.0_281\\bin\\java.exe"

# RESERVED words
SAFETY = "SAFETY"
SECURITY = "SECURITY"
PRIVACY = "PRIVACY"
RELIABILITY = "RELIABILITY"
PERFORMANCE = "PERFORMANCE"

provided_in_wrong_order = 1
provided_too_early = 2
provided_too_late = 3
not_provided = 4
provided = 5
applied_too_long = 6
stopped_too_son = 7

# Database data
DB_ID_CONTROLLER = 1
DB_ID_ACTUATOR = 2
DB_ID_CP = 3
DB_ID_SENSOR = 4
DB_ID_INPUT = 5
DB_ID_OUTPUT = 6
DB_ID_EXT_INFORMATION = 7
DB_ID_ALGORITHM = 8
DB_ID_PROCESS_MODEL = 9
DB_ID_ENV_DISTURBANCES = 10
DB_ID_HLC = 11

# Database UCA Type
DB_ID_UT_PWO = 1
DB_ID_UT_PTE = 2
DB_ID_UT_PTL = 3
DB_ID_UT_NP = 4
DB_ID_UT_P = 5
DB_ID_UT_ATL = 6
DB_ID_UT_STS = 7

# Database Control Action
DB_ID_ACT_CACA = 1
DB_ID_ACT_CACCP = 2
DB_ID_ACT_FCP = 3
DB_ID_ACT_CAHC = 4
DB_ID_ACT_CAHCP = 5
DB_ID_ACT_FCH = 6


# Control structure analysis variables
ACTUATOR = "Actuator"
ALGORITHM = "Algorithm"
CONTEXT = "Context"
CONTROL_ACTION = "Control_action"
CONTROL_ACTION_ACTUATOR = "Control_action_actuator"
CONTROL_ACTION_CP = "Control_action_CP"
CONTROL_ACTION_HLC_CONTROLLER = "Control_action_HLC_controller"
CONTROL_ACTION_HLC_CP = "Control_action_HLC_CP"
CONTROLLED_PROCESS = "CP"
CONTROLLED_PROCESS_full_name = "Controlled_process_CP"
CONTROLLER = "Controller"
CONTROLLER_CONSTANTS = "Controller_constraints"
EXTERNAL_INFORMATION = "External-information"
EXTERNAL_INFORMATION_SENT = "External-information-sent"
EXTERNAL_INFORMATION_RECEIVED = "External-information-received"
ENVIRONMENTAL_DISTURBANCES = "Environmental_disturbances"
FEEDBACK_OF_CONTROLLER = "Feedback_of_controller"
FEEDBACK_OF_CP = "Feedback_of_CP"
HIGH_LEVEL_CONTROLLER = "HLC"
INPUT = "Input"
LINK = "Link"
LINK_ACTUATOR_CP = "Link_actuator_CP"
LINK_CONTROLLER_ACTUATOR = "Link_controller_actuator"
LINK_CONTROLLER_CP = "Link_controller_CP"
LINK_CONTROLLER_EXT_INF = "Link_controller_external-information"
LINK_CONTROLLER_HLC = "Link_controller_HLC"
LINK_CP_CONTROLLER = "Link_CP_controller"
LINK_CP_HLC = "Link_CP_HLC"
LINK_CP_SENSOR = "Link_CP_sensor"
LINK_EXT_INF_CONTROLLER = "Link_external-information_controller"
LINK_HLC_CONTROLLER = "Link_HLC_controller"
LINK_HLC_CP = "Link_HLC_CP"
LINK_SENSOR_CONTROLLER = "Link_sensor_controller"
LINK_SENSOR_HLC = "Link_sensor_HLC"
OUTPUT = "Output"
PROCESS_MODEL = "Process_model"
PROCESS_MODEL_full_name = "Process Model"
SENSOR = "Sensor"
VARIABLES = "Variables"
VALUES = "Values"


# Safety analysis variables
CAUSAL_FACTOR = "Saf_Causal_factor"
CAUSAL_FACTOR_A = "Saf_Causal_factor_A"
CAUSAL_FACTOR_B = "Saf_Causal_factor_B"
LOSS_MISHAP = "Saf_Loss_mishap"
LOSS_SCENARIO = "Saf_Loss_scenario"
LOSS_SCENARIO_A = "Saf_Loss_scenario_A"
LOSS_SCENARIO_B = "Saf_Loss_scenario_B"
SAFETY_REQUIREMENT = "Saf_Safety_recommendation"
TIME = "Saf_Time"
UCA = "Saf_UCA"
UCA_TYPE = "Saf_UCA_type"
UCA_RULE = "rule"
UCA_CELL = "cell"
HAZARDS = "Saf_System_level_hazards"

STPA_UNSAFE_CONTROLLER_BEHAVIOR = "Unsafe controller behavior"
STPA_INADEQUATE_FEEDBACK = "Causes of inadequate feedback/information"
STPA_CONTROL_PATH = "Control path"
STPA_OTHER_FACTORS = "Other factors related to the controlled process"


###### Security ######
DB_ID_SPOOFING = 1
DB_ID_TAMPERING = 2
DB_ID_REPUDIATION = 3
DB_ID_INFORMATION_DISCLOSURE = 4
DB_ID_DENIAL_OF_SERVICE = 5
DB_ID_ELEVATION_OF_PRIVILEGE = 6

DB_ID_EXTERNAL_ENTITY = 1
DB_ID_DATA_FLOW = 2
DB_ID_DATA_STORE = 3
DB_ID_PROCESS = 4

DB_ID_HIGH = 1
DB_ID_MEDIUM = 2
DB_ID_LOW = 3

DB_NAME_SPOOFING = "Spoofing"
DB_NAME_TAMPERING = "Tampering"
DB_NAME_REPUDIATION = "Repudiation"
DB_NAME_INFORMATION_DISCLOSURE = "Information disclosure"
DB_NAME_DENIAL_OF_SERVICE = "Denial of service"
DB_NAME_ELEVATION_OF_PRIVILEGE = "Elevation of privilege"

SEC_IS_EXTERNAL_ENTITY_NAME = "External entity"
SEC_IS_DATA_FLOW_NAME = "Data flow"
SEC_IS_DATA_STORE_NAME = "Data store"
SEC_IS_PROCESS_NAME = "Process"

DB_NAME_HIGH = "High"
DB_NAME_MEDIUM = "Medium"
DB_NAME_LOW = "Low"


# Security analysis variables
SEC_SECURITY_REQUIREMENT = "Sec_Security_requirement"
SEC_SPOOFING = "Sec_Spoofing"
SEC_TAMPERING = "Sec_Tampering"
SEC_REPUDIATION = "Sec_Repudiation"
SEC_INFORMATION_DISCLOSURE = "Sec_Information_disclosure"
SEC_DENIAL_OF_SERVICE = "Sec_Denial_of_service"
SEC_ELEVATION_OF_PRIVILEGE = "Sec_Elevation_of_privilege"

SEC_SPOOFING_CONTROL = "Sec_Spoofing_control"
SEC_TAMPERING_CONTROL = "Sec_Tampering_control"
SEC_REPUDIATION_CONTROL = "Sec_Repudiation_control"
SEC_INFORMATION_DISCLOSURE_CONTROL = "Sec_Information_disclosure_control"
SEC_DENIAL_OF_SERVICE_CONTROL = "Sec_Denial_of_service_control"
SEC_ELEVATION_OF_PRIVILEGE_CONTROL = "Sec_Elevation_of_privilege_control"

SEC_CAUSAL_FACTOR = "Sec_Causal_factor"
SEC_SPOOFING_CAUSAL_FACTOR = "Sec_Spoofing_causal_factor"
SEC_TAMPERING_CAUSAL_FACTOR = "Sec_Tampering_causal_factor"
SEC_REPUDIATION_CAUSAL_FACTOR = "Sec_Repudiation_causal_factor"
SEC_INFORMATION_DISCLOSURE_CAUSAL_FACTOR = "Sec_Information_disclosure_causal_factor"
SEC_DENIAL_OF_SERVICE_CAUSAL_FACTOR = "Sec_Denial_of_service_causal_factor"
SEC_ELEVATION_OF_PRIVILEGE_CAUSAL_FACTOR = "Sec_Elevation_of_privilege_causal_factor"

SEC_SPOOFING_OBJECT = "sec_unauthenticated_access_spoofing"
SEC_TAMPERING_OBJECT = "sec_exposed_tampering"
SEC_REPUDIATION_OBJECT = "sec_repudiation_behaviour"
SEC_INFORMATION_DISCLOSURE_OBJECT = "sec_unprotected_id"
SEC_DENIAL_OF_SERVICE_OBJECT = "sec_not_available_dos"
SEC_ELEVATION_OF_PRIVILEGE_OBJECT = "sec_unauthorized_access_eop"
SEC_IS_EXTERNAL_ENTITY_OBJECT = "sec_is_external_entity"
SEC_IS_PROCESS_OBJECT = "sec_is_process"
SEC_IS_DATA_STORE_OBJECT = "sec_is_data_store"
SEC_IS_DATA_FLOW_OBJECT = "sec_is_data_flow"

SEC_SPOOFING_REQUIREMENT = "Sec_Spoofing_requirement"
SEC_TAMPERING_REQUIREMENT = "Sec_Tampering_requirement"
SEC_REPUDIATION_REQUIREMENT = "Sec_Repudiation_requirement"
SEC_INFORMATION_DISCLOSURE_REQUIREMENT = "Sec_Information_disclosure_requirement"
SEC_DENIAL_OF_SERVICE_REQUIREMENT = "Sec_Denial_of_service_requirement"
SEC_ELEVATION_OF_PRIVILEGE_REQUIREMENT = "Sec_Elevation_of_privilege_requirement"
SEC_IS_EXTERNAL_ENTITY = "Sec_External_entity"
SEC_IS_PROCESS = "Sec_Process"
SEC_IS_DATA_STORE = "Sec_Data_store"
SEC_IS_DATA_FLOW = "Sec_Data_flow"


# ---------------- Conflicts ----------------
SAF_CONFLICT_REINFORCEMENT_RECOMMENDATION = "Saf_conflict_reinforcement_recommendation"
SEC_CONFLICT_REINFORCEMENT_RECOMMENDATION = "Sec_conflict_reinforcement_mechanism"
IS_SAF_SEC_CONFLICT = "is_saf_sec_conflict"
IS_SAF_SEC_REINFORCEMENT = "is_saf_sec_reinforcement"
IS_SEC_SAF_CONFLICT = "is_sec_saf_conflict"
IS_SEC_SAF_REINFORCEMENT = "is_sec_saf_reinforcement"

MUST = " must "
MUST_HAVE = " must have "
SHALL = " shall "
SHALL_HAVE = " shall have "
WHEN = " when "
BEFORE = " before "
AFTER = " after "
WHILE = " while "
FOR = " for "

# ---------------- Conflicts ----------------

# ---------------- Performance ----------------

DB_ID_COMMUNICATION_TIME = 1
DB_ID_LATENCY = 2
DB_ID_RESOURCE_UTILIZATION = 3
DB_ID_RESPONSE_TIME = 4
DB_ID_SCALABILITY = 5
DB_ID_THROUGHPUT = 6
DB_ID_WORKLOAD = 7

DB_NAME_COMMUNICATION_TIME = "Communication time"
DB_NAME_LATENCY = "Latency"
DB_NAME_RESOURCE_UTILIZATION = "Resource utilization"
DB_NAME_RESPONSE_TIME = "Response time"
DB_NAME_SCALABILITY = "Scalability"
DB_NAME_THROUGHPUT = "Throughput"
DB_NAME_WORKLOAD = "Workload"

PEF_COMMUNICATION_TIME = "Pef_Communication_time_recommendation"
PEF_LATENCY = "Pef_Latency_recommendation"
PEF_RESOURCE_UTILIZATION = "Pef_Resource_utilization_recommendation"
PEF_RESPONSE_TIME = "Pef_Response_time_recommendation"
PEF_SCALABILITY = "Pef_Scalability_recommendation"
PEF_THROUGHPUT = "Pef_Throughput_recommendation"
PEF_WORKLOAD = "Pef_Workload_recommendation"

DB_ID_APPLICATION = 1
DB_ID_INTERFACE_I_O = 2
DB_ID_MEMORY = 3
DB_ID_OPERATING_SYSTEM = 4
DB_ID_PHYSICAL_LINK = 5
DB_ID_PROCESSOR = 6
DB_ID_STORAGE = 7

DB_NAME_APPLICATION = "Application"
DB_NAME_INTERFACE_I_O = "Interface I/O"
DB_NAME_MEMORY = "Memory"
DB_NAME_OPERATING_SYSTEM = "Operating system"
DB_NAME_PHYSICAL_LINK = "Physical link"
DB_NAME_PROCESSOR = "Processor"
DB_NAME_STORAGE = "Storage"

PEF_APPLICATION = "Pef_Application"
PEF_INTERFACE_I_O = "Pef_Interface_I/O"
PEF_MEMORY = "Pef_Memory"
PEF_OPERATING_SYSTEM = "Pef_Operating_system"
PEF_PHYSICAL_LINK = "Pef_Physical_link"
PEF_PROCESSOR = "Pef_Processor"
PEF_STORAGE = "Pef_Storage"

PEF_COMPOSED_BY = "pef_composed_by"
PEF_PRESENT_IN = "pef_present_in"

PEF_PERFORMANCE_RECOMMENDATION = "Pef_Performance_recommendation"
# ---------------- Performance ----------------


VAR_ERR = "VAR_ERR"
VAL_ERR = "VAL_ERR"

DATETIME_MASK = "%d/%m/%Y %H:%M:%S"
DATETIME_MASK_FILE = "%d-%m-%Y_%H-%M-%S"
DATETIME_MASK_FILE_COPY = "%Y_%m_%d_%H_%M_%S"