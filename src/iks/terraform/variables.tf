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

variable ibmcloud_api_key {
    type = string
    description = "Unique API Key to verify access permissions"
    validation {
    # regex(...) fails if it cannot find a match
    condition     = length(var.ibmcloud_api_key)==44
    error_message = "This is not a valid API key."
  }
}
variable cis_name {
    type = string
    description = "Name of the CIS instance"
  validation {
      condition = can(regex("^([^[:ascii:]]|[a-zA-Z0-9-._: ])+$", var.cis_name))
      error_message = "Not a valid CIS Name."
  }
}

variable resource_group {
    type = string
    description = "Name of the group the resource was created under"
}

variable cis_domain {
    type = string
    description = "Domain name that you want to be attached to the CIS Instance and Code Engine app"
    validation {
    # regex(...) fails if it cannot find a match
    condition     = can(regex("^([^[:ascii:]]|[a-zA-Z0-9-._: ])+$", var.cis_domain))
    error_message = "This is not a valid domain name for the CIS Instance."
  }
}

variable cluster_id {
    type = string
    description = "Cluster ID of the IKS instance"
}