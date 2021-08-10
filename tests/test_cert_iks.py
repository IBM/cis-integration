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
        cert_manager_crn="testCertCRN:::::testRegion",
        token="test-token",
        cert_name="testCertName"
    )


class MockGetNoCertsResponse:

    # __init__() method defines mock variables for the class
    def __init__(self):
        self.status_code = 200
        self.certificates = []

    # mock json() method always returns a specific testing dictionary
    def json(self):
        return {"certificates": self.certificates}


class MockPostCertsResponse:

    # mock json() method always returns a specific testing dictionary
    def json(self):
        return {"_id": "newTestId"}


def test_check_certificate_no_cert(monkeypatch):
    mock_get_obj = MockGetNoCertsResponse()
    mock_post_obj = MockPostCertsResponse()

    # Any arguments may be passed and mock_requests() will always return our
    # mocked object, which only has the .json() method
    def mock_requests(method_type, *args, **kwargs):
        if method_type == "GET":
            return mock_get_obj
        elif method_type == "POST":
            mock_get_obj.certificates.append(mock_post_obj.json())
            return mock_post_obj

    # apply the monkeypatch for requests.request to mock_requests
    monkeypatch.setattr(requests, "request", mock_requests)

    # app.get_json, which contains requests.request, uses the monkeypatch
    test_cert_creator = cert_creator()
    result = test_cert_creator.check_certificate()
    assert(result == "newTestId")
    assert(len(mock_get_obj.certificates) == 1)
    assert(mock_get_obj.certificates[0]["_id"] == "newTestId")


class MockGetCertsDomainResponse:

    # __init__() method defines mock variables for the class
    def __init__(self):
        self.status_code = 200
        self.certificates = [{"_id": "testId", "domains": ["*.wrong-domain.com", "wrong-domain.com"]}, {"_id": "testId3", "domains": [
            "*.test-domain.com", "test-domain.com"]}, {"_id": "testId2", "domains": ["*.test-domain.com", "test-domain.com"]}]

    # mock json() method always returns a specific testing dictionary
    def json(self):
        return {"certificates": self.certificates}


def test_check_certificate_cert_domain(monkeypatch):
    mock_get_obj = MockGetCertsDomainResponse()

    # Any arguments may be passed and mock_requests() will always return our
    # mocked object, which only has the .json() method
    def mock_requests(*args, **kwargs):
        return mock_get_obj

    # apply the monkeypatch for requests.request to mock_requests
    monkeypatch.setattr(requests, "request", mock_requests)

    # app.get_json, which contains requests.request, uses the monkeypatch
    test_cert_creator = cert_creator()
    result = test_cert_creator.check_certificate()
    assert(result == "testId3")
    assert(len(mock_get_obj.certificates) == 3)


class MockGetCertsNoDomainResponse:

    # __init__() method defines mock variables for the class
    def __init__(self):
        self.status_code = 200
        self.certificates = [{"_id": "testId", "domains": ["*.wrong-domain.com", "wrong-domain.com"]}, {
            "_id": "testId2", "domains": ["*.wrong-domain-2.com", "wrong-domain-2.com"]}]

    # mock json() method always returns a specific testing dictionary
    def json(self):
        return {"certificates": self.certificates}


def test_check_certificate_cert_no_domain(monkeypatch):
    mock_get_obj = MockGetCertsNoDomainResponse()
    mock_post_obj = MockPostCertsResponse()

    # Any arguments may be passed and mock_requests() will always return our
    # mocked object, which only has the .json() method
    def mock_requests(method_type, *args, **kwargs):
        if method_type == "GET":
            return mock_get_obj
        elif method_type == "POST":
            mock_get_obj.certificates.append(mock_post_obj.json())
            return mock_post_obj

    # apply the monkeypatch for requests.request to mock_requests
    monkeypatch.setattr(requests, "request", mock_requests)

    # app.get_json, which contains requests.request, uses the monkeypatch
    test_cert_creator = cert_creator()
    result = test_cert_creator.check_certificate()
    assert(result == "newTestId")
    assert(len(mock_get_obj.certificates) == 3)
    assert(mock_get_obj.certificates[2]["_id"] == "newTestId")


