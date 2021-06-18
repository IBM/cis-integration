import sys
import getpass
import os
import certcreate
import argparse
from dotenv.main import load_dotenv
from functions import Color as Color
from create_glb import GLB
from dns_creator import DNSCreator
from create_edge_function import EdgeFunctionCreator
from create_terraform_workspace import WorkspaceCreator

'''
To get python script to run globally run following command: $ pip3 install -e /path/to/script/folder
'''

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

    def read_envfile(self, filename):
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
            if os.getenv("RESOURCE_GROUP") is None or os.getenv("CIS_NAME") is None or os.getenv("GITHUB_PAT") is None:
                print("Missing one or more necessary attributes in .env!")
                sys.exit(1)
        
        if os.getenv("API_ENDPOINT") is None or os.getenv("CIS_SERVICES_APIKEY") is None or os.getenv("CIS_DOMAIN") is None or os.getenv("APP_URL") is None:
            print("Missing one or more necessary attributes in .env!")
            sys.exit(1)
                   

# method used to display the command usage if user uses `-h` or `--help`
def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine\n")

    print(Color.BOLD + "USAGE:" + Color.END)
    print("\t[python implementation]\t\tcis-integration [positional arguments] [global options] [-c CIS CRN] [-z CIS ZONE ID] [-d CIS DOMAIN] [-a CODE ENGINE APP URL]")
    print("\t[terraform implementation]\tcis-integration [positional arguments] [global options] --terraform [-r RESOURCE GROUP] [-n CIS NAME] [-d CIS DOMAIN] [-a CODE ENGINE APP URL] [-p GITHUB PAT]")
    print("\t[use existing credentials.env file]\tcis-integration [positional arguments] [global options] --env\n")

    print(Color.BOLD + "POSITIONAL ARGUMENTS (required):" + Color.END)
    print("\t{code-engine,ce} \t\t connect a Code Engine application to the CIS instance\n")

    print(Color.BOLD + "GLOBAL OPTIONS:" + Color.END)
    print("\t--help, -h \t\t show help")
    print("\t--env, -e \t\t use an already existing credentials.env file")
    print("\t--terraform, -t \t build resources for CIS instance using terraform\n")

    print(Color.BOLD + "OPTIONAL ARGUMENTS:" + Color.END)
    print("\t--crn, -c \t\t CRN of the CIS instance")
    print("\t--zone_id, -z \t\t Zone ID of the CIS instance")
    print("\t--cis_domain, -d \t domain name of the CIS instance")
    print("\t--app_url, -a \t\t URL of the application")
    print("\t--resource_group, -r \t resource group associated with the CIS instance")
    print("\t--name, -n \t\t name of the CIS instance")
    print("\t--pat, -p \t\t GitHub PAT\n")

# handles the arguments given for both the python and terraform command options
def handle_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h","--help",action='store_true')
    parser.add_argument("platform",\
        choices=["code-engine","ce"])
    parser.add_argument("-c","--crn")
    parser.add_argument("-z","--zone_id")
    parser.add_argument("-d","--cis_domain")
    parser.add_argument("-a","--app_url")

    parser.add_argument("-t","--terraform",action='store_true')
    parser.add_argument("-r","--resource_group")
    parser.add_argument("-n","--name")
    parser.add_argument("-p","--pat")
    

    parser.add_argument("-e","--env", action='store_true')
    
    args=parser.parse_args()

    if args.help:
        print_help()
        sys.exit(1)

    UserInfo = IntegrationInfo()
    UserInfo.terraforming = False
    if args.terraform:
        UserInfo.terraforming = True
    if args.env:
        UserInfo.read_envfile("credentials.env")

    # terraforming vs. not terraforming
    if UserInfo.terraforming:
        try:
            UserInfo.resource_group = args.resource_group
        except IndexError:
            print("You did not specify a resource group.")
            sys.exit(1)
        
        try:
            UserInfo.cis_name = args.name
        except:
            print("You did not specify a CIS Name.")
            sys.exit(1)
        
        try:
            UserInfo.github_pat = args.path
        except IndexError:
            print("You did not specify a GitHub PAT.")
            sys.exit(1)
    else:
        try:
            UserInfo.crn = args.crn
        except IndexError:
            print("You did not specify a CIS CRN.")
            sys.exit(1)

        try:
            UserInfo.zone_id = args.zone_id
        except IndexError:
            print("You did not specify a CIS Zone_ID.")
            sys.exit(1)
    
    # common arguments
    try:
        UserInfo.cis_domain = args.cis_domain
    except IndexError:
        print("You did not specify a CIS Domain.")
        sys.exit(1)

    try:
        UserInfo.app_url = args.app_url
    except IndexError:
        print("You did not specify a application URL.")
        sys.exit(1)
        
    # determining API key and creating the .env file
    UserInfo.cis_api_key = getpass.getpass(prompt="Enter CIS Services API Key: ")

    if not args.env:
        UserInfo.create_envfile()

    return UserInfo.terraforming

def main():
    terraforming = handle_args()

    if terraforming: # handle the case of using terraform
        work_creator = WorkspaceCreator()
        work_creator.create_terraform_workspace()
    else: # handle the case of using python
        # 1. Domain Name and DNS
        user_DNS = DNSCreator()
        user_DNS.create_records()

        # 2. Global Load Balancer
        user_GLB = GLB()
        user_GLB.create_glb()

        # 3. TLS Certificate Configuration
        certcreate.main()

        # 4. Edge Functions
        userEdgeFunction = EdgeFunctionCreator()
        userEdgeFunction.create_edge_function()
