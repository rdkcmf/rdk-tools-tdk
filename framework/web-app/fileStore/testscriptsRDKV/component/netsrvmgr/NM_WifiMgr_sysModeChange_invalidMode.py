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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>NM_WifiMgr_sysModeChange_invalidMode</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>NetSrvMgr_WifiMgr_SetGetParameters</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective:To change mode of wifi manager to invalid mode
Test CaseID:CT_NM_26
Test Type: Negative</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
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
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_NM_26</test_case_id>
    <test_objective>Objective:To change mode of wifi manager to invalid mode</test_objective>
    <test_type>Negative</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1. netSrvMgr should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init (test agent process_name)
IARM_Bus_Connect()
IARM_Bus_Call(IARM_BUS_COMMON_API_SysModeChange)
IARM_Bus_Disconnect()
IARM_Bus_Term</api_or_interface_used>
    <input_parameters>char* - methodName
int - new_mode</input_parameters>
    <automation_approch>1. TM loads the NetSrvMgr_Agent via the test agent.
2.NetSrvMgr_Agent should fail on trying to change the wifi manager to invalid mode
3.NetSrvMgr_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1.Mode of wifi manager should not be changed to invalid mode</except_output>
    <priority>High</priority>
    <test_stub_interface>libnetsrvmgrstub.so</test_stub_interface>
    <test_script>NM_WifiMgr_sysModeChange_invalidMode</test_script>
    <skipped>No</skipped>
    <release_version>M48</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from iarmbus import IARMBUS_Init,IARMBUS_Connect,IARMBUS_DisConnect,IARMBUS_Term;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
iarmObj.configureTestCase(ip,port,'NM_WifiMgr_sysModeChange');
#Get the result of connection with test component and STB
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "Iarmbus module loading status : %s" %iarmLoadStatus ;
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);

if "SUCCESS" in iarmLoadStatus.upper():
        #Calling IARMBUS API "IARM_Bus_Init"
        result = IARMBUS_Init(iarmObj,"SUCCESS")
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if "SUCCESS" in result:
                #Calling IARMBUS API "IARM_Bus_Connect"
                result = IARMBUS_Connect(iarmObj,"SUCCESS")
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if "SUCCESS" in result:
                        #Test component to be tested
                        netsrvObj = tdklib.TDKScriptingLibrary("netsrvmgr","1");
                        netsrvObj.configureTestCase(ip,port,'NM_WifiMgr_sysModeChange');

                        #Get the result of connection with test component and STB
                        netsrvLoadStatus =netsrvObj.getLoadModuleResult();
                        print "[LIB LOAD STATUS]  :  %s" %netsrvLoadStatus;
                        #Set the module loading status
                        netsrvObj.setLoadModuleStatus(netsrvLoadStatus);

                        if "SUCCESS" in netsrvLoadStatus.upper():
                        	#Prmitive test case which associated to this Script
                        	tdkTestObj = netsrvObj.createTestStep('NetSrvMgr_WifiMgr_SetGetParameters');

                                #Execute the test case in STB
                                tdkTestObj.addParameter("method_name", "SysModeChange");
                                tdkTestObj.addParameter("new_mode",3);
                                expectedresult="FAILURE"
                        	tdkTestObj.executeTestCase(expectedresult);

                        	#Get the result of execution
                        	actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                        	print "[TEST EXECUTION RESULT] : %s" %actualresult;
                                print "Details: [%s]"%details;

                                #Set the result status of execution
                        	if expectedresult in actualresult:
                        	        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                netsrvObj.unloadModule("netsrvmgr");
                        	
                        else :
                        	print "Failed to Load netsrvmgr Module "

                        #Calling IARM_Bus_DisConnect API
                        result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
                #calling IARMBUS API "IARM_Bus_Term"
                result = IARMBUS_Term(iarmObj,"SUCCESS")
        #Unload iarmbus module
        iarmObj.unloadModule("iarmbus");

else :
        print "Failed to Load iarmbus Module "
