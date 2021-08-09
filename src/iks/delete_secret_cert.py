import requests

class DeleteSecretCMS:
    def __init__(self, cluster_id, cis_domain, cert_manager_crn, cert_name, token):
        self.cis_crn = cis_crn
        self.cluster_id = cluster_id
        self.cis_domain = cis_domain
        self.cert_manager_crn = cert_manager_crn
        self.cert_name = cert_name
        self.token = token

    def delete_cms_cert(self):
        url = "https://$REGION.certificate-manager.cloud.ibm.com/api/v2/certificate/<URL encoded CRN-based certificateId>"

        payload={}
        headers = {
        'Authorization': 'Bearer $token'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text)

    # Converts the certificate manager CRN into a URL-encoded CRN
    def URLify(self, replacement_str):
        new_string = replacement_str.replace(":", "%3A")
        return new_string.replace("/", "%2F")