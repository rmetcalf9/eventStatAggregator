# main.tf

module "saas_infra" {
  source  = "./saas_infra"

  ws_name = var.ws_name
  deployment_config = var.deployment_config

  include_test_public = false
  # include_test_private = false
  # include_main_public = false
  # include_main_private = false
  # secure_test_private = false
  # secure_main_private = false

  #private_allow_tenant_role_whitelist = [
  #  "aa:bb",
  #  "cc:dd"
  #]
}

