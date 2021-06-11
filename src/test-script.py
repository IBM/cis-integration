import os
import json
from dotenv import load_dotenv
from ibm_cloud_networking_services import GlobalLoadBalancerV1

def main():
    load_dotenv()
    # read crn, zone id and end-point from environment
    crn = os.getenv("CRN")
    zone_identifier = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")
    # create instance
    glb = GlobalLoadBalancerV1.new_instance(
        crn=crn, zone_identifier=zone_identifier, service_name="cis_services")
    glb.set_service_url(endpoint)
    resp = json.dumps(glb.list_all_load_balancers().get_result(), indent=4)
    print(resp)

if __name__ == "__main__":
    main()
