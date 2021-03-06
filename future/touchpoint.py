from api.exception import *
from api.alpineobject import AlpineObject

class TouchPoint(AlpineObject):

    def __init__(self, base_url, session, token):
        super(TouchPoint, self).__init__(base_url, session, token)


    def add_touchpoint(self, touchpoint_name, workfile_id, workspace_id, touchpoint_description):
        """
        Does nothing

        :param touchpoint_name:
        :param workfile_id:
        :param workspace_id:
        :param touchpoint_description:
        :return:
        """
        pass

    def delete_touchpoint(self, touchpoint_name, workspace_id):
        """
        Does nothing

        :param touchpoint_name:
        :param workspace_id:
        :return:
        """
        pass

    def publish_touchpoint(self, workspace_id, touchpoint_name):
        pass

    def unpublish_touchpoint(self, workspace_id, touchpoint_name):
        pass

    def run_touchpoint(self, workspace_id, touchpoint_name, output_table, parameter_list=None):
        pass

    def stop_touchpoint(self, workspace_id, touchpoint_name):
        pass

    def get_touchpoint_list(self, workspace_id=None):
        pass

    def get_touchpoint_info(self, touchpoint_name):
        pass

    def get_touchpoint_id(self, touchpoint_name):
        pass

    def add_touchpoint_parameter(self, workspace_id, touchpoint_name, variable_name, data_type,
                             variable_label, variable_desc, options, required_val, use_default):
        pass

    def get_touchpoint_parameters(self, workspace_id, touchpoint_name):
        pass

