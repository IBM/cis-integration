from src.dns_creator import DNSCreator
from src.create_terraform_workspace import WorkspaceCreator
from src.functions import Color, IntegrationInfo, healthCheck
from src.delete_dns import DeleteDNS
from src.delete_workspaces import DeleteWorkspace
import sys, getpass, os

def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine")
    print("\t- call this tool with either 'cis-integration' or 'ci'\n")

    print("IKS VERSION: PRINT HELP NOT FINISHED")

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

    # determining API key 
    UserInfo.cis_api_key = getpass.getpass(prompt="Enter CIS Services API Key: ")
    os.environ["CIS_SERVICES_APIKEY"] = UserInfo.cis_api_key

    # common arguments
    UserInfo.request_token()

    if not UserInfo.delete:
        UserInfo.iks_cluster_id = args.iks_cluster_id
        if UserInfo.iks_cluster_id is None:
            print("You did not specify an IKS cluster ID.")
            sys.exit(1)

    iks_info = UserInfo.get_iks_info()

    UserInfo.cis_domain = args.cis_domain
    if UserInfo.cis_domain is None:
        print("You did not specify a CIS Domain.")
        sys.exit(1)
    
    # terraforming vs. not terraforming
    if UserInfo.terraforming and not UserInfo.delete:
        UserInfo.resource_group = args.resource_group
        if UserInfo.resource_group is None:         
            print("You did not specify a resource group.")
            sys.exit(1)
        
        UserInfo.get_resource_id()
        
        UserInfo.cis_name = args.name
        if UserInfo.cis_name is None:
            print("You did not specify a CIS Name.")
            sys.exit(1)

        if not UserInfo.get_crn_and_zone():
                print("Failed to retrieve CRN and Zone ID. Check the name of your CIS instance and try again")
                sys.exit(1)
        
    else:
        UserInfo.resource_group = args.resource_group
        if UserInfo.resource_group is None:         
            print("You did not specify a resource group.")
            sys.exit(1)

        UserInfo.get_resource_id()

        UserInfo.crn=args.crn
        UserInfo.zone_id = args.zone_id
        if UserInfo.crn is None or UserInfo.zone_id is None:
            UserInfo.cis_name = args.name
        
            if UserInfo.cis_name is None:
                print("Please specify the name of your CIS instance or both the CIS CRN and CIS Zone ID")
                sys.exit(1)

            if not UserInfo.get_crn_and_zone():
                print("Failed to retrieve CRN and Zone ID. Check the name of your CIS instance and try again")
                sys.exit(1)

    return UserInfo

def iks(args):
    UserInfo = handle_args(args)
    if UserInfo.delete:
        delete_dns = DeleteDNS(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_dns.delete_dns()

        if UserInfo.terraforming:
            delete_workspaces = DeleteWorkspace(UserInfo.schematics_url, UserInfo.cis_api_key, UserInfo.token)
            delete_workspaces.delete_workspace()
    elif UserInfo.terraforming: # handle the case of using terraform
        work_creator = WorkspaceCreator(
            UserInfo.cis_api_key, UserInfo.schematics_url, 
            UserInfo.app_url, UserInfo.cis_domain, 
            UserInfo.resource_group, UserInfo.cis_name, 
            UserInfo.api_endpoint, UserInfo.crn, 
            UserInfo.zone_id, UserInfo.verbose, UserInfo.token)
        work_creator.create_terraform_workspace()
    else:
        # handle the case of using python
        # 1. Domain Name and DNS
        user_DNS = DNSCreator(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.app_url)
        user_DNS.create_records()
        
    if not UserInfo.delete:
        hostUrl="https://"+UserInfo.cis_domain

        healthCheck(hostUrl)

        hostUrl="https://www."+UserInfo.cis_domain

        healthCheck(hostUrl)