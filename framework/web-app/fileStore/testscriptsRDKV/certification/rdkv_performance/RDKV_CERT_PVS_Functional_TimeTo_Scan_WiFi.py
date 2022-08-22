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
  <name>RDKV_CERT_PVS_Functional_TimeTo_Scan_WiFi</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to scan WIFI SSID details</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_62</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to scan WIFI SSID details</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>wpeframework should be running
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ssid:string</input_parameters>
    <automation_approch>1. Enable Network plugin and Wifi plugins as a precondition.
2. Listen to "onAvailableSSIDs" of Wifi plugin.
3. Start scanning for the given SSID and wait for 60 seconds
4. Calculate the time taken by finding the difference between start scan and event triggered time.
</automation_approch>
    <expected_output>The time taken to scan SSID details should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_Scan_WiFi</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from PerformanceTestVariables import *
from StabilityTestUtility import *
from web_socket_util import *
import rdkv_performancelib
from rdkv_performancelib import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_Scan_WiFi');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    event_listener = None
    status = "SUCCESS"
    revert = "NO"
    plugins_list = ["org.rdk.Network","org.rdk.Wifi"]
    plugin_status_needed = {"org.rdk.Network":"activated","org.rdk.Wifi":"activated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting plugin status"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    conf_file,file_status = getConfigFileName(obj.realpath)
    config_status,ssid = getDeviceConfigKeyValue(conf_file,"WIFI_SSID_NAME")
    if ssid == "":
        print "\n Please configure the WIFI_SSID_NAME value in device config file !!"
        status = "FAILURE"
    if status == "SUCCESS":
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.Wifi.1.register","params": {"event": "onAvailableSSIDs", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(10)
        tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
        tdkTestObj.addParameter("realpath",obj.realpath)
        tdkTestObj.addParameter("deviceIP",obj.IP)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
        if ssh_param_dict != {} and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Enable the RFC Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.PreferredNetworkInterface.Enable in DUT"
            #command to enable RFC for PreferredNetworkInterface
            command = "tr181 -s -v true Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.PreferredNetworkInterface.Enable; tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.PreferredNetworkInterface.Enable"
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            output = tdkTestObj.getResultDetails()
            if output != "EXCEPTION" and expectedResult in result:
                if "true" in output.split("\n")[1]:
                    print "\n Enabled RFC feature \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                    #list of interfaces supported by this device including their state
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","org.rdk.Network.1.getInterfaces");
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    interfaces = tdkTestObj.getResultDetails()
                    if expectedResult in result:
                        wifi_interface = False
                        interfaces = ast.literal_eval(interfaces)["interfaces"]
                        for interface in interfaces:
                            if interface["interface"] == "WIFI":
                                wifi_interface = True
                        if wifi_interface:
                            print "\n WiFi interface is present in org.rdk.Network.1.getInterfaces list"
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\n Enable WIFI interface"
                            params = '{"interface":"WIFI", "enabled":true, "persist":true}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                            tdkTestObj.addParameter("method","org.rdk.Network.1.setInterfaceEnabled");
                            tdkTestObj.addParameter("value",params);
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult();
                            if expectedResult in  result:
                                time.sleep(20)
                                tdkTestObj.setResultStatus("SUCCESS")
                                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                                tdkTestObj.addParameter("method","org.rdk.Network.1.getInterfaces");
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                interfaces = tdkTestObj.getResultDetails()
                                if expectedResult in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    interfaces = ast.literal_eval(interfaces)["interfaces"]
                                    wifi_dict = {}
                                    for interface in interfaces:
                                        if interface["interface"] == "WIFI":
                                            wifi_dict = interface
                                    else:
                                        if wifi_dict and wifi_dict["enabled"]:
                                            print "\n WIFI is enabled"
                                            print "\n Start scanning for SSID"
                                            #Start scanning for SSID
                                            params = '{"incremental":true,"ssid":"' + ssid + '","frequency":""}'
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                            tdkTestObj.addParameter("method","org.rdk.Wifi.1.startScan")
                                            tdkTestObj.addParameter("value",params)
                                            scan_start_time = str(datetime.utcnow()).split()[1] 
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResult()
                                            if result == "SUCCESS":
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                time.sleep(20)
                                                continue_count = 0
                                                event_time = ""
                                                while True:
                                                    if (continue_count > 60):
                                                        break
                                                    if (len(event_listener.getEventsBuffer())== 0):
                                                        continue_count += 1
                                                        time.sleep(1)
                                                        continue
                                                    event_log = event_listener.getEventsBuffer().pop(0)
                                                    if ("onAvailableSSIDs" in event_log and ssid in str(event_log)):
                                                        print "\n Event is triggered: ", event_log.split('$$$')[1]
                                                        event_time = event_log.split('$$$')[0]
                                                        break
                                                    else:
                                                        print "\n Unable to scan the SSID: ",ssid
                                                if event_time:
                                                    config_status,wifi_scan_threshold = getDeviceConfigKeyValue(conf_file,"WIFI_SCAN_TIME_THRESHOLD_VALUE")
                                                    Summ_list.append('WIFI_SCAN_TIME_THRESHOLD_VALUE :{}ms'.format(wifi_scan_threshold))
                                                    offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                                    if all(value != "" for value in (wifi_scan_threshold,offset)):
                                                        scan_start_time_in_millisec = getTimeInMilliSec(scan_start_time)
                                                        scan_end_time_in_millisec = getTimeInMilliSec(event_time)
                                                        print "\n WIFI scan initiated at: ",scan_start_time
                                                        Summ_list.append('WIFI scan initiated at :{}'.format(scan_start_time))
                                                        print "\n WIFI scan completed at : ", event_time
                                                        Summ_list.append('WIFI scan completed at  :{}'.format(event_time))
                                                        time_taken_for_wifiscan = scan_end_time_in_millisec - scan_start_time_in_millisec
                                                        print "\n Time taken to scan WIFI details: {}(ms)".format(time_taken_for_wifiscan)
                                                        Summ_list.append('Time taken to scan WIFI details :{}ms'.format(time_taken_for_wifiscan))
                                                        print "\n Threshold value for time taken to scan WIFI details: {}(ms)".format(wifi_scan_threshold)
                                                        print "\n Validate the time: \n"
                                                        if 0 < time_taken_for_wifiscan < (int(wifi_scan_threshold) + int(offset)) :
                                                            print "\n Time taken for scanning the SSID details is within the expected range"
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                        else:
                                                            print "\n Time taken for scanning the SSID details is not within the expected range"
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                    else:
                                                        print "\n Please configure the Threshold value in device configuration file"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                else:
                                                    print "\n onAvailableSSIDs event is not triggered"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print "\n Error while executing start scan method"
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print "\n Error while enabling wifi interface"
                                            tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error while getting interfaces"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while enabling WIFI interface"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n WIFI is not present in org.rdk.Network.1.getInterfaces output"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while executing org.rdk.Network.1.getInterfaces method"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while enabling RFC for PreferredNetworkInterface"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while enabling RFC feature in DUT"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Please configure SSH details in Device configuration file \n"
            tdkTestObj.setResultStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(10)
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
