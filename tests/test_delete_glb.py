from _pytest.monkeypatch import resolve
import pytest
import os
from io import StringIO
from unittest.mock import patch
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.functions import Color
from src.delete_glb import DeleteGLB
from ibm_cloud_sdk_core.detailed_response import DetailedResponse
from ibm_cloud_networking_services import GlobalLoadBalancerPoolsV0
from ibm_cloud_networking_services import GlobalLoadBalancerV1
from ibm_cloud_networking_services import GlobalLoadBalancerMonitorV1

def glb_delete():
    return DeleteGLB(
        crn="testString",
        zone_id="testString",
        endpoint="test-endpoint.com",
        cis_domain="test.com"
    )

# custom class to be a mock Global Load Balancer Monitor object
# will override the GlobalLoadBalancerMonitorV1 object in create_glb.py
class MockGlobalLoadBalancerV1DNE:

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_load_balancer(self, load_balancer_identifier):
        return DetailedResponse(response={"result": { "id": glb_id}})

    def list_all_load_balancers(self):
        return DetailedResponse(response={"result": []})

    def set_service_url(self, url):
        pass

class MockExistingGlobalLoadBalancerV1:

    def __init__(self):
        self.load_balancers_list = []
        glb = { "id": "testId", "created_on": "testDate", "modified_on": "testDate", "name": "test.com", "fallback_pool": "test-pool-id"}
        self.load_balancers_list.append(glb)

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_load_balancer(self, load_balancer_identifier):
        return DetailedResponse(response={"result": []})

    def list_all_load_balancers(self):
        return DetailedResponse(response={"result": self.load_balancers_list})

    def set_service_url(self, url):
        pass

# custom class to be a mock Global Load Balancer Pools object
# will override the GlobalLoadBalancerPoolsV0 object in create_glb.py
class MockGlobalLoadBalancerPoolsV0:

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_load_balancer_pool(self, pool_identifier):
        return DetailedResponse(response={"result": {"id": pool_identifier}})

    def get_load_balancer_pool(self, pool_identifier):
        return DetailedResponse(response={"result": { "id": "testId", "monitor": "test-monitor-id"}})

    def set_service_url(self, url):
        pass

# custom class to be a mock Global Load Balancer Pools object
# will override the GlobalLoadBalancerPoolsV0 object in create_glb.py
class MockGlobalLoadBalancerMonitorV1:

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_load_balancer_monitor(self, monitor_identifier):
        return DetailedResponse(response={"result": {"id": monitor_identifier}})

    def set_service_url(self, url):
        pass
        

def test_yn_exists(monkeypatch):

    sample_inputs = StringIO('y\nn\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)
    
    def mock_glb(*args, **kwargs):
        return MockExistingGlobalLoadBalancerV1()

    monkeypatch.setattr(GlobalLoadBalancerV1, "new_instance", mock_glb)

    delete = glb_delete()
    successful_delete_glb = "Delete global load balancer? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted global load balancer" + Color.END + '\n'
    no_delete_pool = "Delete origin pool? Input 'y' or 'yes' to execute: "
    expected_out = successful_delete_glb + no_delete_pool
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_glb()
            assert fake_out.getvalue() == expected_out

def test_yn_dne(monkeypatch):
    sample_inputs = StringIO('y\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_glb(*args, **kwargs):
        return MockGlobalLoadBalancerV1DNE()

    monkeypatch.setattr(GlobalLoadBalancerV1, "new_instance", mock_glb)

    delete = glb_delete()
    dne_delete_glb = "Delete global load balancer? Input 'y' or 'yes' to execute: " + Color.RED + "ERROR: No global load balancer associated with domain test.com was found" + Color.END + '\n'
    expected_out = dne_delete_glb
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_glb()
            assert fake_out.getvalue() == expected_out

def test_yyn(monkeypatch):
    sample_inputs = StringIO('y\ny\nn\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_glb(*args, **kwargs):
        return MockExistingGlobalLoadBalancerV1()

    def mock_glb_pool(*args, **kwargs):
        return MockGlobalLoadBalancerPoolsV0()

    monkeypatch.setattr(GlobalLoadBalancerV1, "new_instance", mock_glb)
    monkeypatch.setattr(GlobalLoadBalancerPoolsV0, "new_instance", mock_glb_pool)

    delete = glb_delete()
    successful_delete_glb = "Delete global load balancer? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted global load balancer" + Color.END
    successful_delete_pool = "Delete origin pool? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted origin pool" + Color.END
    no_delete_monitor = "Delete health check monitor? Input 'y' or 'yes' to execute: "
    expected_out = successful_delete_glb + '\n' + successful_delete_pool + '\n' + no_delete_monitor
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_glb()
            assert fake_out.getvalue() == expected_out

def test_yyy(monkeypatch):
    sample_inputs = StringIO('y\ny\ny\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_glb(*args, **kwargs):
        return MockExistingGlobalLoadBalancerV1()

    def mock_glb_pool(*args, **kwargs):
        return MockGlobalLoadBalancerPoolsV0()

    def mock_glb_monitor(*args, **kwargs):
        return MockGlobalLoadBalancerMonitorV1()

    monkeypatch.setattr(GlobalLoadBalancerV1, "new_instance", mock_glb)
    monkeypatch.setattr(GlobalLoadBalancerPoolsV0, "new_instance", mock_glb_pool)
    monkeypatch.setattr(GlobalLoadBalancerMonitorV1, "new_instance", mock_glb_monitor)

    delete = glb_delete()
    successful_delete_glb = "Delete global load balancer? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted global load balancer" + Color.END
    successful_delete_pool = "Delete origin pool? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted origin pool" + Color.END
    successful_delete_monitor = "Delete health check monitor? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted health check" + Color.END
    expected_out = successful_delete_glb + '\n' + successful_delete_pool + '\n' + successful_delete_monitor + '\n'
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_glb()
            assert fake_out.getvalue() == expected_out
    