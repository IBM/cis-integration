import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import DnsRecordsV1

def main():
    env_path = input("Enter the path for your .env file: ")
    load_dotenv(env_path)
    # read crn, zone id and end-point from environment
    crn = os.getenv("CRN")
    zone_id = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")
    # create instance
    record = DnsRecordsV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    record.set_service_url(endpoint)
    record_type = 'CNAME'
    name = '@' # creating a root DNS record
    content = os.getenv("APP_URL") # For now an env variable, could be user input
    resp1 = record.create_dns_record(
        type=record_type, name=name, content=content)
    print(resp1)

    # creating a DNS record for the www subdomain
    name = 'www'
    resp2 = record.create_dns_record(
        type=record_type, name=name, content=content)
    print(resp2)

if __name__ == "__main__":
    main()