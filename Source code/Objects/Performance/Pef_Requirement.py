class Pef_Resource:

    def __init__(self, id = 0, name = "", onto_name = ""):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.name = name  # TEXT NOT NULL
        self.onto_name = onto_name  # TEXT NOT NULL


class Saf_Pef_UCA:

    def __init__(self, id, description):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.description = description  # TEXT NOT NULL


class Pef_Saf_Resource:

    def __init__(self, id = 0, requirement = "", id_saf_requirement = 0, id_component = 0, id_resource = 0, id_project = 0, comp_name = "", res_name = ""):
        self.id = id
        self.requirement = requirement
        self.id_saf_requirement = id_saf_requirement
        self.id_component = id_component
        self.id_resource = id_resource
        self.id_project = id_project
        self.comp_name = comp_name
        self.res_name = res_name


class Sec_Pef_UCA:

    def __init__(self, id, name):
        self.id = id  # INTEGER PRIMARY KEY AUTOINCREMENT
        self.name = name  # TEXT NOT NULL


class Pef_Sec_Resource:

    def __init__(self, id = 0, requirement = "", id_sec_requirement = 0, id_component = 0, id_resource = 0, id_project = 0, comp_name = "", res_name = ""):
        self.id = id
        self.requirement = requirement
        self.id_sec_requirement = id_sec_requirement
        self.id_component = id_component
        self.id_resource = id_resource
        self.id_project = id_project
        self.comp_name = comp_name
        self.res_name = res_name


class Pef_Bus_Resource:

    def __init__(self, id = 0, requirement = "", id_bus_requirement = 0, id_component = 0, id_resource = 0, id_project = 0, comp_name = "", res_name = ""):
        self.id = id
        self.requirement = requirement
        self.id_bus_requirement = id_bus_requirement
        self.id_component = id_component
        self.id_resource = id_resource
        self.id_project = id_project
        self.comp_name = comp_name
        self.res_name = res_name


class Pef_Req_Resource:

    def __init__(self, id = 0, requirement = "", id_component = 0, id_resource = 0, id_project = 0, comp_name = "", res_name = ""):
        self.id = id
        self.requirement = requirement
        self.id_component = id_component
        self.id_resource = id_resource
        self.id_project = id_project
        self.comp_name = comp_name
        self.res_name = res_name