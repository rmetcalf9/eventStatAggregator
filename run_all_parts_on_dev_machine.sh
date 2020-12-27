#!/bin/bash

echo "This script launches all the components on a development machine"
echo "It can be used to testing"

tmux \
  new-session  "cd ./services ; ./run_app_developer.sh" \; \
  split-window "cd ./services ; ./run_msgproc_developer.sh" \; \
  select-layout main-horizontal \; \
  select-pane -t 0 \; \
  split-window "cd ./util/devMachineTester ; ./run.sh"




