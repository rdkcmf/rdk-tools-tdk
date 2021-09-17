#!/bin/sh
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
TEST=$1
TIMEOUT=$2

#Check if APP is specified using arguments
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
else
  #Check if APP is executable
  if which $TEST >/dev/null; then
    #Execute APP in Background
    $TEST &
  #Check if APP specified exists
  elif [ -f $TEST ]; then
    $TEST 0 &
  else
    echo "No App present"
  fi
fi

#Wait for the given time if TIMEOUT is passed to the script as a non zero value
if ([ $TIMEOUT ] && [ $TIMEOUT -ne 0 ]);then
    sleep $TIMEOUT
    pkill $TEST
fi
