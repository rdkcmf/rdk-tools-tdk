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
  <version>2</version>
  <name>DSHal_GetEDIDBytes</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_GetEDIDBytes</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to get EDID bytes info</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>IPClient-3</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_128</test_case_id>
    <test_objective>Test script to get EDID bytes info for HDMI </test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetDisplay(dsVideoPortType_t type, int index, int *handle)
dsGetEDIDBytes(int handle, unsigned char **edid, int *length)</api_or_interface_used>
    <input_parameters>type - Video port type
index-  port index
handle - display handle</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the API dsGetEDIDBytes after setting display handle using dsGetDisplay API
3. Update test result as SUCCESS/FAILURE based on the API return value
4.Unload the module</automation_approch>
    <expected_output>API should return EDID bytes details</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetEDIDBytes</test_script>
    <skipped>No</skipped>
    <release_version>M77</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
import tdklib;
from dshalUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_GetEDIDBytes');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    isDisplayConnected = "FALSE"
    print "\nTEST STEP1 : Get the video port handle for HDMI using dsGetVideoPort API"
    print "EXPECTED RESULT : Should get the handle for HDMI"
    tdkTestObj = obj.createTestStep('DSHal_GetVideoPort');
    #Port 6 - VIDEOPORT_TYPE_HDMI
    tdkTestObj.addParameter("portType", 6);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetVideoPort call is success";
        print "Value Returned : ",details

        print "\nTEST STEP2 : Check whether device is connected to TV using dsIsDisplayConnected API"
        print "EXPECTED RESULT : Should get the connection status & device should be connected to HDMI"
        tdkTestObj = obj.createTestStep('DSHal_IsDisplayConnected');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            isDisplayConnected = str(details).upper();
            print "ACTUAL RESULT : [DisplayConnection Status : %s]" %(isDisplayConnected)

            #Check for display connection status
            if isDisplayConnected == "TRUE":
                print "\nTEST STEP3 : Get the display handle for HDMI using dsGetDisplay API"
                print "EXPECTED RESULT : Should get the handle for HDMI"
                tdkTestObj = obj.createTestStep('DSHal_GetDisplay');
                tdkTestObj.addParameter("portType", videoPortType["HDMI"]);
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    details = tdkTestObj.getResultDetails();
                    print "Value Returned : ",details
                    print "ACTUAL RESULT  : dsGetDisplay call is success";

                    print "\nTEST STEP4: Get EDID bytes using dsGetEDIDBytes API"
                    print "EXPECTED RESULT : Should get the EDID bytes details"
                    tdkTestObj = obj.createTestStep('DSHal_GetEDIDBytes');
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        details = tdkTestObj.getResultDetails();
                        n1 = 32
                        n2 = 2
                        edidData = str(details)
                        edidList = [edidData[i:i+n1] for i in range(0, len(edidData), n1)]
                        for edidChunk in edidList:
                            data = [edidChunk[j:j+n2] for j in range(0, len(edidChunk), n2)]
                            print(" ".join(data))
                        print "ACTUAL RESULT  : EDID bytes retrieved successfully"
                        print "[TEST EXECUTION RESULT] : SUCCESS\n"

                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print "Value Returned : ",details
                        print "ACTUAL RESULT  : dsGetEDIDBytes call failed"
                        print "[TEST EXECUTION RESULT] : FAILURE\n"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print "Value Returned : ",details
                    print "ACTUAL RESULT  : dsGetDisplay call failed"
                    print "[TEST EXECUTION RESULT] : FAILURE\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "\nPlease test with HDMI connected device. Exiting....!!!\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print "ACTUAL RESULT  : dsIsDisplayConnected call failed"
            print "Value Returned : ",details
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetVideoPort call failed"
        print "Value Returned : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("dshal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus(loadModuleStatus.upper());
