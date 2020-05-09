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
SCRIPT_AT_RDM_DLPATH=/media/apps/tdk-dl/var/TDK/StartTDK.sh
SCRIPT_AT_TMP_DLPATH=/tmp/tdk-dl/var/TDK/StartTDK.sh

LOG_FILE=/opt/TDK/tdk_service.log
LOG_PATH=/opt/TDK/
[ ! -d $LOG_PATH ] && mkdir -p $LOG_PATH
[ -f $LOG_FILE ] && rm $LOG_FILE

log_msg() {
  DateTime=`date "+%m%d%y-%H:%M:%S:%N"`
  #check if parameter non zero size
  if [ -n "$1" ];
  then
    STR="$1"
  fi
  #print log message
  echo "[$DateTime] [pid=$$] $STR" >>$LOG_FILE
  echo "[$DateTime] [pid=$$] $STR"
}

start_script=""
checkscript_presence()
{
    if [ -e $SCRIPT_AT_RDM_DLPATH ]; then
        start_script=$SCRIPT_AT_RDM_DLPATH
                log_msg $start_script
    elif [ -e $SCRIPT_AT_TMP_DLPATH ]; then
        start_script=$SCRIPT_AT_TMP_DLPATH
                log_msg $start_script
    fi
}

log_msg "systemctl status apps-rdm.service"
systemctl status apps-rdm.service >> $LOG_FILE
log_msg "systemctl status apps_rdm.path"
systemctl status apps_rdm.path >> $LOG_FILE
log_msg $APPLN_HOME_PATH
log_msg $start_script
check_tdk_download()
{
  count=0
  #Iterating for maximum 60 times with 10sec wait time util package is downloaded.
  while [ "$count" -lt "60" ]
  do
    rdm_status=`cat /opt/persistent/rdmDownloadInfo.txt | grep "tdk-dl"  | awk {'print $5'}`
    log_msg $rdm_status
    if [[ "$rdm_status" == "SUCCESS" ]]; then
        log_msg "Checking if timestamp in image name and package name specified in rdmDownloadInfo.txt are matching"
        timestamp_image=`cat /version.txt | grep -i "imagename" | cut -d ":" -f2 | sed 's/.*_\([0-9]\{8,\}\).*/\1/'`
        timestamp_rdm_tdkv_package=`cat /opt/persistent/rdmDownloadInfo.txt | grep "tdk-dl" | awk {'print $2'} | sed 's/.*_\([0-9]\{8,\}\).*/\1/'`
        if [[ "$timestamp_image" == "$timestamp_rdm_tdkv_package" ]]; then
            log_msg "timestamp in image name and package name specified in rdmDownloadInfo.txt are matching.."
            checkscript_presence
            if [ ! -z $start_script ]; then
                log_msg "tdk-dl RDM package is downloaded sccessfully and also startup script is found..."
                return 1
            else
                log_msg "tdk-dl RDM package downloade status is success but startup script is not present in the package..."
                log_msg "count is $count"
                log_msg $start_script
                sleep 10
                ((count++))
            fi
        else
            log_msg "timestamp in image name and package name specified in rdmDownloadInfo.txt are not matching..."
            log_msg "Waiting for 10 second to have latest RDM tdk-dl paackage downloaded..."
            log_msg "count is $count"
            sleep 10
            ((count++))
        fi
    else
        log_msg "Download is in progress or not started... waiting for 10 seconds"
        sleep 10
        log_msg "count is $count"
        ((count++))
    fi
  done
  log_msg "300 seconds wait time is completed.. but tdk-dl package is not downloaded.."
  return 0
}
is_tdk_as_rdm()
{
  package=`cat /etc/rdm/rdm-manifest.json | grep "app_name" | grep -i tdk | cut -d "\"" -f4`
  if [[ "$package" == "tdk-dl" ]]; then
    log_msg "tdk-dl RDM package is available for download"
    return 1
  else
    log_msg "tdk-dl RDM package is not available.. it is traditional TDK build"
    return 0
  fi
}


is_tdk_as_rdm
if [ $? -eq 1 ]; then
  log_msg "Checking if TDK RDM package is downloaded..after box rebooted or service restarted"
  check_tdk_download
  ret=$?
  if [ $ret -eq  1 ]; then
    log_msg "Starting StartTDK.sh.."
    $start_script
  else
    log_msg "Failed to start TDK startup scripts"
  fi
else
  log_msg "TDK is not RDM in this build. It is traditional TDK build"
  log_msg "Starting TDK..."
  rm -rf /opt/TDK/lib*
  cp -r /var/TDK /opt/
  sh /opt/TDK/StartTDK.sh
fi

