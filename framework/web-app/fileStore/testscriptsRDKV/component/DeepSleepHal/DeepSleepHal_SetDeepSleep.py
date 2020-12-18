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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>2</version>
  <name>DeepSleepHal_SetDeepSleep</name>
  <primitive_test_id/>
  <primitive_test_name>DeepSleepHal_SetDeepSleep</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to invoke deep sleep HAL API PLAT_DS_SetDeepSleep  to set deep sleep for 60 sec.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_DeepSleepHal_01</test_case_id>
    <test_objective>Test script to invoke deep sleep HAL API PLAT_DS_SetDeepSleep  to set deep sleep for 60 sec.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>1.TDK agent should be up and running
2.Initialize DeepSleep management module</pre_requisite>
    <api_or_interface_used>PLAT_DS_SetDeepSleep(uint32_t deep_sleep_timeout)</api_or_interface_used>
    <input_parameters>timeout - time in seconds</input_parameters>
    <automation_approch>1.Load the deep sleep hal module
2.Initialise the deep sleep module using PLAT_DS_INIT API
3.Invoke PLAT_DS_SetDeepSleep API with 60 sec timeout
4.CPU will be freezed for about an minute and resumes back.
5.Stub calculates the time interval between API call and CPU resume time and return it.
6.Check the CPU freeze duration and if it is greater than the timeout set, reboot  the device.
7.Update test result as SUCCESS/FAILURE if device satisfies expected behavior
8.Unload the module</automation_approch>
    <expected_output>API should set deep sleep and CPU should be freezed and resume back once the timeout is reached</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdeepsleephalstub.so.0.0.0</test_stub_interface>
    <test_script>DeepSleepHal_SetDeepSleep</test_script>
    <skipped>No</skipped>
    <release_version>M77</release_version>
    <remarks>Applicable for client devices only</remarks>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("deepsleephal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DeepSleepHal_SetDeepSleep');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    print "\nTEST STEP1 : Set deep sleep for 60 seconds using PLAT_DS_SetDeepSleep API"
    print "EXPECTED RESULT : Should set the deep sleep & cpu should be freezed for given timeout duration"
    timeout = 60;
    print "Timeout for deep sleep : %d (secs)" %(timeout)
    tdkTestObj = obj.createTestStep('DeepSleepHal_SetDeepSleep');
    tdkTestObj.addParameter("timeout", timeout);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        if "GPIOWakeup" in str(details):
            freezeDuration = int(str(details).split(";")[0].split(":")[1].strip())
            GPIOWakeup = int(str(details).split(";")[1].split(":")[1].strip())
            print "Value Returned : %s secs (approx), %s" %(str(details).split(";")[0],str(details).split(";")[1])
            print "ACTUAL RESULT  : %s" %(str(details).split(";")[2])
            print "[TEST EXECUTION RESULT] : SUCCESS\n"

            print "\nTEST STEP2: Check CPU freeze duration & GPIO Wakeup status and reboot the device"
            print "EXPECTED RESULT : Reboot if freeze duration is >= timeout & GPIO Wakeup status should be 0"
            if int(freezeDuration) >= int(timeout) and int(GPIOWakeup) == 0:
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT  : CPU freeze duration & GPIO Wakeup status are as expected"
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
                obj.initiateReboot();
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT  : CPU freeze duration & GPIO Wakeup status are not as expected"
                print "[TEST EXECUTION RESULT] : FAILURE\n"
        else:
            freezeDuration = int(str(details).split(";")[0].split(":")[1].strip())
            print "Value Returned : %s secs (approx)" %(str(details).split(";")[0])
            print "ACTUAL RESULT  : %s" %(str(details).split(";")[1])
            print "[TEST EXECUTION RESULT] : SUCCESS\n"

            print "\nTEST STEP2: Check CPU freeze duration and reboot the device"
            print "EXPECTED RESULT : Reboot if freeze duration is >= timeout"
            if int(freezeDuration) >= int(timeout):
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT  : CPU freeze duration is as expected"
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
                obj.initiateReboot();
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT  : CPU freeze duration is not as expected"
                print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("deepsleephal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


