import os
from functions import Color as Color
from dotenv import load_dotenv
from ibm_cloud_networking_services import SslCertificateApiV1

def create_cert(crn, zone_id, endpoint, domain):

    hostNames=[domain,"*."+domain]
 
    # create instance
    cert = SslCertificateApiV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    cert.set_service_url(endpoint)

    try:
        resp = cert.order_certificate(x_correlation_id="1864", type="dedicated", hosts=hostNames)
        print(resp)  
        print(Color.GREEN+"Certificate created"+Color.END)
    except:
        print(Color.RED+"ERROR: Unable to create certificate. Make sure hostname(s) match custom domain name"+Color.END)