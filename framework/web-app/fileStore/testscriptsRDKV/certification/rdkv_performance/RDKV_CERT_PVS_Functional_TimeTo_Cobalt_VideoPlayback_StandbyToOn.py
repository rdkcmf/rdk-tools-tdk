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
  <version>2</version>
  <name>RDKV_CERT_PVS_Functional_TimeTo_Cobalt_VideoPlayback_StandbyToOn</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get time to start playback in cobalt from standby mode.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_35</test_case_id>
    <test_objective>The objective of this test is to get time to start playback in cobalt from standby mode.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Time in Test Manager should be in sync with UTC time
2. wpeframework should be running in DUT.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. As a prerequisite enable System plugin disable WebKit and Cobalt plugins.
2. Get the current power state.
3. Get the preferred standby mode and if it is not LIGHT_SLEEP set it to LIGHT_SLEEP.
4. Launch Cobalt using RDKShell and load a video URL using deeplink method.
5. Click OK using generatekey method.
6. Verify video playback using wpeframework log
7. Set the power state to STANDBY
8. Set the power state to ON after storing the current system time
6. Get the event logs from wpeframework log and parse the time stamp 
7. Calculate the result by finding the difference between system time stored and time stamp of event
8. Revert values</automation_approch>
    <expected_output>Device's power state should be changed.
