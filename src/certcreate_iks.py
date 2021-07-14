import requests, json
from src.functions import Color as Color

class SecretCertificateCreator:

    def __init__(self, cluster_id, cert_manager_crn, cert_name, apikey, token):
        self.cluster_id = cluster_id
        self.cert_manager_crn = cert_manager_crn
        self.cert_name = cert_name
        self.apikey = apikey
        self.token = token

    def create_certificate(self):
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
            print(Color.GREEN+"SUCCESS: Created TLS certificate for IKS"+Color.END)
        else:
            print(Color.RED+"ERROR: Failed to create TLS certificate for IKS with error code " + str(cert_response.status_code) + Color.END)

        return cert_response
    
    '''
    def request_token(self, apikey: str):
        """
        Requests an access token for the client so that we can execute the plan and apply commands in
        the workspace.
        
        param: apikey is the client's IBM Cloud Apikey
        returns: the generated access token
        """
        data={'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': apikey}
        headers= {'Accept': 'application/json',
                'Content-type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic Yng6Yng='}
        url="https://iam.cloud.ibm.com/identity/token"
        token = requests.post(url=url, data=data, headers=headers)
        return token.json()["access_token"]
    '''
