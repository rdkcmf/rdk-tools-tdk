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
  <id>586</id>
  <version>1</version>
  <name>DS_SetBrightness_Minimum value test_23</name>
  <primitive_test_id>76</primitive_test_id>
  <primitive_test_name>DS_SetBrightness</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Sets and gets the minimum Brightness of the given Front panel Indicator
Test Case ID : CT_DS_23</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_23</test_case_id>
    <test_objective>Device Setting – Get and Set brightness for front panel Indicator with Minimum value</test_objective>
    <test_type>Positive(Boundary condition)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()                                  FrontPanelIndicator::getInstance()
FrontPanelIndicator::getIndicators()
FrontPanelIndicator::getIndicator(string)
FrontPanelIndicator::getBrightness() 
FrontPanelIndicator::setBrightness(int)                  device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>getIndicator : string  - name
E.g.: name: “POWER” 
SetBrightness : int - brightness 
E.g.: Value is  0. </input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the list of Indicators.
3.Device_Settings_Agent will get the indicators by passing the “name: POWER”
4.Device_Settings_Agent will get the value of brightness for POWER Indicator.
5.Device_Settings_Agent will set the brightness value to “brightness” for the POWER Indicator.
6.TM makes RPC calls for getting the POWER Indicator brightness value from Device_Settings_Agent and verify whether the brightness has changed.
7.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step(6th)</automation_approch>
    <except_output>
Checkpoint 1.Check for the value of POWER Indicator brightness after and before setting the value of brightness.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_getIndicators
TestMgr_DS_FP_setBrightness
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetBrightness_Minimum value test_23</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
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
obj.configureTestCase(ip,port,'CT_DS_23');
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
                tdkTestObj = obj.createTestStep('DS_GetIndicators');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                indicatordetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_GetIndicators 
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of Indicators";
                        print "Indicators:%s" %indicatordetails
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the Indicators list";
                tdkTestObj = obj.createTestStep('DS_SetBrightness');
                #setting brightness parameter value
                brightness = 0;
                print "Brightness value set to:%d" %brightness;
                indicator_name = "Power";
                print "Indicator name value set to:%s" %indicator_name;
                tdkTestObj.addParameter("brightness",brightness);
                tdkTestObj.addParameter("indicator_name",indicator_name);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                getBrightness = tdkTestObj.getResultDetails();
                setBrightness = "%s" %brightness;
                print "getBrightness:%s" %getBrightness;
                #Check for SUCCESS/FAILURE return value of DS_SetBrightness
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully gets and sets the Minimum Brightness";
                        #comparing the brightness value before and after setting
                        if setBrightness in getBrightness :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the Brightness are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the Brightness are not same";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failure: Failed to get and set Brightness for LED";
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
