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
  <version>2</version>
  <name>RDKV_CERT_PVS_Functional_TimeTo_LaunchWebKitBrowser_AfterReboot</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to launch WebKitBrowser immediately after reboot</synopsis>
  <groups_id/>
  <execution_time>7</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_68</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to launch WebKitBrowser immediately after reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Time in Test Manager and DUT should be in sync</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Reboot the DUT using harakiri method of Controller plugin
2.Register for onLaunched event of RDKShell.
3. Save current system time and launch WebKitBrowser using RDKShell.
4. Get the time from triggered event
5. Validate the output with threshold value</automation_approch>
    <expected_output>WebKitBrowser should be launched and time taken to launch Cobalt should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_LaunchWebKitBrowser_AfterReboot</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import PerformanceTestVariables
from StabilityTestUtility import *
from web_socket_util import *
import rdkv_performancelib
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_LaunchWebKitBrowser_AfterReboot')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    event_listener = None
    rebootwaitTime = 160
    status = "SUCCESS"
    revert = "NO"
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    initial_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if all(initial_plugins_status_dict[plugin] != "FAILURE" for plugin in plugins_list):
        tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
        tdkTestObj.addParameter("waitTime",rebootwaitTime)
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
                if uptime < 260:
                    print "\n Device is rebooted and uptime is: {}\n".format(uptime)
                    time.sleep(20)
                    tdkTestObj.setResultStatus("SUCCESS")
                    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
                    if initial_plugins_status_dict != curr_plugins_status_dict:
                        revert = "YES"
                    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
                        print "\n Error while getting status of plugins"
                        status = "FAILURE"
                    elif curr_plugins_status_dict != plugin_status_needed:
                        status = set_plugins_status(obj,plugin_status_needed)
                        time.sleep(10)
                        new_plugins_status_dict = get_plugins_status(obj,plugins_list)
                        if new_plugins_status_dict != plugin_status_needed:
                            status = "FAILURE"
                    if status == "SUCCESS":
                        plugin = "WebKitBrowser"
                        thunder_port = rdkv_performancelib.devicePort
                        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onLaunched", "id": "client.events.1" }}'],"/jsonrpc",False)
                        time.sleep(10)
                        launch_status,launch_start_time = launch_plugin(obj,plugin)
                        if launch_status == expectedResult:
                            time.sleep(5)
                            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                            tdkTestObj.addParameter("plugin",plugin)
                            tdkTestObj.executeTestCase(expectedResult)
                            webkit_status = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if webkit_status == 'resumed' and expectedResult in result:
                                print "\nWebKitBrowser Resumed Successfully\n"
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(10)
                                continue_count = 0
                                launched_time = ""
                                while True:
                                    if (continue_count > 60):
                                        break
                                    if (len(event_listener.getEventsBuffer())== 0):
                                        continue_count += 1
                                        time.sleep(1)
                                        continue
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    print "\n Triggered event: ",event_log,"\n"
                                    if ("WebKitBrowser" in event_log and "onLaunched" in str(event_log)):
                                        print "\n Event :onLaunched is triggered during WebKitBrowser launch \n"
                                        launched_time = event_log.split('$$$')[0]
                                        break
                                if launched_time:
                                    conf_file,file_status = getConfigFileName(obj.realpath)
                                    config_status,webkit_launch_threshold = getDeviceConfigKeyValue(conf_file,"WEBKITBROWSER_LAUNCH_AFTER_BOOT_THRESHOLD_VALUE")
                                    Summ_list.append('WEBKITBROWSER_LAUNCH_AFTER_BOOT_THRESHOLD_VALUE :{}ms'.format(webkit_launch_threshold))
                                    offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                    if all(value != "" for value in (webkit_launch_threshold,offset)):
                                        launch_start_time_in_millisec = getTimeInMilliSec(launch_start_time)
                                        launched_time_in_millisec = getTimeInMilliSec(launched_time)
                                        print "\n WebKitBrowser launch initiated at: ",launch_start_time
                                        Summ_list.append('WebKitBrowser launch initiated at :{}'.format(launch_start_time))
                                        print "\n WebKitBrowser launched at : ",launched_time
                                        Summ_list.append('WebKitBrowser launched at :{}'.format(launched_time))
                                        time_taken_for_launch = launched_time_in_millisec - launch_start_time_in_millisec
                                        print "\n Time taken to launch WebKitBrowser: {}(ms)".format(time_taken_for_launch)
                                        Summ_list.append('Time taken to launch WebKitBrowser :{}ms'.format(time_taken_for_launch))
                                        print "\n Threshold value for time taken to launch WebKitBrowser : {} ms".format(webkit_launch_threshold)
                                        print "\n Validate the time: \n"
                                        if 0 < time_taken_for_launch < (int(webkit_launch_threshold) + int(offset)) :
                                            print "\n Time taken for launching WebKitBrowser is within the expected range \n"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print "\n Time taken for launching WebKitBrowser is not within the expected range \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Please configure the Threshold value in device configuration file \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n onLaunched event not triggered for during WebKitBrowser launch\n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while checking WebKitBrowser status \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error while launching WebKitBrowser \n"
                            tdkTestObj.setResultStatus("FAILURE")
                        print "\n Exiting from WebKitBrowser \n"
                        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                        tdkTestObj.addParameter("plugin",plugin)
                        tdkTestObj.addParameter("status","deactivate")
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "Unable to deactivate Cobalt"
                            tdkTestObj.setResultStatus("FAILURE")
                        event_listener.disconnect()
                        time.sleep(10)
                    else:
                        print "\n Preconditions are not met"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n  Device is not rebooted, uptime:",uptime
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                "\n Error while getting uptime of the DUT"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while rebooting the DUT"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Error while getting status of plugins"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,initial_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
