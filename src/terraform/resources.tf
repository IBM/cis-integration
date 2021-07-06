# Creating the www DNS Record
resource "ibm_cis_dns_record" "test_dns_www_record" {
    cis_id  = data.ibm_cis.cis_instance.id
    domain_id = data.ibm_cis_domain.cis_instance_domain.domain_id
    name    = "www"
    type    = "CNAME"
    content = var.app_url
    proxied = true
}

# Creating the root DNS Record
resource "ibm_cis_dns_record" "test_dns_root_record" {
    cis_id  = data.ibm_cis.cis_instance.id
    domain_id = data.ibm_cis_domain.cis_instance_domain.domain_id
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
    cis_id    = data.ibm_cis.cis_instance.id          
    domain_id = data.ibm_cis_domain.cis_instance_domain.domain_id  
    hosts     = [var.cis_domain, var.wild_domain]   
}

# Creating the monitor (health check) resource using Terraform
resource "ibm_cis_healthcheck" "test" {
  cis_id           = data.ibm_cis.cis_instance.id       
  expected_codes   = "200"
  method           = "GET"
  timeout          = 2
  path             = "/"
  type             = "https"
  interval         = 60
  retries          = 3
  description      = "default health check"
  follow_redirects = true
}

# Creating the origin pool resource using Terraform
resource "ibm_cis_origin_pool" "example" {
    cis_id          = data.ibm_cis.cis_instance.id       
    name            = var.pool_name
    origins {
        name        = "default-origin"
        address     = var.app_url     
        enabled     = true
    }
    description     = "origin pool created with cis-integration tool"
    enabled = true
    minimum_origins = 1
    check_regions   = ["ENAM"]
    monitor         = ibm_cis_healthcheck.test.monitor_id
}

# Creating the global load balancer resource using Terraform
resource "ibm_cis_global_load_balancer" "example-glb" {
    cis_id            = data.ibm_cis.cis_instance.id        
    domain_id         = data.ibm_cis_domain.cis_instance_domain.domain_id      
    name              = var.cis_domain     
    fallback_pool_id  = ibm_cis_origin_pool.example.id
    default_pool_ids  = [ibm_cis_origin_pool.example.id]
    description       = "global load balancer created with cis-integration tool"
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

# Add a Edge Functions Trigger to the domain
resource "ibm_cis_edge_functions_trigger" "test_trigger3" {
  cis_id      = ibm_cis_edge_functions_action.test_action.cis_id
  domain_id   = ibm_cis_edge_functions_action.test_action.domain_id
  action_name = ibm_cis_edge_functions_action.test_action.action_name
  pattern_url = var.wild_domain # add * to cis_domain
}

# Add a Edge Functions Action to the domain
resource "ibm_cis_edge_functions_action" "test_action" {
  cis_id      = data.ibm_cis.cis_instance.id
  domain_id   = data.ibm_cis_domain.cis_instance_domain.domain_id
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
