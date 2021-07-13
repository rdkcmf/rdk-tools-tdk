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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Profiling_Load_Html_Page</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate profiling data from Grafana tool after loading a HTML page</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_PROFILING_01</test_case_id>
    <test_objective>The objective of this test is to validate profiling data from Grafana tool after loading a HTML page</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework.service should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch WebKitBrowser plugin using RDKShell.
2. Set the given URL using WebKitBrowser.1.url method.
3. Verify whether URL is set.
4. Validate the profiling data from Grafana tool based on threshold values.
5. Revert the URL and plugin status.</automation_approch>
    <expected_output>URL should be launched successfully and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Load_Html_Page</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import json
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Load_Html_Page')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    browser_test_url = "https://www.google.com/"
    print "\n Check Pre conditions"
    status = "SUCCESS"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated"}
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess']
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
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugin_status = get_plugins_status(obj,plugins_list)
        if new_plugin_status != plugin_status_needed:
            status = "FAILURE"
    time.sleep(10)
    if status == "SUCCESS":
        print "\n Pre conditions for the test are set successfully"
        print "\n Get the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","WebKitBrowser.1.url")
        tdkTestObj.executeTestCase(expectedResult)
        current_url = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Current URL:",current_url
            print "\n Set HTML page URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","WebKitBrowser.1.url")
            tdkTestObj.addParameter("value",browser_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in result:
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","WebKitBrowser.1.url")
                tdkTestObj.executeTestCase(expectedResult)
                new_url = tdkTestObj.getResultDetails()
                result = tdkTestObj.getResult()
                if browser_test_url in new_url and expectedResult in result:
                    print "\n Successfully loaded the URL:{} in WebKitBrowser".format(browser_test_url)
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\n Validate data from Grafana"
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
                                print "\n Successfully validated the {}".format(system_wide_method_names_dict[method])
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Error while validating the {}".format(system_wide_method_names_dict[method])
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
                    else:
                        print "\n Error while getting device config file"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\nFailed to load the URL ",browser_test_url
                    print "current url:",new_url
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "Failed to set the URL"
            #Set the URL back to previous
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","WebKitBrowser.1.url")
            tdkTestObj.addParameter("value",current_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if result == "SUCCESS":
                print "\nURL is reverted successfully"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\nFailed to revert the URL"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "\nFailed to get current URL from webkitbrowser"
    else:
        print "\nPre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\nRevert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_profiling")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
