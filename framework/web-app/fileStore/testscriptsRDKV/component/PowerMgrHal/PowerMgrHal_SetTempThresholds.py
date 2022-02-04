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
  <name>PowerMgrHal_SetTempThresholds</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_SetTempThresholds</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to set high and critical temperature threshold values using PLAT_API_SetTempThresholds API</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PowerMgrHal_05</test_case_id>
    <test_objective>Test Script to set high and critical temperature threshold values using PLAT_API_SetTempThresholds API</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3,XI6,Video_Accelerator</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module</pre_requisite>
    <api_or_interface_used>int PLAT_INIT(void)
int PLAT_API_GetTempThresholds(float *tempHigh, float *tempCritical)
int PLAT_API_SetTempThresholds(float tempHigh, float tempCritical)</api_or_interface_used>
    <input_parameters>high - temp high value
critical - temp critical value</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialize the PowerMgr Hal module using PLAT_INIT API
3.Get the default temperature threshold levels using PLAT_API_GetTempThresholds. Add 10 to the default levels to get new threshold levels
4.Invoke PLAT_API_SetTempThresholds API to set the new temperature thresholds
5.Get current threshold levels using PLAT_API_GetTempThresholds. Current levels should be equal to the new values set.
6.Based on the API return value and and comparing the current threshold levels with new levels set, update the test status as SUCCESS/FAILURE
7.Unload the module</automation_approch>
    <expected_output>Should set the new temperature threshold levels using PLAT_API_SetTempThresholds  and get new  threshold levels set using PLAT_API_GetTempThresholds</expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_SetTempThresholds</test_script>
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
obj.configureTestCase(ip,port,'PowerMgrHal_SetTempThresholds');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # Sample stub output:
    # PLAT_API_GetTempThresholds
    #   Thermal threshold : high=%f, critical=%f

    print "\nTEST STEP1 : Get the high & critical temperature threshold using PLAT_API_GetTempThresholds API"
    print "EXEPECTED OUTPUT : Should get the current temperature thresholds"
    tdkTestObj = obj.createTestStep('PowerMgrHal_GetTempThresholds');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        actual_high     = float(str(str(details).split(":")[1].split(",")[0].split("=")[1]))
        actual_critical = float(str(str(details).split(":")[1].split(",")[1].split("=")[1]))
        print "Value Returned : ",details
        print "ACTUAL RESULT  : PLAT_API_GetTempThresholds call is success"

        print "\nTEST STEP2 : Set the high & critical temperature threshold using PLAT_API_SetTempThresholds API"
        print "EXEPECTED OUTPUT : Should set the new temperature thresholds"
        tdkTestObj = obj.createTestStep('PowerMgrHal_SetTempThresholds');
        new_high     = int(actual_high)     + 10
        new_critical = int(actual_critical) + 10
        print "New Thermal threshold : high=%f, critical=%f" %(new_high,new_critical)
        tdkTestObj.addParameter("high",int(new_high));
        tdkTestObj.addParameter("critical",int(new_critical));
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT  :",details

            print "\nTEST STEP3 : Get the latest high & critical temperature threshold using PLAT_API_GetTempThresholds API"
            print "EXEPECTED OUTPUT : Should get the updated temperature thresholds"
            tdkTestObj = obj.createTestStep('PowerMgrHal_GetTempThresholds');
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                updated_high     = float(str(str(details).split(":")[1].split(",")[0].split("=")[1]))
                updated_critical = float(str(str(details).split(":")[1].split(",")[1].split("=")[1]))
                print "Value Returned : ",details
                if updated_high == float(new_high) and updated_critical == float(new_critical):
                    print "ACTUAL RESULT : Thermal thresholds set operation success"
                    print "[TEST EXECUTION RESULT] : SUCCESS"

                    print "\nTEST STEP4 : Revert the high & critical temperature threshold using PLAT_API_SetTempThresholds API"
                    print "EXEPECTED OUTPUT : Should set the actual temperature thresholds"
                    tdkTestObj = obj.createTestStep('PowerMgrHal_SetTempThresholds');
                    print "Actual Thermal threshold : high=%f, critical=%f" %(actual_high,actual_critical)
                    tdkTestObj.addParameter("high",int(actual_high));
                    tdkTestObj.addParameter("critical",int(actual_critical));
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "ACTUAL RESULT : Thermal thresholds revert operation success"
                        print "[TEST EXECUTION RESULT] : SUCCESS\n"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "ACTUAL RESULT : Thermal thresholds revert operation failed"
                        print "[TEST EXECUTION RESULT] : FAILURE\n"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "ACTUAL RESULT : Thermal thresholds set operation failed"
                    print "[TEST EXECUTION RESULT] : FAILURE\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT  : ",details
                print "[TEST EXECUTION RESULT] : FAILURE\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "ACTUAL RESULT  :",details
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("pwrmgrhal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


