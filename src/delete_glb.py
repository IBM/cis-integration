import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import GlobalLoadBalancerMonitorV1, GlobalLoadBalancerV1, GlobalLoadBalancerPoolsV0
from ibm_cloud_sdk_core.api_exception import ApiException
from src.functions import Color

class DeleteGLB:
    def __init__(self, crn: str, zone_id: str, endpoint: str, cis_domain: str) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = endpoint
        self.cis_domain = cis_domain
        
    def delete_glb(self):
        # delete the glb
        globalLoadBalancer = GlobalLoadBalancerV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        globalLoadBalancer.set_service_url(self.endpoint)
        balancers = globalLoadBalancer.list_all_load_balancers().get_result()
        for glb in balancers["result"]:
            if glb["name"] == self.cis_domain:
                glb_id = glb["id"]
                pool_id = glb["fallback_pool"]
        try:
            glb_delete = globalLoadBalancer.delete_load_balancer(
                load_balancer_identifier=glb_id).get_result()
            print(Color.GREEN + "SUCCESS: Deleted global load balancer" + Color.END)
        except ApiException as ae:
            print(Color.RED + "ERROR: " + ae.http_response + " " + ae.message + Color.END)
            exit()

        # delete the origin pool
        
        globalLoadBalancerPools = GlobalLoadBalancerPoolsV0.new_instance(
            crn=self.crn, service_name="cis_services")
        globalLoadBalancerPools.set_service_url(self.endpoint)
        try:
            pool = globalLoadBalancerPools.get_load_balancer_pool(
                pool_identifier=pool_id).get_result()
            monitor_id = pool["result"]["monitor"]
            pool_delete = globalLoadBalancerPools.delete_load_balancer_pool(
                pool_identifier=pool_id).get_result()
            print(Color.GREEN + "SUCCESS: Deleted origin pool" + Color.END)
        except ApiException as ae:
            print(Color.RED + "ERROR: " + ae.http_response + " " + ae.message + Color.END)
            exit()
        
        # delete the linked health check
        cert = GlobalLoadBalancerMonitorV1.new_instance(
            crn=self.crn, service_name="cis_services")
        cert.set_service_url(self.endpoint)
        try:
            monitor_delete = cert.delete_load_balancer_monitor(
                monitor_identifier=monitor_id).get_result()
            print(Color.GREEN + "SUCCESS: Deleted health check" + Color.END)
        except ApiException as ae:
            print(Color.RED + "ERROR: " + ae.http_response + " " + ae.message + Color.END)