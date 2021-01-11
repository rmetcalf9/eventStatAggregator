# variables.tf

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
