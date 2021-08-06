from ibm_platform_services.case_management_v1 import Resource
import requests
import sys
import json
from ibm_platform_services import ResourceControllerV2, ResourceManagerV2
from ibm_cloud_networking_services import ZonesV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

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
    print("Checking if", hostUrl, "is up...")
    try:
        requests.request("GET", hostUrl)
        print(Color.GREEN+hostUrl, "has successfully been deployed."+Color.END)
    except:
        print(Color.YELLOW+hostUrl,
              "is not up yet. May take a few minutes to start."+Color.END)

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
    resource_id = ''
    namespace=''
    service_name=''
    secret_name=''
    service_port=''
    cis_name = ''
    cis_api_key = ''
    cert_name= ''
    cis_domain = ''
    schematics_url = 'https://us.schematics.cloud.ibm.com'
    iks_master_url = ''
    terraforming = False
    verbose = False
    delete = False
    standard = False
    token = None
    vpc_name = ''
    id_token = ''

    # loads .env file if it exists
    def read_envfile(self, filename):
        env_vars = load_vars(filename)

        if not self.terraforming:
            if "CRN" not in env_vars or "ZONE_ID" not in env_vars:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                self.crn = env_vars["CRN"]
                self.zone_id = env_vars["ZONE_ID"]
        else:
            if "RESOURCE_GROUP" not in env_vars or "CIS_NAME" not in env_vars:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                self.resource_group = env_vars["RESOURCE_GROUP"]
                self.cis_name = env_vars["CIS_NAME"]

        if "API_ENDPOINT" not in env_vars or "CIS_SERVICES_APIKEY" not in env_vars or "CIS_DOMAIN" not in env_vars or "APP_DOMAIN" not in env_vars:
            print("Missing one or more necessary attributes in .env!")
            sys.exit(1)
        else:
            self.cis_domain = env_vars["CIS_DOMAIN"]
            self.app_url = env_vars["APP_DOMAIN"]
            self.cis_api_key = env_vars["CIS_SERVICES_APIKEY"]
            self.api_endpoint = env_vars["API_ENDPOINT"]
    def get_id_token(self):
        if self.iks_master_url =="":
            print(Color.RED+"ERROR: Public service endpoint for IKS Cluster is not enabled"+Color.END)
        #1. get id token to make Kubernetes API calls
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
            self.id_token = data["id_token"]
        except:
            print(Color.RED+"ERROR: Unable to get id token"+Color.END)

    def request_token(self):
        """
        Requests an access token for the client so that we can execute the plan and apply commands in
        the workspace.

        param: apikey is the client's IBM Cloud Apikey
        returns: the generated access token
        """
        data = {'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
                'apikey': self.cis_api_key}
        headers = {'Accept': 'application/json',
                   'Content-type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Basic Yng6Yng='}
        url = "https://iam.cloud.ibm.com/identity/token"
        self.token = requests.post(url=url, data=data, headers=headers).json()
        return self.token

    def get_iks_info(self):

        url = "https://containers.cloud.ibm.com/global/v2/getCluster?cluster="+self.iks_cluster_id

        payload = ""
        headers = {
          'accept': 'application/json',
          'Authorization': self.token["access_token"],
          'X-Auth-Resource-Group': self.resource_id
        }

        try:
            response = requests.request("GET", url, headers=headers, data=payload)

            data=json.loads(response.text)
            self.app_url=data["ingress"]["hostname"]
            self.iks_master_url=data["serviceEndpoints"]["publicServiceEndpointURL"]
            return data
        except:
            print(Color.RED+"ERROR: Unable to get cluster's data"+Color.END)

    def get_resource_id(self):
        authenticator = IAMAuthenticator(self.cis_api_key)
        manager = ResourceManagerV2(authenticator=authenticator)
        resource = manager.list_resource_groups(
            name=self.resource_group, include_deleted=False).get_result()
        self.resource_id = resource["resources"][0]["id"]
        return self.resource_id

    def get_cms(self):
        authenticator = IAMAuthenticator(self.cis_api_key)
        controller = ResourceControllerV2(authenticator=authenticator)
        resource_list = controller.list_resource_instances(
            name="kube-certmgr-"+self.iks_cluster_id, resource_group_id=self.resource_id).get_result()
        # print(resource_list)
        return resource_list["resources"][0]["id"]

    def get_crn_and_zone(self) -> bool:
        '''
        Returns the True if the cis instance information was found
        '''
        authenticator = IAMAuthenticator(self.cis_api_key)
        controller = ResourceControllerV2(authenticator=authenticator)
        resource_list = controller.list_resource_instances(
            name=self.cis_name, resource_group_id=self.resource_id, type="service_instance").get_result()
        if len(resource_list["resources"]) > 0:
            for resource in resource_list["resources"]:
                if resource["name"] == self.cis_name:
                    self.crn = resource["id"]
        else:
            print(Color.RED + "ERROR: Could not find a CIS instance with the name " +
                  self.cis_name + Color.END)
            return False
        zone = ZonesV1.new_instance(
            crn=self.crn, service_name="cis_services"
        )
        zone.set_service_url(self.api_endpoint)  # change to var
        zone_response = zone.list_zones().get_result()
        for z in zone_response["result"]:
            if z["name"] == self.cis_domain:
                self.zone_id = z["id"]
        return True
