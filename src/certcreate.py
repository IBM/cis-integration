from .functions import Color as Color
from dotenv import load_dotenv
from ibm_cloud_networking_services import SslCertificateApiV1

class CertificateCreator:

    def __init__(self, crn, zone_id, endpoint, domain):
        self.crn = crn
        self.zone_id = zone_id
        self.endpoint = endpoint
        self.hostNames=[domain,"*."+domain]

    def create_certificate(self):   
        #setting tls mode to strict
        cert = SslCertificateApiV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        cert.set_service_url(self.endpoint)
        try:
            resp = cert.change_ssl_setting(value="strict")
            print(Color.GREEN+"Successfully set TLS mode to End-to-end CA Signed (strict)"+Color.END)
        except:
            print(Color.RED+"ERROR: Unable to set mode TLS mode to End-to-end CA Signed (strict)"+Color.END)

        # checking for duplicated hostnames
        cert = SslCertificateApiV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        cert.set_service_url(self.endpoint)
        resp = cert.list_certificates()
        for cert in resp.result['result']:
            if set(self.hostNames) == set(cert['hosts']):
                print(Color.YELLOW+"WARNING: certificate already made with host names: "+" ".join(self.hostNames)+Color.END)
            return
        # end
    
        # creating certificate
        cert = SslCertificateApiV1.new_instance(
            crn=self.crn, zone_identifier=self.zone_id, service_name="cis_services")
        cert.set_service_url(self.endpoint)

        try:
            resp = cert.order_certificate(x_correlation_id="1864", type="dedicated", hosts=self.hostNames)
            print(Color.GREEN+"Successfully created certificate"+Color.END)
        except:
            print(Color.RED+"ERROR: Unable to create certificate. Make sure hostname(s) match custom domain name"+Color.END)
