# Saas infrastructure module

module "saas_infra" {
  source  = "./major_version"

  for_each = var.deployment_config.major_versions

  ws_name = var.ws_name
  major_version = each.key
  major_version_deployment_config = each.value

  include_test_public = var.include_test_public
  include_test_private = var.include_test_private
  include_main_public = var.include_main_public
  include_main_private = var.include_main_private
  secure_test_private = var.secure_test_private
  secure_main_private = var.secure_main_private
  private_allow_tenant_role_whitelist = var.private_allow_tenant_role_whitelist
}
