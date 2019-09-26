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
  <name>XUPNP_GetDevType</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>XUPNP_GetUpnpResult</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To get the device type from  xdiscovery process.
Testcase ID: CT_XUPNP_47</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_XUPNP_47</test_case_id>
    <test_objective>To get the device type value from  xdiscovery process.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.start_upnp.sh should be started.
2.Process xcal-device and xdiscovery should be running on GW Box and xdiscovery should be running on IPClient Box</pre_requisite>
    <api_or_interface_used>ARM_Bus_Init : 
(test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_Call(IARM_BUS_XUPNP_API_GetXUPNPDeviceInfo)
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</api_or_interface_used>
    <input_parameters>string paramName = DevType</input_parameters>
    <automation_approch>1.TM loads xupnp_agent via the test agent. 
2.The stub will invokes the RPC method for checking the parameter name in xupnp result resturned from IARM_Bus call and send the results.
3. The stub function will verify the parameter name in xupnp result and  sends the results as Json response 
4. TM will receive and display the result.</automation_approch>
    <expected_output>Checkpoint 1 stub will parse for parameter name in xupnp result.</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_XUPNP_GetUpnpResult</test_stub_interface>
    <test_script>XUPNP_GetDevType</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
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
iarmObj.configureTestCase(ip,port,'XUPNP_GetDevType');
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
                        xUpnpObj = tdklib.TDKScriptingLibrary("xupnp","2.0");
                        xUpnpObj.configureTestCase(ip,port,'XUPNP_GetDevType');
                        #Get the result of connection with test component and STB
                        xupnpLoadStatus = xUpnpObj.getLoadModuleResult();
                        print "XUPNP module loading status : %s" %xupnpLoadStatus;
                        #Set the module loading status
                        xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

                        if "SUCCESS" in xupnpLoadStatus.upper():
                                tdkTestObj = xUpnpObj.createTestStep('XUPNP_GetUpnpResult');
                                expectedresult="SUCCESS";
                                #Configuring the test object for starting test execution
                                tdkTestObj.addParameter("paramName","DevType");
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                details = details.replace('\\','') 
				details = details.replace('\"','')
				details_list = details.split(',')
				for detail in details_list:
					if detail.split(':')[0]!= 'DevType':
						details_list.remove(detail)
                                print "GetDevType Result : %s"%actualresult;
                                print "GetDevType Details : %s"%str(details_list);
                                #Check for SUCCESS return value of XUPNP_GetUpnpResult
                                if "SUCCESS" in actualresult.upper():
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                #Unload xupnp module
                                xUpnpObj.unloadModule("xupnp");

                        #Calling IARM_Bus_DisConnect API
                        result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
                #calling IARMBUS API "IARM_Bus_Term"
                result = IARMBUS_Term(iarmObj,"SUCCESS")
        #Unload iarmbus module
        iarmObj.unloadModule("iarmbus");

