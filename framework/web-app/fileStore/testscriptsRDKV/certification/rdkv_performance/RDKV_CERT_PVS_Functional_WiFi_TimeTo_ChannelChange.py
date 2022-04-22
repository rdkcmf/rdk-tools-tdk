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
  <name>RDKV_CERT_PVS_Functional_WiFi_TimeTo_ChannelChange</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the time taken for channel change when connected to Wifi</synopsis>
  <groups_id/>
  <execution_time>12</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_25</test_case_id>
    <test_objective>The objective of this test is to get the time taken for channel change when connected to Wifi</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with WiFi IP in test manager or WiFi Access point with same IP range is required.
2. Lightning application for ip change detection should be already hosted.
3. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string
channel change app url :string
webinspect port : string
</input_parameters>
    <automation_approch>1. Check the current active interface of DUT and if it is already WIFI then validate the channel change time
2.a) If current active interface is ETHERNET, enable the WIFI interface.
b) Connect to SSID
c) Launch Lightning app for detecting IP change in WebKitBrowser
d) Set WIFI as default interface
3. validate channel change time by listening to the webinspect port.
4. Check logs for playing event 
5. Find the channel change time for 5  channel changes and find the average time
6. Revert the values</automation_approch>
    <expected_output>Device should work fine even the interface is WiFi.
Channel change time should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_WiFi_TimeTo_ChannelChange</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from ip_change_detection_utility import *
from web_socket_util import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_WiFi_TimeTo_ChannelChange');

