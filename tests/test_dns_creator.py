from _pytest.monkeypatch import resolve
import pytest
import os
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.dns_creator import DNSCreator

class MockDNSRecords:
    pass

def test_neither_exist(monkeypatch):
    monkeypatch.setattr()
    pass

def dns_creator():
    return DNSCreator(
        crn="crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::",
        zone_id="f4604bfab1a024690e30bfd72ae36727",
        endpoint="https://api.cis.cloud.ibm.com"
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