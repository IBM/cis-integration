import pytest
import os
from dotenv import load_dotenv
from src import create_edge_function
import requests, json

# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"success": True}

# custom class to be a mock token
# will override request token
class MockToken:

    # mock token() method always returns a specific access token
    @staticmethod
    def token(self, dummy):
        return "test-token"


def test_get_json(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_put(*args, **kwargs):
        return MockResponse()

    def mock_token(*args, **kwargs):
        return MockToken()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "request", mock_put)
    monkeypatch.setattr(create_edge_function.EdgeFunctionCreator, "request_token", mock_token().token)

    # app.get_json, which contains requests.get, uses the monkeypatch
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_action()
    assert result.json()["success"] == True

def edge_function():
    return create_edge_function.EdgeFunctionCreator(
        crn="testString",
        app_url="test-url.com",
        apikey="testString",
        zone_id="testString",
        domain="test-domain.com"
    )

def test_create_edge_action():
    #test the creation of edge function action
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_action()
    print("Test Create Edge Action 1")
    print(result)
    pytest.assertEqual(result.status_code, 200)

def test_create_edge_trigger():
    #test the creation of edge function trigger
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_trigger()
    print("Test Create Edge Trigger 1.1")
    print(result)
    assert result.status_code == 200

    #test the creation of an already existing edge function trigger
    result = test_edge_function.create_edge_function_trigger()
    print("Test Create Edge Trigger 1.2")
    print(result)
    assert result.status_code == 409

def test_create_edge_www_trigger():
    #test the creation of edge function trigger
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_www_trigger()
    print("Test Create Edge Trigger 2.1")
    print(result)
    assert result.status_code == 200

    #test the creation of an already existing edge function trigger
    result = test_edge_function.create_edge_function_www_trigger()
    print("Test Create Edge Trigger 2.2")
    print(result)
    assert result.status_code == 409

def test_create_edge_trigger():
    #test the creation of edge function trigger
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_wild_card_trigger()
    print("Test Create Edge Trigger 3.1")
    print(result)
    assert result.status_code == 200

    #test the creation of an already existing edge function trigger
    result = test_edge_function.create_edge_function_wild_card_trigger()
    print("Test Create Edge Trigger 3.2")
    print(result)
    assert result.status_code == 409