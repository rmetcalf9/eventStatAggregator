
resource "kong_service" "service_test_private" {
	name     	= format("TF_%s_v%s_TEST_PRIVATE", var.ws_name, var.major_version)
	protocol 	= "http"
	host     	= format("tasks.%s_%s", var.ws_name, var.version_underscore)
	port     	= 80
	path     	= "/private/"
	retries  	= 5
	connect_timeout = 60000
	write_timeout 	= 60000
	read_timeout  	= 60000
}

resource "kong_route" "route_test_private" {
	protocols 	    = [ "https" ]
	hosts 		    = [ format("api.metcarob.com") ]
	paths 		    = [ format("/%s/test/v%s/private", var.ws_name, var.major_version) ]
	strip_path 	    = true
	preserve_host 	= false
	regex_priority 	= 0
	service_id 	    = kong_service.service_test_private.id
}

resource "kong_service" "service_private" {
	name     	= format("TF_%s_v%s_PRIVATE", var.ws_name, var.major_version)
	protocol 	= "http"
	host     	= kong_upstream.upstream.name
	port     	= 80
	path     	= "/private/"
	retries  	= 5
	connect_timeout = 60000
	write_timeout 	= 60000
	read_timeout  	= 60000
}

resource "kong_route" "route_private" {
	protocols 	    = [ "https" ]
	hosts 		    = [ format("api.metcarob.com") ]
	paths 		    = [ format("/%s/v%s/private", var.ws_name, var.major_version) ]
	strip_path 	    = true
	preserve_host 	= false
	regex_priority 	= 0
	service_id 	    = kong_service.service_private.id
}
