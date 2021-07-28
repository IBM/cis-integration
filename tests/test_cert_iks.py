from src.iks.certcreate_iks import SecretCertificateCreator
from ibm_cloud_sdk_core.detailed_response import DetailedResponse
import requests

# custom class to be the mock return value
# will override the requests.Response returned from requests.get


def cert_creator():
    return SecretCertificateCreator(
        cis_crn="testCRN",
        cluster_id="testClusterID",
        cis_domain="test-domain.com",
        cert_manager_crn="testCertCRN",
        token="test-token"
    )


class MockGetNoCertsResponse:

    # mock json() method always returns a specific testing dictionary
    def __init__(self):
        self.status_check = 200


class MockPutCertResponse:

    # mock json() method always returns a specific testing dictionary
    pass


def test_check_certificate_no_cert(monkeypatch):
    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method
    def mock_get(*args, **kwargs):
        return MockGetNoCertsResponse()


def test_check_certificate_cert(monkeypatch):
    pass


def test_create_secret(monkeypatch):
    pass
