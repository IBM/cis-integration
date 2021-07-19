import json
from ibm_vpc import VpcV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibm_platform_services import ResourceManagerV2

class AclRuleCreator:
    def __init__(self, resource_group, api_key):
        self.api_key = api_key
        self.resource_group = resource_group

    def create_acl(self):
        authenticator = IAMAuthenticator(self.api_key)
        vpc_serivce = VpcV1(authenticator = authenticator)

        resource_service = ResourceManagerV2.new_instance()
        resource_group = resource_service.get_resource_group(id=self.resource_group)
        resource_group_identity_model = {}
        resource_group_identity_model['id'] = resource_group['id']
        print(json.dumps(resource_group, indent=2))
       
        network_acl_prototype_model = {}
        network_acl_prototype_model['name'] = "cis-integration_default"