from _pytest.monkeypatch import resolve
import pytest
import os
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.create_glb import GLB
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

    assert monitor.result["result"]["description"] == "default health check"
    assert monitor.result["result"]["type"] == "https"
    assert monitor.result["result"]["expected_codes"] == "2xx"
    assert monitor.result["result"]["follow_redirects"] == True


# custom class to be a mock Global Load Balancer Pools object
# will override the GlobalLoadBalancerPoolsV0 object in create_glb.py
class MockGlobalLoadBalancerPoolsV0:
    
    def list_all_load_balancer_pools():
        return DetailedResponse(response={"result": []})

    def create_load_balancer_pool(self, origin_pool_id, name, origins, enabled, monitor):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "enabled": enabled, "monitor": monitor, "origins": origins}})

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def edit_load_balancer_pool(self, origin_pool_id, name, origins, enabled, monitor):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "enabled": enabled, "monitor": monitor, "origins": origins}})


def test_create_origin_pool(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockGlobalLoadBalancerPoolsV0()

    monkeypatch.setattr(GlobalLoadBalancerPoolsV0, "new_instance", mock_get)
    creator = glb_creator()
    monitor = creator.create_origin_pool()

    assert monitor.result["result"]["name"] == 'default-pool'
    assert monitor.result["result"]["enabled"] == True
    assert monitor.result["result"]["origins"] == [{"name": 'default-origin', "address": "gcat-interns-rock.com", "enabled": True, "weight":1}]


class MockGlobalLoadBalancerV1:

     # mock set_service_url() serves as a useless mock method
    def set_service_url(self, url):
        pass
    
    def list_all_load_balancers():
        return DetailedResponse(response={"result": []})

    def create_load_balancer(self, name, default_pools, fallback_pool, enabled=True, proxied=True):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "enabled": enabled, "default_pools": default_pools, "fallback_pool": fallback_pool, "proxied": proxied}})

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def edit_load_balancer(self, name, default_pools, fallback_pool, enabled=True, proxied=True):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "enabled": enabled, "default_pools": default_pools, "fallback_pool": fallback_pool, "proxied": proxied}})

def test_create_global_load_balancer(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockGlobalLoadBalancerV1()

    monkeypatch.setattr(GlobalLoadBalancerV1, "new_instance", mock_get)
    creator = glb_creator()
    monitor = creator.create_global_load_balancer()

    assert monitor.result["result"]["name"] == "gcat-interns-rock.com"
    assert monitor.result["result"]["enabled"] == True
    assert monitor.result["result"]["proxied"] == True

def glb_creator():
    return GLB(
        crn="crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::",
        zone_identifier="f4604bfab1a024690e30bfd72ae36727",
        api_endpoint="https://api.cis.cloud.ibm.com",
        domain="gcat-interns-rock.com"
    )