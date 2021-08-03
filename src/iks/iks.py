from src.iks.certcreate_iks import SecretCertificateCreator
from src.iks.create_ingress import IngressCreator
from src.common.dns_creator import DNSCreator
from src.iks.create_terraform_workspace import WorkspaceCreator
from src.common.functions import Color, IntegrationInfo, healthCheck
from src.common.delete_dns import DeleteDNS
from src.iks.create_acl_rules import AclRuleCreator
from src.ce.delete_workspaces import DeleteWorkspace
from src.ce.certcreate import CertificateCreator

import sys
import getpass
import os


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
    UserInfo.cis_api_key = getpass.getpass(
        prompt="Enter CIS Services API Key: ")
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
        #vpc name
        UserInfo.vpc_name = args.vpc_name
        if UserInfo.vpc_name is None:
            print("You did not specify a VPC instance name.")
            sys.exit(1)

        UserInfo.resource_group = args.resource_group
        if UserInfo.resource_group is None:
            print("You did not specify a resource group.")
            sys.exit(1)

        UserInfo.namespace = args.namespace
        if UserInfo.namespace is None:         
            print("You did not specify a namespace for IKS cluster.")
            sys.exit(1)

        UserInfo.service_name = args.service_name
        if UserInfo.service_name is None:         
            print("You did not specify a service name from the IKS cluster.")
            sys.exit(1)

        UserInfo.service_port = args.service_port
        if UserInfo.service_port is None:         
            print("You did not specify the target port of the service from the IKS cluster.")
            sys.exit(1)

        UserInfo.get_resource_id()

        UserInfo.crn = args.crn
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
    if UserInfo.delete and not UserInfo.terraforming:
        delete_dns = DeleteDNS(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_dns.delete_dns()

    elif UserInfo.delete and UserInfo.terraforming:
        delete_workspaces = DeleteWorkspace(UserInfo.crn, UserInfo.zone_id,
        UserInfo.cis_domain, UserInfo.api_endpoint,
        UserInfo.schematics_url, UserInfo.cis_api_key, UserInfo.token, ce=False, iks=True)
        delete_workspaces.delete_workspace()
    elif UserInfo.terraforming: # handle the case of using terraform
        work_creator = WorkspaceCreator(
            UserInfo.cis_api_key, UserInfo.schematics_url,
            UserInfo.cis_name, UserInfo.resource_group,
            UserInfo.cis_domain, UserInfo.iks_cluster_id,
            UserInfo.verbose, UserInfo.token)
        work_creator.create_terraform_workspace()
    else:
        
        # handle the case of using python
        # 1. Domain Name and DNS
        
        user_DNS = DNSCreator(UserInfo.crn, UserInfo.zone_id,
                              UserInfo.api_endpoint, UserInfo.app_url)

        user_DNS.create_records()

        user_edge_cert = CertificateCreator(UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        user_edge_cert.create_certificate()

        resource_group_id = UserInfo.get_resource_id()
        user_ACL = AclRuleCreator(resource_group_id, UserInfo.vpc_name, UserInfo.cis_api_key)
        user_ACL.check_network_acl()
        
        # 2. Generate certificate in manager if necessary
        
        UserInfo.cert_name="cis-cert"
        
        cms_id = UserInfo.get_cms()
        # print("\n"+cms_id)
        user_cert = SecretCertificateCreator(
            cis_crn=UserInfo.crn,
            cluster_id=UserInfo.iks_cluster_id,
            cis_domain=UserInfo.cis_domain,
            cert_manager_crn=cms_id,

            token=UserInfo.token["access_token"],
            cert_name=UserInfo.cert_name
            )
        user_cert.create_secret()

       
        
        #3 generate ingress
        
        UserInfo.secret_name=UserInfo.cert_name
        user_ingress = IngressCreator(
            clusterNameOrID=UserInfo.iks_cluster_id,
            resourceGroupID=UserInfo.resource_id, 
            namespace=UserInfo.namespace, 
            secretName=UserInfo.secret_name, 
            serviceName=UserInfo.service_name, 
            servicePort=UserInfo.service_port, 
            accessToken=UserInfo.token["access_token"], 
            refreshToken=UserInfo.token["refresh_token"],
            ingressSubdomain=UserInfo.app_url,
            iks_master_url=UserInfo.iks_master_url
        )
        user_ingress.create_ingress()
        
        
        
    if not UserInfo.delete:
        hostUrl = "https://"+UserInfo.cis_domain

        healthCheck(hostUrl)

        hostUrl = "https://www."+UserInfo.cis_domain

        healthCheck(hostUrl)
