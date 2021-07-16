import requests, json
from src.functions import Color as Color

class SecretCertificateCreator:

    def __init__(self, cis_crn, cluster_id, cis_domain, cert_manager_crn, cert_name, token):
        self.cis_crn = cis_crn
        self.cluster_id = cluster_id
        self.cis_domain = cis_domain
        self.cert_manager_crn = cert_manager_crn
        self.cert_name = cert_name
        self.token = token

    def create_secret(self):
        cert_url = "https://containers.cloud.ibm.com/global/ingress/v2/secret/createSecret"
        
        # Creating the data required for the request
        cert_data = json.dumps({
            "cluster": self.cluster_id,
            "crn": self.cert_manager_crn,
            "name": self.cert_name,
            "namespace": "default",
            "persistence": True
        })

        # Creating the headers required for the request
        cert_headers = {
            "Content-Type": 'application/json',
            "Accept": 'application/json',
            "Authorization": 'Bearer ' + self.token
        }

        cert_response = requests.request("POST", url=cert_url, headers=cert_headers, data=cert_data)
        
        if cert_response.status_code == 200:
            print(Color.GREEN+"SUCCESS: Created secret for IKS"+Color.END)
        else:
            print(Color.RED+"ERROR: Failed to create secret for IKS with error code " + str(cert_response.status_code) + Color.END)

        return cert_response

    def check_certificate(self):
        url_cert_man_crn = self.URLify(self.cert_manager_crn)
        try:
            region = self.cert_manager_crn.split(":")[5]
        except:
            print(Color.RED+"ERROR: CRN provided not in correct format"+Color.END)
            exit(1)

        cert_check_url = f"https://{region}.certificate-manager.cloud.ibm.com/api/v3/{url_cert_man_crn}/certificates/"

        cert_check_headers = {
            "Authorization": 'Bearer ' + self.token
        }

        cert_check_response = requests.request("GET", url=cert_check_url, headers=cert_check_headers)
        for cert in cert_check_response.json()["certificates"]:
            if self.cis_domain in cert["domains"] and ("*." + self.cis_domain) in cert["domains"]:
                print("Certificate with domain already exists in certificate manager")
                return cert["_id"]
        
        print("Ordering a certificate for the certificate manager...")

        cert_create_url = f"https://{region}.certificate-manager.cloud.ibm.com/api/v1/{url_cert_man_crn}/certificates/order"

        cert_create_data = json.dumps({
            "name": self.cert_name,
            "domains": [self.cis_domain, "*."+self.cis_domain],
            "dns_provider_instance_crn": self.cis_crn
        })

        cert_create_headers = {
            "Content-Type": 'application/json',
            "authorization": 'Bearer ' + self.token
        }

        cert_create_response = requests.request("POST", url=cert_create_url, headers=cert_create_headers, data=cert_create_data)
       
        print(Color.GREEN+"SUCESS: Ordered a certificate for the certificate manager!"+Color.END)
        return cert_create_response.json()["_id"]
        

    def URLify(self, replacement_str):
        new_string = replacement_str.replace(":", "%3A")
        return new_string.replace("/", "%2F")