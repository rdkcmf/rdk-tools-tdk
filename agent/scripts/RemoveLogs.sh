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


#export LOG_PATH=/opt/logs/
cd /opt/logs
if [ -d "$1" ]
 then
    echo "file $1 found"
    rm -rf $1
  else
    echo "folder  not found"
fi
if [ -f "$1.tgz" ]
  then
    echo "file $1.tgz found"
    rm $1.tgz
  else
    echo "file $1.tgz not found"
fi

#rm -rf $LOG_PATH/$1
