resource "ibm_cis_certificate_order" "test" {
    cis_id    = "crn:v1:bluemix:public:internet-svcs:global:a/cdefe6d99f7ea459aacb25775fb88a33:d6097e79-fd41-4dd3-bdc9-342fe1b28073::"  
    domain_id = "f4604bfab1a024690e30bfd72ae36727"
    hosts     = ["gcat-interns-rock.com"]
}