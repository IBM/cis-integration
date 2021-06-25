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


def test_get_json(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_put(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "request", mock_put)

    # app.get_json, which contains requests.get, uses the monkeypatch
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_action()
    assert result.json()["success"] == True

def edge_function():
    return create_edge_function.EdgeFunctionCreator(
        crn="crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::",
        app_url="demo-app.9y43h3pccht.us-south.codeengine.appdomain.cloud",
        apikey="0fFExM228FeuA7c1eZAhAw_Tdq-MJKlVjEav5D8Tf7BF",
        zone_id="f4604bfab1a024690e30bfd72ae36727",
        domain="gcat-interns-rock.com"
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