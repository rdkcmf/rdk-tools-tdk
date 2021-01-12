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
  <name>RdkService_Media_Video_PlayPause_STRESS</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>4</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to launch a lightning Video player application via Webkit Browser and perform video play pause operations continuously for given number of times</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_Media_Validation_08</test_case_id>
    <test_objective>Test Script to launch a lightning Video player application via Webkit Browser and perform video play pause operations continuously for given number of times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Player app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning player App URL: string
webinspect_port: string
video_src_url : string
pause_interval_stress:int
play_interval_stress:int
repeat_count_stress:int</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the player app url with the operations play, pause and repeat info.
4. App performs the pause and play operation repeatedly and validates using events
5. If expected events occurs for pause and play in all the repetition, then app gives the validation result as SUCCESS or else FAILURE
6. Update the test script result as SUCCESS/FAILURE based on event validation result from the app and proc check status (if applicable)
7. Revert all values</automation_approch>
    <expected_output>Player pause and play should happen and expected events should occur for all the repetition and if proc validation is applicable, then expected data should be available in proc file </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkservices</test_stub_interface>
    <test_script>RdkService_Media_Video_PlayPause_STRESS</test_script>
    <skipped>No</skipped>
    <release_version>M82</release_version>
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


obj = tdklib.TDKScriptingLibrary("rdkservices","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_Media_Video_PlayPause_STRESS')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = MediaValidationVariables.lightning_video_test_app_url
    videoURL  = MediaValidationVariables.video_src_url
    # Setting VideoPlayer Operations
    setOperation("pause",MediaValidationVariables.pause_interval_stress)
    setOperation("play",MediaValidationVariables.play_interval_stress)
    setOperation("repeat",MediaValidationVariables.repeat_count_stress)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    appArguments = getURLArguments()
    # Getting the complete test app URL
    video_test_url = getTestURL(appURL,appArguments)

    #Example video test url
    #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/tdkmediaplayer/build/index.html?
    #url=<video_url>&operations=pause(5),play(5),repeat(15)&autotest=true

    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_ux_status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nUX:%s\nWebKitBrowser:%s\nCobalt:%s"%(curr_ux_status,curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        set_pre_requisites(obj)
        #Need to revert the values since we are changing plugin status
        revert="YES"
        status,ux_status,webkit_status,cobalt_status = check_pre_requisites(obj)
    #Checking whether device supports proc entry validation. If supported, get
    #device information to access and read the proc file
    validation_dict = getProcValidationParams(obj,"VIDEO_PROC_FILE")
    if status == "SUCCESS" and validation_dict != {}:
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        if current_url != None:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,MediaValidationVariables.webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "Current URL:",current_url
            print "\nSet Lightning video player test app URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",video_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            new_url = tdkTestObj.getResultDetails();
            if new_url in video_test_url:
                tdkTestObj.setResultStatus("SUCCESS");
                print "URL(",new_url,") is set successfully"
                if validation_dict["proc_check"]:
                    proc_file = validation_dict["proc_file"]
                    if validation_dict["ssh_method"] == "directSSH":
                        if validation_dict["password"] == "None":
                            password = ""
                        else:
                            password = validation_dict["password"]
                        credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                    else:
                        #TODO
                        print "selected ssh method is {}".format(validation_dict["ssh_method"])
                        pass
                    print "\nProc entry validation for video player test is enabled\n"
                else:
                    print "\nProc entry validation for video player test is skipped\n"
                test_result = ""
                proc_check_list = []
                while True:
                    if (len(webkit_console_socket.getEventsBuffer())== 0):
                        time.sleep(1)
                        continue
                    console_log = webkit_console_socket.getEventsBuffer().pop(0)
                    dispConsoleLog(console_log)
                    if "Observed Event: play" in console_log and validation_dict["proc_check"]:
                        proc_check_list.append(checkProcEntry(validation_dict["ssh_method"],credentials,proc_file,"started"));
                        time.sleep(1);
                    if "TEST RESULT:" in console_log or "Connection refused" in console_log:
                        test_result = getConsoleMessage(console_log)
                        break;
                webkit_console_socket.disconnect()
                if "SUCCESS" in test_result and "FAILURE" not in proc_check_list:
                    print "Video play is fine"
                    print "[TEST EXECUTION RESULT]: SUCCESS"
                    tdkTestObj.setResultStatus("SUCCESS");
                elif "SUCCESS" in test_result and "FAILURE" not in proc_check_list:
                    print "Decoder proc entry check returns failure.Video not playing fine"
                    print "[TEST EXECUTION RESULT]: FAILURE"
                    tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "Video not playing fine"
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
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_ux_status,curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkservices");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