class MockCreateSecretSuccess:

    # __init__() method defines mock variables for the class
    def __init__(self):
        self.status_code = 200


def test_create_secret_success(monkeypatch):
    mock_create_obj = MockCreateSecretSuccess()

    # A way to mock our check_certificate method, which includes calls using
    # the requests library and may take a while to complete
    def mock_crn(*args, **kwargs):
        return "testCRN"

    # Any arguments may be passed and mock_requests() will always return our
    # mocked object, which only has the status_code variable
    def mock_requests(*args, **kwargs):
        return mock_create_obj

    # apply the monkeypatch for check_certificate to mock_crn
    monkeypatch.setattr(SecretCertificateCreator,
                        "check_certificate", mock_crn)

    # apply the monkeypatch for requests.request to mock_requests
    monkeypatch.setattr(requests, "request", mock_requests)

    # app.get_json, which contains requests.request, uses the monkeypatch
    test_cert_creator = cert_creator()
    result = test_cert_creator.create_secret()
    assert(result.status_code == 200)


class MockCreateSecretFakeFailure:

    # __init__() method defines mock variables for the class
    def __init__(self):
        self.status_code = 500

    # mock json() method always returns a specific testing dictionary
    def json(self):
        return {}


def test_create_secret_initial_failure(monkeypatch):
    failed = False
    mock_create_obj = MockCreateSecretFakeFailure()

    # A way to mock our check_certificate method, which includes calls using
    # the requests library and may take a while to complete
    def mock_crn(*args, **kwargs):
        return "testCRN"

    # Any arguments may be passed and mock_requests() will always return our
    # mocked object, which only has the .json() method
    def mock_requests(*args, **kwargs):
        if not failed:
            mock_create_obj.status_code = 200
            return mock_create_obj
        else:
            return mock_create_obj

    # apply the monkeypatch for check_certificate to mock_crn
    monkeypatch.setattr(SecretCertificateCreator,
                        "check_certificate", mock_crn)

    # apply the monkeypatch for requests.request to mock_requests
    monkeypatch.setattr(requests, "request", mock_requests)

    # app.get_json, which contains requests.request, uses the monkeypatch
    test_cert_creator = cert_creator()
    result = test_cert_creator.create_secret()
    assert(result.status_code == 200)


def test_create_secret_timeout(monkeypatch):
    mock_create_obj = MockCreateSecretFakeFailure()

    # A way to mock our check_certificate method, which includes calls using
    # the requests library and may take a while to complete
    def mock_crn(*args, **kwargs):
        return "testCRN"

    # Any arguments may be passed and mock_requests() will always return our
    # mocked object, which only has the .json() method
    def mock_requests(*args, **kwargs):
        return mock_create_obj

    # apply the monkeypatch for check_certificate to mock_crn
    monkeypatch.setattr(SecretCertificateCreator,
                        "check_certificate", mock_crn)

    # apply the monkeypatch for requests.request to mock_requests
    monkeypatch.setattr(requests, "request", mock_requests)

    # app.get_json, which contains requests.request, uses the monkeypatch
    test_cert_creator = cert_creator()
    result = test_cert_creator.create_secret()
    assert(result.status_code == 500)


class MockCreateSecretRealFailure:

    # __init__() method defines mock variables for the class
    def __init__(self):
        self.status_code = 404


def test_create_secret_failue(monkeypatch):
    mock_create_obj = MockCreateSecretRealFailure()

    # A way to mock our check_certificate method, which includes calls using
    # the requests library and may take a while to complete
    def mock_crn(*args, **kwargs):
        return "testCRN"

    # Any arguments may be passed and mock_requests() will always return our
    # mocked object, which only has the status_code variable
    def mock_requests(*args, **kwargs):
        return mock_create_obj

    # apply the monkeypatch for check_certificate to mock_crn
    monkeypatch.setattr(SecretCertificateCreator,
                        "check_certificate", mock_crn)

    # apply the monkeypatch for requests.request to mock_requests
    monkeypatch.setattr(requests, "request", mock_requests)

    # app.get_json, which contains requests.request, uses the monkeypatch
    test_cert_creator = cert_creator()
    result = test_cert_creator.create_secret()
    assert(result.status_code == 404)
