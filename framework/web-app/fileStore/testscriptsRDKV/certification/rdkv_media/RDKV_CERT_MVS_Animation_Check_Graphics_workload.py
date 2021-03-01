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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_MVS_Animation_Check_Graphics_workload</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to perform animation of multiple objects from count of 1,10,20,50,100,250,500,1000 one by one for the provided duration using lightning application and check how many objects can be rendered by the device with expected FPS value.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <test_case_id>RDKV_Media_Validation_11</test_case_id>
    <test_objective>Test Script to perform animation of multiple objects from count of 1,10,20,50,100,250,500,1000 one by one for the provided duration using lightning application and check how many objects can be rendered by the device with expected FPS value.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Multi Animation app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning Multi Animation App URL: string
webinspect_port: string
thunder_port :string
expected_fps:int
threshold:int</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the Multi Animation app url with the arguments like fps,threshold,ip,port,duration and testing methods
4. App performs animation of multiple objects from count of 1,10,20,50,100,250,500,1000 one by one for the provided duration.
5. App starts with animation of single object for provided duration and collect the fps for every second, then find the average of collected fps.
6. If the average FPS obtained is greater than or equal to expected fps value (i.e) expected_fps - threshold, then app increases number of objects to 10. Again average fps is calculated and checked, then app decides to proceed for further more number of objects or not.
7. Average fps for single object animation should be as expected. If this condition is satisfied test result is set as SUCCESS or else FAILURE.
8. Test script finally gives the number of objects the device can animate with expected FPS
9. Revert all values</automation_approch>
    <expected_output>Device should be able to atleast animate single object with expected FPS and number of objects the device can animate with expected FPS should be obtained</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RdkService_Media_Animation_Check_Device_Capability</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from BrowserPerformanceUtility import *
from rdkv_performancelib import *
from web_socket_util import *
import MediaValidationVariables
from MediaValidationUtility import *

obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Animation_Check_Graphics_workload')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = MediaValidationVariables.lightning_multianimation_test_app_url
    # Setting Animation test app URL arguments
    setURLArgument("ip",ip)
    setURLArgument("port",MediaValidationVariables.thunder_port)
    setURLArgument("duration",MediaValidationVariables.animation_duration)
    setURLArgument("testtype","generic")
    setURLArgument("autotest","true")

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
    #Check residentApp status and deactivate if its activated
    check_status,resapp_status,resapp_revert,resapp_url = checkAndDeactivateResidentApp(obj)
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
    if status == "SUCCESS" and config_status == "SUCCESS" and check_status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,MediaValidationVariables.webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "Current URL:",current_url
            setURLArgument("fps",expected_fps)
            setURLArgument("threshold",threshold)
            appArguments = getURLArguments()
            # Getting the complete test app URL
            animation_test_url = getTestURL(appURL,appArguments)
            print "\nSet Multiple objects Animation test URL"
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
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if new_url in animation_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    continue_count = 0
                    avgerage_fps_list = []
                    minfps = float(int(expected_fps) - int(threshold))
                    while True:
                        if continue_count > 180:
                            print "\nApp not proceeding for 3 mins. Exiting..."
                            break
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            time.sleep(1)
                            continue_count += 1
                            continue
                        else:
                            continue_count = 0
                        console_log = webkit_console_socket.getEventsBuffer().pop(0)
                        if "[DiagnosticInfo]: CPU Load" not in console_log:
                            dispConsoleLog(console_log)
                        if "[DiagnosticInfo]: No.of Animated Objects" in console_log:
                            log_message = getConsoleMessage(console_log)
                            avgerage_fps_list.append(log_message)
                        if "TEST COMPLETED" in console_log or "TEST STOPPED" in console_log:
                            break;
                    webkit_console_socket.disconnect()
                    avg_fps_single_object = str(avgerage_fps_list[0]).split(",")[1].split(":")[1]
                    if "NaN" in avg_fps_single_object:
                        print "Failed to get the average FPS Value"
                        print "[TEST EXECUTION RESULT]: FAILURE"
                        tdkTestObj.setResultStatus("FAILURE");
                    elif float(avg_fps_single_object) >= minfps:
                        print "Average FPS (for single object) >= %f" %(minfps)
                        print "\nBelow are the no.of objects the device can animate with the expected FPS:"
                        for info in avgerage_fps_list:
                            if float(str(info).split(",")[1].split(":")[1]) >= minfps:
                                print info
                        print "\n[TEST EXECUTION RESULT]: SUCCESS"
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print "Average FPS (for single object) < %f" %(minfps)
                        print "Average FPS for single object animation is not as expected"
                        print "[TEST EXECUTION RESULT]: FAILURE"
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
    if resapp_revert=="YES":
        setURLAndActivateResidentApp(obj,resapp_url)
        time.sleep(10)
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

