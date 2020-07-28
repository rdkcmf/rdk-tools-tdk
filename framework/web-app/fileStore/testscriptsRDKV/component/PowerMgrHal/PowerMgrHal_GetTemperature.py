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
  <name>PowerMgrHal_GetTemperature</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_GetTemperature</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to get the temperature of the core by invoking PowerMgr  HAL API PLAT_API_GetTemperature</synopsis>
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
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PowerMgrHal_03</test_case_id>
    <test_objective>Test script to get the temperature of the core by invoking PowerMgr  HAL API PLAT_API_GetTemperature</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3,XI6</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module</pre_requisite>
    <api_or_interface_used>int PLAT_INIT(void)
int PLAT_API_GetTempThresholds(float *tempHigh, float *tempCritical)
int PLAT_API_GetTemperature(IARM_Bus_PWRMgr_ThermalState_t *curState, float *curTemperature, float *wifiTemperature)</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialise the powerMgr hal module using PLAT_INIT API
3.Invoke PLAT_API_GetTempThresholds API to get the temperature thresholds
4.Invoke PLAT_API_GetTemperature API to get the core,wifi chip temperature in degree celcius and thermal state
5.Based on the API return value,comparing the temperature with threshold levels and checking the thermal state, update the test status as SUCCESS/FAILURE
6.Unload the module</automation_approch>
    <expected_output>API should give the temperature of core, wifi chip and thermal state. state should be NORMAL if temp &lt; high &lt; critical or state should be HIGH if high &lt; temp &lt; critical or state should be CRITICAL if temp &gt; critical &gt; high </expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_GetTemperature</test_script>
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
obj.configureTestCase(ip,port,'PowerMgrHal_GetTemperature');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # This test script compares the core temperature with the threshold levels
    # Thermal state should be NORMAL   if temp < high < critical
    # Thermal state should be HIGH     if high < temp < critical
    # Thermal state should be CRITICAL if temp > critical > high

    # Sample stub output:
    # PLAT_API_GetTempThresholds
    #   Thermal threshold : high=%f, critical=%f
    # PLAT_API_GetTemperature
    #   Current_Temp=%f, Wifi_Temp=%f, State=%s

    print "\nTEST STEP1 : Get the high & critical temperature threshold using PLAT_API_GetTempThresholds API"
    print "EXEPECTED RESULT : Should get the default temperature thresholds"
    tdkTestObj = obj.createTestStep('PowerMgrHal_GetTempThresholds');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Value Returned : ",details
        actual_high     = float(str(str(details).split(":")[1].split(",")[0].split("=")[1]))
        actual_critical = float(str(str(details).split(":")[1].split(",")[1].split("=")[1]))

        print "\nTEST STEP2 : Get the Core Temperature using PLAT_API_GetTemperature"
        print "EXEPECTED RESULT : Should get the temperature in centigrade"
        tdkTestObj = obj.createTestStep('PowerMgrHal_GetTemperature');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Value Returned : ",details
            core_temp  = float(str(str(details).split(",")[0].split("=")[1]))
            wifi_temp  = float(str(str(details).split(",")[1].split("=")[1]))
            temp_state = str(details).split(",")[2].split("=")[1]
            if core_temp != 0 and core_temp < float(actual_high) and core_temp < float(actual_critical) and "NORMAL" in temp_state:
                print "Core temperature within thermal threshold levels"
                print "ACTUAL RESULT  : PLAT_API_GetTemperature call is success"
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
            elif core_temp != 0 and core_temp > float(actual_high) and core_temp < float(actual_critical) and "HIGH" in temp_state:
                print "Core temperature greater than high level but less than critical level"
                print "ACTUAL RESULT  : PLAT_API_GetTemperature call is success"
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
            elif core_temp != 0 and core_temp > float(actual_high) and core_temp > float(actual_critical) and "CRITICAL" in temp_state:
                print "Core temperature greater than high and critical threshold levels"
                print "ACTUAL RESULT  : PLAT_API_GetTemperature call is success"
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
            else:
                print "Core temperature details are not as expected"
                print "ACTUAL RESULT  : PLAT_API_GetTemperature call is failed"
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


