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
import requests, json
from src.common.functions import Color as Color

class EdgeFunctionCreator:
    def __init__(self, crn, app_url, apikey, zone_id, domain, token):
        self.crn = crn
        self.app_url = app_url
        self.apikey = apikey
        self.zone_id = zone_id
        self.domain = domain
        self.fn_name = self.domain.replace('.', '-') # The name of the edge function action
        self.token = token
        #self.token = self.request_token(self.apikey)

    def create_edge_function_action(self):

        action_url = "https://api.cis.cloud.ibm.com/v1/" + self.crn + "/workers/scripts/" + self.fn_name
        
        # The javascript for the edge function action
        action_payload = "addEventListener('fetch', (event) => {\n    const mutable_request = new Request(event.request);\n    event.respondWith(redirectAndLog(mutable_request));\n});\n\nasync function redirectAndLog(request) {\n    const response = await redirectOrPass(request);\n    return response;\n}\n\nasync function getSite(request, site) {\n    const url = new URL(request.url);\n    // let our servers know what origin the request came from\n    // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-Host\n    request.headers.set('X-Forwarded-Host', url.hostname);\n    request.headers.set('host', site);\n    url.hostname = site;\n    url.protocol = \"https:\";\n    response = fetch(url.toString(), request);\n    console.log('Got getSite Request to ' + site, response);\n    return response;\n}\n\nasync function redirectOrPass(request) {\n    const urlObject = new URL(request.url);\n\n    let response = null;\n\n    try {\n        console.log('Got MAIN request', request);\n\n        response = await getSite(request, '"+ self.app_url + "');\n        console.log('Got MAIN response', response.status);\n        return response;\n\n    } catch (error) {\n        // if no action found, play the regular request\n        console.log('Got Error', error);\n        return await fetch(request);\n\n    }\n\n}\n"
        # Headers for the action http request
        action_headers = {
            'Content-Type': 'application/javascript',
            'Accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + self.token
        }
        # Executing the edge function action request
        action_response = requests.request("PUT", url=action_url, headers=action_headers, data=action_payload)

        if action_response.json()["success"]:
            print(Color.GREEN+"Success: Created edge function action"+Color.END)
        else:
            print(Color.RED+"ERROR: Failed to create edge function action with status code " + str(action_response.status_code)+Color.END)

        return action_response

    def create_edge_function_trigger(self):

        trigger_url = "https://api.cis.cloud.ibm.com/v1/" + self.crn + "/zones/" + self.zone_id + "/workers/routes"

        # Trigger 1 handles all subdomains of the CIS domain
        trigger_payload_1 = json.dumps({
            "pattern": self.domain,
            "script": self.fn_name
        })
        trigger_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + self.token
        }
        # Executing the 1st edge function trigger request
        trigger_response_1 = requests.request("POST", url=trigger_url, headers=trigger_headers, data=trigger_payload_1)

        if trigger_response_1.json()["success"]:
            print(Color.GREEN+"SUCCESS: Created edge function trigger"+Color.END)
        elif trigger_response_1.status_code == 409:
            print(Color.YELLOW+"WARNING: Did not create edge function trigger. Trigger already exists"+Color.END)
        else:
            print(Color.RED+"ERROR: Failed to create edge function trigger with status code " + str(trigger_response_1.status_code)+Color.END)
        
        return trigger_response_1

    def create_edge_function_www_trigger(self):

        trigger_url = "https://api.cis.cloud.ibm.com/v1/" + self.crn + "/zones/" + self.zone_id + "/workers/routes"

        trigger_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + self.token
        }

        # Trigger 2 handles the root domain of the CIS domain
        trigger_payload_2 = json.dumps({
            "pattern": "www." + self.domain,
            "script": self.fn_name
        })
        # Executing the 2nd edge function trigger request
        trigger_response_2 = requests.request("POST", url=trigger_url, headers=trigger_headers, data=trigger_payload_2)

        if trigger_response_2.json()["success"]:
            print(Color.GREEN+"SUCCESS: Created edge function trigger"+Color.END)
        elif trigger_response_2.status_code == 409:
            print(Color.YELLOW+"WARNING: Did not create edge function trigger. Trigger already exists"+Color.END)
        else:
            print(Color.RED+"ERROR: Failed to create edge function trigger with status code " + str(trigger_response_2.status_code)+Color.END)

        return trigger_response_2

    def create_edge_function_wild_card_trigger(self):

        trigger_url = "https://api.cis.cloud.ibm.com/v1/" + self.crn + "/zones/" + self.zone_id + "/workers/routes"

        trigger_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + self.token
        }

        # Trigger 2 handles the root domain of the CIS domain
        trigger_payload_3 = json.dumps({
            "pattern": "*." + self.domain,
            "script": self.fn_name
        })
        # Executing the 2nd edge function trigger request
        trigger_response_3 = requests.request("POST", url=trigger_url, headers=trigger_headers, data=trigger_payload_3)

        if trigger_response_3.json()["success"]:
            print(Color.GREEN+"SUCCESS: Created edge function trigger"+Color.END)
        elif trigger_response_3.status_code == 409:
            print(Color.YELLOW+"WARNING: Did not create edge function trigger. Trigger already exists"+Color.END)
        else:
            print(Color.RED+"ERROR: Failed to create edge function trigger with status code " + str(trigger_response_3.status_code)+Color.RED)

        return trigger_response_3

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