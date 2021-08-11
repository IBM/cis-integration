import requests
from src.common.functions import Color as Color

class DeleteSecretCMS:
    region = ''


    def __init__(self, cluster_id, cis_domain, cert_manager_crn, cert_name, token):
        self.cluster_id = cluster_id
        self.cis_domain = cis_domain
        self.cert_manager_crn = cert_manager_crn
        self.cert_name = cert_name
        self.token = token

    def delete_cms_cert(self):
        cert_id = self.check_certificate()
        if not cert_id is None:
            url_cert_id = self.URLify(cert_id)
            url = f"https://{self.region}.certificate-manager.cloud.ibm.com/api/v2/certificate/{url_cert_id}"

            payload={}
            headers = {
            'Authorization': 'Bearer ' + self.token
            }

            response = requests.request("DELETE", url, headers=headers, data=payload)
            if response.status_code == 200:

                print("Certificate successfully deleted")
            else:
                print("Failed to remove certificate from Certificate Manager")
        else:
            print("Failed to find certificate in Certificate Manager")

    def check_certificate(self):
        url_cert_man_crn = self.URLify(self.cert_manager_crn)
        try:
            self.region = self.cert_manager_crn.split(":")[5]
        except:
            print(Color.RED+"ERROR: CRN provided not in correct format"+Color.END)
            exit(1)

        cert_check_url = f"https://{self.region}.certificate-manager.cloud.ibm.com/api/v3/{url_cert_man_crn}/certificates/"
        cert_check_headers = {
            "Authorization": 'Bearer ' + self.token
        }

        # Gets all certificates previously present in the certificate manager
        cert_check_response = requests.request(
            "GET", url=cert_check_url, headers=cert_check_headers)
        # print(cert_check_response.text)
        # If a valid certificate exists, it returns the CRN of that certificate
        if cert_check_response.status_code == 200:
            for cert in cert_check_response.json()["certificates"]:
                if self.cis_domain in cert["domains"] and ("*." + self.cis_domain) in cert["domains"] and cert["name"] == self.cert_name:
                    print(
                        "Certificate found in certificate manager")
                    return cert["_id"]
        return None

    # Converts the certificate manager CRN into a URL-encoded CRN
    def URLify(self, replacement_str):
        new_string = replacement_str.replace(":", "%3A")
        return new_string.replace("/", "%2F")