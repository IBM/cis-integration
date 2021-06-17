variable "ibmcloud_api_key" {}
variable "cis_name" {}
variable "resource_group" {}
variable "app_url" {}
variable "cis_domain" {}
variable "www_domain" {}
variable "action_name" {}

provider "ibm" {
    ibmcloud_api_key = var.ibmcloud_api_key
}