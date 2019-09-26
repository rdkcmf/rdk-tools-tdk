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

cd $TDK_PATH

rm cpu.log memused.log

while read line
do

    sed -e '0,/Average:        CPU/d' -e '/Average:         eth1/,$d' sysStatAvg.log > performance.temp

    cat performance.temp | awk 'BEGIN { RS="" ; FS="\n" } { print $2 }' | awk '{print $8}' >> cpu.log

    cat performance.temp  | awk 'BEGIN { RS="" ; FS="\n" } { print $8 }' | awk '{print$2,$3,$4}' >> memused.log

    sed -e '1,25d' < sysStatAvg.log > temp

    mv temp sysStatAvg.log

done < sysStatAvg.log

echo "Performance data Extracted"
