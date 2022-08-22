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
  <name>RDKV_CERT_PVS_Functional_HtmlApp_TimeTo_Destroy</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setPluginStatus</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to destroy HtmlApp plugin</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_73</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to destroy HtmlApp plugin</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Time in Test Manager and DUT should be in sync with UTC</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Register for onDestroyed event of RDKShell.
2. Launch HtmlApp using RDKShell
3. Save current system time and destroy HtmlApp using destroy method of RDKShell plugin
4. Get the time from triggered event
5. Validate the output with threshold value</automation_approch>
    <expected_output>The time taken should be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_HtmlApp_TimeTo_Destroy</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_HtmlApp_TimeTo_Destroy')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    event_listener = None
    status = "SUCCESS"
    revert = "NO"
    plugins_list = ["HtmlApp","Cobalt","WebKitBrowser"]
    plugin_status_needed = {"HtmlApp":"deactivated","Cobalt":"deactivated","WebKitBrowser":"deactivated"}
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
            print "\n Unable to deactivate the plugins"
            status = "FAILURE"
    if status == "SUCCESS":
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onDestroyed", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(10)
        launch_status,launch_start_time = launch_plugin(obj,"HtmlApp")
        if launch_status == expectedResult:
            time.sleep(5)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","HtmlApp")
            tdkTestObj.executeTestCase(expectedResult)
            htmlapp_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if htmlapp_status == 'resumed' and expectedResult in result:
                print "\n HtmlApp resumed successfully "
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                #Deactivate HtmlApp
                print "\n Destroying HtmlApp \n"
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                tdkTestObj.addParameter("plugin","HtmlApp")
                tdkTestObj.addParameter("status","deactivate")
                destroy_start_time = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin","HtmlApp")
                    tdkTestObj.executeTestCase(expectedResult)
                    htmlapp_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if htmlapp_status == 'deactivated' and expectedResult in result:
                        print "\n HtmlApp destroyed successfully"
                        tdkTestObj.setResultStatus("SUCCESS")
                        destroyed_time = ""
                        continue_count = 0
                        while True:
                            if (continue_count > 60):
                                break
                            if (len(event_listener.getEventsBuffer())== 0):
                                continue_count += 1
                                time.sleep(1)
                                continue
                            event_log = event_listener.getEventsBuffer().pop(0)
                            print "\n Triggered event: ",event_log,"\n"
                            if ("HtmlApp" in event_log and "onDestroyed" in str(event_log)):
                                print "\n Event :onDestroyed is triggered during HtmlApp destroy"
                                destroyed_time = event_log.split('$$$')[0]
                                break
                        if destroyed_time:
                            conf_file,file_status = getConfigFileName(obj.realpath)
                            config_status,htmlapp_destroy_threshold = getDeviceConfigKeyValue(conf_file,"HTMLAPP_DESTROY_THRESHOLD_VALUE")
                            Summ_list.append('HTMLAPP_DESTROY_THRESHOLD_VALUE :{}'.format(htmlapp_destroy_threshold))
                            offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                            Summ_list.append('THRESHOLD_OFFSET :{}'.format(offset))
                            if all(value != "" for value in (htmlapp_destroy_threshold,offset)):
                                destroy_start_time_in_millisec = getTimeInMilliSec(destroy_start_time)
                                destroyed_time_in_millisec = getTimeInMilliSec(destroyed_time)
                                print "\n HtmlApp destroy initiated at: ",destroy_start_time
                                Summ_list.append('HtmlApp destroy initiated at :{}'.format(destroy_start_time))
                                print "\n HtmlApp destroyed at : ",destroyed_time
                                Summ_list.append('HtmlApp destroyed at :{}'.format(destroyed_time))
                                time_taken_for_destroy = destroyed_time_in_millisec - destroy_start_time_in_millisec
                                print "\n Time taken to destroy HtmlApp: {}(ms)".format(time_taken_for_destroy)
                                Summ_list.append('Time taken to destroy HtmlApp :{}ms'.format(time_taken_for_destroy))
                                print "\n Threshold value for time taken to destroy HtmlApp plugin : {} ms".format(htmlapp_destroy_threshold)
                                print "\n Validate the time:"
                                if 0 < time_taken_for_destroy < (int(htmlapp_destroy_threshold) + int(offset)) :
                                    print "\n Time taken for destroying HtmlApp is within the expected range"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Time taken for destroying HtmlApp is not within the expected range"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Please configure the Threshold value in device configuration file"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n onDestroyed event not triggered for during HtmlApp destroy"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Unable to destroy HtmlApp, current status: ",htmlapp_status
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while destroying HtmlApp"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to launch HtmlApp, current status: ",htmlapp_status
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching HtmlApp"
            obj.setLoadModuleStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(10)
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
