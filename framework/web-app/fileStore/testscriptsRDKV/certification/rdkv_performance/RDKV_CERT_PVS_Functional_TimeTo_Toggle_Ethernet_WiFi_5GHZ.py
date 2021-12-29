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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_TimeTo_Toggle_Ethernet_WiFi_5GHZ</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the time to switch to Ethernet from 5GHZ SSID and vice versa.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_48</test_case_id>
    <test_objective>The objective of this test is to validate the time to switch to Ethernet from 5GHZ SSID and vice versa.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. 5GHZ WiFi Access point with same IP range of Ethernet is required.
2. Lightning application should be already hosted.
3. Wpeframework process should be up and running in the device.
4. If DUT is RPI, the version must be RPI 3B+ for detecting 5GHZ SSID  </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Get the default interface of DUT. Decide the new  interface based on current interface.
In a loop of 2
2. Load the Lightning application in WebKitBrowser
3a). If new interface is WIFI, connect to 5GHZ SSID, get the current system time and set WIFI as default interface.
b) Get netsrvmgr logs to calculate the time taken to set WIFI as default interface,
4a) Else get the current system time and set Ethernet as default interface.
b) Get netsrvmgr logs to calculate the time taken to set WIFI as default interface,
5. Validate the time taken in both cases with threshold values.</automation_approch>
    <expected_output>The time taken must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_Toggle_Ethernet_WiFi_5GHZ</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from ip_change_detection_utility import *
