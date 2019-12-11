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

import json;
import pycurl
import os
from StringIO import StringIO
from webpaVariables import *
import snmplib;
from time import sleep;
from tdkbVariables import *;

def webpaQuery(obj, parameter, method="get"):
# webpaQuery

# Syntax      : webpaQuery(obj,parameter, method="get")
# Description : Function to create and send curl request to WEBPA server
# Parameters  : obj - Object of the tdk library
#               parameter - parameter list to be passed on to the curl request
#             : method - whether the method is get or set
# Return Value: SUCCESS/FAILURE

   response_buffer = StringIO()
   curl = pycurl.Curl()
   webpaQuery.parameter_list=[parameter]
   post_data=json.dumps({"parameters":webpaQuery.parameter_list})
   print post_data

   deviceDetails = obj.getDeviceDetails()
   macaddress = deviceDetails["mac"]

   if SAT_REQUIRED == "true":
       SatKey=""
       response_file = SAT_TOKEN_FILE
       print response_file

       if os.path.exists(response_file):
          print "SAT Token file is available"
          with open(response_file,'r') as f:
             data=json.load(f)
          SatKey=str(data["serviceAccessToken"])
       else:
          print "No SAT Token file is available"

   curl.setopt(curl.URL, str(SERVER_URI+"/api/v2/device/mac:"+macaddress+"/config?names="+ parameter['name']))

   if SAT_REQUIRED == "true":
       curl.setopt(curl.HTTPHEADER, ['Content-Type: application/json','Accept: application/json','Authorization:' + AUTHTYPE + ' '+ SatKey])
   else:
       curl.setopt(curl.HTTPHEADER, ['Content-Type: application/json','Accept: application/json','Authorization:' + AUTHTYPE])

   if method == "set":
      curl.setopt(curl.POSTFIELDS, post_data)
      curl.setopt(pycurl.POST, 1)
      curl.setopt(curl.CUSTOMREQUEST, 'PATCH')

   curl.setopt(curl.WRITEFUNCTION, response_buffer.write)
   curl.perform()
   print('Status: %d' %curl.getinfo(curl.RESPONSE_CODE))
   curl.close()
   response_value = response_buffer.getvalue()
   print "WEBPA response received as: ", response_value
   return response_value
########## End of Function ##########

def parseWebpaResponse(response, count, method="get"):
# parseWebpaResponse

# Syntax      : parseWebpaResponse(response, method="get")
# Description : Function to parse the WEBPA response
# Parameters  : response - the response message to be parsed
#             : count  - no: of parameters to be get/set
#             : method - whether the method was get or set
# Return Value: SUCCESS/FAILURE

   responseDict = json.loads(response)
   statusCode = responseDict['statusCode'];

   if statusCode == 200:
        print "GET/SET success for parameter: ",list(responseDict["parameters"])[0]['name']
        msg = list(responseDict["parameters"])[0]['message']
        if method == "get":
           value = " "
           param = webpaQuery.parameter_list[0]['name'].split(",");
           for j in range(len(param)):
               for i in range(count):
                   if list(responseDict["parameters"])[i]['name'] == param[j]:
                       value = value + list(responseDict["parameters"])[i]['value'] + "  "
                   else:
                        i=i+1;
           value = value.strip()
           print "Got parameter value as: ",value
           return ["SUCCESS",value]
        else:
           print "Set operation response is: ", msg
           return ["SUCCESS", msg]
   else:
        if method == "get":
            msg = responseDict["message"]
        elif method == 'set':
            msg = list(responseDict["parameters"])[0]['message']
        else:
            msg = responseDict["message"]
        print "GET/SET operation failed. Response msg for failure: ",msg
        return ["FAILURE", msg]
########## End of Function ##########
def webpaPreRequisite(obj):
# webpaPreRequisite

# Syntax      : webpaPreRequisite()
# Description : Function to do the pre requisite of webpa
# Parameters  : response - the response message to be parsed
# Return Value: SUCCESS/FAILURE

    tdkTestObj = obj.createTestStep('ExecuteCmd');
    expectedresult = "SUCCESS"
    returnStatus = "FAILURE"
    parodusStatus = "FAILURE"
    webpaStatus = "FAILURE"

    cmd= "sh %s/tdk_utility.sh parseConfigFile WEBPA_CHECK_CMD" %TDK_PATH;
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    cmd_webpa = tdkTestObj.getResultDetails().rstrip();
    cmd_webpa = cmd_webpa.split("\\")[0];
    print cmd_webpa

    cmd= "sh %s/tdk_utility.sh parseConfigFile PARODUS_CHECK_CMD" %TDK_PATH;
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    cmd_parodus = tdkTestObj.getResultDetails().rstrip();
    cmd_parodus=cmd_parodus.split("\\")[0];
    print cmd_parodus

    if cmd_parodus and cmd_webpa :
        #Check for the parodus process
        tdkTestObj.addParameter("command",cmd_parodus);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails().rstrip();

        if expectedresult in actualresult and "SUCCESS" in details:
            print "parodus process is up and running"
            parodusStatus = "SUCCESS"
        else:
            #Check for every 2 mins whether the process is up
            retryCount = 0;
            MAX_RETRY = 8;
            while retryCount < MAX_RETRY:
                sleep(120);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails().strip();
                if expectedresult in actualresult and "SUCCESS" in details:
                    print "Parodus process is up and running in device"
                    parodusStatus = "SUCCESS"
                    break;
                else:
                    retryCount = retryCount + 1;
        if parodusStatus == "SUCCESS":
            #Check for webpa process
            tdkTestObj.addParameter("command",cmd_webpa)
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails().strip();
            if expectedresult in actualresult and "SUCCESS" in details:
                print "Webpa process is up and running in device"
                webpaStatus = "SUCCESS"
            else:
                print "Webpa process is not running in device"
                #Check for every 2 mins whether the process is up
                retryCount = 0;
                MAX_RETRY = 8;
                while retryCount < MAX_RETRY:
                    sleep(120);
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails().strip();
                    if expectedresult in actualresult and "SUCCESS" in details:
                        print "Webpa process is up and running in device"
                        webpaStatus = "SUCCESS"
                        break;
                    else:
                        retryCount = retryCount + 1;
            if parodusStatus =="SUCCESS" and webpaStatus == "SUCCESS":
                returnStatus = "SUCCESS"
        else:
            print "Parodus process is not running in device"
    else:
        print "Failed to get the commands for webpa and parodus"
    return tdkTestObj,returnStatus;
########## End of Function ##########




