# config.tf

terraform {
  required_providers {
    kong = {
      source = "greut/kong"
      version = "5.3.0"
    }
  }
}

provider "kong" {
    kong_admin_uri = var.kong_admin_uri
}

