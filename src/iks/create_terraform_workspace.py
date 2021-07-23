from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import time
from ibm_cloud_sdk_core import ApiException
from src.common.functions import Color as Color


class WorkspaceCreator:
    def __init__(self, cis_api_key, schematics_url, cis_name, resource_group, cis_domain, cluster_id):
        self.cis_api_key = cis_api_key
        self.schematics_url = schematics_url
        self.cis_name = cis_name
        self.resource_group = resource_group
        self.cis_domain = cis_domain
        self.cluster_id = cluster_id

    def create_terraform_workspace(self):
        authenticator = IAMAuthenticator(self.cis_api_key)
        schematics_service = SchematicsV1(authenticator=authenticator)
        schematics_service.set_service_url(self.schematics_url)

        keepgoing = True

        # Creating the workspace and connecting to the github repo
        if keepgoing:
            # Setting up the necessary information to create the workspace
            workspace_apikey_variable_request = {}
            workspace_apikey_variable_request['name'] = 'ibmcloud_api_key'
            workspace_apikey_variable_request['value'] = self.cis_api_key
            workspace_apikey_variable_request['secure'] = True

            workspace_cis_name_variable_request = {}
            workspace_cis_name_variable_request['name'] = 'cis_name'
            workspace_cis_name_variable_request['value'] = self.cis_name

            workspace_resource_group_variable_request = {}
            workspace_resource_group_variable_request['name'] = 'resource_group'
            workspace_resource_group_variable_request['value'] = self.resource_group

            workspace_cis_domain_variable_request = {}
            workspace_cis_domain_variable_request['name'] = 'cis_domain'
            workspace_cis_domain_variable_request['value'] = self.cis_domain

            workspace_cluster_id_variable_request = {}
            workspace_cluster_id_variable_request['name'] = 'cluster_id'
            workspace_cluster_id_variable_request['value'] = self.cluster_id

            template_source_data_request_model = {}

            template_source_data_request_model['type'] = 'terraform_v0.14.00'
            template_source_data_request_model['variablestore'] = [workspace_apikey_variable_request,
                                                                   workspace_cis_name_variable_request,
                                                                   workspace_resource_group_variable_request,
                                                                   workspace_cis_domain_variable_request,
                                                                   workspace_cluster_id_variable_request]

            template_repo_request_model = {}
