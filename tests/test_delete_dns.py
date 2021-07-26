import pytest
import os
from io import StringIO
from unittest.mock import patch
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.common.functions import Color
from dotenv import load_dotenv
from ibm_cloud_networking_services import DnsRecordsV1
from src.common.delete_dns import DeleteDNS
import requests, json
from ibm_cloud_sdk_core.detailed_response import DetailedResponse

def dns_delete():
    return DeleteDNS(
        crn="testString",
        zone_id="testString",
        endpoint="test-endpoint.com",
        cis_domain="test-domain.com"
    )

class MockBothDNSRecordsV1:

    def __init__(self):
        self.dns_records_list = []
        www_record = {"name": "www.test-domain.com", "id": "testid"}
        root_record = {"name": "test-domain.com", "id": "testid"}
        self.dns_records_list.append(www_record)
        self.dns_records_list.append(root_record)

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_dns_record(self, dnsrecord_identifier):
        return DetailedResponse(response={"result": []})

    def list_all_dns_records(self):
        return DetailedResponse(response={"result": self.dns_records_list})

    def set_service_url(self, url):
        pass

class MockRootDNSRecordsV1:

    def __init__(self):
        self.dns_records_list = []
        www_record = {"name": "www.test-domain.com", "id": "testid"}
        root_record = {"name": "test-domain.com", "id": "testid"}
        self.dns_records_list.append(root_record)

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_dns_record(self, dnsrecord_identifier):
        return DetailedResponse(response={"result": []})

    def list_all_dns_records(self):
        return DetailedResponse(response={"result": self.dns_records_list})

    def set_service_url(self, url):
        pass

class MockWWWDNSRecordsV1:

    def __init__(self):
        self.dns_records_list = []
        www_record = {"name": "www.test-domain.com", "id": "testid"}
        root_record = {"name": "test-domain.com", "id": "testid"}
        self.dns_records_list.append(www_record)

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_dns_record(self, dnsrecord_identifier):
        return DetailedResponse(response={"result": []})

    def list_all_dns_records(self):
        return DetailedResponse(response={"result": self.dns_records_list})

    def set_service_url(self, url):
        pass

class MockNeitherDNSRecordsV1:

    def __init__(self):
        self.dns_records_list = []

    # create_load_balancer_monitor() creates a fake Load Balancer Monitor for testing
    def delete_dns_record(self, dnsrecord_identifier):
        return DetailedResponse(response={"result": []})

    def list_all_dns_records(self):
        return DetailedResponse(response={"result": self.dns_records_list})

    def set_service_url(self, url):
        pass

def test_both_dns_records(monkeypatch):
    sample_inputs = StringIO('y\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_dns(*args, **kwargs):
        return MockBothDNSRecordsV1()

    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_dns)

    delete = dns_delete()
    successful_delete_root = "Delete DNS Records? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted '@' record" + Color.END
    successful_delete_www = Color.GREEN + "SUCCESS: Deleted 'www' record" + Color.END
    expected_out = successful_delete_root + '\n' + successful_delete_www + '\n'
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_dns()
            assert fake_out.getvalue() == expected_out

def test_www_dns_records(monkeypatch):
    sample_inputs = StringIO('y\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_dns(*args, **kwargs):
        return MockWWWDNSRecordsV1()

    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_dns)

    delete = dns_delete()
    successful_delete_root = "Delete DNS Records? Input 'y' or 'yes' to execute: " + Color.RED + "ERROR: No '@' DNS record found" + Color.END
    successful_delete_www = Color.GREEN + "SUCCESS: Deleted 'www' record" + Color.END
    expected_out = successful_delete_root + '\n' + successful_delete_www + '\n'
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_dns()
            assert fake_out.getvalue() == expected_out

def test_root_dns_records(monkeypatch):
    sample_inputs = StringIO('y\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_dns(*args, **kwargs):
        return MockRootDNSRecordsV1()

    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_dns)

    delete = dns_delete()
    successful_delete_root = "Delete DNS Records? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted '@' record" + Color.END
    successful_delete_www = Color.RED + "ERROR: No 'www' DNS record found" + Color.END
    expected_out = successful_delete_root + '\n' + successful_delete_www + '\n'
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_dns()
            assert fake_out.getvalue() == expected_out

def test_neither_dns_records(monkeypatch):
    sample_inputs = StringIO('y\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_dns(*args, **kwargs):
        return MockNeitherDNSRecordsV1()

    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_dns)

    delete = dns_delete()
    successful_delete_root = "Delete DNS Records? Input 'y' or 'yes' to execute: " + Color.RED + "ERROR: No '@' DNS record found" + Color.END
    successful_delete_www = Color.RED + "ERROR: No 'www' DNS record found" + Color.END
    expected_out = successful_delete_root + '\n' + successful_delete_www + '\n'
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_dns()
            assert fake_out.getvalue() == expected_out

def test_no_dns_records(monkeypatch):
    sample_inputs = StringIO('n\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_dns(*args, **kwargs):
        return MockNeitherDNSRecordsV1()

    monkeypatch.setattr(DnsRecordsV1, "new_instance", mock_dns)

    delete = dns_delete()
    no_delete = "Delete DNS Records? Input 'y' or 'yes' to execute: "
    expected_out = no_delete
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_dns()
            assert fake_out.getvalue() == expected_out