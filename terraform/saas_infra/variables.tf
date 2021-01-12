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

variable "include_test_public" {
  description = "Should the main public endpoint be included"
  type = bool
  default = true
}

variable "include_test_private" {
  description = "Should the main public endpoint be included"
  type = bool
  default = true
}

variable "include_main_public" {
  description = "Should the main public endpoint be included"
  type = bool
  default = true
}

variable "include_main_private" {
  description = "Should the main public endpoint be included"
  type = bool
  default = true
}
