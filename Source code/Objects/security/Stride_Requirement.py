class Stride_Requirement:

    def __init__(self, id, title, description, justification, mechanism, id_priority, name_priority, id_component, name_comp_link, id_link, id_dfd, name_dfd,
                 id_stride, name_stride, is_imported = False, is_component = True, list_of_controls = [], performance_req = "", list_res = []):
        self.id = id  #0
        self.title = title  #1
        self.description = description  #2
        self.justification = justification  #3
        self.mechanism = mechanism #4
        self.id_priority = id_priority #5
        self.name_priority = name_priority  #6
        self.id_component = id_component  #7
        self.name_comp_link = name_comp_link  #8
        self.id_link = id_link  #9
        self.id_dfd = id_dfd  #10
        self.name_dfd = name_dfd  #11
        self.id_stride = id_stride  #12
        self.name_stride = name_stride  #13
        self.is_imported = is_imported  #14
        self.is_component = is_component  #15
        self.list_of_controls = list_of_controls  #16
        self.performance_req = performance_req #17
        self.list_res = list_res #18

class Stride_Requirement_imported:

    def __init__(self, id, id_req, id_req_imported):
        self.id = id
        self.id_req = id_req
        self.id_req_imported = id_req_imported

class Pef_Stride_Requirement:

    def __init__(self, id, title, description, justification, mechanism, id_priority, name_priority, id_component,
                 id_link, id_dfd, name_dfd, id_stride, name_stride, component_src_name, component_dst_name, id_project, control_selecteds):
        self.id = id  #0
        self.title = title  #1
        self.description = description  #2
        self.justification = justification  #3
        self.mechanism = mechanism #4
        self.id_priority = id_priority #5
        self.name_priority = name_priority  #6
        self.id_component = id_component  #7
        self.id_link = id_link  #8
        self.id_dfd = id_dfd  #9
        self.name_dfd = name_dfd  #10
        self.id_stride = id_stride  #11
        self.name_stride = name_stride  #12
        self.component_src_name = component_src_name  #13
        self.component_dst_name = component_dst_name  #14
        self.id_project = id_project  #15
        self.control_selecteds = control_selecteds  #16