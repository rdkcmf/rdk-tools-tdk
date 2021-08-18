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
  <version>5</version>
  <name>RDKV_CERT_RVS_LongDuration_ChannelChange</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_checkChannelChangeLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to load the channel change URL and runs for given time and validate CPU load and memory usage.</synopsis>
  <groups_id/>
  <execution_time>730</execution_time>
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
    <test_case_id>RDKV_STABILITY_08</test_case_id>
    <test_objective>The objective of this test is to do the stability testing by changing the channel for given time duration</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Channel change URL
2. Webinspect port</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the application to change channels for a given time.
4.Validate the channel change using events
5. Check if the CPU load and Memory usage is within the expected value.
6.Revert all values before exiting</automation_approch>
    <expected_output>Channel should change for given time. The cpu load and memory usage must be within the expected values.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_LongDuration_ChannelChange</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import StabilityTestVariables
from StabilityTestUtility import *
from rdkv_performancelib import *
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_LongDuration_ChannelChange');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

webkit_console_socket = None
channel_change_count = 1
output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    channel_change_url = StabilityTestVariables.channel_change_url
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
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
            webkit_console_socket = createEventListener(ip,StabilityTestVariables.webinspect_port,[],"/devtools/page/1",False)
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
                    check_channel_tune = True
                    check_play_count = 0
                    error_msg = ""
                    test_time_in_mins = StabilityTestVariables.channel_change_duration
                    test_time_in_millisec = test_time_in_mins * 60000
                    time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                    while True:
                        result_dict = {}
                        if (int(round(time.time() * 1000)) > time_limit ) or (continue_count > 20):
                            validate = not(continue_count > 20)
                            break
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            continue_count += 1
                            time.sleep(1)
                            continue
                        console_log = webkit_console_socket.getEventsBuffer().pop(0)
                        if check_channel_tune == True:
                            #checking whether Tuning print is coming
                            tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
                            tdkTestObj.addParameter('log',console_log)
                            tdkTestObj.addParameter('text','Tuning to channel')
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                            if result_val == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                check_channel_tune = False
                                channel_change_log = json.loads(console_log)
                                remarks = channel_change_log.get("params").get("message").get("text")
                                continue
                        else:
                            #checking for playing event
                            tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
                            tdkTestObj.addParameter('log',console_log)
                            tdkTestObj.addParameter('text','Playing')
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                            if result_val == "SUCCESS":
	            	        tdkTestObj.setResultStatus("SUCCESS")
                                check_channel_tune = True
                                check_play_count = 0
                                continue_count = 0
				print "\n ##### Validating CPU load and memory usage #####\n"
            			print "Iteration : ", channel_change_count
            			tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            			tdkTestObj.executeTestCase(expectedResult)
            			status = tdkTestObj.getResult()
            			result = tdkTestObj.getResultDetails()
            			if expectedResult in status and result != "ERROR":
            			    tdkTestObj.setResultStatus("SUCCESS")
            			    cpuload = result.split(',')[0]
            			    memory_usage = result.split(',')[1]
                                    result_dict["iteration"] = channel_change_count
                                    result_dict["remarks"] = remarks
                                    result_dict["cpu_load"] = float(cpuload)
                                    result_dict["memory_usage"] = float(memory_usage)
                                    result_dict_list.append(result_dict)
				else:
				    print "\n Error while validating Resource usage"
                		    tdkTestObj.setResultStatus("FAILURE")
                		    break
                                channel_change_count += 1
                            else:
                                check_play_count += 1
                                if(check_play_count > 4):
                                    error_msg = "\nNot able to play the content after {} times channel change,remarks: {}\n".format(channel_change_count,remarks)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                    if (validate):
                        print "\nSuccessfully completed {} channel changes in {} minutes\n".format(channel_change_count-1,test_time_in_mins)
                        tdkTestObj.setResultStatus("SUCCESS")
                    elif(continue_count > 20):
                        print "\nchannel change didn't happen after {}channel changes\n".format(channel_change_count)
                        tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print error_msg
                    webkit_console_socket.disconnect()
                    cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                    json.dump(cpu_mem_info_dict,json_file)
                    json_file.close()
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
                tdkTestObj.setResultStatus("FAILURE")
                print "Failed to set the URL"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE");

