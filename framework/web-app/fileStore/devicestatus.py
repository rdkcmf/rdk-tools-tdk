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


def isValidIpv6Address(ip):
                try:
                        socket.inet_pton(socket.AF_INET6, ip)
                except socket.error:  # not a valid address
                        return False
                return True

def getSocketInstance(ip):
                if isValidIpv6Address(ip):
                        tcpClient = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
                else:
                        tcpClient = socket.socket()
                return tcpClient

def getStatus(deviceIP,managerIP,boxName,statusPort):

        # Syntax       : devicestatus.getStatus( deviceIP, managerIP, boxName, statusPort)
        # Description  : Sends a json query and decides the status of device from the json response.
        # Parameters   : deviceIP - IP address of the device whose status to be checked.
	#		 managerIP - IP address of test manager.
	#		 boxName - Box friendly name.
	#		 statusPort - port used for status checking.
        # Return Value : Returns string which holds status of device.

	try:
        	port = statusPort
		tcpClient = getSocketInstance(deviceIP)
        	tcpClient.connect((deviceIP, port))

       		#jsonMsg = {'jsonrpc':'2.0','id':'2','method':'getHostStatus','params':{'managerIP':managerIP,'boxName':boxName}'\r\n'}
       		#jsonMsg = '{"jsonrpc":"2.0","id":"2","method":"getHostStatus","params":{"managerIP":"96.114.220.236","boxName":"RK04-PX1V3-6184"}\r\n}'
       		jsonMsg = '{"jsonrpc":"2.0","id":"2","method":"getHostStatus","params":{"managerIP":"'+managerIP+'","boxName":"'+boxName+'"}\r\n}' #sarves
		#query = json.dumps(jsonMsg)
     		#query = jsonMsg
        	#tcpClient.send(query) #Sending json query
        	tcpClient.send(jsonMsg) #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 5) #Setting timeout for response(3 Sec)
		if recvStatus[0]:
	       		result = tcpClient.recv(1048) #Receiving response
			tcpClient.close()
			if "Free" in result:
        			return "FREE"
			if "Busy" in result:
        			return "BUSY"
			if "TDK Disabled" in result:
				return "TDK_DISABLED"

		else:
			tcpClient.close()
			return "HANG"

	except socket.error:
		return "NOT_FOUND"

