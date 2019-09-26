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
import json
import sys

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

def getImageName(deviceIP,devicePort):

        # Syntax       : getImageName.getImageName( deviceIP,devicePort )
        # Description  : Sends a json query to get the RDK image name on device.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test. 
        # Return Value : Returns string which holds RDK image name on device.

	try:
		tcpClient = getSocketInstance(deviceIP)
		tcpClient.connect((deviceIP, devicePort))

       		#jsonMsg = {'jsonrpc':'2.0','id':'2','method':'getImageName'}
       		jsonMsg = '{"jsonrpc":"2.0","id":"2","method":"getImageName"}\r\n'
     		#query = json.dumps(jsonMsg)
        	#tcpClient.send(query) #Sending json query
        	tcpClient.send(jsonMsg) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		if "Method not found" in result:
			message = "METHOD_NOT_FOUND"
			#sys.stdout.flush()
		else:
			data = json.loads(result)
			resultJson = data["result"]
			message = resultJson["result"]
			sys.stdout.flush()
		return message

	except socket.error:
		#print "AGENT_NOT_FOUND"
		#sys.stdout.flush()
		return "AGENT_NOT_FOUND"
