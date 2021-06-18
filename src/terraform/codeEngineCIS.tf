#
# 1. Creating Global Load Balancer
#

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
  description      = "example health check"
  follow_redirects = true
}

# Creating the origin pool resource using Terraform
resource "ibm_cis_origin_pool" "example" {
    cis_id          = data.ibm_cis.cis_instance.id       
    name            = "test-pool-1"
    origins {
        name        = "app-server-1"
        address     = data.ibm_cis_domain.cis_instance_domain.domain   
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
    cis_id            = data.ibm_cis.cis_instance.id        
    domain_id         = data.ibm_cis_domain.cis_instance_domain.id    
    name              = data.ibm_cis_domain.cis_instance_domain  
    fallback_pool_id  = ibm_cis_origin_pool.example.id
    default_pool_ids  = [ibm_cis_origin_pool.example.id]
    description       = "example load balancer using Terraform"
    enabled           = true
    proxied           = true
}

#
# 2. Creating Edge Certificate
#

resource "ibm_cis_certificate_order" "test" {
    cis_id    = data.ibm_cis.cis_instance.id      
    domain_id = data.ibm_cis_domain.cis_instance_domain.id  
    hosts     = [data.ibm_cis_domain.cis_instance_domain,"*."+data.ibm_cis_domain.cis_instance_domain] 
}

###############################
# 3. Creating Edge Function
###############################

# Add a Edge Functions Trigger to the domain
resource "ibm_cis_edge_functions_trigger" "test_trigger" {
  cis_id      = ibm_cis_edge_functions_action.test_action.cis_id
  domain_id   = ibm_cis_edge_functions_action.test_action.domain_id
  action_name = ibm_cis_edge_functions_action.test_action.action_name
  pattern_url = data.ibm_cis_domain.cis_instance_domain
}

# Add a Edge Functions Trigger to the domain
resource "ibm_cis_edge_functions_trigger" "test_trigger2" {
  cis_id      = ibm_cis_edge_functions_action.test_action.cis_id
  domain_id   = ibm_cis_edge_functions_action.test_action.domain_id
  action_name = ibm_cis_edge_functions_action.test_action.action_name
  pattern_url = "www."+data.ibm_cis_domain.cis_instance_domain
}

# Add a Edge Functions Action to the domain
resource "ibm_cis_edge_functions_action" "test_action" {
  cis_id      = data.ibm_cis.cis_instance.id
  domain_id   = data.ibm_cis_domain.cis_instance_domain.id
  action_name = "gcat-interns-rock-com"  #input
  script      = file("./edge_function_method.js")
}

data "ibm_resource_group" "group" {
  name = "Interns-2021"   #input
}

data "ibm_cis_domain" "cis_instance_domain" {
  domain = "gcat-interns-rock.com"  #input
  cis_id = data.ibm_cis.cis_instance.id
}

data "ibm_cis" "cis_instance" {
  name              = "Internet Services-v7"  #input
  resource_group_id = data.ibm_resource_group.group.id
}


