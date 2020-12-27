#!/bin/bash

export APIAPP_MQCLIENTCONFIG="{ \"Type\": \"Stomp\", \"ConnectionString\": \"stomp://127.0.0.1:61613\", \"Username\": \"admin\", \"Password\": \"admin\" }"

python3 ./main.py
RES=$?
if [ $RES -ne 0 ]; then
  echo "Process Errored"
  read -p "Press enter to continue"
fi