webkit_console_socket = None
channel_change_count = 1
max_channel_change_count = 5
#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert_plugins_dict = {}
    revert_if  = revert_device_info = revert_plugins = "NO"
    #Check current interface
    current_interface,revert_nw = check_current_interface(obj)
    if revert_nw == "YES":
        revert_plugins_dict = {"org.rdk.Network":"deactivated"}
    if current_interface == "EMPTY":
        status = "FAILURE"
    elif current_interface == "ETHERNET":
        revert_if = "YES"
        wifi_connect_status,plugins_status_dict,revert_plugins = switch_to_wifi(obj)
        if revert_plugins == "YES":
            revert_plugins_dict.update(plugins_status_dict)
        if wifi_connect_status == "FAILURE":
            status = "FAILURE"
    else:
        print "\n Current interface is WIFI \n"
        webkit_instance = PerformanceTestVariables.webkit_instance
        set_method = webkit_instance+'.1.url'
        if webkit_instance in "WebKitBrowser":
            webinspect_port = PerformanceTestVariables.webinspect_port
        elif webkit_instance in "LightningApp":
            webinspect_port = PerformanceTestVariables.lightning_app_webinspect_port
        else:
            webinspect_port = PerformanceTestVariables.html_app_webinspect_port
        webkit_status = get_plugins_status(obj,[webkit_instance])
        webkit_status = webkit_status[webkit_instance]
        if webkit_status != "resumed":
            status = set_plugins_status(obj,{webkit_instance:"resumed"})
            revert_plugins_dict[webkit_instance] = "deactivated"
    if status == "SUCCESS":
        if revert_if == "YES":
            closed_status = close_lightning_app(obj)
            time.sleep(10)
        channel_change_url = PerformanceTestVariables.channel_change_url
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL "
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_webkit_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_webkit_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(obj.IP,webinspect_port,[],"/devtools/page/1",False)
            time.sleep(60)
            print "Current URL:",current_webkit_url
            print "\nSet Channel change test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",channel_change_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if new_url == channel_change_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    validate = False
                    continue_count = 0
                    check_log_for = "tune"
                    check_play_count = 0
                    error_msg = ""
                    total_time = 0
                    while True:
                        if (channel_change_count > max_channel_change_count) or (continue_count > 20):
                            validate = not(continue_count > 20)
                            break
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            continue_count += 1
                            time.sleep(1)
                            continue
                        console_log = webkit_console_socket.getEventsBuffer().pop(0)
                        if check_log_for == "tune":
                            print "checking for Tuning event"
                            #checking whether Tuning print is coming
                            tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
                            tdkTestObj.addParameter('log',console_log)
                            tdkTestObj.addParameter('text','Tuning to channel')
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if result_val == "SUCCESS" and expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                continue_count = 0
                                check_log_for = "play"
                        elif check_log_for == "play":
                            print "checking for playing event"
                            #checking for playing event
                            tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
                            tdkTestObj.addParameter('log',console_log)
                            tdkTestObj.addParameter('text','Playing')
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            result_val = tdkTestObj.getResultDetails()
                            if result_val == "SUCCESS" and expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                check_log_for  = "time"
                                check_play_count = 0
                                continue_count = 0
                            else:
                                check_play_count += 1
                                if(check_play_count > 4):
                                    error_msg = "\nNot able to play the content after {} times channel change\n".format(channel_change_count)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                        else:
                            print "\nchecking time taken for channel change"
                            #checking for time taken print
                            tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
                            tdkTestObj.addParameter('log',console_log)
                            tdkTestObj.addParameter('text','channel change')
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if result_val == "SUCCESS" and expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                check_log_for = 'tune'
                                channel_change_log = json.loads(console_log)
                                time_info = channel_change_log.get("params").get("message").get("text")
                                time_taken = int(time_info.split(':')[1].split()[0])
                                print "time_taken :",time_taken
                                total_time += time_taken
                                channel_change_count += 1
                            else:
                                error_msg = "Unable to get the channel change time"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                    if (validate):
                        print "\nSuccessfully completed {} channel changes\n".format(max_channel_change_count)
                        tdkTestObj.setResultStatus("SUCCESS")
                        avg_time = total_time/5
                        print "\nAverage time taken for channel change: {} ms\n".format(avg_time)
                        Summ_list.append('Average time taken for channel change :{}ms'.format(avg_time))
                        conf_file,result = getConfigFileName(tdkTestObj.realpath)
                        result1, channelchange_time_threshold_value = getDeviceConfigKeyValue(conf_file,"CHANNEL_CHANGE_TIME_THRESHOLD_VALUE")
                        Summ_list.append('CHANNEL_CHANGE_TIME_THRESHOLD_VALUE :{}ms'.format(channelchange_time_threshold_value))
                        result2,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        Summ_list.append('THRESHOLD_OFFSET :{}'.format(offset))
                        if all (value != "" for value in (channelchange_time_threshold_value,offset)):
                            print "\n Threshold value for average time taken for channel change : {} ms".format(channelchange_time_threshold_value)
                            if 0 < int(avg_time) < (int(channelchange_time_threshold_value) + int(offset)):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "\n The channel change time is within the expected limit\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "\n The channel change time is not within the expected limit \n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to get the threshold value from config file"
                    elif(continue_count > 20):
                        print "\nchannel change didn't happen after {}channel changes\n".format(channel_change_count)
                        tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print error_msg
                    webkit_console_socket.disconnect()
                    time.sleep(30)
                    #Set the URL back to previous
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method",set_method);
                    tdkTestObj.addParameter("value",current_webkit_url);
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if result == "SUCCESS":
                        print "URL is reverted successfully"
                        tdkTestObj.setResultStatus("SUCCESS");
                        time.sleep(10)
                    else:
                        print "Failed to revert the URL"
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "Failed to load the URL:{}, Current URL:{}".format(channel_change_url,new_url)
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set the URL"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert_if == "YES" and status == "SUCCESS":
        status,complete_url = get_lightning_app_url(obj)
        status = launch_lightning_app(obj,complete_url)
        time.sleep(60)
        interface_status = set_default_interface(obj,"ETHERNET")
        if interface_status == "SUCCESS":
            print "\n Successfully reverted to ETHERNET \n"
            status = close_lightning_app(obj)
        else:
            print "\n Error while reverting to ETHERNET \n"
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

