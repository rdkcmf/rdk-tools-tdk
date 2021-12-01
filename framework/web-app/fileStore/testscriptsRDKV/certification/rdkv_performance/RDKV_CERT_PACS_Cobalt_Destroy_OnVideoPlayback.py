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
  <name>RDKV_CERT_PACS_Cobalt_Destroy_OnVideoPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play a video in Cobalt, destroy the plugin and validate the video playback again after launching the plugin again</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_91</test_case_id>
    <test_objective>The objective of this test is to play a video in Cobalt, destroy the plugin and validate the video playback again after launching the plugin again</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. Set a video URL
3. Destroy the plugin during video playback
4. Launch Cobalt again
5. Set the URL
6. Validate the video playback using decoder entries if the platform is supporting
7. Destroy the plugin</automation_approch>
    <expected_output>Device should be stable after destroying the plugin and it should be able play the video after launching again.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_Destroy_OnVideoPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M95</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
from StabilityTestUtility import *
import PerformanceTestVariables
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_Destroy_OnVideoPlayback')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result

obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        time.sleep(10)
        if new_status_dict != plugin_status_needed:
            print "\n Error while setting status of plugins"
            status = "FAILURE"
    error_in_loop = False
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
        for count in range(0,2):
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
                    print "Clicking OK to play video"
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    for key_count in range(0,2):
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if not(count == 0 and key_count == 1):
                            time.sleep(50)
                        if result == "SUCCESS":
                            print "\n Pressed OK key"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error during key press"
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    else:
                        result_val = "SUCCESS"
                        if count == 1 and validation_dict["validation_required"]:
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
                                break
                    if error_in_loop:
                        print "\n Stopping the test"
                        break
                else:
                    print "Unable to launch the url"
                    tdkTestObj.setResultStatus("FAILURE")
                #Deactivate cobalt
                print "\n Exiting from Cobalt \n"
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
                print "\n Unable to launch Cobalt \n"
                obj.setLoadModuleStatus("FAILURE")
        else:
            print "\n Completing the test"
    else:
        print "\n[Error] Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert == "YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
