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
  <version>8</version>
  <name>DTCP_GetNumSess_InvalidType_15</name>
  <primitive_test_id/>
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>To retrieve the total number of active sessions for an invalid device type.
TestType: Negative
TestcaseID: CT_DTCP_15</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DTCP_15</test_case_id>
    <test_objective>To retrieve the total number of active sessions for an invalid device type.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>DTCPMgrInitialize</pre_requisite>
    <api_or_interface_used>int DTCPMgrGetNumSessions(DTCPDeviceType deviceType);</api_or_interface_used>
    <input_parameters>deviceType':3</input_parameters>
    <automation_approch>1.TM loads DTCP_agent via the test agent. 
2.The stub will invokes the RPC method for to stop active session.
3. The stub function will call the API and result will be shared back to TM
4. TM will receive and display the result.</automation_approch>
    <except_output>Checkpoint 1 stub will check for the return value of the function.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DTCP_Test_Execute</test_stub_interface>
    <test_script>DTCP_GetNumSess_InvalidType_15</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from dtcp import init,getNumSessions;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dtcp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DTCP_GetNumSess_InvalidType_15');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('DTCP_Comp_Test');

  expectedresult="SUCCESS";
  #Pre-Cond: DTCPMgrInit
  init(tdkTestObj,expectedresult)
  #Calling DTCPMgrGetNumSessions for Invalid device Types
  getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':3})

  #Unload the dtcp module
  obj.unloadModule("dtcp");
else:
  print"DTCP module load failed";
