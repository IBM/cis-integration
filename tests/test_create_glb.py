from _pytest.monkeypatch import resolve
import pytest
import os
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.ce.create_glb import GLB
from ibm_cloud_sdk_core.detailed_response import DetailedResponse
from ibm_cloud_networking_services import GlobalLoadBalancerPoolsV0
from ibm_cloud_networking_services import GlobalLoadBalancerV1
from ibm_cloud_networking_services import GlobalLoadBalancerMonitorV1



# custom class to be a mock Global Load Balancer Monitor object
# will override the GlobalLoadBalancerMonitorV1 object in create_glb.py
class MockGlobalLoadBalancerMonitorV1:

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def create_load_balancer_monitor(self, description, crn, type, expected_codes, follow_redirects):
        return DetailedResponse(response={"result": { "id": "testId", "description": description, "type": type, "expected_codes": expected_codes, "follow_redirects": follow_redirects}})


def test_create_load_balancer_monitor(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockGlobalLoadBalancerMonitorV1()

    monkeypatch.setattr(GlobalLoadBalancerMonitorV1, "new_instance", mock_get)
    creator = glb_creator()
    monitor = creator.create_load_balancer_monitor()

    assert monitor["result"]["description"] == "default health check"
    assert monitor["result"]["type"] == "https"
    assert monitor["result"]["expected_codes"] == "2xx"
    assert monitor["result"]["follow_redirects"] == True


# custom class to be a mock Global Load Balancer Pools object
# will override the GlobalLoadBalancerPoolsV0 object in create_glb.py
class MockGlobalLoadBalancerPoolsV0:
    
    def list_all_load_balancer_pools(self):
        return DetailedResponse(response={"result": []})

    def create_load_balancer_pool(self, name, origins, enabled, monitor):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "enabled": enabled, "monitor": monitor, "origins": origins}})

def test_create_origin_pool(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockGlobalLoadBalancerPoolsV0()

    monkeypatch.setattr(GlobalLoadBalancerPoolsV0, "new_instance", mock_get)
    creator = glb_creator()
    pool = creator.create_origin_pool()

    assert pool["result"]["name"] == 'default-pool'
    assert pool["result"]["enabled"] == True
    assert pool["result"]["origins"] == [{"name": 'default-origin', "address": "test.com", "enabled": True, "weight":1}]


class MockGlobalLoadBalancerV1:

     # mock set_service_url() serves as a useless mock method
    def set_service_url(self, url):
        pass
    
    def list_all_load_balancers(self):
        return DetailedResponse(response={"result": []})

    def create_load_balancer(self, name, default_pools, fallback_pool, enabled=True, proxied=True):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "enabled": enabled, "default_pools": default_pools, "fallback_pool": fallback_pool, "proxied": proxied}})

def test_create_global_load_balancer(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockGlobalLoadBalancerV1()

    monkeypatch.setattr(GlobalLoadBalancerV1, "new_instance", mock_get)
    creator = glb_creator()
    glb = creator.create_global_load_balancer()

    assert glb["result"]["name"] == "test.com"
    assert glb["result"]["enabled"] == True
    assert glb["result"]["proxied"] == True

# custom class to be a mock DNS Records object
# will override the DnsRecordsV1 object in dns_creator.py
class MockExistingGlobalLoadBalancerV1:
    def __init__(self):
        self.load_balancers_list = []
        glb = { "id": "testId", "created_on": "testDate", "modified_on": "testDate", "name": "test.com"}
        self.load_balancers_list.append(glb)

    # mock set_service_url() serves as a useless mock method
    def set_service_url(self, url):
        pass

    # mock list_all_dns_records() creates a fake list of DNS records
    def list_all_load_balancers(self):
        return DetailedResponse(response={"result": self.load_balancers_list})
    
    # mock update_dns_records() updates a fake DNS record for testing
    def edit_load_balancer(self, global_load_balancer_id, name, default_pools, fallback_pool, enabled, proxied):
        for item in self.load_balancers_list:
            if item['id'] == global_load_balancer_id:
                item['name'] = name
                item['default_pools'] = default_pools
                item['fallback_pool'] = fallback_pool
                item['enabled'] = enabled
                item['proxied'] = proxied

                return DetailedResponse(response={"result": item})

def test_edit_global_load_balancer(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockExistingGlobalLoadBalancerV1()

    monkeypatch.setattr(GlobalLoadBalancerV1, "new_instance", mock_get)
    creator = glb_creator()
    glb = creator.create_global_load_balancer()

    assert glb.result["result"]["name"] == "test.com"
    assert glb.result["result"]["enabled"] == True
    assert glb.result["result"]["proxied"] == True

# custom class to be a mock Global Load Balancer Pools object
# will override the GlobalLoadBalancerPoolsV0 object in create_glb.py
class MockExistingGlobalLoadBalancerPoolsV0:

    def __init__(self):
        self.origin_pool_list = []
        origin_pool = { "id": "testId", "created_on": "testDate", "modified_on": "testDate", "name": "default-pool"}
        self.origin_pool_list.append(origin_pool)
    
    def list_all_load_balancer_pools(self):
        return DetailedResponse(response={"result": self.origin_pool_list})

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def edit_load_balancer_pool(self, origin_pool_id, name, origins, enabled, monitor):
        for item in self.origin_pool_list:
            if item['id'] == origin_pool_id:
                item['name'] = name
                item['origins'] = origins
                item['monitor'] = monitor
                item['enabled'] = enabled

                return DetailedResponse(response={"result": item})


def test_edit_origin_pool(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockExistingGlobalLoadBalancerPoolsV0()

    monkeypatch.setattr(GlobalLoadBalancerPoolsV0, "new_instance", mock_get)
    creator = glb_creator()
    pool = creator.create_origin_pool()

    assert pool.result["result"]["name"] == 'default-pool'
    assert pool.result["result"]["enabled"] == True
    assert pool.result["result"]["origins"] == [{"name": 'default-origin', "address": "test.com", "enabled": True, "weight":1}]

def glb_creator():
    return GLB(
        crn="testString",
        zone_identifier="testString",
        api_endpoint="test-endpoint.com",
        domain="test.com"
    )
