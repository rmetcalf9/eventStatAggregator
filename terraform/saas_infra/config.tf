# See https://github.com/greut/terraform-provider-kong

terraform {
  required_providers {
    kong = {
      source = "greut/kong"
      version = "5.3.0"
    }
  }
}
