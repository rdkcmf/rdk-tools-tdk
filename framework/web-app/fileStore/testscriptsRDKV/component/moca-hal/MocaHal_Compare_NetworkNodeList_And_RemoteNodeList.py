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
  <version>2</version>
  <name>MocaHal_Compare_NetworkNodeList_And_RemoteNodeList</name>
  <primitive_test_id/>
  <primitive_test_name>MocaHal_GetRemoteNodeIds</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To verify that remote node list contains all node ids as in network node list except self node id</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
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
    <test_case_id>CT_MOCA_HAL_36</test_case_id>
    <test_objective>To verify that remote node list contains all node ids as in network node list except self node id</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>1.Initialize the moca handle
RMH_Initialize(NULL, NULL);
2.Destroy the moca handle at the end of the test.</pre_requisite>
    <api_or_interface_used>SoC_IMPL__RMH_Network_GetRemoteNodeIds,api SoC_IMPL__RMH_Network_GetNodeIds</api_or_interface_used>
    <input_parameters>[in]	handle	The RMH handle as returned by RMH_Initialize.
[out]	response	List of node IDs.</input_parameters>
    <automation_approch>1. TM loads the Moca hal agent via the test agent.
2. Moca hal agent will invoke the api SoC_IMPL__RMH_Network_GetRemoteNodeIds
3. Moca hal agent will invoke the api SoC_IMPL__RMH_Network_GetNodeIds
4. Verify that the remote node list contains all elements in network node list except self node id and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API calls return value
Checkpoint 2 Verify that the remote node list contains all elements in network node list except self node id </expected_output>
    <priority>High</priority>
    <test_stub_interface>libmocahalstub.so</test_stub_interface>
    <test_script>MocaHal_Compare_NetworkNodeList_And_RemoteNodeList</test_script>
    <skipped>No</skipped>
    <release_version>M71</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
mocahalObj = tdklib.TDKScriptingLibrary("mocahal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
mocahalObj.configureTestCase(ip,port,'MocaHal_Compare_NetworkNodeList_And_RemoteNodeList');

#Get the result of connection with test component and STB
mocaLoadStatus =mocahalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %mocaLoadStatus;
mocahalObj.setLoadModuleStatus(mocaLoadStatus.upper());

if "SUCCESS" in mocaLoadStatus.upper():
    expectedresult="SUCCESS"
    #Prmitive test case which associated to this Script
    #Get remote node list 
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

        #Get network node list
        tdkTestObj = mocahalObj.createTestStep('MocaHal_GetNetworkNodeIds');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "RESULT: Network NodeIds : " , actualresult
        nwNodeList = tdkTestObj.getResultDetails().split(',');
        print "DETAILS: Network NodeIds : " , nwNodeList

        if expectedresult in actualresult and nwNodeList:
            #Get Self node id
            tdkTestObj = mocahalObj.createTestStep('MocaHal_GetNodeId');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            print "RESULT: Self NodeId : " , actualresult
            selfNodeId = tdkTestObj.getResultDetails();
            print "DETAILS: Self NodeId : " , selfNodeId
            if expectedresult in actualresult and selfNodeId:
                tdkTestObj.setResultStatus("SUCCESS")
                print "Self node id retrieved" 
		diffList = list(set(nwNodeList) - set(remoteNodeList))
                print "Difference List: ", diffList
                if diffList == [selfNodeId]:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "Remote node list and network node list are same except the self node id"
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print "Remote node list and network node list difference is not self node id"

            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "Self node id not retrieved" 

        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Network  NodeIds not retrieved" 

    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "Remote NodeIds not retrieved" 

    mocahalObj.unloadModule("mocahal");

else:
    print "Failed to load moca hal module\n";

