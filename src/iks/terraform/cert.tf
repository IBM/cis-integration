# DISCLAIMER OF WARRANTIES:
# Permission is granted to copy this Tools or Sample code for internal use only, provided that this
# permission notice and warranty disclaimer appears in all copies.
#
# THIS TOOLS OR SAMPLE CODE IS LICENSED TO YOU AS-IS.
# IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE,
# INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A
# PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR ANY DAMAGES ARISING
# OUT OF THE USE OF OR INABILITY TO USE THE TOOLS OR SAMPLE CODE, DISTRIBUTION OF THE TOOLS OR SAMPLE CODE,
# OR COMBINATION OF THE TOOLS OR SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND
# SUPPLIERS BE LIABLE FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL,
# CONSEQUENTIAL,INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
# EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

data "ibm_resource_instance" "cm" {
  name              = "kube-certmgr-${var.cluster_id}"
  resource_group_id = data.ibm_resource_group.group.id
  service           = "cloudcerts"
}

data ibm_resource_group group {
  name = var.resource_group
}

data ibm_cis_domain cis_instance_domain {
  domain = var.cis_domain
  cis_id = data.ibm_cis.cis_instance.id
}

data ibm_cis cis_instance {
  name              = var.cis_name
  resource_group_id = data.ibm_resource_group.group.id
}

data ibm_iam_auth_token token {}

resource "ibm_certificate_manager_order" "cert" {
  certificate_manager_instance_id = data.ibm_resource_instance.cm.id
  name                            = "test"
  description                     = "test description"
  domains                         = [var.cis_domain, "*.${var.cis_domain}"]
  dns_provider_instance_crn       = data.ibm_cis.cis_instance.id
  auto_renew_enabled              = true
}

resource null_resource create_cert_secret_via_api {

    provisioner local-exec {
        command = <<BASH
curl -X POST https://containers.cloud.ibm.com/global/ingress/v2/secret/createSecret \
    -H "Authorization: ${data.ibm_iam_auth_token.token.iam_access_token}" \
    -d '{
        "cluster" : "${var.cluster_id}",
        "crn" : "${ibm_certificate_manager_order.cert.id}",
        "name" : "cis-cert",
        "namespace" : "default",
        "persistence" : true
    }'
        BASH 
    }
    
}