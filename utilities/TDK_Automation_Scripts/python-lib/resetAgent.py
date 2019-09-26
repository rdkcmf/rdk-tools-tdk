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
import sys

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def resetAgent(deviceIP,devicePort,enableReset):

        # Syntax       : resetAgent.resetAgent (deviceIP,devicePort,enableReset)
        # Description  : Sends a json message to reset agent.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 devicePort - Port Number of the device under test.
	#		 enableReset - true/false 
	#		 true - To restart agent
	#		 false - To reset device state to FREE
        # Return Value : Nil

	try:
        	port = devicePort
        	tcpClient = socket.socket()
		tcpClient.settimeout(5.0)
        	tcpClient.connect((deviceIP, port))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'ResetAgent','enableReset':enableReset}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		resultIndex = result.find("result") + len("result"+"\":\"")

                message = result[resultIndex:]
                message = message[:(message.find("\""))]
                if "SUCCESS" in message.upper():
			print "Test timed out.. Agent Reset.."
		else:
			print "Test timed out.. Failed to reset agent.."
		sys.stdout.flush()

	except socket.error:
		print "ERROR: Script timed out.. Unable to reach agent.." 
		sys.stdout.flush()

