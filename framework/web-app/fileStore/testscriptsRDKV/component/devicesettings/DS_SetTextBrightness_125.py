##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
  <version>4</version>
  <name>DS_SetTextBrightness_125</name>
  <primitive_test_id>76</primitive_test_id>
  <primitive_test_name>DS_SetBrightness</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script Sets and gets a valid brightness value in the text display of given Front panel Indicator.
Test Case ID : CT_DS125</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS125</test_case_id>
    <test_objective>Sets and gets a valid brightness value in the text display of given Front panel Indicator.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()                                  
FrontPanelTextDisplay::getInstance("Text")
FrontPanelTextDisplay::setText(string)
FrontPanelTextDisplay::setTextBrightness(int)      
FrontPanelTextDisplay::getTextBrightness()             
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>integer brightness=100
string text="Hello"
integer get_only (0,1)</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2. Device_Settings_Agent will set the front panel text to message "hello".
3. Device_Settings_Agent will set the brightness of front panel text value to brightness value.
4. Device_Settings_Agent will get the brightness value of front panel text and verify whether the brightness has changed.</automation_approch>
    <except_output>
Checkpoint 1.Check for the brightness value of front panel text after and before setting the value of brightness.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setBrightness
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetTextBrightness_125</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks>XONE-11060</remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'DS_SetTextBrightness_125');
loadmodulestatus =obj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result.upper():
                #Primitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('DS_FP_setTextBrightness');
                value = 100
                tdkTestObj.addParameter("brightness",value);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION RESULT] : %s" %actualresult;
                print "Details: [%s]"%details;
                #Set the result status of execution
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(obj)
else :
        print "Failed to Load Module"

obj.unloadModule("devicesettings");

