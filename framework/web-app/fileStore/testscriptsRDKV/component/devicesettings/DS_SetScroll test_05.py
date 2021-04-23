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
  <id>196</id>
  <version>1</version>
  <name>DS_SetScroll test_05</name>
  <primitive_test_id>84</primitive_test_id>
  <primitive_test_name>DS_SetScroll</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Sets and gets the scroll information of given Front panel Indicator
Test Case ID : CT_DS_05</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_5</test_case_id>
    <test_objective>Device Setting –  Get and Set the  information for scroll</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()                                 FrontPanelConfig::getInstance()
FrontPanelConfig::getTextDisplay(String)
FrontPanelConfig::getScroll();
FrontPanelConfig::setScroll(Scroll);
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>getTextDisplay : string  “TEXT”  
SetScroll : Scroll - object for Scroll class</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get scroll details.
3.Device_Settings_Agent will set scroll details to “Scroll object”.
4.Device_Settings_Agent will get scroll details.
5.TM compares the scroll details(iteration and duration) before and after setting the value of iteration and duration.</automation_approch>
    <except_output>
Checkpoint 1.Check for the scroll value of Text Display before and after setting the value.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setScroll
TestMgr_DS_managerDeinitialize
</test_stub_interface>
    <test_script>DS_SetScroll test_05</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_5');
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
            tdkTestObj = obj.createTestStep('DS_FP_enableDisplay');
            #Disable clock display by setting enable = 0 before calling setScroll
            enable = 0
            print "Value given to enable/disable display : ", enable
            tdkTestObj.addParameter("enable", enable);
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "[TEST EXECUTION RESULT] : %s" %actualresult;
            print "Details: [%s]"%details;
            #Set the result status of execution
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");

                #calling Device Settings - setScroll and getScroll APIs
                tdkTestObj = obj.createTestStep('DS_SetScroll');
                #setting scroll class parameters
                viteration=2;
                print "Viteration set to:%d" %viteration;
                hiteration=4;
                print "Hiteration set to:%d" %hiteration;
                hold_duration=6;
                print "Hold value set to:%d" %hold_duration;
                tdkTestObj.addParameter("viteration",viteration);
                tdkTestObj.addParameter("hiteration",hiteration);
                tdkTestObj.addParameter("hold_duration",hold_duration);
                tdkTestObj.addParameter("text","Text");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                scrolldetails = tdkTestObj.getResultDetails();
                str_viteration="%s" %viteration;
                str_hiteration="%s" %hiteration;
                str_hold_duration="%s" %hold_duration;
                #Check for SUCCESS/FAILURE return value of DS_SetScroll
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully gets and sets the blink rate";
                        print "getScroll %s" %scrolldetails;
                        #comparing the scroll parameters before and after setting
                        if ((str_viteration in scrolldetails)and(str_hiteration in scrolldetails)and(str_hold_duration in scrolldetails)):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the scroll details are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the scroll details are not same";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failure: Failed to get and set scroll details";
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
                print "FAILURE : Clock disable failed";
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
