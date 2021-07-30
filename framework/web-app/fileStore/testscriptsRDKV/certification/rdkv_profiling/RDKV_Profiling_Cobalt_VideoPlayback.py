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
  <version>4</version>
  <name>RDKV_Profiling_Cobalt_VideoPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate profiling data from Grafana tool during video playback in Cobalt.</synopsis>
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
    <test_case_id>RDKV_PROFILING_06</test_case_id>
    <test_objective>The objective of this test is to validate profiling data from Grafana tool during video playback in Cobalt.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1.  wpeframework should be running
2. User should sign in to Cobalt before executing the test.
3. Video validation related details should be given in the device config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url: string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell.
2. Set a video URL
3. Check video playback using proc entries
4. Validate the profiling data from Grafana tool based on threshold values.
5. Revert the plugin status.</automation_approch>
    <expected_output>Video should be playing and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Cobalt_VideoPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
from StabilityTestUtility import *
import PerformanceTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Cobalt_VideoPlayback')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\n Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','Cobalt']
    system_wide_methods_list = ['rdkv_profiling_collectd_check_system_memory','rdkv_profiling_collectd_check_system_loadavg','rdkv_profiling_collectd_check_system_CPU']
    system_wide_method_names_dict = {'rdkv_profiling_collectd_check_system_memory':'system memory','rdkv_profiling_collectd_check_system_loadavg':'system load avg','rdkv_profiling_collectd_check_system_CPU':'system cpu'}
    process_wise_methods = ['rdkv_profiling_collectd_check_process_metrics','rdkv_profiling_collectd_check_process_usedCPU','rdkv_profiling_collectd_check_process_usedSHR']
    process_wise_method_names_dict = {'rdkv_profiling_collectd_check_process_metrics':'metrics','rdkv_profiling_collectd_check_process_usedCPU':'used CPU','rdkv_profiling_collectd_check_process_usedSHR':'used shared memory'}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
        cobalt_launch_status = launch_cobalt(obj)
        if cobalt_launch_status in expectedResult:
            time.sleep(30)
            print "\n Set the URL : {} using Cobalt deeplink method".format(cobalt_test_url)
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","Cobalt.1.deeplink")
            tdkTestObj.addParameter("value",cobalt_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_result = tdkTestObj.getResult()
            time.sleep(10)
            if(cobalt_result in expectedResult):
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Clicking OK to play video"
                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result1 = tdkTestObj.getResult()
                time.sleep(50)
                #Clicking OK to skip Ad
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result2 = tdkTestObj.getResult()
                time.sleep(60)
                if "SUCCESS" == (result1 and result2):
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
                            print "\n Video playback is happening"
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print "\n Video playback is not happening"
                    if result_val == "SUCCESS":
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
                        print "\n Stopping the test"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to press OK button"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to launch the video URL"
                tdkTestObj.setResultStatus("FAILURE")
            #Deactivate cobalt
            print "\n Exiting from Cobalt"
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Unable to deactivate Cobalt"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching Cobalt"
            obj.setLoadModuleStatus("FAILURE")
    else:
        print "\n[Error] Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert == "YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_profiling");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"