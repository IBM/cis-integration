from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import time
import json
from ibm_cloud_sdk_core import ApiException
from src.common.functions import Color as Color


class WorkspaceCreator:
    def __init__(self, cis_api_key, schematics_url, cis_name, resource_group, cis_domain, cluster_id, ingress, cert_name, verbose, token):
        self.cis_api_key = cis_api_key
        self.schematics_url = schematics_url
        self.cis_name = cis_name
        self.resource_group = resource_group
        self.cis_domain = cis_domain
        self.cluster_id = cluster_id
        self.ingress = ingress
        self.cert_name = cert_name
        self.verbose = verbose
        self.token = token

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

            workspace_ingress_variable_request = {}
            workspace_ingress_variable_request['name'] = 'ingress'
            workspace_ingress_variable_request['value'] = self.ingress

            workspace_cert_name_variable_request = {}
            workspace_cert_name_variable_request['name'] = 'cert_name'
            workspace_cert_name_variable_request['value'] = self.cert_name

            workspace_create_ce_variable_request = {}
            workspace_create_ce_variable_request['name'] = 'create_ce'
            workspace_create_ce_variable_request['value'] = 'false'

            workspace_create_iks_variable_request = {}
            workspace_create_iks_variable_request['name'] = 'create_iks'
            workspace_create_iks_variable_request['value'] = 'true'

            template_source_data_request_model = {}

            template_source_data_request_model['type'] = 'terraform_v0.14.00'
            template_source_data_request_model['variablestore'] = [workspace_apikey_variable_request,
                                                                   workspace_cis_name_variable_request,
                                                                   workspace_resource_group_variable_request,
                                                                   workspace_cis_domain_variable_request,
                                                                   workspace_cluster_id_variable_request,
                                                                   workspace_ingress_variable_request,
                                                                   workspace_cert_name_variable_request,
                                                                   workspace_create_ce_variable_request,
                                                                   workspace_create_iks_variable_request]

            template_repo_request_model = {}
            template_repo_request_model['url'] = 'https://github.com/IBM/cis-integration/tree/master/src/root_terraform'

            workspace_response = schematics_service.create_workspace(
                description="Workspace for building resources for the CIS-IKS integration using Terraform",
                name="temp-workspace",
                template_data=[template_source_data_request_model],
                template_repo=template_repo_request_model,
                type=['terraform_v0.14.00'],
                location='us-south',
                resource_group=self.resource_group,
            ).get_result()

            print(Color.GREEN +
                  'SUCCESS: Successfully created the workspace!' + Color.END)

            workspace_activity_plan_result = None

            # Generate a plan from the imported terraform files
            while keepgoing:
                # The command will throw an ApiException while the workspace is still generating,
                # so we catch that exception and try again every 2 seconds as long as some other
                # error does not occur
                try:
                    workspace_activity_plan_result = schematics_service.plan_workspace_command(
                        w_id=workspace_response["id"],
                        refresh_token=self.token["refresh_token"]

                    ).get_result()
                    break
                except ApiException as ae:
                    # Error 409 means that the workspace is still busy, we just have to wait for it to finish
                    if ae.http_response.status_code == 409:
                        print("Generating a plan....")
                        time.sleep(2)
                    else:
                        # Some other error occurred so we need to break out of the loop and end execution
                        print(
                            Color.RED + "ERROR {0}: ".format(ae.http_response.status_code) + ae.message + Color.END)
                        keepgoing = False
                        break

            # Now we apply the plan if it was successfully generated
            if keepgoing:
                print(Color.GREEN + "SUCCESS: Plan Generated! Applying: " + Color.END)
                # This command will also throw an ApiException while the plan is still finalizing,
                # so we just wait for it to finish
                while keepgoing:
                    try:
                        workspace_activity_apply_result = schematics_service.apply_workspace_command(
                            w_id=workspace_response["id"],
                            refresh_token=self.token["refresh_token"]

                        ).get_result()
                        break
                    except ApiException as ae:
                        if ae.http_response.status_code == 409:
                            print("Building the resources....")
                            time.sleep(2)
                        else:
                            print(
                                Color.RED + "ERROR; {0}: ".format(ae.http_response.status_code) + ae.message + Color.END)
                            keepgoing = False
                            break

            while keepgoing:
                print("Checking workspace status...")
                status = self.action_status(
                    w_id=workspace_response["id"],
                    a_id=workspace_activity_apply_result["activityid"],
                    access_token=self.token["access_token"]
                )

                if status.json()["status"] == "COMPLETED" or status.json()["status"] == "FAILED":
                    if self.verbose:
                        apply_log = self.apply_response(
                            w_id=workspace_response["id"],
                            a_id=workspace_activity_apply_result["activityid"],
                            t_id=workspace_response["template_data"][0]["id"],
                            access_token=self.token["access_token"]
                        )
                        print(apply_log)
                    elif status.json()["status"] == "COMPLETED":
                        print("Workspace status: " + Color.GREEN +
                              status.json()["status"] + Color.END)
                        print(
                            "Refer to your Schematics workspace on cloud.ibm.com for more details.")
                    elif status.json()["status"] == "FAILED":
                        print("Workspace status: " + Color.RED +
                              status.json()["status"] + Color.END)
                        print(
                            "Refer to your Schematics workspace on cloud.ibm.com for more details.")
                    keepgoing = False
                else:
                    print("Workspace status: " + status.json()["status"])
                    time.sleep(10)

    def action_status(self, w_id: str, a_id: str, access_token: str):
        url = "https://schematics.cloud.ibm.com/v1/workspaces/" + w_id + "/actions/" + a_id

        headers = {'Authorization': access_token}

        response = requests.request("GET", url, headers=headers)
        return response

    def apply_response(self, w_id: str, t_id: str, a_id: str, access_token: str):
        url = "https://schematics.cloud.ibm.com/v1/workspaces/" + \
            w_id + "/runtime_data/" + t_id + "/log_store/actions/" + a_id

        headers = {'Authorization': access_token}

        response = requests.request("GET", url, headers=headers)
        return response.text
