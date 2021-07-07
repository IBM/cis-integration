from ibm_cloud_networking_services import DnsRecordsV1
from ibm_cloud_sdk_core import ApiException
from src.functions import Color as Color

class DNSCreator:
    def __init__(self, crn, zone_id, api_endpoint, app_url):
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = api_endpoint
        self.content = app_url
    
    def create_records(self):
        # create instance
        record = DnsRecordsV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        record.set_service_url(self.endpoint)
        record_type = 'CNAME'
        root_name = '@' # creating a root DNS record
        www_name = 'www' # creating a www DNS record
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
                print(Color.YELLOW+"WARNING: A '@' DNS Record already exists"+Color.END)
                try:
                    root_record = record.update_dns_record(dnsrecord_identifier=item["id"],
                        type=record_type, name=root_name, content=self.content, proxied=True)
                    print(Color.GREEN+"SUCCESS: DNS Record updated!"+Color.END+"\nDNS Record name: " + root_record.result["result"]["name"] + "\nDNS Record ID: " + root_record.result["result"]["id"] + "\n")
                except ApiException as ae:
                    print(Color.RED + "ERROR: " + ae.message + "\nError occurred when trying to update '@' DNS record. Check your application URL and try again\n" + Color.END)        
            # checking for the www record    
            if item["type"] == "CNAME" and item["name"] == "www." + item["zone_name"]:
                create_www_record = False
                print(Color.YELLOW+"WARNING: A 'www' DNS Record already exists"+Color.END)
                try:
                    www_record = record.update_dns_record(dnsrecord_identifier=item["id"],
                        type=record_type, name=www_name, content=self.content, proxied=True)
                    print(Color.GREEN+"SUCCESS: DNS Record created!"+Color.END+"\nDNS Record name: " + www_record.result["result"]["name"] + "\nDNS Record ID: " + www_record.result["result"]["id"] + "\n")
                except ApiException as ae:
                    print(Color.RED + "ERROR: " + ae.message + "\nError occurred when trying to update 'www' DNS record. Check your application URL and try again\n" + Color.END)

        # create a new root record if one does not already exist
        if create_root_record:
            try:
                root_record = self.create_root_record(record, record_type, root_name)
                print(Color.GREEN+"SUCCESS: DNS Record created!"+Color.END+"\nDNS Record name: " + root_record.result["result"]["name"] + "\nDNS Record ID: " + root_record.result["result"]["id"] + "\n")
            except ApiException as ae:
                print(Color.RED + "ERROR: " + ae.message + "\nError occurred when trying to create '@' DNS record. Check your application URL and try again\n" + Color.END)
        
        

        if create_www_record:
            try:
                www_record = self.create_www_record(record, record_type, www_name)
                print(Color.GREEN+"SUCCESS: DNS Record created!"+Color.END+"\nDNS Record name: " + www_record.result["result"]["name"] + "\nDNS Record ID: " + www_record.result["result"]["id"] + "\n")
            except ApiException as ae:
                print(Color.RED + "ERROR: " + ae.message + "\nError occurred when trying to create 'www' DNS record. Check your application URL and try again\n" + Color.END)
        

        return (root_record, www_record)

    def create_root_record(self, record, record_type, root_name):
        root_record = record.create_dns_record(type=record_type, name=root_name, content=self.content, proxied=True)
        return root_record

    def create_www_record(self, record, record_type, www_name):
        www_record = record.create_dns_record(type=record_type, name=www_name, content=self.content, proxied=True)
        return www_record
