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
  <id>192</id>
  <version>3</version>
  <name>DS_SetColor test_02</name>
  <primitive_test_id>77</primitive_test_id>
  <primitive_test_name>DS_SetColor</primitive_test_name>
  <primitive_test_version>6</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script Sets and gets the COLOR of given Front panel Indicator
Test Case ID : CT_DS_02</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_2</test_case_id>
    <test_objective>Device Setting – Get and Set the color of the POWER LED</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()                                  FrontPanelConfig::getInstance()
FrontPanelConfig::getColors() 
FrontPanelConfig::getIndicator(string)
FrontPanelConfig::getColor()
FrontPanelConfig::setColor(int)      
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>getIndicator : string – name
E.g.: name : “POWER”
SetColor : int – color
E.g.: 0,1,2,3,4,5</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get the list of colors.
3.Device_Settings_Agent will get a indicator by passing”name:POWER”.
4.Device_Settings_Agent will get the color for POWER Indicator.
5.Device_Settings_Agent will set the new color to “color” for the POWER Indicator.
6. TM makes RPC calls for getting the color of POWER Indicator from Device Settings_stub and verify whether the color has changed.</automation_approch>
    <except_output>

Checkpoint 1.Check for the color of POWER Indicator after and before setting the color.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_FP_getSupportedColors
TestMgr_DS_FP_setColor
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetColor test_02</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_02');
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
                tdkTestObj = obj.createTestStep('DS_GetSupportedColors');
                tdkTestObj.addParameter("indicator_name","Message");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                colordetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedColors
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of supported colors";
                        print "%s" %colordetails
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the color list";
                print "SUCCESS :Application successfully initialized with Device Settings library";
                print "0-Blue";
                print "1-Green";
                print "2-Red";
                print "3-Yellow";
                print "4-Orange";
                tdkTestObj = obj.createTestStep('DS_SetColor');
                #setting color parameter value
                color = 0;
                print "Color value set to:%d" %color;
                indicator = "Power";
                print "Indicator value set to:%s" %indicator;
                tdkTestObj.addParameter("indicator_name",indicator);
                tdkTestObj.addParameter("color",color);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                colordetails = tdkTestObj.getResultDetails();
                setColor = "%s" %color;
                list = ['255','65280','16711680','16777184','16747520']
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully gets and sets the color";
                        print "getColor %s" %colordetails;
                        print "Color to be verified: %s"%list[int(setColor)];
                        #comparing the color before and after setting
                        if list[int(setColor)] in colordetails :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the colors are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the colors are not same";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failure: Failed to get and set color for LED";
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
