from _pytest.monkeypatch import resolve
import pytest
import json
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.common.dns_creator import DNSCreator
from ibm_cloud_networking_services.dns_records_v1 import DnsRecordsV1
from ibm_cloud_sdk_core.detailed_response import DetailedResponse

# custom class to be a mock DNS Records object
# will override the DnsRecordsV1 object in dns_creator.py
class MockDNSRecordsV1Neither:

    # mock set_service_url() serves as a useless mock method
    def set_service_url(self, url):
        pass

    # mock list_all_dns_records() creates a fake list of DNS records
    def list_all_dns_records(self):
        return DetailedResponse(response={"result": []})

    # mock create_dns_records() creates a fake DNS record for testing
    def create_dns_record(self, type, name, content, proxied):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "type": type, "content": content, "proxied": proxied}})

# custom class to be a mock DNS Records object
# will override the DnsRecordsV1 object in dns_creator.py
class MockDNSRecordsV1Root:
    def __init__(self):
        self.records_list = []
        root_record = { "id": "testId", "created_on": "testDate", "modified_on": "testDate", "name": "test.com", "type": "CNAME", "zone_name": "test.com" }
        self.records_list.append(root_record)

    # mock set_service_url() serves as a useless mock method
    def set_service_url(self, url):
        pass

    # mock list_all_dns_records() creates a fake list of DNS records
    def list_all_dns_records(self):
        return DetailedResponse(response={"result": self.records_list})

    # mock create_dns_records() creates a fake DNS record for testing
    def create_dns_record(self, type, name, content, proxied):
        return DetailedResponse(response={"result": { "id": "testId", "name": name, "type": type, "content": content, "proxied": proxied}})
    
    # mock update_dns_records() updates a fake DNS record for testing
    def update_dns_record(self, dnsrecord_identifier, type, name, content, proxied):
        for item in self.records_list:
            if item['id'] == dnsrecord_identifier:
                item['type'] = type
                item['name'] = name
                item['content'] = content
                item['proxied'] = proxied

                return DetailedResponse(response={"result": item})

# custom class to be a mock DNS Records object
# will override the DnsRecordsV1 object in dns_creator.py
class MockDNSRecordsV1Both:
    def __init__(self):
        self.records_list = []
        root_record = { "id": "testId", "created_on": "testDate", "modified_on": "testDate", "name": "test.com", "type": "CNAME", "zone_name": "test.com" }
        www_record = { "id": "testId2", "created_on": "testDate", "modified_on": "testDate", "name": "www.test.com", "type": "CNAME", "zone_name": "test.com" }
        self.records_list.append(root_record)
        self.records_list.append(www_record)

    # mock set_service_url() serves as a useless mock method
    def set_service_url(self, url):
        pass

    # mock list_all_dns_records() creates a fake list of DNS records
    def list_all_dns_records(self):
        return DetailedResponse(response={"result": self.records_list})

    # mock update_dns_records() updates a fake DNS record for testing
    def update_dns_record(self, dnsrecord_identifier, type, name, content, proxied):
        for item in self.records_list:
            if item['id'] == dnsrecord_identifier:
                item['type'] = type
                item['name'] = name
                item['content'] = content
                item['proxied'] = proxied

                return DetailedResponse(response={"result": item})

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

def test_one_exist(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockDNSRecordsV1Root()
    
    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_get)
    creator = dns_creator()
    root_record, www_record = creator.create_records()

    assert root_record.result["result"]["type"] == "CNAME"
    assert root_record.result["result"]["name"] == "@"
    assert root_record.result["result"]["content"] == "test-url.com"
    
    assert www_record.result["result"]["type"] == "CNAME"
    assert www_record.result["result"]["name"] == "www"
    assert www_record.result["result"]["content"] == "test-url.com"

def test_both_exist(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object
    def mock_get(*args, **kwargs):
        return MockDNSRecordsV1Both()
    
    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_get)
    creator = dns_creator()
    root_record, www_record = creator.create_records()

    assert root_record.result["result"]["type"] == "CNAME"
    assert root_record.result["result"]["name"] == "@"
    assert root_record.result["result"]["content"] == "test-url.com"
    
    assert www_record.result["result"]["type"] == "CNAME"
    assert www_record.result["result"]["name"] == "www"
    assert www_record.result["result"]["content"] == "test-url.com"

def dns_creator():
    return DNSCreator(
        crn="testString",
        zone_id="testString",
        api_endpoint="test-endpoint.com",
        app_url="test-url.com"
    )

