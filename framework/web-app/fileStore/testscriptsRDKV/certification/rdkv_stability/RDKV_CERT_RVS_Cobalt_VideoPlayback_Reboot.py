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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Cobalt_VideoPlayback_Reboot</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateProcEntry</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to calculate the resource usage of the device after rebooting, launching Cobalt and initiating video playback multiple times</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>540</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_62</test_case_id>
    <test_objective>The objective of this test is to calculate the resource usage of the device after rebooting, launching Cobalt and initiating video playback multiple times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Number of times the reboot should happen
2. The URL of the video to be played
3. Maximum allowed CPU load
4. Maximum allowed Memory usage</input_parameters>
    <automation_approch>1. As a pre requisite, disable all the other plugins and enable Cobalt only.
2. Set the URL of video to be played.
3. Validate if the video is playing using proc entries
4. Validate CPU load
5. Validate memory usage
6. Reboot the device</automation_approch>
    <expected_output>The resource usage calculated after multiple reboots should be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_VideoPlayback_Reboot</test_script>
    <skipped>No</skipped>
    <release_version>M108</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import StabilityTestVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_VideoPlayback_Reboot');

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
    cobalt_test_url = StabilityTestVariables.cobalt_test_url;
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","DeviceInfo":"activated","Cobalt":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} :
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
        reboot_times = int(StabilityTestVariables.deviceReboot_times)
        iteration = 1
        completed = True
        rebootwaitTime = 160
        while iteration <= reboot_times:
            print "\n Rebooting the device. Iteration number:{}".format(iteration)
            tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
            tdkTestObj.addParameter("waitTime",rebootwaitTime)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Rebooted device successfully and launching the Cobalt\n"
                cobalt_launch_status = launch_cobalt(obj)
                print "\n Set the URL : {} using Cobalt deeplink method".format(cobalt_test_url)
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                tdkTestObj.addParameter("value",cobalt_test_url)
                tdkTestObj.executeTestCase(expectedResult)
                cobalt_result = tdkTestObj.getResult()
                time.sleep(10)
                if(cobalt_result in expectedResult):
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "Clicking OK to play video"
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result1 = tdkTestObj.getResult()
                    time.sleep(50)
                    #Clicking OK to skip Ad
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result2 = tdkTestObj.getResult()
                    time.sleep(60)
                    if "SUCCESS" == (result1 and result2):
                        result_val = "SUCCESS"
                        if validation_dict["validation_required"]:
                            tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                            tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",credentials)
                            tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                            if result_val == "SUCCESS" :
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\nVideo playback is happening\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print "Video playback is not happening"
                        if result_val == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\n Validate Resource Usage"
                            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                            tdkTestObj.executeTestCase(expectedResult)
                            resource_usage = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if expectedResult in result and resource_usage != "ERROR":
                                print "\n Successfully validated Resource usage"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Error while validating Resource usage"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                            iteration +=1
                    else:
                        print "\n Error while playing the video"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Unable to launch Cobalt"
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "\n Error while rebooting the device"
                tdkTestObj.setResultStatus("FAILURE")
                break
        print "\n Exit from Cobalt \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"