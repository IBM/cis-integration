import requests
import json
from src.common.functions import Color as Color

class IngressCreator:
    def __init__(self, clusterNameOrID, resourceGroupID, namespace, secretName, serviceName, servicePort, accessToken, refreshToken, ingressSubdomain, iks_master_url, idToken):
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
        self.idToken=idToken
        
    def create_ingress(self):  

      #1. apply ingress file with the Kubernetes API
      url = self.iks_master_url+"/apis/networking.k8s.io/v1beta1/namespaces/"+self.namespace+"/ingresses"
      payload = json.dumps({
        "apiVersion": "networking.k8s.io/v1beta1",
        "kind": "Ingress",
        "metadata": {
          "name": "cis-ingress",
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
        'Authorization': 'bearer'+' '+self.idToken,
        'Content-Type': 'application/json'
      }
      try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(Color.GREEN+"SUCCESS: Created ingress file"+Color.END)

      except:
        print(Color.RED+"ERROR: Unable to create ingress file"+Color.END)



