#!/bin/bash

echo "Start of bash file - params: $@"

if [ E${APP_DIR} = "E" ]; then
  echo 'APP_DIR not set'
  exit 1
fi

export APIAPP_VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${APIAPP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi

_term() {
  echo "run_msgproc_docker.sh - Caught SIGTERM signal!"
  kill -TERM "pythonprocess" 2>/dev/null
}

trap _term SIGTERM

echo "${0} about to call python3 command"
python3 -u ${APP_DIR}/msgproc.py "$@" &
pythonprocess=$!

wait "$pythonprocess"

echo "End of ${0}"


exit 0
