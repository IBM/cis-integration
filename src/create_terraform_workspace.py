
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os, requests, time, tarfile
from ibm_cloud_sdk_core import ApiException
from ibm_platform_services import ResourceControllerV2
from ibm_cloud_networking_services import ZonesV1, GlobalLoadBalancerPoolsV0, GlobalLoadBalancerV1, DnsRecordsV1
from src.functions import Color as Color

class WorkspaceCreator:
    def __init__(self, cis_api_key, schematics_url, app_url, cis_domain, resource_group, cis_name, api_endpoint, crn, zone_id, verbose):
        self.cis_api_key = cis_api_key
        self.schematics_url = schematics_url
        self.app_url = app_url
        self.cis_domain = cis_domain
        self.resource_group = resource_group
        self.cis_name = cis_name
        self.api_endpoint = api_endpoint
        self.crn = crn
        self.zone_id = zone_id
        self.verbose = verbose

    def create_terraform_workspace(self):
        authenticator = IAMAuthenticator(self.cis_api_key)
        schematics_service = SchematicsV1(authenticator = authenticator)
        schematics_service.set_service_url(self.schematics_url)
        r_token = self.request_token(self.cis_api_key)
        keepgoing = True

        pool_name = self.pool_check()
        keepgoing = self.glb_check()
        keepgoing = self.dns_check(keepgoing)
        keepgoing = self.edge_check(r_token["access_token"], keepgoing)

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

            workspace_app_url_variable_request = {}
            workspace_app_url_variable_request['name'] = 'app_url'
            workspace_app_url_variable_request['value'] = self.app_url

            # workspace_www_variable_request = {}
            # workspace_www_variable_request['name'] = 'www_domain'
            # workspace_www_variable_request['value'] = 'www.' + self.cis_domain

            # workspace_wild_variable_request = {}
            # workspace_wild_variable_request['name'] = 'wild_domain'
            # workspace_wild_variable_request['value'] = '*.' + self.cis_domain

            workspace_domain_variable_request = {}
            workspace_domain_variable_request['name'] = 'cis_domain'
            workspace_domain_variable_request['value'] = self.cis_domain

            workspace_action_variable_request = {}
            workspace_action_variable_request['name'] = 'action_name'
            workspace_action_variable_request['value'] = self.cis_domain.replace('.', '-')

            workspace_pool_variable_request = {}
            workspace_pool_variable_request['name'] = 'pool_name'
            workspace_pool_variable_request['value'] = pool_name

            template_source_data_request_model = {}
            
            template_source_data_request_model['type'] = 'terraform_v0.14.40'
            template_source_data_request_model['variablestore'] = [workspace_apikey_variable_request,
                                                                workspace_resource_group_variable_request,
                                                                workspace_cis_name_variable_request,
                                                                workspace_app_url_variable_request,
                                                                workspace_domain_variable_request,
                                                                # workspace_www_variable_request,
                                                                workspace_action_variable_request,
                                                                # workspace_wild_variable_request,
                                                                workspace_pool_variable_request]

            workspace_response = schematics_service.create_workspace(
                description="Workspace for building resources for the CIS instance using terraform", 
                name="temp-workspace",
                template_data=[template_source_data_request_model],
                type=['terraform_v0.14.40'],
                location="us-south",
                resource_group=self.resource_group,
            ).get_result()

            print(Color.GREEN + 'SUCCESS: Successfully created the workspace!' + Color.END)
        workspace_activity_plan_result = None
        #keepgoing = True

        if keepgoing:
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
                        print(Color.RED + "ERROR {0}: ".format(ae.http_response.status_code) + ae.message + Color.END)
                        keepgoing = False
                        break


            print(Color.GREEN + "SUCCESS: Uploaded tar file!" + Color.END)

        # Generate a plan from the imported terraform files
        while keepgoing:
            # The command will throw an ApiException while the workspace is still generating,
            # so we catch that exception and try again every 2 seconds as long as some other
            # error does not occur
            try:
                workspace_activity_plan_result = schematics_service.plan_workspace_command(
                    w_id=workspace_response["id"],
                    refresh_token=r_token["refresh_token"]
                    
                ).get_result()
                break
            except ApiException as ae:
                # Error 409 means that the workspace is still busy, we just have to wait for it to finish
                if ae.http_response.status_code == 409:
                    print('Generating a plan....')
                    time.sleep(2)
                else:
                    # Some other error occurred so we need to break out of the loop and end execution
                    print(Color.RED + "ERROR {0}: ".format(ae.http_response.status_code) + ae.message + Color.END)
                    keepgoing = False
                    break
        
        # Now we apply the plan if it was successfully generated
        if keepgoing:
            print(Color.GREEN + 'SUCCESS: Plan Generated! Applying:' + Color.END)
            # This command will also throw an ApiException while the plan is still finalizing,
            # so we just wait for it to finish
            while keepgoing:
                try:
                    workspace_activity_apply_result = schematics_service.apply_workspace_command(
                        w_id=workspace_response["id"],
                        refresh_token=r_token["refresh_token"]
                        
                    ).get_result()
                    break
                except ApiException as ae:
                    if ae.http_response.status_code == 409:
                        print('Building the resources....')
                        time.sleep(2)
                    else:
                        print(Color.RED + "ERROR {0}: ".format(ae.http_response.status_code) + ae.message + Color.END)
                        keepgoing = False
                        break
        while keepgoing:
            print("Checking workspace status...")
            status = self.action_status(
                w_id=workspace_response["id"],
                a_id=workspace_activity_apply_result["activityid"],
                access_token=r_token["access_token"]
            )
            
            if status.json()["status"] == "COMPLETED" or status.json()["status"] == "FAILED":
                if self.verbose:
                    apply_log = self.apply_response(
                    w_id=workspace_response["id"],
                    a_id=workspace_activity_apply_result["activityid"],
                    t_id=workspace_response["template_data"][0]["id"],
                    access_token=r_token["access_token"]
                    )
                    print(apply_log)
                elif status.json()["status"] == "COMPLETED":
                    print("Workspace status: " + Color.GREEN + status.json()["status"] + Color.END)
                    print("Refer to your Schematics workspace on cloud.ibm.com for more details.")
                elif status.json()["status"] == "FAILED":
                    print("Workspace status: " + Color.RED + status.json()["status"] + Color.END)
                    print("Refer to your Schematics workspace on cloud.ibm.com for more details.")
                keepgoing = False
            else:
                print("Workspace status: " + status.json()["status"])
                time.sleep(10)

    def pool_check(self) -> str:
        '''
        Returns the name of the pool
        '''
        pools = GlobalLoadBalancerPoolsV0.new_instance(crn=self.crn, service_name="cis_services")
        pools.set_service_url(self.api_endpoint)
        pool_response = pools.list_all_load_balancer_pools().get_result()
        default_pool = "default-pool"
        pool_name = default_pool
        pool_count = 1
        pool_check = True
        while pool_check:
            for pool in pool_response["result"]:
                if pool_name == pool["name"]:
                    pool_name = default_pool + "-" + str(pool_count)
                    pool_count += 1
            else:
                pool_check = False
        return pool_name

    def glb_check(self) -> bool:
        glb = GlobalLoadBalancerV1.new_instance(
            crn=self.crn,
            zone_identifier=self.zone_id,
            service_name="cis_services"
        )
        glb.set_service_url(self.api_endpoint)
        glb_response = glb.list_all_load_balancers().get_result()
        for balancer in glb_response["result"]:
            if balancer["name"] == self.cis_domain:
                print(Color.RED + "ERROR: A global load balancer connected to " + self.cis_domain + " already exists. Remove this resource and try again" + Color.END)
                return False
        return True
    
    def dns_check(self, keepgoing: bool) -> bool:
        records = DnsRecordsV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services"
        )
        records.set_service_url(self.api_endpoint)
        record_response = records.list_all_dns_records().get_result()
        for record in record_response["result"]:
            if record["name"] == self.cis_domain:
                print(Color.RED + "ERROR: A CNAME DNS record with the name " + self.cis_domain + " already exists. Remove this resource and try again" + Color.END)
                keepgoing = False
            if record["name"] == "www." + self.cis_domain:
                print(Color.RED + "ERROR: A CNAME DNS record with the name www." + self.cis_domain + " already exists. Remove this resource and try again" + Color.END)
                keepgoing = False
        return keepgoing

    def edge_check(self, access_token: str, keepgoing: bool) -> bool:
        
        edge_url = "https://api.cis.cloud.ibm.com/v1/" + self.crn + "/zones/" + self.zone_id + "/workers/routes"

        edge_headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + access_token
        }

        edge_response = requests.request("GET", edge_url, headers=edge_headers)
        for trigger in edge_response.json()['result']:
            if trigger["pattern"] == '*.' + self.cis_domain:
                print(Color.RED + "ERROR: An edge function trigger matching the pattern *." + self.cis_domain + " already exists. Remove this resource and try again" + Color.END)
                keepgoing = False
            elif trigger["pattern"] == 'www.' + self.cis_domain:
                print(Color.RED + "ERROR: An edge function trigger matching the pattern www." + self.cis_domain + " already exists. Remove this resource and try again" + Color.END)
                keepgoing = False
            elif trigger["pattern"] == self.cis_domain:
                print(Color.RED + "ERROR: An edge function trigger matching the pattern " + self.cis_domain + " already exists. Remove this resource and try again" + Color.END)
                keepgoing = False
        return keepgoing        

    def action_status(self, w_id: str, a_id: str, access_token: str):
        url = "https://schematics.cloud.ibm.com/v1/workspaces/" + w_id + "/actions/" + a_id
        
        headers = {'Authorization': access_token}

        response = requests.request("GET", url, headers=headers)
        return response

    def apply_response(self, w_id: str, t_id: str, a_id: str, access_token: str):
        url = "https://schematics.cloud.ibm.com/v1/workspaces/" + w_id + "/runtime_data/" + t_id + "/log_store/actions/" + a_id

        headers = {'Authorization': access_token}

        response = requests.request("GET", url, headers=headers)
        return response.text

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
        return token.json()
        #return token.json()["refresh_token"] 
    

