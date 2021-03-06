#!/bin/sh
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

export PATH=$PATH:/usr/local/bin:/usr/local/lib:/usr/local/lib/sa

if [ -z "$TDK_LOG_PATH" ]
then
        echo "TDK_LOG_PATH is not defined so using TDK_PATH"
        TDK_LOG_PATH=$TDK_PATH
fi
cd $TDK_LOG_PATH

sar -r -u 1 1 | awk ' /Average:/ { print $0 }' >> sysStatAvg.log

echo "ITERATION" >> sysStatAvg.log
