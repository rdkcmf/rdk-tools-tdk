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
  <name>RDKV_Profiling_Cobalt_VideoPlayback_Encrypted</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_CPU</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play an encrypted video in Cobalt and validate the profiling metrics after few minutes of playback</synopsis>
  <groups_id/>
  <execution_time>11</execution_time>
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
    <test_case_id>RDKV_PROFILING_10</test_case_id>
    <test_objective>The objective of this test is to play an encrypted video in Cobalt and validate the profiling metrics after few minutes of playback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1.  wpeframework should be running
2. Device should have DRM support
3. User should sign in to Cobalt before executing the test and the video URL used must be the URL of a paid content.
4. Video validation related details should be given in the device config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_encrypted_test_url: string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell.
2. Set a video URL with DRM protected
3. Check video playback using decoder proc entries if applicable
4. Validate the profiling data from Grafana tool with the threshold values for the pre-configured process list.
5. Execute the smem tool and collect the log
6. Execute pmap tool for the list of given process and collect the log
7. Check for alerts from Grafana tool.
8. Revert the plugin status.</automation_approch>
    <expected_output>Video should be playing and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Cobalt_VideoPlayback_Encrypted</test_script>
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
import json
import RDKVProfilingVariables
from rdkv_profilinglib import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True);

start_datetime_string = str(datetime.utcnow()).split('.')[0]

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Cobalt_VideoPlayback_Encrypted');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    revert="NO"
    cobalt_test_url = RDKVProfilingVariables.cobalt_encrypted_test_url
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url in Config file"
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','Cobalt','OCDM','tr69hostif']
    pre_process_list = [process for process in process_list if process!='Cobalt']
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    conf_file,result = getConfigFileName(obj.realpath)
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
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
        time.sleep(30)
        #Validate system wide profiling data before encrypted cobalt videoplayback
        end_datetime_string = str(datetime.utcnow()).split('.')[0]
        print "\n Validating system wide profiling mettrics from grafana before encrypted cobalt videoplayback \n"
        for result,validation_result,system_wide_methods,tdkTestObj in get_systemwide_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string):
            if expectedResult in (result and validation_result):
                print "Successfully validated the {}\n".format(system_wide_methods)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Error while validating the {}\n".format(system_wide_methods)
                tdkTestObj.setResultStatus("FAILURE")
        #Validate process wise profiling data before encrypted cobalt videoplayback
        print "\n Validating process wise profiling metrics from grafana before encrypted cobalt videoplayback\n"
        for result,validation_result,process_wise_methods_list,tdkTestObj in get_processwise_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string,pre_process_list):
            if expectedResult in (result and validation_result):
                print "Successfully validated the {}\n".format(process_wise_methods_list)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Error while validating the {}\n".format(process_wise_methods_list)
                tdkTestObj.setResultStatus("FAILURE")
        launch_status,launch_start_time = launch_plugin(obj,plugin)
        if expectedResult in launch_status:
            time.sleep(20)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin",plugin)
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
                    print "Clicking OK to play video"
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result1 = tdkTestObj.getResult()
                    time.sleep(40)
                    #Clicking OK to skip Ad
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result2 = tdkTestObj.getResult()
                    time.sleep(40)
                    if "SUCCESS" == (result1 and result2):
                        #TODO
                        #Add gstplayer logs validation

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
                        else:
                            print "\n Validation is not needed, proceeding the test"
                        if result_val == "SUCCESS":
                            time.sleep(300)
                            if result == "SUCCESS":
                                #Validate system wide profiling data
                                for result,validation_result,system_wide_methods,tdkTestObj in get_systemwidemethods(obj,conf_file):
                                    if expectedResult in (result and validation_result):
                                        print "Successfully validated the {}\n".format(system_wide_methods)
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "Error while validating the {}\n".format(system_wide_methods)
                                        tdkTestObj.setResultStatus("FAILURE")
                                #Validate process wise profiling data
                                for result,validation_result,process,process_wise_methods_list,tdkTestObj in get_processwisemethods(obj,process_list,conf_file):
                                    if expectedResult in (result and validation_result):
                                        print "Successfully validated the {} process {}\n".format(process,process_wise_methods_list)
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "Error while validating the {} process {}\n".format(process,process_wise_methods_list)
                                        tdkTestObj.setResultStatus("FAILURE")
                                #smem data collection
                                result,tdkTestObj = get_smemdata(obj,ip,conf_file)
                                if "SUCCESS" in result:
                                    print "\nSMEM tool execution success and transferred the log"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\nSMEM tool execution or log transfer failed"
                                    tdkTestObj.setResultStatus("FAILURE")
                                #pmap data collection
                                #Automatic process selection to get pmap data will be added in the later releases
                                result,tdkTestObj = get_pmapdata(obj,ip,conf_file,process_list)
                                if "SUCCESS" in result:
                                    print "\npmap tool execution success and transferred the log"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\npmap tool execution or log transfer failed"
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
                            print "\n Error while playing video in Cobalt"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while pressing OK button"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to set URL in Cobalt"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Cobalt is not in resumed state"
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
            print "\n Unable to launch Cobalt"
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_profiling")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
