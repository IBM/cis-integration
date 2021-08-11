import pytest
import os
from io import StringIO
from unittest.mock import patch
from src.common import functions
from src.common.functions import Color
from src.common.functions import IntegrationInfo

# def test_health_check():
#     expected_out = Color.GREEN + "google.com has successfully been deployed." + Color.END
#     with patch('sys.stdout', new = StringIO()) as fake_out:
#             functions.healthCheck("www.cloud.ibm.com")
#             assert fake_out.getvalue() == expected_out

def test_read_envfile():
    test_integration = IntegrationInfo()
    test_integration.read_envfile("test_var.env")

    assert test_integration.app_url == "test_app_url.com"
    assert test_integration.cis_domain == "gcat-interns-test.com"
    assert test_integration.crn == "test_crn"
    assert test_integration.zone_id == "test_zone_id"
    assert test_integration.cis_api_key == "test_api_key"
    assert test_integration.api_endpoint == "www.test_api_endpoint.com"


def test_terraform_read_envfile():
    test_integration = IntegrationInfo()
    test_integration.terraforming = True
    test_integration.read_envfile("test_var.env")

    assert test_integration.app_url == "test_app_url.com"
    assert test_integration.cis_domain == "gcat-interns-test.com"
    assert test_integration.cis_api_key == "test_api_key"
    assert test_integration.api_endpoint == "www.test_api_endpoint.com"
    assert test_integration.resource_group == "test-resource-group"
    assert test_integration.cis_name == "test_instance_name"


