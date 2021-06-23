import os
from .functions import Color as Color
from dotenv import load_dotenv
from ibm_cloud_networking_services import SslCertificateApiV1

<<<<<<< HEAD
class CertificateCreator:
    def create_certificate(self):   
        load_dotenv()
        # read crn, zone id and end-point from environment
        crn = os.getenv("CRN")
        zone_id = os.getenv("ZONE_ID")
        endpoint = os.getenv("API_ENDPOINT")
        hostNames=[os.getenv("CIS_DOMAIN"),"*."+os.getenv("CIS_DOMAIN")]

        #setting tls mode to strict
        cert = SslCertificateApiV1.new_instance(
            crn=crn, zone_identifier=zone_id, service_name="cis_services")
        cert.set_service_url(endpoint)
        try:
            resp = cert.change_ssl_setting(value="strict")
            print(Color.GREEN+"Successfully set TLS mode to End-to-end CA Signed (strict)"+Color.END)
        except:
            print(Color.RED+"ERROR: Unable to set mode TLS mode to End-to-end CA Signed (strict)"+Color.END)

        # checking for duplicated hostnames
        cert = SslCertificateApiV1.new_instance(
            crn=crn, zone_identifier=zone_id, service_name="cis_services")
        cert.set_service_url(endpoint)
        resp = cert.list_certificates()
        for cert in resp.result['result']:
            if set(hostNames) == set(cert['hosts']):
                print(Color.YELLOW+"WARNING: certificate already made with host names: "+" ".join(hostNames)+Color.END)
            return
        # end
    
        # creating certificate
        cert = SslCertificateApiV1.new_instance(
            crn=crn, zone_identifier=zone_id, service_name="cis_services")
        cert.set_service_url(endpoint)

        try:
            resp = cert.order_certificate(x_correlation_id="1864", type="dedicated", hosts=hostNames)
            print(Color.GREEN+"Successfully created certificate"+Color.END)
        except:
            print(Color.RED+"ERROR: Unable to create certificate. Make sure hostname(s) match custom domain name"+Color.END)
=======
def create_cert():
    
    load_dotenv()
    # read crn, zone id and end-point from environment
    crn = os.getenv("CRN")
    zone_id = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")
    hostNames=[os.getenv("CIS_DOMAIN"),"*."+os.getenv("CIS_DOMAIN")]

    #setting tls mode to strict
    cert = SslCertificateApiV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    cert.set_service_url(endpoint)
    try:
        resp = cert.change_ssl_setting(value="strict")
        print(Color.GREEN+"Successfully set TLS mode to End-to-end CA Signed (strict)"+Color.END)
    except:
        print(Color.RED+"ERROR: Unable to set mode TLS mode to End-to-end CA Signed (strict)"+Color.END)

    # checking for duplicated hostnames
    cert = SslCertificateApiV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    cert.set_service_url(endpoint)
    resp = cert.list_certificates()
    for cert in resp.result['result']:
        if set(hostNames) == set(cert['hosts']):
           print(Color.YELLOW+"WARNING: certificate already made with host names: "+" ".join(hostNames)+Color.END)
           return
    # end
 
    # creating certificate
    cert = SslCertificateApiV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    cert.set_service_url(endpoint)

    try:
        resp = cert.order_certificate(x_correlation_id="1864", type="dedicated", hosts=hostNames)
        print(Color.GREEN+"Successfully created certificate"+Color.END)
    except:
        print(Color.RED+"ERROR: Unable to create certificate. Make sure hostname(s) match custom domain name"+Color.END)

>>>>>>> a76c43f (enchanced certcreate.py by checking for duplicates and setting TLS mode to strict)
