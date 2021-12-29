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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>RDKV_CERT_PACS_Cobalt_TimeTo_Video_PlayPause</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to play and pause a video on YouTube.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_38</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to play and pause a video on YouTube.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Time in Test Manager and DUT should be in sync with UTC</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. Set a video URL using deeplink method.
3. Save current system time and Start playing by generateKey method
4. Get wpeframework logs to related with video playback and parse the time stamp
5. Compare the time stamps and check video started playing
6. Save current system time and click pause button using generateKey
7. Get the wpeframework log and parse pause related time stamps and compare with time before pausing and get time taken for pause
8. Save current system time and click play button using generateKey.
9. Get the wpeframework log and parse play related time stamps and compare with time before playing and get time taken for play
10. Deactivate the Cobalt plugin.
</automation_approch>
    <expected_output>The time taken to play and time taken to pause a video must be within the expected limits</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_TimeTo_Video_PlayPause</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import PerformanceTestVariables
from StabilityTestUtility import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_TimeTo_Video_PlayPause');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url value\n"
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and expectedResult in result and ssh_param_dict != {} and cobalt_test_url != "":
        tdkTestObj.setResultStatus("SUCCESS")
        cobal_launch_status = launch_cobalt(obj)
        print "\nPre conditions for the test are set successfully"
        time.sleep(30)
        if cobal_launch_status == "SUCCESS":
            print "\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url)
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","Cobalt.1.deeplink")
            tdkTestObj.addParameter("value",cobalt_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_result = tdkTestObj.getResult()
            time.sleep(20)
            if(cobalt_result == expectedResult):
                tdkTestObj.setResultStatus("SUCCESS")
                print "Clicking OK to play video"
                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                video_start_time = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                result1 = tdkTestObj.getResult()
                time.sleep(40)
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result2 = tdkTestObj.getResult()
                time.sleep(50)
                if "SUCCESS" == (result1 and result2):
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\n Check video is started \n"
                    command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                    tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                    tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                    tdkTestObj.addParameter("command",command)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    output = tdkTestObj.getResultDetails()
                    if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                        video_playing_log = output.split('\n')[1]
                        video_play_starttime_in_millisec = getTimeInMilliSec(video_start_time)
                        video_played_time = getTimeStampFromString(video_playing_log)
                        video_played_time_in_millisec = getTimeInMilliSec(video_played_time)
                        if video_played_time_in_millisec > video_play_starttime_in_millisec:
                            print "\n Video started Playing\n"
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(10)
                            print "\n Pausing Video \n"
                            params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            pause_start_time = str(datetime.utcnow()).split()[1]
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if result == "SUCCESS":
                                time.sleep(20)
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n Check video is paused \n"
                                command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PLAYING.*new.*PAUSED | tail -1'
                                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                tdkTestObj.addParameter("command",command)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                output = tdkTestObj.getResultDetails()
                                if output != "EXCEPTION" and expectedResult in result and "old: PLAYING" in output:
                                    pause_log = output.split('\n')[1]
                                    pause_starttime_in_millisec = getTimeInMilliSec(pause_start_time)
                                    video_pausedtime = getTimeStampFromString(pause_log)
                                    video_pausedtime_in_millisec = getTimeInMilliSec(video_pausedtime)
                                    time_for_video_pause = video_pausedtime_in_millisec - pause_starttime_in_millisec
                                    if video_pausedtime_in_millisec > pause_starttime_in_millisec:
                                        print "\n Video is paused \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        #Play video
                                        print "\n Play video \n"
                                        params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                        tdkTestObj.addParameter("value",params)
                                        play_start_time = str(datetime.utcnow()).split()[1]
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        if result == "SUCCESS":
                                            print "\n Check video is playing \n"
                                            time.sleep(20)
                                            command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                            tdkTestObj.addParameter("command",command)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResult()
                                            output = tdkTestObj.getResultDetails()
                                            if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                                playing_log = output.split('\n')[1]
                                                play_starttime_in_millisec = getTimeInMilliSec(play_start_time)
                                                video_playedtime = getTimeStampFromString(playing_log)
                                                print "\n Played time",video_playedtime
                                                video_playedtime_in_millisec = getTimeInMilliSec(video_playedtime)
                                                time_for_video_play = video_playedtime_in_millisec - play_starttime_in_millisec
                                                #Get threshold values from device config file
                                                conf_file,file_status = getConfigFileName(obj.realpath)
                                                result1,cobalt_pause_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_PAUSE_TIME_THRESHOLD_VALUE")
                                                result2,cobalt_play_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_PLAY_TIME_THRESHOLD_VALUE")
                                                offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                                if all(value != "" for value in (cobalt_pause_threshold,cobalt_play_threshold,offset)):
                                                    print "\n play initiated at {} ".format(play_start_time)
                                                    print "\n play happend at {} ".format(video_playedtime)
                                                    print "\n Time taken for play operation: {} milliseconds \n".format(time_for_video_play)
                                                    print "\n Threshold value for time taken for play operation : {} ms".format(cobalt_play_threshold)
                                                    if 0 < int(time_for_video_play) < (int(cobalt_play_threshold) + int(offset)):
                                                        print "\n Time taken for play operation is within the expected limit"
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                    else:
                                                        print "\n Time taken for play operation is not within the expected limit"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                    print "\n pause initiated at {} ".format(pause_start_time)
                                                    print "\n pause happend at {} (UTC)".format(video_pausedtime)
                                                    print "\n Time taken for pause operation: {} milleseconds \n".format(time_for_video_pause)
                                                    print "\n Threshold value for time taken for pause operation : {} ms".format(cobalt_pause_threshold)
                                                    if 0 < int(time_for_video_pause) < (int(cobalt_pause_threshold) + int(offset)):
                                                        print "\n Time taken for pause operation is within the expected limit \n"
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                    else:
                                                        print "\n Time taken for pause operation is not within the expected limit \n"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                else:
                                                    print "\n Please configure the threshold values in device config file \n"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print "\n Video play related logs are not available"
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print "\n Error while executing generateKey method \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Video pause related logs are not available \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Video pause related logs are not available"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while executing generateKey method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Video is not started playing \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Video play related logs are not available \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing generateKey method \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing deeplink method \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching Cobalt \n"
            tdkTestObj.setResultStatus("FAILURE")
        print "\n Exiting from Cobalt \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met \n"
        tdkTestObj.setResultStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
