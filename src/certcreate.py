import os
from src.functions import Color as Color
from dotenv import load_dotenv
from ibm_cloud_networking_services import SslCertificateApiV1

def main():
    load_dotenv()
    # read crn, zone id and end-point from environment
    crn = os.getenv("CRN")
    zone_id = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")

    string = input("Enter hostname(s). Seperate hostnames by space if neccesary: ")
    hostNames=string.split()
 
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

if __name__ == "__main__":
    main()
