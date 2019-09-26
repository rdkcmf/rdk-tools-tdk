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
  <id>1593</id>
  <version>6</version>
  <name>DS_TextBrightness_Persistent_117</name>
  <primitive_test_id>76</primitive_test_id>
  <primitive_test_name>DS_SetBrightness</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check that Front Panel timer brightness value is persisted after STB reboot.
TestcaseID: CT_DS117</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS117</test_case_id>
    <test_objective>To check that Front Panel timer brightness value is persisted after STB reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize() 
FrontPanelIndicator::getInstance()
FrontPanelIndicator::getTextDisplay()
FrontPanelIndicator::setBrightness(int) 
FrontPanelIndicator::getBrightness() 
device::Manager::DeInitialize()
</api_or_interface_used>
    <input_parameters>integer brightness=5
string text="Hello"
integer get_only (0,1)</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the textdisplay by passing the message: "Hello"
3.Device_Settings_Agent will set the value of brightness for text.
4.Reboot the STB
5.TM makes RPC calls for getting the text brightness value from Device_Settings_Agent and verify whether the brightness has changed.</automation_approch>
    <except_output>Checkpoint 1 Check for return value of the brightness before and after reboot</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setBrightness
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_TextBrightness_Persistent_117</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>XONE-11452 </remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_TextBrightness_Persistent_117');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");

		#calling Device Settings - Set/Get TextDisplay Brightness
                tdkTestObj = obj.createTestStep('DS_FP_setTextBrightness');
                value = 5
                tdkTestObj.addParameter("brightness",value);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                setBrightness = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION RESULT] : %s" %actualresult;
                print "Details: [%s]"%setBrightness;
                #Set the result status of execution
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");

                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        # Reboot the box
        obj.initiateReboot();

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                #calling Device Settings - Get TextDisplay Brightness
                tdkTestObj = obj.createTestStep('DS_FP_getTextBrightness');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                getBrightness = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION RESULT] : %s" %actualresult;
                print "Details: [%s]"%getBrightness;
                #Set the result status of execution
                if expectedresult in actualresult:
                        #comparing the brightness value before and after setting
                        if setBrightness in getBrightness :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: TextBrightness same after reboot";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: TextBrightness changed after reboot";

                else:
                        tdkTestObj.setResultStatus("FAILURE");

                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
