##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
###########################################################################

import subprocess
import sys
#!!!!!!!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!!!!
#Need to install sshpass before executing this script

#Usage example
if((len(sys.argv))!=7):
        print "Usage : python " + sys.argv[0] + " DeviceIP username password LogFileName DestinationFolderPath DestinationFileName"
        print "eg    : python " + sys.argv[0] + " <Valid DUT IP Address> root None /opt/logs/wpeframework.log /home/tdk/LOGS boxLog.log"

else:
    host_ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    file_name = sys.argv[4]
    dest_path = sys.argv[5]
    dest_file_name = sys.argv[6]
    #COPY FILES FROM DEVICE
    try:
        scp_command = 'sshpass -p '+password+' scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '+ username + '@' +host_ip +':'+file_name+' '+dest_path+'/'
        p = subprocess.Popen(scp_command,shell=True)
        sts = p.wait()
    except Exception as error:
        print "Failed to copy files from device"
        print error
