# Add a Edge Functions Trigger to the domain
resource "ibm_cis_edge_functions_trigger" "test_trigger" {
  cis_id      = ibm_cis_edge_functions_action.test_action.cis_id
  domain_id   = ibm_cis_edge_functions_action.test_action.domain_id
  action_name = ibm_cis_edge_functions_action.test_action.action_name
  pattern_url = "gcat-interns-rock.com"
}

# Add a Edge Functions Trigger to the domain
resource "ibm_cis_edge_functions_trigger" "test_trigger2" {
  cis_id      = ibm_cis_edge_functions_action.test_action.cis_id
  domain_id   = ibm_cis_edge_functions_action.test_action.domain_id
  action_name = ibm_cis_edge_functions_action.test_action.action_name
  pattern_url = "www.gcat-interns-rock.com"
}

# Add a Edge Functions Action to the domain
resource "ibm_cis_edge_functions_action" "test_action" {
  cis_id      = data.ibm_cis.cis_instance.id
  domain_id   = data.ibm_cis_domain.cis_instance_domain.id
  action_name = "gcat-interns-rock-com"
  script      = file("./edge_function_method.js")
}

data "ibm_resource_group" "group" {
  name = "Interns-2021"
}

data "ibm_cis_domain" "cis_instance_domain" {
  domain = "gcat-interns-rock.com"
  cis_id = data.ibm_cis.cis_instance.id
}

data "ibm_cis" "cis_instance" {
  name              = "Internet Services-v7"
  resource_group_id = data.ibm_resource_group.group.id
}


