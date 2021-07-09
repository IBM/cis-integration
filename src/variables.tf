variable TF_VERSION {
    default         = "0.13"
    description     = "The version of Terraform that's used in the Schematics workspace."
}

variable ibmcloud_api_key {
    description     = "The IBM Cloud platform IBM key needed for IAM enabled resources."
    type            = string
}

variable cis_name {
    description     = "The name of the CIS instance that is to be integrated with a CodeEngine application."
    type            = string
}

variable resource_group {
    description     = "The resource group that contains the CIS instance and CodeEngine application to be connected."
    type            = string
}

variable app_url {
    description     = "The URL of the CodeEngine application that is to be connected."
    type            = string
}

variable cis_domain {
    description     = "The domain of the CIS instance that is to be connected."
    type            = string
}