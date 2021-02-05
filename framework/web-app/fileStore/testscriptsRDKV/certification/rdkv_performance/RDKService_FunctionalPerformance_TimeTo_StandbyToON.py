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
  <name>RDKService_FunctionalPerformance_TimeTo_StandbyToON</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to 	get the time taken for the DUT to change power state to ON from STANDBY.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_24</test_case_id>
    <test_objective>The objective of this test is to 	get the time taken for the DUT to change power state to ON from STANDBY.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Time in Test Manager should be in sync with UTC time
2. wpeframework should be running in DUT.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Threshold value</input_parameters>
    <automation_approch>1. As a prerequisite enable System plugin
2. Get the current power state and if it is not ON turn it to ON.
3. Get the preferred standby mode and if it is not LIGHT_SLEEP set it to LIGHT_SLEEP.
4. Set the power state to STANDBY
5. Set the power state to ON after storing the current system time
6. Get the event logs from wpeframework log and parse the time stamp 
7. Calculate the result by finding the difference between system time stored and time stamp of event
8. Revert values</automation_approch>
    <expected_output>Device's power state should be changed.
The time should be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKService_FunctionalPerformance_TimeTo_StandbyToON</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
from datetime import datetime
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKService_FunctionalPerformance_TimeTo_StandbyToON');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["org.rdk.System"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"org.rdk.System":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict == plugin_status_needed:
            status = "SUCCESS"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    result = tdkTestObj.getResult()
    revert_power_state = False
    if status == "SUCCESS" and ssh_param_dict != {} and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print "\nPre conditions for the test are set successfully"
        print "\n Get the current power state: \n"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
        tdkTestObj.addParameter("reqValue","powerState")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        current_power_state = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            if current_power_state != "ON":
                revert_power_state = True
            print "\n Current power state : \n",current_power_state
            print "\n Set Preferred standby mode as LIGHT_SLEEP \n"
            params = '{"standbyMode":"LIGHT_SLEEP"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\n setPreferredStandbyMode is success \n"
                tdkTestObj.setResultStatus("SUCCESS")
                print "Invoke org.rdk.System.1.getPreferredStandbyMode \n"
                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
                tdkTestObj.addParameter("reqValue","preferredStandbyMode")
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                preferred_standby = tdkTestObj.getResultDetails()
                if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
                    print "\n Preferred standby mode is LIGHT_SLEEP \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                    power_states = ["STANDBY","ON"]
                    for i in range (0,2):
                        print "\n Set power state to {} \n".format(power_states[i])
                        params = '{"powerState":"'+power_states[i]+'", "standbyReason":"APIUnitTest"}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue');
                        tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                        tdkTestObj.addParameter("value",params);
                        if power_states[i] == "ON":
                            start_power_on = str(datetime.utcnow()).split()[1]
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult();
                        if expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(10)
                            print "\n Verify the Power state \n"
                            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                            tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                            tdkTestObj.addParameter("reqValue","powerState")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            power_state = tdkTestObj.getResultDetails()
                            if expectedResult in result:
                                if power_state == power_states[i]:
                                    print "\n Successfully set power state to : {}\n".format(power_states[i])
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Unable to set the powerstate to : {}, current power state:{}\n".format(power_states[i],power_state)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print "\n Error while executing org.rdk.System.1.getPowerState method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Error while executing org.rdk.System.1.setPowerState method \n"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        time.sleep(10)
                        if ssh_param_dict["ssh_method"] == "directSSH":
                            if ssh_param_dict["password"] == "None":
                                password = ""
                            else:
                                password = ssh_param_dict["password"]
                            credentials = ssh_param_dict["host_name"]+','+ssh_param_dict["user_name"]+','+password
                        else:
                            #TODO
                            print "selected ssh method is {}".format(ssh_param_dict["ssh_method"])
                            pass
                        #Command to get onSystemPowerStateChanged event log from wpeframework.log for power state ON
                        command = 'cat /opt/logs/wpeframework.log | grep -inr "onSystemPowerStateChanged: power state changed to.*ON.*" |  tail -1'
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",credentials)
                        tdkTestObj.addParameter("command",command)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        output = tdkTestObj.getResultDetails()
                        if output != "EXCEPTION" and expectedResult in result:
                            if len(output.split('\n')) == 3 :
                                power_on_log = output.split('\n')[1]
                                conf_file,file_status = getConfigFileName(obj.realpath)
                                config_status,standby_to_on_threshold = getDeviceConfigKeyValue(conf_file,"STANDBY_TO_ON_THRESHOLD_VALUE")
                                if standby_to_on_threshold != "":
                                    start_power_on_in_millisec = getTimeInMilliSec(start_power_on)
                                    power_on_time = getTimeStampFromString(power_on_log)
                                    power_on_time_in_millisec = getTimeInMilliSec(power_on_time)
                                    print "\n Set power state to ON initiated at: " + start_power_on + "(UTC)"
                                    print "\n Power state became ON at : "+ power_on_time + "(UTC)"
                                    time_taken_for_poweron = power_on_time_in_millisec - start_power_on_in_millisec
                                    print "\n Time taken to Power ON from STANDBY: {}(ms)".format(time_taken_for_poweron)
                                    print "\n Validate the time: \n"
                                    if 0 < time_taken_for_poweron < int(standby_to_on_threshold) :
                                        print "\n Time taken for setting power state to ON is within the expected range \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Time taken for setting power state to ON is not within the expected range \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Please configure the Threshold value in device configuration file \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n onSystemPowerStateChanged log is not present in wpeframework.log \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error in SSH session to the device \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    if revert_power_state:
                        print "Reverting the Power state \n"
                        print "\n Set power state to {} \n".format(current_power_state)
                        params = '{"powerState":"'+current_power_state+'", "standbyReason":"APIUnitTest"}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue');
                        tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                        tdkTestObj.addParameter("value",params);
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult();
                        if expectedResult in result:
                            print "Reverted the power state to {}\n".format(current_power_state)
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while reverting the power state to {}\n".format(current_power_state)
                            tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing org.rdk.System.1.getPreferredStandbyMode method \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing org.rdk.System.1.setPreferredStandbyMode method \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while executing org.rdk.System.1.getPowerState method \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
