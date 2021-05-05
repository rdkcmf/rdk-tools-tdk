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
  <name>RDKV_CERT_RVS_FastChannelChange</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to change channel continuously without delay for 1000 times and check the stability of device.</synopsis>
  <groups_id/>
  <execution_time>600</execution_time>
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
    <test_case_id>RDKV_STABILITY_35</test_case_id>
    <test_objective>The objective of this test is to change channel continuously without delay for 1000 times and check the stability of device.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Enable WebkitBrowser plugin
2. Start listening for webinspect console logs.
3. Load the fast channel change application in WebKit.
4. Check whether channel change is happening in frequent intervals using console prints from webinspect page.
5. After 1000 channel changes check whether channel is playing.
6. Validate CPU load and memory usage after 1000 iterations
7. Close the application and disable the WebKitBrowser</automation_approch>
    <expected_output>DUT should be stable and video must be playing after 1000 channel changes.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_FastChannelChange</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from web_socket_util import *
from StabilityTestUtility import *
import StabilityTestVariables
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_FastChannelChange');

webkit_console_socket = None
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    channel_change_url = obj.url+'/fileStore/lightning-apps/FastChannelChangeTest.html'
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugin_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    plugins_cur_status_dict = get_plugins_status(obj,plugin_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if plugin_status_needed != plugins_cur_status_dict :
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugin_status = get_plugins_status(obj,plugin_list)
        if new_plugin_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        current_url = tdkTestObj.getResultDetails();
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
            print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            result1 = tdkTestObj.getResult()
            new_url = tdkTestObj.getResultDetails();
            if new_url == channel_change_url and expectedResult == (result and result1):
                tdkTestObj.setResultStatus("SUCCESS");
                print "URL(",new_url,") is set successfully"
                continue_count = 0
                channel_count = 0
                max_channel_change_count = 1000
                while channel_count < max_channel_change_count:
                    if continue_count > 120:
                        print "\n Channel change is not working"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                    if (len(webkit_console_socket.getEventsBuffer())== 0):
                        continue_count += 1
                        time.sleep(2)
                        continue
                    console_log = webkit_console_socket.getEventsBuffer().pop(0)
                    tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
                    tdkTestObj.addParameter('log',console_log)
                    tdkTestObj.addParameter('text','Count')
                    tdkTestObj.executeTestCase(expectedResult)
                    result_val = tdkTestObj.getResultDetails()
                    if result_val == "SUCCESS":
                        continue_count = 0
                        tdkTestObj.setResultStatus("SUCCESS")
                        channel_count_log = json.loads(console_log)
                        channel_count_params  = channel_count_log.get("params").get("message").get("parameters")
                        for parameter in channel_count_params:
                            if parameter["type"] == "number":
                                channel_count = parameter["value"]
                        print "\n Channel change count: ",channel_count
                    else:
                        continue_count += 1
                        continue
                else:
                    print "\n Check channel is playing after {} channel changes \n".format(max_channel_change_count)
                    time.sleep(10)
                    if (len(webkit_console_socket.getEventsBuffer())!= 0):
                        for event in webkit_console_socket.getEventsBuffer():
                            if "Playing" in event:
                                print "\n Channel is playing after {} channel changes\n".format(max_channel_change_count)
                                channel_change_log = json.loads(event)
                                remarks = channel_change_log.get("params").get("message").get("text")
                                print "\n Validate CPU load and memory usage \n"
                                tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                cpuload = tdkTestObj.getResultDetails()
                                if (result == "SUCCESS"):
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    #validate the cpuload
                                    tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                    tdkTestObj.addParameter('value',float(cpuload))
                                    tdkTestObj.addParameter('threshold',90.0)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult();
                                    is_high_cpuload = tdkTestObj.getResultDetails()
                                    if is_high_cpuload == "YES" or  expectedResult not in result:
                                        print "\n CPU load is high :{}% after channel change :{} times\nchannel_info:{}\n".format(cpuload,max_channel_change_count,remarks)
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                    else:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "\ncpu load is:{}% after channel change: {} times\n".format(cpuload,max_channel_change_count)
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print "\nUnable to get cpuload\n"
                                    break
                                tdkTestObj = obj.createTestStep('rdkservice_getMemoryUsage')
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                memory_usage = tdkTestObj.getResultDetails()
                                if (result == "SUCCESS"):
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    #validate memory usage
                                    tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
                                    tdkTestObj.addParameter('value',float(memory_usage))
                                    tdkTestObj.addParameter('threshold',90.0)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    is_high_memory_usage = tdkTestObj.getResultDetails()
                                    result  =  tdkTestObj.getResult()
                                    if is_high_memory_usage == "YES" or expectedResult not in result:
                                        print "\n Memory usage is high :{} % after channel change:{} times\nchannel_info:{}\n".format(memory_usage,max_channel_change_count,remarks)
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                    else:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "\n Memory usage is {}% after channel change {} times\n".format(memory_usage,max_channel_change_count)
                                else:
                                    print "\n Unable to get the memory usage\n"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                print "\n Successfully completed the {} channel changes".format(max_channel_change_count)
                                break
                            else:
                                continue
                        else:
                            print "\n Channel is not playing after {} channel changes \n".format(max_channel_change_count)
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n No events are available in the application console\n"
                        tdkTestObj.setResultStatus("FAILURE")
                webkit_console_socket.disconnect()
                time.sleep(5)
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
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,plugins_cur_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
