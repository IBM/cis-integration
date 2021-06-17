import sys
import getpass
import os
import certcreate
from functions import Color as Color
from create_glb import GLB
from dns_creator import DNSCreator
from create_edge_function import EdgeFunctionCreator

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

    def remove_quotes(self, item):
        result = item
        if result[0] == '"':
            result = result[1:]
        if result[-1] == '"':
            result = result[:-1]
        return result

    def read_envfile(self, filename):
        env_vars = {}
        try:
            file = open(filename, "r")
        except FileNotFoundError:
            print("Env file doesn't exist!")
            sys.exit(1)

        info = file.read().split("\n")

        for item in info:
            try:
                item.index('=')
                broken_item = item.split('=')
                broken_item[1] = self.remove_quotes(broken_item[1])
                env_vars[broken_item[0]] = broken_item[1]
            except ValueError:
                pass

        try:
            if not self.terraforming:
                os.environ["CRN"] = env_vars["CRN"]
                os.environ["ZONE_ID"] = env_vars["ZONE_ID"]
            else:
                os.environ["RESOURCE_GROUP"] = env_vars["RESOURCE_GROUP"]
                os.environ["CIS_NAME"] = env_vars["CIS_NAME"]

            os.environ["API_ENDPOINT"] = env_vars["API_ENDPOINT"]
            os.environ["CIS_SERVICES_APIKEY"] = env_vars["CIS_SERVICES_APIKEY"]
            os.environ["CIS_DOMAIN"] = env_vars["CIS_DOMAIN"]
            os.environ["APP_URL"] = env_vars["APP_URL"]
        except:
            print("Missing one or more necessary attributes in .env!")
            sys.exit(1)            

def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine\n")

    print(Color.BOLD + "USAGE:" + Color.END)
    print("\t[python implementation]\t\tcis-integration [global options] [CIS CRN] [CIS ID] [CIS DOMAIN] [CODE ENGINE APP URL] [GITHUB PAT]")
    print("\t[terraform implementation]\tcis-integration [global options] [RESOURCE GROUP] [CIS NAME] [CIS DOMAIN] [CODE ENGINE APP URL]\n")

    print(Color.BOLD + "GLOBAL OPTIONS:" + Color.END)
    print("\t--help, -h \t\t show help\n")

def handle_args():
    UserInfo = IntegrationInfo()

    UserInfo.terraforming = True
    try:
        sys.argv.index('--terraform')
    except ValueError:
        UserInfo.terraforming = False

    try:
        env_index = sys.argv.index('--env')
    except:
        env_index = -1

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

    args = [arg for arg in sys.argv if arg[0] != '-']

    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print_help()
        sys.exit(1)

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

    # temp variable github PAT while the project is private, will need to be removed once prject is public

    try:
        UserInfo.github_pat = args[5]
    except IndexError:
        print("You did not specify a GitHub PAT.")
        sys.exit(1)

    UserInfo.cis_api_key = getpass.getpass(prompt="Enter CIS Services API Key: ")
    UserInfo.create_envfile()

    return UserInfo.terraforming

def main():
    terraforming = handle_args()
    
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
