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
  <id>653</id>
  <version>1</version>
  <name>DS_SetEncoding_STRESS_test_108</name>
  <primitive_test_id>81</primitive_test_id>
  <primitive_test_name>DS_SetEncoding</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test is to successfully change the Encoding format  continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_108</synopsis>
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
    <test_case_id>CT_DS_108</test_case_id>
    <test_objective>Device Setting –  Get and set the supporting encoding format continuously for every 100ms repeatedly for x times.</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
Host::getAudioOutputPort()
AudioOutputPort::getSupportedEncodings()
AudioOutputPort::getEncoding()
AudioOutputPort::setEncoding(int)
AudioOutputPort::setEncoding(string)
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>setEncoding : string
E.g.: AC3
setEncoding : int – id
E.g.: 1</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the supported encoding formats.
3.Device_Settings_Agent will get the current encoding format.
4.Device_Settings_Agent will set new encoding format.
5.Device_Settings_Agent will get the current encoding format.
6.Device_Settings_Agent will check the current encoding format with new encoding format set.
7.Device_Settings_Agent will wait for 100 ms and change to another encoding format and verify the change.
8.The steps 3-7 will be repeated for 100 times and check the successful change of encoding format and store the result.
9.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step(8th).
</automation_approch>
    <except_output>
Checkpoint 1. Check the encoding format before and after setting it.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_getSupportedEncodings
TestMgr_DS_AOP_setEncoding
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetEncoding_STRESS_test_108</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_108');
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
                        #calling DS_SetEncoding to get and set the encoding
                        tdkTestObj = obj.createTestStep('DS_SetEncoding');
                        encoding="AC3";
                        print "Encoding value set to:%s" %encoding; 
                        tdkTestObj.addParameter("encoding_format",encoding);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        encodingdetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetEncoding
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully get and set the encoding";
                                print "getencoding: %s" %encodingdetails;
                                # comparing the encoding detail before and after setting
                                if encoding in encodingdetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the encoding formats are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the encoding formats are not same";
                                        print "****************%d" %i;
                        time.sleep(100/1000)
                        #calling DS_SetEncoding to get and set the encoding
                        tdkTestObj = obj.createTestStep('DS_SetEncoding');
                        encoding="PCM";
                        print "Encoding value set to:%s" %encoding; 
                        tdkTestObj.addParameter("encoding_format",encoding);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        encodingdetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetEncoding
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully get and set the encoding";
                                print "getencoding: %s" %encodingdetails;
                                # comparing the encoding detail before and after setting
                                if encoding in encodingdetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the encoding formats are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the encoding formats are not same";
                                        print "****************%d" %i;
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
                #tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE :Application failed to set and get the encoding formats";
                print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
