module ibm_cis_ce_integration {
    source = "../ce/terraform"
    ibmcloud_api_key = var.ibmcloud_api_key
    cis_name = var.cis_name
    resource_group = var.resource_group
    app_url = var.app_url
    cis_domain = var.cis_domain
    pool_name = var.pool_name
}

module ibm_cis_iks_integration {
    source = "../iks/terraform"
    ibmcloud_api_key = var.ibmcloud_api_key
    cis_name = var.cis_name
    resource_group = var.resource_group
    cis_domain = var.cis_domain
    cluster_id = var.cluster_id
    token = var.token
}