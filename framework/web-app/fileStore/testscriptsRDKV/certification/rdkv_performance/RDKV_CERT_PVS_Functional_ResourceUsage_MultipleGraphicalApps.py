##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_ResourceUsage_MultipleGraphicalApps</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the resource usage while launching and playing video in multiple graphical apps</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_132</test_case_id>
    <test_objective>The objective of this test is to validate the resource usage while launching and playing video in multiple graphical apps	</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Deactivate all the graphical plugins
2. Set the plugin status as Resumed for the available graphical plugins based on the data in config file
3. Launch the graphical apps and do the operations based on the data given in config file
3. Validate the resource usage of the device</automation_approch>
    <expected_output>The objective of this test is to validate the resource usage while launching and playing video in multiple graphical apps</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_ResourceUsage_MultipleGraphicalApps</test_script>
    <skipped>No</skipped>
    <release_version>M107</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#from PerformanceTestVariables import *
import PerformanceTestVariables
from rdkv_performancelib import *
from StabilityTestUtility import *


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_ResourceUsage_MultipleGraphicalApps');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

req_plugins = PerformanceTestVariables.req_graphical_plugins
print "\n Required plugin details: {}".format(req_plugins)
pluginName, pluginMethod, pluginLink, pluginAction = [], {}, {}, {}
flag = 0
plugin_name = "" 
plugin_data_list = req_plugins.split(";")
if len(plugin_data_list)>0:
    for plugin in range(len(plugin_data_list)):
        pluginDetails = plugin_data_list[plugin].split(",")
        if len(pluginDetails)>1:
            flag += 1
            pluginName.append(pluginDetails[0])
            pluginMethod[pluginDetails[0]] = pluginDetails[1]
            pluginLink[pluginDetails[0]] = pluginDetails[2]
            if len(pluginDetails) > 3:
                pluginAction[pluginDetails[0]] = pluginDetails[3]
if flag >0:
    if expectedResult in result.upper():
        status = "SUCCESS"
        revert = "NO"        
        print "Check Pre conditions"
        status = "SUCCESS"
        revert_dict = {}
        curr_plugins_status_dict = get_plugins_status(obj, pluginName)
        time.sleep(10)
        plugin_status_needed = {}
        for pluginData in pluginName:
            plugin_status_needed[pluginData] = "deactivated"
        if any(curr_plugins_status_dict == "FAILURE" for plugin in pluginName):
            print "\n Error while getting the status of plugins"
            status = "FAILURE"
        elif curr_plugins_status_dict != plugin_status_needed:
            revert = "YES"
            status = set_plugins_status(obj, plugin_status_needed)
            new_plugins_status = get_plugins_status(obj,pluginName)
            if new_plugins_status != plugin_status_needed:
                status = "FAILURE"
                print "\n Unable to set status of plugin"
        validation_dict = get_validation_params(obj)
        if status == "SUCCESS":
            print "\n Preconditions are set successfully"
            for plugin_data in range(len(plugin_data_list)):
                expectedResult = "SUCCESS"
                plugin_name = pluginName[plugin_data]
                launch_status,launch_start_time = launch_plugin(obj,plugin_name)
                revert_dict[plugin_name] = "deactivated"
                if launch_status == expectedResult:
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin",plugin_name)
                    tdkTestObj.executeTestCase(expectedResult)
                    plugin_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if plugin_status == 'resumed' and expectedResult in result:
                        print "\n {} resumed successfully".format(plugin_name)
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(5)
                    else:
                        print "\n Unable to resume {} plugin,current status: {}".format(plugin_name,plugin_status)
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                    plugin_method = pluginMethod.get(pluginName[plugin_data])    
                    plugin_link = pluginLink.get(pluginName[plugin_data])
                    method_param = plugin_name+".1."+plugin_method
                    get_param = plugin_name+".1.url"
                    print "\n Set the URL : {}".format(plugin_link)
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method",method_param)
                    tdkTestObj.addParameter("value",'"'+"https://"+plugin_link+'"')
                    tdkTestObj.executeTestCase(expectedResult)
                    launch_result = tdkTestObj.getResult()
                    time.sleep(10)
                    if expectedResult in result:
                        result_val = "SUCCESS"
                        if validation_dict["validation_required"]:
                            tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                            tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",credentials)
                            tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                            if result_val == "SUCCESS" :
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\nVideo playback is happening\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print "Video playback is not happening"
                                break
                        plugin_action = pluginAction.get(pluginName[plugin_data])
                        if plugin_action: 
                            print "\n Clicking OK to play video"
                            params = '{"keys":[ {"keyCode":"'+plugin_action+'","modifiers": [],"delay":1.0}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method", "org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value", params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result1 = tdkTestObj.getResult()
                            time.sleep(40)
                else:
                    print "\n Please enter the details in the config file to launch the url and/or video playback"
                    tdkTestObj.setResultStatus("FAILURE")
            print "\n Validating resource usage:"
            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
            tdkTestObj.executeTestCase(expectedResult)
            resource_usage = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if expectedResult in result and resource_usage != "ERROR":
                print "\n Resource usage is within the expected limit"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Resource usage is greater than the expected limit"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while setting up the pre-conditions"
            tdkTestObj.setResultStatus("FAILURE")
        status = set_plugins_status(obj,revert_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print "\n Failed to load module"