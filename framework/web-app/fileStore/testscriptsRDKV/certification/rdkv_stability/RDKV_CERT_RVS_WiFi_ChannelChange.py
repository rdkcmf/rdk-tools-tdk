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
  <version>3</version>
  <name>RDKV_CERT_RVS_WiFi_ChannelChange</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_checkChannelChangeLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do the stability testing by changing the channel for given number of times when the DUT is connected to WiFi.</synopsis>
  <groups_id/>
  <execution_time>170</execution_time>
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
    <test_case_id>RDKV_STABILITY_12</test_case_id>
    <test_objective>The objective of this test is to do the stability testing by changing the channel for given number of times when the DUT is connected to WiFi.</test_objective>
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
webinspect port : string</input_parameters>
    <automation_approch>1. Check the current active interface of DUT and if it is already WIFI then validate the channel changes
2.a) If current active interface is ETHERNET, enable the WIFI interface.
b) Connect to SSID
c) Launch Lightning app for detecting IP change in WebKitBrowser
d) Set WIFI as default interface
3. validate channel changes by listening to the webinspect port.
4. Check logs for playing event 
5. Validate CPU load and memory usage of each iteration.
6. Revert the values and interface </automation_approch>
    <expected_output>Device should work fine even the interface is WiFi.
CPU load and memory usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_WiFi_ChannelChange</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
import StabilityTestVariables
from web_socket_util import *
from StabilityTestUtility import *
from ip_change_detection_utility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_WiFi_ChannelChange');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

webkit_console_socket = None
channel_change_count = 1
max_channel_change_count = StabilityTestVariables.max_channel_change_count
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
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugin_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    plugins_cur_status_dict = get_plugins_status(obj,plugin_list)
    time.sleep(10)
    plugin_required_status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if any(plugins_cur_status_dict[plugin] == "FAILURE" for plugin in plugin_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif plugin_status_needed != plugins_cur_status_dict :
        revert = "YES"
        plugin_required_status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        plugins_status_after_set = get_plugins_status(obj,plugin_list)
        if plugins_status_after_set == plugin_status_needed:
            plugin_required_status = "SUCCESS"
        else:
            plugin_required_status = "FAILURE"
        revert_plugins_dict.update(plugins_cur_status_dict)
    if status == "SUCCESS" and plugin_required_status == "SUCCESS":
        if revert_if == "YES":
            closed_status = close_lightning_app(obj)
            time.sleep(10)
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        current_url = tdkTestObj.getResultDetails();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(obj.IP,StabilityTestVariables.webinspect_port,[],"/devtools/page/1",False)
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
                validate = False
                continue_count = 0
                check_channel_tune = True
                check_play_count = 0
                error_msg = ""
                while True:
                    result_dict = {}
                    if (channel_change_count > max_channel_change_count) or (continue_count > 20):
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
                    print "\nSuccessfully completed {} channel changes\n".format(max_channel_change_count)
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
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
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
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

