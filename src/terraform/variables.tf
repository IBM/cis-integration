variable ibmcloud_api_key {
    type = string
    description = "Unique API Key to verify access permissions"
    validation {
    # regex(...) fails if it cannot find a match
    condition     = length(var.ibmcloud_api_key)==44
    error_message = ""
  }
}
variable cis_name {
    type = string
    description = "Name of the CIS instance"
  validation {
      condition = can(regex("^([^[:ascii:]]|[a-zA-Z0-9-._: ])+$", var.cis_name))
      error_message = "Not a valid CIS Name"
  }
}
variable resource_group {
    type = string
    description = "Name of the group the resource was created under"
}
variable app_url {
    type = string
    description = "URL generated for the code engine app"
    validation {
    # regex(...) fails if it cannot find a match
    condition     = can(regex("^([^[:ascii:]]|[a-zA-Z0-9-._: ])+$", var.app_url))
    error_message = "This is not a valid url for the code engine app"
  }
}
variable cis_domain {
    type = string
    description = "Domain name that you want to be attached to the CIS Instance and Code Engine app"
    validation {
    # regex(...) fails if it cannot find a match
    condition     = can(regex("/((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/", var.cis_domain))
    error_message = "This is not a valid domain name for the CIS Instance"
  }
}
variable action_name {
    type = string
    description = "Name for the Edge Function Action"
}