The time should be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_Cobalt_VideoPlayback_StandbyToOn</test_script>
    <skipped>No</skipped>
    <release_version>M87</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from datetime import datetime
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import json
import rdkv_performancelib
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_Cobalt_VideoPlayback_StandbyToOn');

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
    print "Check Pre conditions"
    continue_count = 0
    event_listener = None
    power_state = ""
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url;
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url value\n"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","org.rdk.System"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","org.rdk.System":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and expectedResult in result and ssh_param_dict != {} and cobalt_test_url != "":
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "org.rdk.System.1.register","params": {"event": "onSystemPowerStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(10)
        print "\nPre conditions for the test are set successfully"
        print "\n Get the current power state: \n"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
        tdkTestObj.addParameter("reqValue","powerState")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        current_power_state = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Current power state : \n",current_power_state
            print "\n Set Preferred standby mode as LIGHT_SLEEP \n"
            params = '{"standbyMode":"LIGHT_SLEEP"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\n SetPreferredStandbyMode is success \n"
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Invoke org.rdk.System.1.getPreferredStandbyMode \n"
                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
                tdkTestObj.addParameter("reqValue","preferredStandbyMode")
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                preferred_standby = tdkTestObj.getResultDetails()
                if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
                    print "\n Preferred standby mode is LIGHT_SLEEP \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                    cobal_launch_status = launch_cobalt(obj)
                    time.sleep(30)
                    if cobal_launch_status == "SUCCESS":
                        print "\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url)
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                        tdkTestObj.addParameter("value",cobalt_test_url)
                        tdkTestObj.executeTestCase(expectedResult)
                        cobalt_result = tdkTestObj.getResult()
                        time.sleep(10)
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
                            #Skip if Ad is playing by pressing OK
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
                                print output
                                if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                    playing_log = output.split('\n')[1]
                                    video_starttime_in_millisec = getTimeInMilliSec(video_start_time)
                                    video_playedtime = getTimeStampFromString(playing_log)
                                    video_playedtime_in_millisec = getTimeInMilliSec(video_playedtime)
                                    if video_playedtime_in_millisec > video_starttime_in_millisec:
                                        print "\n Video started playing \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        power_states = ["STANDBY","ON"]
                                        time.sleep(5)
                                        power_on_time = ""
                                        for i in range (0,2):
                                            print "\n Set power state to {} \n".format(power_states[i])
                                            params = '{"powerState":"'+power_states[i]+'", "standbyReason":"APIUnitTest"}'
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                                            tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                                            tdkTestObj.addParameter("value",params);
                                            if power_states[i] == "ON":
                                                start_power_on = str(datetime.utcnow()).split()[1]
                                            tdkTestObj.executeTestCase(expectedResult);
                                            result = tdkTestObj.getResult();
                                            if expectedResult in result:
                                                time.sleep(10)
                                                while True:
                                                    if (continue_count > 60):
                                                        break
                                                    if (len(event_listener.getEventsBuffer())== 0):
                                                        continue_count += 1
                                                        time.sleep(1)
                                                        continue
                                                    event_log = event_listener.getEventsBuffer().pop(0)
                                                    print "\n Triggered event: ",event_log
                                                    if (power_states[i] == "STANDBY" and ("LIGHT_SLEEP" in event_log or "STANDBY" in event_log)) or (power_states[i] == "ON" and "ON" in event_log):
                                                        print "\n Event: onSystemPowerStateChanged triggered while setting {} power state".format(power_states[i])
                                                        break
                                                    else:
                                                        continue_count = 61
                                                if continue_count > 60 :
                                                    print "\n Event: onSystemPowerStateChanged is not triggered for power state: {} \n".format(power_states[i])
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    break
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print "\n Verify the Power state \n"
                                                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                                                tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                                                tdkTestObj.addParameter("reqValue","powerState")
                                                tdkTestObj.executeTestCase(expectedResult)
                                                result = tdkTestObj.getResult()
                                                power_state = tdkTestObj.getResultDetails()
                                                if expectedResult in result:
                                                    if power_state == power_states[i]:
                                                        print "\n Successfully set power state to : {}\n".format(power_states[i])
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        if power_state == "ON":
                                                            time.sleep(60)
                                                            print "\n Check video is started \n"
                                                            command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                                            tdkTestObj.addParameter("command",command)
                                                            tdkTestObj.executeTestCase(expectedResult)
                                                            result = tdkTestObj.getResult()
                                                            output = tdkTestObj.getResultDetails()
                                                            print output
                                                            if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                                                playing_log = output.split('\n')[1]
                                                                start_poweron_time_in_millisec = getTimeInMilliSec(start_power_on)
                                                                print "\n Set power state to ON from STANDBY at: {} UTC \n".format(start_power_on)
                                                                video_playedtime = getTimeStampFromString(playing_log)
                                                                video_playedtime_in_millisec = getTimeInMilliSec(video_playedtime)
                                                                print "\n Video started playing at: {} UTC \n".format(video_playedtime)
                                                                time_to_video_playfrom_standby = video_playedtime_in_millisec-start_poweron_time_in_millisec
                                                                print "\n Time taken to play video  :{} ms\n".format(time_to_video_playfrom_standby)
                                                                conf_file,file_status = getConfigFileName(obj.realpath)
                                                                result1, video_lauch_threshold_value = getDeviceConfigKeyValue(conf_file,"VIDEOPLAY_FROM_STANDBY_THRESHOLD_VALUE")
                                                                Summ_list.append('VIDEOPLAY_FROM_STANDBY_THRESHOLD_VALUE :{}ms'.format(video_lauch_threshold_value))
                                                                result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                                                Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                                                Summ_list.append('Time taken to play video :{}ms'.format(time_to_video_playfrom_standby))
                                                                if all(value != "" for value in (video_lauch_threshold_value,offset)):
                                                                    print "\n Threshold value for time taken to play video from standby : {} ms".format(video_lauch_threshold_value)
                                                                    if 0 < int(time_to_video_playfrom_standby) < (int(video_lauch_threshold_value) + int(offset)):
                                                                        print "\n The time taken to play video from standby is within the expected limit\n"
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                    else:
                                                                        print "\n The time taken to play video from standby is not within the expected limit \n"
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        break
                                                                else:
                                                                    print "\n Failed to get the threshold value from config file"
                                                                    tdkTestObj.setResultStatus("FAILURE");
                                                                    break
                                                            else:
                                                                print "\n Unable to find logs related to video playback from wpeframework.log \n"
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                break
                                                    else:
                                                        print "\n Unable to set the powerstate to : {}, current power state:{}\n".format(power_states[i],power_state)
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                                else:
                                                    print "\n Error while executing org.rdk.System.1.getPowerState method \n"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    break
                                            else:
                                                print "\n Error while executing org.rdk.System.1.setPowerState method \n"
                                                tdkTestObj.setResultStatus("FAILURE")
                                                break
                                        if continue_count > 60 or power_state != current_power_state:
                                            print "Reverting the Power state \n"
                                            print "\n Set power state to {} \n".format(current_power_state)
                                            params = '{"powerState":"'+current_power_state+'", "standbyReason":"APIUnitTest"}'
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                                            tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                                            tdkTestObj.addParameter("value",params);
                                            tdkTestObj.executeTestCase(expectedResult);
                                            result = tdkTestObj.getResult();
                                            if expectedResult in result:
                                                print "Reverted the power state to {}\n".format(current_power_state)
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            else:
                                                print "\n Error while reverting the power state to {}\n".format(current_power_state)
                                                tdkTestObj.setResultStatus("FAILURE")
                                        
                                    else:
                                        print "\n Video is not started playing \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Unable to find logs related to video playback from wpeframework.log \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while executing generatekey method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error while executing deeplink method of Cobalt \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while lauching Cobalt \n"
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
                        print "\n Unable to deactivate Cobalt"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing org.rdk.System.1.getPreferredStandbyMode method \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing org.rdk.System.1.setPreferredStandbyMode method \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while executing org.rdk.System.1.getPowerState method \n"
            tdkTestObj.setResultStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(5)
        getSummary(Summ_list)
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
