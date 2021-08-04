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
    type = string
    description = "Cluster ID of the IKS instance"
}

variable standard {
    type = bool
    description = "Determines whether the CIS instance is using the Standard Plan"
}

variable create_ce {
    type = bool
    description = "Whether or not to build the CodeEngine module"
    default         = false
}

variable create_iks {
    type            = bool
    description     = "Whether or not to build the IKS module"
    default         = false
}