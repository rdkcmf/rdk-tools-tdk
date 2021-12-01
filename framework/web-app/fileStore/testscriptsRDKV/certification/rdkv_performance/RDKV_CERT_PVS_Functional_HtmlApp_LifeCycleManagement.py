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
  <name>RDKV_CERT_PVS_Functional_HtmlApp_LifeCycleManagement</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do lifecycle management of  HtmlApp plugin.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_90</test_case_id>
    <test_objective>The objective of this test is to do lifecycle management of HtmlApp plugin.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>html_page_url:string</input_parameters>
    <automation_approch>1. Launch plugin using launch method of RDKShell.
2. Set given URL using HtmlApp.1.url method.
3.  Validate whether URL is set using above method itself.
4. Suspend the plugin using suspend method of RDKShell
5. Resume the plugin using resume method of RDKShell
6. Move the plugin to back using moveToBack method of RDKShell
7. Move the plugin to front using moveToFront method of RDKShell
8. Deactivate the plugin using destroy method of RDKShell.</automation_approch>
    <expected_output>Device should be stable after completing a lifecycle.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_HtmlApp_LifeCycleManagement</test_script>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_HtmlApp_LifeCycleManagement')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper() :
    status = "SUCCESS"
    revert="NO"
    html_app_test_url = PerformanceTestVariables.html_page_url
    plugins_list = ["HtmlApp","WebKitBrowser","Cobalt"]
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    plugin_status_needed = {"HtmlApp":"deactivated","WebKitBrowser":"deactivated","Cobalt":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugin"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            print "\n Error while setting status of plugins"
            status = "FAILURE"
    if status == "SUCCESS":
        plugin = "HtmlApp"
        print "\n Preconditions are set successfully"
        plugin_operations_list = []
        plugin_validation_details = ["HtmlApp.1.url",html_app_test_url]
        plugin_operations_list.append({plugin_validation_details[0]:plugin_validation_details[1]})
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
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"

