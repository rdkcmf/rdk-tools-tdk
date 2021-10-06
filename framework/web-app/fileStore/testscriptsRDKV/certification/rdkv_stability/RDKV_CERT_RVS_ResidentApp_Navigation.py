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
  <name>RDKV_CERT_RVS_ResidentApp_Navigation</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do navigations in ResidentApp UI in every 5 minutes and validate resource usage for a minimum of 10 hours</synopsis>
  <groups_id/>
  <execution_time>610</execution_time>
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
    <test_case_id>RDKV_STABILITY_44</test_case_id>
    <test_objective>The objective of this test is to do navigations in ResidentApp UI in every 5 minutes and validate resource usage for a minimum of 10 hours</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Check ResidenApp plugin is in front
2. In a while loop for a duration of 10 hours, Ddokey navigations using generateKey method of RDKShell
3. Validate resource usage after each set of key navigations
</automation_approch>
    <expected_output>Device should be stable after each set of key navigations and resource usage must be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_ResidentApp_Navigation</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import ast
from rdkv_performancelib import *
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_ResidentApp_Navigation')

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
test_interval = 60

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    status = "SUCCESS"
    navigation_key_sequence = StabilityTestVariables.navigation_key_sequence
    navigation_key_dictionary = {"ArrowLeft":37,"ArrowUp":38,"ArrowRight":39,"ArrowDown":40,"OK":13}
    plugins_list = ["ResidentApp","DeviceInfo"]
    curr_plugin_status = get_plugins_status(obj,plugins_list)
    resident_app = "ResidentApp"
    is_front = False
    device_info = "DeviceInfo"
    device_info_status = curr_plugin_status[device_info]
    if device_info_status != "activated":
        set_status = rdkservice_setPluginStatus(device_info,"activate")
        time.sleep(10)
        device_info_status = rdkservice_getPluginStatus(device_info)
    if device_info_status in "activated" and curr_plugin_status[resident_app] in ("activated","resumed"):
        #Check zorder to check ResidentApp is in the front
        print "\n Get the zorder"
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
        tdkTestObj.executeTestCase(expectedResult)
        zorder = tdkTestObj.getResultDetails()
        zorder_status = tdkTestObj.getResult()
        if expectedResult in zorder_status :
            tdkTestObj.setResultStatus("SUCCESS")
            zorder = ast.literal_eval(zorder)["clients"]
            if resident_app.lower() in zorder and zorder[0].lower() == resident_app.lower():
                is_front = True
                print "\n ResidentApp is in front"
            elif resident_app.lower() in zorder and zorder[0].lower() != resident_app.lower():
                param_val = '{"client": "'+resident_app+'"}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
                tdkTestObj.addParameter("value",param_val)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check zorder to check ResidentApp is in the front
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                    tdkTestObj.executeTestCase(expectedResult)
                    zorder = tdkTestObj.getResultDetails()
                    zorder_status = tdkTestObj.getResult()
                    if expectedResult in zorder_status :
                        zorder = ast.literal_eval(zorder)["clients"]
                        if zorder[0].lower() == resident_app.lower():
                            print "\n Successfully moved ResidentApp to front"
                            is_front = True
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Unable to move ResidentApp to front"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while getting the zorder"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing moveToFront method"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n ResidentApp is not present in zorder"
                tdkTestObj.setResultStatus("FAILURE")
            if is_front:
                test_time_in_mins = int(StabilityTestVariables.navigation_test_duration)
                test_time_in_millisec = test_time_in_mins * 60 * 1000
                time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                iteration = 0
                error_in_loop = False
                while int(round(time.time() * 1000)) < time_limit:
                    print "\n########## Iteration :{} ##########\n".format(iteration+1)
                    result_dict = {}
                    #Navigate in ResidentApp UI
                    for key in navigation_key_sequence:
                        params = '{"keys":[ {"keyCode": '+str(navigation_key_dictionary[key])+',"modifiers": [],"delay":1.0}]}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            print "\n Pressed {} key".format(key)
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while pressing {} key".format(key)
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    else:
                        print "\n Successfully completed navigations in ResidentApp UI"
                        print "\n ##### Validating CPU load and memory usage #####\n"
                        time.sleep(test_interval)
                        print "Iteration : ", iteration+1
                        tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        result = tdkTestObj.getResultDetails()
                        if expectedResult in status and result != "ERROR":
                            tdkTestObj.setResultStatus("SUCCESS")
                            cpuload = result.split(',')[0]
                            memory_usage = result.split(',')[1]
                            result_dict["iteration"] = iteration+1
                            result_dict["cpu_load"] = float(cpuload)
                            result_dict["memory_usage"] = float(memory_usage)
                            result_dict_list.append(result_dict)
                            iteration += 1
                        else:
                            print "\n Error while validating Resource usage"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    if error_in_loop:
                        print "\n Stopping the test"
                        break
                else:
                    print "\n Successfully completed {} iterations in {} minutes".format(iteration,test_time_in_mins)
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
            else:
                print "\n Unable to move ResidentApp to front"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while getting zorder"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
