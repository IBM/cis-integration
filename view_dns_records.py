import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import DnsRecordsV1

def main():
    env_path = input("List the path to the .env file")
    load_dotenv(env_path)
    # read crn, zone id and end-point from environment
    crn = os.getenv("CRN")
    zone_id = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")
    # create instance
    record = DnsRecordsV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    record.set_service_url(endpoint)
    resp = record.list_all_dns_records()
    #print(resp.result)
    for item in resp.result["result"]:
        print(item["name"])
    

if __name__ == "__main__":
    main()