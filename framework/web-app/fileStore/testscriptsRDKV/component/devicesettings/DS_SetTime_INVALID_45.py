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
  <id>659</id>
  <version>1</version>
  <name>DS_SetTime_INVALID_45</name>
  <primitive_test_id>80</primitive_test_id>
  <primitive_test_name>DS_SetTime</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Sets and gets an Invalid Time in the text display of given Front panel Indicator
Test Case ID : CT_DS_45  NOTE: This test fails due to bug in DS component.</synopsis>
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
    <test_case_id>CT_DS_45</test_case_id>
    <test_objective>Device Setting – Get and Set the Time by passing invalid value.</test_objective>
    <test_type>Negative(Boundary Condition)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()   
FrontPanelConfig::getInstance()
FrontPanelConfig::getCurrentTimeForamt() 
FrontPanelConfig::setTimeFormat(int)
FrontPanelConfig::setTime()
Device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>
setTimeFormat : int id 
E.g.: id: 5.
SetTime : int – hrs, int – mins
</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get the Time format displayed in the front panel 
3.Device_Settings_Agent will get Time format in the front panel.
4.Device_Settings_Agent will set a new time by passing “hrs” and “mins” value.
5.TM makes RPC calls for getting the Time format from Device_Settings_Agent and verify whether the format has changed.
6.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step(5th)</automation_approch>
    <except_output>
Checkpoint 1.Check for the Time format in the Front panel after and before setting the format.

Checkpoint 2. Check for the return value of setTime </except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setTime
TestMgr_DS_FP_setTimeForamt

TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetTime_INVALID_45</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_45');
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
                tdkTestObj = obj.createTestStep('DS_SetTime');
                #setting time 
                hrs = 30;
                print "Hours value set to:%d" %hrs;
                mins = 65;
                print "Minutes value set to:%d" %mins; 
                tdkTestObj.addParameter("time_hrs",hrs);
                tdkTestObj.addParameter("time_mins",mins);
                expectedresult="FAILURE";
                tdkTestObj.executeTestCase(expectedresult);
                #time="%s" %time;
                actualresult = tdkTestObj.getResult();
                #Check for FAILURE return value of DS_SetTime
                if expectedresult in actualresult:
                        print "SUCCESS :Failed to get and set the Invalid time";
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Application successfully gets and sets the Invalid time";    
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
        #Set the module loading status
        print"Load module failed";
