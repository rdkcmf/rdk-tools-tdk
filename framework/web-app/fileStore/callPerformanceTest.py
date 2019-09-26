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

# Module Imports
import sys
import socket
import json

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

def tftpDownload(ipaddrs,agentmonitorport,boxFile,tmFile):

	# Connect to TFTP server and download the file
	try:
		tcpClient = getSocketInstance(ipaddrs)
		tcpClient.connect((ipaddrs, agentmonitorport))

		# Sending message to push the logs from STB to TM
		#jsonMsg = {'jsonrpc':'2.0','id':'2','method':'PushLog','STBfilename':boxFile,'TMfilename':tmFile}
		jsonMsg = '{"jsonrpc":"2.0","id":"2","method":"PushLog","parameter":{"STBfilename":'+ boxFile +',"TMfilename":'+ tmFile +'}}\r\n'
		#query = json.dumps(jsonMsg)
		#tcpClient.send(query) #Sending json query
		tcpClient.send(jsonMsg) #Sending json query

		result = tcpClient.recv(1048) #Receiving response
		tcpClient.close()

		data = json.loads(result)
		result=data["result"]
		message=result["result"]
		print message.upper()

		sys.stdout.flush()

	except TypeError:
		print "Connection Error!!! Transfer of " + boxFile + " Failed: Make sure Agent is running"
		sys.exit()

	except:
		print "Error!!! Transfer of " + boxFile + " Failed.."
		sys.exit()


# Check the number of arguments and print the syntax if args not equal to 6
if ( (len(sys.argv)) != 6):
	print "Usage : python " + sys.argv[0] + " Device_IP_Address Agent_Port_Number Agent_Monitor_Port RPC_Method TM_File_Name"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8087 8090 RPC_Method_Name(PerformanceBenchMarking/PerformanceSystemDiagnostics) \"11_22_33_44version.txt\""
	exit()

# Assigning IP address, port numbers, path of destination files and rpcmethod to be invoked
ipaddrs = sys.argv[1]
deviceport = int (sys.argv[2])
agentmonitorport = int (sys.argv[3])
rpcmethod = sys.argv[4]
tmfilename = sys.argv[5]

# Sending json request and receiving response
try:
	tcpClient = getSocketInstance(ipaddrs)
	tcpClient.connect((ipaddrs, deviceport))

	#jsonMsg = {'jsonrpc':'2.0','id':'2','method':rpcmethod}
	jsonMsg = '{"jsonrpc":"2.0","id":"2","method":'rpcmethod'}\r\n'
	#query = json.dumps(jsonMsg)
	#tcpClient.send(query) #Sending json query
	tcpClient.send(jsonMsg) #Sending json query

	result = tcpClient.recv(1048) #Receiving response

	tcpClient.close()

	# Extracting result and logpath from response message
	data = json.loads(result)
	result=data["result"]
	message=result["result"]
	print message.upper()

	message=result["logpath"]
	logpath = message
	print "Log Path : " + logpath

except socket.error:
	print "Unable to reach agent"
	exit()


if "PerformanceSystemDiagnostics" in rpcmethod:

	# Constructing path for remote and local files
	boxFile = logpath + "/cpu.log"
	tmFile = tmfilename + "_cpu.log"

	tftpDownload(ipaddrs, agentmonitorport, boxFile, tmFile)

	# Constructing path for remote and local files
	boxFile = logpath + "/memused.log"
	tmFile = tmfilename + "_memused.log"

	tftpDownload(ipaddrs, agentmonitorport, boxFile, tmFile)

else:
	# Constructing path for remote and local files
	filename = logpath.split("/")[-1]
	boxFile = logpath
	tmFile = tmfilename + "_" +filename

        tftpDownload(ipaddrs, agentmonitorport, boxFile, tmFile)

# End of File
