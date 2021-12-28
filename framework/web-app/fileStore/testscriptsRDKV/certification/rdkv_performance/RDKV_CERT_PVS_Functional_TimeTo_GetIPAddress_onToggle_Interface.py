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
  <name>RDKV_CERT_PVS_Functional_TimeTo_GetIPAddress_onToggle_Interface</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to get the IP address by toggling Ethernet to WIFI and vice versa.</synopsis>
  <groups_id/>
  <execution_time>12</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_96</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to get the IP address by toggling Ethernet to WIFI and vice versa.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Lightning application for ip change detection should be already hosted.
2. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Activate org.rdk.Network plugin  Check the current interface of DUT.
2. Launch the Lightning app to detect ip address change in webkitbrowser.
3. If the default interface is ETHERNET then make the new default interface as WIFI else make ETHERNET as default interface
4. Check for the event captured by tdkipchange Lightning app in wpeframework.log
5. Validate the time taken to get WIFI IP address and ethernet IP address during interface toggling.
6. Revert the status of plugin</automation_approch>
    <expected_output>1. The time taken to get IP address should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_GetIPAddress_onToggle_Interface</test_script>
    <skipped>No</skipped>
    <release_version>M96</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import ip_change_detection_utility
from datetime import datetime
from ip_change_detection_utility import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_GetIPAddress_onToggle_Interface')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result

obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    start_time_dict = {}
    wifi_connect_dict = {}
    validation_dict = {}
    event_time_dict = {}
    plugins_list = ["WebKitBrowser","org.rdk.Network"]
    inverse_dict = {"ETHERNET":"WIFI","WIFI":"ETHERNET"}
    plugin_status_needed = {"WebKitBrowser":"deactivated","org.rdk.Network":"activated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            print "\n Unable to set status of plugins"
            status = "FAILURE"
    offset = 10
    conf_file,file_status = get_configfile_name(obj)
    result1, validation_dict["WIFI"] = getDeviceConfigKeyValue(conf_file,"GET_WIFI_IPADDRESS_TIME_THRESHOLD_VALUE")
    result2, validation_dict["ETHERNET"] = getDeviceConfigKeyValue(conf_file,"GET_ETHERNET_IPADDRESS_TIME_THRESHOLD_VALUE")
    result3, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
    if status == "SUCCESS":
        for count in range(0,2):
            current_interface,revert_nw = check_current_interface(obj)
            if current_interface != "EMPTY":
                new_interface = inverse_dict[current_interface]
                connect_status,revert_dict, revert_plugin_status,start_time_dict[new_interface],wifi_connect_dict[new_interface] = connect_to_interface(obj,new_interface,True,True)
                if event_time_dict == {}:
                    revert = "YES"
                    curr_plugins_status_dict.update(revert_dict)
                if connect_status == "SUCCESS":
                    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                    tdkTestObj.addParameter("realpath",obj.realpath)
                    tdkTestObj.addParameter("deviceIP",obj.IP)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                    if ssh_param_dict != {}:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print "\n Validate the time taken to get IP address during toggle interafce"
                        command = 'cat /opt/logs/wpeframework.log | grep -inr IP.*Changed.*to.*'+obj.IP+'| tail -1'
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                        tdkTestObj.addParameter("command",command)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        output = tdkTestObj.getResultDetails()
                        if output != "EXCEPTION" and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            if len(output.split('\n')) > 2:
                                required_log = output.split('\n')[1]
                                print "\n Toggle from {} to {} started at: {} UTC".format(current_interface,new_interface,wifi_connect_dict[new_interface])
                                start_time_dict[new_interface] = int(getTimeInMilliSec(start_time_dict[new_interface]))
                                event_time = getTimeStampFromString(required_log)
                                print "\n {} ip address obtained at: {} UTC".format(new_interface,event_time)
                                event_time_dict[new_interface] = int(getTimeInMilliSec(event_time))
                                time_taken = event_time_dict[new_interface] -  start_time_dict[new_interface]
                                if new_interface == "WIFI" and time_taken < 0:
                                    wifi_connect_dict[new_interface] = int(getTimeInMilliSec(wifi_connect_dict[new_interface]))
                                    time_taken = event_time_dict[new_interface] - wifi_connect_dict[new_interface]
                                print "\n Time taken for getting {} ip address: {}(ms) ".format(new_interface,time_taken)
                                if 0 < time_taken < ( int(validation_dict[new_interface]) + int(offset)):
                                    print "\n Time taken for getting {} ip address is within the expected range".format(new_interface)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n  Time taken for getting {}ip address is not within the expected range".format(new_interface)
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Unable to find the ip address change related logs in wpeframework.log file"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error in command execution in DUT"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Please configure SSH details in device config file"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                    time.sleep(40)
                else:
                    print "\n Error while setting interface as :{}".format(new_interface)
                    obj.setLoadModuleStatus("FAILURE")
                    break
            else:
                print "\n Error while getting default interface"
                obj.setLoadModuleStatus("FAILURE")
                break
    else:
        print "\n[Error] Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert == "YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
