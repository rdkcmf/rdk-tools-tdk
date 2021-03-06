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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>MocaHal_Get_RemoteNodes_TxPackets</name>
  <primitive_test_id/>
  <primitive_test_name>MocaHal_RemoteNode_GetTxPackets</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the number of packets transmitted by the remoe node</synopsis>
  <groups_id/>
  <execution_time>1</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_MOCA_HAL_65</test_case_id>
    <test_objective>To get the number of packets transmitted by the remoe node</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>1.Initialize the moca handle
RMH_Initialize(NULL, NULL);
2.Destroy the moca handle at the end of the test.</pre_requisite>
    <api_or_interface_used>SoC_IMPL__RMH_RemoteNode_GetTxPackets</api_or_interface_used>
    <input_parameters>[in]	handle	The RMH handle as preturned by RMH_Initialize.
[in]    nodeId	The node Id of the remote node to inspect	
[out]	response	The number of packets transmitted by the remoe node.</input_parameters>
    <automation_approch>1. TM loads the Moca hal agent via the test agent.
2. Moca hal agent will invoke the api SoC_IMPL__RMH_Network_GetRemoteNodeIds to get list of remote node ids
3. Moca hal agent will invoke the api SoC_IMPL__RMH_RemoteNode_GetTxPackets with each node id
4. Check the api call return value and return SUCCESS/FAILURE status.</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value</except_output>
    <priority>High</priority>
    <test_stub_interface>libmocahalstub.so</test_stub_interface>
    <test_script>MocaHal_Get_RemoteNodes_TxPackets</test_script>
    <skipped>No</skipped>
    <release_version>M72</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
mocahalObj = tdklib.TDKScriptingLibrary("mocahal","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
mocahalObj.configureTestCase(ip,port,'MocaHal_Get_RemoteNodes_TxPackets');

#Get the result of connection with test component and STB
mocaLoadStatus =mocahalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %mocaLoadStatus;
mocahalObj.setLoadModuleStatus(mocaLoadStatus.upper());

if "SUCCESS" in mocaLoadStatus.upper():
    expectedresult="SUCCESS"
    #Prmitive test case to get remote Node Ids
    tdkTestObj = mocahalObj.createTestStep('MocaHal_GetRemoteNodeIds');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    print "RESULT: Remote NodeIds : " , actualresult
    remoteNodeList = tdkTestObj.getResultDetails().split(',');
    print "DETAILS: Remote NodeIds : " , remoteNodeList

    if expectedresult in actualresult and remoteNodeList:
        tdkTestObj.setResultStatus("SUCCESS")
        print "Remote NodeIds retrieved" , remoteNodeList

        for nodeId in remoteNodeList:
            #Prmitive test case to get remote node TxPackets
            tdkTestObj = mocahalObj.createTestStep('MocaHal_RemoteNode_GetTxPackets');
            tdkTestObj.addParameter("nodeId",int(nodeId));
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            print "RESULT: RemoteNode_GetTxPackets : " , actualresult
            txPackets = tdkTestObj.getResultDetails();
            print "DETAILS: RemoteNode_GetTxPackets : " , txPackets

            if expectedresult in actualresult and txPackets:
                tdkTestObj.setResultStatus("SUCCESS")
                print "TxPackets %s retrieved for node id %d" %(txPackets, int(nodeId))
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "TxPackets not retrieved for node id ", int(nodeId)
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "Remote NodeIds not retrieved"

    mocahalObj.unloadModule("mocahal");

else:
    print "Failed to load moca hal module\n";

