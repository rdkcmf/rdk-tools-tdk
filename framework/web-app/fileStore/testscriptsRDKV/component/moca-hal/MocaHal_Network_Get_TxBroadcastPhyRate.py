##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>MocaHal_Network_Get_TxBroadcastPhyRate</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MocaHal_GetTxBroadcastPhyRate</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To get the PHY rate at which broadcast packets are transmitted from the node</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_MOCA_HAL_18</test_case_id>
    <test_objective>To get the PHY rate at which broadcast packets are transmitted from the node</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>1.Initialize the moca handle
RMH_Initialize(NULL, NULL);
2.Destroy the moca handle at the end of the test.</pre_requisite>
    <api_or_interface_used>SoC_IMPL__RMH_Network_GetTxBroadcastPhyRate</api_or_interface_used>
    <input_parameters>[in]	handle	The RMH handle as returned by RMH_Initialize.
[out]	response	The broadcast transmission PHY rate.</input_parameters>
    <automation_approch>1. TM loads the Moca hal agent via the test agent.
2 .Moca hal agent will invoke the api   SoC_IMPL__RMH_Network_GetTxBroadcastPhyRate
3. Verify that the TxBroadcastPhyRate is retrieved
4.Based on the the values are same and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call return value
Checkpoint 2 Verify that theTxBroadcastPhyRate  is retrieved</expected_output>
    <priority>High</priority>
    <test_stub_interface>libmocahalstub.so</test_stub_interface>
    <test_script>MocaHal_Network_Get_TxBroadcastPhyRate</test_script>
    <skipped>No</skipped>
    <release_version>M70</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from time import sleep;

#Test component to be tested
mocahalObj = tdklib.TDKScriptingLibrary("mocahal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
mocahalObj.configureTestCase(ip,port,'MocaHal_Network_Get_TxBroadcastPhyRate');

#Get the result of connection with test component and STB
mocaLoadStatus =mocahalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %mocaLoadStatus;
mocahalObj.setLoadModuleStatus(mocaLoadStatus.upper());

if "SUCCESS" in mocaLoadStatus.upper():
    expectedresult="SUCCESS"
    #Prmitive test case which associated to this Script
    tdkTestObj = mocahalObj.createTestStep('MocaHal_GetTxBroadcastPhyRate');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    print "RESULT: GetTxBroadcastPhyRate : " , actualresult
    phyRate = tdkTestObj.getResultDetails();
    print "DETAILS: GetTxBroadcastPhyRate : " , phyRate
    
    if expectedresult in actualresult and phyRate:
        tdkTestObj.setResultStatus("SUCCESS")
        print "TxBroadcastPhyRate has valid value" , phyRate
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "GetTxBroadcastPhyRate has invalid value"

    mocahalObj.unloadModule("mocahal");

else:
    print "Failed to load moca hal module\n";

