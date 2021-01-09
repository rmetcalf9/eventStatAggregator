# main.tf

module "saas_infra" {
  source  = "./saas_infra"

  ws_name = var.ws_name
  major_version = var.major_version
  version_underscore = var.version_underscore
}

