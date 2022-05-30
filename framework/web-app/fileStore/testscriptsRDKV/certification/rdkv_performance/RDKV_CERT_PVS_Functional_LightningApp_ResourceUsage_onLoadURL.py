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
  <name>RDKV_CERT_PVS_Functional_LightningApp_ResourceUsage_onLoadURL</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the resource usage after loading a URL in LightningApp plugin</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_78</test_case_id>
    <test_objective>The objective of this test is to validate the resource usage after loading a URL in LightningApp plugin</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url:string</input_parameters>
    <automation_approch>1. Launch LightningApp using RDKShell
2. Register for the urlchange event
3. Set a URL in LightningApp using LightningApp.1.url method.
4. Verify whether URL is changed using urlchange event.
5. Validate the resource usage by DeviceInfo.1.systeminfo method
6. Revert the status of LightningApp.</automation_approch>
    <expected_output>URL should be launched successfully and resource usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_LightningApp_ResourceUsage_onLoadURL</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import PerformanceTestVariables
import IPChangeDetectionVariables
from StabilityTestUtility import *
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_LightningApp_ResourceUsage_onLoadURL')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result

obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    event_listener = None
    lightningapp_test_url = IPChangeDetectionVariables.ip_change_app_url
    thunder_port = PerformanceTestVariables.thunder_port
    print "\n Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status = "SUCCESS"
    plugins_list = ["LightningApp","Cobalt","WebKitBrowser","DeviceInfo"]
    plugin_status_needed = {"LightningApp":"deactivated","Cobalt":"deactivated","WebKitBrowser":"deactivated","DeviceInfo":"activated"}
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
            print "\n Unable to deactivate plugins"
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully"
        launch_status,launch_start_time = launch_plugin(obj,"LightningApp")
        if launch_status == expectedResult:
            time.sleep(10)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","LightningApp")
            tdkTestObj.executeTestCase(expectedResult)
            lightningapp_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if lightningapp_status == 'resumed' and expectedResult in result:
                print "\n LightningApp resumed successfully"
                tdkTestObj.setResultStatus("SUCCESS")
                event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "LightningApp.1.register","params": {"event": "urlchange", "id": "client.events.1" }}'],"/jsonrpc",False)
                time.sleep(10)
                print "\n Set test URL"
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","LightningApp.1.url")
                tdkTestObj.addParameter("value",lightningapp_test_url)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                time.sleep(10)
                if expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
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
                        if "urlchange" in event_log and lightningapp_test_url in event_log:
                            if not json_msg["params"]["loaded"]:
                                url_change_count += 1
                            elif json_msg["params"]["loaded"]:
                                url_change_count += 1
                            else:
                                continue_count += 1
                        else:
                            continue_count += 1
                    else:
                        print "\nValidate if the URL is set successfully or not"
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method","LightningApp.1.url")
                        tdkTestObj.executeTestCase(expectedResult)
                        new_url = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if lightningapp_test_url in new_url and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "\n URL(",new_url,") is set successfully"
                            print "\n Validating resource usage:"
                            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                            tdkTestObj.executeTestCase(expectedResult)
                            resource_usage = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if expectedResult in result and resource_usage != "ERROR":
                                print "\n Resource usage is within the expected limit"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Error while validating resource usage"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\nFailed to load the URL, current url:",new_url
                            tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Failed to set the URL"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while resuming LightningApp, current status: ",lightningapp_status
                tdkTestObj.setResultStatus("FAILURE")
            #Deactivate plugin
            print "\n Exiting from LightningApp"
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","LightningApp")
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Unable to deactivate LightningApp"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to launch LightningApp"
            obj.setLoadModuleStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(5)
    else:
        print "\nPre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
