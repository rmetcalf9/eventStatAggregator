#!/bin/bash

echo "saas_linkvi_connectorss - run_msgproc_developer.sh"

PYTHON_CMD=python3
if [ E${EXTPYTHONCMD} != "E" ]; then
  PYTHON_CMD=${EXTPYTHONCMD}
fi

#pyCharm will run in project root directory. Check if we are here and if so then change into services directory
if [ -d "./services" ]; then
  echo "Changing into services directory"
  cd ./services
fi

PYTHONVERSIONCHECKSCRIPT="import sys\nprint(\"Python version \" + str(sys.version_info))\nif sys.version_info[0] < 3:\n  exit(1)\nif sys.version_info[0] == 3:\n  if sys.version_info[1] < 6:\n    exit(1)\nexit(0)\n"
printf "${PYTHONVERSIONCHECKSCRIPT}" | ${PYTHON_CMD}
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Wrong python version - this version won't have all the required libraries"
  echo "Using command ${PYTHON_CMD}"
  echo "you can set enviroment variable EXTPYTHONCMD to make this script use a different python command"
  echo ""
  exit 1
fi

APP_DIR=.

export APIAPP_OBJECTSTORECONFIG="{\"Type\": \"SQLAlchemy\",\"connectionString\": \"sqlite:///objectstoredata/mainfile.db\", \"create_engine_args\": {\"poolclass\": \"StaticPool\", \"connect_args\": {\"check_same_thread\":false}}}"

export APIAPP_MQCLIENTCONFIG="{ \"Type\": \"Stomp\", \"ConnectionString\": \"stomp://127.0.0.1:61613\", \"Username\": \"admin\", \"Password\": \"admin\", \"clientId\": \"run_msgproc_developer\" }"

export APIAPP_LISTENDESTLIST="[{\"tenant\":\"dev\", \"name\":\"/queue/eventCountTestQueue001\",\"durableSubscriptionName\":\"run_msgproc_developer\"}, {\"tenant\":\"dev\", \"name\":\"/queue/eventCountTestQueue002\",\"durableSubscriptionName\":\"run_msgproc_developer\"},{\"tenant\":\"dev2\", \"name\":\"/queue/eventCountTestQueue003\",\"durableSubscriptionName\":\"run_msgproc_developer\"}, {\"tenant\":\"dev2\", \"name\":\"/queue/eventCountTestQueue004\",\"durableSubscriptionName\":\"run_msgproc_developer\"}]"

export APIAPP_VERSION=
if [ -f ${APP_DIR}/VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/VERSION)
fi
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${APIAPP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi

#Python app reads most parameters from environment variables but destinations from args
${PYTHON_CMD} ./src/msgproc.py
RES=$?
if [ $RES -ne 0 ]; then
  echo "Process Errored"
  read -p "Press enter to continue"
fi
