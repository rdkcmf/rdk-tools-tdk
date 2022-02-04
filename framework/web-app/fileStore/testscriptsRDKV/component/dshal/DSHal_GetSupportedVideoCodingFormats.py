##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <name>DSHal_GetSupportedVideoCodingFormats</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_GetSupportedVideoCodingFormats</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test Script is to check which video formats the SoC supports</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_61</test_case_id>
    <test_objective>Test Script is to check which video formats the SoC supports</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetSupportedVideoCodingFormats(vdHandle, &amp;supportedFormat)</api_or_interface_used>
    <input_parameters>vdHandle -video device handle
supportedFormat - to hold supported Video Coding formats</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the API dsGetSupportedVideoCodingFormats
3.Should get ORed value of STB minimum video coding formats MPEG2 &amp; MPEG4
4. Update test result as SUCCESS/FAILURE based on the API return value
5.Unload the module</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2.supported Video Coding format value should be greater than or equal to 6</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetSupportedVideoCodingFormats</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_GetSupportedVideoCodingFormats');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    print "\nTEST STEP1 : To check video formats the SoC supports using dsGetSupportedVideoCodingFormats API"
    print "EXPECTED RESULT : Should get the OR-ed value of Video formats supported"
    tdkTestObj = obj.createTestStep('DSHal_GetSupportedVideoCodingFormats');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetSupportedVideoCodingFormats call is success"
        print "Value Returned : Supported video coding : ",details

        print "\nTEST STEP2 : Check whether STB supports minimum video coding formats"
        print "EXPECTED RESULT : STB should have minimum compression formats, value >=6"
        if int(details) == 6:
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT : STB supports MPEG2,MPEG4 formats"
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
        elif int(details) >= 6:
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT : STB supports MPEG2,MPEG4,MPEGH(HEVC codec) formats"
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "ACTUAL RESULT : STB's expected minimum formats MPEG2,MPEG4 not retrieved"
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetSupportedVideoCodingFormats call failed"
        print "Value Returned : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("dshal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


