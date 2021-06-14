resource "ibm_cis_dns_record" "test_dns_www_record" {
    cis_id  = var.cis_crn
    domain_id = var.zone_id
    name    = "www"
    type    = "CNAME"
    content = var.app_url
    proxied = true
}

resource "ibm_cis_dns_record" "test_dns_root_record" {
    cis_id  = var.cis_crn
    domain_id = var.zone_id
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