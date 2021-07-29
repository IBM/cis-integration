from ibm_schematics import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os, requests, time, json
from ibm_cloud_sdk_core import ApiException
from src.common.functions import Color as Color
from ibm_cloud_networking_services import ZonesV1, GlobalLoadBalancerPoolsV0, GlobalLoadBalancerV1, DnsRecordsV1, SslCertificateApiV1
class DeleteWorkspace:
    

    def __init__(self, crn, zone_id, cis_domain, api_endpoint, schematics_url: str, apikey: str, token) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.cis_domain = cis_domain
        self.api_endpoint = api_endpoint
        self.schematics_url = schematics_url
        self.apikey = apikey
        self.token = token
        self.w_ids = []

    def delete_workspace(self):
        execute = input("Delete all associated Schematics workspaces and connected CIS resources? Input 'y' or 'yes' to execute: ").lower()
        if execute == 'y' or execute == 'yes':
            
            authenticator = IAMAuthenticator(self.apikey)
            schematics_service = SchematicsV1(authenticator = authenticator)
            schematics_service.set_service_url(self.schematics_url)
            workspace_response_list = schematics_service.list_workspaces().get_result()

            # retrieving the workspaces relating to our github repo
            for workspace in workspace_response_list['workspaces']:
                if workspace['template_repo']['url'] == 'https://github.com/IBM/cis-integration':
                    w_info = {'id': workspace['id'], 'status': workspace['status'], 'created_at': workspace['created_at']}
                    self.w_ids.append(w_info)
            
            # search CIS instance for GLB
            glb_info = self.glb_check()
            # search for origin pool and health check in CIS instance
            if not glb_info is None:
                glb_info = self.pool_check(glb_info)

            # search for edge functions in CIS instance
            edge_ids = self.edge_check(self.token['access_token'])   
            dns_ids = self.dns_check()
            

            keepgoing = True
            check_cis = True
            # if any of the resources are missing, the Schematics workspace destroy function will fail
            if glb_info is None or len(edge_ids) == 0 or len(dns_ids) == 0:
                check_cis = False
                print("Some resources connected to the Schematics workspace have already been modified or destroyed.")
                print("Please use the Python delete option to delete any remaining resources on your CIS instance.")
                execute = input("Would you like to continue with deleting the associated workspaces? Input 'y' or 'yes' to execute: ").lower()
                if  not execute == 'y' and not execute == 'yes':
                    keepgoing = False
            
            root_dns_found = False
            www_dns_found = False
            glb_found = False
            pool_found = False
            monitor_found = False
            edge_trigger_1 = False
            edge_trigger_2 = False
            edge_trigger_3 = False
            edge_action = False
            cert_found = False
            num_deleted = 0

            # need to find the most recent active workspace - this will be the one connected to the CIS instance
            destroyer = self.most_recent()
            # if there are no active workspaces, we can't delete any resources 
            if destroyer is None:
                check_cis = False
                print("Could not find any active workspaces connected to the resources on your CIS instance")
                print("Please use the Python delete option to delete any remaining resources on your CIS instance.")
                execute = input("Would you like to continue with deleting the associated workspaces? Input 'y' or 'yes' to execute: ").lower()
                if  not execute == 'y' and not execute == 'yes':
                    keepgoing = False
            elif check_cis: # we need to check the workspace that it contains all the resources we're looking for
                # retrieving the template ID of the workspace
                destroyer_response = schematics_service.get_workspace(
                    w_id=destroyer['id']
                ).get_result()
                # retrieving the template state with all the resource information
                state = schematics_service.get_workspace_template_state(
                    w_id=destroyer['id'],
                    t_id=destroyer_response['template_data'][0]['id']
                ).get_result()
                # searching the template state for each required resource
                for resource in state['resources']:
                    if resource['name'] == 'test_dns_root_record':
                        if resource['instances'][0]['attributes']['record_id'] in dns_ids:
                            root_dns_found = True
                    elif resource['name'] == 'test_dns_www_record':
                        if resource['instances'][0]['attributes']['record_id'] in dns_ids:
                            www_dns_found = True
                    elif resource['name'] == 'test_action':
                        if resource['instances'][0]['attributes']['action_name'] == self.cis_domain.replace('.','-'):
                            edge_action = True
                    elif resource['name'] == 'action_trigger':
                        for trigger in resource['instances']:
                            if trigger['attributes']['trigger_id'] in edge_ids:
                                if trigger['attributes']['pattern_url'] == self.cis_domain:
                                    edge_trigger_1 = True
                                elif trigger['attributes']['pattern_url'] == 'www.' + self.cis_domain:
                                    edge_trigger_2 = True
                                elif trigger['attributes']['pattern_url'] == '*.' + self.cis_domain:
                                    edge_trigger_3 = True
                    elif resource['name'] == 'example-glb':
                        if resource['instances'][0]['attributes']['glb_id'] == glb_info['glb']:
                            glb_found = True
                    elif resource['name'] == 'test' and resource['type'] == 'ibm_cis_healthcheck':
                        if resource['instances'][0]['attributes']['monitor_id'] == glb_info['monitor']:
                            monitor_found = True
                    elif resource['name'] == 'example' and resource['type'] == 'ibm_cis_origin_pool':
                        if resource['instances'][0]['attributes']['pool_id'] == glb_info['pool']:
                            pool_found = True
                    elif resource['name'] == 'test' and resource['type'] == 'ibm_cis_certificate_order':
                        cert_to_find = resource['instances'][0]['attributes']['certificate_id']
                        cis_cert = self.cert_check()
                        for cert in cis_cert['result']:
                            if cert_to_find == cert['id']:
                                cert_found = True


            if keepgoing and check_cis and not (glb_found and cert_found and pool_found 
                and monitor_found and www_dns_found and root_dns_found 
                and edge_action and edge_trigger_1 and edge_trigger_2 and edge_trigger_3):
                check_cis = False
                print("Some resources connected to the Schematics workspace have already been modified or destroyed.")
                print("Please use the Python delete option to delete any remaining resources on your CIS instance.")
                execute = input("Would you like to continue with deleting the associated workspaces? Input 'y' or 'yes' to execute: ").lower()
                if  not execute == 'y' and not execute == 'yes':
                    keepgoing = False

            if check_cis and (glb_found and cert_found and pool_found 
                and monitor_found and www_dns_found and root_dns_found 
                and edge_action and edge_trigger_1 and edge_trigger_2 and edge_trigger_3):
                print("Ready to remove CIS resources and all associated Schematics workspaces. Are you sure you would like to continue?")
                execute = input("Deleted workspaces and resources cannot be recovered. Input 'y' or 'yes' to execute: ").lower()
                if not execute == 'y' and not execute == 'yes':
                    keepgoing = False

            if keepgoing:
            
                for id in self.w_ids:
                    keepgoing = True
                    while keepgoing:
                        try:
                            if not destroyer is None and id['id'] == destroyer['id'] and check_cis:
                                print("Calling workspace destroy action to remove CIS resources...")
                                workspace_delete_response = schematics_service.delete_workspace(
                                    w_id=id['id'],
                                    destroy_resources=True,
                                    refresh_token=self.token['refresh_token']
                                )
                            else:
                                workspace_delete_response = schematics_service.delete_workspace(
                                    w_id=id['id'],
                                    refresh_token=self.token['refresh_token']
                                )
                            if workspace_delete_response.status_code == 200:
                                num_deleted += 1
                                print("Deleted workspace " + id['id'])
                            keepgoing = False
                        except ApiException as ae:
                            # Error 409 means that the workspace is still busy, we just have to wait for it to finish
                            if ae.http_response.status_code == 409:
                                print('Waiting for workspace actions to complete...')
                                time.sleep(2)
                            else:
                                # Some other error occurred so we need to break out of the loop and end execution
                                print(Color.RED + "ERROR {0}: ".format(ae.http_response.status_code) + ae.message + Color.END)
                                keepgoing = False
                                break
            print("Deleted " + str(num_deleted) + " associated workspaces")
            
    def most_recent(self):
        '''
        Finds the most recent active Schematics workspace related to our github repo.
        '''
        for num in range(len(self.w_ids)):
            if self.w_ids[num]['status'] == 'ACTIVE':
                return self.w_ids[num]
        return None

    def pool_check(self, glb_info):
        '''
        Returns the name of the pool
        '''
        pools = GlobalLoadBalancerPoolsV0.new_instance(crn=self.crn, service_name="cis_services")
        pools.set_service_url(self.api_endpoint)
        pool_response = pools.list_all_load_balancer_pools().get_result()
        for pool in pool_response["result"]:
            if glb_info['pool'] == pool['id']:
                glb_info['monitor'] = pool['monitor']
                return glb_info
        return None

    def glb_check(self) -> bool:
        glb_info = {}
        glb = GlobalLoadBalancerV1.new_instance(
            crn=self.crn,
            zone_identifier=self.zone_id,
            service_name="cis_services"
        )
        glb.set_service_url(self.api_endpoint)
        glb_response = glb.list_all_load_balancers().get_result()
        for balancer in glb_response["result"]:
            if balancer["name"] == self.cis_domain:
                glb_info["glb"] = balancer["id"]
                glb_info["pool"] = balancer["fallback_pool"]
                return glb_info
        return None
    
    def dns_check(self):
        dns_ids = []
        records = DnsRecordsV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services"
        )
        records.set_service_url(self.api_endpoint)
        record_response = records.list_all_dns_records().get_result()
        for record in record_response['result']:
            dns_ids.append(record['id'])
        return dns_ids

    def edge_check(self, access_token: str):
        edge_ids = []
        edge_url = "https://api.cis.cloud.ibm.com/v1/" + self.crn + "/zones/" + self.zone_id + "/workers/routes"

        edge_headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + access_token
        }

        edge_response = requests.request("GET", edge_url, headers=edge_headers)

        for trigger in edge_response.json()['result']:
            edge_ids.append(trigger['id'])
        return edge_ids
    
    def cert_check(self):
        cert = SslCertificateApiV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        cert.set_service_url(self.api_endpoint)
        resp = cert.list_certificates().get_result()
        return resp
