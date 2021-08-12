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
        
        try:
            response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
            data=json.loads(response.text)

            if data["status"]!="Failure":            
                print(Color.GREEN+"SUCCESS: Deleted ingress file"+Color.END)
            else:
                print(Color.RED+"ERROR: Unable to delete ingress file"+Color.END)
        except:
            print(Color.RED+"ERROR: Unable to delete ingress file"+Color.END)
