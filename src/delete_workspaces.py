from ibm_schematics import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os, requests

class DeleteWorkspace:
    def __init__(self, schematics_url: str, apikey: str) -> None:
        self.schematics_url = schematics_url
        self.apikey = apikey

    def delete_workspace(self):
        w_ids = []
        execute = input("Delete all associated Schematics workspaces? Input 'y' to execute: ")
        if execute == 'y':
            token = self.request_token(self.apikey)
            authenticator = IAMAuthenticator(self.apikey)
            schematics_service = SchematicsV1(authenticator = authenticator)
            schematics_service.set_service_url(self.schematics_url)
            workspace_response_list = schematics_service.list_workspaces().get_result()
            for workspace in workspace_response_list['workspaces']:
                for template in workspace['template_data']:
                    for variable in template['variablestore']:
                        if variable['name'] == 'cis_name':
                            print(variable['value'])
                            w_ids.append(workspace['id'])

            num_deleted = 0
            for id in w_ids:
                workspace_delete_response = schematics_service.delete_workspace(
                    w_id=id,
                    refresh_token=token['refresh_token']
                )
                if workspace_delete_response.status_code == 200:
                    num_deleted += 1
            print("Deleted " + str(num_deleted) + " associated workspaces")
        

    def request_token(self, apikey: str):
            """
            Requests a refresh token for the client so that we can execute the plan and apply commands in
            the workspace.
            
            param: apikey is the client's IBM Cloud Apikey

            returns: the generated refresh token
            """
            data={'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': apikey}
            headers= {'Accept': 'application/json',
                    'Content-type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic Yng6Yng='}
            url="https://iam.cloud.ibm.com/identity/token"
            token = requests.post(url=url, data=data, headers=headers)
            return token.json()