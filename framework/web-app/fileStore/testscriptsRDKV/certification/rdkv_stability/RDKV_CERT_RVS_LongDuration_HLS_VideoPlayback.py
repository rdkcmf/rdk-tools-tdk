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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>4</version>
  <name>RDKV_CERT_RVS_LongDuration_HLS_VideoPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the resource usage while playing a video in video player Lightning application for a minimum of 10 hours.</synopsis>
  <groups_id/>
  <execution_time>630</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_43</test_case_id>
    <test_objective>The objective of this test is to validate the resource usage while playing a video in video player Lightning application for a minimum of 10 hours.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch LightningApp webkit instance
2. Set the URL of tdkvideoplayer LightningApp with a live video URL
3. Check whether video playback is started based on application console logs.
4. Validate resource usage in every minute.</automation_approch>
    <expected_output>Video should be start playing and resource usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_LongDuration_HLS_VideoPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from web_socket_util import *
from MediaValidationUtility import *
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_LongDuration_HLS_VideoPlayback');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    status = "SUCCESS"
    print "\n Check Pre conditions"
    appURL    = StabilityTestVariables.lightning_video_test_app_url
    videoURL  = StabilityTestVariables.video_src_url_hls
    videoURL_type = "hls"
    if any(value == "" for value in (appURL,videoURL,videoURL_type)):
        print "\n Please configure the variables in StabilityTestVariables file"
        status = "FAILURE"
    else:
        # Setting VideoPlayer Operations
        test_duration_in_seconds = 36000
        setOperation("close",test_duration_in_seconds)
        operations = getOperations()
        # Setting VideoPlayer test app URL arguments
        setURLArgument("url",videoURL)
        setURLArgument("operations",operations)
        setURLArgument("autotest","true")
        setURLArgument("type",videoURL_type)
        appArguments = getURLArguments()
        # Getting the complete test app URL
        video_test_url = getTestURL(appURL,appArguments)
    webkit_console_socket = None
    started = False
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    webkit_instance = StabilityTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
    plugins_list = ["Cobalt","DeviceInfo",webkit_instance]
    if webkit_instance in "WebKitBrowser":
        webinspect_port = StabilityTestVariables.webinspect_port
    else:
        webinspect_port = StabilityTestVariables.lightning_app_webinspect_port
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
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
                tdkTestObj.setResultStatus("SUCCESS")
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult();
                if new_url in video_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "\n URL(",new_url,") is set successfully \n"
                    continue_count = 0
                    count = 0
                    while True:
                        result_dict = {}
                        if continue_count > 180:
                            print "\n Not able to play the video"
                            print "\n Current webkit console logs: ",webkit_console_socket.getEventsBuffer()
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            print "\n Waiting for video plaback"
                            time.sleep(1)
                            continue_count += 1
                            continue
                        else:
                            if [True for element in webkit_console_socket.getEventsBuffer() if "VIDEO STARTED PLAYING" in str(element)]:
                                started = True
                                print "\n Video playback is started"
                                webkit_console_socket.clearEventsBuffer()
                                continue_count = 0
                            elif [True for element in webkit_console_socket.getEventsBuffer() if "TEST RESULT:" in str(element)]:
                                if [True for element in webkit_console_socket.getEventsBuffer() if "TEST RESULT: SUCCESS" in str(element)] :
                                    print "\n Successfully completed video playback"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Error occurred while playing Video"
                                    tdkTestObj.setResultStatus("FAILURE")
                                break
                            elif [True for element in webkit_console_socket.getEventsBuffer() if "Connection refused" in str(element)]:
                                print "\n Error occurred while playing video"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                            if started:
                                continue_count = 0
                                if not [True for element in webkit_console_socket.getEventsBuffer() if "TEST RESULT:" in str(element)]:
                                    webkit_console_socket.clearEventsBuffer()
                                    #Validate resource usage
                                    print "\n Validate Resource usage for iteration: {}".format(count+1)
                                    tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                                    tdkTestObj.executeTestCase(expectedResult)
                                    resource_usage = tdkTestObj.getResultDetails()
                                    result = tdkTestObj.getResult()
                                    if expectedResult in result and resource_usage != "ERROR":
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        cpuload = resource_usage.split(',')[0]
                                        memory_usage = resource_usage.split(',')[1]
                                        result_dict["iteration"] = count+1
                                        result_dict["cpu_load"] = float(cpuload)
                                        result_dict["memory_usage"] = float(memory_usage)
                                        result_dict_list.append(result_dict)
                                        time.sleep(30)
                                        count += 1
                                    else:
                                        print "\n Error while validating Resource usage"
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    print "\n Video player is stopped"
                                    continue
                            else:
                                print "\n Video playback is not happening"
                                time.sleep(20)
                                continue_count += 5
                    webkit_console_socket.disconnect()
                    time.sleep(5)
                    cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                    json.dump(cpu_mem_info_dict,json_file)
                    json_file.close()
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
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "\n Failed to load module"
