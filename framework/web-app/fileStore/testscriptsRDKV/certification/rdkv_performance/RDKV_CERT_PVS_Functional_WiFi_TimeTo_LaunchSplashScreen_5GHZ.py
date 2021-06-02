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
  <name>RDKV_CERT_PVS_Functional_WiFi_TimeTo_LaunchSplashScreen_5GHZ</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The script is to get the time to launch the splash screen after reboot, when the DUT is connected to 5GHZ Wi-Fi SSID.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_49</test_case_id>
    <test_objective>The script is to get the time to launch the splash screen after reboot, when the DUT is connected to 5GHZ Wi-Fi SSID.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with 5GHZ WiFi IP in test manager or WiFi Access point with same IP range is required.
2. Lightning application for ip change detection should be already hosted.
3. Wpeframework process should be up and running in the device.
4. If DUT is RPI, the version must be RPI 3B+ for detecting 5GHZ SSID.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Check the current active interface of DUT and if it is already WIFI then validate the Splash screen launch time.
2.a) If current active interface is ETHERNET, enable the WIFI interface.
b) Launch Lightning app for detecting IP change in WebKitBrowser
c) Connect to  5GHZ SSID
d) Set WIFI as default interface
3. Reboot the device after saving current time
4. Get the Resident app URL from the DUT
5. Check for the load finished log for above URL in wpeframework log
6. Find the time taken to launch UI by finding the difference between load finished log time stamp and time saved before reboot.
7. Validate the result against threshold value
8. Revert the interface </automation_approch>
    <expected_output>The splash screen launch time should be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_WiFi_TimeTo_LaunchSplashScreen_5GHZ</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestVariables import *
import rebootTestUtility
from rebootTestUtility import *
from datetime import datetime
import time
from rdkv_performancelib import *
from ip_change_detection_utility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_WiFi_TimeTo_LaunchSplashScreen_5GHZ');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    revert_plugins_dict = {}
    connected_to_5ghz = True
    ssid_freq = ""
    revert_wifi_ssid = False
    plugins_status_needed = {"org.rdk.Network":"activated","WebKitBrowser":"activated"}
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
        time.sleep(20)
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
    if status == "SUCCESS":
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
            tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
            tdkTestObj.addParameter("waitTime",rebootwaitTime)
            #get the current system time before reboot
            start_time = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Rebooted device successfully \n"
                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo")
                tdkTestObj.addParameter("reqValue","uptime")
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    uptime = int(tdkTestObj.getResultDetails())
                    if uptime < 240:
                        print "\n Device is rebooted and uptime is: {} \n".format(uptime)
                        time.sleep(60)
                        tdkTestObj.setResultStatus("SUCCESS")
                        tdkTestObj = obj.createTestStep('rdkservice_getValue');
                        tdkTestObj.addParameter("method","ResidentApp.1.url");
                        tdkTestObj.executeTestCase(expectedResult);
                        ui_app_url = tdkTestObj.getResultDetails();
                        result = tdkTestObj.getResult()
                        if ui_app_url != "" and  result == "SUCCESS" :
                            print "\n Resident App URL :",ui_app_url
                            ui_app_url = ui_app_url.split('#')[0]
                            print "\n URL to check in device logs: ",ui_app_url
                            tdkTestObj.setResultStatus("SUCCESS")
                            tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                            tdkTestObj.addParameter("realpath",obj.realpath)
                            tdkTestObj.addParameter("deviceIP",obj.IP)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                            if ssh_param_dict != {} and expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                command = 'cat /opt/logs/wpeframework.log | grep -inr LoadFinished.*url.*'+ui_app_url+'.*splash.*| tail -1'
                                #get the log line containing the loadfinished info from wpeframework log
                                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                tdkTestObj.addParameter("command",command)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                output = tdkTestObj.getResultDetails()
                                if output != "EXCEPTION" and expectedResult in result:
                                    print "\n Output: " + output + "\n"
                                    load_finished_list = output.split('\n')
                                    load_finished_line = ""
                                    for item in load_finished_list:
                                        if "LoadFinished:" in item:
                                            load_finished_line = item
                                    if load_finished_line != "" and '"httpstatus":200' in load_finished_line:
                                        load_finished_time = getTimeStampFromString(load_finished_line)
                                        print "\n Device reboot initiated at :{} (UTC)".format(start_time)
                                        print "\n UI load finished at :{} (UTC)".format(load_finished_time)
                                        start_time_millisec = getTimeInMilliSec(start_time)
                                        loadfinished_time_millisec = getTimeInMilliSec(load_finished_time)
                                        ui_uptime = loadfinished_time_millisec - start_time_millisec
                                        print "\n Time taken for the UI to load after reboot : {} ms".format(ui_uptime)
                                        conf_file,result = getConfigFileName(tdkTestObj.realpath)
                                        result1, ui_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"UI_LAUNCH_TIME_THRESHOLD_VALUE")
                                        result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                        if all(value != "" for value in (ui_launch_threshold_value,offset)):
                                            if 0 < int(ui_uptime) < (int(ui_launch_threshold_value) + int(offset)) :
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "\n The time taken for UI to load after reboot is within the expected limit"
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "\n The time taken for UI to load after reboot is not within the expected limit"
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "\n Failed to get the threshold value from config file"
                                    else:
                                        print "\n Splash screen url is not loaded in DUT"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error occurred while executing the command:{} in DUT,\n Please check the SSH details".format(command)
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n please configure the details in device config file"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error while executing ResidentApp.1.url method"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print "\n Device is not rebooted, device uptime:{}".format(uptime)
                else:
                    print "\n Failed to get the uptime";
                    tdkTestObj.setResultStatus("FAILURE")
                if revert_wifi_ssid:
                    print "\n Reconnecting to 2.4 GHZ SSID"
                    plugin_status,plugins_status_dict,revert = set_plugins(obj)
                    time.sleep(5)
                    connect_wifi_status = connect_wifi(obj,"2.4")
                    if connect_wifi_status == "FAILURE":
                        print "\n Error while reconnecting to 2.4 GHZ SSID"
                        tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error occurred during reboot"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while connecting to 5GHZ SSID"
            obj.setLoadModuleStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
    if revert_if == "YES" and status == "SUCCESS":
        activate_status = set_plugins_status(obj,plugins_status_needed)
        url_status,complete_url = get_lightning_app_url(obj)
        lauch_app_status = launch_lightning_app(obj,complete_url)
        time.sleep(60)
        if all(status == "SUCCESS" for status in (activate_status,url_status,lauch_app_status)):
            interface_status = set_default_interface(obj,"ETHERNET")
            if interface_status  == "SUCCESS":
                print "\n Successfully reverted to ETHERNET"
                status = close_lightning_app(obj)
            else:
                print "\n Error while reverting to ETHERNET"
        else:
            print "\n Error while launching Lightning App"
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
