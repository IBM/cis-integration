from requests.api import delete
from src.iks.create_terraform_workspace import WorkspaceCreator
from src.common.dns_creator import DNSCreator
from src.iks.certcreate_iks import SecretCertificateCreator
import pytest
import os
import getpass
from io import StringIO
from _pytest.monkeypatch import resolve
from unittest.mock import patch
from src.common import functions
from src.common.functions import Color
from src.common.functions import IntegrationInfo
from ibm_cloud_sdk_core.detailed_response import DetailedResponse
from src.iks import iks as IKS
from src.iks.iks import handle_args
from src.iks.iks import iks
from src.common.delete_dns import DeleteDNS
from src.ce.delete_workspaces import DeleteWorkspace


class MockArgs():
    def __init__(self, terraform, verbose, delete, iks_cluster_id, cis_domain, resource_group, name, crn, zone_id, namespace, service_name, service_port, vpc_name):
        self.help = False
        self.terraform = terraform
        self.verbose = verbose
        self.delete = delete
        self.iks_cluster_id = iks_cluster_id
        self.cis_domain = cis_domain
        self.resource_group = resource_group
        self.name = name
        self.crn = crn
        self.zone_id = zone_id
        self.namespace = namespace
        self.service_name = service_name
        self.service_port = service_port
        self.vpc_name = vpc_name


class MockIntegrationInfoObj():
    def set_attr(self, terraform, verbose, delete, iks_cluster_id, cis_domain, resource_group, name, crn, zone_id, namespace, service_name, service_port, vpc_name, iks_master_url):
        self.crn = crn
        self.zone_id = zone_id
        self.api_endpoint = 'https://api.cis.cloud.ibm.com'
        self.iks_cluster_id = iks_cluster_id
        self.app_url = "test_url"
        self.resource_group = resource_group
        self.resource_id = resource_group
        self.cis_name = name
        self.cis_api_key = "fake_key"
        self.cis_domain = cis_domain
        self.schematics_url = 'https://us.schematics.cloud.ibm.com'
        self.terraforming = terraform
        self.verbose = verbose
        self.delete = delete
        self.token = {"access_token": "123456789",
                      "refresh_token": "testingRefresh"}
        self.namespace = namespace
        self.service_name = service_name
        self.service_port = service_port
        self.vpc_name = vpc_name
        self.iks_master_url = iks_master_url

    def get_cms(arg):
        return "123456789"
    
    def request_token():
        return "123456789_fake_token"

    def get_iks_info(self):
        return DetailedResponse(response={"result": []})

    def get_resource_id():
        return "123456789"

    def get_crn_and_zone(self):
        return True

    def get_resource_id(self):
        return self.resource_id


def get_no_crn_and_zone(self):
    return False


def mock_handle_args_delete_terr(args):
    integration_info = MockIntegrationInfoObj()
    integration_info.set_attr(True, True, True, "fake_cluster_id", "fake_cis_domain", "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc", "fake_master_url")
    return integration_info

def mock_handle_args_delete_not_terr(args):
    integration_info = MockIntegrationInfoObj()
    integration_info.set_attr(False, True, True, "fake_cluster_id", "fake_cis_domain", "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc", "fake_master_url")
    return integration_info

def mock_handle_args_terr(args):
    integration_info = MockIntegrationInfoObj()
    integration_info.set_attr(True, True, False, "fake_cluster_id", "fake_cis_domain", "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc", "fake_master_url")
    return integration_info

def mock_handle_args_reg(args):
    integration_info = MockIntegrationInfoObj()
    integration_info.set_attr(False, False, False, "fake_cluster_id", "fake_cis_domain", "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc", "fake_master_url")
    return integration_info

def mock_delete_dns(arg):
    pass

def mock_delete_workspace(arg):
    pass

def mock_create_terraform_workspace(arg):
    pass


def mock_create_records(arg):
    pass

def mock_create_secret(arg):
    pass

def mock_create_certificate(arg):
    pass

def mock_create_ingress(arg):
    pass

def mock_check_network_acl(arg):
    pass

