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
  <id>1591</id>
  <version>3</version>
  <name>DS_SetState_Stress_115</name>
  <primitive_test_id>656</primitive_test_id>
  <primitive_test_name>DS_SetState</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check too frequent calls (50 times) to Front Panel SetState.
Test case ID: CT_DS115</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS115</test_case_id>
    <test_objective>Check too frequent calls (50 times) to FP setState</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize() 
device::FrontPanelIndicator::setState
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>integer state(0,1)
string indicator_name ("Power")</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2. Device_Settings_Agent will set the state of front panel to ON/OFF for 50 times.
3. Device_Settings_Agent will check for the state after each set will return SUCCESS or FAILURE</automation_approch>
    <except_output>Checkpoint 1 Check for return value of the state in each loop</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setState
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetState_Stress_115</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>MOT7425-6090 </remarks>
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
obj.configureTestCase(ip,port,'DS_SetState_Stress_115');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");
    indicator_name = "Power";
    print "Indicator name: %s" %indicator_name;
    # Repeat setState change for 50 times
    for x in range(0,50):
        # Toggle between state values 0 and 1
        for state in range(0,2):
            #calling Device Settings - initialize API
            tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            print "[DS Initialize RESULT] : %s" %actualresult;
            #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                #calling Device Settings - Set state
                tdkTestObj = obj.createTestStep('DS_SetState');
                #setting state parameter value
                print "Setting State to %d" %state;
                tdkTestObj.addParameter("state",state);
                tdkTestObj.addParameter("indicator_name",indicator_name);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS SetState RESULT] : %s" %actualresult;
                stateDetails = tdkTestObj.getResultDetails();
                print "SetState Details: %s"%stateDetails;
                #Check for SUCCESS/FAILURE return value of DS_SetState
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
        #End of for loop for state toggle
    #End of for loop for 50 times

    #Unload the deviceSettings module
    obj.unloadModule("devicesettings");
else:
    print"Load module failed";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
