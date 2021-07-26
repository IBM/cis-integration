from ibm_vpc import VpcV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibm_platform_services import ResourceManagerV2
from src.functions import Color

class AclRuleCreator:
    def __init__(self, resource_group, vpc_name, api_key):
        self.api_key = api_key
        self.resource_group = resource_group
        self.resource_group_id = ''
        self.vpc_name = vpc_name
        self.vpc_id = ''

    def check_ips(self, subnet_acl):
        notfound = False
        needed_acl_ips = ["161.26.0.0/16", "166.8.0.0/14", "103.21.244.0/22", "173.245.48.0/20", "103.22.200.0/22", "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/12", "172.64.0.0/13", "131.0.72.0/22", "10.10.30.0/24", "10.10.20.0/24", "10.10.10.0/24"]
        for rule in subnet_acl["rules"]:
            if rule["source"] != "0.0.0.0/0" and rule["source"] not in needed_acl_ips:
                notfound = True
        return notfound
    
    '''
    def create_acl_rules(self):
        network_acl_rules = [
            {
                "name" : "iks-create-worker-nodes-inbound",
                "action" : "allow",
                "source" : "161.26.0.0/16",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "all",
            },
            {
                "name" : "iks-nodes-to-master-inbound",
                "action" : "allow",
                "source" : "166.8.0.0/14",
                "destination": "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "all",
            },
            {
                "name" : "cf-ip-1",
                "action" : "allow",
                "source" : "103.21.244.0/22",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-2",
                "action" : "allow",
                "source" : "173.245.48.0/20",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-3",
                "action" : "allow",
                "source" : "103.22.200.0/22",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-4",
                "action" : "allow",
                "source" : "103.31.4.0/22",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-5",
                "action" : "allow",
                "source" : "141.101.64.0/18",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-6",
                "action" : "allow",
                "source" : "108.162.192.0/18",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-7",
                "action" : "allow",
                "source" : "190.93.240.0/20",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-8",
                "action" : "allow",
                "source" : "188.114.96.0/20",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-9",
                "action" : "allow",
                "source" : "197.234.240.0/22",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-10",
                "action" : "allow",
                "source" : "198.41.128.0/17",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-11",
                "action" : "allow",
                "source" : "162.158.0.0/15",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-12",
                "action" : "allow",
                "source" : "104.16.0.0/12",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-13",
                "action" : "allow",
                "source" : "172.64.0.0/13",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "cf-ip-14",
                "action" : "allow",
                "source" : "131.0.72.0/22",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "tcp",
                "source_port_min" : 1,
                "source_port_max" : 65535,
                "destination_port_min" : 443,
                "destination_port_max" : 443
            },
            {
                "name" : "worker-1",
                "action" : "allow",
                "source" : "10.10.30.0/24",
                "destination" : "0.0.0.0/0",
            },
            {
                "name" : "worker-2",
                "action" : "allow",
                "source" : "10.10.20.0/24",
                "destination" : "0.0.0.0/0",
            },
            {
                "name" : "worker-3",
                "action" : "allow",
                "source" : "10.10.10.0/24",
                "destination" : "0.0.0.0/0",
            },
            {
                "name" : "allow-all-outbound",
                "action" : "allow",
                "source" : "0.0.0.0/0",
                "destination" : "0.0.0.0/0",
                "direction" : "outbound",
                "protocol" : "all",
            },
            {
                "name" : "deny-all-inbound",
                "action" : "deny",
                "source" : "0.0.0.0/0",
                "destination" : "0.0.0.0/0",
                "direction" : "inbound",
                "protocol" : "all",
            },               
        ]

        return network_acl_rules
'''



    def check_network_acl(self):
        print("Starting Network ACL Rule Check")
        authenticator = IAMAuthenticator(self.api_key)
        resource_service = ResourceManagerV2(authenticator=authenticator)
        resource = resource_service.list_resource_groups(name=self.resource_group, include_deleted=False).get_result()
        self.resource_group_id = resource["resources"][0]["id"]

        vpc_service = VpcV1(authenticator=authenticator)
        vpc_list = vpc_service.list_vpcs(resource_group_id=self.resource_group_id).get_result()
        for vpc in vpc_list["vpcs"]:
            if vpc["name"] == self.vpc_name:
                self.vpc_id = vpc["id"]

        subnets = vpc_service.list_subnets(resource_groud_id=self.resource_group_id).get_result()["subnets"]

        for sub in subnets:
            if sub["vpc"]["id"] == self.vpc_id:
                resp = vpc_service.get_subnet_network_acl(sub["id"]).get_result()
                if not self.check_ips(resp):
                    print(Color.YELLOW + "WARNING: Please check and verify needed ACL rules are present" + Color.END)
