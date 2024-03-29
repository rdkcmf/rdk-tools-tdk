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

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import sys
from setTDKAvailablity import setTDKAvailablity

if((len(sys.argv))!=4):
	print "Invalid Arguments !!!"
	print "Usage : python " + sys.argv[0] + " DeviceIP PortNumber option(enable/disable)"
	print "eg    : python " + sys.argv[0] + " <Valid DUT IP Address> 8088 enable"

else:
	deviceIP = sys.argv[1]
	devicePort = (int)(sys.argv[2])
	option = sys.argv[3]
	retVal = setTDKAvailablity(deviceIP,devicePort,option)

