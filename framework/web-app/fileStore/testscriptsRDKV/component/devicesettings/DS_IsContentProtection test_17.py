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
  <id>255</id>
  <version>3</version>
  <name>DS_IsContentProtection test_17</name>
  <primitive_test_id>101</primitive_test_id>
  <primitive_test_name>DS_IsContentProtected</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script checks for Content Protection support of Video Output Port
Test Case ID : CT_DS_17</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_17</test_case_id>
    <test_objective>Device Setting –  check for Content Protection status in the port.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
VideoOutputPort::isContentProtected()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>null</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will check for content protection support(either true/false) for the given port
3.Device_Settings_Agent will return SUCCESS or FAILURE based on the result. 
</automation_approch>
    <except_output>Checkpoint 1. Check the  content protection support for the given port.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_VOP_isContentProtected
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_IsContentProtection test_17</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from devicesettings import dsManagerInitialize,dsManagerDeInitialize;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load module to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'CT_DS_17');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Initialize Device Settings
        result = dsManagerInitialize(obj)
        #Check for return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check if Content is Protected
                tdkTestObj = obj.createTestStep('DS_IsContentProtected')
                tdkTestObj.addParameter("port_name",'HDMI0')
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult)
                actualresult = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,actualresult)
                print "Details: [%s]"%details
                #Check for return value of DS_IsContentProtected
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS")
                else:
                        tdkTestObj.setResultStatus("FAILURE")
                #calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(obj)
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
