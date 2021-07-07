
import requests
from src.functions import Color

class DeleteEdge:
    def __init__(self, crn: str, zone_id: str, cis_domain: str, apikey: str) -> None:
        self.crn = crn
        self.zone_id = zone_id
        self.cis_domain = cis_domain
        self.apikey = apikey

    def delete_edge(self):
        execute = input("Delete edge function? Input 'y' to execute: ")
        if execute == 'y':
            action_name = self.cis_domain.replace('.','-')
            token = self.request_token(self.apikey)
            
            triggers = self.get_triggers(self.crn, self.zone_id, token)

            for trigger in triggers["result"]:
                if trigger["script"] == action_name:
                    self.delete_trigger(self.crn, self.zone_id, trigger["id"], token)
                    print(Color.GREEN + "SUCCESS: Deleted trigger " + trigger["pattern"] + Color.END)

            action_response = self.delete_action(self.crn, action_name, token)
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