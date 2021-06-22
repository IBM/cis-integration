import requests
import os
import sys
from dotenv.main import load_dotenv

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
   
class IntegrationInfo:
    crn = ''
    zone_id = ''
    api_endpoint = 'https://api.cis.cloud.ibm.com'
    app_url = ''
    resource_group = ''
    cis_name = ''
    cis_api_key = ''
    cis_domain = ''
    schematics_url = 'https://us.schematics.cloud.ibm.com'
    github_pat = ''     # might need to be removed later
    terraforming = None

    # used to create .env file
    def create_envfile(self):
        if not self.terraforming:
            os.environ["CRN"] = self.crn
            os.environ["ZONE_ID"] = self.zone_id
        else:
            os.environ["RESOURCE_GROUP"] = self.resource_group
            os.environ["CIS_NAME"] = self.cis_name
            os.environ["GITHUB_PAT"] = self.github_pat

        os.environ["API_ENDPOINT"] = self.api_endpoint
        os.environ["CIS_SERVICES_APIKEY"] = self.cis_api_key
        os.environ["CIS_DOMAIN"] = self.cis_domain
        os.environ["APP_URL"] = self.app_url

        if not self.terraforming:
            info = [f"CRN=\"{self.crn}\"\n", f"ZONE_ID=\"{self.zone_id}\"\n"]
        else:
            info = [f"RESOURCE_GROUP=\"{self.resource_group}\"\n", f"CIS_NAME=\"{self.cis_name}\"\n"]
        
        common = [f"API_ENDPOINT=\"{self.api_endpoint}\"\n", f"CIS_SERVICES_APIKEY=\"{self.cis_api_key}\"\n", f"CIS_DOMAIN=\"{self.cis_domain}\"\n", f"SCHEMATICS_URL=\"{self.schematics_url}\"\n", f"GITHUB_PAT=\"{self.github_pat}\"\n", f"APP_URL=\"{self.app_url}\"\n"]
        for item in common:
            info.append(item)


        file = open("credentials.env", "w")
        file.writelines(info)
        file.close()

    # loads .env file if it exists
    def remove_quotes(self, item):
        result = item
        if result[0] == '"':
            result = result[1:]
        if result[-1] == '"':
            result = result[:-1]
        return result

    def read_envfile(self, filename,args):
        try:
            file = open(filename, "r")
        except FileNotFoundError:
            print("Env file doesn't exist!")
            sys.exit(1)

        # load_dotenv(filename)
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

        if not self.terraforming:
            if "CRN" not in env_vars or "ZONE_ID" not in env_vars:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                args.crn=env_vars["CRN"]
                args.zone_id=env_vars["ZONE_ID"]
        else:
            if "RESOURCE_GROUP" not in env_vars or "CIS_NAME" not in env_vars or "GITHUB_PAT" not in env_vars:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                args.resource_group=env_vars["RESOURCE_GROUP"]
                args.name=env_vars["CIS_NAME"]
                args.pat=env_vars["GITHUB_PAT"]
        
        if "API_ENDPOINT" not in env_vars or "CIS_SERVICES_APIKEY" not in env_vars or "CIS_DOMAIN" not in env_vars or "APP_URL" not in env_vars:
            print("Missing one or more necessary attributes in .env!")
            sys.exit(1)
        else:
            args.cis_domain=env_vars["CIS_DOMAIN"]
            args.app_url=env_vars["APP_URL"]
            self.cis_api_key=env_vars["CIS_SERVICES_APIKEY"]
            self.api_endpoint=env_vars["API_ENDPOINT"]
   