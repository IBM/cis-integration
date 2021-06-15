
'''
curl -X POST "https://iam.cloud.ibm.com/identity/token" 
-H "Content-Type: application/x-www-form-urlencoded"
 -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY" -u bx:bx
'''
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from ibm_cloud_sdk_core.base_service import BaseService, DetailedResponse
from ibm_schematics.common import get_sdk_headers
import json

class IAMTokenV1(BaseService):
    DEFAULT_SERVICE_URL = 'https://iam.cloud.ibm.com'
    DEFAULT_SERVICE_NAME = "iam_token"
    @classmethod
    def new_instance(cls,
                     authenticator: Authenticator,
                     service_name: str = DEFAULT_SERVICE_NAME
                    ) -> 'IAMTokenV1':
        #authenticator = get_authenticator_from_environment(service_name)
        print(authenticator)
        service = cls(authenticator)
        service.configure_service(service_name)
        return service

    def __init__(self,
                authenticator: Authenticator = None) -> None:
        BaseService.__init__(self, service_url=self.DEFAULT_SERVICE_URL, authenticator=authenticator)

    def get_iam_token(self, apikey: str, **kwargs) -> DetailedResponse:

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic Yng6Yng=',
            'Accept': 'application/json'
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                        service_version='V1',
                                        operation_id='get_iam_token')
        headers.update(sdk_headers)
        data = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'apikey': apikey,
            'response_type': 'cloud_iam'
        }
        #data = {k: v for (k,v) in data.items() if v is not None}
        #data = json.dumps(data)
        #headers['Content-type'] = 'application/x-www-form-urlencoded'
        #if 'headers' in kwargs:
        #   headers.update(kwargs.get('headers'))

        url = '/identity/token'
        request = self.prepare_request(method='POST',
                                        url=url,
                                        headers=headers,
                                        data=data)
        print(request)
        response = self.send(request)
        return response
