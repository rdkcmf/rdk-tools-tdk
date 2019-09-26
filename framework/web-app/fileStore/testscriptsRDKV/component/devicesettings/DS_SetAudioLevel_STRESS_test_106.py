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
  <id>650</id>
  <version>1</version>
  <name>DS_SetAudioLevel_STRESS_test_106</name>
  <primitive_test_id>110</primitive_test_id>
  <primitive_test_name>DS_SetAudioLevel</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test is to successfully change Audio level continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_106</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
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
    <test_case_id>CT_DS_106</test_case_id>
    <test_objective>Device Setting – Get and Set the random  audio level continuously for every 100ms repeatedly for x times.</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>
device::Manager::Initialize()
Host::getVideoOutputPort()
Host::getAudioOutputPort()
AudioOutputPort::setLevel(float)
AudioOutputPort::getLevel();
device::Manager::DeInitialize()


</api_or_interface_used>
    <input_parameters>
SetLevel: float – newLevel
Eg: value is 100.000</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get audio level. 
3.Device_Settings_Agent will set audio level to “newLevel”.
4. Device_Settings_Agent will get audio level.
5.Device_Settings_Agent will wait for 100 ms and change to another audio level and verify the change.
6. The steps 3-5 will be repeated for 100 times and check the successful change of  audio level and store the result.
7.TM compares the audio level  before and after setting the value of level.</automation_approch>
    <except_output>
Checkpoint 1.Check for the value of audio level before and after setting the value.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_setLevel
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetAudioLevel_STRESS_test_106</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_106');
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
                for i in range(0,100):
                        print "****************%d" %i;
                        #calling Device Settings - setLevel and getLevel APIs
                        tdkTestObj = obj.createTestStep('DS_SetAudioLevel');
                        #setting audio level parameter
                        audiolevel=4.32;
                        print "Audio level value set to:%d" %audiolevel;
                        tdkTestObj.addParameter("audio_level",audiolevel);
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        leveldetails = tdkTestObj.getResultDetails();
                        setlevel = "%s" %audiolevel;
                        #Check for SUCCESS/FAILURE return value of DS_SetLevel
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the audio level";
                                #print "setlevel %s" %setlevel;
                                print "getlevel %s" %leveldetails;
                                #comparing audio level before and after setting
                                if setlevel in leveldetails :
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the audio levels are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the audio levels are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "Failure: Failed to get and set audio level";
                        time.sleep(100/1000);
                        #calling Device Settings - setLevel and getLevel APIs
                        tdkTestObj = obj.createTestStep('DS_SetAudioLevel');
                        #setting audio level parameter
                        audiolevel=6.32;
                        print "Audio level value set to:%d" %audiolevel;
                        tdkTestObj.addParameter("audio_level",audiolevel);
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        leveldetails = tdkTestObj.getResultDetails();
                        setlevel = "%s" %audiolevel;
                        #Check for SUCCESS/FAILURE return value of DS_SetLevel
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the audio level";
                                #print "setlevel %s" %setlevel;
                                print "getlevel %s" %leveldetails;
                                #comparing audio level before and after setting
                                if setlevel in leveldetails :
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the audio levels are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the audio levels are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "Failure: Failed to get and set audio level";
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
