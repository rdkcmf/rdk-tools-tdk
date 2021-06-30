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
  <version>2</version>
  <name>RDKV_CERT_PVS_Functional_TimeTo_ChannelChange</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The script is to get the time taken for channel change.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_10</test_case_id>
    <test_objective>The objective of the script is to get the time taken for channel change.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>channel_change_url : string,
webinspect_port: string</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the application to change channels for 5 times.
4.Validate the channel change using events.
5. Get the time taken for each channel change.
6. Calculate the average time taken for channel change using the above data.
7. Revert all values
</automation_approch>
    <expected_output>The channel change must happen within expected  range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_ChannelChange</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
import PerformanceTestVariables
from web_socket_util import *
from rdkv_stabilitylib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_ChannelChange');

webkit_console_socket = None
channel_change_count = 1
max_channel_change_count = 5

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    channel_change_url = PerformanceTestVariables.channel_change_url
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        if "FAILURE" not in (curr_webkit_status,curr_cobalt_status):
            set_status =set_pre_requisites(obj)
            #Need to revert the values since we are changing plugin status
            revert="YES"
            if set_status == "SUCCESS":
                status,webkit_status,cobalt_status = check_pre_requisites(obj)
            else:
                status = "FAILURE";
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,PerformanceTestVariables.webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "Current URL:",current_url
            print "\nSet Channel change test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",channel_change_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
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
                        conf_file,result = getConfigFileName(tdkTestObj.realpath)
                        result1, channelchange_time_threshold_value = getDeviceConfigKeyValue(conf_file,"CHANNEL_CHANGE_TIME_THRESHOLD_VALUE")
                        result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        if all(value != "" for value in (channelchange_time_threshold_value,offset)):
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
                    print "Failed to load the URL:{}, Current URL:{}".format(channel_change_url,new_url)
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set the URL"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

