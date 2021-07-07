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
        execute = input("Delete TLS Certificates? Input 'y' to execute: ")

        if execute == 'y':
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