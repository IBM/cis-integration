import requests
import sys
from ibm_platform_services import ResourceControllerV2
from ibm_cloud_networking_services import ZonesV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def healthCheck(hostUrl):
   print("Checking if",hostUrl,"is up...")
   try:
      requests.request("GET", hostUrl)
      print(Color.GREEN+hostUrl,"has successfully been deployed."+Color.END)
   except:
      print(Color.YELLOW+hostUrl,"is not up yet. May take a few minutes to start."+Color.END)

# A way to load variables from the "credentials.env" file without risk of overwriting env variables in the current session
def load_vars(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("Env file doesn't exist!")
        sys.exit(1)

    env_vars = {}
    lines = file.readlines()
    for line in lines:
        if line[-1] == '\n':
            line = line[:-1]
        components = line.split("=")

        if components[1][0] == '"':
            components[1] = components[1][1:]
        if components[1][-1] == '"':
            components[1] = components[1][:-1]
        
        env_vars[components[0]] = components[1]
    
    return env_vars
   
# Keeping track of all of the necessary attributes that result from the integration of Internet Services and an application
class IntegrationInfo:
    crn = ''
    zone_id = ''
    api_endpoint = 'https://api.cis.cloud.ibm.com'
    iks_cluster_id = ''
    app_url = ''
    resource_group = ''
    cis_name = ''
    cis_api_key = ''
    cis_domain = ''
    schematics_url = 'https://us.schematics.cloud.ibm.com'
    terraforming = False
    verbose = False
    delete = False
    token = None
    vpc_name = ''

    # loads .env file if it exists
    def read_envfile(self, filename):
        env_vars = load_vars(filename)

        if not self.terraforming:
            if "CRN" not in env_vars or "ZONE_ID" not in env_vars:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                self.crn=env_vars["CRN"]
                self.zone_id=env_vars["ZONE_ID"]
        else:
            if "RESOURCE_GROUP" not in env_vars or "CIS_NAME" not in env_vars:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                self.resource_group=env_vars["RESOURCE_GROUP"]
                self.cis_name=env_vars["CIS_NAME"]

        
        if "API_ENDPOINT" not in env_vars or "CIS_SERVICES_APIKEY" not in env_vars or "CIS_DOMAIN" not in env_vars or "APP_DOMAIN" not in env_vars:
            print("Missing one or more necessary attributes in .env!")
            sys.exit(1)
        else:
            self.cis_domain=env_vars["CIS_DOMAIN"]
            self.app_url=env_vars["APP_DOMAIN"]
            self.cis_api_key=env_vars["CIS_SERVICES_APIKEY"]
            self.api_endpoint=env_vars["API_ENDPOINT"]
    
    def request_token(self):
            """
            Requests an access token for the client so that we can execute the plan and apply commands in
            the workspace.
            
            param: apikey is the client's IBM Cloud Apikey
            returns: the generated access token
            """
            data={'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': self.cis_api_key}
            headers= {'Accept': 'application/json',
                    'Content-type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic Yng6Yng='}
            url="https://iam.cloud.ibm.com/identity/token"
            self.token = requests.post(url=url, data=data, headers=headers).json()
            return self.token

    def get_iks_info(self):

        url = "https://containers.cloud.ibm.com/global/v1/nlb-dns/clusters/" + self.iks_cluster_id + "/list"

        headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + self.token["access_token"]
        }

        response = requests.request("GET", url, headers=headers).json()

        for cluster in response["nlbs"]:
            if cluster["clusterID"] == self.iks_cluster_id:
                self.app_url = cluster["nlbHost"]
        return response



    def get_crn_and_zone(self) -> bool:
        '''
        Returns the True if the cis instance information was found
        '''
        authenticator = IAMAuthenticator(self.cis_api_key)
        controller = ResourceControllerV2(authenticator=authenticator)
        resource_list = controller.list_resource_instances(name=self.cis_name, type="service_instance").get_result()
        if len(resource_list["resources"]) > 0:
            for resource in resource_list["resources"]:
                if resource["name"] == self.cis_name:
                    self.crn = resource["id"]
        else:
            print(Color.RED + "ERROR: Could not find a CIS instance with the name " + self.cis_name + Color.END)
            return False
        zone = ZonesV1.new_instance(
            crn=self.crn, service_name="cis_services"
        )
        zone.set_service_url(self.api_endpoint) # change to var
        zone_response = zone.list_zones().get_result()
        for z in zone_response["result"]:
            if z["name"] == self.cis_domain:
                self.zone_id = z["id"]
        return True
   