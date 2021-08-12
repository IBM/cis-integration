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

module ibm_cis_ce_integration {
    source = "../ce/terraform"
    ibmcloud_api_key = var.ibmcloud_api_key
    cis_name = var.cis_name
    resource_group = var.resource_group
    app_url = var.app_url
    cis_domain = var.cis_domain
    pool_name = var.pool_name
    standard = var.standard
    count = (var.create_ce) ? 1 : 0
}

module ibm_cis_iks_integration {
    source = "../iks/terraform"
    ibmcloud_api_key = var.ibmcloud_api_key
    cis_name = var.cis_name
    resource_group = var.resource_group
    cis_domain = var.cis_domain
    cluster_id = var.cluster_id
    count = (var.create_iks) ? 1 : 0
}