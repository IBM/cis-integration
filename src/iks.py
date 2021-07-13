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

    return UserInfo

def iks(args):
    UserInfo = handle_args(args)
    if UserInfo.delete:
        delete_dns = DeleteDNS(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_dns.delete_dns()

        if UserInfo.terraforming:
            delete_workspaces = DeleteWorkspace(UserInfo.schematics_url, UserInfo.cis_api_key)
            delete_workspaces.delete_workspace()
    elif UserInfo.terraforming: # handle the case of using terraform
        work_creator = WorkspaceCreator(UserInfo.cis_api_key, UserInfo.schematics_url, UserInfo.app_url, UserInfo.cis_domain, UserInfo.resource_group, UserInfo.cis_name, UserInfo.api_endpoint, UserInfo.crn, UserInfo.zone_id, UserInfo.verbose)
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