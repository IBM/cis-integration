
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os, requests, time, tarfile
from dotenv import load_dotenv
from ibm_cloud_sdk_core import ApiException

class WorkspaceCreator:
    def __init__(self, cis_api_key, schematics_url, app_url, cis_domain, resource_group, cis_name):
        self.cis_api_key = cis_api_key
        self.schematics_url = schematics_url
        self.app_url = app_url
        self.cis_domain = cis_domain
        self.resource_group = resource_group
        self.cis_name = cis_name

    def create_terraform_workspace(self):
        authenticator = IAMAuthenticator(self.cis_api_key)
        schematics_service = SchematicsV1(authenticator = authenticator)
        schematics_service.set_service_url(self.schematics_url)
        r_token = self.request_token(self.cis_api_key)

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

        workspace_app_url_variable_request = {}
        workspace_app_url_variable_request['name'] = 'app_url'
        workspace_app_url_variable_request['value'] = self.app_url

        workspace_www_variable_request = {}
        workspace_www_variable_request['name'] = 'www_domain'
        workspace_www_variable_request['value'] = 'www.' + self.cis_domain

        workspace_wild_variable_request = {}
        workspace_wild_variable_request['name'] = 'wild_domain'
        workspace_wild_variable_request['value'] = '*.' + cis_domain

        workspace_domain_variable_request = {}
        workspace_domain_variable_request['name'] = 'cis_domain'
        workspace_domain_variable_request['value'] = self.cis_domain

        workspace_action_variable_request = {}
        workspace_action_variable_request['name'] = 'action_name'
        workspace_action_variable_request['value'] = self.cis_domain.replace('.', '-')

        template_source_data_request_model = {}
        
        template_source_data_request_model['type'] = 'terraform_v0.14.40'
        template_source_data_request_model['variablestore'] = [workspace_apikey_variable_request,
                                                               workspace_resource_group_variable_request,
                                                               workspace_cis_name_variable_request,
                                                               workspace_app_url_variable_request,
                                                               workspace_domain_variable_request,
                                                               workspace_www_variable_request,
                                                               workspace_action_variable_request,
                                                               workspace_wild_variable_request]


        

        # Creating the workspace and connecting to the github repo
        workspace_response = schematics_service.create_workspace(
            description="Workspace for building resources for the CIS instance using terraform", 
            name="temp-workspace",
            template_data=[template_source_data_request_model],
            type=['terraform_v0.14.40'],
            location="us-south",
            resource_group=workspace_resource_group_variable_request,
        ).get_result()

        print('Successfully created the workspace!')
        workspace_activity_plan_result = None
        keepgoing = True

        terra = self.build_tar(self.app_url)

        file = open(terra, "rb")
        while keepgoing:
            try:    
                template_repo_tar_upload_response = schematics_service.upload_template_tar(
                    w_id=workspace_response["id"],
                    t_id=workspace_response["template_data"][0]["id"],
                    file = file,
                    file_content_type = 'multipart/form-data'
                ).get_result()
                break
            except ApiException as ae:
                if ae.http_response.status_code == 409:
                    print('Uploading tar file...')
                    time.sleep(2)
                else:
                    print("Error {0}: ".format(ae.http_response.status_code) + ae.message)
                    keepgoing = False
                    break


        print("Uploaded tar file!")

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

    def build_tar(self, app_url: str):
        """
        Builds the tar file of terraform scripts to be sent to the Schematics workspace

        param: app_url is the URL of the Code Engine application

        returns: the path to the generated file
        """
        path_to_script = os.path.dirname(os.path.abspath(__file__))
        terraform_path = path_to_script + "/terraform"
        try:
            js_file = open(terraform_path + "/edge_function_method.js", "w")
        except:
            path_to_script = "./src"
            terraform_path = path_to_script + "/terraform"
            js_file = open(terraform_path + "/edge_function_method.js", "w")

        js_file.write("addEventListener('fetch', (event) => {\n    const mutable_request = new Request(event.request);\n    event.respondWith(redirectAndLog(mutable_request));\n});\n\nasync function redirectAndLog(request) {\n    const response = await redirectOrPass(request);\n    return response;\n}\n\nasync function getSite(request, site) {\n    const url = new URL(request.url);\n    // let our servers know what origin the request came from\n    // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-Host\n    request.headers.set('X-Forwarded-Host', url.hostname);\n    request.headers.set('host', site);\n    url.hostname = site;\n    url.protocol = \"https:\";\n    response = fetch(url.toString(), request);\n    console.log('Got getSite Request to ' + site, response);\n    return response;\n}\n\nasync function redirectOrPass(request) {\n    const urlObject = new URL(request.url);\n\n    let response = null;\n\n    try {\n        console.log('Got MAIN request', request);\n\n        response = await getSite(request, '"+ app_url + "');\n        console.log('Got MAIN response', response.status);\n        return response;\n\n    } catch (error) {\n        // if no action found, play the regular request\n        console.log('Got Error', error);\n        return await fetch(request);\n\n    }\n\n}\n")
        js_file.close()

        with tarfile.open(path_to_script + '/terra.tar', "w") as tar:
            tar.add(terraform_path, arcname="terra")
        return path_to_script + '/terra.tar'

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
    

