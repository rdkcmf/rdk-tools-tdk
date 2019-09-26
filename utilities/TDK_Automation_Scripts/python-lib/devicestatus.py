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
import socket
import select
import json

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def getStatus(deviceIP,managerIP,boxName,statusPort):

        # Syntax       : devicestatus.getStatus( deviceIP, managerIP, boxName, statusPort)
        # Description  : Sends a json query and decides the status of device from the json response.
        # Parameters   : deviceIP - IP address of the device whose status to be checked.
		#				 managerIP - IP address of test manager.
		#				 boxName - Box friendly name.
		#				 statusPort - port used for status checking.
        # Return Value : Returns string which holds status of device.

	try:
        	port = statusPort
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'getHostStatus','managerIP':managerIP,'boxName':boxName}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 5) #Setting timeout for response(3 Sec)
		if recvStatus[0]:
	       		result = tcpClient.recv(1048) #Receiving response
			tcpClient.close()
			if "Free" in result:
        			return "FREE"
			if "Busy" in result:
        			return "BUSY"

		else:
			tcpClient.close()
			return "HANG"

	except socket.error:
		return "NOT_FOUND"

