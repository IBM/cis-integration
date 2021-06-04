import os
import json
from dotenv import load_dotenv
from ibm_cloud_networking_services import GlobalLoadBalancerPoolsV0
from ibm_cloud_networking_services import GlobalLoadBalancerV1
from ibm_cloud_networking_services import GlobalLoadBalancerMonitorV1
from ibm_cloud_networking_services import *

def main():
    load_dotenv()

    crn = os.getenv("CRN")
    zone_identifier = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")

    name = "test-lb-pool1"
    origins = [{"name": "app-server-1", "address": "gcat-interns-rock.com", "enabled": True, "weight":1}]

    monitor = GlobalLoadBalancerMonitorV1.new_instance(crn=crn, service_name="cis_services")
    health_check = monitor.create_load_balancer_monitor(description="test-monitor-2", crn=crn, type="https", expected_codes="2xx", follow_redirects=True).get_result()
    monitor_id = health_check["result"]["id"]
    print("Monitor ID:", monitor_id)

    origin_pools = GlobalLoadBalancerPoolsV0.new_instance(crn=crn, service_name="cis_services")
    origin_pool_name_check_resp = origin_pools.list_all_load_balancer_pools().get_result()["result"]
    
    origin_pools_dict = {}
    for i in range(len(origin_pool_name_check_resp)):
        origin_pools_dict[origin_pool_name_check_resp[i]["name"]] = origin_pool_name_check_resp[i]["id"]

    if name not in origin_pools_dict:
        origin_pool_result = origin_pools.create_load_balancer_pool(name=name, origins=origins, enabled=True, monitor=monitor_id).get_result()
        origin_pool_id = origin_pool_result["result"]["id"]
    else:
        print("A origin pool with that name already exists.")
        origin_pool_id = origin_pools_dict[name]
        origin_pools.edit_load_balancer_pool(origin_pool_id, name=name, origins=origins, enabled=True, monitor=monitor_id)

    print("Origin Pool ID:", origin_pool_id)

    load_bal_name = "gcat-interns-rock.com"

    global_load_balancer = GlobalLoadBalancerV1.new_instance(crn=crn, zone_identifier=zone_identifier, service_name="cis_services")
    global_load_balancer.set_service_url(endpoint)
    glb_name_check_resp = global_load_balancer.list_all_load_balancers().get_result()["result"]

    glb_dict = {}
    for i in range(len(glb_name_check_resp)):
        glb_dict[glb_name_check_resp[i]["name"]] = glb_name_check_resp[i]["id"]

    if load_bal_name not in glb_dict:
        global_load_balancer_result = global_load_balancer.create_load_balancer(name=load_bal_name, default_pools=[origin_pool_id], fallback_pool=origin_pool_id, enabled=True, proxied=True).get_result()
        global_load_balancer_id = global_load_balancer_result["result"]["id"]
    else:
        print("A global load balancer with this name already exists.")
        global_load_balancer_id = glb_dict[name]
        global_load_balancer.edit_load_balancer(global_load_balancer_id, name=load_bal_name, default_pools=[origin_pool_id], fallback_pool=origin_pool_id, enabled=True, proxied=True)

    print("Global Load Balancer ID:", global_load_balancer_id)

if __name__ == "__main__":
    main()