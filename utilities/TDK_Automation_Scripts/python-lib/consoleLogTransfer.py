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
import tftpy
import socket
import select

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def consoleLogTransfer(deviceIP,agentPort,logTransferPort,fileName,localFilePath):

        # Syntax       : consoleLogTransfer.consoleLogTransfer (deviceIP,agentPort,logTransferPort,fileName,localFilePath)
        # Description  : Sends a json query to get path to console log file and transfer the same.
        # Parameters   : deviceIP - IP address of the device under test.
	#		 agentPort - Port Number of the device under test. 
	#		 logTransferPort - Port Number for log transfer using TFTP.
	#		 fileName - Name of log file.
	#		 localFilePath - Path to which the file is transferred.
        # Return Value : Nil

	# Sending JSON request to get log path
	try:
        	tcpClient = socket.socket()
        	tcpClient.connect((deviceIP, agentPort))

       		jsonMsg = {'jsonrpc':'2.0','id':'2','method':'GetAgentConsoleLogPath'}
     		query = json.dumps(jsonMsg)
        	tcpClient.send(query) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		resultIndex = result.find("result") + len("result"+"\":\"")

                message = result[resultIndex:]
                message = message[:(message.find("\""))]
		sys.stdout.flush()

	except socket.error:
		print "ERROR: Unable to connect agent.." 
		sys.stdout.flush()
		sys.exit()

	# Transferring file using TFTP
	try:

		remoteFile = message + "/" + fileName
		localFile = localFilePath + "/" + fileName
		print localFile
		print remoteFile
		client = tftpy.TftpClient( deviceIP, logTransferPort )
		client.download( remoteFile, localFile, timeout=20 )
	except TypeError:
      		print "Connection Error!!! Transfer of " + remoteFile + " Failed: Make sure Agent is running"
		sys.exit()

	except:
      		print "Error!!! Transfer of " + remoteFile + " Failed.."
		sys.exit()

# End of File
