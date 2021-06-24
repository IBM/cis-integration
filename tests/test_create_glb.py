from _pytest.monkeypatch import resolve
import pytest
import os
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.create_glb import GLB

def glb_creator():
    return GLB(
        crn="crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::",
        zone_identifier="f4604bfab1a024690e30bfd72ae36727",
        api_endpoint="https://api.cis.cloud.ibm.com",
        domain="gcat-interns-rock.com"
    )

def test_load_balancer_monitor():
    load_balancer = glb_creator()
    result = load_balancer.create_load_balancer_monitor()
    assert result.status_code == 200

    result = load_balancer.create_load_balancer_monitor()
    assert result.status_code == 200

def test_origin_pools():
    load_balancer = glb_creator()
    result = load_balancer.create_origin_pool()
    assert result.status_code == 200

    result = load_balancer.create_origin_pool()
    assert result.status_code == 200

def test_load_balancer():
    load_balancer = glb_creator()
    result = load_balancer.create_global_load_balancer()
    assert result.status_code == 200

    result = load_balancer.create_global_load_balancer()
    assert result.status_code == 200
