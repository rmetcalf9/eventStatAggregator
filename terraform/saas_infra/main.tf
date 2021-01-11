# Saas infrastructure module

module "saas_infra" {
  source  = "./major_version"

  for_each = var.deployment_config.major_versions

  ws_name = var.ws_name
  major_version = each.key
  major_version_deployment_config = each.value
}
