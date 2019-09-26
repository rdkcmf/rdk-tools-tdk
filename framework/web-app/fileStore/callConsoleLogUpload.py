#!/usr/bin/python
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


#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import sys
from consoleLogUpload import consoleLogUpload

if((len(sys.argv))!=6):
	print "Usage : python " + sys.argv[0] + " DeviceIP AgentMonitorPortNumber BoxFileName TMFileName logUploadURL"
	print "eg    : python " + sys.argv[0] + " 192.168.160.189 8090 \"AgentConsole.log\" \"111_222_333_AgentConsole.log\" http://192.168.160.101:8080/rdk-test-tool/"

else:
	deviceIP = sys.argv[1]
	agentMonitorPort = (int)(sys.argv[2])
	boxFileName = sys.argv[3]
	tmFileName = sys.argv[4]
	logUploadURL = sys.argv[5]
	consoleLogUpload(deviceIP,agentMonitorPort,boxFileName,tmFileName,logUploadURL)
