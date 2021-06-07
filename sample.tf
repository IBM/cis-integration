# Creating the monitor (health check) resource using Terraform
resource "ibm_cis_healthcheck" "test" {
  cis_id           = "crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::"
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
    cis_id          = "crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::"
    name            = "test-pool-1"
    origins {
        name        = "app-server-1"
        address     = "demo-app.9y43h3pccht.us-south.codeengine.appdomain.cloud"
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
    cis_id            = "crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::"
    domain_id         = "f4604bfab1a024690e30bfd72ae36727"
    name              = "gcat-interns-rock.com"
    fallback_pool_id  = ibm_cis_origin_pool.example.id
    default_pool_ids  = [ibm_cis_origin_pool.example.id]
    description       = "example load balancer using Terraform"
    enabled           = true
    proxied           = true
}
