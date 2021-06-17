
<<<<<<< HEAD
# Creating the www DNS Record
=======
>>>>>>> c5eadaf (working on terraform files to better align with what the CLI needs)
resource "ibm_cis_dns_record" "test_dns_www_record" {
    cis_id  = data.ibm_cis.cis_instance.id
    domain_id = data.ibm_cis_domain.cis_instance_domain.id
    name    = "www"
    type    = "CNAME"
    content = var.app_url
    proxied = true
}

resource "ibm_cis_dns_record" "test_dns_root_record" {
    cis_id  = data.ibm_cis.cis_instance.id
    domain_id = data.ibm_cis_domain.cis_instance_domain.id
    name    = "@"
    type    = "CNAME"
    content = var.app_url
    proxied = true
}

output "cname_www_record_output" {
    value = ibm_cis_dns_record.test_dns_www_record
}

output "cname_root_record_output" {
    value = ibm_cis_dns_record.test_dns_root_record
}

# Ordering a TLS certificate
resource "ibm_cis_certificate_order" "test" {
    cis_id    = data.ibm_cis.cis_instance.id        # placeholder 
    domain_id = data.ibm_cis_domain.cis_instance_domain.id  # placeholder
    hosts     = var.cis_domain   # placeholder
}

# Creating the monitor (health check) resource using Terraform
resource "ibm_cis_healthcheck" "test" {
  cis_id           = data.ibm_cis.cis_instance.id       # placeholder
  expected_codes   = "200"
  method           = "GET"
  timeout          = 2
  path             = "/"
  type             = "https"
  interval         = 60
  retries          = 3
  description      = "example health check"
  follow_redirects = true
}

# Creating the origin pool resource using Terraform
resource "ibm_cis_origin_pool" "example" {
    cis_id          = data.ibm_cis.cis_instance.id       # placeholder
    name            = "test-pool-1"
    origins {
        name        = "app-server-1"
        address     = var.app_url     # placeholder
        enabled     = true
    }
    description     = "example origin pool"
    enabled = true
    minimum_origins = 1
    check_regions   = ["WEU"]
    monitor         = ibm_cis_healthcheck.test.monitor_id
}

# Creating the global load balancer resource using Terraform
resource "ibm_cis_global_load_balancer" "example-glb" {
    cis_id            = data.ibm_cis.cis_instance.id        # placeholder
    domain_id         = data.ibm_cis_domain.cis_instance_domain.id      # placeholder
    name              = var.cis_domain     # placeholder
    fallback_pool_id  = ibm_cis_origin_pool.example.id
    default_pool_ids  = [ibm_cis_origin_pool.example.id]
    description       = "example load balancer using Terraform"
    enabled           = true
    proxied           = true
}



# Add a Edge Functions Trigger to the domain
resource "ibm_cis_edge_functions_trigger" "test_trigger" {
  cis_id      = ibm_cis_edge_functions_action.test_action.cis_id
  domain_id   = ibm_cis_edge_functions_action.test_action.domain_id
  action_name = ibm_cis_edge_functions_action.test_action.action_name
  pattern_url = var.cis_domain
}

# Add a Edge Functions Trigger to the domain
resource "ibm_cis_edge_functions_trigger" "test_trigger2" {
  cis_id      = ibm_cis_edge_functions_action.test_action.cis_id
  domain_id   = ibm_cis_edge_functions_action.test_action.domain_id
  action_name = ibm_cis_edge_functions_action.test_action.action_name
  pattern_url = var.www_domain # add www to cis_domain
}

# Add a Edge Functions Action to the domain
resource "ibm_cis_edge_functions_action" "test_action" {
  cis_id      = data.ibm_cis.cis_instance.id
  domain_id   = data.ibm_cis_domain.cis_instance_domain.id
  action_name = var.action_name # change . to - in cis_domain
  script      = file("./edge_function_method.js")
}

data "ibm_resource_group" "group" {
  name = var.resource_group
}

data "ibm_cis_domain" "cis_instance_domain" {
  domain = var.cis_domain
  cis_id = data.ibm_cis.cis_instance.id
}

data "ibm_cis" "cis_instance" {
  name              = var.cis_name
  resource_group_id = data.ibm_resource_group.group.id
}


