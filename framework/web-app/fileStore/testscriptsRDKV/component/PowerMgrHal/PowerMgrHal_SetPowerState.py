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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>PowerMgrHal_SetPowerState</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_SetPowerState</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to set power state using PLAT_API_SetPowerState API. As far as Broadcom is concerned, PLAT_API_SetPowerState API updates the global variable only but not the devices's actual state</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PowerMgrHal_02</test_case_id>
    <test_objective>Test Script to set power state using PLAT_API_SetPowerState API. As far as Broadcom is concerned, PLAT_API_SetPowerState API updates the global variable only but not the devices's actual state</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG,XI3,XI6</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module</pre_requisite>
    <api_or_interface_used>int PLAT_INIT(void)
int PLAT_API_GetPowerState(IARM_Bus_PWRMgr_PowerState_t *curState)
int PLAT_API_SetPowerState(IARM_Bus_PWRMgr_PowerState_t newState)</api_or_interface_used>
    <input_parameters>state - ON / OFF (power states)</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialise the powerMgr hal module using PLAT_INIT API
3.Invoke PLAT_API_SetPowerState API to set the power state. API updates the global variable only
4.Based on the API return value update the test status as SUCCESS/FAILURE
5.Unload the module</automation_approch>
    <expected_output>API should update the power state.</expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_SetPowerState</test_script>
    <skipped>No</skipped>
    <release_version>M77</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
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
obj.configureTestCase(ip,port,'PowerMgrHal_SetPowerState');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # As far as Broadcom is concerned, PLAT_API_SetPowerState API updates the
    # global variable only but not the devices's actual state
    print "\nTEST STEP1 : Set the power state using PLAT_API_SetPowerState"
    print "EXEPECTED OUTPUT : Should set the power state"
    tdkTestObj = obj.createTestStep('PowerMgrHal_SetPowerState');
    state = "STANDBY";
    print "Setting power state as %s" %(state)
    tdkTestObj.addParameter("state",state);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : SUCCESS"

        print "\nTEST STEP2 : Get the CPE power state using PLAT_API_GetPowerState"
        print "EXEPECTED OUTPUT : Should get the updated power state"
        tdkTestObj = obj.createTestStep('PowerMgrHal_GetPowerState');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult and state in details:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Value Returned : ",details
            print "ACTUAL RESULT  : Power state set operation success"
            print "[TEST EXECUTION RESULT] : SUCCESS"

            print "\nTEST STEP3 : Revert power state to ON using PLAT_API_SetPowerState"
            print "EXPECTED RESULT : Should set the power state as ON"
            tdkTestObj = obj.createTestStep('PowerMgrHal_SetPowerState');
            state = "ON"
            print "Setting power state as %s" %(state)
            tdkTestObj.addParameter("state",state);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT  : ",details
                print "[TEST EXECUTION RESULT] : SUCCESS"

                print "\nTEST STEP4 : Get the reverted power state using PLAT_API_GetPowerState"
                print "EXEPECTED OUTPUT : Should get the power state as ON"
                tdkTestObj = obj.createTestStep('PowerMgrHal_GetPowerState');
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedResult in actualResult and state in details:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Value Returned : ",details
                    print "ACTUAL RESULT  : Power state revert  operation success"
                    print "[TEST EXECUTION RESULT] : SUCCESS\n"

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
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("pwrmgrhal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


