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
  <name>RDKV_CERT_PVS_Functional_HtmlApp_Reboot_OnLoadURL</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to load URL in HtmlApp, reboot the device, check whether HtmlApp is stable and able to load URL again in it once the device is online.</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_86</test_case_id>
    <test_objective>The objective of this test is to load URL in HtmlApp, reboot the device, check whether HtmlApp is stable and able to load URL again in it once the device is online.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1.wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>html_page_url:string</input_parameters>
    <automation_approch>1. Launch the plugin using RDKShell
2. Register for urlchange event
3. Set given URL using url method
4. Verify the events for URL change
5. Reboot the DUT.
6. Launch the plugin using RDKShell
7. Register for urlchange event
8. Set given URL using url method
9. Verify the events for URL change
10. Destroy the plugin</automation_approch>
    <expected_output>The device should be stable after reboot and URL should be loaded before and after reboot</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_HtmlApp_Reboot_OnLoadURL</test_script>
    <skipped>No</skipped>
    <release_version>M95</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import PerformanceTestVariables
from StabilityTestUtility import *
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_HtmlApp_Reboot_OnLoadURL')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    event_listener = None
    thunder_port = PerformanceTestVariables.thunder_port
    htmlapp_test_url = PerformanceTestVariables.html_page_url
    print "\n Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    rebootwaitTime = 160
    plugin = "HtmlApp"
    plugins_list = ["Cobalt","WebKitBrowser","HtmlApp"]
    plugin_status_needed = {"Cobalt":"deactivated","HtmlApp":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            print "\n Unable to set status of plugins"
            status = "FAILURE"
    if status == "SUCCESS" :
        print "\n Preconditions are set successfully"
        plugin = "HtmlApp"
        for count in range(0,2):
            launch_status,launch_start_time = launch_plugin(obj,plugin)
            if launch_status == expectedResult:
                time.sleep(10)
                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                tdkTestObj.addParameter("plugin",plugin)
                tdkTestObj.executeTestCase(expectedResult)
                plugin_status = tdkTestObj.getResultDetails()
                result = tdkTestObj.getResult()
                if plugin_status == 'resumed' and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\n {} is resumed successfully".format(plugin)
                    if count == 1:
                        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "'+plugin+'.1.register","params": {"event": "urlchange", "id": "client.events.1" }}'],"/jsonrpc",False)
                        time.sleep(15)
                    print "\n Set test URL"
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method",plugin+".1.url")
                    tdkTestObj.addParameter("value",htmlapp_test_url)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        if count == 1:
                            time.sleep(10)
                            continue_count = 0
                            url_change_count = 0
                            while url_change_count < 2:
                                if (continue_count > 60):
                                    print "\n URL change related events are not triggered \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                if (len(event_listener.getEventsBuffer())== 0):
                                    continue_count += 1
                                    time.sleep(1)
                                    continue
                                event_log = event_listener.getEventsBuffer().pop(0)
                                print "\n Triggered event: ",event_log
                                json_msg = json.loads(event_log.split('$$$')[1])
                                if "urlchange" in event_log and htmlapp_test_url in event_log:
                                    if not json_msg["params"]["loaded"]:
                                        url_change_count += 1
                                    elif json_msg["params"]["loaded"]:
                                        url_change_count += 1
                                    else:
                                        continue_count += 1
                                else:
                                    continue_count += 1
                            else:
                                print "\n Validate if the URL is set successfully or not"
                                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                tdkTestObj.addParameter("method",plugin+".1.url")
                                tdkTestObj.executeTestCase(expectedResult);
                                new_url = tdkTestObj.getResultDetails();
                                result = tdkTestObj.getResult()
                                if htmlapp_test_url in new_url and expectedResult in result:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "\n URL(",new_url,") is set successfully"
                                else:
                                    print "\n Unable to set the test URL in {}, current URL: {}".format(plugin,new_url)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            event_listener.disconnect()
                            time.sleep(5)
                        else:
                            tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
                            tdkTestObj.addParameter("waitTime",rebootwaitTime)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            if expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n Device is rebooted"
                                uptime = get_device_uptime(obj)
                                if uptime != -1 and uptime < 280:
                                    print "\n Device is rebooted and uptime is: {}\n".format(uptime)
                                else:
                                    print "\n Error while validating uptime"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print "\n Error while rebooting the device"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                    else:
                        print "\n Error while setting the URL in ",plugin
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Error while resuming {}, current status: {} ".format(plugin,plugin_status)
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "\n Error while resuming the plugin"
                obj.setLoadModuleStatus("FAILURE")
                break
        else:
            print "\n Completing the test"
            #Deactivate plugin
            print "\n Exiting from ",plugin
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin",plugin)
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                print "\n Destroyed {} plugin".format(plugin)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Unable to deactivate ",plugin
                tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
