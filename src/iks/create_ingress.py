import requests
import os
import subprocess
from src.common.functions import Color as Color

class IngressCreator:
    def __init__(self, clusterNameOrID, resourceGroupID, namespace, secretName, serviceName, servicePort, accessToken, refreshToken, ingressSubdomain ):
        self.clusterNameOrID=clusterNameOrID
        self.resourceGroupID=resourceGroupID
        self.namespace=namespace
        self.secretName=secretName
        self.serviceName=serviceName
        self.servicePort=servicePort
        self.accessToken= accessToken
        self.refreshToken=refreshToken
        self.ingressSubdomain=ingressSubdomain

    def getKubeConfig(self):

        url = "https://containers.cloud.ibm.com/global/v2/getKubeconfig?cluster="+self.clusterNameOrID

        payload = ""
        headers = {
            'X-Auth-Resource-Group': self.resourceGroupID,
            'X-Auth-Refresh-Token': self.refreshToken,
            'Authorization': self.accessToken,
            'accept': 'application/json'
        }
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            text_file = open("config.txt", "w")
            n = text_file.write(response.text)
            text_file.close()
            os.environ['KUBECONFIG'] = "config.txt"
            print(Color.GREEN+"SUCCESS: Installed kube config file"+Color.END)
            
        except:
            print(Color.RED+"ERROR: Unable to Install kube config file"+Color.END)

    def create_ingress(self):

        #1. setting config
        self.getKubeConfig()

        #2. getting ingressSubdomain
        ingressFileName="ingress.yaml"
  
        
        yaml='''apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: cis-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  tls:
  - hosts:
    - '''+self.ingressSubdomain+'''
    secretName: '''+self.secretName+'''
  rules:
  - host: '''+self.ingressSubdomain+'''
    http:
      paths:
      - path: /
        backend:
          serviceName: '''+self.serviceName+'''
          servicePort: '''+self.servicePort

        #3. create yaml file
        text_file = open(ingressFileName, "w")
        n = text_file.write(yaml)
        text_file.close()

        #4. kubectl sanity check
        try:
            subprocess.check_output(["kubectl", "--help"], stderr=subprocess.STDOUT)
        except:
            print(Color.RED+"ERROR: Kubectl is not installed"+Color.END)

        #5. apply yaml
        try:
        
            subprocess.check_output(["kubectl", "apply", "-f", ingressFileName, "--namespace="+self.namespace], stderr=subprocess.STDOUT)
            print(Color.GREEN+"SUCCESS: Ingress was created"+Color.END)
            
        except subprocess.CalledProcessError as e:
            print(Color.RED+"ERROR: Ingress was not created"+Color.END)
            #6 delete ingress yaml and kube config file
        os.remove(ingressFileName)
        os.remove("config.txt")
        #future enchancements: use kubectl api