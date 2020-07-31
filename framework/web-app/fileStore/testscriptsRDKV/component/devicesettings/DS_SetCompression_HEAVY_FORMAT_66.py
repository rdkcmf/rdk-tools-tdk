##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>616</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetCompression_HEAVY_FORMAT_66</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>78</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetCompression</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script Sets and gets the HEAVY Compression Format of Audio Test Case ID : CT_DS_66.Note:This script will return duplicates, If running second time without restarting agent. Agent process may lead to crash/restart.This is an issue with DS.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_66</test_case_id>
    <test_objective>Device Setting –  Get and set  compression format to HEAVY</test_objective>
    <test_type>Positive(Boundary condition)</test_type>
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
    <input_parameters>SetCompression : HEAVY FORMAT value :10</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the current compression format.
3.Device_Settings_Agent will set new compression format.
4.Device_Settings_Agent will get the current compression format.
5.Device_Settings_Agent will check the current compression format with new compression format set.
6.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step(5th).</automation_approch>
    <expected_output>Checkpoint 1. Check the compression format before and after setting it.</expected_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_setCompression
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetCompression_HEAVY_FORMAT_66</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_66');
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
        print "SUCCESS :Application successfully initialized with Device Settings library";
        #calling DS_SetCompression to get and set the compression
        tdkTestObj = obj.createTestStep('DS_SetCompression');
        compression= 10;
        print "Compression Format : HEAVY";
        print "Compression value set to:%d" %compression;
        tdkTestObj.addParameter("compression_format",compression);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        compressiondetails = tdkTestObj.getResultDetails();
        setcompression = "Compression format:%d" %compression;
        #Check for SUCCESS/FAILURE return value of DS_SetCompression
        if expectedresult in actualresult:
            print "SUCCESS :Application successfully get and set the compression";
            print "setcompression: %s" %setcompression;
            print "getcompression: %s" %compressiondetails;
            #comparing compression before and after setting
            if setcompression == compressiondetails:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Both the compression formats are same";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Both the compression formats are not same";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "FAILURE :Application failed to set and get the compression formats";
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
