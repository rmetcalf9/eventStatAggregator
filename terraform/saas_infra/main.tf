# Saas infrastructure module

resource "kong_upstream" "upstream" {
  name                 = format("TF_%s_%s", var.ws_name, var.major_version)
  slots                = 	10000
}

resource "kong_target" "target" {
    target  		= format("tasks.%s_%s:80", var.ws_name, var.version_underscore)
    weight 	  	= 100
    upstream_id = kong_upstream.upstream.id
}
