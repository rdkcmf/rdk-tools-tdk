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

echo "Stopping TDK Agent.."
export TDK_PATH=/opt/TDK #Path where TDK libs and bins are installed

sleep 1

#Killing inactive TDK processes
#Make sure "ps -ef" list all running process or make changes in below commands accordingly.
ps -ef | grep "tdk_agent" | grep -v "grep" | grep -v "tr69agent" | awk '{print $2}' | xargs kill -9 >& /dev/null
ps -ef | grep "tftp" | grep -v "grep" | awk '{print $2}' | xargs kill -9 >& /dev/null
ps -ef | grep $TDK_PATH | grep -v "grep" | awk '{print $2}' | xargs kill -9 >& /dev/null
sleep 2

echo "Done"
