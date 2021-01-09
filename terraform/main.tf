# main.tf

module "saas_infra" {
  source  = "./saas_infra"

  ws_name = "test_service"
  major_version = "0"
  version_underscore = "0_1_23"
}