from datetime import datetime
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_Toggle_Ethernet_WiFi_5GHZ');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert_plugins_dict = {}
    revert_wifi_ssid = False
    start_time_dict = {}
    validation_dict = {}
    event_time_dict = {}
    plugins_list = ["WebKitBrowser","org.rdk.Wifi"]
    plugin_status_needed = {"WebKitBrowser":"resumed","org.rdk.Wifi":"activated"}
    print "\n Get plugins status"
    current_plugin_status_dict = get_plugins_status(obj,plugins_list)
    if plugin_status_needed != current_plugin_status_dict:
        print "\n Set plugins status"
        status = set_plugins_status(obj,plugin_status_needed)
    #Check current interface
    current_interface,revert_nw = check_current_interface(obj)
    initial_interface = current_interface
    url_status,complete_url = get_lightning_app_url(obj)
    if revert_nw == "YES":
        revert_plugins_dict["org.rdk.Network"] = "deactivated"
    if current_interface == "WIFI":
        print "\n Current interface is WIFI"
        ssid_freq = check_cur_ssid_freq(obj)
        if ssid_freq == "FAILURE":
            status = "FAILURE"
        elif ssid_freq == "2.4":
            revert_wifi_ssid = True
            status = launch_lightning_app(obj,complete_url)
            time.sleep(20)
            if "SUCCESS" == (url_status and status):
                connect_wifi_status = connect_wifi(obj,"5")
                if connect_wifi_status == "FAILURE":
                    status = "FAILURE"
                else:
                    status = close_lightning_app(obj)
            else:
                status = "FAILURE"
    if current_interface != "EMPTY" and current_plugin_status_dict != {} and url_status == status == "SUCCESS":
        revert_plugins_dict.update(current_plugin_status_dict)
        conf_file,file_status = getConfigFileName(obj.realpath)
        wifi_to_ethernet_config_status,wifi_to_ethernet_threshold = getDeviceConfigKeyValue(conf_file,"WIFI_TO_ETHERNET_THRESHOLD_VALUE")
        ethernet_to_wifi_config_status,ethernet_to_wifi_threshold = getDeviceConfigKeyValue(conf_file,"ETHERNET_TO_WIFI_THRESHOLD_VALUE")
        offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
        if all(value != "" for value in (wifi_to_ethernet_threshold,ethernet_to_wifi_threshold,offset)):
            for count in range(0,2):
                time.sleep(30)
                result_status = "FAILURE"
                if current_interface == "ETHERNET":
                    new_interface = "WIFI"
                    command = "cat /opt/logs/netsrvmgr.log | grep -inr set_interface_state:.*wlan0.*up | tail -1"
                    keyword = "ip link set dev wlan0 up"
                    wifi_connect_status,plugins_status_dict,revert_plugins,start_time_dict[new_interface] = switch_to_wifi(obj,"5",True)
                    if wifi_connect_status == "SUCCESS":
                        print "\n Successfully Set WIFI as default interface"
                        result_status = "SUCCESS"
                    else:
                        print "\n Error while setting WIFI as default interface"
                        result_status = "FAILURE"
                else:
                    new_interface = "ETHERNET"
                    command = 'cat /opt/logs/netsrvmgr.log | grep -inr set_interface_state:.*eth0.*up | tail -1'
                    keyword = "ip link set dev eth0 up"
                    status = launch_lightning_app(obj,complete_url)
                    time.sleep(30)
                    interface_status,start_time_dict[new_interface] = set_default_interface(obj,"ETHERNET",True)
                    if interface_status  == "SUCCESS":
                        print "\n Successfully set ETHERNET as default interface"
                        result_status = close_lightning_app(obj)
                    else:
                        print "\n Error while setting to ETHERNET"
                        result_status = "FAILURE"
                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                tdkTestObj.addParameter("realpath",obj.realpath)
                tdkTestObj.addParameter("deviceIP",obj.IP)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                if result_status == "SUCCESS" and ssh_param_dict != {} and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    validation_dict["ETHERNET"] = int(wifi_to_ethernet_threshold)
                    validation_dict["WIFI"] = int(ethernet_to_wifi_threshold)
                    current_interface = new_interface
                    tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                    tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                    tdkTestObj.addParameter("command",command)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    output = tdkTestObj.getResultDetails()
                    if output != "EXCEPTION" and expectedResult in result and keyword in output:
                        required_log = output.split('\n')[1]
                        print "\n Successfully switched to {}, logs:{}".format(new_interface,required_log)
                        print "\n Setting {} as default interface started at: {} UTC".format(new_interface,start_time_dict[new_interface])
                        start_time_dict[new_interface] = int(getTimeInMilliSec(start_time_dict[new_interface]))
                        event_time = getTimeStampFromString(required_log)
                        print "\n {} interface became default interface at: {} UTC".format(new_interface,event_time)
                        event_time_dict[new_interface] = int(getTimeInMilliSec(event_time))
                        time_taken = event_time_dict[new_interface] -  start_time_dict[new_interface]
                        print "\n Time taken for setting {} as default interface: {}(ms) ".format(new_interface,time_taken)
                        print "\n Threshold value for time taken for setting {} as default interface: {}(ms) ".format(new_interface,validation_dict[new_interface])
                        if 0 < time_taken < ( validation_dict[new_interface] + int(offset)):
                            print "\n Time taken is within the expected range"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n  Time taken is not within the expected range"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error happened during SSH session, logs are not available"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Error while setting default interface"
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "\n Successfully completed validation"
        else:
            print "\n Please configure the SSH details and threshold values in the device config file"
            tdkTestObj.setResultStatus("FAILURE")
        #Revert interface
        if current_interface != initial_interface:
            print "\n Revert network interface to {}\n".format(initial_interface)
            if initial_interface == "ETHERNET":
                status = launch_lightning_app(obj,complete_url)
                time.sleep(30)
                interface_status = set_default_interface(obj,"ETHERNET")
                if interface_status == "SUCCESS":
                    print "\n Successfully reverted ETHERNET as default interface"
                else:
                    print "\n Error while reverting ETHERNET as default interface"
                    status = "FAILURE"
            else:
                wifi_connect_status,plugins_status_dict,revert_plugins = switch_to_wifi(obj)
                if wifi_connect_status == "SUCCESS":
                    print "\n Successfully reverted WIFI as default interface"
                else:
                    print "\n Error while reverting WIFI as default interface"
                    status = "FAILURE"
        if revert_wifi_ssid:
            status = launch_lightning_app(obj,complete_url)
            time.sleep(20)
            if "SUCCESS" == (url_status and status):
                connect_wifi_status = connect_wifi(obj,"5")
                if connect_wifi_status == "FAILURE":
                    status = "FAILURE"
                else:
                    status = close_lightning_app(obj)
            else:
                status = "FAILURE"
        if status == "FAILURE":
            obj.setLoadModuleStatus("FAILURE")
    else:
        print "\n Preconditions are not met "
        obj.setLoadModuleStatus("FAILURE")
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
