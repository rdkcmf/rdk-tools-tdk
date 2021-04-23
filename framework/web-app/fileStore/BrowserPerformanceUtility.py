##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
#########################################################################
import time

expectedResult ="SUCCESS"
#METHODS
#---------------------------------------------------------------
#CHECK FOR THE PRE_REQUISITES
#---------------------------------------------------------------
def check_pre_requisites(obj):
    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
    tdkTestObj.addParameter("plugin","WebKitBrowser");
    tdkTestObj.executeTestCase(expectedResult);
    webkit_result = tdkTestObj.getResult();
    webkit_status = tdkTestObj.getResultDetails();

    tdkTestObj.addParameter("plugin","Cobalt");
    tdkTestObj.executeTestCase(expectedResult);
    cobalt_result = tdkTestObj.getResult()
    cobalt_status = tdkTestObj.getResultDetails();

    expected_status_list =["deactivated","suspended","None"]
    expected_webkit_status = "resumed"
    status_list = ["activated","deactivated","resumed","suspended","None"]
    #Check if all the status are valid or not.
    if "FAILURE" not in (webkit_result,cobalt_result):
        if all(status in status_list for status in [webkit_status,cobalt_status]):
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            tdkTestObj.setResultStatus("FAILURE");

        if cobalt_status in expected_status_list and webkit_status == "resumed":
            return ("SUCCESS",webkit_status,cobalt_status)
        else:
            return ("FAILURE",webkit_status,cobalt_status)
    else:
        return ("FAILURE",webkit_result,cobalt_result)
#---------------------------------------------------------------------
#SET PRE_REQUISITES
#---------------------------------------------------------------------
def set_pre_requisites(obj):
    print "\nDeactivating Cobalt"
    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
    tdkTestObj.addParameter("plugin","Cobalt");
    tdkTestObj.addParameter("status","deactivate");
    tdkTestObj.executeTestCase(expectedResult);
    result1 = tdkTestObj.getResult();
    time.sleep(5)

    print "\nActivate and resume WebKitBrowser"
    params = '{"callsign":"WebKitBrowser", "type":"", "uri":""}'
    tdkTestObj = obj.createTestStep('rdkservice_setValue')
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase(expectedResult);
    result2 = tdkTestObj.getResult();
    time.sleep(5)

    if all(result == "SUCCESS" for result in [result1,result2]):
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"
#---------------------------------------------------------------------
#REVERT THE VALUES
#---------------------------------------------------------------------
def revert_value(curr_webkit_status,curr_cobalt_status,obj):
    webkit_status = "SUCCESS" if curr_webkit_status == "None" else 'FAILURE';
    if curr_webkit_status != "deactivated" and curr_webkit_status != "None":
        print "WebKit was activated"
    elif curr_webkit_status == "deactivated":
        print "WebKit was deactivated"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","WebKitBrowser");
        tdkTestObj.addParameter("status","deactivate");
        tdkTestObj.executeTestCase(expectedResult);
        webkit_status = tdkTestObj.getResult();

    print "\nRevert Cobalt status"
    cobalt_status = "SUCCESS" if curr_cobalt_status == "None" else "FAILURE";
    if curr_cobalt_status != "deactivated" and curr_cobalt_status != "None":
        print "Cobalt was activated"
        params = '{"callsign":"Cobalt", "type":"", "uri":""}'
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
        tdkTestObj.addParameter("value",params)
        tdkTestObj.executeTestCase(expectedResult);
        cobalt_status = tdkTestObj.getResult();
    elif curr_cobalt_status == "deactivated":
        print "Cobalt was deactivated"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","Cobalt");
        tdkTestObj.addParameter("status","deactivate");
        tdkTestObj.executeTestCase(expectedResult);
        cobalt_status = tdkTestObj.getResult();
    if all(status == "SUCCESS" for status in [webkit_status,cobalt_status]):
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"
