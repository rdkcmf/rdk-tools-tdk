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

from setRoute import setRoute
import sys

if((len(sys.argv))!=8):
        print "Usage : python " + sys.argv[0] + " DeviceIP PortNumber ClientMACaddress ClientExecutionPort ClientStatusPort clientLogTransferPort clientAgentMonitorPort"
        print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088 b4:f2:e8:de:1b:0e 9000 9001 9002 9003"

else:
	deviceIP = sys.argv[1]
	devicePort = (int)(sys.argv[2])
	clientMAC = sys.argv[3]
	clientAgentPort = (sys.argv[4])
	clientStatusPort = (sys.argv[5])
	clientLogTransferPort = (sys.argv[6])
	clientAgentMonitorPort = (sys.argv[7])

	setRoute(deviceIP,devicePort,clientMAC,clientAgentPort,clientStatusPort,clientLogTransferPort,clientAgentMonitorPort)

