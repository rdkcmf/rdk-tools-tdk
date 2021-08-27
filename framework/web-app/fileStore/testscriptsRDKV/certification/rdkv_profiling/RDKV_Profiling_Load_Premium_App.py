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
  <version>3</version>
  <name>RDKV_Profiling_Load_Premium_App</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate profiling data from Grafana tool after launching the Cobalt Application.</synopsis>
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
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PROFILING_05</test_case_id>
    <test_objective>The objective of this test is to validate profiling data from Grafana tool after launching the Cobalt Application.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch Cobalt and sleep for a minimum of 30 seconds
2. Validate the profiling data from Grafana tool based on threshold values.
3. Execute the smem tool and collect the log
4. Check for alerts from Grafana tool
5. Revert the URL and plugin status.</automation_approch>
    <expected_output>Cobalt should be launched successfully and  profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Load_Premium_App</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import json
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Load_Premium_App')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\n Check Pre conditions"
    status = "SUCCESS"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated"}
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','Cobalt','tr69hostif']
    system_wide_methods_list = ['rdkv_profiling_collectd_check_system_memory','rdkv_profiling_collectd_check_system_loadavg','rdkv_profiling_collectd_check_system_CPU']
    system_wide_method_names_dict = {'rdkv_profiling_collectd_check_system_memory':'system memory','rdkv_profiling_collectd_check_system_loadavg':'system load avg','rdkv_profiling_collectd_check_system_CPU':'system cpu'}
    process_wise_methods = ['rdkv_profiling_collectd_check_process_metrics','rdkv_profiling_collectd_check_process_usedCPU','rdkv_profiling_collectd_check_process_usedSHR']
    process_wise_method_names_dict = {'rdkv_profiling_collectd_check_process_metrics':'metrics','rdkv_profiling_collectd_check_process_usedCPU':'used CPU','rdkv_profiling_collectd_check_process_usedSHR':'used shared memory'}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
	status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        set_status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(20)
        new_plugin_status = get_plugins_status(obj,plugins_list)
        if new_plugin_status != plugin_status_needed:
            print "\n Unable to set plugin status"
            status = "FAILURE"
    if status == "SUCCESS":
        cobal_launch_status,launch_start_time = launch_plugin(obj,"Cobalt")
        if cobal_launch_status == "SUCCESS":
            time.sleep(20)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if cobalt_status == 'resumed' and expectedResult in result:
                print "\nCobalt Resumed Successfully\n"
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(60)
                conf_file,result = getConfigFileName(obj.realpath)
                if result == "SUCCESS":
                    for method in system_wide_methods_list:
                        tdkTestObj = obj.createTestStep(method)
                        tdkTestObj.addParameter('tmUrl',obj.url)
                        tdkTestObj.addParameter('resultId',obj.resultId)
                        tdkTestObj.addParameter('deviceConfig',conf_file)
                        tdkTestObj.executeTestCase(expectedResult)
                        details = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        validation_result = json.loads(details).get("test_step_status")
                        if expectedResult in (result and validation_result):
                            print "Successfully validated the {}\n".format(system_wide_method_names_dict[method])
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while validating the {}\n".format(system_wide_method_names_dict[method])
                            tdkTestObj.setResultStatus("FAILURE")
                    for process in process_list:
                        for method in process_wise_methods:
                            tdkTestObj = obj.createTestStep(method)
                            tdkTestObj.addParameter('tmUrl',obj.url)
                            tdkTestObj.addParameter('resultId',obj.resultId)
                            tdkTestObj.addParameter('processName',process)
                            tdkTestObj.addParameter('deviceConfig',conf_file)
                            tdkTestObj.executeTestCase(expectedResult)
                            details = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            validation_result = json.loads(details).get("test_step_status")
                            if expectedResult in (result and validation_result):
                                print "\n Successfully validated the {} process {}".format(process,process_wise_method_names_dict[method])
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Error while validating the {} process {}".format(process,process_wise_method_names_dict[method])
                                tdkTestObj.setResultStatus("FAILURE")
                    #smem data collection
                    tdkTestObj = obj.createTestStep("rdkv_profiling_smem_execute")
                    tdkTestObj.addParameter('deviceIP',ip)
                    tdkTestObj.addParameter('deviceConfig',conf_file)
                    tdkTestObj.addParameter('realPath',obj.realpath)
                    tdkTestObj.addParameter('execId',obj.execID)
                    tdkTestObj.addParameter('execDeviceId',obj.execDevId)
                    tdkTestObj.addParameter('execResultId',obj.resultId)
                    tdkTestObj.executeTestCase(expectedResult)
                    details = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if "SUCCESS" in result:
                        print "\nSMEM tool execution success and transferred the log"
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "\nSMEM tool execution or log transfer failed"
                        tdkTestObj.setResultStatus("FAILURE")
                    #check for alerts from Grafana tool
                    print "\nCheck for profiling alerts...."
                    tdkTestObj = obj.createTestStep("rdkv_profiling_get_alerts")
                    tdkTestObj.addParameter('tmUrl',obj.url)
                    tdkTestObj.addParameter('resultId',obj.resultId)
                    tdkTestObj.executeTestCase(expectedResult)
                    details = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    validation_result = json.loads(details).get("test_step_status")
                    if expectedResult in (result and validation_result):
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while getting device config file"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Cobalt is not in resumed state, current state: ",cobalt_status
                tdkTestObj.setResultStatus("FAILURE")
            #Deactivate cobalt
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
            print "\n Error while launching Cobalt"
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_profiling");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
