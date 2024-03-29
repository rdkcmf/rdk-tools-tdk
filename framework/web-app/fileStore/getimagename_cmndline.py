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


# Module imports
import sys
import signal
from getImageName import getImageName

# To enable time out
class NotFoundException(Exception):
    pass
    
def timeout(signum, frame):
    raise NotFoundException
		
# Check the number of arguments and print the syntax if args not equal to 5
if ( (len(sys.argv)) != 3):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address PortNumber"
        print "eg    : python " + sys.argv[0] + " <Valid DUT IP Address> 8087"
        exit()

# Assigning Box IP address, port number
boxipaddress = sys.argv[1]
port = int (sys.argv[2])

#SIGALRM is only usable on a unix platform
signal.signal(signal.SIGALRM, timeout)

#change 15 to any other desired value
signal.alarm(5)

try:
    status = getImageName(boxipaddress, port)
    print status
except NotFoundException:
    print "NOT_FOUND"
