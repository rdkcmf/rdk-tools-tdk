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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DSHal_EnableAudioAtmosOutputMode_HDMI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_SetAudioAtmosOutputMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To enable AudioAtmosOutputMode for the audio port HDMI</synopsis>
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
    <box_type>IPClient-Wifi</box_type>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_120</test_case_id>
    <test_objective>To enable AudioAtmosOutputMode for the audio port HDMI</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI6,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsSetAudioAtmosOutputMode(int handle, bool enable)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
enable - enable</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsSetAudioAtmosOutputMode to enable the AudioAtmosOutputMode
3. TM checks if the API call is success and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_EnableAudioAtmosOutputMode_HDMI</test_script>
    <skipped>No</skipped>
    <release_version>M76</release_version>
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
dshalObj.configureTestCase(ip,port,'DSHal_EnableAudioAtmosOutputMode_HDMI');

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
        actualResult = tdkTestObj.getResult();
        print "DSHal_GetAudioPort result: ", actualResult

        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print details;

            enable = 1;
            tdkTestObj = dshalObj.createTestStep('DSHal_SetAudioAtmosOutputMode');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            tdkTestObj.addParameter("enable",1);
            actualResult = tdkTestObj.getResult();
            print "DSHal_SetAudioAtmosOutputMode result: ", actualResult
            details = tdkTestObj.getResultDetails();
            print details;
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SetAudioAtmosOutputMode call success"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "SetAudioAtmosOutputMode call Failed";

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "AudioPort handle not retrieved";

        dshalObj.unloadModule("dshal");

else:
    print "Module load failed";
