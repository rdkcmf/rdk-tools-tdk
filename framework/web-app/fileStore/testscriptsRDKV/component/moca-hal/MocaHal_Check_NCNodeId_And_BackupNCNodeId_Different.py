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
  <name>MocaHal_Check_NCNodeId_And_BackupNCNodeId_Different</name>
  <primitive_test_id/>
  <primitive_test_name>MocaHal_GetNCNodeId</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check if NC node id and backup NC node id are not same</synopsis>
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
    <test_case_id>CT_MOCA_HAL_32</test_case_id>
    <test_objective>To check if NC node id and backup NC node id are not same</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>1.Initialize the moca handle
RMH_Initialize(NULL, NULL);
2.Destroy the moca handle at the end of the test.</pre_requisite>
    <api_or_interface_used>SoC_IMPL__RMH_Network_GetNCNodeId</api_or_interface_used>
    <input_parameters>[in]	handle	The RMH handle as returned by RMH_Initialize.
[out]	response	The NC's node ID.</input_parameters>
    <automation_approch>1. TM loads the Moca hal agent via the test agent.
2 .Moca hal agent will invoke the api  SoC_IMPL__RMH_Network_GetNCNodeId and SoC_IMPL__RMH_Network_GetBackupNCNodeId
3. Verify that the node ids are retrieved
4.Based on the the values are different or not return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call return value
Checkpoint 2 Verify that the node ids are different</expected_output>
    <priority>High</priority>
    <test_stub_interface>libmocahalstub.so</test_stub_interface>
    <test_script>MocaHal_Check_NCNodeId_And_BackupNCNodeId_Different</test_script>
    <skipped>No</skipped>
    <release_version>M70</release_version>
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
mocahalObj.configureTestCase(ip,port,'MocaHal_Check_NCNodeId_And_BackupNCNodeId_Different');

#Get the result of connection with test component and STB
mocaLoadStatus =mocahalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %mocaLoadStatus;
mocahalObj.setLoadModuleStatus(mocaLoadStatus.upper());

if "SUCCESS" in mocaLoadStatus.upper():
    expectedresult="SUCCESS"
    #Prmitive test case which associated to this Script
    tdkTestObj = mocahalObj.createTestStep('MocaHal_GetNCNodeId');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    print "RESULT: NCNodeId : " , actualresult
    ncNodeId = tdkTestObj.getResultDetails();
    print "DETAILS: NCNodeId : " , ncNodeId

    if expectedresult in actualresult and ncNodeId:
        tdkTestObj.setResultStatus("SUCCESS")
        print "NCNodeId retrieved" , ncNodeId 
        #Prmitive test case which associated to this Script
        tdkTestObj = mocahalObj.createTestStep('MocaHal_GetBackupNCNodeId');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "RESULT: BackupNCNodeId : " , actualresult
        bkNcNodeId = tdkTestObj.getResultDetails();
        print "DETAILS: BackupNCNodeId : " , bkNcNodeId
        
        if expectedresult in actualresult and bkNcNodeId:
            tdkTestObj.setResultStatus("SUCCESS")
            print "BackupNCNodeId retrieved" , bkNcNodeId 
            if int(ncNodeId) != int(bkNcNodeId):
                tdkTestObj.setResultStatus("SUCCESS")
                print "NCNodeId and BackupNCNodeId are not same" 
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "NCNodeId and BackupNCNodeId are same" 
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "BackupNCNodeId not retrieved" 
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "NCNodeId not retrieved" 

    mocahalObj.unloadModule("mocahal");

else:
    print "Failed to load moca hal module\n";

