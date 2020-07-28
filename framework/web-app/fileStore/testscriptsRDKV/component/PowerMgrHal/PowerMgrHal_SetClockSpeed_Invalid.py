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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>PowerMgrHal_SetClockSpeed_Invalid</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_SetClockSpeed</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to set invalid value as cpu speed using PLAT_API_SetClockSpeed API and verify that the invalid values is  not taken by the CPU</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PowerMgrHal_13</test_case_id>
    <test_objective>Test Script to set invalid value as cpu speed using PLAT_API_SetClockSpeed API and verify that the invalid values is not taken by the CPU</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI6</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module</pre_requisite>
    <api_or_interface_used>int PLAT_INIT(void)
int PLAT_API_SetClockSpeed(uint32_t speed)
int PLAT_API_GetClockSpeed(uint32_t *speed)</api_or_interface_used>
    <input_parameters>speed - minimal  cpu clock speed</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialise the powerMgr hal module using PLAT_INIT API
3. Invoke PLAT_API_SetClockSpeed  API to set some invalid clock speed value
4.Invoke PLAT_API_GetClockSpeed to get the current clock speed
5. Based on the API return value and comparing the clock speed value before and after set, update the test status as SUCCESS/FAILURE
6.Unload the module</automation_approch>
    <expected_output>Invalid clock speed values should not be set</expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_SetClockSpeed_Invalid</test_script>
    <skipped>No</skipped>
    <release_version>M79</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("pwrmgrhal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'PowerMgrHal_SetClockSpeed_Invalid');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # Test script tries to set invalid clock speed. If we try to set some arbitrary values
    # it will return success but CPU may not run input value

    # Sample stub output:
    # PLAT_API_GetClockSpeed
    #   Default Frequency=%d

    print "\nTEST STEP1 : Get the CPU clock speed using PLAT_API_GetClockSpeed"
    print "EXEPECTED OUTPUT : Should get the default clock speed of CPU"
    tdkTestObj = obj.createTestStep('PowerMgrHal_GetClockSpeed');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        cpu_speed_default = int(str(str(details).split("=")[1]))
        print "Value Returned : ",details
        print "ACTUAL RESULT  : PLAT_API_GetClockSpeed call is success"


        # PLAT_API_SetClockSpeed  API is applicable for ARM platform only. Not supposed to execute on MIPS platform
        print "\nTEST STEP2 : Set the CPU clock speed using PLAT_API_SetClockSpeed API"
        print "EXPECTED RESULT : Should set the invalid cpu speed value"
        tdkTestObj = obj.createTestStep('PowerMgrHal_SetClockSpeed');
        expectedResult = "FAILURE"
        cpu_speed_invalid = -10
        print "CPU invalid speed to be set : %d" %(cpu_speed_invalid)
        tdkTestObj.addParameter("speed",int(cpu_speed_invalid));
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT  : ",details

            print "\nTEST STEP3 : Get the CPU clock speed using PLAT_API_GetClockSpeed"
            print "EXEPECTED OUTPUT : Should get the current clock speed of CPU"
            tdkTestObj = obj.createTestStep('PowerMgrHal_GetClockSpeed');
            expectedResult = "SUCCESS"
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                cpu_speed_actual = int(str(str(details).split("=")[1]))
                print "Vailue Returned : ",details
                if cpu_speed_actual == cpu_speed_default:
                    print "ACTUAL RESULT  : Invalid CPU speed is not set"
                    print "[TEST EXECUTION RESULT] : SUCCESS\n"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "ACTUAL RESULT  : Invalid CPU speed is set"
                    print "[TEST EXECUTION RESULT] : FAILURE\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT  : ",details
                print "[TEST EXECUTION RESULT] : FAILURE\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "ACTUAL RESULT  : ",details
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("pwrmgrhal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


