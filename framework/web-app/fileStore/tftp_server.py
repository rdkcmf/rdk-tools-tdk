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
import tftpy
import socket
import sys

# Check the number of arguments and print the syntax if args not equal to 3
if ( (len(sys.argv)) != 3):
        print "Usage : python " + sys.argv[0] + " port DestinationDirectory"
        print "eg    : python " + sys.argv[0] + " 69 \"/home/anoop/tftpserver/\""
        sys.exit()

# Assigning IP address, port number and destination path
logpath = sys.argv[2]
tmIP = '0.0.0.0'
port = int (sys.argv[1])

# Starting TFTP server
try:
	print "Server listening"
	server = tftpy.TftpServer(logpath)
	server.listen(tmIP, port)

except KeyboardInterrupt:
	print "Stopping server"

# End of file
