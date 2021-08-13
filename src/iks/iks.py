
from src.iks.delete_secret_cert import DeleteSecretCMS
from src.iks.delete_ingress import DeleteIngress
from src.iks.certcreate_iks import SecretCertificateCreator
from src.iks.create_ingress import IngressCreator
from src.common.dns_creator import DNSCreator
from src.iks.create_terraform_workspace import WorkspaceCreator
from src.common.functions import Color, IntegrationInfo, healthCheck
from src.common.delete_dns import DeleteDNS
from src.iks.create_acl_rules import AclRuleCreator
from src.common.delete_workspaces import DeleteWorkspace
from src.common.certcreate import CertificateCreator
from src.common.delete_certs import DeleteCerts


import sys
import getpass
import os


def print_help():
    print(Color.BOLD + 'NAME:' + Color.END)
    print("\tcis-integration - a command line tool used to connect a CIS instance with an application deployed on Code Engine")
    print("\t- call this tool with either 'cis-integration' or 'ci'\n")

    print(Color.BOLD + "USAGE:" + Color.END)
    print("\t[python command]\t\tcis-integration [positional args] [global options] -n [CIS NAME] -r [RESOURCE GROUP] -d [CIS DOMAIN] -i [CLUSTER ID] --namespace [IKS NAMESPACE] --service_name [IKS SERVICE NAME] --service_port [IKS TARGET PORT] -p [VPC NAME]")
    print("\t[alt python command]\t\tcis-integration [positional args] [global options] -c [CIS CRN] -z [CIS ZONE ID] -d [CIS DOMAIN] -i [CLUSTER ID] --namespace [IKS NAMESPACE] --service_name [IKS SERVICE NAME] --service_port [IKS TARGET PORT] -p [VPC NAME]\n")
    print("\t[terraform command]\t\tcis-integration [positional args] [global options] --terraform -r [RESOURCE GROUP] -n [CIS NAME] -d [CIS DOMAIN] -i [CLUSTER ID] --namespace [IKS NAMESPACE] --service_name [IKS SERVICE NAME] --service_port [IKS TARGET PORT] -p [VPC NAME]\n")
    print("\t[delete command]\t\tcis-integration [positional args] [global options] --delete -n [CIS NAME] -r [RESOURCE GROUP] -d [CIS DOMAIN]")
    print("\t[alt delete command]\t\tcis-integration [positional args] [global options] --delete -c [CIS CRN] -z [CIS ZONE ID] -d [CIS DOMAIN]\n")

    print(Color.BOLD + "POSITIONAL ARGUMENTS:" + Color.END)
    print("\tiks, ks \t\t connect a kubernetes cluster\n")

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
    print("\t--iks_cluster_id, -j \t\t ID of IKS cluster")
    print("\t--resource_group, -r \t resource group associated with the CIS instance")
    print("\t--name, -n \t\t name of the CIS instance")
    print("\t--namespace \t\t name of the virtual cluster using your physical IKS cluster resources")
    print("\t--service_name \t\t the name of the IKS Service exposing your application by rerouting incoming traffic to pods.")
    print("\t--service_port \t\t the target port of your Service that every incoming port is mapped to")
    print("\t--vpc_name, -p \t\t name of the virtual private cloud")


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

    UserInfo.iks_cluster_id = args.iks_cluster_id
    if UserInfo.iks_cluster_id is None:
        print("You did not specify an IKS cluster ID.")
        sys.exit(1)

    UserInfo.resource_group = args.resource_group
    if UserInfo.resource_group is None:
        print("You did not specify a resource group.")
        sys.exit(1)
    UserInfo.get_resource_id()

    iks_info = UserInfo.get_iks_info()

    UserInfo.cis_domain = args.cis_domain
    if UserInfo.cis_domain is None:
        print("You did not specify a CIS Domain.")
        sys.exit(1)

    # terraforming vs. not terraforming
    if UserInfo.terraforming and not UserInfo.delete:
        UserInfo.cis_name = args.name
        if UserInfo.cis_name is None:
            print("You did not specify a CIS Name.")
            sys.exit(1)

        if not UserInfo.get_crn_and_zone():
            print(
                "Failed to retrieve CRN and Zone ID. Check the name of your CIS instance and try again")
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
            print(
                "You did not specify the target port of the service from the IKS cluster.")
            sys.exit(1)

        UserInfo.vpc_name = args.vpc_name
        if UserInfo.vpc_name is None:
            print("You did not specify a VPC instance name.")
            sys.exit(1)

    elif not UserInfo.delete:
        # vpc name
        UserInfo.vpc_name = args.vpc_name
        if UserInfo.vpc_name is None:
            print("You did not specify a VPC instance name.")
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
            print(
                "You did not specify the target port of the service from the IKS cluster.")
            sys.exit(1)

        UserInfo.get_resource_id()

        UserInfo.crn = args.crn
        UserInfo.zone_id = args.zone_id
        if UserInfo.crn is None or UserInfo.zone_id is None:
            UserInfo.cis_name = args.name

            if UserInfo.cis_name is None:
                print(
                    "Please specify the name of your CIS instance or both the CIS CRN and CIS Zone ID")
                sys.exit(1)

            if not UserInfo.get_crn_and_zone():
                print(
                    "Failed to retrieve CRN and Zone ID. Check the name of your CIS instance and try again")
                sys.exit(1)

    elif UserInfo.delete:
        UserInfo.resource_group = args.resource_group
        if UserInfo.resource_group is None:
            print("You did not specify a resource group.")
            sys.exit(1)

        UserInfo.get_resource_id()

        UserInfo.crn = args.crn
        UserInfo.zone_id = args.zone_id
        if UserInfo.crn is None or UserInfo.zone_id is None:
            UserInfo.cis_name = args.name

            if UserInfo.cis_name is None:
                print(
                    "Please specify the name of your CIS instance or both the CIS CRN and CIS Zone ID")
                sys.exit(1)

            if not UserInfo.get_crn_and_zone():
                print(
                    "Failed to retrieve CRN and Zone ID. Check the name of your CIS instance and try again")
                sys.exit(1)

    return UserInfo


