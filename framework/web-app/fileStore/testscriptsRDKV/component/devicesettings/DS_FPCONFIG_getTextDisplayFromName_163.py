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
  <version>1</version>
  <name>DS_FPCONFIG_getTextDisplayFromName_163</name>
  <primitive_test_id/>
  <primitive_test_name>DS_FPCONFIG_getTextDisplayFromName</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: This API gets the FrontPanelTextDisplay instance corresponding to the name parameter, only if the name passed is valid.
Test Case Id: CT_DS_163
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_163</test_case_id>
    <test_objective>This API gets the FrontPanelTextDisplay instance corresponding to the name parameter, only if the name passed is valid.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>FrontPanelTextDisplay &amp;getTextDisplay(const string &amp;name)</api_or_interface_used>
    <input_parameters>string text_name="Text"</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the front panel text instance by text name.
3.Device_Settings_Agent will check if text name retrieved using front panel text instance is same as text name provided.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check if text name retrieved using front panel text instance is same as text name provided</except_output>
    <priority>High</priority>
    <test_stub_interface>none</test_stub_interface>
    <test_script>DS_FPCONFIG_getTextDisplayFromName_163</test_script>
    <skipped>No</skipped>
    <release_version>M27</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_FPCONFIG_getTextDisplayFromName_163');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;

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

                #calling Device Settings - Get Front Panel Get Text Display From Name.
                tdkTestObj = obj.createTestStep('DS_FPCONFIG_getTextDisplayFromName');

                text_input = "Text" 
                tdkTestObj.addParameter("text_name",text_input);
                expectedresult="SUCCESS"
		print " " 
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails()
                print "[DS_FPCONFIG_getTextDisplayFromName RESULT] : %s" %actualresult;
                print "[DS_FPCONFIG_getTextDisplayFromName DETAILS] : %s" %details;

                #Check for SUCCESS/FAILURE return value of DS_FPCONFIG_getTextDisplayFromName
                if expectedresult in actualresult:
	                tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Get DS_FPCONFIG_getTextDisplayFromName";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Get DS_FPCONFIG_getTextDisplayFromName"
			
		print " "
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
