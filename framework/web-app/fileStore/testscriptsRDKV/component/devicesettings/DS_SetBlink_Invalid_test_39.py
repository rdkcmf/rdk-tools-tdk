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
  <id>597</id>
  <version>1</version>
  <name>DS_SetBlink_Invalid_test_39</name>
  <primitive_test_id>75</primitive_test_id>
  <primitive_test_name>DS_SetBlink</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Sets and gets the iinvalid value for blink feature of given Front panel Indicator
Test Case ID : CT_DS_39</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_39</test_case_id>
    <test_objective>Device Setting – Get and Set the blink value of the POWER LED with negative input</test_objective>
    <test_type>Negative(Boundary Condition)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
FrontPanelConfig::getInstance()
FrontPanelConfig::getIndicator(string)
FrontPanelConfig::setBlink(int)
FrontPanelConfig::getBlink()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>getIndicator : string – name 
Eg:name: “POWER”
setBlink : int – blink
E.g.: -1,-2</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get Blink interval of front panel indicator LED.
3.Device_Settings_Agent will set Blink interval to “blink ” of front panel indicator LED.
4.Device_Settings_Agent will get  Blink interval of front panel indicator LED.
5.TM compares the Blink Interval before and after setting the Interval and returns SUCCESS or FAILURE status to Test Agent .</automation_approch>
    <except_output>
Checkpoint 1.Check for the error in setting blink value of POWER Indicator for invalid value.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setBlink
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetBlink_Invalid_test_39</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_39');
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
                #calling Device Settings - setBlink and getBlink APIs with invalid value
                tdkTestObj = obj.createTestStep('DS_SetBlink');
                # setting scroll class parameters values
                blink_interval = -1;
                print "Blink interval value set to:%d" %blink_interval; 
                blink_iteration = -2;
                print "Blink iteration value set to:%d" %blink_iteration;
                tdkTestObj.addParameter("blink_interval",blink_interval);
                tdkTestObj.addParameter("blink_iteration",blink_iteration);
                expectedresult="FAILURE"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                blinkdetails = tdkTestObj.getResultDetails();
                blinkinterval="%s" %blink_interval;
                blinkiteration="%s" %blink_iteration;
                #Check for SUCCESS/FAILURE return value of DS_SetBlink
                print blinkdetails;
                if expectedresult in actualresult:
                        print "SUCCESS :Failed to get and set the blink rate";
                        
                        #comparing the blink paramaters before and after setting
                        if ((blinkinterval in blinkdetails)and(blinkiteration in blinkdetails)):
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the blink rates are same";                                
                        else:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the blink rates are not same";                                
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "getblink %s" %blinkdetails;
                        print "Failure: Application successfully gets and sets blink rate for LED";
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
