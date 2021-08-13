'''
DISCLAIMER OF WARRANTIES:
Permission is granted to copy this Tools or Sample code for internal use only, provided that this
permission notice and warranty disclaimer appears in all copies.

THIS TOOLS OR SAMPLE CODE IS LICENSED TO YOU AS-IS.
IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE,
INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A
PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR ANY DAMAGES ARISING
OUT OF THE USE OF OR INABILITY TO USE THE TOOLS OR SAMPLE CODE, DISTRIBUTION OF THE TOOLS OR SAMPLE CODE,
OR COMBINATION OF THE TOOLS OR SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND
SUPPLIERS BE LIABLE FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL,
CONSEQUENTIAL,INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
'''

import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import DnsRecordsV1
from ibm_cloud_sdk_core.api_exception import ApiException
from src.common.functions import Color

def get_input(text):
    return input(text)

class DeleteDNS:
    def __init__(self, crn: str, zone_id: str, endpoint: str, cis_domain: str) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = endpoint
        self.cis_domain = cis_domain

    def delete_dns(self):
        execute = get_input("Delete DNS Records? Input 'y' or 'yes' to execute: ").lower()
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