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

# Module Imports
import socket
import sys
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

# Check the number of arguments and print the syntax if args not equal to 5
if((len(sys.argv))!=5):
        print "Usage : python " + sys.argv[0] + " DeviceIP AgentMonitorPortNumber BoxFileName TMFileName"
        print "eg    : python " + sys.argv[0] + " 192.168.160.189 8090 \"/version.txt\" \"111_222_333_version.txt\""
	sys.exit()

# Assigning IP address, port number and path of source and destination files
deviceIP = sys.argv[1]
agentMonitorPort = int (sys.argv[2])
boxFile = sys.argv[3]
tmFile = sys.argv[4]

try:
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

#End of file
