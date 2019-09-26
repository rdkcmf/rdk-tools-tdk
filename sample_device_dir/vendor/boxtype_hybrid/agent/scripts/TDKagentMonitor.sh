##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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

loop=1
sleep 60

# To monitor TDK Agent process and reboot box on its crash
while [ $loop -eq 1 ]
do
   status=`ps | grep tdk_agent_monitor | grep -v grep` #Make sure ps will list all process. In some platform it is "ps -ef".
   if [ ! "$status" ]; 
   then 
       echo "TDK agent monitor crashed.. Box going for Reboot.."
       echo $(date) >> $TDK_PATH/monitorcrash.log
       sleep 10 && /rebootNow.sh -s TDKagentRecovery -o "Rebooting the box since TDK agent monitor process crashed..." 
   fi
   sleep 5

done
