#!/bin/bash

echo "Script to run a local container which can be accessed via container access descrubed in FRONTEND_NOTES"

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

#Removed
##-e APIAPP_OBJECTSTORECONFIGFILE=/run/secrets/saas_user_management_system_objectstore_config \
##-e APIAPP_DEFAULTHOMEADMINPASSWORDFILE=/run/secrets/saas_user_management_system_objectstore_adminpw \
#and added
##-e APIAPP_DEFAULTHOMEADMINPASSWORD=admin \
# to enable container tests to run and login as admin

#TODO Remove APIAPP_DEFAULTMASTERTENANTJWTCOLLECTIONALLOWEDORIGINFIELD as I think it's not needed

docker service create --name ${RJM_RUNNING_SERVICE_NAME} \
--network main_net \
--mount type=bind,source=$(pwd),destination=/ext_volume \
-e APIAPP_APIURL=${EXTURL}:${EXTPORT80}/api \
-e APIAPP_APIDOCSURL=${EXTURL}:${EXTPORT80}/public/web/apidocs \
-e APIAPP_FRONTENDURL=${EXTURL}:${EXTPORT80}/public/web/frontend \
-e APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN="http://localhost" \
-e APIAPP_OBJECTSTORECONFIG="{\"Type\": \"SimpleFileStore\",\"BaseLocation\": \"/ext_volume/services/objectstoredata\"}" \
-e APIAPP_USERMANAGERCONFIG="{ \"baseURL\": \"MOCK\", \"tenant\": \"linkvis\", \"originToUseInRequests\": \"http://127.0.0.1:8099\" }" \
--publish 80:80 \
${RJM_IMAGE_TO_RUN}
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Failed to start service"
  echo ""
  exit 1
fi

echo "Complete"
echo "Start from http://127.0.0.1/public/web/frontend/#/"
echo ""
echo "End docker service rm ${RJM_RUNNING_SERVICE_NAME} to stop"
echo ""
exit 0
