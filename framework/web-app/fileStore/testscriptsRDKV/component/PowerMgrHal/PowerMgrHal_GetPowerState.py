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
  <name>PowerMgrHal_GetPowerState</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_GetPowerState</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to get the CPE power state.As far as Broadcom is concerned, PLAT_API_GetPowerState  API reads the power state from the global variable only</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PowerMgrHal_01</test_case_id>
    <test_objective>Test Script to get the CPE Power using PLAT_API_GetPowerState API. As far as Broadcom is concerned, this API reads the power state from the global variable only </test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module
</pre_requisite>
    <api_or_interface_used>PLAT_API_GetPowerState(IARM_Bus_PWRMgr_PowerState_t *state)</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialise the powerMgr hal module using PLAT_INIT API
3.Invoke PLAT_API_GetPowerState API to get the power state. API reads the global variable only
4.Based on the API return value update the test status as SUCCESS/FAILURE
5.Unload the module</automation_approch>
    <expected_output>Should return the CPE Power state</expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_GetPowerState</test_script>
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
obj.configureTestCase(ip,port,'PowerMgrHal_GetPowerState');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # As far as Broadcom is concerned, PLAT_API_GetPowerState API reads the
    # power state from the global variable only
    print "\nTEST STEP1 : Get the CPE power state using PLAT_API_GetPowerState"
    print "EXEPECTED OUTPUT : Should get the current power state"
    tdkTestObj = obj.createTestStep('PowerMgrHal_GetPowerState');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Value Returned : ",details
        print "ACTUAL RESULT  : PLAT_API_GetPowerState call is success"
        print "[TEST EXECUTION RESULT] : SUCCESS\n"

    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("pwrmgrhal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


