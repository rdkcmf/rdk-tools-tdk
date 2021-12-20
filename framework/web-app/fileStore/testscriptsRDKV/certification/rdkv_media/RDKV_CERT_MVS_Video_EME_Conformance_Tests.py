##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
  <name>RDKV_CERT_MVS_Video_EME_Conformance_Tests</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to launch the EME conformance test url in Webkit browser and execute the tests.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_Media_Validation_148</test_case_id>
    <test_objective>Test script to launch the EME conformance test url in Webkit browser and execute the tests.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Ensure that the eme_conformance_test_app_url and eme_key_sequence parameters in the MediaValidationVariables file has latest values.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>webinspect_port: string
eme_conformance_test_app_url:string
eme_key_sequence:string</input_parameters>
    <automation_approch>1. As pre requisite, launch webkit browser via RDKShell, open websocket connection to webinspect page
2. Store the details of other launched apps. Move the webkit browser to front, if its z-order is low.
3. Read the eme url and key sequence info from the MVS config file
4.Launch the webkit browser with eme conformance test url
5.Provide the keys via RDKShell to navigate and select Run All to start the tests.
6.Collect the failed tests and store the details.
7.After the test completion, if there are any failed tests, list then and make the test status as FAILURE else SUCCESS.
8. Revert all values</automation_approch>
    <expected_output>EME conformance test should run properly</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Video_EME_Conformance_Tests</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_EME_Conformance_Tests')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\nCheck Pre conditions..."
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    setWebKitSocketPort(webinspect_port)
    # Setting the pre-requites for media test. Launching the wekit instance via RDKShell and
    # moving it to the front, openning a socket connection to the webkit inspect page and
    # disabling proc validation
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,"WebKitBrowser",False)
    config_status = "SUCCESS"
    if pre_requisite_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print "Pre conditions for the test are set successfully"

        print "\nSet EME Conformance test app url..."
        #Setting device config file
        test_app_url = MediaValidationVariables.eme_conformance_test_app_url
        print "\n================================================="
        print "URL Used: ",test_app_url
        print "=================================================\n"

        # Setting the EME test url in webkit instance using RDKShell
        launch_status = launchPlugin(obj,"WebKitBrowser",test_app_url)
        if "SUCCESS" in launch_status:
            # Monitoring the app progress, checking whether app runs tests properly or any hang detected in between,
            # and getting the test result from the app
            # Monitoring the EME test with hang detection time-out of 5 mins (300 seconds)
            test_result,failed_test_list = monitorConformanceTest(obj,webkit_console_socket,300)
            tdkTestObj = obj.createTestStep('rdkv_media_test');
            tdkTestObj.executeTestCase(expectedResult);
            if "SUCCESS" in test_result:
                print "All EME Conformance Tests Success"
                print "[TEST EXECUTION RESULT]: SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "EME Conformance Tests Failed"
                print "[TEST EXECUTION RESULT]: FAILURE"
                tdkTestObj.setResultStatus("FAILURE");

            print "\nSet post conditions..."
            tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
            tdkTestObj.executeTestCase(expectedResult);
            # Setting the post-requites for media test.Removing app utl from webkit instance and
            # moving next high z-order app to front (residentApp if its active)
            post_requisite_status = setMediaTestPostRequisites(obj,"WebKitBrowser")
            if post_requisite_status == "SUCCESS":
                print "Post conditions for the test are set successfully\n"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "Post conditions are not met\n"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to load the EME Conformance Test URL in Webkit\n"
    else:
        print "Pre conditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"


