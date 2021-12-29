##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Browser_Strike</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the browser score using strike tool</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>6</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_82</test_case_id>
    <test_objective>The objective of this test is to validate the browser score using strike tool</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>strike_tool_url:string
webinspect_port:string</input_parameters>
    <automation_approch>1. Launch WebKitBrowser using RDKShell.
2. Create we websocket connection to the webinspect page of WebKit
3. Set strike tool URL using url method of WebKitBrowser
4. Listen to the socket output and wait for "Score" value to come.
5. Validate the score using threshold value</automation_approch>
    <expected_output>The browser score should be greater than the threshold value</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Browser_Strike</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import BrowserPerformanceVariables
import PerformanceTestVariables
import json
from BrowserPerformanceUtility import *
from web_socket_util import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Browser_Strike')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    browser_test_url = BrowserPerformanceVariables.strike_tool_url
    webinspect_port = PerformanceTestVariables.webinspect_port
    webkit_console_socket = None
    print "\n Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "\n Current values: \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status)
    if status == "FAILURE":
        if "FAILURE" not in (curr_webkit_status,curr_cobalt_status):
            #Need to revert the values since we are changing plugin status
            revert="YES"
            set_status = set_pre_requisites(obj)
            if set_status == "SUCCESS":
                status,webkit_status,cobalt_status = check_pre_requisites(obj)
            else:
                status = "FAILURE"
        else:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully"
        webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
        time.sleep(20)
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","WebKitBrowser.1.url")
        tdkTestObj.executeTestCase(expectedResult)
        current_url = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Current URL:",current_url
            print "\n Set test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","WebKitBrowser.1.url")
            tdkTestObj.addParameter("value",browser_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in  result:
                time.sleep(10)
                print "\n Validate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","WebKitBrowser.1.url")
                tdkTestObj.executeTestCase(expectedResult)
                new_url = tdkTestObj.getResultDetails()
                result = tdkTestObj.getResult()
                if browser_test_url in new_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "URL(",new_url,") is set successfully"
                    time.sleep(10)
                    webkit_console_socket.clearEventsBuffer()
                    #Press enter to start the test
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        continue_count = 0
                        browser_score = 0
                        while True:
                            if continue_count > 180:
                                print "\n Unable to run strike tool \n"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                            if (len(webkit_console_socket.getEventsBuffer())== 0):
                                time.sleep(1)
                                continue_count += 1
                                continue
                            console_log = webkit_console_socket.getEventsBuffer().pop(0)
                            continue_count = 0
                            if '"text":"Score "' in console_log or "Connection refused" in console_log:
                                console_log = json.loads(console_log)
                                browser_score_list = console_log.get('params').get('message').get('parameters')
                                browser_score = [element.get('value') for element in browser_score_list if element.get('type') == 'number'][0]
                                print "\n Score from Strike tool: ",browser_score
                                break;
                        if browser_score:
                            conf_file,result = getConfigFileName(tdkTestObj.realpath)
                            result, strike_threshold_value = getDeviceConfigKeyValue(conf_file,"STRIKE_THRESHOLD_VALUE")
                            if strike_threshold_value != "" :
                                print "\n Threshold value for performance score: ",strike_threshold_value
                                if int(browser_score) > int(strike_threshold_value):
                                    print "\n The browser performance score is high as expected\n"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n The browser performance main score is lower than expected \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print "\n Failed to get the threshold value from config file"
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print "\n Failed to get the browser score"
                else:
                    print "\n Failed to load the URL",new_url
                    tdkTestObj.setResultStatus("FAILURE")
                #Set the URL back to previous
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","WebKitBrowser.1.url")
                tdkTestObj.addParameter("value",current_url)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    print "\n URL is reverted successfully"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n Failed to revert the URL"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "\n Failed to set URL to webkitbrowser"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "\n Failed to get URL in webkitbrowser"
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")

    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = revert_value(curr_webkit_status,curr_cobalt_status,obj)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
