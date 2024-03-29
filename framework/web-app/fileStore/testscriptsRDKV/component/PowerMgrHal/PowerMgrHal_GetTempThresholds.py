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
  <name>PowerMgrHal_GetTempThresholds</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_GetTempThresholds</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to invoke PLAT_API_GetTempThresholds to get high and critical temperatures thresholds at which mfrTEMPERATURE_HIGH and mfrTEMPERATURE_CRITICAL are reported.</synopsis>
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
    <test_case_id>TC_PowerMgrHal_04</test_case_id>
    <test_objective>Test script to invoke PLAT_API_GetTempThresholds to get high and critical temperatures thresholds at which mfrTEMPERATURE_HIGH and mfrTEMPERATURE_CRITICAL are reported.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3,XI6,Video_Accelerator</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module
</pre_requisite>
    <api_or_interface_used>int PLAT_INIT(void)
int PLAT_API_GetTempThresholds(float *tempHigh, float *tempCritical)</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialize the PowerMgr Hal module using PLAT_INIT API
3.Invoke PLAT_API_GetTempThresholds API to get the temperature thresholds
4.Compare the threshold levels obtained with default threshold levels set during power manager initialization
5.Based on the API return value and comparing the current threshold levels with default levels set, update the test status as SUCCESS/FAILURE
6.Unload the module</automation_approch>
    <expected_output>High and Critical threshold levels should be equal to 100 and 110 </expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_GetTempThresholds</test_script>
    <skipped>No</skipped>
    <release_version>M77</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from ConfigParser import SafeConfigParser
import os

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("pwrmgrhal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'PowerMgrHal_GetTempThresholds');

# Temperature Threshold levels are set as high:100 and critical:110
# by power manager each time when the module is initialized

# Sample stub output:
# PLAT_API_GetTempThresholds
#   Thermal threshold : high=%f, critical=%f

default_high_level     = 100
default_critical_level = 110

Default_Temperature_Thresholds = {"thermal_concern_threshold":default_high_level,"thermal_critical_threshold":default_critical_level};

def getconfig(threshold):
    parser = SafeConfigParser()
    # Fetching the config details from configuration file
    parser.read( os.path.dirname(os.path.abspath(__file__))+"/temperatureThresholds.ini")
    print "Parsing Temperature Thresholds config file ..."
    ConfigValue = parser.get('threshold',threshold);
    if ConfigValue:
        print "Obtained %s for %s from config File"%(ConfigValue,threshold);
        return ConfigValue;
    else:
        print "%s not configured in Config File\nProceeding with execution with default %s"%(threshold,threshold);
        return Default_Temperature_Thresholds[threshold];


#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    default_high_level = getconfig("thermal_concern_threshold");
    default_critical_level = getconfig("thermal_critical_threshold");

    print "\nTEST STEP1 : Get the high & critical temperature threshold using PLAT_API_GetTempThresholds API"
    print "EXEPECTED OUTPUT : Should get the default temperature thresholds"
    tdkTestObj = obj.createTestStep('PowerMgrHal_GetTempThresholds');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Value Returned : ",details
        actual_high_level     = float(str(str(details).split(":")[1].split(",")[0].split("=")[1]))
        actual_critical_level = float(str(str(details).split(":")[1].split(",")[1].split("=")[1]))
        if actual_high_level == float(default_high_level) and  actual_critical_level == float(default_critical_level):
            tdkTestObj.setResultStatus("SUCCESS");
            print "Thermal Threshold levels are same as that of expected default levels"
            print "ACTUAL RESULT  : PLAT_API_GetTempThresholds call is success"
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Thermal Threshold levels are not same as that of expected default levels"
            print "ACTUAL RESULT  : PLAT_API_GetTempThresholds call is success"
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("pwrmgrhal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