def test_terr_verb_del_handle_args(monkeypatch):

    def mock_getpass(*args, **kwargs):
        return "fake_api_key"

    monkeypatch.setattr(getpass, "getpass", mock_getpass)
    monkeypatch.setattr(IntegrationInfo, "__init__",
                        MockIntegrationInfoObj.__init__)
    monkeypatch.setattr(IntegrationInfo, "get_iks_info",
                        MockIntegrationInfoObj.get_iks_info)
    monkeypatch.setattr(IntegrationInfo, "get_resource_id",
                        MockIntegrationInfoObj.get_resource_id)

    args = MockArgs(True, True, True, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")
    user_info = handle_args(args)

    assert user_info.terraforming == True
    assert user_info.verbose == True
    assert user_info.delete == True


def test_no_iks_cluster_handle_args(monkeypatch):

    def mock_getpass(*args, **kwargs):
        return "fake_api_key"

    monkeypatch.setattr(getpass, "getpass", mock_getpass)
    monkeypatch.setattr(IntegrationInfo, "__init__",
                        MockIntegrationInfoObj.__init__)
    monkeypatch.setattr(IntegrationInfo, "get_iks_info",
                        MockIntegrationInfoObj.get_iks_info)
    monkeypatch.setattr(IntegrationInfo, "get_resource_id",
                        MockIntegrationInfoObj.get_resource_id)

    args = MockArgs(True, True, False, None, "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        user_info = handle_args(args)
    assert pytest_wrapped_e.value.code == 1


def test_no_cis_domain_handle_args(monkeypatch):
    def mock_getpass(*args, **kwargs):
        return "fake_api_key"

    monkeypatch.setattr(getpass, "getpass", mock_getpass)
    monkeypatch.setattr(IntegrationInfo, "__init__",
                        MockIntegrationInfoObj.__init__)
    monkeypatch.setattr(IntegrationInfo, "get_iks_info",
                        MockIntegrationInfoObj.get_iks_info)
    monkeypatch.setattr(IntegrationInfo, "get_resource_id",
                        MockIntegrationInfoObj.get_resource_id)

    args = MockArgs(True, True, False, "fake_cluster_id", None,
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        user_info = handle_args(args)
    assert pytest_wrapped_e.value.code == 1


def test_terr_and_not_delete_no_cis_handle_args(monkeypatch):
    def mock_getpass(*args, **kwargs):
        return "fake_api_key"

    monkeypatch.setattr(getpass, "getpass", mock_getpass)
    monkeypatch.setattr(IntegrationInfo, "__init__",
                        MockIntegrationInfoObj.__init__)
    monkeypatch.setattr(IntegrationInfo, "get_iks_info",
                        MockIntegrationInfoObj.get_iks_info)
    monkeypatch.setattr(IntegrationInfo, "get_resource_id",
                        MockIntegrationInfoObj.get_resource_id)

    args = MockArgs(True, True, False, "fake_cluster_id",
                    "fake_cis_domain", None, "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        user_info = handle_args(args)
    assert pytest_wrapped_e.value.code == 1


def test_terr_and_not_crn_zone_handle_args(monkeypatch):
    def mock_getpass(*args, **kwargs):
        return "fake_api_key"

    monkeypatch.setattr(getpass, "getpass", mock_getpass)
    monkeypatch.setattr(IntegrationInfo, "__init__",
                        MockIntegrationInfoObj.__init__)
    monkeypatch.setattr(IntegrationInfo, "get_iks_info",
                        MockIntegrationInfoObj.get_iks_info)
    monkeypatch.setattr(IntegrationInfo, "get_resource_id",
                        MockIntegrationInfoObj.get_resource_id)

    args = MockArgs(True, True, False, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", None, "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        user_info = handle_args(args)
    assert pytest_wrapped_e.value.code == 1


def test_no_resource_group_handle_args(monkeypatch):
    def mock_getpass(*args, **kwargs):
        return "fake_api_key"

    monkeypatch.setattr(getpass, "getpass", mock_getpass)
    monkeypatch.setattr(IntegrationInfo, "__init__",
                        MockIntegrationInfoObj.__init__)
    monkeypatch.setattr(IntegrationInfo, "get_iks_info",
                        MockIntegrationInfoObj.get_iks_info)
    monkeypatch.setattr(IntegrationInfo, "get_resource_id",
                        MockIntegrationInfoObj.get_resource_id)
    monkeypatch.setattr(IntegrationInfo, "get_crn_and_zone",
                        get_no_crn_and_zone)

    args = MockArgs(True, True, False, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone_id", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        user_info = handle_args(args)
    assert pytest_wrapped_e.value.code == 1


def test_no_zone_id_handle_args(monkeypatch):
    def mock_getpass(*args, **kwargs):
        return "fake_api_key"

    monkeypatch.setattr(getpass, "getpass", mock_getpass)
    monkeypatch.setattr(IntegrationInfo, "get_iks_info",
                        MockIntegrationInfoObj.get_iks_info)
    monkeypatch.setattr(IntegrationInfo, "get_resource_id",
                        MockIntegrationInfoObj.get_resource_id)
    monkeypatch.setattr(IntegrationInfo, "get_crn_and_zone",
                        get_no_crn_and_zone)

    args = MockArgs(True, True, False, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", None, "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        user_info = handle_args(args)
    assert pytest_wrapped_e.value.code == 1


def test_iks_delete_terr(monkeypatch):

    monkeypatch.setattr(IKS, "handle_args", mock_handle_args_delete_terr)

    args = MockArgs(True, True, True, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with patch("src.common.delete_dns.DeleteDNS.delete_dns", mock_delete_dns):
        with patch("src.ce.delete_workspaces.DeleteWorkspace.delete_workspace", mock_delete_workspace):
            delete_dns, delete_workspaces, work_creator, user_ingress = iks(args)

    assert work_creator == None
    assert user_ingress == None
    assert delete_dns == None
    assert delete_workspaces.crn == "fake_crn"
    assert delete_workspaces.zone_id == "fake_zone_id"
    assert delete_workspaces.api_endpoint == 'https://api.cis.cloud.ibm.com'
    assert delete_workspaces.cis_domain == "fake_cis_domain"
    assert delete_workspaces.schematics_url == 'https://us.schematics.cloud.ibm.com'
    assert delete_workspaces.apikey == "fake_key"
    assert delete_workspaces.token == {"access_token": "123456789",
                      "refresh_token": "testingRefresh"}

def test_iks_delete_not_terr(monkeypatch):

    monkeypatch.setattr(IKS, "handle_args", mock_handle_args_delete_not_terr)

    args = MockArgs(False, True, True, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")
    
    with patch("src.common.delete_dns.DeleteDNS.delete_dns", mock_delete_dns):
        with patch("src.ce.delete_workspaces.DeleteWorkspace.delete_workspace", mock_delete_workspace):
            delete_dns, delete_workspaces, work_creator, user_ingress = iks(args)


    assert delete_workspaces == None
    assert work_creator == None
    assert user_ingress == None
    assert delete_dns.crn == "fake_crn"
    assert delete_dns.zone_id == "fake_zone_id"
    assert delete_dns.endpoint == 'https://api.cis.cloud.ibm.com'
    assert delete_dns.cis_domain == "fake_cis_domain"


def test_iks_terraform(monkeypatch):
    monkeypatch.setattr(IKS, "handle_args", mock_handle_args_terr)

    args = MockArgs(True, True, False, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with patch("src.iks.create_terraform_workspace.WorkspaceCreator.create_terraform_workspace", mock_create_terraform_workspace):
        with patch("src.ce.delete_workspaces.DeleteWorkspace.delete_workspace", mock_delete_workspace):
            delete_dns, delete_workspaces, work_creator, user_ingress = iks(args)

    assert work_creator.cis_api_key == "fake_key"
    assert work_creator.schematics_url == 'https://us.schematics.cloud.ibm.com'
    assert work_creator.cis_name == "fake_name"
    assert work_creator.resource_group == "fake_resource_group"
    assert work_creator.cis_domain == "fake_cis_domain"
    assert work_creator.cluster_id == "fake_cluster_id"
    assert work_creator.token == {"access_token": "123456789",
                      "refresh_token": "testingRefresh"}

    assert user_ingress == None
    assert delete_dns == None
    assert delete_workspaces == None
            


def test_iks_regular(monkeypatch):
    monkeypatch.setattr(IKS, "handle_args", mock_handle_args_reg)

    args = MockArgs(True, True, True, "fake_cluster_id", "fake_cis_domain",
                    "fake_resource_group", "fake_name", "fake_crn", "fake_zone", "fake_namespace", "fake_service_name", "fake_service_port", "fake_vpc")

    with patch("src.common.dns_creator.DNSCreator.create_records", mock_create_records):
        with patch("src.iks.certcreate_iks.SecretCertificateCreator.create_secret", mock_create_secret):
            with patch("src.ce.certcreate.CertificateCreator.create_certificate", mock_create_certificate):
                with patch("src.ce.delete_workspaces.DeleteWorkspace.delete_workspace", mock_delete_workspace):
                    with patch("src.iks.create_ingress.IngressCreator.create_ingress", mock_create_ingress):
                        with patch("src.iks.create_acl_rules.AclRuleCreator.check_network_acl", mock_check_network_acl):
                            delete_dns, delete_workspaces, work_creator, user_ingress = iks(args)

    assert work_creator == None
    assert user_ingress.clusterNameOrID == "fake_cluster_id"
    assert user_ingress.resourceGroupID == "fake_resource_group"
    assert user_ingress.namespace == "fake_namespace"
    assert user_ingress.secretName == "cis-cert"
    assert user_ingress.serviceName == "fake_service_name"
    assert user_ingress.servicePort == "fake_service_port"
    assert user_ingress.accessToken == "123456789"
    assert user_ingress.refreshToken == "testingRefresh"
    assert user_ingress.ingressSubdomain == "test_url"
    assert user_ingress.iks_master_url == "fake_master_url"
    assert delete_dns == None
    assert delete_workspaces == None
