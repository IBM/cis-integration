import os
import sys
import getpass


from src.certcreate import CertificateCreator
from src.functions import IntegrationInfo as IntegrationInfo
from src.functions import Color as Color
from src.functions import healthCheck as healthCheck
from src.create_glb import GLB
from src.dns_creator import DNSCreator
from src.create_edge_function import EdgeFunctionCreator
from src.create_terraform_workspace import WorkspaceCreator
from src.delete_glb import DeleteGLB
from src.delete_dns import DeleteDNS
from src.delete_certs import DeleteCerts
from src.delete_edge import DeleteEdge

'''
To get python script to run globally run following command: $ pip3 install -e /path/to/script/folder
'''

             
# method used to display the command usage if user uses `-h` or `--help`
def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine")
    print("\t- call this tool with either 'cis-integration' or 'ci'\n")

    print(Color.BOLD + "USAGE:" + Color.END)
    print("\t[python implementation]\t\tcis-integration [positional args] [global options] -c [CIS CRN] -z [CIS ZONE ID] -d [CIS DOMAIN] -a [APP URL] ")
    print("\t[terraform implementation]\tcis-integration [positional args] [global options] --terraform -r [RESOURCE GROUP] -n [CIS NAME] -d [CIS DOMAIN] -a [APP URL]\n")
    print("\t[removing resources]\t\tcis-integration [positional args] [global options] --delete -c [CIS CRN] -z [CIS ZONE ID] -d [CIS DOMAIN]\n")

    print(Color.BOLD + "POSITIONAL ARGUMENTS:" + Color.END)
    print("\tcode-engine, ce \t\t connect a Code Engine app\n")

    print(Color.BOLD + "GLOBAL OPTIONS:" + Color.END)
    print("\t--help, -h \t\t show help")
    print("\t--delete \t\t removes resources created using this tool")
    print("\t--env, -e \t\t gets arguments from a credentials.env file")
    print("\t--terraform, -t \t build resources for CIS instance using terraform")
    print("\t--verbose, -v \t\t prints a detailed log from the Schematics workspace if --terraform is selected\n")

    print(Color.BOLD + "OPTIONAL ARGUMENTS:" + Color.END)
    print("\t--crn, -c \t\t CRN of the CIS instance")
    print("\t--zone_id, -z \t\t Zone ID of the CIS instance")
    print("\t--cis_domain, -d \t domain name of the CIS instance")
    print("\t--app_url, -a \t\t URL of the application")
    print("\t--resource_group, -r \t resource group associated with the CIS instance")
    print("\t--name, -n \t\t name of the CIS instance")

# handles the arguments given for both the python and terraform command options
def handle_args(args):
    
    if args.help:
        print_help()
        sys.exit(1)
    
    UserInfo = IntegrationInfo()
    UserInfo.terraforming = False
    if args.terraform:
        UserInfo.terraforming = True

    if args.verbose:
        UserInfo.verbose = True

    if args.delete:
        UserInfo.delete = True

    if args.env:
        UserInfo.read_envfile("credentials.env")
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
    
    if not UserInfo.delete:
        UserInfo.app_url = args.app_url
        if UserInfo.app_url is None:
            print("You did not specify a application URL.")
            sys.exit(1)
        
    # determining API key and creating the .env file
    UserInfo.cis_api_key = getpass.getpass(prompt="Enter CIS Services API Key: ")

    return UserInfo

def CodeEngine(args):
    UserInfo = handle_args(args)
    os.environ["CIS_SERVICES_APIKEY"] = UserInfo.cis_api_key

    if UserInfo.delete:
        delete_glb = DeleteGLB(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_glb.delete_glb()

        delete_dns = DeleteDNS(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_dns.delete_dns()

        delete_certs = DeleteCerts(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_certs.delete_certs()

        delete_edge = DeleteEdge(UserInfo.crn, UserInfo.zone_id, UserInfo.cis_domain, UserInfo.cis_api_key)
        delete_edge.delete_edge()

    elif UserInfo.terraforming: # handle the case of using terraform
        work_creator = WorkspaceCreator(UserInfo.cis_api_key, UserInfo.schematics_url, UserInfo.app_url, UserInfo.cis_domain, UserInfo.resource_group, UserInfo.cis_name, UserInfo.api_endpoint, UserInfo.verbose)
        work_creator.create_terraform_workspace()
    else: # handle the case of using python
        # 1. Domain Name and DNS
        user_DNS = DNSCreator(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.app_url)
        user_DNS.create_records()

        # 2. Global Load Balancer
        user_GLB = GLB(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        user_GLB.create_load_balancer_monitor()
        user_GLB.create_origin_pool()
        user_GLB.create_global_load_balancer()

        # 3. TLS Certificate Configuration
        cert_creator = CertificateCreator(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        cert_creator.create_certificate()

        # 4. Edge Functions
        userEdgeFunction = EdgeFunctionCreator(UserInfo.crn, UserInfo.app_url, UserInfo.cis_api_key, UserInfo.zone_id, UserInfo.cis_domain)
        userEdgeFunction.create_edge_function_action()
        userEdgeFunction.create_edge_function_trigger()
        userEdgeFunction.create_edge_function_wild_card_trigger()
        userEdgeFunction.create_edge_function_www_trigger()

    hostUrl="https://"+UserInfo.cis_domain

    healthCheck(hostUrl)

    hostUrl="https://www."+UserInfo.cis_domain

    healthCheck(hostUrl)