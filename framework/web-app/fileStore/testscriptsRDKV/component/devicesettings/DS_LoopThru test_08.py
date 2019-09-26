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
  <id>199</id>
  <version>1</version>
  <name>DS_LoopThru test_08</name>
  <primitive_test_id>67</primitive_test_id>
  <primitive_test_name>DS_LoopThru</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Sets and gets the Loop Thro Configuration of Audio Output Port
Test Case ID : CT_DS_08</synopsis>
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
    <test_case_id>CT_DS_8</test_case_id>
    <test_objective>Device Setting – checking whether the given audio port is configured for loop thro'.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
Host::getAudioOutputPort()
AudioOutputPort::setLoopThru(bool);
AudioOutputPort::IsLoopThru();
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>setLoopThru: bool - loopthru
</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will check for the status of Loop thru functionality.
3. Device_Settings_Agent will set LoopThru functionality of audio port to “loopthru”.
4. Device_Settings_Agent will check for the status of Loop thru functionality of audio port and will return SUCCESS or FAILURE based on the result. 
</automation_approch>
    <except_output>Checkpoint 1. Check the status of LoopThru before and after setting it.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_loopThru
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_LoopThru test_08</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_08');
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
                #calling DS_LoopThru to check audio loop thru for a port.
                loop_thru=1;
                print "LoopThru value set to:%d" %loop_thru;
                tdkTestObj = obj.createTestStep('DS_LoopThru');
                tdkTestObj.addParameter("port_name","HDMI0");
                tdkTestObj.addParameter("loop_thru",loop_thru);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                loopthrudetails = tdkTestObj.getResultDetails();
                setloopthru = "%s" %loop_thru;
                #Check for SUCCESS/FAILURE return value of DS_LoopThru
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully calls setLoopThru";
                        print "1:set 0:not set";
                        print "getloopthru %s" %loopthrudetails;
                        #comparing loopthru status before and after setting
                        if setloopthru in loopthrudetails:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS : setLoopThru and isLoopThru executed successfully";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE : setLoopThru and isLoopThru failed to execute";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Application failed execute setLoopThru ";
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
