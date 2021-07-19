from ibm_vpc import VpcV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibm_platform_services import ResourceManagerV2

class AclRuleCreator:
    def __init__(self, resource_group, vpc_name, api_key):
        self.api_key = api_key
        self.resource_group = resource_group
        self.resource_group_id = ''
        self.vpc_name = vpc_name
        self.vpc_id = ''

    def create_acl(self):
        authenticator = IAMAuthenticator(self.api_key)

        resource_service = ResourceManagerV2(authenticator=authenticator)
        resource = resource_service.list_resource_groups(name=self.resource_group, include_deleted=false).get_result()
        self.resource_group_id = resource["resources"][0]["id"]
        resource_group_identity_model = {}
        resource_group_identity_model['id'] = self.resource_group_id
        
        vpc_serivce = VpcV1(authenticator=authenticator)
        vpc_list = vpc_serivce.list_vpcs(resource_group_id=self.resource_group_id).get_result()
        for vpc in vpc_list["vpcs"]:
            if vpc["name"] == self.vpc_name:
                self.vpc_id = vpc["id"]
        vpc_identity_model = {}
        vpc_identity_model["id"] = self.vpc_id
       
        network_acl_prototype_model = {}
        network_acl_prototype_model['name'] = "cis-integration_default"