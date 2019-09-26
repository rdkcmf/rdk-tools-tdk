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
  <version>1</version>
  <name>MocaHal_Set_andGet_Enabled</name>
  <primitive_test_id/>
  <primitive_test_name>MocaHal_SetEnabled</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check whether moca hal is enabled successfully</synopsis>
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
    <test_case_id>CT_MOCA_HAL_02</test_case_id>
    <test_objective>To check whether moca hal is enabled successfully</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>1.Initialize the moca handle
RMH_Initialize(NULL, NULL);
2.Destroy the moca handle at the end of the test.</pre_requisite>
    <api_or_interface_used>bool MocaHal_SetEnabled(rmh handle,&amp;response);
bool MocaHal_GetEnabled(rmh handle,&amp;response);</api_or_interface_used>
    <input_parameters>MocaHal_SetEnabled -  with parameter true
MocaHal_GetEnabled</input_parameters>
    <automation_approch>1. TM loads the Moca hal agent via the test agent.
2 .Moca hal agent will invoke the api   SoC_IMPL__RMH_Self_SetEnabled  with parameter true
3. Veirfy the enable status using SoC_IMPL__RMH_Self_SetEnabled api.
4.Based on the the values are same and return SUCCESS/FAILURE status.</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
Checkpoint 2 Verify the enable status is true.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmocahalstub.so</test_stub_interface>
    <test_script>MocaHal_Set_andGet_Enabled</test_script>
    <skipped>No</skipped>
    <release_version/>
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
mocahalObj.configureTestCase(ip,port,'MocaHal_Set_andGet_Enabled');

#Get the result of connection with test component and STB
mocaLoadStatus =mocahalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %mocaLoadStatus;
mocahalObj.setLoadModuleStatus(mocaLoadStatus.upper());

if "SUCCESS" in mocaLoadStatus.upper():

   #Prmitive test case which associated to this Script
   expectedresult="SUCCESS"
   tdkTestObj = mocahalObj.createTestStep('MocaHal_SetEnabled');
   tdkTestObj.addParameter("enable",1);
   #Execute the test case in STB
   tdkTestObj.executeTestCase(expectedresult);
   actualresult = tdkTestObj.getResult();
   print "RESULT: SetEnabled : " , actualresult

   tdkTestObj = mocahalObj.createTestStep('MocaHal_GetEnabled');
   #Execute the test case in STB
   tdkTestObj.executeTestCase(expectedresult);
   actualresult = tdkTestObj.getResult();
   print "RESULT: Getenabled : " , actualresult
   enabled = tdkTestObj.getResultDetails();
   print "DETAILS: GetEnabled : " , enabled

   if "true" in enabled :
       print "Moca has enabled successfully"
       tdkTestObj.setResultStatus("SUCCESS")
   else:
       print "Moca has NOT enabled"
       tdkTestObj.setResultStatus("FAILURE")

   mocahalObj.unloadModule("mocahal");

else:
    print "Failed to load moca hal module\n";
    #Set the module loading status
    mocahalObj.setLoadModuleStatus("FAILURE");
