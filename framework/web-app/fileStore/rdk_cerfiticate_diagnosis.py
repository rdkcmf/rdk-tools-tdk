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
##########################################################################
import sys, os
from SSHUtility import ssh_and_execute
#Function to disable print from SSHUtility
def StopPrint():
    sys.stdout = open(os.devnull, 'w')
#Function to enable print
def StartPrint():
    sys.stdout = sys.__stdout__
dev_ip = str(sys.argv[1])
StopPrint()
output = ssh_and_execute("directSSH",dev_ip,"root","","cat /version.txt")
StartPrint()
file_not_present = 'No such file or directory'
if file_not_present in output:
    print "version.txt file is missing"
else:
    print "version.txt file is available"