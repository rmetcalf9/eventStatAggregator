# variables.tf

variable "kong_admin_uri" {
  description = "e.g. http://kong:8001"
}

variable "ws_name" {
  description = "Name of webservice"
}

variable "deployment_config" {
  description = "Describes the current test and main versions for each major version"
  type = object({
    major_versions = map(
      object({
        main_version = string,
        test_version = string
      })
    )
  })

}
