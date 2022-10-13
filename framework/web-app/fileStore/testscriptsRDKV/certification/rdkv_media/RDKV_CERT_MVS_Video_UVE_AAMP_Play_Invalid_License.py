##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <name>RDKV_CERT_MVS_Video_UVE_AAMP_Play_Invalid_License</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to launch a lightning UVE AAMP player application via Webkit instance and perform playback of drm stream with invalid license url, check for error message and close the player</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_Media_Validation_260</test_case_id>
    <test_objective>Test Script to launch a lightning UVE AAMP player application via Webkit instance and perform playback of drm stream with invalid license url, check for error message and close the player</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDKTV, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning UVE AAMP Player app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning UVE player App URL: string
webkit_instance:string
webinspect_port: string
video_src_url_playready_dash_h264: string
video_src_url_playready_dash_h264_drmconfigs:string
video_src_url_widevine_dash_h264:string
video_src_url_widevine_dash_h264_drmconfigs:string</input_parameters>
    <automation_approch>1. As pre requisite, launch webkit instance via RDKShell, open websocket connection to webinspect page
2. Store the details of other launched apps. Move the webkit instance to front, if its z-order is low.
3. Launch webkit instance with uve test app with the drm stream with invalid  license url.
4. App tries to play the drm stream with invalid license and gives the playback failure event and error message.
5. If expected event playback failed is observed then update the result as SUCCESS or else FAILURE
6. Update the test script result as SUCCESS/FAILURE based on event validation result
7. Revert all values</automation_approch>
    <expected_output>UVE AAMP Player should take the drm stream with invalid license, expected event playback failed and error message should occur</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Video_UVE_AAMP_Play_Invalid_License</test_script>
    <skipped>No</skipped>
    <release_version>M105</release_version>
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
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_UVE_AAMP_Play_Invalid_License')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\nCheck Pre conditions..."
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    # Setting the pre-requites for media test. Launching the webkit instance via RDKShell and
    # moving it to the front, opening a socket connection to the webkit inspect page and
    # disabling proc validation
    selected_drm = "Playready"
    drm_pre_requisite_status = checkDRMSupported(obj,"Playready")
    if drm_pre_requisite_status == "NA":
        selected_drm = "Widevine"
        drm_pre_requisite_status = checkDRMSupported(obj,"Widevine")
    if drm_pre_requisite_status == "TRUE":
        pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,webkit_instance,False)
    elif drm_pre_requisite_status == "NA":
        pre_requisite_status = "NA"
    else:
        pre_requisite_status = "FAILURE"

    if pre_requisite_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print "Pre conditions for the test are set successfully"

        print "\nSet Lightning video player test app url..."
        #Setting device config file
        conf_file,result = getDeviceConfigFile(obj.realpath)
        result, logging_method= readDeviceConfigKeyValue(conf_file,"LOGGING_METHOD")
        setDeviceConfigFile(conf_file)
        appURL    = MediaValidationVariables.lightning_uve_test_app_url
        if selected_drm == "Playready":
            videoURL  = MediaValidationVariables.video_src_url_playready_dash_h264
            drm_configs = MediaValidationVariables.video_src_url_playready_dash_h264_drmconfigs
        else:
            videoURL  = MediaValidationVariables.video_src_url_widevine_dash_h264
            drm_configs = MediaValidationVariables.video_src_url_widevine_dash_h264_drmconfigs

        drm_invalid_configs = ""
        for config in drm_configs.split("|"):
            if "headers[" not in config:
                drm = config.split("[",1)[0]
                license = config.split("[",1)[1].rsplit("]",1)[0]
                invalid_license = license + "_invalid_license_testing"
                drm_system_config = drm+"["+invalid_license+"]"
            else:
                drm_system_config = config
            if drm_invalid_configs != "":
                drm_invalid_configs = drm_invalid_configs + "|"
            drm_invalid_configs = drm_invalid_configs + drm_system_config

        # Setting VideoPlayer Operations
        setOperation("close",MediaValidationVariables.close_interval)
        operations = getOperations()
        # Setting VideoPlayer test app URL arguments
        setURLArgument("url",videoURL)
        setURLArgument("operations",operations)
        setURLArgument("drmconfigs",drm_invalid_configs)
        setURLArgument("autotest","true")
        appArguments = getURLArguments()
        # Getting the complete test app URL
        video_test_url = getTestURL(appURL,appArguments)

        #Example video test url
        #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/tdkuveplayer/build/index.html?
        #url=<video_url>.mpd&drmconfigs=(invalid_license_url)&operations=close(60)&autotest=true

        # Setting the video test url in webkit instance using RDKShell
        launch_status = launchPlugin(obj,webkit_instance,video_test_url)
        # Monitoring the app progress and capturing the player messages
        if "SUCCESS" in launch_status:
            continue_count = 0
            event_status = 0
            error_status = 0
            file_check_count = 0
            logging_flag = 0
            hang_detected = 0
            test_result = ""
            lastLine = None
            lastIndex = 0
            app_log_file = obj.logpath+"/"+str(obj.execID)+"/"+str(obj.execID)+"_"+str(obj.execDevId)+"_"+str(obj.resultId)+"_mvs_applog.txt"
            if logging_method == "REST_API":
                while True:
                    if file_check_count > 60:
                        print "\nREST API Logging is not happening properly. Exiting..."
                        break;
                    if os.path.exists(app_log_file):
                        logging_flag = 1
                        break;
                    else:
                        file_check_count += 1
                        time.sleep(1);

                while logging_flag:
                    if continue_count > 60:
                        hang_detected = 1
                        print "\nApp not proceeding for 60 secs. Exiting..."
                        break;

                    with open(app_log_file,'r') as f:
                        lines = f.readlines()
                    if lines:
                        if len(lines) != lastIndex:
                            continue_count = 0
                            #print(lastIndex,len(lines))
                            for i in range(lastIndex,len(lines)):
                                print(lines[i])
                                if "Event Occurred: playbackFailed" in lines[i]:
                                    event_status = 1
                                if "AAMP: DRM License Request Failed" in lines[i] or "AAMP: DRM License Challenge Generation Failed" in lines[i]:
                                    error_status = 1
                                if "Video PlayBack Failed" in lines[i]:
                                    test_result = lines[i]

                            #lastLine  = lines[-1]
                            lastIndex = len(lines)
                            if test_result != "":
                                break;
                        else:
                            continue_count += 1
                    else:
                        continue_count += 1

                    time.sleep(1)
            elif logging_method == "WEB_INSPECT":
                while True:
                    if continue_count > 60:
                        print "\nApp not proceeding for 60 secs. Exiting..."
                        break
                    if (len(webkit_console_socket.getEventsBuffer())== 0):
                        time.sleep(1)
                        continue_count += 1
                        continue
                    else:
                        continue_count = 0
                    console_log = webkit_console_socket.getEventsBuffer().pop(0)
                    dispConsoleLog(console_log)
                    if "Event Occurred: playbackFailed" in console_log:
                        event_status = 1
                    if "AAMP: DRM License Request Failed" in console_log or "AAMP: DRM License Challenge Generation Failed" in console_log:
                        error_status = 1
                    if "Video PlayBack Failed" in console_log:
                        break;
                webkit_console_socket.disconnect()

            tdkTestObj = obj.createTestStep('rdkv_media_test');
            tdkTestObj.executeTestCase(expectedResult);
            if event_status == 1 and error_status == 1:
                print "Video not playing fine due to invalid license url"
                print "[TEST EXECUTION RESULT]: SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
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
    elif pre_requisite_status == "NA":
        print "Pre conditions are not met\n"
        obj.setAsNotApplicable();            
    else:
        print "Pre conditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
