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
  <name>DSHal_SetFPColor_Blue_INVALID_Indicator</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_SetFPColor</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to set the color of invalid front panel indicator LED and check whether API returns invalid param</synopsis>
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
    <test_case_id>CT_DS_HAL_76</test_case_id>
    <test_objective>Test script to set the color of the specified front panel indicator LED, if the indicator supports it (i.e. is multi-colored)</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsSetFPColor(eIndicator,eColor)</api_or_interface_used>
    <input_parameters>eIndicator - FP LED indicator [INVALID VALUE]
eColor - Blue</input_parameters>
    <automation_approch>1.TM loads the DSHAL agent via the test agent.
2.DSHAL agent will invoke the API dsSetFPColor with parameter LED indicator 6 [INVALID LED] and color Blue
3.Check the API return status 
4.Update the test result as SUCCESS/FAILURE , based on API return status
5.Unload the module</automation_approch>
    <expected_output>Checkpoint 1.API return value should be invalid-param</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_SetFPColor_Blue_INVALID_Indicator</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
obj.configureTestCase(ip,port,'DSHal_SetFPColor_Blue_INVALID_Indicator');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

#Check if SetColor is supported by DUT
capable = deviceCapabilities.getconfig(obj,"SetColor");

if "SUCCESS" in loadModuleStatus.upper() and capable:
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="FAILURE";
    print "\nTEST STEP1 : To set color of Invalid indicator in Front Panel to Blue"
    print "EXEPECTED RESULT : Should get the response as invalid LED"
    tdkTestObj = obj.createTestStep('DSHal_SetFPColor');
    # INVALID LED
    indicator = 6;
    color = "BLUE";
    tdkTestObj.addParameter("indicator",indicator);
    tdkTestObj.addParameter("color",color);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult and "Invalid LED Indicator" in details:
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT  : dsSetFPColor API returned dsERR_INVALID_PARAM for LED Indicator-%d" %(indicator)
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


