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
  <name>RDKV_CERT_PACS_WiFi_Cobalt_ResourceUsage_VideoPlayback_5GHZ</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play video in Cobalt with 5GHZ Wi-Fi connected and validate CPU load and memory usage.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_51</test_case_id>
    <test_objective>The objective of this test is to play video in Cobalt with 5GHZ Wi-Fi connected and validate CPU load and memory usage.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with 5GHZ WiFi IP in test manager or 5GHZ WiFi Access point with same IP range is required.
2. Lightning application should be already hosted.
3. Wpeframework process should be up and running in the device.
4. If DUT is RPI, the version must be RPI 3B+ for detecting 5GHZ SSID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Check the current active interface of DUT and if it is already 5GHZ WIFI then,
a) Launch Cobalt using RDKShell.
b) Load a video using Deeplink method
c)  Validate the CPU load and memory usage.
2.a) If current active interface is ETHERNET, enable the WIFI interface.
b) Launch Lightning app for detecting IP change in WebKitBrowser
c) Connect to 5GHZ SSID
d) Set WIFI as default interface
e) Launch Cobalt using RDKShell.
f) Load a video using Deeplink method
g) Validate CPU load and memory usage
3. Revert to the default interface and plugins status</automation_approch>
    <expected_output>If default interface is ETHERNET then DUT should connect to WIFI.
