##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>2</version>
  <name>RDKV_CERT_PVS_Apps_ResourceUsage_Video_4K_HLS</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the CPU load and Memory usage while playing an 4k hls video</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_126</test_case_id>
    <test_objective>The objective of this test is to get the CPU and Memory usage while playing an 4k hls video</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.
</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable DeviceInfo and WebKitBrowser/LightningApp/HtmlApp plugin based on configuration.
2. Set the application URL.
3. Get the cpu load and memory usage after playing the 4k hls video
4. Revert the status of plugins</automation_approch>
    <expected_output>CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_ResourceUsage_Video_4K_HLS</test_script>
    <skipped>No</skipped>
    <release_version>M103</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from web_socket_util import *
import PerformanceTestVariables
from MediaValidationUtility import *
from StabilityTestUtility import *
from rdkv_performancelib import *


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_ResourceUsage_Video_4K_HLS');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = PerformanceTestVariables.lightning_video_test_app_url
    videoURL  = MediaValidationVariables.video_src_url_4k_hls
    videoURL_type = "hls"
    # Setting VideoPlayer Operations
    setOperation("close",5)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    setURLArgument("type",videoURL_type)
    appArguments = getURLArguments()
    # Getting the complete test app URL
    video_test_url = getTestURL(appURL,appArguments)

    print "\n Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    webkit_instance = PerformanceTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
    plugins_list = ["Cobalt","DeviceInfo",webkit_instance]
    if webkit_instance in "WebKitBrowser":
        webinspect_port = PerformanceTestVariables.webinspect_port
    elif webkit_instance in "LightningApp":
        webinspect_port = PerformanceTestVariables.lightning_app_webinspect_port
    else:
        webinspect_port = PerformanceTestVariables.html_app_webinspect_port
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    status = "SUCCESS"
    plugin_status_needed = {webkit_instance:"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting plugin status"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        set_status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in {}".format(webkit_instance)
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "\nCurrent URL:",current_url
            print "\nSet Lightning Application URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",video_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult();
                if new_url in video_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "\n URL(",new_url,") is set successfully \n"
                    continue_count = 0
                    test_result = ""
                    while True:
                        if continue_count > 60:
                            print "\n Application is not playing the content"
                            break
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            time.sleep(1)
                            continue_count += 1
                            continue
                        console_log = webkit_console_socket.getEventsBuffer().pop(0)
                        dispConsoleLog(console_log)
                        if "VIDEO STARTED PLAYING" in console_log:
                            print "\n Video playback is started \n "
                            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                            tdkTestObj.executeTestCase(expectedResult)
                            resource_usage = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if expectedResult in result and resource_usage != "ERROR":
                                print "\n Successfully validated Resource usage"
                                tdkTestObj.setResultStatus("SUCCESS")
                                break;
                            else:
                                print "\n Error while validating Resource usage"
                                tdkTestObj.setResultStatus("FAILURE")
                                break;
                        elif "Connection refused" in console_log:
                            print "\n Error occurred while playing Video"
                            tdkTestObj.setResultStatus("FAILURE");
                            break;
                    webkit_console_socket.disconnect()
                    time.sleep(5)
                    #Set the URL back to previous
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method",set_method);
                    tdkTestObj.addParameter("value",current_url);
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if result == "SUCCESS":
                        print "\n URL is reverted successfully \n"
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print "\n Failed to revert the URL"
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "\n Failed to load the URL,new URL: %s" %(new_url)
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "\n Failed to set the URL"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "\n Unable to get the current URL"
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "\n Failed to load module"
