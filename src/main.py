import sys
import getpass
import os
import certcreate
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
    print("\t[python implementation]\t\tcis-integration [global options] [CIS CRN] [CIS ID] [CIS DOMAIN] [CODE ENGINE APP URL] [GITHUB PAT]")
    print("\t[terraform implementation]\tcis-integration [global options] --terraform [RESOURCE GROUP] [CIS NAME] [CIS DOMAIN] [CODE ENGINE APP URL]\n")

    print(Color.BOLD + "GLOBAL OPTIONS:" + Color.END)
    print("\t--help, -h \t\t show help\n")

# handles the arguments given for both the python and terraform command options
def handle_args():
    UserInfo = IntegrationInfo()

    # handle terraform option
    UserInfo.terraforming = True
    try:
        sys.argv.index('--terraform')
    except ValueError:
        UserInfo.terraforming = False

    # grab the index of the `--env` argument if it exists
    try:
        env_index = sys.argv.index('--env')
    except:
        env_index = -1

    # handle case where .env file name is given
    if env_index != -1:
        if env_index == len(sys.argv) - 1:
            print("No env file found!")
            sys.exit(1)

        env_file = sys.argv[env_index + 1]
        if env_file[-4:] != '.env':
            print("Not an env file!")
            sys.exit(1)

        UserInfo.read_envfile(env_file)

        return UserInfo.terraforming

    # handle case where .env file name is not given
    args = [arg for arg in sys.argv if arg[0] != '-']

    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print_help()
        sys.exit(1)

    # terraforming vs. not terraforming
    if UserInfo.terraforming:
        try:
            UserInfo.resource_group = args[1]
        except IndexError:
            print("You did not specify a resource group.")
            sys.exit(1)
        
        try:
            UserInfo.cis_name = args[2]
        except:
            print("You did not specify a CIS Name.")
            sys.exit(1)
        
        try:
            UserInfo.github_pat = args[5]
        except IndexError:
            print("You did not specify a GitHub PAT.")
            sys.exit(1)
    else:
        try:
            UserInfo.crn = args[1]
        except IndexError:
            print("You did not specify a CIS CRN.")
            sys.exit(1)

        try:
            UserInfo.zone_id = args[2]
        except IndexError:
            print("You did not specify a CIS Zone_ID.")
            sys.exit(1)
    
    # common arguments
    try:
        UserInfo.cis_domain = args[3]
    except IndexError:
        print("You did not specify a CIS Domain.")
        sys.exit(1)

    try:
        UserInfo.app_url = args[4]
    except IndexError:
        print("You did not specify a application URL.")
        sys.exit(1)
        
    # determining API key and creating the .env file
    UserInfo.cis_api_key = getpass.getpass(prompt="Enter CIS Services API Key: ")
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
