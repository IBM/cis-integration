'''
DISCLAIMER OF WARRANTIES:
Permission is granted to copy this Tools or Sample code for internal use only, provided that this
permission notice and warranty disclaimer appears in all copies.

THIS TOOLS OR SAMPLE CODE IS LICENSED TO YOU AS-IS.
IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE,
INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A
PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR ANY DAMAGES ARISING
OUT OF THE USE OF OR INABILITY TO USE THE TOOLS OR SAMPLE CODE, DISTRIBUTION OF THE TOOLS OR SAMPLE CODE,
OR COMBINATION OF THE TOOLS OR SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND
SUPPLIERS BE LIABLE FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL,
CONSEQUENTIAL,INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
'''
import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import GlobalLoadBalancerMonitorV1, GlobalLoadBalancerV1, GlobalLoadBalancerPoolsV0
from ibm_cloud_sdk_core.api_exception import ApiException
from src.common.functions import Color

def get_input(text):
    return input(text)

class DeleteGLB:
    def __init__(self, crn: str, zone_id: str, endpoint: str, cis_domain: str) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = endpoint
        self.cis_domain = cis_domain    
        
    def delete_glb(self):
        # delete the glb
        execute_glb = get_input("Delete global load balancer? Input 'y' or 'yes' to execute: ").lower()
        if execute_glb == 'y' or execute_glb == 'yes':
            globalLoadBalancer = GlobalLoadBalancerV1.new_instance(
                crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
            globalLoadBalancer.set_service_url(self.endpoint)
            balancers = globalLoadBalancer.list_all_load_balancers().get_result()
            glb_id = ''
            pool_id = ''
            keepgoing = True
            for glb in balancers["result"]:
                if glb["name"] == self.cis_domain:
                    glb_id = glb["id"]
                    pool_id = glb["fallback_pool"]
            try:
                if len(glb_id) > 0:
                    glb_delete = globalLoadBalancer.delete_load_balancer(
                        load_balancer_identifier=glb_id).get_result()
                    print(Color.GREEN + "SUCCESS: Deleted global load balancer" + Color.END)
                else:
                    print(Color.RED + "ERROR: No global load balancer associated with domain " + self.cis_domain + " was found" + Color.END)
                    keepgoing = False
            except ApiException as ae:
                print(Color.RED + "ERROR: " + str(ae.http_response.status_code) + " " + ae.message + Color.END)
                exit()

            if keepgoing:
                # delete the origin pool
                execute_origin = get_input("Delete origin pool? Input 'y' or 'yes' to execute: ").lower()
                if execute_origin == 'y' or execute_origin == 'yes':
                    globalLoadBalancerPools = GlobalLoadBalancerPoolsV0.new_instance(
                        crn=self.crn, service_name="cis_services")
                    globalLoadBalancerPools.set_service_url(self.endpoint)
                    monitor_id = ''
                    try:
                        if len(pool_id) > 0:
                            pool = globalLoadBalancerPools.get_load_balancer_pool(
                                pool_identifier=pool_id).get_result()
                            monitor_id = pool["result"]["monitor"]
                            pool_delete = globalLoadBalancerPools.delete_load_balancer_pool(
                                pool_identifier=pool_id).get_result()
                            print(Color.GREEN + "SUCCESS: Deleted origin pool" + Color.END)
                        else:
                            print(Color.RED + "ERROR: No related origin pool was found" + Color.END)
                            keepgoing = False
                            
                    except ApiException as ae:
                        print(Color.RED + "ERROR: " + str(ae.http_response.status_code) + " " + ae.message + Color.END)
                        exit()
                    
                    if keepgoing:
                        # delete the linked health check
                        execute_monitor = get_input("Delete health check monitor? Input 'y' or 'yes' to execute: ").lower()
                        if execute_monitor == 'y' or execute_monitor == 'yes':
                            
                            cert = GlobalLoadBalancerMonitorV1.new_instance(
                                crn=self.crn, service_name="cis_services")
                            cert.set_service_url(self.endpoint)
                            try:
                                if len(monitor_id) > 0:
                                    monitor_delete = cert.delete_load_balancer_monitor(
                                        monitor_identifier=monitor_id).get_result()
                                    print(Color.GREEN + "SUCCESS: Deleted health check" + Color.END)
                                else:
                                    print(Color.RED + "ERROR: No related health check was found" + Color.END)
                            except ApiException as ae:
                                print(Color.RED + "ERROR: " + str(ae.http_response.status_code) + " " + ae.message + Color.END)