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
  <name>RDKV_CERT_RVS_Toggle_PowerStates</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to perform continuous toggling of power states as ON and Standby for given number of times</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>360</execution_time>
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
    <test_case_id>RDKV_STABILITY_14</test_case_id>
    <test_objective>The objective of this test is to perform continuous toggling of power states as ON and Standby for given number of times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite> Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>max_power_state_changes:int</input_parameters>
    <automation_approch>1. Check the current power state and current Preferred Standby mode
In a loop given number of times
2. Set the preferred mode as LIGHT SLEEP
3. Check if the preferred mode is LIGHTSLEEP
4. If LIGHTSLEEP, toggle the power state. 
5. Get power state and confirm
6. Check if the CPU and Memory usage is within 90%.
Outside loop
7. Revert everything back</automation_approch>
    <expected_output>The device must be stable after power toggling stress test</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Toggle_PowerStates</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import StabilityTestVariables
from StabilityTestUtility import *
from rdkv_performancelib import *
from web_socket_util import *
import PerformanceTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Toggle_PowerStates');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
max_powerstate_changes = StabilityTestVariables.max_power_state_changes


#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    print "Check Pre conditions"
    event_listener = None
    thunder_port = PerformanceTestVariables.thunder_port
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["org.rdk.System","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = set_status = "SUCCESS"
    plugin_status_needed = {"org.rdk.System":"activated","DeviceInfo":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        set_status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "org.rdk.System.1.register","params": {"event": "onSystemPowerStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(5)
        print "\nPre conditions for the test are set successfully"
        print "\n Get the current power state: \n"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
        tdkTestObj.addParameter("reqValue","powerState")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        current_power_state = initial_power_state = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "Get the current Preferred Standby Mode \n"
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
            tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
            tdkTestObj.addParameter("reqValue","preferredStandbyMode")
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            initial_preferred_standby = preferred_standby = tdkTestObj.getResultDetails()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                for count in range(0,max_powerstate_changes):
                    print "\n********************ITERATION: {} ********************\n".format(count+1)
                    print "\n Set Preferred standby mode as LIGHT_SLEEP \n"
                    params = '{"standbyMode":"LIGHT_SLEEP"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if expectedResult in result:
                        print "\n Setting Preferred Standby Mode is success \n"
                        tdkTestObj.setResultStatus("SUCCESS")
                        print "Get the Preferred Standby Mode \n"
                        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                        tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
                        tdkTestObj.addParameter("reqValue","preferredStandbyMode")
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult();
                        preferred_standby = tdkTestObj.getResultDetails()
                        if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
                            print "\n Preferred standby mode is LIGHT_SLEEP \n"
                            tdkTestObj.setResultStatus("SUCCESS")
                            if current_power_state in ("STANDBY","DEEP_SLEEP","LIGHT_SLEEP"):
                                new_power_state = "ON"
                            else:
                                new_power_state = "STANDBY"
                            params = '{"powerState":"'+new_power_state+'", "standbyReason":"APIUnitTest"}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                            tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                            tdkTestObj.addParameter("value",params);
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult();
                            if expectedResult in result:
                                time.sleep(10)
                                continue_count = 0
                                while True:
                                    if (continue_count > 60):
                                        break
                                    if (len(event_listener.getEventsBuffer())== 0):
                                        continue_count += 1
                                        time.sleep(1)
                                        continue
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    print "\n Triggered event: ",event_log
                                    if (new_power_state == "STANDBY" and ("LIGHT_SLEEP" in event_log or "STANDBY" in event_log)) or (new_power_state == "ON" and "ON" in event_log):
                                        print "onSystemPowerStateChanged event triggered while setting {} power state".format(new_power_state)
                                        break
                                    else:
                                       continue_count = 61
                                if continue_count > 60 :
                                    print "\n onSystemPowerStateChanged event is not triggered for power state: {} \n".format(new_power_state)
                                    current_power_state = new_power_state
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n Verify the Power state \n"
                                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                                tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                                tdkTestObj.addParameter("reqValue","powerState")
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                current_power_state = tdkTestObj.getResultDetails()
                                if expectedResult in result and current_power_state == new_power_state:
                                    print "\n Successfully set power state to : {}\n".format(new_power_state)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    result_dict = {}
                                    #get the cpu load
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
                                else:
                                    print "\n Unable to set the powerstate to : {}, current power state:{}\n".format(new_power_state,current_power_state)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print "\n Error while executing org.rdk.System.1.setPowerState method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Error while setting Preferred Standby Mode to LIGHT_SLEEP \n"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Error while executing org.rdk.System.1.setPreferredStandbyMode method \n"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Successfully completed {} iterations \n".format(max_powerstate_changes)
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
                #Revert preferred standby mode
                if initial_preferred_standby != preferred_standby:
                    print "\n Reverting the Preferred Standby mode \n"
                    params = '{"standbyMode":"'+initial_preferred_standby+'"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if expectedResult in result:
                        print "\n setPreferredStandbyMode is success \n"
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "\n Error while setting PreferredStandbyMode\n"
                        tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing org.rdk.System.1.getPreferredStandbyMode method \n"
                tdkTestObj.setResultStatus("FAILURE")
            #Revert power state
            if current_power_state != initial_power_state:
                print "Reverting the Power state \n"
                print "\n Set power state to {} \n".format(initial_power_state)
                params = '{"powerState":"'+initial_power_state+'", "standbyReason":"APIUnitTest"}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                tdkTestObj.addParameter("value",params);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    print "Reverted the power state to {}\n".format(initial_power_state)
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n Error while reverting the power state to {}\n".format(initial_power_state)
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while executing org.rdk.System.1.getPowerState method \n"
            tdkTestObj.setResultStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(5)
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
