import sys
import getpass
import os


from src.certcreate import CertificateCreator
from src.functions import IntegrationInfo as IntegrationInfo
from src.functions import Color as Color
from src.functions import healthCheck as healthCheck
from src.create_glb import GLB
from src.dns_creator import DNSCreator
from src.create_edge_function import EdgeFunctionCreator
from src.create_terraform_workspace import WorkspaceCreator

'''
To get python script to run globally run following command: $ pip3 install -e /path/to/script/folder
'''

             
# method used to display the command usage if user uses `-h` or `--help`
def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine\n")

    print(Color.BOLD + "USAGE:" + Color.END)
    print("\t[python implementation]\t\tcis-integration [global options] [CIS CRN] [CIS ID] [CIS DOMAIN] [CODE ENGINE APP URL] ")
    print("\t[terraform implementation]\tcis-integration [global options] --terraform [RESOURCE GROUP] [CIS NAME] [CIS DOMAIN] [CODE ENGINE APP URL] [GITHUB PAT]\n")

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
def handle_args(args):
    
    if args.help:
        print_help()
        sys.exit(1)
    
    UserInfo = IntegrationInfo()
    UserInfo.terraforming = False
    if args.terraform:
        UserInfo.terraforming = True
    if args.env:
        UserInfo.read_envfile("credentials.env", args)
        print(UserInfo)
        return UserInfo

    # terraforming vs. not terraforming
    if UserInfo.terraforming:
        UserInfo.resource_group = args.resource_group
        if UserInfo.resource_group is None:         
            print("You did not specify a resource group.")
            sys.exit(1)
        
        
        UserInfo.cis_name = args.name
        if UserInfo.cis_name is None:
            print("You did not specify a CIS Name.")
            sys.exit(1)
        
        
        UserInfo.github_pat = args.pat
        if UserInfo.github_pat is None:
            print("You did not specify a GitHub PAT.")
            sys.exit(1)
    else:
        UserInfo.crn=args.crn
        if UserInfo.crn is None:
            print("You did not specify a CIS CRN.")
            sys.exit(1)

        UserInfo.zone_id = args.zone_id
        if UserInfo.zone_id is None:
            print("You did not specify a CIS Zone_ID.")
            sys.exit(1)
    
    # common arguments
    
    UserInfo.cis_domain = args.cis_domain
    if UserInfo.cis_domain is None:
        print("You did not specify a CIS Domain.")
        sys.exit(1)

    UserInfo.app_url = args.app_url
    if UserInfo.app_url is None:
        print("You did not specify a application URL.")
        sys.exit(1)
        
    # determining API key and creating the .env file
    UserInfo.cis_api_key = getpass.getpass(prompt="Enter CIS Services API Key: ")

    if not args.env:
        UserInfo.create_envfile()

    return UserInfo

def CodeEngine(args):
    UserInfo = handle_args(args)

    if UserInfo.terraforming: # handle the case of using terraform
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
        cert_creator = CertificateCreator()
        cert_creator.create_certificate()

        # 4. Edge Functions
        userEdgeFunction = EdgeFunctionCreator()
        userEdgeFunction.create_edge_function()

    hostUrl="https://"+UserInfo.cis_domain

    healthCheck(hostUrl)

    hostUrl="https://www."+UserInfo.cis_domain

    healthCheck(hostUrl)