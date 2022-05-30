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
  <name>RDKV_CERT_PVS_Functional_Cobalt_Reboot_OnVideoPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch Cobalt and start playback. During playback reboot device. Once the device is online verify by launching the cobalt again and starting video playback</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_70</test_case_id>
    <test_objective>The objective of this test is to launch Cobalt and start playback. During playback reboot device. Once the device is online verify by launching the cobalt again and starting video playback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. Set video URL
3. Validate the video playback using decoder entries if the platform support 
4. Reboot the device using harakiri method.
5. Launch Cobalt using RDKShell
6.  Set video URL
7. Validate the video playback using decoder 
</automation_approch>
    <expected_output>DUT should be stable after the reboot on video playback also. </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Cobalt_Reboot_OnVideoPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import PerformanceTestVariables
import json
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Cobalt_Reboot_OnVideoPlayback');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    revert="NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url in Config file"
    plugins_list = ["Cobalt"]
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    plugin_status_needed = {"Cobalt":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting plugin status"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and cobalt_test_url != "" and validation_dict != {}:
        plugin = "Cobalt"
        rebootwaitTime = 160
        print "\n Preconditions are set successfully"
        enterkey_keycode = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
        generatekey_method = 'org.rdk.RDKShell.1.generateKey'
        plugin_operations_list = [{'Cobalt.1.deeplink':cobalt_test_url},{generatekey_method:enterkey_keycode},{generatekey_method:enterkey_keycode}]
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
            plugin_validation_details = ["video_validation", validation_dict["ssh_method"], credentials, validation_dict["video_validation_script"]]
        else:
            plugin_validation_details = ["no_validation"]
        plugin_operations = json.dumps(plugin_operations_list)
        plugin_validation_details = json.dumps(plugin_validation_details)
        tdkTestObj = obj.createTestStep('rdkservice_validatePluginFunctionality')
        tdkTestObj.addParameter("plugin",plugin)
        tdkTestObj.addParameter("operations",plugin_operations)
        tdkTestObj.addParameter("validation_details",plugin_validation_details)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails();
        if expectedResult in result and details == "SUCCESS" :
            print "\n Successfully launched Cobalt and started video playback"
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Rebooting device"
            tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
            tdkTestObj.addParameter("waitTime",rebootwaitTime)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            result = expectedResult
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Rebooted device successfully \n"
                uptime = get_device_uptime(obj) 
                if 0 < uptime < 250:
                    print "\n Device is rebooted and uptime is: {}\n".format(uptime)
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_validatePluginFunctionality')
                    tdkTestObj.addParameter("plugin",plugin)
                    tdkTestObj.addParameter("operations",plugin_operations)
                    tdkTestObj.addParameter("validation_details",plugin_validation_details)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in result and details == "SUCCESS" :
                        print "\n Successfully launched Cobalt and started video playback"
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "\n Error while launching and playing video in Cobalt"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Uptime is not within the expected range: ",uptime
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while rebooting device"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching and playing video in Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
        #Deactivate cobalt
        print "\n Exiting from Cobalt \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
