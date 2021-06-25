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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_MVS_Animation_StartStop_STRESS</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to launch a lightning Animation application and perform animation start and stop operation repeatedly for given number of times</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_Media_Validation_02</test_case_id>
    <test_objective>Test Script to launch a lightning Animation application and perform animation start and stop operation repeatedly for given number of times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Animation app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning Animation App URL: string
webinspect_port: string
thunder_port :string
interval: int
stress_repeat_count: int</input_parameters>
    <automation_approch>1. As pre requisite, launch LightningApp  webkit instance via RDKShell, open websocket conntion to webinspect page
2. Store the details of other launched apps. Move the LightningApp  webkit instance to front, if its z-order is low.
3. Launch LightningApp webkit instance with animation test app url  with the operations stop, start and repeat info.
4. App performs the stop and start operation repeatedly and validates using events
5. If expected events occurs for start and stop in all the repetition, then app gives the validation result as SUCCESS or else FAILURE
6. Get the event validation result from the app and update the test script status
7. Revert all values</automation_approch>
    <expected_output>Animation start and stop should happen for all the repetition</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Animation_StartStop_STRESS</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Animation_StartStop_STRESS')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\nCheck Pre conditions..."
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    setWebKitSocketPort(webinspect_port_lightning)    
    # Setting the pre-requites for media test. Launching the wekit instance via RDKShell and
    # moving it to the front, openning a socket connection to the webkit inspect page and
    # disabling proc validation
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,"LightningApp",False)
    if pre_requisite_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print "Pre conditions for the test are set successfully"

        print "\nSet Lightning animation test app url..."
        #Setting device config file
        conf_file,result = getDeviceConfigFile(obj.realpath)
        setDeviceConfigFile(conf_file)
        appURL    = MediaValidationVariables.lightning_animation_test_app_url
        # Setting Animation Operations
        setOperation("stop",MediaValidationVariables.pause_interval_stress)
        setOperation("start",MediaValidationVariables.play_interval_stress)
        setOperation("repeat",MediaValidationVariables.repeat_count_stress)
        operations = getOperations()
        # Setting Animation test app URL arguments
        setURLArgument("ip",ip)
        setURLArgument("port",MediaValidationVariables.thunder_port)
        setURLArgument("operations",operations)
        setURLArgument("autotest","true")
        appArguments = getURLArguments()
        # Getting the complete test app URL
        animation_test_url = getTestURL(appURL,appArguments)

        # Setting the animation test url in webkit instance using RDKShell
        launch_status = launchPlugin(obj,"LightningApp",animation_test_url)
        if "SUCCESS" in launch_status:
            # Monitoring the app progress, checking whether app performs animation properly or any hang detected in between,
            # and getting the test result from the app
            test_result,diagnostics_info = monitorAnimationTest(obj,webkit_console_socket,None);
            tdkTestObj = obj.createTestStep('rdkv_media_test');
            tdkTestObj.executeTestCase(expectedResult);
            if "SUCCESS" in test_result:
                print "Animation using Lightning app works fine"
                print "[TEST EXECUTION RESULT]: SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "Animation using Lightning app not working fine"
                print "[TEST EXECUTION RESULT]: FAILURE"
                tdkTestObj.setResultStatus("FAILURE");

            print "\nSet post conditions..."
            tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
            tdkTestObj.executeTestCase(expectedResult);
            # Setting the post-requites for media test.Removing app url from webkit instance and
            # moving next high z-order app to front (residentApp if its active)
            post_requisite_status = setMediaTestPostRequisites(obj,"LightningApp")
            if post_requisite_status == "SUCCESS":
                print "Post conditions for the test are set successfully\n"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "Post conditions are not met\n"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to load the Animation Test URL in Webkit\n"
    else:
        print "Pre conditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

