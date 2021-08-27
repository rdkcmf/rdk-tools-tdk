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
  <name>RDKV_Profiling_Cobalt_VideoPlayback_4K</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_loadavg</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate profiling metrics after 4K video playback in Cobalt</synopsis>
  <groups_id/>
  <execution_time>12</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PROFILING_11</test_case_id>
    <test_objective>The objective of this test is to validate profiling metrics after 4K video playback in Cobalt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1.  wpeframework should be running
2. User should sign in to Cobalt before executing the test.
3. Video validation related details should be given in the device config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url_4k: string
key_navigation_for_4k : List of strings</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell.
2. Set a 4K video URL
3. Navigate to set resolution option in the application and set 4K resolution for the video.
4. Check video playback using decoder entries
5. Validate the profiling data from Grafana tool based on threshold values.
6. Execute the smem tool and collect the log
7. Check for alerts from Grafana tool.
8. Revert the plugin status.</automation_approch>
    <expected_output>Video should be playing and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Cobalt_VideoPlayback_4K</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
import RDKVProfilingVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Cobalt_VideoPlayback_4K');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\n Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = RDKVProfilingVariables.cobalt_test_url_4k
    if cobalt_test_url == "":
        print "\n Please configure cobalt_test_url_4k variable in RDKVProfilingVariables file \n"
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','Cobalt','tr69hostif']
    system_wide_methods_list = ['rdkv_profiling_collectd_check_system_memory','rdkv_profiling_collectd_check_system_loadavg','rdkv_profiling_collectd_check_system_CPU']
    system_wide_method_names_dict = {'rdkv_profiling_collectd_check_system_memory':'system memory','rdkv_profiling_collectd_check_system_loadavg':'system load avg','rdkv_profiling_collectd_check_system_CPU':'system cpu'}
    process_wise_methods = ['rdkv_profiling_collectd_check_process_metrics','rdkv_profiling_collectd_check_process_usedCPU','rdkv_profiling_collectd_check_process_usedSHR']
    process_wise_method_names_dict = {'rdkv_profiling_collectd_check_process_metrics':'metrics','rdkv_profiling_collectd_check_process_usedCPU':'used CPU','rdkv_profiling_collectd_check_process_usedSHR':'used shared memory'}
    video_playback_key_sequence = ['OK','OK']
    key_navigation_for_4k = RDKVProfilingVariables.key_navigation_for_4k
    video_playback_key_sequence = video_playback_key_sequence + key_navigation_for_4k
    navigation_key_dictionary = RDKVProfilingVariables.navigation_key_dictionary
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
        cobalt_launch_status,launch_start_time = launch_plugin(obj,"Cobalt")
        if cobalt_launch_status in expectedResult:
            time.sleep(20)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if cobalt_status == 'resumed' and expectedResult in result:
                print "\nCobalt Resumed Successfully\n"
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Set the URL : {} using Cobalt deeplink method".format(cobalt_test_url)
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                tdkTestObj.addParameter("value",cobalt_test_url)
                tdkTestObj.executeTestCase(expectedResult)
                cobalt_result = tdkTestObj.getResult()
                time.sleep(20)
                if(cobalt_result in expectedResult):
                    tdkTestObj.setResultStatus("SUCCESS")
                    for idx, key in enumerate(video_playback_key_sequence):
                        print "\n Sending {} Key using generateKey method".format(key)
                        params = '{"keys":[ {"keyCode": ' + str(navigation_key_dictionary[key]) + ',"modifiers": [],"delay":1.0}]}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            #Wait for few seconds after pressing OK button for the first time
                            if idx == 0 or idx == 1:
                                time.sleep(45)
                        else:
                            print "\n Error while executing generateKey method"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Successfully completed key navigations to play 4K video"
                        result_val = "SUCCESS"
                        time.sleep(20)
                        #TODO
                        #Add validation with gstplayer logs

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
                        else:
                            print "\n Validation is not needed"
                        if result_val == "SUCCESS":
                            time.sleep(240)
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
                                        print "Error while validating the {}\n".format(system_wide_method_names_dict[method])
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
                                            print "Successfully validated the {} process {}\n".format(process,process_wise_method_names_dict[method])
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print " Error while validating the {} process {}\n".format(process,process_wise_method_names_dict[method])
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
                            print "\n Stopping the test"
                            tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to launch the video URL"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Cobalt is not in resumed state, current state:",cobalt_status
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
