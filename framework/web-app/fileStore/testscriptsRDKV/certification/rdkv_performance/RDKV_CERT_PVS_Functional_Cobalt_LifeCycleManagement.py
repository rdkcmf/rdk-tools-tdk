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
  <name>RDKV_CERT_PVS_Functional_Cobalt_LifeCycleManagement</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do lifecycle management of Cobalt plugin.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_56</test_case_id>
    <test_objective>The objective of this test is to do lifecycle management of Cobalt plugin.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework must be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url</input_parameters>
    <automation_approch>1. Launch plugin using launch method of RDKShell.
2. Set given  video URL using deeplink method of Cobalt
3.  Validate whether video is playing using proc entries
4. Suspend the plugin using suspend method of RDKShell
5. Resume the plugin using resume method of RDKShell
6. Move the plugin to back using moveToBack method of RDKShell
7. Move the plugin to front using moveToFront method of RDKShell
8. Deactivate the plugin using destroy method of RDKShell.</automation_approch>
    <expected_output>Device should be stable after completing a lifecycle.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Cobalt_LifeCycleManagement</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from StabilityTestUtility import *
import PerformanceTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Cobalt_LifeCycleManagement');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
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
        tdkTestObj = obj.createTestStep('rdkservice_executeLifeCycle')
        tdkTestObj.addParameter("plugin",plugin)
        tdkTestObj.addParameter("operations",plugin_operations)
        tdkTestObj.addParameter("validation_details",plugin_validation_details)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails();
        if expectedResult in result and details == "SUCCESS" :
            print "\n Successfully completed lifecycle"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Error while executing life cycle methods"
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
