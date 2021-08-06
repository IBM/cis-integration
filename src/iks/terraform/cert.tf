data ibm_resource_instance cm {
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

resource ibm_certificate_manager_order cert {
  count = var.cert_name == "cis_cert" ? 1 : 0
  certificate_manager_instance_id = data.ibm_resource_instance.cm.id
  name                            = var.cert_name
  description                     = "Certificate for connecting CIS to IKS cluster"
  domains                         = [var.cis_domain, "*.${var.cis_domain}"]
  dns_provider_instance_crn       = data.ibm_cis.cis_instance.id
  auto_renew_enabled              = true
}

resource null_resource create_cert_secret_via_api {
    count = var.cert_name == "cis_cert" ? 1 : 0

    provisioner local-exec {
        command = <<BASH
      URL_ENCODED_CMS_ID=$(echo ${ibm_certificate_manager_order.cert[0].id} | sed 's/:/%3A/g' | sed 's/\//%2F/g')
      REGION=$(echo ${ibm_certificate_manager_order.cert[0].id} | cut -d'.' -f 1)

      CERT=$(curl -X GET https://$REGION.certificate-manager.cloud.ibm.com/api/v2/certificate/$URL_ENCODED_CMS_ID
          -H "Authorization: ${data.ibm_iam_auth_token.token.iam_access_token}"
        )
      STATUS=$(
          echo $CERT | jq -r ".status"
        )

      while [ "$STATUS" == "pending" ]
      do
        CERT=$(curl -X GET https://$REGION.certificate-manager.cloud.ibm.com/api/v2/certificate/$URL_ENCODED_CMS_ID
          -H "Authorization: ${data.ibm_iam_auth_token.token.iam_access_token}"
        )
        STATUS=$(
          echo $CERT | jq -r ".status"
        )
      done

      if [ "$STATUS" == "valid" ]; then
        RESPONSE=$(curl -X POST https://containers.cloud.ibm.com/global/ingress/v2/secret/createSecret \
          -H "Authorization: ${data.ibm_iam_auth_token.token.iam_access_token}" \
          -d '{
              "cluster" : "${var.cluster_id}",
              "crn" : "${ibm_certificate_manager_order.cert[0].id}",
              "name" : "${var.cert_name}",
              "namespace" : "default",
              "persistence" : true
          }'
        )

        ERROR=$(echo $RESPONSE | jq -r ".incidentID")

        if [ "$ERROR" != "null" ]; then
          echo $ERROR
          exit 2
        fi
      fi
      
        BASH 
    }
    
}

# Setting TLS mode to strict
# Setting minimum TLS version to 1.2
resource ibm_cis_domain_settings test {
    cis_id          = data.ibm_cis.cis_instance.id
    domain_id       = data.ibm_cis_domain.cis_instance_domain.domain_id 
    ssl             = "strict"
    min_tls_version = "1.2"
}

# Ordering a TLS certificate
resource ibm_cis_certificate_order test {
    cis_id    = data.ibm_cis.cis_instance.id          
    domain_id = data.ibm_cis_domain.cis_instance_domain.domain_id  
    hosts     = [var.cis_domain, "*.${var.cis_domain}"]   
}

# Creating the www DNS Record
resource ibm_cis_dns_record test_dns_www_record {
    cis_id  = data.ibm_cis.cis_instance.id
    domain_id = data.ibm_cis_domain.cis_instance_domain.domain_id
    name    = "www"
    type    = "CNAME"
    content = var.ingress
    proxied = true
}

# Creating the root DNS Record
resource ibm_cis_dns_record test_dns_root_record {
    cis_id  = data.ibm_cis.cis_instance.id
    domain_id = data.ibm_cis_domain.cis_instance_domain.domain_id
    name    = "@"
    type    = "CNAME"
    content = var.ingress
    proxied = true
}