The methods of each plugin must work fine.  
The CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_WiFi_Cobalt_ResourceUsage_VideoPlayback_5GHZ</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from ip_change_detection_utility import *
import PerformanceTestVariables
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_WiFi_Cobalt_ResourceUsage_VideoPlayback_5GHZ');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    connected_to_5ghz = True
    ssid_freq = ""
    revert_wifi_ssid = False
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
        wifi_connect_status,plugins_status_dict,revert_plugins = switch_to_wifi(obj,"5",False)
        if revert_plugins == "YES":
            revert_plugins_dict.update(plugins_status_dict)
        if wifi_connect_status == "FAILURE":
            status = "FAILURE"
    else:
        print "\n Current interface is WIFI \n"
        plugin_status,plugins_status_dict,revert = set_plugins(obj)
        if plugin_status == "SUCCESS":
            revert_plugins_dict.update(plugins_status_dict)
            print "\n Check frequency of Connected SSID"
            ssid_freq = check_cur_ssid_freq(obj)
            if ssid_freq == "FAILURE":
                status = "FAILURE"
        else:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        if current_interface == "WIFI" and ssid_freq == "2.4":
            revert_wifi_ssid = True
            url_status,complete_url = get_lightning_app_url(obj)
            status = launch_lightning_app(obj,complete_url)
            time.sleep(20)
            if "SUCCESS" == (url_status and status):
                connect_wifi_status = connect_wifi(obj,"5")
                if connect_wifi_status == "FAILURE":
                    connected_to_5ghz = False
            else:
                connected_to_5ghz = False
        if connected_to_5ghz:
            #Get DeviceInfo Plugin status
            device_info_activated = False
            plugin = "DeviceInfo"
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
            tdkTestObj.addParameter("plugin",plugin);
            tdkTestObj.executeTestCase(expectedResult);
            device_info_result = tdkTestObj.getResult();
            device_info_status = tdkTestObj.getResultDetails();
            if expectedResult in device_info_result:
                tdkTestObj.setResultStatus("SUCCESS")
                if device_info_status not in "activated":
                    revert_revert_plugins_dict["DeviceInfo"] = "deactivated"
                    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
                    tdkTestObj.addParameter("plugin",plugin);
                    tdkTestObj.addParameter("status","activate");
                    tdkTestObj.executeTestCase(expectedResult);
                    result1 = tdkTestObj.getResult();
                    if expectedResult in result1:
                        print "\n Deviceinfo is activated"
                        tdkTestObj.setResultStatus("SUCCESS")
                        device_info_activated = True
                    else:
                        print "\n Error while activating DeviceInfo"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                   print "\n Device info is in activated state"
                   device_info_activated = True
            else:
                print "\n Error while getting DeviceInfo status"
                tdkTestObj.setResultStatus("FAILURE")
            if device_info_activated:
                if validation_dict["validation_required"]:
                    if validation_dict["password"] == "None":
                        password = ""
                    else:
                        password = validation_dict["password"]
                    credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                if revert_if == "YES":
                    status,start_suspend = suspend_plugin(obj,"WebKitBrowser")
                if status == "SUCCESS":
                    cobal_launch_status = launch_cobalt(obj)
                    time.sleep(30)
                    print "\n Set the URL : {} using Cobalt deeplink method".format(cobalt_test_url)
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                    tdkTestObj.addParameter("value",cobalt_test_url)
                    tdkTestObj.executeTestCase(expectedResult)
                    cobalt_result = tdkTestObj.getResult()
                    time.sleep(10)
                    if(cobalt_result in expectedResult and cobal_launch_status in expectedResult ):
                        tdkTestObj.setResultStatus("SUCCESS")
                        print "Clicking OK to play video"
                        params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result1 = tdkTestObj.getResult()
                        time.sleep(50)
                        #Clicking OK to skip Ad
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result2 = tdkTestObj.getResult()
                        time.sleep(40)
                        if "SUCCESS" == (result1 and result2):
                            result_val = "SUCCESS"
                            if validation_dict["validation_required"]:
                                tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                tdkTestObj.addParameter("credentials",credentials)
                                tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                                tdkTestObj.executeTestCase(expectedResult)
                                result_val = tdkTestObj.getResultDetails()
                                if result_val == "SUCCESS" :
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n Video playback is happening"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print " \n Video playback is not happening"
                            if result_val == "SUCCESS":
                                tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                cpuload = tdkTestObj.getResultDetails()
                                if result == "SUCCESS":
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    #validate the cpuload
                                    tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                    tdkTestObj.addParameter('value',float(cpuload))
                                    tdkTestObj.addParameter('threshold',90.0)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    is_high_cpuload = tdkTestObj.getResultDetails()
                                    if is_high_cpuload == "YES"  or expectedResult not in result:
                                        print "\n CPU load is high :{}%".format(cpuload)
                                        tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "\n CPU load: {}%".format(cpuload)
                                else:
                                    print "\n Unable to get cpuload"
                                    tdkTestObj.setResultStatus("FAILURE")
                                #get the memory usage
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
                                    result = tdkTestObj.getResult()
                                    is_high_memory_usage = tdkTestObj.getResultDetails()
                                    if is_high_memory_usage == "YES" or expectedResult not in result:
                                        print "\n Memory usage is high :{}%".format(memory_usage)
                                        tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "\n Memory usage is {}%".format(memory_usage)
                                else:
                                    print "\n Unable to get the memory usage"
                                    tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Unable to press OK button"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Unable to launch the url"
                        tdkTestObj.setResultStatus("FAILURE")
                    #Deactivate cobalt
                    print "\n Exiting from Cobalt"
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
                    print "\n Precondition to suspend WebKitBrowser didn't work"
            else:
                print "\n Precondition to activate DeviceInfo is not working"
            if revert_wifi_ssid:
                print "\n Reconnecting to 2.4 GHZ SSID"
                connect_wifi_status = connect_wifi(obj,"2.4")
                if connect_wifi_status == "FAILURE":
                    print "\n Error while reconnecting to 2.4 GHZ SSID"
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while connecting to 5GHZ SSID"
            obj.setLoadModuleStatus("FAILURE")
    else:
        print "\n[Error] Preconditions are not met "
        obj.setLoadModuleStatus("FAILURE")
    if revert_if == "YES" and status == "SUCCESS":
        resume_status,start_resume = launch_plugin(obj,"WebKitBrowser")
        time.sleep(60)
        interface_status = set_default_interface(obj,"ETHERNET")
        if interface_status == "SUCCESS" and resume_status == "SUCCESS":
            print "\n Successfully reverted to ETHERNET"
            status = close_lightning_app(obj)
        else:
            print "\n Error while reverting to ETHERNET"
            obj.setLoadModuleStatus("FAILURE")
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
