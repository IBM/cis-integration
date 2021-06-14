import os
from dotenv import load_dotenv
from ibm_cloud_networking_services import SslCertificateApiV1

def main():
    load_dotenv()
    # read crn, zone id and end-point from environment
    crn = os.getenv("CRN")
    zone_id = os.getenv("ZONE_ID")
    endpoint = os.getenv("API_ENDPOINT")

    hostNames=["gcat-interns-rock.com"]

    # create instance
    cert = SslCertificateApiV1.new_instance(
        crn=crn, zone_identifier=zone_id, service_name="cis_services")
    cert.set_service_url(endpoint)
    resp = cert.order_certificate(x_correlation_id="1864", type="dedicated", hosts=hostNames)
    print(resp)

if __name__ == "__main__":
    main()
