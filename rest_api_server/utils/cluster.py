import uuid

import yaml

from utils.miscellaneous_operations import create_cluster_config_file


class Cluster:
    def __init__(self, cluster_config):
        """
        constructor for the On_Premises_Cluster classs
        :param cluster_config:
        :param cluster_config:
        """
        self.cluster_config = cluster_config

    def add_cluster(self):
        """
        This method will add Cluster
        :return:
        """
        error = True
        response = None
        cluster_id = str(uuid.uuid4())
        cluster_config = yaml.safe_load(self.cluster_config)
        try:
            error_create_cluster_config_file, response_create_cluster_config_file = create_cluster_config_file(
                cluster_id=cluster_id, config_details=cluster_config)
            if not error:
                raise Exception(response_create_cluster_config_file)
            else:
                response = cluster_id
                error = False

        except Exception as e:
            response = str(e)
        finally:
            return error, response
