##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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

import pycurl
import StringIO
import xml.etree.ElementTree as ET
import sys
from tr69Config import *

# send_xml

# Syntax      : send_xml()
# Description : Function to post a soap xml request to ACS server and to receive and parse the response from server
# Parameters  : xmlfile - xml file holding the soap xml request to be sent to server
#	      : method -  whether method is get/set 
# Return Value: status of operation. In case of get operation, returns value retrived by get also

def send_xml(xmlfile, method):

 #parse the soap xml to create a python string
 tree = ET.parse(xmlfile)
 root = tree.getroot()
 encodedBody = ET.tostring(root, encoding="UTF-8")

 #send the soap request
 curl = pycurl.Curl()
 curl.setopt(pycurl.URL, ACS_URI)
 curl.setopt(pycurl.POST, 1)
 curl.setopt(pycurl.HTTPHEADER, ["Content-type: text/xml"])
 curl.setopt(pycurl.POSTFIELDS, encodedBody)
 b = StringIO.StringIO()
 curl.setopt(pycurl.WRITEFUNCTION, b.write)
 curl.perform()
 print b.getvalue() # printing response XML
 response = b.getvalue()
 status = curl.getinfo(pycurl.HTTP_CODE)

 print "status code: %s" %status

 #parse the response xml using ElementTree library
 tree = ET.ElementTree(ET.fromstring(response))
 if status == 200:
     if method == "get":
         print "GET operation is success"
         for elem in tree.iter():
             if elem.tag == "value":
                 print "Value retreived is: ", elem.text
                 return [status, elem.text]
     else:
         print "SET operation is success"
         for elem in tree.iter():
             if elem.tag == "status":
                 print "Status: ", elem.text
                 return [status]
 else:
     print "GET/SET operation failed"
     for elem in tree.iter():
         if elem.tag == "message":
             print elem.text
             return [status]
