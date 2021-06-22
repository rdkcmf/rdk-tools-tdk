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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Cobalt_TrickPlay</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to do continuous Pause-Play-FF-Rewind of YouTube for 24 hours.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1460</execution_time>
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
    <test_case_id>RDKV_STABILITY_29</test_case_id>
    <test_objective>The objective of this test is to do continuous Pause-Play-FF-Rewind of YouTube for 24 hours.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string
cobalt_trickplay_duration: int</input_parameters>
    <automation_approch>1. Enable Cobalt plugin
2. Set a video URL 
3. Send keys to press OK
4. In a while loop till test duration send keys corresponding to pause, play, FF and rewind.
5. Check video play back based on each operation
6. Validate CPU load and memory usage
7. Revert plugin.</automation_approch>
    <expected_output>DUT must be stable after each iteration. Video must be paused while sending key for pause and Video must be playing in all other scenarios.(play,FF and rewind)</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_TrickPlay</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_TrickPlay');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
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
    test_time_in_mins = StabilityTestVariables.cobalt_trickplay_duration
    print "Check Pre conditions"
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url value\n"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        cobal_launch_status = launch_cobalt(obj)
        print "\nPre conditions for the test are set successfully"
        time.sleep(30)
        print "\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url)
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","Cobalt.1.deeplink")
        tdkTestObj.addParameter("value",cobalt_test_url)
        tdkTestObj.executeTestCase(expectedResult)
        cobalt_result = tdkTestObj.getResult()
        time.sleep(10)
        if(cobal_launch_status == "SUCCESS" and cobalt_result == expectedResult):
            tdkTestObj.setResultStatus("SUCCESS")
            print "Clicking OK to play video"
            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            result1 = tdkTestObj.getResult()
            time.sleep(50)
            #Skip if Ad is playing by pressing OK
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            result2 = tdkTestObj.getResult()
            time.sleep(60)
            if "SUCCESS" == (result1 and result2):
                result = "SUCCESS"
                result_val = playback_details = ""
                tdkTestObj.setResultStatus("SUCCESS")
                if validation_dict["validation_required"]:
                    if validation_dict["password"] == "None":
                        password = ""
                    else:
                        password = validation_dict["password"]
                    credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                    print "\n check whether video is playing"
                    tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                    tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",credentials)
                    tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                    tdkTestObj.executeTestCase(expectedResult)
                    playback_details = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                else:
                    print "\n Validation is not required, proceeding the test \n"
                if (playback_details == "SUCCESS" or not validation_dict["validation_required"]) and result == "SUCCESS":
                    if validation_dict["validation_required"]:
                        print "\nVideo playback is happening\n"
                        tdkTestObj.setResultStatus("SUCCESS")
                    test_time_in_millisec = test_time_in_mins * 60 * 1000
                    time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                    count = 0
                    completed = True
                    operations = ["pause","play","forward","rewind"]
                    keycodes = [32,32,39,37]
                    error_in_loop = False
                    while int(round(time.time() * 1000)) < time_limit:
                        if error_in_loop:
                            break
                        for index,operation in enumerate(operations):
                            result_dict = {}
                            if operation in ("forward","rewind"):
                                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0},{"keyCode": '+str(keycodes[index])+',"modifiers": [],"delay":1.0},{"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                            else:
                                params = '{"keys":[ {"keyCode": '+str(keycodes[index])+',"modifiers": [],"delay":1.0}]}'
                            if operation == "pause":
                                expected_val = "FAILURE"
                            else:
                                expected_val = "SUCCESS"
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            time.sleep(15)
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                if validation_dict["validation_required"]:
                                    print "\n Check operation :{} happened \n".format(operation)
                                    tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                    tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                    tdkTestObj.addParameter("credentials",credentials)
                                    tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result_val = tdkTestObj.getResultDetails()
                                    operation_result = tdkTestObj.getResult()
                                else:
                                    result_val = expected_val
                                    operation_result = "SUCCESS"
                                if result_val in expected_val and operation_result == "SUCCESS":
                                    print "\n {} is success \n".format(operation)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n{} is not happened \n".format(operation)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    error_in_loop = True
                                    break
                            else:
                                print "\n Error while executing generateKey method\n"
                                tdkTestObj.setResultStatus("FAILURE")
                                error_in_loop = True
                                break
                        else:
                            print "\n ##### Validating CPU load and memory usage #####\n"
			    print "Iteration : ", count+1
            		    tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            		    tdkTestObj.executeTestCase(expectedResult)
            		    status = tdkTestObj.getResult()
            		    result = tdkTestObj.getResultDetails()
            		    if expectedResult in status and result != "ERROR":
            		        tdkTestObj.setResultStatus("SUCCESS")
            		        cpuload = result.split(',')[0]
            		        memory_usage = result.split(',')[1]
                                result_dict["iteration"] = count+1
                                result_dict["cpu_load"] = float(cpuload)
                                result_dict["memory_usage"] = float(memory_usage)
                                result_dict_list.append(result_dict)
                                count += 1
			    else:
				print "\n Error while validating Resource usage"
                		tdkTestObj.setResultStatus("FAILURE")
                		break
                    else:
                        print "\nSuccessfully completed the {} times in {} minutes".format(count,test_time_in_mins)
                    cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                    json.dump(cpu_mem_info_dict,json_file)
                    json_file.close()
                else:
                    print "\n Video is not playing \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to click OK \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to load the cobalt_test_url \n"
            tdkTestObj.setResultStatus("FAILURE")
        print "\n Exiting from Cobalt \n"
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
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
