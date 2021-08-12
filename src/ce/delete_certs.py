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
from ibm_cloud_networking_services import SslCertificateApiV1
from requests.models import stream_decode_response_unicode

class DeleteCerts:
    def __init__(self, crn: str, zone_id: str, endpoint: str, cis_domain: str) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = endpoint
        self.cis_domain = cis_domain

    def delete_certs(self):
        certIds=[]
        execute = input("Delete TLS Certificates? Input 'y' or 'yes' to execute: ").lower()

        if execute == 'y' or execute == 'yes':
            # create instance
            cert = SslCertificateApiV1.new_instance(
                crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
            cert.set_service_url(self.endpoint)
            resp = cert.list_certificates()
            
            for cert in resp.result['result']:
                if self.cis_domain in cert['hosts'] or '*.' + self.cis_domain in cert['hosts']:
                    certIds.append(cert['id']) 
            
            #deleting certificates
            
            for id in certIds:
                cert = SslCertificateApiV1.new_instance(
                    crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
                cert.set_service_url(self.endpoint)
                resp = cert.delete_certificate(
                    cert_identifier=id)
                
            print("Deleted",len(certIds),"affiliated certificates")