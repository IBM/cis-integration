module ibm_cis_integration {
    source = "./ce/terraform"
    cis_name = var.cis_name
    resource_group = var.resource_group
    app_url = var.app_url
    cis_domain = var.cis_domain
    ibmcloud_api_key = var.ibmcloud_api_key
    pool_name = var.pool_name
}