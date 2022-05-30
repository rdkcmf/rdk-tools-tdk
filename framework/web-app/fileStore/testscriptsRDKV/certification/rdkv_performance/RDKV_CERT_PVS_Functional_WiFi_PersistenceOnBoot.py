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
  <name>RDKV_CERT_PVS_Functional_WiFi_PersistenceOnBoot</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the WIFI persistence after reboot.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_64</test_case_id>
    <test_objective>The objective of this test is to validate the WIFI persistence after reboot.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either WIFI should be the default interface of DUT or WIFI -SSID with same IP address range of ETHERNET should be available to connect during test
2. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Check the default interface of DUT and if it is not WIFI connect to WIFI.
2. Reboot the DUT using harakiri method.
3. Check whether WIFI connection is persisted.</automation_approch>
    <expected_output>WIFI connection should persist.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_WiFi_PersistenceOnBoot</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from rdkv_performancelib import *
import StabilityTestVariables
from StabilityTestUtility import *
from ip_change_detection_utility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_WiFi_PersistenceOnBoot');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    rebootwaitTime = StabilityTestVariables.rebootwaitTime
    plugins_list = ["org.rdk.Network","org.rdk.Wifi"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {"org.rdk.Network":"activated","org.rdk.Wifi":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        status = "FAILURE"
        print "\n Error while getting status of plugins"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    connect_status, revert_dict, revert_plugin_status = connect_to_interface(obj, "WIFI")
    if connect_status == "SUCCESS" and status == "SUCCESS":
        #get the connected SSID
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.Wifi.1.getConnectedSSID")
        tdkTestObj.addParameter("reqValue","ssid")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            connected_ssid = tdkTestObj.getResultDetails()
            print " \n Connected SSID Name: {}\n ".format(connected_ssid)
            tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
            tdkTestObj.addParameter("waitTime",rebootwaitTime)
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
                        time.sleep(60)
                        tdkTestObj.setResultStatus("SUCCESS")
                        #Check current interface
                        interface,revert = check_current_interface(obj)
                        if interface == "WIFI":
                            print "\n Current interface is WIFI"
                            #Check connected SSID
                            wifi_activated = False
                            wifi_status = rdkservice_getPluginStatus("org.rdk.Wifi")
                            if wifi_status == "activated":
                                wifi_activated = True
                            elif wifi_status == "deactivated":
                                new_status = rdkservice_setPluginStatus("org.rdk.Wifi","activate")
                                time.sleep(5)
                                if new_status != "EXCEPTION OCCURRED":
                                    wifi_status = rdkservice_getPluginStatus("org.rdk.Wifi")
                                    if wifi_status == "activated":
                                        wifi_activated = True
                                    else:
                                        print "\n Error while getting Wifi plugin status"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error while activating Wifi plugin"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while getting Wifi plugin status"
                                tdkTestObj.setResultStatus("FAILURE")
                            if wifi_activated:
                                #get the connected SSID
                                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                                tdkTestObj.addParameter("method","org.rdk.Wifi.1.getConnectedSSID")
                                tdkTestObj.addParameter("reqValue","ssid")
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                if result == "SUCCESS":
                                    new_ssid = tdkTestObj.getResultDetails()
                                    print " \n Connected SSID Name: {}".format(new_ssid)
                                    if new_ssid == connected_ssid:
                                        print "\n Wifi connection is persisted"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Wifi connection before reboot and after reboot are different"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error while getting connected SSID"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Wifi plugin is not in activated state"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Wifi connection is not persisted"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print "\n Device is not rebooted, device uptime:{}".format(uptime)
                else:
                    print "\n Failed to get the uptime";
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error occurred during reboot"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while getting Connected SSID details"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    revert_if = revert_dict.pop("revert_if")
    current_connection = revert_dict.pop("current_if")
    if revert_if:
        result_status, revert_dict_new, revert_plugins = connect_to_interface(obj, current_connection)
        time.sleep(30)
        if result_status == "FAILURE":
            obj.setLoadModuleStatus("FAILURE")
    if revert_plugin_status == "YES":
        status = set_plugins_status(obj,revert_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
