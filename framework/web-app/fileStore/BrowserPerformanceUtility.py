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

    tdkTestObj.addParameter("plugin","UX");
    tdkTestObj.executeTestCase(expectedResult);
    ux_result = tdkTestObj.getResult()
    ux_status = tdkTestObj.getResultDetails();

    tdkTestObj.addParameter("plugin","Cobalt");
    tdkTestObj.executeTestCase(expectedResult);
    cobalt_result = tdkTestObj.getResult()
    cobalt_status = tdkTestObj.getResultDetails();

    expected_status_list =["deactivated","suspended","None"]
    expected_webkit_status = "resumed"
    status_list = ["activated","deactivated","resumed","suspended","None"]
    #Check if all the status are valid or not.
    if "FAILURE" not in (webkit_result,ux_result,cobalt_result):
        if all(status in status_list for status in [webkit_status,ux_status,cobalt_status]):
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            tdkTestObj.setResultStatus("FAILURE");

        if ux_status in expected_status_list and cobalt_status in expected_status_list and webkit_status == "resumed":
            return ("SUCCESS",ux_status,webkit_status,cobalt_status)
        else:
            return ("FAILURE",ux_status,webkit_status,cobalt_status)
    else:
        return ("FAILURE",ux_result,webkit_result,cobalt_result)
#---------------------------------------------------------------------
#SET PRE_REQUISITES
#---------------------------------------------------------------------
def set_pre_requisites(obj):
    print "\nDeactivating UX and Cobalt"
    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
    tdkTestObj.addParameter("plugin","UX");
    tdkTestObj.addParameter("status","deactivate");
    tdkTestObj.executeTestCase(expectedResult);
    result1 = tdkTestObj.getResult();

    time.sleep(5)
    tdkTestObj.addParameter("plugin","Cobalt");
    tdkTestObj.addParameter("status","deactivate");
    tdkTestObj.executeTestCase(expectedResult);
    result2 = tdkTestObj.getResult();
    time.sleep(5)

    print "\nActivate and resume WebKitBrowser"
    tdkTestObj.addParameter("plugin","WebKitBrowser");
    tdkTestObj.addParameter("status","activate");
    tdkTestObj.executeTestCase(expectedResult);
    result3 = tdkTestObj.getResult();
    time.sleep(5)

    tdkTestObj = obj.createTestStep('rdkservice_setValue')
    tdkTestObj.addParameter("method","WebKitBrowser.1.state");
    tdkTestObj.addParameter("value","resumed");
    tdkTestObj.executeTestCase(expectedResult);
    result4 = tdkTestObj.getResult();
    if all(result == "SUCCESS" for result in [result1,result2,result3,result4]):
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"
#---------------------------------------------------------------------
#REVERT THE VALUES
#---------------------------------------------------------------------
def revert_value(curr_ux_status,curr_webkit_status,curr_cobalt_status,obj):
    ux_status = "SUCCESS" if curr_ux_status == "None" else 'FAILURE';
    print "\nRevert UX Status"
    if curr_ux_status != "deactivated" and curr_ux_status != "None":
        print "UX was activated"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","UX");
        tdkTestObj.addParameter("status","activate");
        tdkTestObj.executeTestCase(expectedResult);
        ux_status = tdkTestObj.getResult();
        if ux_status == "SUCCESS":
            if curr_ux_status == "resumed":
                print "UX was in resumed state"
                tdkTestObj = obj.createTestStep('rdkservice_setPluginState');
                tdkTestObj.addParameter("plugin","UX");
                tdkTestObj.addParameter("state","resumed");
                tdkTestObj.executeTestCase(expectedResult);
                ux_status = tdkTestObj.getResult();
    elif curr_ux_status == "deactivated":
        print "UX was disabled"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","UX");
        tdkTestObj.addParameter("status","deactivate");
        tdkTestObj.executeTestCase(expectedResult);
        ux_status = tdkTestObj.getResult();

    print "\nRevert WebKitBrowser status"
    webkit_status = "SUCCESS" if curr_webkit_status == "None" else 'FAILURE';
    if curr_webkit_status != "deactivated" and curr_webkit_status != "None":
        print "WebKit was activated"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","WebKitBrowser");
        tdkTestObj.addParameter("status","activate");
        tdkTestObj.executeTestCase(expectedResult);
        webkit_status = tdkTestObj.getResult();
        if webkit_status == "SUCCESS":
            if curr_webkit_status == "resumed":
                print "WebKit was in resumed state"
                tdkTestObj = obj.createTestStep('rdkservice_setPluginState');
                tdkTestObj.addParameter("plugin","WebKitBrowser");
                tdkTestObj.addParameter("state","resumed");
                tdkTestObj.executeTestCase(expectedResult);
                webkit_status = tdkTestObj.getResult();
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
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","Cobalt");
        tdkTestObj.addParameter("status","activate");
        tdkTestObj.executeTestCase(expectedResult);
        cobalt_status = tdkTestObj.getResult();
        if cobalt_status  == "SUCCESS":
            if curr_cobalt_status == "resumed":
                print "Cobalt was in resumed state"
                tdkTestObj = obj.createTestStep('rdkservice_setPluginState');
                tdkTestObj.addParameter("plugin","Cobalt");
                tdkTestObj.addParameter("state","resumed");
                tdkTestObj.executeTestCase(expectedResult);
                cobalt_status = tdkTestObj.getResult();
    elif curr_cobalt_status == "deactivated":
        print "Cobalt was deactivated"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","Cobalt");
        tdkTestObj.addParameter("status","deactivate");
        tdkTestObj.executeTestCase(expectedResult);
        cobalt_status = tdkTestObj.getResult();
    if all(status == "SUCCESS" for status in [ux_status,webkit_status,cobalt_status]):
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"
