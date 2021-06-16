variable "ibmcloud_api_key" {}
variable "cis_crn" {}
variable "zone_id" {}
variable "app_url" {}

provider "ibm" {
    ibmcloud_api_key = var.ibmcloud_api_key
}