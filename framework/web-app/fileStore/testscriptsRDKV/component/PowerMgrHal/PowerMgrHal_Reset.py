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
  <version>3</version>
  <name>PowerMgrHal_Reset</name>
  <primitive_test_id/>
  <primitive_test_name>PowerMgrHal_Reset</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to invoke the HAL API PLAT_Reset , which will reboot the device</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-Wifi</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PowerMgrHal_10</test_case_id>
    <test_objective>Test script to invoke the HAL API PLAT_Reset , which will reboot the device</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG,XI3,XI6,Video_Accelerator</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module</pre_requisite>
    <api_or_interface_used>int PLAT_INIT(void)
void PLAT_Reset(IARM_Bus_PWRMgr_PowerState_t newState)</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialise the powerMgr hal module using PLAT_INIT API
3.Invoke PLAT_Reset  API to reset power state.API reboots the device
4.Based on the device uptime update the test status as SUCCESS/FAILURE
5.Unload the module</automation_approch>
    <expected_output>API should reboot the device </expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_Reset</test_script>
    <skipped>No</skipped>
    <release_version>M77</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from time import sleep


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("pwrmgrhal","1");
sysObj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'PowerMgrHal_Reset');
sysObj.configureTestCase(ip,port,'PowerMgrHal_Reset');

#Get the result of connection with test component and STB
loadModuleStatus1 = obj.getLoadModuleResult();
loadModuleStatus2 = sysObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus1;
print "[SYS UTIL LIB LOAD STATUS]  :  %s" %loadModuleStatus2;

if "SUCCESS" in loadModuleStatus1.upper() and "SUCCESS" in loadModuleStatus2.upper():
    obj.setLoadModuleStatus("SUCCESS");
    sysObj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    print "\nTEST STEP1 : Reset the power state of the device using PLAT_Reset API"
    print "EXEPECTED OUTPUT : API should reboot the device"
    tdkTestObj = obj.createTestStep('PowerMgrHal_Reset');
    sysObj.saveCurrentState();
    tdkTestObj.executeTestCaseReboot(expectedResult);
    sysObj.restorePreviousStateAfterReboot();
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    tdkTestObj.setResultStatus("SUCCESS");
    print "PLAT_Reset API Invocation : ",actualResult


    print "\nTEST STEP2 : Check the device uptime"
    print "EXPECTED RESULT : Should get the uptime less than or equal to 3 minutes"
    tdkTestObj = sysObj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command", "uptime");
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    uptime = str(str(details).split(",")[0].split("up")[1].strip())
    time = int(float(uptime.split(" ")[0]))
    if expectedResult in actualResult and time <= 3:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Value Returned : ",details
        print "Device Uptime  : ",uptime
        print "ACTUAL RESULT  : PLAT_Reset call success"
        print "[TEST EXECUTION RESULT] : SUCCESS\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("pwrmgrhal");
    obj.unloadModule("systemutil");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");
    sysObj.setLoadModuleStatus("FAILURE");


