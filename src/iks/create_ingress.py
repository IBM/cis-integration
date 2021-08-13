'''
DISCLAIMER OF WARRANTIES:
Permission is granted to copy this Tools or Sample code for internal use only, provided that this
permission notice and warranty disclaimer appears in all copies.

THIS TOOLS OR SAMPLE CODE IS LICENSED TO YOU AS-IS.
IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE,
INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A
PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR ANY DAMAGES ARISING
OUT OF THE USE OF OR INABILITY TO USE THE TOOLS OR SAMPLE CODE, DISTRIBUTION OF THE TOOLS OR SAMPLE CODE,
OR COMBINATION OF THE TOOLS OR SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND
SUPPLIERS BE LIABLE FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL,
CONSEQUENTIAL,INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
'''
import requests
import os
import json
import urllib3
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
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
      'Authorization': 'bearer'+' '+ self.idToken,
      'Content-Type': 'application/json'
    }
    try:
      response = requests.request("POST", url, headers=headers, data=payload, verify=False)
      print(Color.GREEN+"SUCCESS: Created ingress file"+Color.END)
      
    except:
      print(Color.RED+"ERROR: Unable to create ingress file"+Color.END)



