import pytest
import os
from dotenv import load_dotenv
from src.ce import create_edge_function
import requests
import json

# custom class to be the mock return value
# will override the requests.Response returned from requests.get


class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"success": True}

# custom class to be a mock token
# will override request token
# class MockToken:

    # mock token() method always returns a specific access token
    # @staticmethod
    # def token(self, dummy):
        # return "test-token"


def edge_function():
    return create_edge_function.EdgeFunctionCreator(
        crn="testString",
        app_url="test-url.com",
        apikey="testString",
        zone_id="testString",
        domain="test-domain.com",
        token="test-token"
    )


def test_create_edge_action(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_put(*args, **kwargs):
        return MockResponse()

    # def mock_token(*args, **kwargs):
    #    return MockToken()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "request", mock_put)
    # monkeypatch.setattr(create_edge_function.EdgeFunctionCreator,
    #                     "request_token", mock_token().token)

    # app.get_json, which contains requests.get, uses the monkeypatch
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_action()
    assert result.json()["success"] == True


def test_create_edge_trigger(monkeypatch):
    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_put(*args, **kwargs):
        return MockResponse()

    # def mock_token(*args, **kwargs):
    #    return MockToken()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "request", mock_put)
    # monkeypatch.setattr(create_edge_function.EdgeFunctionCreator,
    #                     "request_token", mock_token().token)

    # app.get_json, which contains requests.get, uses the monkeypatch
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_trigger()
    assert result.json()["success"] == True


def test_create_edge_www_trigger(monkeypatch):
    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_put(*args, **kwargs):
        return MockResponse()

    # def mock_token(*args, **kwargs):
    #    return MockToken()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "request", mock_put)
    # monkeypatch.setattr(create_edge_function.EdgeFunctionCreator,
    #                     "request_token", mock_token().token)

    # app.get_json, which contains requests.get, uses the monkeypatch
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_www_trigger()
    assert result.json()["success"] == True


def test_create_edge_wild_card_trigger(monkeypatch):
    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_put(*args, **kwargs):
        return MockResponse()

    # def mock_token(*args, **kwargs):
    #    return MockToken()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "request", mock_put)
    # monkeypatch.setattr(create_edge_function.EdgeFunctionCreator,
    #                     "request_token", mock_token().token)

    # app.get_json, which contains requests.get, uses the monkeypatch
    test_edge_function = edge_function()
    result = test_edge_function.create_edge_function_wild_card_trigger()
    assert result.json()["success"] == True
