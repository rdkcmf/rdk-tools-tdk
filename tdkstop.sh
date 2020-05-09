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
APPLN_HOME_PATH=/tmp
APP_MOUNT_PATH=/media/apps

tst_file=$APP_MOUNT_PATH/testfile
touch $tst_file
if [ -e $tst_file ]; then
	APPLN_HOME_PATH=$APP_MOUNT_PATH
	rm $tst_file
fi
rdm_tdk_stop_script=$APPLN_HOME_PATH/tdk-dl/var/TDK/StopTDK.sh
tdk_stop_script=/opt/TDK/StopTDK.sh

is_tdk_as_rdm()
{
  package=`cat /etc/rdm/rdm-manifest.json | grep "app_name" | grep -i tdk | cut -d "\"" -f4`
  if [[ "$package" == "tdk-dl" ]]; then
    echo "tdk-dl is RDM package in this build"
    return 1
  else
    echo "tdk-dl RDM package is not available.. it is traditional TDK build"
    return 0
  fi
}

is_tdk_as_rdm
if [ $? -eq 1 ]; then
  sh $rdm_tdk_stop_script
else
  sh $tdk_stop_script
fi
