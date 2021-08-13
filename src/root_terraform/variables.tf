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

variable TF_VERSION {
    default         = "0.14"
    description     = "The version of Terraform that's used in the Schematics workspace."
}

variable ibmcloud_api_key {
    description     = "The IBM Cloud platform IBM key needed for IAM enabled resources."
    type            = string
    default         = "null"
}

variable cis_name {
    description     = "The name of the CIS instance that is to be integrated with a CodeEngine application."
    type            = string
    default         = "test"
}

variable resource_group {
    description     = "The resource group that contains the CIS instance and CodeEngine application to be connected."
    type            = string
    default         = "test"
}

variable app_url {
    description     = "The URL of the CodeEngine application that is to be connected."
    type            = string
    default         = "test"
}

variable cis_domain {
    description     = "The domain of the CIS instance that is to be connected."
    type            = string
    default         = "test"
}

variable pool_name {
    description     = "Name of the pool attached to the CIS Instance"
    type            = string
    default         = "test"
}

variable cluster_id {
    type            = string
    description     = "Cluster ID of the IKS instance"
    default         = "null"

}

variable standard {
    type            = bool
    description     = "Determines whether the CIS instance is using the Standard Plan"
    default         = false
}

variable create_ce {
    type            = bool
    description     = "Whether or not to build the CodeEngine module"
    default         = false
}

variable create_iks {
    type            = bool
    description     = "Whether or not to build the IKS module"
    default         = false
}

variable ingress {
    type            = string
    description     = "Ingress subdomain of IKS cluster"
    default         = "null"
}

variable cert_name {
    type            = string
    description     = "Name of certificate/secret in IKS"
    default         = "null"
}