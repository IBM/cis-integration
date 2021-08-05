import requests
import os
import json
import urllib3
from src.common.functions import Color as Color

class IngressCreator:
    def __init__(self, clusterNameOrID, resourceGroupID, namespace, secretName, serviceName, servicePort, accessToken, refreshToken, ingressSubdomain, iks_master_url):
        self.clusterNameOrID=clusterNameOrID
        self.resourceGroupID=resourceGroupID
        self.namespace=namespace
        self.secretName=secretName
        self.serviceName=serviceName
        self.servicePort=servicePort
        self.accessToken=accessToken
        self.refreshToken=refreshToken
        self.ingressSubdomain=ingressSubdomain
        self.iks_master_url=iks_master_url

    def create_ingress(self):
      urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
      
      if self.iks_master_url =="":
        print(Color.RED+"ERROR: Public service endpoint for IKS Cluster is not enabled"+Color.END)
      #1. get id token to make kubernetes API calls
      url = "https://iam.cloud.ibm.com/identity/token"

      payload="grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey="+os.getenv("CIS_SERVICES_APIKEY")
      headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic a3ViZTprdWJl',
        'cache-control': 'no-cache'
      }
      try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data=json.loads(response.text)
        idToken=data["id_token"]
      except:
        print(Color.RED+"ERROR: Unable to get id token"+Color.END)

      

      #2. apply yaml file through kubernetes API
      url = self.iks_master_url+"/apis/networking.k8s.io/v1beta1/namespaces/"+self.namespace+"/ingresses"
      payload = json.dumps({
        "apiVersion": "networking.k8s.io/v1beta1",
        "kind": "Ingress",
        "metadata": {
          "name": "cis-cert",
          "annotations": {
            "nginx.ingress.kubernetes.io/ssl-redirect": "false"
          }
        },
        "spec": {
          "tls": [
            {
              "hosts": [
                self.ingressSubdomain
              ],
              "secretName": self.secretName
            }
          ],
          "rules": [
            {
              "host": self.ingressSubdomain,
              "http": {
                "paths": [
                  {
                    "path": "/",
                    "backend": {
                      "serviceName": self.serviceName,
                      "servicePort": int(self.servicePort)
                    }
                  }
                ]
              }
            }
          ]
        }
      })
      headers = {
        'Authorization': 'bearer'+' '+idToken,
        'Content-Type': 'application/json'
      }
      try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(Color.GREEN+"SUCCESS: Created ingress file"+Color.END)
        
      except:
        print(Color.RED+"ERROR: Unable to create ingress file"+Color.END)



