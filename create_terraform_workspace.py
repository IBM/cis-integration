
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import time
import subprocess
from dotenv import load_dotenv
from ibm_cloud_sdk_core import ApiException

def main():
    load_dotenv()
    apikey = os.getenv("CIS_SERVICES_APIKEY")
    schematics_url = os.getenv("SCHEMATICS_URL")
    github_PAT = os.getenv("GITHUB_PAT")
    authenticator = IAMAuthenticator(apikey)
    schematics_service = SchematicsV1(authenticator = authenticator)
    schematics_service.set_service_url(schematics_url)

    r_token = subprocess.Popen("./refresh_token.sh", shell=True, stdout=subprocess.PIPE)
    last_token = r_token.stdout.read()
    encoding = 'utf-8'
    last_token = last_token.decode(encoding).replace('\n','')
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
    while keepgoing:
        try:
            workspace_activity_plan_result = schematics_service.plan_workspace_command(
                w_id=workspace_response["id"],
                refresh_token=last_token
                
            ).get_result()
            break
        except ApiException as ae:

            if ae.http_response.status_code == 409:
                print('Generating a plan....')
                time.sleep(2)
            else:
                print("Error {0}: ".format(ae.http_response.status_code) + ae.message)
                keepgoing = False
                break
    
    if keepgoing:
        print('Plan Generated! Applying:')
        while keepgoing:
            try:
                workspace_activity_apply_result = schematics_service.apply_workspace_command(
                    w_id=workspace_response["id"],
                    refresh_token=last_token
                    
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

    
    
    

if __name__ == "__main__":
    main()