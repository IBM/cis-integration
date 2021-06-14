import requests, os, json
from dotenv import load_dotenv

class EdgeFunctionCreator:
    def create_edge_function(self):
        load_dotenv("./credentials.env")
        crn = os.getenv("CRN")
        app_url = os.getenv("APP_URL")
        apikey = os.getenv("CIS_SERVICES_APIKEY")
        zone_id = os.getenv("ZONE_ID")
        domain = os.getenv("CIS_DOMAIN") # The domain associated with the CIS instance
        fn_name = domain.replace('.', '-') # The name of the edge function action
        token = self.request_token(apikey)
        action_url = "https://api.cis.cloud.ibm.com/v1/" + crn + "/workers/scripts/" + fn_name

        # The javascript for the edge function action
        action_payload = "addEventListener('fetch', (event) => {\n    const mutable_request = new Request(event.request);\n    event.respondWith(redirectAndLog(mutable_request));\n});\n\nasync function redirectAndLog(request) {\n    const response = await redirectOrPass(request);\n    return response;\n}\n\nasync function getSite(request, site) {\n    const url = new URL(request.url);\n    // let our servers know what origin the request came from\n    // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-Host\n    request.headers.set('X-Forwarded-Host', url.hostname);\n    request.headers.set('host', site);\n    url.hostname = site;\n    url.protocol = \"https:\";\n    response = fetch(url.toString(), request);\n    console.log('Got getSite Request to ' + site, response);\n    return response;\n}\n\nasync function redirectOrPass(request) {\n    const urlObject = new URL(request.url);\n\n    let response = null;\n\n    try {\n        console.log('Got MAIN request', request);\n\n        response = await getSite(request, '"+ app_url + "');\n        console.log('Got MAIN response', response.status);\n        return response;\n\n    } catch (error) {\n        // if no action found, play the regular request\n        console.log('Got Error', error);\n        return await fetch(request);\n\n    }\n\n}\n"
        # Headers for the action http request
        action_headers = {
            'Content-Type': 'application/javascript',
            'Accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + token
        }
        # Executing the edge function action request
        action_response = requests.request("PUT", url=action_url, headers=action_headers, data=action_payload)

        print("Uploading edge function action: " + action_response)

        trigger_url = "https://api.cis.cloud.ibm.com/v1/" + crn + "/zones/" + zone_id + "/workers/routes"

        # Trigger 1 handles all subdomains of the CIS domain
        trigger_payload_1 = json.dumps({
            "pattern": "*." + domain,
            "script": fn_name
        })
        trigger_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-auth-user-token': 'Bearer ' + token
        }
        # Executing the 1st edge function trigger request
        trigger_response_1 = requests.request("POST", url=trigger_url, headers=trigger_headers, data=trigger_payload_1)

        print("Uploading edge function trigger 1: " + trigger_response_1)
        # Trigger 2 handles the root domain of the CIS domain
        trigger_payload_2 = json.dumps({
            "pattern": domain,
            "script": fn_name
        })
        # Executing the 2nd edge function trigger request
        trigger_response_2 = requests.request("POST", url=trigger_url, headers=trigger_headers, data=trigger_payload_2)

        print("Uploading edge function trigger 2: " + trigger_response_2)

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