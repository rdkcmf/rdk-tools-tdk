#!/bin/bash

##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
#

#Start hub
start_hub()
{
        export DISPLAY=:10
        java -jar $var2 -role hub -host $var3 > $var4 2>&1 &
        sleep 10
        value="$(cat $var4 | grep "Selenium Grid hub is up and running" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}
#To start node
start_node()
{
        export DISPLAY=:10
        java -jar $var2 -role node -host $var5 -hub http://$var3:4444/grid/register/ > $var4 2>&1 &
        sleep 20
        value="$(cat $var4 | grep "The node is registered to the hub and ready to use" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}
kill_selenium()
{
        sudo kill -9 `echo $(ps -ef | grep selenium | grep -v grep|awk '{print $2;}')`
}

# Store the arguments to a variable
event=$1
var2=$2
var3=$3
var4=$4
var5=$5

# Invoke the function based on the argument passed
case $event in
   "start_hub")
        start_hub;;
   "start_node")
        start_node;;
   "kill_selenium")
        kill_selenium;;
   *) echo "Invalid Argument passed";;
esac
