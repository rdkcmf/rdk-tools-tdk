##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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
import json;
import pycurl
import os
import sys
from StringIO import StringIO

response_buffer = StringIO()
curl = pycurl.Curl()

if ( (len(sys.argv)) != 2):
	print "Usage : python " + sys.argv[0] + " Device_IP_Address"
	print "eg    : python " + sys.argv[0] + " 192.168.160.229"
	exit()
else:
	url = 'http://'+sys.argv[1]+'/Service/DeviceInfo'
	curl.setopt(curl.URL, url)
	curl.setopt(pycurl.HTTPGET, True)
	curl.setopt(curl.WRITEFUNCTION, response_buffer.write)
	curl.perform()
	response = response_buffer.getvalue()
	statusCode = curl.getinfo(pycurl.RESPONSE_CODE);

	if statusCode == 200:
		print "FREE"
	else:
		print "NOTFOUND"	