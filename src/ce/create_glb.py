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

from ibm_cloud_networking_services import GlobalLoadBalancerPoolsV0
from ibm_cloud_networking_services import GlobalLoadBalancerV1
from ibm_cloud_networking_services import GlobalLoadBalancerMonitorV1
from ibm_cloud_networking_services import *
from src.common.functions import Color as Color

class GLB:
    def __init__(self, crn, zone_identifier, api_endpoint, domain):
        # Setting up connection to project-specific .env file
        # load_dotenv()

        # Getting info from .env
        self.crn = crn
        self.zone_identifier = zone_identifier
        self.endpoint = api_endpoint
        self.hostname = domain
        self.monitor_id = ''
        self.origin_pool_id = ''

    def create_load_balancer_monitor(self):
        # Setting up and creating the monitor (health check)

        monitor = GlobalLoadBalancerMonitorV1.new_instance(crn=self.crn, service_name="cis_services")
        health_check = monitor.create_load_balancer_monitor(description="default health check", crn=self.crn, type="https", expected_codes="2xx", follow_redirects=True).get_result()
        self.monitor_id = health_check["result"]["id"]
        print(Color.GREEN+"SUCCESS: Monitor created ID:", self.monitor_id+Color.END)
        return health_check

    def create_origin_pool(self):
        # Setting up and creating the origin pool

        name = 'default-pool'
        origin_name = 'default-origin'
        origins = [{"name": origin_name, "address": self.hostname, "enabled": True, "weight":1}]

        origin_pools = GlobalLoadBalancerPoolsV0.new_instance(crn=self.crn, service_name="cis_services")
        origin_pool_name_check_resp = origin_pools.list_all_load_balancer_pools().get_result()["result"]
        
        # Checking to ensure that no currently present origin pool has the name we wish to use
        origin_pools_dict = {}
        for i in range(len(origin_pool_name_check_resp)):
            origin_pools_dict[origin_pool_name_check_resp[i]["name"]] = origin_pool_name_check_resp[i]["id"]

        if name not in origin_pools_dict:
            origin_pool_result = origin_pools.create_load_balancer_pool(name=name, origins=origins, enabled=True, monitor=self.monitor_id).get_result()
            self.origin_pool_id = origin_pool_result["result"]["id"]
        else:
            print(Color.YELLOW+"WARNING: An origin pool with that name already exists."+Color.END)
            self.origin_pool_id = origin_pools_dict[name]
            origin_pool_result = origin_pools.edit_load_balancer_pool(self.origin_pool_id, name=name, origins=origins, enabled=True, monitor=self.monitor_id)

        print(Color.GREEN+"SUCCESS: Origin Pool created with ID:", self.origin_pool_id+Color.END)
        return origin_pool_result

    def create_global_load_balancer(self):
        # Setting up and creating the global load balancer
        global_load_balancer = GlobalLoadBalancerV1.new_instance(crn=self.crn, zone_identifier=self.zone_identifier, service_name="cis_services")
        global_load_balancer.set_service_url(self.endpoint)
        glb_name_check_resp = global_load_balancer.list_all_load_balancers().get_result()["result"]

        # Checking to ensure that no currently present global load balancer has the name we wish to use
        glb_dict = {}
        for i in range(len(glb_name_check_resp)):
            glb_dict[glb_name_check_resp[i]["name"]] = glb_name_check_resp[i]["id"]

        if self.hostname not in glb_dict:
            global_load_balancer_result = global_load_balancer.create_load_balancer(name=self.hostname, default_pools=[self.origin_pool_id], fallback_pool=self.origin_pool_id, enabled=True, proxied=True).get_result()
            global_load_balancer_id = global_load_balancer_result["result"]["id"]
        else:
            print(Color.YELLOW+"WARNING: A global load balancer with this name already exists."+Color.END)
            global_load_balancer_id = glb_dict[self.hostname]
            global_load_balancer_result = global_load_balancer.edit_load_balancer(global_load_balancer_id, name=self.hostname, default_pools=[self.origin_pool_id], fallback_pool=self.origin_pool_id, enabled=True, proxied=True)

        print(Color.GREEN+"SUCCESS: Global Load Balancer with ID:", global_load_balancer_id+Color.END)
        return global_load_balancer_result