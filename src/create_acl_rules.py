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

    def create_resource_group_model(self, authenticator):
        resource_service = ResourceManagerV2(authenticator=authenticator)
        resource = resource_service.list_resource_groups(name=self.resource_group, include_deleted=False).get_result()
        self.resource_group_id = resource["resources"][0]["id"]
        resource_group_identity_model = {}
        resource_group_identity_model['id'] = self.resource_group_id
        return resource_group_identity_model

    def create_vpc_model(self, authenticator):
        vpc_serivce = VpcV1(authenticator=authenticator)
        vpc_list = vpc_serivce.list_vpcs(resource_group_id=self.resource_group_id).get_result()
        for vpc in vpc_list["vpcs"]:
            if vpc["name"] == self.vpc_name:
                self.vpc_id = vpc["id"]
        vpc_identity_model = {}
        vpc_identity_model["id"] = self.vpc_id
        return vpc_identity_model

    def create_acl_rules(self):
        network_acl_rules = [
            {
                "name" : "iks-create-worker-nodes-inbound",
                "action" : "allow",
                "source" : "161.26.0.0/16",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
            },
            {
                "name" : "iks-nodes-to-master-inbound",
                "action" : "allow",
                "source" : "166.8.0.0/14",
                "destination": "0.0.0.0/0",
                "direction" : "inbound",
            }
        ]




    def create_network_acl(self):
        authenticator = IAMAuthenticator(self.api_key)

        resource_group_identity_model = self.create_resource_group_model(authenticator)
        
        vpc_identity_model = self.create_vpc_model(authenticator)
       
        network_acl_prototype_model = {}
        network_acl_prototype_model['name'] = "cis-integration_default"
        network_acl_prototype_model["resource_group"] = resource_group_identity_model
        network_acl_prototype_model["vpc"] = vpc_identity_model