def iks(args):
    delete_dns = None
    delete_workspaces = None
    work_creator = None
    user_ingress = None

    UserInfo = handle_args(args)
    if UserInfo.delete and not UserInfo.terraforming:

        delete_dns = DeleteDNS(
            UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_dns.delete_dns()

        UserInfo.get_id_token()
        delete_ingress = DeleteIngress(
            UserInfo.namespace, UserInfo.id_token, UserInfo.iks_master_url)
        delete_ingress.delete_ingress()

        delete_certs = DeleteCerts(
            UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        delete_certs.delete_certs()

        print("If you created a certificate in the certificate manager and imported it as a secret to your IKS cluster, you may delete them now.")
        secret = input(
            "Delete certificate and secret? Input 'y' or 'yes' to execute:").lower()
        if secret == 'y' or secret == 'yes':
            UserInfo.cert_name = "cis-cert"

            cms_id = UserInfo.get_cms()

            delete_secret = DeleteSecretCMS(
                UserInfo.iks_cluster_id, UserInfo.cis_domain, cms_id, UserInfo.cert_name, UserInfo.token['access_token'])
            delete_secret.delete_cms_cert()
            delete_secret.delete_secret()
    elif UserInfo.delete and UserInfo.terraforming:
        print("If you created a certificate in the certificate manager and imported it as a secret to your IKS cluster, you may delete them now.")
        secret = input(
            "Delete certificate and secret? Input 'y' or 'yes' to execute:").lower()
        if secret == 'y' or secret == 'yes':
            UserInfo.cert_name = "cis-cert"

            cms_id = UserInfo.get_cms()

            delete_secret = DeleteSecretCMS(
                UserInfo.iks_cluster_id, UserInfo.cis_domain, cms_id, UserInfo.cert_name, UserInfo.token['access_token'])
            delete_secret.delete_secret()

        delete_workspaces = DeleteWorkspace(UserInfo.crn, UserInfo.zone_id,
                                            UserInfo.cis_domain, UserInfo.api_endpoint,
                                            UserInfo.schematics_url, UserInfo.cis_api_key, UserInfo.token, ce=False, iks=True)
        delete_workspaces.delete_workspace()
    elif UserInfo.terraforming:  # handle the case of using terraform
        print("Currently using the default secret in IKS, but a new TLS certificate can be ordered and imported as a secret if you wish.")
        execute = input(
            "Would you like to create a new secret? Input 'y' or 'yes' to execute:").lower()
        if execute == 'y' or execute == 'yes':
            UserInfo.cert_name = 'cis-cert'
        else:
            secret = UserInfo.app_url.split('.')
            UserInfo.cert_name = secret[0]

        resource_group_id = UserInfo.get_resource_id()
        user_ACL = AclRuleCreator(
            resource_group_id, UserInfo.vpc_name, UserInfo.cis_api_key)
        user_ACL.check_network_acl()

        UserInfo.secret_name = UserInfo.cert_name
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
            iks_master_url=UserInfo.iks_master_url,
            idToken=UserInfo.id_token
        )
        user_ingress.create_ingress()

        work_creator = WorkspaceCreator(
            UserInfo.cis_api_key, UserInfo.schematics_url,
            UserInfo.cis_name, UserInfo.resource_group,
            UserInfo.cis_domain, UserInfo.iks_cluster_id,
            UserInfo.app_url, UserInfo.cert_name,
            UserInfo.verbose, UserInfo.token)
        work_creator.create_terraform_workspace()
    else:

        # handle the case of using python
        # 1. Domain Name and DNS

        user_DNS = DNSCreator(UserInfo.crn, UserInfo.zone_id,
                              UserInfo.api_endpoint, UserInfo.app_url, token=UserInfo.token["access_token"])

        user_DNS.create_records()

        # 2. Order Edge Certificate from CIS
        user_edge_cert = CertificateCreator(
            UserInfo.crn, UserInfo.zone_id, UserInfo.api_endpoint, UserInfo.cis_domain)
        user_edge_cert.create_certificate()

        # 3. Check ACL Rules
        resource_group_id = UserInfo.get_resource_id()
        user_ACL = AclRuleCreator(
            resource_group_id, UserInfo.vpc_name, UserInfo.cis_api_key)
        user_ACL.check_network_acl()

        # 4. Generate certificate in manager if necessary
        print("Currently using the default secret in IKS, but a new TLS certificate can be ordered and imported as a secret if you wish.")
        execute = input(
            "Would you like to create a new secret? Input 'y' or 'yes' to execute:").lower()
        if execute == 'y' or execute == 'yes':
            UserInfo.cert_name = "cis-cert"

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
        else:
            secret = UserInfo.app_url.split('.')
            UserInfo.cert_name = secret[0]

        # 5. generate ingress

        UserInfo.get_id_token()
        UserInfo.secret_name = UserInfo.cert_name
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
            iks_master_url=UserInfo.iks_master_url,
            idToken=UserInfo.id_token
        )

        user_ingress.create_ingress()

    if not UserInfo.delete:
        hostUrl = "https://"+UserInfo.cis_domain

        healthCheck(hostUrl)

        hostUrl = "https://www."+UserInfo.cis_domain

        healthCheck(hostUrl)

    return delete_dns, delete_workspaces, work_creator, user_ingress
