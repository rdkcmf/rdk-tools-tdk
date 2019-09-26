#!/bin/sh
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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
TOOL_PATH=$1
IP=$(awk -F"@" '/Manager IP/{ip=$2}END{print ip}' $TDK_PATH/tdkconfig.ini )
cd /home/root
export HOME=/home/root/
remote_testrunner_url="sparkui"
if [[ $TOOL_PATH =~ $remote_testrunner_url ]]
then
    ./pxscene $TOOL_PATH &
else
    if [[ $IP =~ .*:.* ]]
    then
      ./pxscene http://[$IP]:8080/$TOOL_PATH/testRunner.js &
    else
      ./pxscene http://$IP:8080/$TOOL_PATH/testRunner.js &
    fi
fi
sleep 600
pkill pxscene
