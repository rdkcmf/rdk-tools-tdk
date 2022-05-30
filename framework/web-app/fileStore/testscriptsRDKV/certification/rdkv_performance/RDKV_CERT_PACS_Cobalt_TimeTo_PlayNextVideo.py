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
  <version>4</version>
  <name>RDKV_CERT_PACS_Cobalt_TimeTo_PlayNextVideo</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to start a new video after playing a given video in Cobalt.</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_66</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to start a new video after playing a given video in Cobalt.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running
2. Time in DUT and TM should be in sync</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url</input_parameters>
    <automation_approch>1. Launch Cobalt
2. Set video URL using deeplink method.
3. Click OK to start video playback.
4. Validate video playback using decoder logs
5. Click down arrow key 2 times and then press ok to select the new video.
6. Check gstplayer state change logs in wpeframework log to get the next video start time.
7. Validate the time taken to play the new video.</automation_approch>
    <expected_output>Time taken should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_TimeTo_PlayNextVideo</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import PerformanceTestVariables
from StabilityTestUtility import *
from datetime import datetime
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_TimeTo_PlayNextVideo');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable 
Summ_list=[]

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    revert="NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url in Config file"
    plugins_list = ["Cobalt","WebKitBrowser"]
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting plugin status"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if expectedResult in result:
        ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    else:
        ssh_param_dict = {}
    if status == "SUCCESS" and cobalt_test_url != "" and validation_dict != {} and ssh_param_dict != {}:
        plugin = "Cobalt"
        print "\n Preconditions are set successfully"
        keycode_list = ['40', '40', '13']
        enterkey_keycode = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
        generatekey_method = 'org.rdk.RDKShell.1.generateKey'
        plugin_operations_list = [{'Cobalt.1.deeplink':cobalt_test_url},{generatekey_method:enterkey_keycode},{generatekey_method:enterkey_keycode}]
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
            plugin_validation_details = ["video_validation", validation_dict["ssh_method"], credentials, validation_dict["video_validation_script"]]
        else:
            plugin_validation_details = ["no_validation"]
        plugin_operations = json.dumps(plugin_operations_list)
        plugin_validation_details = json.dumps(plugin_validation_details)
        tdkTestObj = obj.createTestStep('rdkservice_validatePluginFunctionality')
        tdkTestObj.addParameter("plugin",plugin)
        tdkTestObj.addParameter("operations",plugin_operations)
        tdkTestObj.addParameter("validation_details",plugin_validation_details)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails();
        if expectedResult in result and details == "SUCCESS" :
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Play next video"
            for keycode in keycode_list:
                params = '{"keys":[ {"keyCode": ' + keycode + ',"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                if keycode == '13':
                    play_start_time = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    print "\n Sending keycode : {} using generateKey".format(keycode)
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n Error while executing generateKey method with keycode: {}".format(keycode)
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                time.sleep(25)
                print "\n Check the logs from DUT"
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
                    print "\n Playing log  :",playing_log
                    play_starttime_in_millisec = getTimeInMilliSec(play_start_time)
                    video_playedtime = getTimeStampFromString(playing_log)
                    video_playedtime_in_millisec = getTimeInMilliSec(video_playedtime)
                    time_for_video_play = video_playedtime_in_millisec - play_starttime_in_millisec
                    #Get threshold values from device config file
                    conf_file,file_status = getConfigFileName(obj.realpath)
                    result2,cobalt_play_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_PLAY_NEXT_VIDEO_TIME_THRESHOLD_VALUE")
                    Summ_list.append('COBALT_PLAY_NEXT_VIDEO_TIME_THRESHOLD_VALUE :{}ms'.format(cobalt_play_threshold))
                    offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                    if all(value != "" for value in (cobalt_play_threshold,offset)):
                        print "\n Play initiated at {}".format(play_start_time)
                        Summ_list.append('Play initiated at :{}'.format(play_start_time))
                        print "\n Play happend at {}".format(video_playedtime)
                        Summ_list.append('Play happend at :{}'.format(video_playedtime))
                        print "\n Time taken for play operation: {} milliseconds \n".format(time_for_video_play)
                        Summ_list.append('Time taken for play operation :{}ms'.format(time_for_video_play))
                        print "\n Threshold value for Time taken for playing next video: {} milliseconds \n".format(cobalt_play_threshold)
                        if 0 < int(time_for_video_play) < (int(cobalt_play_threshold) + int(offset)):
                            print "\n Time taken for play operation is within the expected limit"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Time taken for play operation is not within the expected limit"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Please configure the threshold values in device config file"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to find video playback logs from DUT"
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while playing video in Cobalt"
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
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
