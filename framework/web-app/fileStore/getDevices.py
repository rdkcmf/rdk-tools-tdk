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

def getConnectedDevices(deviceIP,devicePort):

        # Syntax       : getDevices.getConnectedDevices( deviceIP,devicePort )
        # Description  : Sends a json query to get the MAC address of connected devices from the json response.
        # Parameters   : deviceIP - IP address of the device under test(Gateway box).
	#		 devicePort - Port Number of the device under test(Gateway box). 
        # Return Value : Returns string which holds MAC address of connected devices.

	try:
        	port = devicePort
		tcpClient = getSocketInstance(deviceIP)
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = '{"jsonrpc":"2.0","id":"2","method":"getConnectedDevices"}\r\n'
     		#query = json.dumps(jsonMsg)
        	tcpClient.send(jsonMsg) #Sending json query
                #tcpClient.sendall('{"jsonrpc":"2.0","id":"2","method":"getConnectedDevices"}\r\n')
        	#tcpClient.sendall('{"jsonrpc":"2.0","id":"2","method":"getHostStatus","params":{"boxName":"pacexg1v3","managerIP":"106"}}\r\n') #Sending json query

		tcpClient.setblocking(0)
		recvStatus = select.select([tcpClient], [], [], 3) #Setting timeout for response(3 Sec)
		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close() 
		data = json.loads(result)
		result=data["result"]
		message=result["result"]
		print message

	except socket.error:
		print "AGENT_NOT_FOUND"

