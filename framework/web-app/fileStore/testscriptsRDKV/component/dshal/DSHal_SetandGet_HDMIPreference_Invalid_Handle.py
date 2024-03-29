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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DSHal_SetandGet_HDMIPreference_Invalid_Handle</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_SetHdmiPreference</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if HDMI preference is set for invalid handle</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks>Script logic need to be revisited -- RDKTT-3219</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_63</test_case_id>
    <test_objective>To check if HDMI preference is set for invalid handle</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetVideoPort(dsVideoPortType_t vType, int index, int *handle)
dsGetHdmiPreference(int handle, dsHdcpProtocolVersion_t *hdcpCurrentProtocol)
dsSetHdmiPreference(int handle, dsHdcpProtocolVersion_t *hdcpCurrentProtocol)</api_or_interface_used>
    <input_parameters>type - Video port type
index- Video port index
handle - Video port handle
hdcpCurrentProtocol - HDCP protocol version</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsGetVideoPort to get the handle for RF video port
3 . DSHAL agent will invoke the api dsSetHdmiPreference to set the HDCP protocol version to 2.x
4 . DSHAL agent will invoke the api dsGetHdmiPreference to get the HDCP protocol version
5. TM checks if the HDCP protocol version is not set and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the HDCP protocol version is not set</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_SetandGet_HDMIPreference_Invalid_Handle</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from dshalUtility import *;

#Test component to be tested
dshalObj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
dshalObj.configureTestCase(ip,port,'DSHal_SetandGet_HDMIPreference_Invalid_Handle');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus;

dshalObj.setLoadModuleStatus(dshalloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper():
    expectedResult="SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioPort');
    tdkTestObj.addParameter("portType", audioPortType["HDMI"]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    print "Getting audio port handle instead of video port handle";
    actualResult = tdkTestObj.getResult();
    print "DSHal_GetAudioPort result: ", actualResult

    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print details;

        details = tdkTestObj.getResultDetails();
        print details;
        tdkTestObj = dshalObj.createTestStep('DSHal_SetHdmiPreference');
        tdkTestObj.addParameter("hdcpProtocol", hdcpProtocolVersion["VERSION_2X"]);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print "DSHal_SetHdmiPreference result: ", actualResult;
        details = tdkTestObj.getResultDetails();
        print details;
        if expectedResult in actualResult:
            tdkTestObj = dshalObj.createTestStep('DSHal_GetHdmiPreference');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print "DSHal_GetHdmiPreference result: ", actualResult
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                print "HdmiPreference retrieved", details
                if int(details) != hdcpProtocolVersion["VERSION_2X"]:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "HdmiPreference not set for invalid handle";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "HdmiPreference set for invalid handle";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to get HdmiPreference";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "DSHal_SetHdmiPreference call Failed";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "AudioPort handle not retrieved";

    dshalObj.unloadModule("dshal");

else:
    print "Module load failed";
