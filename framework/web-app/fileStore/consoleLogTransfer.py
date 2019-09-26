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
import json
import socket

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


def consoleLogTransfer(deviceIP,agentMonitorPort,boxFileName,tmFileName):

        # Syntax       : consoleLogTransfer.consoleLogTransfer (deviceIP,agentMonitorPort,boxFileName,tmFileName)
        # Description  : Sends a json query to get path to console log file and transfer the same.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 agentMonitorPort - Port Number of the device under test.
	#		 boxFileName - Name of log file in box.
	#		 tmFileName - Name in which the file is saved in TM after transferring.
        # Return Value : Nil

	# Sending JSON request to get log path
	try:
		tcpClient = getSocketInstance(deviceIP)
		tcpClient.connect((deviceIP, agentMonitorPort))

		#jsonMsg = {'jsonrpc':'2.0','id':'2','method':'GetAgentConsoleLogPath'}
		jsonMsg = '{"jsonrpc":"2.0","id":"2","method":"getAgentConsoleLogPath"}\r\n'
		#query = json.dumps(jsonMsg)
		tcpClient.send(jsonMsg) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()
		data = json.loads(result)
		result=data["result"]
		message=result["result"]

		sys.stdout.flush()

	except socket.error:
		print "ERROR: Unable to connect agent.." 
		sys.stdout.flush()
		sys.exit()

	# Transferring file using TFTP
	try:

		boxFile = message + "/" + boxFileName
		tmFile = tmFileName
		tcpClient = getSocketInstance(deviceIP)
		tcpClient.connect((deviceIP, agentMonitorPort))

		# Sending message to push the logs from STB to TM
		#jsonMsg = {'jsonrpc':'2.0','id':'2','method':'PushLog','STBfilename':boxFile,'TMfilename':tmFile}
		jsonMsg = '{"jsonrpc":"2.0","id":"2","method":"PushLog","params":{"STBfilename":"'+ boxFile +'","TMfilename":"'+ tmFile +'"}}\r\n'
		#query = json.dumps(jsonMsg)
		#tcpClient.send(query) #Sending json query
		tcpClient.send(jsonMsg) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()
		data = json.loads(result)
		result=data["result"]
		message=result["result"]
		print message

		sys.stdout.flush()

        except socket.error:
		print "ERROR: Unable to connect agent.."
		sys.stdout.flush()
		sys.exit()

	except TypeError:
		print "Connection Error!!! Transfer of " + boxFile + " Failed: Make sure Agent is running"
		sys.exit()

	except:
		print "Error!!! Transfer of " + boxFile + " Failed.."
		sys.exit()

# End of File
