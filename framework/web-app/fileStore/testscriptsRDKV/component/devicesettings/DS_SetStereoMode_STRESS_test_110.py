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
  <id>654</id>
  <version>1</version>
  <name>DS_SetStereoMode_STRESS_test_110</name>
  <primitive_test_id>85</primitive_test_id>
  <primitive_test_name>DS_SetStereoMode</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test is to successfully change the Stereo Mode continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_110</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
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
    <test_case_id>CT_DS_110</test_case_id>
    <test_objective>Device Setting –  Get and set the supported stereo format continuously for every 100ms repeatedly for x times.</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
Host::getAudioOutputPort()
AudioOutputPort::getSupportedStereoModes()
AudioOutputPort::getStereoMode()
AudioOutputPort::setStereoMode(int)
AudioOutputPort::setStereoMode(string)
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>setStereoMode : string
E.g.: MONO
setStereoMode : int – id
E.g.: 1</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the supported stereo modes.
3.Device_Settings_Agent will get the current stereo format.
4.Device_Settings_Agent will set new stereo format.
5.Device_Settings_Agent will get the current stereo format.
6.Device_Settings_Agent will check the current stereo format with new stereo format set.
7.Device_Settings_Agent will wait for 100 ms and change to another stereo format and verify the change.
8.The steps 3-7 will be repeated for 100 times and check the successful change of stereo format and store the result.
9.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step(8th).</automation_approch>
    <except_output>Checkpoint 1. Check the current stereo mode is present in the list of supported stereo modes.
Checkpoint 2. Check the stereo mode before and after setting it.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_getSupportedStereoModes
TestMgr_DS_AOP_setStereoMode
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetStereoMode_STRESS_test_110</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_110');
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
                #calling DS_GetSupportedStereoModes get list of StereoModes.
                i = 0;
                for i in range(0,100):
                        print "****************%d" %i;
                        #calling DS_SetStereoMode to get and set the stereo modes
                        tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                        stereomode="SURROUND";
                        print "Stereo mode value set to : %s" %stereomode;
                        tdkTestObj.addParameter("stereo_mode",stereomode);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        stereomodedetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully get and set the stereo modes";
                                print "getstereomode: %s" %stereomodedetails;
                                #comparing stereo modes before and after setting
                                if stereomode in stereomodedetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the stereo modes are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the stereo modes are not same";
                        else:           
                                print "****************%d" %i;
                                print "FAILURE :Application failed to set and get the stereo modes";
                        time.sleep(100/1000);
                        #calling DS_SetStereoMode to get and set the stereo modes
                        tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                        stereomode="STEREO";
                        print "Stereo mode value set to: %s" %stereomode;
                        tdkTestObj.addParameter("stereo_mode",stereomode);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        stereomodedetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully get and set the stereo modes";
                                print "getstereomode: %s" %stereomodedetails;
                                #comparing stereo modes before and after setting
                                if stereomode in stereomodedetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the stereo modes are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the stereo modes are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "FAILURE :Application failed to set and get the stereo modes";
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
