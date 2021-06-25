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
    terraforming = None

    # used to create .env file
    def create_envfile(self):
        if not self.terraforming:
            os.environ["CRN"] = self.crn
            os.environ["ZONE_ID"] = self.zone_id
        else:
            os.environ["RESOURCE_GROUP"] = self.resource_group
            os.environ["CIS_NAME"] = self.cis_name

        os.environ["API_ENDPOINT"] = self.api_endpoint
        os.environ["CIS_SERVICES_APIKEY"] = self.cis_api_key
        os.environ["CIS_DOMAIN"] = self.cis_domain
        os.environ["APP_URL"] = self.app_url

        if not self.terraforming:
            info = [f"CRN=\"{self.crn}\"\n", f"ZONE_ID=\"{self.zone_id}\"\n"]
        else:
            info = [f"RESOURCE_GROUP=\"{self.resource_group}\"\n", f"CIS_NAME=\"{self.cis_name}\"\n"]
        
        common = [f"API_ENDPOINT=\"{self.api_endpoint}\"\n", f"CIS_SERVICES_APIKEY=\"{self.cis_api_key}\"\n", f"CIS_DOMAIN=\"{self.cis_domain}\"\n", f"SCHEMATICS_URL=\"{self.schematics_url}\"\n", f"APP_URL=\"{self.app_url}\"\n"]
        for item in common:
            info.append(item)


        file = open("credentials.env", "w")
        file.writelines(info)
        file.close()

    def read_envfile(self, filename,args):
        try:
            file = open(filename, "r")
        except FileNotFoundError:
            print("Env file doesn't exist!")
            sys.exit(1)

        load_dotenv(filename)

        if not self.terraforming:
            if os.getenv("CRN") is None or os.getenv("ZONE_ID") is None:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                args.crn=os.getenv("CRN")
                args.zone_id=os.getenv("ZONE_ID")

        else:
            if os.getenv("RESOURCE_GROUP") is None or os.getenv("CIS_NAME") is None:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
            else:
                args.resource_group=os.getenv("RESOURCE_GROUP")
                args.name=os.getenv("CIS_NAME")
        
        if os.getenv("API_ENDPOINT") is None or os.getenv("CIS_SERVICES_APIKEY") is None or os.getenv("CIS_DOMAIN") is None or os.getenv("APP_URL") is None:
            print("Missing one or more necessary attributes in .env!")
            sys.exit(1)
        else:
            args.cis_domain=os.getenv("CIS_DOMAIN")
            args.app_url=os.getenv("APP_URL")
            self.cis_api_key=os.getenv("CIS_SERVICES_APIKEY")
            self.api_endpoint=os.getenv("API_ENDPOINT")
   