import os
import json
from dotenv import load_dotenv
from ibm_cloud_networking_services import GlobalLoadBalancerPoolsV0
from ibm_cloud_networking_services import GlobalLoadBalancerV1
from ibm_cloud_networking_services import GlobalLoadBalancerMonitorV1

def main():
    load_dotenv()

    crn = os.getenv("CRN")
    zone_identifier = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")

    name = "test-lb-pool1"
    origins = [{"name": "app-server-1", "address": "alpha1.example.com", "enabled": True, "weight":1}]

    monitor = GlobalLoadBalancerMonitorV1.new_instance(crn=crn, service_name="cis_services")
    health_check = monitor.create_load_balancer_monitor(description="test-monitor", crn=crn, type="https", expected_codes="2xx", follow_redirects=True).get_result()
    monitor_id = health_check["result"]["id"]
    print("Monitor ID:", monitor_id)

    origin_pools = GlobalLoadBalancerPoolsV0.new_instance(crn=crn, service_name="cis_services")
    origin_pool_result = origin_pools.create_load_balancer_pool(name=name, origins=origins, enabled=True, monitor=monitor_id).get_result()
    origin_pool_id = origin_pool_result["result"]["id"]
    print("Origin Pool ID:", origin_pool_id)

    global_load_balancer = GlobalLoadBalancerV1.new_instance(crn=crn, zone_identifier=zone_identifier, service_name="cis_services")
    global_load_balancer.set_service_url(endpoint)
    global_load_balancer_result = global_load_balancer.create_load_balancer(name="alpha1.example.com", default_pools=[origin_pool_id], fallback_pool=origin_pool_id, enabled=True, proxied=True).get_result()
    global_load_balancer_id = global_load_balancer_result["result"]["id"]
    print("Global Load Balancer ID:", global_load_balancer_id)

if __name__ == "__main__":
    main()