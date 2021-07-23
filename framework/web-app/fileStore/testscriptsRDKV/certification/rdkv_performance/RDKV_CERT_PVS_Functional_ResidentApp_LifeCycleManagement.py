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
  <name>RDKV_CERT_PVS_Functional_ResidentApp_LifeCycleManagement</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do life cycle management of ResidentApp</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_61</test_case_id>
    <test_objective>The objective of this test is to do life cycle management of ResidentApp</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Get the ResidentApp.1.url value.
2. Deactivate ResidentApp using destroy method of RDKShell.
3. Launch WebKitBrowser plugin for moveToFront and back operations.
4. Launch resident app with uri as default URL using launch method of RDKShell.
5. Validate ResidentApp.1.url value.
6. Suspend and resume ResidenApp.
7. Do moveToBack and moveToFront.
8. Destroy the plugin
9. Revert the plugins status.</automation_approch>
    <expected_output>Device should be stable after a lifecycle.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_ResidentApp_LifeCycleManagement</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import json
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_ResidentApp_LifeCycleManagement');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper() :
    status = "SUCCESS"
    plugin = "ResidentApp"
    plugins_list = ["ResidentApp","WebKitBrowser"]
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    plugin_status_needed = {"ResidentApp":"deactivated","WebKitBrowser":"resumed"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict[plugin] in ("resumed","activated"):
        #Get the ResidentApp url
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","ResidentApp.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        ui_app_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if ui_app_url and result == "SUCCESS" :
            tdkTestObj.setResultStatus("SUCCESS")
            status = set_plugins_status(obj,plugin_status_needed)
            new_plugins_status = get_plugins_status(obj,plugins_list)
            if new_plugins_status != plugin_status_needed:
                status = "FAILURE"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            status = "FAILURE"
    else:
        print "\n ResidentApp is not in activated/resumed state"
        status = "FAILURE"
    if status == "SUCCESS":
        print "\n Preconditions are set successfully"
        plugin_operations_list = []
        plugin_validation_details = ["ResidentApp.1.url",ui_app_url]
        plugin_validation_details = json.dumps(plugin_validation_details)
        plugin_operations = json.dumps(plugin_operations_list)
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
    print "\n Launch ResidentApp"
    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
    tdkTestObj.addParameter('plugin','ResidentApp')
    tdkTestObj.addParameter('status','activate')
    tdkTestObj.addParameter('uri',ui_app_url)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if result == "SUCCESS":
        print "\n Successfully launched ResidentApp"
        tdkTestObj.setResultStatus("SUCCESS")
        curr_plugins_status_dict.pop("ResidentApp")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    else:
        print "\n Error while launching ResidentApp"
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
