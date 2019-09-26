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
  <id>644</id>
  <version>1</version>
  <name>DS_SetBrightness_STRESS_test_100</name>
  <primitive_test_id>76</primitive_test_id>
  <primitive_test_name>DS_SetBrightness</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test is to successfully change brightness value of the front panel indicator continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_100</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_100</test_case_id>
    <test_objective>Device Setting – Get and Set brightness for front panel Indicator with random values within range continuously for every 100ms repeatedly for x times.</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()                                  FrontPanelIndicator::getInstance()
FrontPanelIndicator::getIndicators()
FrontPanelIndicator::getIndicator(string)
FrontPanelIndicator::getBrightness() 
FrontPanelIndicator::setBrightness(int)                  device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>getIndicator : string  - name
E.g.: POWER
SetBrightness : int - brightness 
E.g.: Value  0. </input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the list of Indicators.
3.Device_Settings_Agent will get the indicators by passing the LED indicators.
4.Device_Settings_Agent will get the value of brightness for LED Indicator.
5.Device_Settings_Agent will set the brightness value to “brightness” for the LED Indicator.
6.Device_Settings_Agent will check for the new brightness value.
7.Device_Settings_Agent will wait for 100 ms and change to another brightness value and verify the change.
8. The steps 4-7 will be repeated for 100 times and check the successful change of resolution and store the result.
9.Device_Settings_Agent will return SUCCESS or FAILURE based on the result.</automation_approch>
    <except_output>
Checkpoint 1.Check for the value of POWER Indicator brightness after and before setting the value of brightness.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_getIndicators
TestMgr_DS_FP_setBrightness
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetBrightness_STRESS_test_100</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_100');
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
                i=0;
                for i in range(0,100):
                        print "****************%d" %i;
                        tdkTestObj = obj.createTestStep('DS_SetBrightness');
                        #setting brightness parameter value
                        brightness = 5;
                        print "Brightness value set to:%d" %brightness;
                        indicator_name = "Power";
                        print "Indicator name set to:%s" %indicator_name;  
                        tdkTestObj.addParameter("brightness",brightness);
                        tdkTestObj.addParameter("indicator_name",indicator_name);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        getBrightness = tdkTestObj.getResultDetails();
                        setBrightness = "%s" %brightness;
                        print "getBrightness:%s" %getBrightness;
                        #Check for SUCCESS return value of DS_SetBrightness
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the Brightness";
                                #comparing the brightness value before and after setting
                                if setBrightness in getBrightness :
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the Brightness are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the Brightness are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "Failure: Failed to get and set Brightness for LED";
                        time.sleep(100/1000);
                        tdkTestObj = obj.createTestStep('DS_SetBrightness');
                        #setting brightness parameter value
                        brightness = 10;
                        print "Brightness value set to:%d" %brightness;
                        indicator_name = "Power";
                        print "Indicator name set to:%s" %indicator_name;
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
                                print "SUCCESS :Application successfully gets and sets the Brightness";
                                #comparing the brightness value before and after setting
                                if setBrightness in getBrightness :
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the Brightness are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the Brightness are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "Failure: Failed to get and set Brightness for LED";
                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS";
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
