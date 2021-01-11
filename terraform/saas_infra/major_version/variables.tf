variable "ws_name" {
  description = "Name of webservice"
}

variable "major_version" {
  description = "Major version used in endpoints"
}

variable "major_version_deployment_config" {
  description = "Describes the current test and main versions for THIS major version"
  type = object({
    main_version = string,
    test_version = string
  })
}

