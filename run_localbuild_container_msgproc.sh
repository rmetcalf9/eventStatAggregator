#!/bin/bash

echo "Script to run a local container in msgproc mode"

if [[ ! -f ./VERSION ]]; then
  echo "VERSION dosen't exist - are you in correct directory?"
  exit 1
fi
export RJM_VERSION=$(cat ./VERSION)
export RJM_VERSION_UNDERSCORE=$(echo ${RJM_VERSION} | tr '.' '_')
export RJM_IMAGE_TO_RUN=metcarob/eventstataggregator:${RJM_VERSION}_localbuild
export RJM_RUNNING_SERVICE_NAME=eventstataggregator${RJM_VERSION_UNDERSCORE}_localbuild

echo "Launching image ${RJM_IMAGE_TO_RUN}"

##Check if container image exists
docker image inspect ${RJM_IMAGE_TO_RUN} > /dev/null
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Image dosen't exist"
  echo "Have you run compile_frontend_and_build_container.sh to generate ${RJM_IMAGE_TO_RUN}?"
  echo ""
  exit 1
fi

##TODO Check if running and error
docker service inspect ${RJM_RUNNING_SERVICE_NAME} > /dev/null
RES=$?
if [ ${RES} -ne 1 ]; then
  echo "Service already runing"
  echo "use service rm ${RJM_RUNNING_SERVICE_NAME} to stop"
  echo ""
  exit 1
fi


docker service create --name ${RJM_RUNNING_SERVICE_NAME} \
--network main_net \
--mount type=bind,source=$(pwd),destination=/ext_volume \
--no-healthcheck \
-e APIAPP_OBJECTSTORECONFIG="{\"Type\": \"SQLAlchemy\",\"connectionString\": \"sqlite:///ext_volume/services/objectstoredata/mainfile.db\", \"create_engine_args\": {\"poolclass\": \"StaticPool\", \"connect_args\": {\"check_same_thread\":false}}}" \
-e APIAPP_MQCLIENTCONFIG="{ \"Type\": \"Stomp\", \"ConnectionString\": \"stomp://dmu-activemq:61613\", \"Username\": \"admin\", \"Password\": \"admin\" }" \
-e APIAPP_USERMANAGERCONFIG="{ \"baseURL\": \"MOCK\", \"tenant\": \"linkvis\", \"originToUseInRequests\": \"http://127.0.0.1:8099\" }" \
-e APIAPP_LISTENDESTLIST="[{\"tenant\":\"dev\", \"name\":\"/queue/eventCountTestQueue001\"}, {\"tenant\":\"dev\", \"name\":\"/queue/eventCountTestQueue002\"},{\"tenant\":\"dev2\", \"name\":\"/queue/eventCountTestQueue003\"}, {\"tenant\":\"dev2\", \"name\":\"/queue/eventCountTestQueue004\"}]" \
${RJM_IMAGE_TO_RUN} \
"/run_msgproc_docker.sh" \
"/queue/inboundConnectorExecutions"
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Failed to start service"
  echo ""
  exit 1
fi

echo "Complete"
echo ""
echo "End docker service rm ${RJM_RUNNING_SERVICE_NAME} to stop"
echo ""
exit 0
