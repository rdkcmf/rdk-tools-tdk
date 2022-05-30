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
  <name>RDKV_CERT_PVS_Functional_ResourceUsage_OnPluginsLaunch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate system resource usage after launching all the graphical plugins available in the DUT.</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_98</test_case_id>
    <test_objective>The objective of this test is to validate system resource usage after launching all the graphical plugins available in the DUT.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch all the graphical plugins configured in the AVAILABLE_GRAPHICAL_PLUGINS variable.
2. Check the status of plugins
3. Validate the resource usage using systeminfo property of DeviceInfo plugin
4. Revert the status of plugins </automation_approch>
    <expected_output>The resource usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_ResourceUsage_OnPluginsLaunch</test_script>
    <skipped>No</skipped>
    <release_version>M96</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import PerformanceTestVariables
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_ResourceUsage_OnPluginsLaunch')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\n Check Pre conditions"
    conf_file,file_status = get_configfile_name(obj)
    plugins_list = get_graphical_plugins(conf_file)
    status = "SUCCESS"
    revert_dict = {}
    if plugins_list != []:
        plugins_list.append("DeviceInfo")
        curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
        if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
            print "\n Error while getting the status of plugin"
            status = "FAILURE"
        elif curr_plugins_status_dict["DeviceInfo"] == "deactivated":
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","DeviceInfo")
            tdkTestObj.addParameter("status","activate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Error while activating DeviceInfo"
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
        elif curr_plugins_status_dict["DeviceInfo"] == None:
            print "\n DeviceInfo is not available in the device"
            status = "FAILURE"
    else:
        status = "FAILURE"
    if status == "SUCCESS":
        for plugin in plugins_list:
            if curr_plugins_status_dict[plugin] == "deactivated":
                launch_status,launch_start_time = launch_plugin(obj,plugin)
                revert_dict[plugin] = "deactivated"
                if launch_status == expectedResult:
                    time.sleep(10)
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin",plugin)
                    tdkTestObj.executeTestCase(expectedResult)
                    plugin_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if plugin_status == 'resumed' and expectedResult in result:
                        print "\n {} resumed successfully".format(plugin)
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(5)
                    else:
                        print "\n Unable to resume {} plugin, current status: {} ".format(plugin,plugin_status)
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Error while launching {} plugin status".format(plugin)
                    obj.setLoadModuleStatus("FAILURE")
                    break
        else:
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
        status = set_plugins_status(obj,revert_dict)
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
