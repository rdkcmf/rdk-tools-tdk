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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_MVS_Video_PlayPause_STRESS_AAC</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to launch a lightning Video player application via Webkit instance and perform video play pause operations of AAC codec stream continuously for given number of times</synopsis>
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
    <box_type>RDKTV</box_type>
    <!-- -->
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
    <test_case_id>RDKV_Media_Validation_50</test_case_id>
    <test_objective>Test Script to launch a lightning Video player application via Webkit instance and perform video play pause operations of AAC codec stream continuously for given number of times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDKTV,RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Player app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning player App URL: string
webkit_instance:string
webinspect_port: string
video_src_url_aac: string
aac_url_type:string
pause_interval_stress:int
play_interval_stress:int
repeat_count_stress:int</input_parameters>
    <automation_approch>1. As pre requisite, launch webkit instance via RDKShell, open websocket conntion to webinspect page
2. Store the details of other launched apps. Move the webkit instance to front, if its z-order is low.
3. Launch webkit instance with video test app url with the operations play, pause and repeat info.
4. App performs the pause and play operation repeatedly and validates using events
5. If expected events occurs for pause and play in all the repetition, then app gives the validation result as SUCCESS or else FAILURE
6. Update the test script result as SUCCESS/FAILURE based on event validation result from the app and proc check status (if applicable)
7. Revert all values</automation_approch>
    <expected_output>Player pause and play should happen and expected events should occur for all the repetition and if proc validation is applicable, then expected data should be available in proc file </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Video_PlayPause_STRESS_AAC</test_script>
    <skipped>No</skipped>
    <release_version>M87</release_version>
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
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_PlayPause_STRESS_AAC')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\nCheck Pre conditions..."
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    # Setting the pre-requites for media test. Launching the wekit instance via RDKShell and
    # moving it to the front, openning a socket connection to the webkit inspect page and
    # getting the details for proc validation from config file
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,webkit_instance)
    if pre_requisite_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print "Pre conditions for the test are set successfully"

        print "\nSet Lightning video player test app url..."
        #Setting device config file
        conf_file,result = getDeviceConfigFile(obj.realpath)
        setDeviceConfigFile(conf_file)
        #appURL    = MediaValidationVariables.lightning_video_test_app_url
        videoURL  = MediaValidationVariables.video_src_url_aac
        # Setting VideoPlayer Operations
        setOperation("pause",MediaValidationVariables.pause_interval_stress)
        setOperation("play",MediaValidationVariables.play_interval_stress)
        setOperation("repeat",MediaValidationVariables.repeat_count_stress)
        operations = getOperations()
        # Setting VideoPlayer test app URL arguments
        setURLArgument("url",videoURL)
        setURLArgument("operations",operations)
        setURLArgument("autotest","true")
        setURLArgument("type",MediaValidationVariables.aac_url_type)
        appArguments = getURLArguments()
        
	# Getting the complete test app URL for selected players
        video_test_urls = []
        test_counter = 0
        if MediaValidationVariables.aac_url_type == "hls":
            players_list = str(MediaValidationVariables.codec_hls_aac).split(",")
        elif MediaValidationVariables.aac_url_type == "dash":
            players_list = str(MediaValidationVariables.codec_dash_aac).split(",")
        else:
            players_list = str(MediaValidationVariables.codec_mp4).split(",")
        print "SELECTED PLAYERS: ", players_list
        video_test_urls = getTestURLs(players_list,appArguments)

	
        #Example video test url
        #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/tdkvideoplayer/build/index.html?
        #url=<video_url>.mpd&operations=pause(5),play(5),repeat(15)&autotest=true&type=dash

        # Setting the video test url in webkit instance using RDKShell
	for video_test_url in video_test_urls:
            launch_status = launchPlugin(obj,webkit_instance,video_test_url)
            if "SUCCESS" in launch_status:
            	# Monitoring the app progress, checking whether app plays the video properly or any hang detected in between,
            	# performing proc entry check and getting the test result from the app
                test_counter += 1
            	test_result,proc_check_list = monitorVideoTest(obj,webkit_console_socket,validation_dict,"Observed Event: play");
            	tdkTestObj = obj.createTestStep('rdkv_media_test');
            	tdkTestObj.executeTestCase(expectedResult);
            	if "SUCCESS" in test_result and "FAILURE" not in proc_check_list:
                    print "Video play is fine"
                    print "[TEST EXECUTION RESULT]: SUCCESS"
                    tdkTestObj.setResultStatus("SUCCESS");
            	elif "SUCCESS" in test_result and "FAILURE" in proc_check_list:
                    print "Decoder proc entry check returns failure.Video not playing fine"
                    print "[TEST EXECUTION RESULT]: FAILURE"
                    tdkTestObj.setResultStatus("FAILURE");
            	else:
                    print "Video not playing fine"
                    print "[TEST EXECUTION RESULT]: FAILURE"
                    tdkTestObj.setResultStatus("FAILURE");

		if test_counter < len(video_test_urls):
                    launch_status = launchPlugin(obj,webkit_instance,"about:blank")
                    time.sleep(3)
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Unable to load the video Test URL in Webkit\n"

        print "\nSet post conditions..."
        tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
        tdkTestObj.executeTestCase(expectedResult);
        # Setting the post-requites for media test.Removing app url from webkit instance and
        # moving next high z-order app to front (residentApp if its active)
        post_requisite_status = setMediaTestPostRequisites(obj,webkit_instance,webkit_console_socket)
        if post_requisite_status == "SUCCESS":
            print "Post conditions for the test are set successfully\n"
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "Post conditions are not met\n"
            tdkTestObj.setResultStatus("FAILURE");
        
    else:
        print "Pre conditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

