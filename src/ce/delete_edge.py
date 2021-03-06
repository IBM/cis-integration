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
from src.common.functions import Color

def get_input(text):
    return input(text)

class DeleteEdge:
    def __init__(self, crn: str, zone_id: str, cis_domain: str, apikey: str, token: str) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.cis_domain = cis_domain
        self.apikey = apikey
        self.token = token

    def delete_edge(self):
        execute = get_input("Delete edge function? Input 'y' or 'yes' to execute: ").lower()
        if execute == 'y' or execute == 'yes':
            action_name = self.cis_domain.replace('.','-')
            #token = self.request_token(self.apikey)
            
            triggers = self.get_triggers(self.crn, self.zone_id, self.token)

            for trigger in triggers["result"]:
                if trigger["script"] == action_name:
                    self.delete_trigger(self.crn, self.zone_id, trigger["id"],self.token)
                    print(Color.GREEN + "SUCCESS: Deleted trigger " + trigger["pattern"] + Color.END)

            action_response = self.delete_action(self.crn, action_name, self.token)
            if action_response["success"]:
                print(Color.GREEN + "SUCCESS: Deleted edge function action with id " + action_response["result"]["id"] + Color.END)
            else:
                print(Color.RED + "ERROR: No edge function action associated with domain " + self.cis_domain + " found" + Color.END)
            #print(ids)

    def get_triggers(self, crn: str, zone_id: str, token: str):
        url = "https://api.cis.cloud.ibm.com/v1/" + crn + "/zones/" + zone_id + "/workers/routes"
        
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-auth-user-token': 'Bearer ' + token
        }

        response = requests.request("GET", url, headers=headers).json()
        return response

    def delete_action(self, crn: str, action_name: str, token: str):
        url = "https://api.cis.cloud.ibm.com/v1/" + crn + "/workers/scripts/" + action_name
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-auth-user-token': 'Bearer ' + token
        }

        response = requests.request("DELETE", url, headers=headers).json()
        return response

    def delete_trigger(self, crn: str, zone_id: str, trigger_id: str, token: str):
        url = "https://api.cis.cloud.ibm.com/v1/" + crn + "/zones/" + zone_id + "/workers/routes/" + trigger_id
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-auth-user-token': 'Bearer ' + token
        }

        response = requests.request("DELETE", url, headers=headers).json()
        return response

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