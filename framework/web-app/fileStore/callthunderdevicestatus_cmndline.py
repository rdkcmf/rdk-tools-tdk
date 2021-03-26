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
###########################################################################
import sys
import requests
import json

if ( (len(sys.argv)) != 3):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address Thunder_Port"
        print "eg    : python " + sys.argv[0] + " 192.168.160.229 9998"
        exit()
else:
    data = '{"jsonrpc":"2.0","id":"3","method": "Controller.1.status@Controller"}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+sys.argv[1]+':'+sys.argv[2]+'/jsonrpc'

    try:
        response = requests.post(url, headers=headers, data=data, timeout=3)
        if response.status_code == 200:
            print "FREE"
        else:
            print "NOT_FOUND"

    except Exception as e:
        print "NOT_FOUND"
