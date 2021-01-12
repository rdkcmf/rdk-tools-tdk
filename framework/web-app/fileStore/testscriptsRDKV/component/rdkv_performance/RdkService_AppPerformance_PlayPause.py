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
  <version>1</version>
  <name>RdkService_AppPerformance_PlayPause</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script is to get the performance of the Lightning application by calculating the time taken for play and pause operations.</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_03</test_case_id>
    <test_objective>This script is to get the performance of the Lightning application by calculating the time taken for play and pause operations.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable webkitbrowser plugin.
2. Set the application URL in webkitbrowser
3. Play and pause the video from the application
3. Get the time taken to play/pause the video</automation_approch>
    <expected_output>The video must play and pause within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RdkService_AppPerformance_PlayPause</test_script>
    <skipped>No</skipped>
    <release_version>M82</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from web_socket_util import *
import MediaValidationVariables
from MediaValidationUtility import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_AppPerformance_PlayPause');

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = MediaValidationVariables.lightning_video_test_app_url
    videoURL  = MediaValidationVariables.video_src_url
    
    setOperation("pause",10)
    setOperation("play",10)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    appArguments = getURLArguments()
    # Getting the complete test app URL
    video_test_url = getTestURL(appURL,appArguments)
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated"}
    if curr_plugins_status_dict != plugin_status_needed:
        status = "FAILURE"
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        if current_url != None:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,MediaValidationVariables.webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "Current URL:",current_url
            print "\nSet Lightning Application URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",video_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            new_url = tdkTestObj.getResultDetails();
            if new_url in video_test_url:
                tdkTestObj.setResultStatus("SUCCESS");
                print "URL(",new_url,") is set successfully"
                continue_count = 0
                test_result = ""
                expected_play_evt = ""
                observed_play_evt = ""
                expected_pause_evt = ""
                observed_pause_evt = ""
                
                while True:
                    if continue_count > 60:
                        print "Application is not playing the content"
                        break
                    if (len(webkit_console_socket.getEventsBuffer())== 0):
                        time.sleep(1)
                        continue_count += 1
                        continue
                    continue_count = 0
                    console_log = webkit_console_socket.getEventsBuffer().pop(0)
                    dispConsoleLog(console_log)
                    if "Expected Event: paused" in console_log:
                        expected_pause_evt = getConsoleMessage(console_log)
                    elif "Observed Event: paused" in console_log:
                        observed_pause_evt = getConsoleMessage(console_log)
                    elif "Expected Event: play" in console_log:
                        expected_play_evt = getConsoleMessage(console_log)
                    elif "Observed Event: play" in console_log:
                        observed_play_evt = getConsoleMessage(console_log)
                    elif "TEST RESULT:" in console_log or "Connection refused" in console_log:
                        test_result = getConsoleMessage(console_log)
                        break;
                    else:
                        continue
                webkit_console_socket.disconnect()
                evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt]
                if ("SUCCESS" in test_result) and (not any(value == "" for value in evt_list)):
                    pausing_time = getTimeFromMsg(expected_pause_evt)
                    print "\n pause initiated at {} (UTC)".format(pausing_time)
                    pausing_time_millisec = getTimeInMilliSeconds(pausing_time)
                    paused_time = getTimeFromMsg(observed_pause_evt)
                    print "\n pause happend at {} (UTC)".format(paused_time)
                    paused_time_millisec = getTimeInMilliSeconds(paused_time)
                    pause_opn_time = paused_time_millisec - pausing_time_millisec
                    print "\n Time taken for pause operation: {} milleseconds \n".format(pause_opn_time)
                    conf_file,result = getConfigFileName(tdkTestObj.realpath)
                    result, pause_time_threshold_value = getDeviceConfigKeyValue(conf_file,"PAUSE_TIME_THRESHOLD_VALUE")
                    if result == "SUCCESS":
                        if int(pause_opn_time) < int(pause_time_threshold_value):
                            pause_status = True 
                            print "\n Time taken for pause operation is within the expected limit \n"
                        else:
                            pause_status = False
                            print "\n Time taken for pause operation is greater than the expected limit \n"
                    else:
                        pause_status = False
                        print "\n Failed to get the threshold value for pause operation time from config file \n"
                    playing_time = getTimeFromMsg(expected_play_evt)
                    print "\n play initiated at {} (UTC)".format(playing_time)
                    playing_time_millisec = getTimeInMilliSeconds(playing_time)
                    played_time = getTimeFromMsg(observed_play_evt)
                    print "\n play happend at {} (UTC)".format(played_time)
                    played_time_millisec = getTimeInMilliSeconds(played_time)
                    play_opn_time = played_time_millisec - playing_time_millisec
                    print "\n Time taken for play operation: {} milliseconds \n".format(play_opn_time)
                    result, play_time_threshold_value = getDeviceConfigKeyValue(conf_file,"PLAY_TIME_THRESHOLD_VALUE")
                    if result == "SUCCESS":
                        if int(play_opn_time) < int(play_time_threshold_value):
                            play_status = True
                            print "\n Time taken for play operation is within the expected limit \n"
                        else:
                            play_status = False
                            print "\n Time taken for play operation is greater than the expected limit \n"
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
                    print "error occured during application launch"
                #Set the URL back to previous
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.addParameter("value",current_url);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if result == "SUCCESS":
                    print "URL is reverted successfully"
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "Failed to revert the URL"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "Failed to load the URL %s" %(new_url)
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

