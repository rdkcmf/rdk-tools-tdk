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
  <id>648</id>
  <version>1</version>
  <name>DS_SetText_STRESS_test_104</name>
  <primitive_test_id>86</primitive_test_id>
  <primitive_test_name>DS_SetText</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test is to successfully change text in the Text Display of the front panel indicator continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_104</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_104</test_case_id>
    <test_objective>Device Setting – Get and Set the Text display with different strings continuously for every 100ms repeatedly for x times.</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()   
FrontPanelConfig::getInstance()
FrontPanelConfig::getTextDisplays ()      
FrontPanelConfig::getTextDisplay(string)
FrontPanelConfig::setText()
Device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>getTextDisplay : string – name 
name:“TEXT” 
SetText : string- text
E.g.: text: “any word”</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get the list of test display panel in the front Panel.
3.Device_Settings_Agent will get a instance for single test display panel by “passing name:TEXT”
4.Device_Settings_Agent will set some text in the text display panel of front panel indicator.
5.TM makes RPC calls for getting the TEXT format from Device_Settings_Agent.
6.Device_Settings_Agent will wait for 100 ms and change to another TEXT and verify the change.
7. The steps 4-6 will be repeated for 100 times and check the successful change of  new Text and store the result.
8.Device_Settings_Agent will return SUCCESS or FAILURE based on the result</automation_approch>
    <except_output>


Checkpoint 1. Check for the return value of setText APIs.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setText
TestMgr_DS_FP_setTime
TestMgr_DS_FP_setTimeForamt
TestMgr_DS_FP_getTextDisplays
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetText_STRESS_test_104</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_104');
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
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                i = 0;
                for i in range(0,5):
                        print "****************%d" %i;
                        #calling DS_SetText to set the TEXT in the FP
                        tdkTestObj = obj.createTestStep('DS_SetText');
                        tdkTestObj.addParameter("text_display","Hello world");
                        tdkTestObj.addParameter("text","Text");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        #Check for SUCCESS/FAILURE return value of DS_SetText
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Application successfully Sets the Text in text panel";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "FAILURE :Application failed to set the text in FP";
                        time.sleep(100/1000);
                        #calling DS_SetText to set the TEXT in the FP
                        tdkTestObj = obj.createTestStep('DS_SetText');
                        tdkTestObj.addParameter("text_display","ANYWORD");
                        tdkTestObj.addParameter("text","Text");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        #Check for SUCCESS/FAILURE return value of DS_SetText
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Application successfully Sets the Text in text panel";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "FAILURE :Application failed to set the text in FP";

                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
