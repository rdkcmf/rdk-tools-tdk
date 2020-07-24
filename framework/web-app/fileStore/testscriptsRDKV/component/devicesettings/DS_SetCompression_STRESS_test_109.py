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
  <id>652</id>
  <version>1</version>
  <name>DS_SetCompression_STRESS_test_109</name>
  <primitive_test_id>78</primitive_test_id>
  <primitive_test_name>DS_SetCompression</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test is to successfully change the Compression format  continuously for every 100ms repeatedly for x times.Test case ID : CT_DS_109</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_109</test_case_id>
    <test_objective>Device Setting –  Get and set  the supported compression format continuously for every 100ms repeatedly for x times.</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>xi6</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
Host::getAudioOutputPort()
AudioOutputPort::getCompression()
AudioOutputPort::setCompression(int)
AudioOutputPort::setCompression(string)
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>SetCompression : Value E.g [1-10]</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the current compression format.
3.Device_Settings_Agent will set new compression format.
4.Device_Settings_Agent will get the current compression format.
5.Device_Settings_Agent will check the current compression format with new compression format set.
6.Device_Settings_Agent will wait for 100 ms and change to another compression format  and verify the change.
7.The steps 3-7 will be repeated for 100 times and check the successful change of compression format and store the result.
8.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step(8th). </automation_approch>
    <except_output>
Checkpoint 1. Check the compression format before and after setting it.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_setCompression
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetCompression_STRESS_test_109</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import random;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_109');
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
        print "SUCCESS :Application successfully initialized with Device Settings library\n";
        for i in range(0,100):
            compression = random.randrange(0,11)
            #calling DS_SetCompression to get and set the compression
            tdkTestObj = obj.createTestStep('DS_SetCompression');
            print "Compression value set to %d" %compression; 
            tdkTestObj.addParameter("compression_format",compression);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            compressiondetails = tdkTestObj.getResultDetails();
            setcompression = "Compression format:%s" %compression;
            #Check for SUCCESS/FAILURE return value of DS_SetCompression
            if expectedresult in actualresult:
                print "SUCCESS :Application successfully get and set the compression";
                print "setcompression: %s" %setcompression;
                print "getcompression: %s" %compressiondetails;
                #comparing compression before and after setting
                if setcompression == compressiondetails:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS: Both the compression formats are same\n";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Both the compression formats are not same\n";
                    break
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE :Application failed to set and get the compression formats\n";
                print "****************%d" %i;
                break
            time.sleep(100/1000);
        #calling DS_ManagerDeInitialize to DeInitialize API
        tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
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
