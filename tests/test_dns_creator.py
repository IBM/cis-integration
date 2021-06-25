from _pytest.monkeypatch import resolve
import pytest
import json
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.dns_creator import DNSCreator
from ibm_cloud_networking_services.dns_records_v1 import DnsRecordsV1
from ibm_cloud_sdk_core.detailed_response import DetailedResponse

# custom class to be a mock DNS Records object
# will override the DnsRecordsV1 object in dns_creator.py
class MockDNSRecordsV1Neither:

    # mock set_service_url() serves as a useless mock method
    def set_service_url(self, url):
        pass

    # mock list_all_dns_records() creates a fake list of dns records
    def list_all_dns_records(self):
        return DetailedResponse(response={"result": []})

    # create_dns_records() creates a fake DNS record for testing
    def create_dns_record(self, type, name, content, proxied):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "type": type, "content": content, "proxied": True}})

#################################################
##### TO DO
##### - neither records exist
##### - both records exist
##### - one record exists
#################################################

def test_neither_exist(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockDNSRecordsV1Neither()

    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_get)
    creator = dns_creator()
    root_record, www_record = creator.create_records()

    assert root_record.result["result"]["type"] == "CNAME"
    assert root_record.result["result"]["name"] == "@"
    assert root_record.result["result"]["content"] == "test-url.com"

    assert www_record.result["result"]["type"] == "CNAME"
    assert www_record.result["result"]["name"] == "www"
    assert root_record.result["result"]["content"] == "test-url.com"


def dns_creator():
    return DNSCreator(
        crn="testString",
        zone_id="testString",
        api_endpoint="test-endpoint.com",
        app_url="test-url.com"
    )

def test_create_root_record():
    dns = dns_creator()
    (response, new_record) = dns.create_root_record()
    assert response.status_code == 200
    assert new_record == True

    (response, new_record) = dns.create_root_record()
    assert response.status_code == 200
    assert new_record == False

def test_create_www_record():
    dns = dns_creator()
    (response, new_record) = dns.create_www_record()
    assert response.status_code == 200
    assert new_record == True

    (response, new_record) = dns.create_www_record()
    assert response.status_code == 200
    assert new_record == False