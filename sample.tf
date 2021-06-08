# Creating the monitor (health check) resource using Terraform
resource "ibm_cis_healthcheck" "test" {
  cis_id           = [CRN]
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
    cis_id          = [CRN]
    name            = "test-pool-1"
    origins {
        name        = "app-server-1"
        address     = [APP_NAME]
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
    cis_id            = [CRN]
    domain_id         = [DOMAIN_ID]
    name              = [DOMAIN_NAME]
    fallback_pool_id  = ibm_cis_origin_pool.example.id
    default_pool_ids  = [ibm_cis_origin_pool.example.id]
    description       = "example load balancer using Terraform"
    enabled           = true
    proxied           = true
}
