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
  <name>DSHal_IsAudioMS12Decode_HDMI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_IsAudioMS12Decode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To get the AudioMS12Decode status for HDMI audio port</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_57</test_case_id>
    <test_objective>To get the AudioMS12Decode status for HDMI audio port</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsIsAudioMS12Decode(int handle, bool *ms12Enabled)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
ms12Enabled - MSdecode status</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsIsAudioMS12Decode to get MS12Decode status
3. TM checks if the status is correct and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the status is correct</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_IsAudioMS12Decode_HDMI</test_script>
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
sysObj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
dshalObj.configureTestCase(ip,port,'DSHal_IsAudioMS12Decode_HDMI');
sysObj.configureTestCase(ip,port,'DSHal_IsAudioMS12Decode_HDMI');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus;
sysloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %sysloadModuleStatus;

dshalObj.setLoadModuleStatus(dshalloadModuleStatus);
sysObj.setLoadModuleStatus(sysloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper() and "SUCCESS" in sysloadModuleStatus.upper():
    expectedResult="SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioPort');
    tdkTestObj.addParameter("portType", audioPortType["HDMI"]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print "DSHal_GetAudioPort result: ", actualResult

    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print details;

        #Check current AudioMS12Decode status
        tdkTestObj = dshalObj.createTestStep('DSHal_IsAudioMS12Decode');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print "DSHal_IsAudioMS12Decode result: ", actualResult
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            ms12Decode = tdkTestObj.getResultDetails();
            print "AudioMS12Decode status retrieved", ms12Decode;
            logName = "/etc/default/nxserver.cfg";
            pattern = "ms12";
            tdkTestObj = sysObj.createTestStep('ExecuteCommand');
            cmd = "grep " + pattern + " " + logName;
            print cmd;
            tdkTestObj.addParameter("command", cmd);
            tdkTestObj.executeTestCase("SUCCESS");
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "OUTPUT:", details;

            if (pattern in details and ms12Decode == "true") or (pattern not in details and ms12Decode == "false"):
                tdkTestObj.setResultStatus("SUCCESS");
                print "AudioMS12Decode status verified"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "AudioMS12Decode status not verified";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Failed to get AudioMS12Decode status";

    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "AudioPort handle not retrieved";

    dshalObj.unloadModule("dshal");
    sysObj.unloadModule("systemutil");

else:
    print "Module load failed";
