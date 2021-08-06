import requests
import json
from src.common.functions import Color as Color

class DeleteIngress:
    def __init__(self, namespace, id_token, iks_master_url) -> None:
        self.namespace = namespace
        self.id_token= id_token
        self.iks_master_url = iks_master_url
    
    def delete_ingress(self):

        #Delete ingress file with Kubernetes API
        url = self.iks_master_url+"/apis/networking.k8s.io/v1beta1/namespaces/"+self.namespace+"/ingresses/cis-ingress"

        payload={}
        headers = {
        'Authorization': 'bearer '+self.id_token
        }
        
        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
        data=json.loads(response.text)

        if data["status"]!="Failure":            
            print(Color.GREEN+"SUCCESS: Deleted ingress file"+Color.END)
        else:
            print(Color.RED+"ERROR: Unable to delete ingress file"+Color.END)
