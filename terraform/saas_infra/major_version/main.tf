# infrastructure for single microservice endpoint

resource "kong_upstream" "upstream" {
  count = (var.include_main_public || var.include_main_private) ? 1 : 0

  name                 = format("TF_%s_%s", var.ws_name, var.major_version)
  slots                = 	10000
}

resource "kong_target" "target" {
  count = (var.include_main_public || var.include_main_private) ? 1 : 0

  target  		= format("tasks.%s_%s:80", var.ws_name, replace(var.major_version_deployment_config.main_version, ".", "_"))
  weight 	  	= 100
  upstream_id = kong_upstream.upstream[count.index].id
}
