# main.tf

module "saas_infra" {
  source  = "./saas_infra"

  ws_name = var.ws_name
  deployment_config = var.deployment_config
}

