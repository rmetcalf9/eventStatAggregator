
resource "kong_service" "service_test_private" {
	count = var.include_test_private ? 1 : 0

	name     	= format("TF_%s_v%s_TEST_PRIVATE", var.ws_name, var.major_version)
	protocol 	= "http"
	host     	= format("tasks.%s_%s", var.ws_name, replace(var.major_version_deployment_config.test_version, ".", "_"))
	port     	= 80
	path     	= "/private/"
	retries  	= 5
	connect_timeout = 60000
	write_timeout 	= 60000
	read_timeout  	= 60000
}

resource "kong_route" "route_test_private" {
	count = var.include_test_private ? 1 : 0

	protocols 	    = [ "https" ]
	hosts 		    = [ format("api.metcarob.com") ]
	paths 		    = [ format("/%s/test/v%s/private", var.ws_name, var.major_version) ]
	strip_path 	    = true
	preserve_host 	= false
	regex_priority 	= 0
	service_id 	    = kong_service.service_test_private[count.index].id
}

resource "kong_service" "service_private" {
	count = var.include_main_private ? 1 : 0

	name     	= format("TF_%s_v%s_PRIVATE", var.ws_name, var.major_version)
	protocol 	= "http"
	host     	= kong_upstream.upstream[count.index].name
	port     	= 80
	path     	= "/private/"
	retries  	= 5
	connect_timeout = 60000
	write_timeout 	= 60000
	read_timeout  	= 60000
}

resource "kong_route" "route_private" {
	count = var.include_main_private ? 1 : 0

	protocols 	    = [ "https" ]
	hosts 		    = [ format("api.metcarob.com") ]
	paths 		    = [ format("/%s/v%s/private", var.ws_name, var.major_version) ]
	strip_path 	    = true
	preserve_host 	= false
	regex_priority 	= 0
	service_id 	    = kong_service.service_private[count.index].id
}
