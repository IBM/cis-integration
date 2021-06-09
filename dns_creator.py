from logging import NullHandler
import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import DnsRecordsV1
from ibm_cloud_sdk_core import ApiException

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
    root_name = '@' # creating a root DNS record
    www_name = 'www' # creating a www DNS record
    content = os.getenv("APP_URL") # For now an env variable, could be user input
    create_root_record = True # determines whether we need to create a new root record
    root_record = None # the result of creating/updating the root record
    create_www_record = True # determines whether we need to create a new www record
    www_record = None # the result of creating/updating the www record
    curr_records = record.list_all_dns_records() # get the DNS records from the CIS instance
    # check if the DNS records we want to create already exist
    for item in curr_records.result["result"]:
        # checking for the root record
        if item["type"] == "CNAME" and item["zone_name"] == item["name"]:
            create_root_record = False
            root_record = record.update_dns_record(dnsrecord_identifier=item["id"],
                type=record_type, name=root_name, content=content, proxied=True)
        # checking for the www record    
        if item["type"] == "CNAME" and item["name"] == "www." + item["zone_name"]:
            create_www_record = False
            www_record = record.update_dns_record(dnsrecord_identifier=item["id"],
                type=record_type, name=www_name, content=content, proxied=True)

    # create a new root record if one does not already exist
    if create_root_record:
        root_record = record.create_dns_record(
            type=record_type, name=root_name, content=content, proxied=True)
    print(root_record)
        

    # creating a DNS record for the www subdomain if one does not exist already
    if create_www_record:
        www_record = record.create_dns_record(
            type=record_type, name=www_name, content=content, proxied=True)
    print(www_record)

if __name__ == "__main__":
    main()