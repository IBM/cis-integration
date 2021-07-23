import pytest
import os
from io import StringIO
from unittest.mock import patch
from dotenv import load_dotenv
from pathlib import Path
from requests.models import Response
from src.functions import Color
from dotenv import load_dotenv
from src.delete_edge import DeleteEdge 
import requests, json
from ibm_cloud_sdk_core.detailed_response import DetailedResponse

class MockGetTriggers:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def list_triggers():
        return {"result": [{"script": "test-url-com"}], "pattern": "www.test-url.com"}

class MockDeleteActionSuccess:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def response():
        return {"success": True, "result": {"id": "testID"}}

class MockDeleteActionFail:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def response():
        return {"success": False}

class MockDeleteTriggers:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"success": True}

def test_fail_delete_action(monkeypatch):
    sample_inputs = StringIO('y\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_get_trigg(*args, **kwargs):
        return MockGetTriggers().list_triggers()

    def mock_delete_trigg(*args, **kwargs):
        return MockDeleteTriggers()

    def mock_delete_action(*args, **kwargs):
        return MockDeleteActionFail().response()

    monkeypatch.setattr(DeleteEdge, "get_triggers", mock_get_trigg)
    monkeypatch.setattr(DeleteEdge, "delete_trigger", mock_delete_trigg)
    monkeypatch.setattr(DeleteEdge, "delete_action", mock_delete_action)

    delete = DeleteEdge(crn="testString", zone_id="testString", cis_domain="test-domain.com", apikey="testString", token="test-token")
    fail_delete_action = "Delete edge function? Input 'y' or 'yes' to execute: " + Color.RED + "ERROR: No edge function action associated with domain test-domain.com found" + Color.END
    expected_out = fail_delete_action + '\n'
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_edge()
            assert fake_out.getvalue() == expected_out

def test_success_delete_action(monkeypatch):
    sample_inputs = StringIO('y\n')
    monkeypatch.setattr('sys.stdin', sample_inputs)

    def mock_get_trigg(*args, **kwargs):
        return MockGetTriggers().list_triggers()

    def mock_delete_trigg(*args, **kwargs):
        return MockDeleteTriggers()

    def mock_delete_action(*args, **kwargs):
        return MockDeleteActionSuccess().response()

    monkeypatch.setattr(DeleteEdge, "get_triggers", mock_get_trigg)
    monkeypatch.setattr(DeleteEdge, "delete_trigger", mock_delete_trigg)
    monkeypatch.setattr(DeleteEdge, "delete_action", mock_delete_action)

    delete = DeleteEdge(crn="testString", zone_id="testString", cis_domain="test-domain.com", apikey="testString", token="test-token")
    successful_delete_action = "Delete edge function? Input 'y' or 'yes' to execute: " + Color.GREEN + "SUCCESS: Deleted edge function action with id testID" + Color.END
    expected_out = successful_delete_action + '\n'
    with patch('sys.stdout', new = StringIO()) as fake_out:
            delete.delete_edge()
            assert fake_out.getvalue() == expected_out