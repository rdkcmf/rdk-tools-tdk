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
  <version>2</version>
  <name>RDKV_Profiling_Load_LightningApp</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate profiling data from Grafana tool after launching a Lightning App.</synopsis>
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
    <test_case_id>RDKV_PROFILING_02</test_case_id>
    <test_objective>The objective of this test is to validate profiling data from Grafana tool after launching a Lightning App.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running.
2. The Lightning App fileStore/lightning-apps/tdkvideoplayer should be hosted successfully
3. User should configure the input parameters in PerformanceTestVariables.py file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>lightning_video_test_app_url: string
video_src_url: string
video_src_url_type: string</input_parameters>
    <automation_approch>1. Launch WebKitBrowser plugin using RDKShell.
2. Set the URL of Lightning App.
3. Check whether application is launched.
4. Validate the profiling data from Grafana tool based on threshold values.
5. Revert the URL and plugin status.</automation_approch>
    <expected_output>Lightning App should be launched and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Load_LightningApp</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from MediaValidationUtility import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Load_LightningApp');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = PerformanceTestVariables.lightning_video_test_app_url
    videoURL  = PerformanceTestVariables.video_src_url
    videoURL_type = PerformanceTestVariables.video_src_url_type.lower()
    # Setting VideoPlayer Operations
    setOperation("close",5)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    setURLArgument("type",videoURL_type)
    appArguments = getURLArguments()
    # Getting the complete test app URL
    video_test_url = getTestURL(appURL,appArguments)
    print "Check Pre conditions"
    status = "SUCCESS"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    #WebKitBrowser will be changed to LightningApp in the upcoming releases.
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
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,PerformanceTestVariables.webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "\nCurrent URL:",current_url
            print "\nSet Lightning Application URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",video_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult();
                if new_url in video_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "\n URL(",new_url,") is set successfully \n"
                    continue_count = 0
                    test_result = ""
                    while True:
                        if continue_count > 60:
                            print "app not launched in 60 seconds"
                            break
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            time.sleep(1)
                            continue_count += 1
                            continue
                        console_log = webkit_console_socket.getEventsBuffer().pop(0)
                        if "URL Info:" in console_log or "Connection refused" in console_log:
                            test_result = getConsoleMessage(console_log)
                            break;
                    webkit_console_socket.disconnect()
                    if "URL Info:" in test_result:
                        #get the cpu load
                        print "\n Application launched successfully \n "
                        time.sleep(30)
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
                        tdkTestObj.setResultStatus("FAILURE");
                        print "error occured during application launch"
                    #Set the URL back to previous
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                    tdkTestObj.addParameter("value",current_url);
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if result == "SUCCESS":
                        print "URL is reverted successfully \n"
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print "Failed to revert the URL"
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "Failed to load the URL %s" %(new_url)
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "Failed to set the URL"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in WebKitBrowser"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_profiling");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
