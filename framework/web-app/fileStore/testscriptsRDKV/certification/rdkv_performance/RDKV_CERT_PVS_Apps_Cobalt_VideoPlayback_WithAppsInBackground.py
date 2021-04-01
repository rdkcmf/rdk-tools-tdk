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
  <name>RDKV_CERT_PVS_Apps_Cobalt_VideoPlayback_WithAppsInBackground</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch an app like WebKitBrowser and then launch YouTube and verify the video playback.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_31</test_case_id>
    <test_objective>The objective of this test is to launch an app like WebKitBrowser and then launch YouTube and verify the video playback.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. Launch WebKitBrowser
2. Launch Cobalt and moveto front
3. Play a video in YT and verify the video playback
4. Revert everything</automation_approch>
    <expected_output>Video should be played in Cobalt with WebKitBrowser in background.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_Cobalt_VideoPlayback_WithAppsInBackground</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
import PerformanceTestVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_Cobalt_VideoPlayback_WithAppsInBackground');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url;
    print "Check Pre conditions"
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url value\n"
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status_dict = get_plugins_status(obj,plugins_list)
        if new_plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        print "\n Launching WebKitBrowser \n"
        webkit_status,webkit_start_time = launch_plugin(obj,"WebKitBrowser")
        time.sleep(5)
        if webkit_status == "SUCCESS":
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
            tdkTestObj.addParameter("plugin","WebKitBrowser");
            tdkTestObj.executeTestCase(expectedResult);
            webkit_result = tdkTestObj.getResult();
            webkit_curr_status = tdkTestObj.getResultDetails();
            if expectedResult in webkit_result:
                tdkTestObj.setResultStatus("SUCCESS")
                if webkit_curr_status in ("resumed","activated"):
                    cobal_launch_status = launch_cobalt(obj)
                    time.sleep(20)
                    if cobal_launch_status == "SUCCESS":
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
                        tdkTestObj.addParameter("plugin","Cobalt");
                        tdkTestObj.executeTestCase(expectedResult);
                        cobalt_result = tdkTestObj.getResult();
                        cobalt_curr_status = tdkTestObj.getResultDetails();
                        if expectedResult in cobalt_result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            if cobalt_curr_status in ("resumed","activated"):
                                print "\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url)
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                                tdkTestObj.addParameter("value",cobalt_test_url)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                time.sleep(10)
                                if expectedResult in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "Clicking OK to play video"
                                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                    tdkTestObj.addParameter("value",params)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result1 = tdkTestObj.getResult()
                                    time.sleep(40)
                                    #Skip if Ad is playing by pressing OK
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                    tdkTestObj.addParameter("value",params)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result2 = tdkTestObj.getResult()
                                    time.sleep(60)
                                    if "SUCCESS" == (result1 and result2):
                                        result_val = ""
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        if validation_dict["validation_required"]:
                                            if validation_dict["validation_method"] == "proc_entry":
                                                if validation_dict["password"] == "None":
                                                    password = ""
                                                else:
                                                    password = validation_dict["password"]
                                                credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                                                print "\n check whether video is playing"
                                                tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                                tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                                tdkTestObj.addParameter("credentials",credentials)
                                                tdkTestObj.addParameter("procfile",validation_dict["validation_file"])
                                                tdkTestObj.addParameter("mincdb",validation_dict["min_cdb"])
                                                tdkTestObj.executeTestCase(expectedResult)
                                                result_val = tdkTestObj.getResultDetails()
                                            else:
                                                print "\n Validation method other than proc_entry is not supported"
                                                validation_dict["validation_required"] = False
                                        else:
                                            print "\n Validation is not required, completing the test\n"
                                        if result_val == "SUCCESS" or not validation_dict["validation_required"]:
                                            if validation_dict["validation_required"]:
                                                print "\nVideo playback is happening\n"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print "\n Video playback is not happening \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Unable to press OK button \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "Error while setting URL in Cobalt using Deeplink method \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Cobalt is not activated, current status is: {} \n".format(cobalt_curr_status)
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Unable to get Cobalt status \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while launching Cobalt \n"
                        tdkTestObj.setResultStatus("FAILURE")
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
                    print "\n WebkitBrowser is not activated, current status is: {} \n".format(webkit_curr_status)
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to get WebKitBrowser status \n"
                tdkTestObj.setResultStatus("FAILURE")
            print "\n Exiting from WebKit \n"
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","WebKitBrowser")
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Unable to deactivate WebKitBrowser"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to launch WebKitBrowser \n" 
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
