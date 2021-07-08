import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import DnsRecordsV1
from ibm_cloud_sdk_core.api_exception import ApiException
from src.functions import Color

class DeleteDNS:
    def __init__(self, crn: str, zone_id: str, endpoint: str, cis_domain: str) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = endpoint
        self.cis_domain = cis_domain

    def delete_dns(self):
        execute = input("Delete DNS Records? Input 'y' or 'yes' to execute: ").lower()
        if execute == 'y' or execute == 'yes':
            # create instance
            record = DnsRecordsV1.new_instance(
                crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
            record.set_service_url(self.endpoint)
            records = record.list_all_dns_records().get_result()
            root_id = ''
            www_id = ''
            for dns in records["result"]:
                if dns["name"] == self.cis_domain:
                    root_id = dns["id"]
                elif dns["name"] == 'www.' + self.cis_domain:
                    www_id = dns["id"]
            if len(root_id) > 0:
                try:
                    root_delete = record.delete_dns_record(
                        dnsrecord_identifier=root_id
                    ).get_result()
                    print(Color.GREEN+"SUCCESS: Deleted '@' record"+Color.END)
                except ApiException as ae:
                    print(Color.RED + "ERROR: Could not delete '@' record with message: " + str(ae.http_response.status_code) + " " + ae.message + Color.END) 
            else:
                print(Color.RED + "ERROR: No '@' DNS record found" + Color.END)
            if len(www_id) > 0:
                try:
                    www_delete = record.delete_dns_record(
                        dnsrecord_identifier=www_id
                    ).get_result()
                    print(Color.GREEN+"SUCCESS: Deleted 'www' record"+Color.END)
                except ApiException as ae:
                    print(Color.RED + "ERROR: Could not delete 'www' record with message: " + str(ae.http_response.status_code) + " " + ae.message + Color.END) 
            else:
                print(Color.RED + "ERROR: No 'www' DNS record found" + Color.END)