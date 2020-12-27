#!/bin/bash

#Not used by codefresh as I am using build container instead

#working directory is always saas_linkvis root
GITROOT=$(pwd)
DOCKER_USERNAME=metcarob
DOCKER_IMAGENAME=eventStatAggregator
VERSIONNUM=$(cat ./VERSION)

docker image inspect ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}_localbuild > /dev/null
RES=$?
if [ ${RES} -eq 0 ]; then
  docker rmi ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}_localbuild
  RES2=$?
  if [ ${RES2} -ne 0 ]; then
    echo "Image exists and delete failed"
    exit 1
  fi
fi

echo "Build docker container (VERSIONNUM=${VERSIONNUM})"
#This file does no version bumping
cd ${GITROOT}
eval docker build . -t ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}_localbuild
RES=$?
if [ ${RES} -ne 0 ]; then
  echo ""
  echo "Docker build failed"
  exit 1
fi

exit 0
