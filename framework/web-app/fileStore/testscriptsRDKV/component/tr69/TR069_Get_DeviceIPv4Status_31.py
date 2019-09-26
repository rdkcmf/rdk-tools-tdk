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
  <id>1357</id>
  <version>2</version>
  <name>TR069_Get_DeviceIPv4Status_31</name>
  <primitive_test_id>585</primitive_test_id>
  <primitive_test_name>Tr069_Get_Profile_Parameter_Values</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: To fetch  the status of the IPv4 stack on a device by querying tr69Hostif through curl.  Query string "Device.IP.IPv4Status".  
TestCaseID: CT_TR69_31
TestType: Positive</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TR69_31</test_case_id>
    <test_objective>To fetch  the status of the IPv4 stack on a device by querying tr69Hostif through curl. 
Query string "Device.IP.IPv4Status".</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>No</pre_requisite>
    <api_or_interface_used>curl -d '{"paramList" : [{"name" : "Device.IP.IPv4Status"}]}' http://127.0.0.1:10999</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. TM loads tr69Test agent via the test agent.
2. Tr69Test agent will frame the curl request message 
"Device.IP.IPv4Status." to fetch  the status of the IPv4 stack on a device.
3. Tr69Test agent will get the curl response which be a vaild string “Enabled”, “Disabled” or “Error” on SUCCESS.
4. If tr69Test agent will get the empty curl response if FAILURE.
5. TM Unloads tr69Test agent.</automation_approch>
    <except_output>Checkpoint 1. Need to get valid string “Enabled”,“Disabled” or “Error” on SUCCESS. Empty on FAILURE.
Checkpoint 2. We can cross check the value using ifconfig.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtr69stub.so</test_stub_interface>
    <test_script>TR069_Get_DeviceIPv4Status_31</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tr069module","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TR069_Get_DeviceIPv4Status_31');

#Get the result of connection with test component and STB
loadStatusResult =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatusResult;

loadStatusExpected = "SUCCESS"

if loadStatusExpected not in loadStatusResult.upper():
        print "[Failed To Load Tr069 Module]"
        print "[Exiting the Script]"
        exit();

#Parameter is the profile path to be queried
profilePath = "Device.IP.IPv4Status"

actualresult,tdkTestObj,details = tdklib.Create_ExecuteTestcase(obj,'Tr069_Get_Profile_Parameter_Values', 'SUCCESS',verifyList ={},path = profilePath);

if "\"" in details:
        details = details[2:-1]
print "[TEST EXCEUTION DETAILS] : %s"%details;

if "Empty" not in details: 
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Tr069_Verify_Profile_Parameter_Values');

        expectedResult = "SUCCESS"

        #Parameter is the profile path to be queried
        tdkTestObj.addParameter("path",profilePath)
        tdkTestObj.addParameter("paramValue",details)

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        
        print "Requested Parameter To Verify: ",profilePath
        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        details = tdkTestObj.getResultDetails();
        print "[TEST EXCEUTION DETAILS] : %s"%details;

        tdkTestObj.setResultStatus(result);
else:
        tdkTestObj.setResultStatus(result);

obj.unloadModule("tr069module");
