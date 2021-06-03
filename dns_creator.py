import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import DnsRecordsV1

def main():
    load_dotenv()
    # read crn, zone id and end-point from environment
    crn = os.getenv("CRN")
    zone_id = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")
    # create instance
    record = DnsRecordsV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    record.set_service_url(endpoint)
    record_type = 'CNAME'
    name = '@'
    content = os.getenv("APP_URL") # For now an env variable, could be user input
    resp = record.create_dns_record(
        type=record_type, name=name, content=content)
    print(resp)

if __name__ == "__main__":
    main()