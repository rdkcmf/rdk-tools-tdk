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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_VP9</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script is to get the performance of the Lightning application by calculating the time taken for play and pause operations of dash vp9 video.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>6</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_120</test_case_id>
    <test_objective>This script is to get the performance of the Lightning application by calculating the time taken for play and pause operations of vp9 video.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable webkitinstance plugin.
2. Set the application URL
3. Play and pause the video from the application
3. Get the time taken to play/pause the video</automation_approch>
    <expected_output>The video must play and pause within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_VP9</test_script>
    <skipped>No</skipped>
    <release_version>M99</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from web_socket_util import *
import PerformanceTestVariables
import MediaValidationVariables
from MediaValidationUtility import *
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_VP9');

webkit_console_socket = None

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    conf_file, status = get_configfile_name(obj);
    result, logging_method = getDeviceConfigKeyValue(conf_file,"LOGGING_METHOD")
    setDeviceConfigFile(conf_file)
    videoURL  = MediaValidationVariables.video_src_url_vp9
    videoURL_type = MediaValidationVariables.vp9_url_type
    setURLArgument("execID",str(obj.execID))
    setURLArgument("execDevId",str(obj.execDevId))
    setURLArgument("resultId",str(obj.resultId))
    setLoggingMethod(obj)
    setURLArgument("logging",logging_method)
    setURLArgument("tmUrl",str(obj.url)+"/")
    setOperation("pause",10)
    setOperation("play",10)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    setURLArgument("type",videoURL_type)
    appArguments = getURLArguments()
    video_test_urls = []
    players_list = str(MediaValidationVariables.codec_vp9).split(",")
    print "SELECTED PLAYERS: ", players_list
    # Getting the complete test app URL
    video_test_urls = getTestURLs(players_list,appArguments)
    print "\n Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    webkit_instance = PerformanceTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
    if webkit_instance in "WebKitBrowser":
        webinspect_port = PerformanceTestVariables.webinspect_port
    elif webkit_instance in "LightningApp":
        webinspect_port = PerformanceTestVariables.lightning_app_webinspect_port
    else:
        webinspect_port = PerformanceTestVariables.html_app_webinspect_port
    plugins_list = ["Cobalt",webkit_instance]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    status = "SUCCESS"
    plugin_status_needed = {webkit_instance:"resumed","Cobalt":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting plugin status"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        set_status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\n Pre conditions for the test are set successfully";
        print "\n Get the URL in {}".format(webkit_instance)
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
            time.sleep(60)
            print "\n Current URL:",current_url
            print "\n Set Lightning Application URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",video_test_urls[0]);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\n Validate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                if new_url in video_test_urls[0]:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "\n URL(",new_url,") is set successfully"
                    if logging_method == "REST_API":
                        expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingRestAPI(obj);
                        evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                    elif logging_method == "WEB_INSPECT":
                        if current_url != None and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS");
                            expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingWebInspect(obj,webkit_console_socket);
                            evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                if ("SUCCESS" in test_result) and (not any(value == "" for value in evt_list)):
                    pausing_time = getTimeFromMsg(expected_pause_evt)
                    print "\n Pause initiated at {} (UTC)".format(pausing_time)
                    pausing_time_millisec = getTimeInMilliSeconds(pausing_time)
                    paused_time = getTimeFromMsg(observed_pause_evt)
                    print "\n Pause happend at {} (UTC)".format(paused_time)
                    paused_time_millisec = getTimeInMilliSeconds(paused_time)
                    pause_opn_time = paused_time_millisec - pausing_time_millisec
                    print "\n Time taken for pause operation: {} milleseconds \n".format(pause_opn_time)
                    conf_file,result = getConfigFileName(tdkTestObj.realpath)
                    result1, pause_time_threshold_value = getDeviceConfigKeyValue(conf_file,"PAUSE_TIME_THRESHOLD_VALUE")
                    Summ_list.append('PAUSE_TIME_THRESHOLD_VALUE :{}ms'.format(pause_time_threshold_value))
                    result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                    Summ_list.append('Pause initiated at  :{}'.format(pausing_time))
                    Summ_list.append('Pause happend at :{}'.format(paused_time))
                    Summ_list.append('Time taken for pause operation :{}ms'.format(pause_opn_time))
                    if all(value != "" for value in (pause_time_threshold_value,offset)):
                        print "\n The threshold value for time taken to pause operation: {} ms".format(pause_time_threshold_value)
                        if 0 < int(pause_opn_time) < (int(pause_time_threshold_value) + int(offset)):
                            pause_status = True
                            print "\n Time taken for pause operation is within the expected limit \n"
                        else:
                            pause_status = False
                            print "\n Time taken for pause operation is not within the expected limit \n"
                    else:
                        pause_status = False
                        print "\n Failed to get the threshold value for pause operation time from config file \n"
                    playing_time = getTimeFromMsg(expected_play_evt)
                    print "\n Play initiated at {} (UTC)".format(playing_time)
                    playing_time_millisec = getTimeInMilliSeconds(playing_time)
                    played_time = getTimeFromMsg(observed_play_evt)
                    print "\n Play happend at {} (UTC)".format(played_time)
                    played_time_millisec = getTimeInMilliSeconds(played_time)
                    play_opn_time = played_time_millisec - playing_time_millisec
                    print "\n Time taken for play operation: {} milliseconds \n".format(play_opn_time)
                    result, play_time_threshold_value = getDeviceConfigKeyValue(conf_file,"PLAY_TIME_THRESHOLD_VALUE")
                    Summ_list.append('PLAY_TIME_THRESHOLD_VALUE :{}ms'.format(play_time_threshold_value))
                    Summ_list.append('Play initiated at :{}'.format(playing_time))
                    Summ_list.append('Play happend at :{}'.format(played_time))
                    Summ_list.append('Time taken for play operation :{}ms'.format(play_opn_time))
                    if play_time_threshold_value != "":
                        print "\n The threshold value for time taken to play operation: {} ms".format(play_time_threshold_value)
                        if 0 < int(play_opn_time) < (int(play_time_threshold_value) + int(offset)):
                            play_status = True
                            print "\n Time taken for play operation is within the expected limit \n"
                        else:
                            play_status = False
                            print "\n Time taken for play operation is not within the expected limit \n"
                    else:
                        play_status = False
                        print "Failed to get the threshold value for play operation time from config file"
                    #Set the result status based on time taken for both pause and play operations.
                    if all(status for status in (pause_status,play_status)):
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "\n Error occured during video playback"
                #Set the URL back to previous
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.addParameter("value",current_url);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if result == "SUCCESS":
                    print "\n URL is reverted successfully"
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "\n Failed to revert the URL"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "\n Failed to load the URL, new URL %s" %(new_url)
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "\n Failed to set the URL"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "\n Failed to load module"
