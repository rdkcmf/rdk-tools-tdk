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
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RdkService_Media_Animation_Average_FPS</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>4</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to launch a lightning Animation application and check whether the average FPS calculated for 60 sec duration value is as expected</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <test_case_id>RDKV_Media_Validation_04</test_case_id>
    <test_objective>Test Script to launch a lightning Animation application and check whether the average FPS calculated for 60 sec duration value is as expected</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Animation app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning Animation App URL: string
webinspect_port: string
thunder_port :string
expected_fps:int
threshold:int</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the Animation app url with the operation stop after 60 sec
4. App performs animation for 60 sec and stops after that.
5. If expected events occurs for stop, then app gives the validation result as SUCCESS or else FAILURE. It also gives average FPS value
6. Get the event validation result and average FPS value from the app and check whether FPS obtained is greater than or equal to expected fps value (i.e) expected_fps - threshold.
7. Revert all values</automation_approch>
    <expected_output>Animation should happen for 60 sec and average FPS should be grater than or equal to expected fps value.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RdkService_Media_Animation_Average_FPS</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
from web_socket_util import *
import MediaValidationVariables
from MediaValidationUtility import *
import MediaValidationUtility


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_Media_Animation_Average_FPS')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = MediaValidationVariables.lightning_animation_test_app_url
    # Setting Animation Operations
    setOperation("stop","60")
    operations = getOperations()
    # Setting Animation test app URL arguments
    setURLArgument("ip",ip)
    setURLArgument("port",MediaValidationVariables.thunder_port)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    appArguments = getURLArguments()
    # Getting the complete test app URL
    animation_test_url = getTestURL(appURL,appArguments)

    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_ux_status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        set_pre_requisites(obj)
        #Need to revert the values since we are changing plugin status
        revert="YES"
        status,ux_status,webkit_status,cobalt_status = check_pre_requisites(obj)
    #Reading the FPS and threshold for FPS from the device config file
    config_status = "SUCCESS"
    conf_file,result = getConfigFileName(obj.realpath)
    result1, expected_fps  = getDeviceConfigKeyValue(conf_file,"EXPECTED_FPS")
    result2, threshold     = getDeviceConfigKeyValue(conf_file,"FPS_THRESHOLD")
    if "SUCCESS" in result1 and "SUCCESS" in result2:
        if expected_fps == "" and threshold == "":
            config_status = "FAILURE"
            print "Please set expected_fps and threshold values in device config file"
    else:
        config_status = "FAILURE"
        print "Failed to get the FPS value & threshold value from device config file"
    if status == "SUCCESS" and config_status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        current_url = tdkTestObj.getResultDetails();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,MediaValidationVariables.webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "Current URL:",current_url
            print "\nSet Lightning Animation test app URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",animation_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                result= tdkTestObj.getResult()
                new_url = tdkTestObj.getResultDetails();
                if new_url in animation_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    test_result = ""
                    average_fps = 0
                    minfps = float(int(expected_fps) - int(threshold))
                    while True:
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            time.sleep(1)
                            continue
                        console_log = webkit_console_socket.getEventsBuffer().pop(0)
                        dispConsoleLog(console_log)
                        if "Average FPS" in console_log:
                            average_fps = getConsoleMessage(console_log).split("[DiagnosticInfo]:")[1].split(":")[1]
                        if "TEST RESULT:" in console_log or "Connection refused" in console_log:
                            test_result = getConsoleMessage(console_log)
                            break;
                    webkit_console_socket.disconnect()
                    if "SUCCESS" in test_result:
                        print "Obtained Average FPS =",average_fps
                        if "NaN" in average_fps:
                            print "Failed to get the average FPS Value"
                            print "[TEST EXECUTION RESULT]: FAILURE"
                            tdkTestObj.setResultStatus("FAILURE");
                        elif float(average_fps) >= minfps:
                            print "Average FPS is >= %f" %(minfps)
                            print "Lightning Animation App is rendered for around 60 sec and average FPS is as expected"
                            print "[TEST EXECUTION RESULT]: SUCCESS"
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            print "Average FPS is < %f" %(minfps)
                            print "Lightning Animation App is rendered for around 60 sec and average FPS is not as expected"
                            print "[TEST EXECUTION RESULT]: FAILURE"
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                    #Set the URL back to previous
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                    tdkTestObj.addParameter("value",current_url);
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if result == "SUCCESS":
                        print "URL is reverted successfully"
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print "Failed to revert the URL"
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "Failed to load the URL %s" %(new_url)
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set the URL"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_ux_status,curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

