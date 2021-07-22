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
    -H "Authorization: ${var.token}" \
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