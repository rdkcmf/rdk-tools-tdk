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
  <name>RDKV_CERT_PVS_Functional_TimeTo_WiFi_InterfaceUp_5GHZ</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to find the time to get the wlan0 interface IP after reboot, when connected to 5GHZ SSID.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_50</test_case_id>
    <test_objective>The objective of this test is to find the time to get the wlan0 interface IP after reboot, when connected to 5GHZ SSID.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with 5GHZ WiFi IP in test manager or 5GHZ WiFi Access point with same IP range is required.
2. Lightning application for ip change detection should be already hosted.
3. Time in TM  and DUT should be in sync with UTC.
4. Wpeframework process should be up and running in the device.
5. If DUT is RPI, the version must be RPI 3B+ for detecting 5GHZ SSID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Load Lightning app in WebKitBrowser
2. Connect to 5GHZ Wi-Fi SSID
3. Set default interface as Wi-Fi
4. Reboot the device
5. Check for the  log for the time taken to get the wlan0 IP.
6. The time must be less than the given threshold +offset and greater than 0.
6. Revert everything back</automation_approch>
    <expected_output>The Lightning app should be launched.
The time taken should be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_WiFi_InterfaceUp_5GHZ</test_script>
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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_WiFi_InterfaceUp_5GHZ');

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
        print "\n Current interface is WIFI"
        plugin_status,plugins_status_dict,revert = set_plugins(obj)
        if plugin_status == "SUCCESS":
            revert_plugins_dict.update(plugins_status_dict)
            print "\n Check frequency of connected SSID"
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
                print "\n Rebooted device successfully"
                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo")
                tdkTestObj.addParameter("reqValue","uptime")
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    uptime = int(tdkTestObj.getResultDetails())
                    if uptime < 240:
                        print "\n Device is rebooted and uptime is: {}".format(uptime)
                        time.sleep(30)
                        tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                        tdkTestObj.addParameter("realpath",obj.realpath)
                        tdkTestObj.addParameter("deviceIP",obj.IP)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                        if ssh_param_dict != {} and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            command = 'cat /opt/logs/netsrvmgr.log | grep eventInterfaceIPAddressStatusChanged.*interface=wlan0.*acquired=1 | head -n 1'
                            #get the log line containing the wlan0 up
                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                            tdkTestObj.addParameter("command",command)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            output = tdkTestObj.getResultDetails()
                            if output != "EXCEPTION" and expectedResult in result:
                                if len(output.split('\n')) == 3 and "eventInterfaceIPAddressStatusChanged:" in output:
                                    print "\n Required logs:",output
                                    interface_up_line = output.split('\n')[1]
                                    interface_up_time = getTimeStampFromString(interface_up_line)
                                    print "\n Device reboot initiated at :{} (UTC)".format(start_time)
                                    Summ_list.append('Device reboot initiated at :{}'.format(start_time))
                                    print "\n wlan0 interface became up  at :{} (UTC)  ".format(interface_up_time)
                                    Summ_list.append('wlan0 interface became up  at  :{}'.format(interface_up_time))
                                    start_time_millisec = getTimeInMilliSec(start_time)
                                    interface_up_time_millisec = getTimeInMilliSec(interface_up_time)
                                    interface_uptime = interface_up_time_millisec - start_time_millisec
                                    print "\n Time taken for the wlan0 interface to up after reboot : {} ms".format(interface_uptime)
                                    Summ_list.append('Time taken for the wlan0 interface to up after reboot :{}'.format(interface_uptime))
                                    conf_file,result = getConfigFileName(tdkTestObj.realpath)
                                    result1, if_uptime_threshold_value = getDeviceConfigKeyValue(conf_file,"WLAN0_IF_UPTIME_THRESHOLD_VALUE")
                                    Summ_list.append('WLAN0_IF_UPTIME_THRESHOLD_VALUE :{}ms'.format(if_uptime_threshold_value))
                                    result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                    if all(value != "" for value in (if_uptime_threshold_value,offset)):
                                        print "\n Threshold value for time taken for wlan0 interface to up after reboot: {} ms".format(if_uptime_threshold_value)
                                        if 0 < int(interface_uptime) < (int(if_uptime_threshold_value) + int(offset)):
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "\n The time taken for wlan0 interface to up after reboot is within the expected limit"
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "\n The time taken for wlan0 interface to up after reboot is not within the expected limit"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "\n Failed to get the threshold value from config file"
                                else:
                                    print "\n wlan0 interface up related logs are not present in log file"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error occurred while executing the command:{} in DUT,\n Please check the SSH details".format(command)
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Please configure the details in device config file"
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
        obj.setLoadModuleStatus("FAILURE")
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
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
