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
  <version>1</version>
  <name>RDKV_CERT_RVS_Cobalt_Video_SearchAndPlay</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_sendKeyCodes</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to continuous video search and play in Cobalt</synopsis>
  <groups_id/>
  <execution_time>4000</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <test_cases>
    <test_case_id>RDKV_STABILITY_33</test_case_id>
    <test_objective>The objective of this test is to continuous video search and play in Cobalt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. In a loop of minimum 1000, Navigate to search page using generateKey method.
3. Search the given keyword and play the same.
4. Validate video playback using proc_entry
5. Validate CPU load and memory usage in that iteration.
6. Navigate to home and repeat above steps
7. Revert the plugin status</automation_approch>
    <expected_output>Video should be played in each search. </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_Video_SearchAndPlay</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_Video_SearchAndPlay');

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
    cobalt_search_name = StabilityTestVariables.cobalt_search_and_play_video_name.lower()
    search_and_play_max_count = StabilityTestVariables.cobalt_search_and_play_max_count
    print "Check Pre conditions"
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    cobalt_launch_status = launch_cobalt(obj)
    if status == "SUCCESS" and validation_dict != {} and cobalt_launch_status == "SUCCESS":
        time.sleep(30)
        for count in range(0,search_and_play_max_count):
            result_dict = {}
            #Go to search page
            print "\n Navigate to search page \n" 
            params = '{"keys":[ {"keyCode": 37,"modifiers": [],"delay":1.0},{"keyCode": 38,"modifiers": [],"delay":1.0},{"keyCode": 13,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in result :
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Search and play video \n"
                tdkTestObj = obj.createTestStep('rdkservice_sendKeyCodes')
                tdkTestObj.addParameter("keyword",cobalt_search_name)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                time.sleep(10)
                if expectedResult in result :
                    tdkTestObj.setResultStatus("SUCCESS")
                    params =  '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0},{"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result1 = tdkTestObj.getResult()
                    time.sleep(50)
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result2 = tdkTestObj.getResult()
                    time.sleep(40)
                    if "SUCCESS" in (result1 and result2):
                        tdkTestObj.setResultStatus("SUCCESS")
                        result = "SUCCESS"
                        result_val = playback_details = ""
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
			    else:
				print "\n Error while validating Resource usage"
                		tdkTestObj.setResultStatus("FAILURE")
                		break
                            params = '{"keys":[ {"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 40,"modifiers": [],"delay":1.0},{"keyCode": 39,"modifiers": [],"delay":1.0},{"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            time.sleep(5)
                            if expectedResult in result :
                                print "\n Navigated to Cobalt home page \n"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Error while navigating to Cobalt home page \n"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Video playback is not happening \n"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Error while sending OK button \n"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Error while searching for video \n"
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "\n Error while navigating to search page \n"
                tdkTestObj.setResultStatus("FAILURE")
                break
        else:
            print "\n Successfully completed {} iterations \n".format(search_and_play_max_count)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
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
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
