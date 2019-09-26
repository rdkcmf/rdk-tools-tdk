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
  <id>1554</id>
  <version>3</version>
  <name>TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionMode_78</name>
  <primitive_test_id>585</primitive_test_id>
  <primitive_test_name>Tr069_Get_Profile_Parameter_Values</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective : To fetch resolution mode of the HDMI output by querying tr69Hostif through curl. 
Query string "Device.Services.STBService.1.Components.HDMI.1.ResolutionMode".	
Test Case ID: CT_TR69_78.
Test Case Type:  Positive.</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TR69_78</test_case_id>
    <test_objective>To fetch resolution mode of the HDMI output by querying tr69Hostif through curl. 
Query string "Device.Services.STBService.1.Components.HDMI.1.ResolutionMode".
No set operation avaliable for this parameter.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>HDMI Cable as to be connected  from XI3 STB to TV.</pre_requisite>
    <api_or_interface_used>curl -d '{"paramList" : [{"name" : "Device.Services.STBService.1.Components.HDMI.1.ResolutionMode”}]}' http://127.0.0.1:10999</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. TM loads tr69Test agent via the test agent.
2. Tr69Test agent will frame the curl request message 
"Device.Services.STBService.1.Components.HDMI.1.ResolutionMode" to resolution mode of the HDMI output.
3. Tr69Test agent will get the curl response which be a valid string value “Auto/Manual” on SUCCESS.
4. If tr69Test agent will get the empty curl response if FAILURE.
5. TM Unloads tr69Test agent.</automation_approch>
    <except_output>Checkpoint 1. Need to get valid string value on SUCCESS. Empty on FAILURE.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtr69stub.so</test_stub_interface>
    <test_script>TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionMode_78</test_script>
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
obj.configureTestCase(ip,port,'TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionMode_78');

#Get the result of connection with test component and STB
loadStatusResult =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatusResult;

loadStatusExpected = "SUCCESS"

if loadStatusExpected not in loadStatusResult.upper():
        print "[Failed To Load Tr069 Module]"
        print "[Exiting the Script]"
        exit();

#Parameter is the profile path to be queried
profilePath = "Device.Services.STBService.1.Components.HDMI.1.ResolutionMode"

actualresult,tdkTestObj,details = tdklib.Create_ExecuteTestcase(obj,'Tr069_Get_Profile_Parameter_Values', 'SUCCESS',verifyList ={},path = profilePath);

if "\"" in details:
        details = details[2:-1]

if 0 == len(details):
        print "[TEST EXCEUTION DETAILS] : [%sEmpty]"%details;
        print "[PRE-REQUSITE] Please!!!! Connect the HDMI Cable from STB to TV to fetch the value before testing";
        tdkTestObj.setResultStatus("FAILURE");
else:
        print "[TEST EXCEUTION DETAILS] : %s"%details;
        expectedOutput = ["Auto","Manual"]
        print "[EXPECTED VALUES] : ",expectedOutput
        if details in expectedOutput:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");

obj.unloadModule("tr069module");
