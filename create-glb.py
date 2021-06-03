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
    origins = [{"name": "app-server-1", "address": "www.test.com", "enabled": True, "weight":1}]

    monitor = GlobalLoadBalancerMonitorV1.new_instance(crn=crn, service_name="cis_services")
    health_check = json.dumps(monitor.create_load_balancer_monitor(crn=crn, type="https", expected_body="alive").get_result(), indent=4)
    print(health_check)

    # origin_pools = GlobalLoadBalancerPoolsV0.new_instance(crn=crn, service_name="cis_services")
    # # resp = origin_pools.create_load_balancer_pool(name=name, origins=origins, enabled=True).get_result()
    # resp = json.dumps(origin_pools.list_all_load_balancer_pools().get_result(), indent=4)

if __name__ == "__main__":
    main()