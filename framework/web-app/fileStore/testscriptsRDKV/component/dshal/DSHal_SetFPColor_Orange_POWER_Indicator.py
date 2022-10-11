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
  <version>1</version>
  <name>DSHal_SetFPColor_Orange_POWER_Indicator</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_SetFPColor</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to set the color of the specified front panel indicator LED, if the indicator supports it (i.e. is multi-colored)</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_72</test_case_id>
    <test_objective>Test script to set the color of the specified front panel indicator LED, if the indicator supports it (i.e. is multi-colored)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsSetFPColor(eIndicator,eColor)</api_or_interface_used>
    <input_parameters>eIndicator - FP LED indicator [POWER]
eColor - Orange</input_parameters>
    <automation_approch>1.TM loads the DSHAL agent via the test agent.
2.DSHAL agent will invoke the API dsSetFPColor with parameter LED indicator 1 [POWER LED] and color Orange
3.Check the API return status 
4.Update the test result as SUCCESS/FAILURE , based on API return status
5.Unload the module</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_SetFPColor_Orange_POWER_Indicator</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import deviceCapabilities;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_SetFPColor_Orange_POWER_Indicator');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

#Check whether the device supports SetColor and Power LED
capable = deviceCapabilities.getconfig(obj,"SetColor") and deviceCapabilities.getconfig(obj,"Indicator","Power");

if "SUCCESS" in loadModuleStatus.upper() and capable:
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    print "\nTEST STEP1 : To set color of Power indicator in Front Panel to Orange"
    print "EXEPECTED RESULT : Should set the power led colour to Orange"
    tdkTestObj = obj.createTestStep('DSHal_SetFPColor');
    # POWER LED
    led = "POWER"
    indicator = 1
    color = "ORANGE";
    tdkTestObj.addParameter("indicator",indicator);
    tdkTestObj.addParameter("color",color);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : %s led [Indicator-%d] color is set to %s" %(led,indicator,color)
        print "Value Returned : ",details
        print "[TEST EXECUTION RESULT] : SUCCESS\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("dshal");

elif not capable and "SUCCESS" in loadModuleStatus.upper():
    print "Exiting from script";
    obj.setLoadModuleStatus("FAILURE");
    obj.unloadModule("dshal");


else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");
