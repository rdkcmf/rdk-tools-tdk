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
SRC="$(dirname $1)"
cd $SRC
CMND="$4/execution/uploadLogs?fileName=$2 -F logFile=@$(basename $1)"
#Get the interface to be used from tdkconfig.ini file
INTERFACE=$(cat $TDK_PATH/tdkconfig.ini | grep "Box Interface" | cut -d@ -f 2 | tr -d '\r\n')
curl -g --interface $INTERFACE $CMND
