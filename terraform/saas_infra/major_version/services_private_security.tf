# JWT and ACL plugins for private endpoints

resource "kong_plugin" "service_test_private_acl" {
	count = (var.include_test_private && var.secure_test_private) ? 1 : 0

	name        = "acl"
  service_id = kong_service.service_test_private[0].id
	config_json = <<EOT
	{
		"whitelist": [ "saas_user_management" ]
	}
EOT
}

resource "kong_plugin" "service_test_private_jwt" {
	count = (var.include_test_private && var.secure_test_private) ? 1 : 0

	name        = "jwt"
  service_id = kong_service.service_test_private[0].id
	config_json = <<EOT
	{
    "secret_is_base64": true,
		"uri_param_names": [ "jwt" ],
    "key_claim_name": "kong_iss",
    "header_names": [
      "authorization"
    ],
    "claims_to_verify": [
      "exp"
    ],
    "cookie_names": [
      "jwt-auth-cookie"
    ]
	}
EOT
}

resource "kong_plugin" "service_private_acl" {
	count = (var.include_main_private && var.secure_main_private) ? 1 : 0

	name        = "acl"
  service_id = kong_service.service_private[0].id
	config_json = <<EOT
	{
		"whitelist": [ "saas_user_management" ]
	}
EOT
}

resource "kong_plugin" "service_private_jwt" {
	count = (var.include_main_private && var.secure_main_private) ? 1 : 0

	name        = "jwt"
  service_id = kong_service.service_private[0].id
	config_json = <<EOT
	{
		"secret_is_base64": true,
		"uri_param_names": [ "jwt" ],
    "key_claim_name": "kong_iss",
    "header_names": [
      "authorization"
    ],
    "claims_to_verify": [
      "exp"
    ],
    "cookie_names": [
      "jwt-auth-cookie"
    ]
	}
EOT
}
