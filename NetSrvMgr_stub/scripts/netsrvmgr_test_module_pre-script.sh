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
NMCONFIG_PATH=/etc
TARGET_PATH=/opt
LOG_PATH=$TDK_PATH/logs
NMLOG_PATH=$TARGET_PATH/logs
CONF_FILE=netsrvmgr.conf
NM_LOG_FILE=netsrvmgr.log
LOGFILE=netsrvmgr_testmodule_prereq_details.log
mkdir -p $LOG_PATH
#removing old pre_requisite log from the opt
rm $LOG_PATH/$LOGFILE
#removing old netsrvmgr.log file from /opt
rm $NMLOG_PATH/$NM_LOG_FILE

#Function to copy the /etc/netsrvmgr.conf to /opt
copy_netsrvconfig(){
        cp $NMCONFIG_PATH/$CONF_FILE $TARGET_PATH/
        if [ $? == 0 ]; then
                sed -i '/imagename=/d' $TARGET_PATH/$CONF_FILE
                echo "imagename="$imagename >> $TARGET_PATH/$CONF_FILE
                echo "image name is set"
                sed -i '/WiFiMgr_Config/a disableWpsXRE=1' $TARGET_PATH/$CONF_FILE
                if [ $? -eq 0 ]; then
                        echo "disableWpsXRE set"
                        touch $LOG_PATH/$LOGFILE
                        echo  "SUCCESS" > $LOG_PATH/$LOGFILE
                else
                        echo "sed utillity is not found"
                        touch $LOG_PATH/$LOGFILE
                        echo  "Failure<details>sed utillity is not found" > $LOG_PATH/$LOGFILE
                        exit 1
                fi
                grep -q -F 'ENABLE_LOST_FOUND' $TARGET_PATH/$CONF_FILE
                if [ $? == 0 ]; then
                        sed -i -e 's/ENABLE_LOST_FOUND=0/ENABLE_LOST_FOUND=1/g' $TARGET_PATH/$CONF_FILE
                        echo "ENABLE_LOST_FOUND set"
                else
                        sed -i '/WiFiMgr_Config/a ENABLE_LOST_FOUND=1' $TARGET_PATH/$CONF_FILE
                        echo "ENABLE_LOST_FOUND set"
                fi
                echo "Going to restart netsrvmgr.service"
                systemctl restart netsrvmgr.service
                if [ $? -eq 0 ]; then
                        echo "Successfully restarted netsrvmgr service"
                        touch $LOG_PATH/$LOGFILE
                        echo  "SUCCESS" > $LOG_PATH/$LOGFILE
                else
                        echo "Restarting netsrvmgr service failed"
                        touch $LOG_PATH/$LOGFILE
                        echo  "Failure<details>netsrvmgr restart failed" > $LOG_PATH/$LOGFILE
                        exit 1
                fi
        fi
}

imagename=`cat /version.txt|grep imagename:|cut -d: -f 2`
echo $imagename
ls $TARGET_PATH/$CONF_FILE
if [ $? == 0 ]; then

        cat $TARGET_PATH/$CONF_FILE|grep "imagename="$imagename && cat $TARGET_PATH/$CONF_FILE|grep "disableWpsXRE=1"
        if [ $? == 0 ]; then
                echo "Proper netsrvmgr is present"
                touch $LOG_PATH/$LOGFILE
                echo  "SUCCESS" > $LOG_PATH/$LOGFILE
        else
                #need to copy the latest netsrvmgr.conf file
                copy_netsrvconfig
        fi
else
         #need to copy netsrvmgr.conf since its not found in /opt
         copy_netsrvconfig
fi
