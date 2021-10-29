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
  <name>RDKV_CERT_PACS_Cobalt_ToggleInterface_onVideoPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play a video in Cobalt, toggle the network interface and check whether video playback is happening</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_81</test_case_id>
    <test_objective>The objective of this test is to play a video in Cobalt, toggle the network interface and check whether video playback is happening</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with WIFI IP in test manager or WIFI Access point with same IP range is required.
2. Lightning application for ip change detection should be already hosted.
3. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url : string
ip_change_app_url : string
tm_username : string
tm_password : string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. Set video URL and click OK to play video
3. Validate video playback using decoder entries if the platform supports
4. Check the current network interface and toggle the interface 
5. Validate video playback using decoder entries if the platform supports
6. Revert the network interface 
7. Close Cobalt</automation_approch>
    <expected_output>Video playback should be happening even if interface is toggled.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_ToggleInterface_onVideoPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks/>
  </test_cases>
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
from StabilityTestUtility import *
import PerformanceTestVariables
from ip_change_detection_utility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_ToggleInterface_onVideoPlayback')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    plugins_list = ["Cobalt","WebKitBrowser","org.rdk.Network"]
    inverse_dict = {"ETHERNET":"WIFI","WIFI":"ETHERNET"}
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated","org.rdk.Network":"activated"}
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
        if new_status_dict != plugin_status_needed:
            print "\n Unable to set status of plugins"
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        plugin = 'Cobalt'
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
        current_interface,revert_nw = check_current_interface(obj)
        if current_interface != "EMPTY":
            new_interface = inverse_dict[current_interface]
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
                    for iteration in range(0,2):
                        params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            time.sleep(35)
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while executing generateKey method"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        result_val = "SUCCESS"
                        if validation_dict["validation_required"]:
                            tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                            tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",credentials)
                            tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                            if result_val == "SUCCESS" :
                                print "\n Video playback is happening"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Video playback is not happening"
                                tdkTestObj.setResultStatus("FAILURE")
                        if result_val == "SUCCESS":
                            connect_status, revert_dict, revert_plugin_status = connect_to_interface(obj,new_interface)
                            if connect_status == "SUCCESS":
                                movetofront_result = move_plugin(obj,"Cobalt","moveToFront")
                                if movetofront_result == "SUCCESS":
                                    if validation_dict["validation_required"]:
                                        if validation_dict["password"] == "None":
                                            password = ""
                                        else:
                                            password = validation_dict["password"]
                                        credentials = obj.IP+','+validation_dict["user_name"]+','+password
                                        tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                        tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                        tdkTestObj.addParameter("credentials",credentials)
                                        tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result_val = tdkTestObj.getResultDetails()
                                        if result_val == "SUCCESS" :
                                            print "\n Video playback is happening after toggling the network interface"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print "\n Video playback is not happening after toggling the network interface"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n User opted for no validation, completing the test"
                                else:
                                    print "\n Error while moving Cobalt to front"
                            else:
                                print "\n Error while setting interface as :{}".format(new_interface)
                                tdkTestObj.setResultStatus("FAILURE")
                            movetofront_result = move_plugin(obj,"WebKitBrowser","moveToFront")
                            result_status, revert_dict_new, revert_plugins = connect_to_interface(obj, current_interface) 
                            if result_status == "SUCCESS":
                                print "\n Successfully reverted the interface to: {}".format(current_interface)
                            else:
                                print "\n Error while reverting the interface to: {}".format(current_interface)
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Stopping the test "
                            tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to launch the url"
                    tdkTestObj.setResultStatus("FAILURE")
                #Deactivate cobalt
                print "\n Exiting from Cobalt "
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
                print "\n Unable to launch Cobalt \n"
                obj.setLoadModuleStatus("FAILURE")
    else:
        print "\n[Error] Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert == "YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
