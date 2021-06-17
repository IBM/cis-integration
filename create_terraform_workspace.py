
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os, requests, time
from dotenv import load_dotenv
from ibm_cloud_sdk_core import ApiException

class WorkspaceCreator:
    def create_terraform_workspace(self):
        load_dotenv("./credentials.env")
        apikey = os.getenv("CIS_SERVICES_APIKEY")
        schematics_url = os.getenv("SCHEMATICS_URL")
        github_PAT = os.getenv("GITHUB_PAT")
        authenticator = IAMAuthenticator(apikey)
        schematics_service = SchematicsV1(authenticator = authenticator)
        schematics_service.set_service_url(schematics_url)
        r_token = self.request_token(apikey)

        # Setting up the necessary information to create the workspace
        workspace_variable_request_model = {}
        workspace_variable_request_model['name'] = 'ibmcloud_api_key'
        workspace_variable_request_model['value'] = apikey
        workspace_variable_request_model['secure'] = True

        template_source_data_request_model = {}
        template_source_data_request_model['folder'] = 'cert-create'
        template_source_data_request_model['type'] = 'terraform_v0.14.40'
        template_source_data_request_model['variablestore'] = [workspace_variable_request_model]

        template_repo_request_model = {}
        template_repo_request_model['url'] = 'https://github.ibm.com/GCAT/cis-integration'

        # Creating the workspace and connecting to the github repo
        workspace_response = schematics_service.create_workspace(
            description="Testing creating a workspace using a python script", 
            name="test-code-workspace-1",
            template_data=[template_source_data_request_model],
            template_repo=template_repo_request_model,
            type=['terraform_v0.14.40'],
            location="us-south",
            resource_group="Interns-2021",
            x_github_token=github_PAT,
        ).get_result()

        print('Successfully created the workspace!')
        workspace_activity_plan_result = None
        keepgoing = True

        # Generate a plan from the imported terraform files
        while keepgoing:
            # The command will throw an ApiException while the workspace is still generating,
            # so we catch that exception and try again every 2 seconds as long as some other
            # error does not occur
            try:
                workspace_activity_plan_result = schematics_service.plan_workspace_command(
                    w_id=workspace_response["id"],
                    refresh_token=r_token
                    
                ).get_result()
                break
            except ApiException as ae:
                # Error 409 means that the workspace is still busy, we just have to wait for it to finish
                if ae.http_response.status_code == 409:
                    print('Generating a plan....')
                    time.sleep(2)
                else:
                    # Some other error occurred so we need to break out of the loop and end execution
                    print("Error {0}: ".format(ae.http_response.status_code) + ae.message)
                    keepgoing = False
                    break
        # Now we apply the plan if it was successfully generated
        if keepgoing:
            print('Plan Generated! Applying:')
            # This command will also throw an ApiException while the plan is still finalizing,
            # so we just wait for it to finish
            while keepgoing:
                try:
                    workspace_activity_apply_result = schematics_service.apply_workspace_command(
                        w_id=workspace_response["id"],
                        refresh_token=r_token
                        
                    ).get_result()
                    break
                except ApiException as ae:
                    if ae.http_response.status_code == 409:
                        print('Building the resources....')
                        time.sleep(2)
                    else:
                        print("Error {0}: ".format(ae.http_response.status_code) + ae.message)
                        keepgoing = False
                        break
        if keepgoing:
            print('Resources built successfully!')

        
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
        return token.json()["refresh_token"] 
    

