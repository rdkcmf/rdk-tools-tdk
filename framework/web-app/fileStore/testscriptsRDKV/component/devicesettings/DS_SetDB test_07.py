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
  <id>266</id>
  <version>1</version>
  <name>DS_SetDB test_07</name>
  <primitive_test_id>109</primitive_test_id>
  <primitive_test_name>DS_SetAudioDB</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This script will check for setting and getting the audio DB level 
TestCase ID:07</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-3</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_7</test_case_id>
    <test_objective>Device Setting –  Get and Set the db value to be used in a given audio port and get the maximum and minimum db level that can be supported by the port.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
Host::getAudioOutputPort()
AudioOutputPort::setDB(float);
AudioOutputPort::getDB();
AudioOutputPort::getMaxDB()
AudioOutputPort::getMinDB()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>
SetDB: int – newDb
Eg:1.0</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get audio db level used in audio output port. 
3.Device_Settings_Agent will set audio db level used in audio output port to “newDb”. 
4.Device_Settings_Agent will get audio db level used in audio output port. 
5.TM compares the audio level  before and after setting the value of db.</automation_approch>
    <except_output>
Checkpoint 1.Check for the value of audio db value before and after setting the value.
</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_setDB
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetDB test_07</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_07');
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
                #calling DS_SetDB to set the audio DB level for the given audio port 
                dblevel=1.120000;
                print "Db level value set to %f" %dblevel; 
                tdkTestObj = obj.createTestStep('DS_SetAudioDB');
                tdkTestObj.addParameter("port_name","HDMI0");
                tdkTestObj.addParameter("db_level",dblevel);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                dbdetails = tdkTestObj.getResultDetails();
                setdb="%s" %dblevel;
                #Check for SUCCESS/FAILURE return value of DS_SetDB
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully sets and gets DB level";
                        print "getdb %s" %dbdetails.upper();
                        #comparing audio DB before anf after setting 
                        if setdb in dbdetails:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Both the audio dbs are same ";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Both the audio dbs are not same ";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Application failed to set and get DB level ";
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
