# variables.tf

variable "kong_admin_uri" {
  description = "e.g. http://kong:8001"
}

variable "ws_name" {
  description = "Name of webservice"
}

variable "major_version" {
  description = "Major version used in endpoints"
}

variable "version_underscore" {
  description = "version with underscores e.g. 0_0_123"
}

