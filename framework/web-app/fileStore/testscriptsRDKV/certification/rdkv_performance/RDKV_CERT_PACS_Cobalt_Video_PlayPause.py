##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <name>RDKV_CERT_PACS_Cobalt_Video_PlayPause</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>.Launch cobalt and validate play and pause of given video .</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_11</test_case_id>
    <test_objective>The objective of this scrip is to launch cobalt and validate play and pause of given video .</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. TV must be connected to the DUT</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url : string</input_parameters>
    <automation_approch>1. As a pre requisite, disable all the other plugins and enable Cobalt only.
2. Set the URL of video to be played.
3. Validate if the video is playing using proc entries.
4. Generate key press corresponding to space key which will pause the video and wait 10 seconds.
5. Validate if the video is paused using proc entries.
6. Generate key press corresponding to space key which will play the video.
7. Validate if the video is playing using proc entries.
8. Revert all values.</automation_approch>
    <expected_output>Video must pause after pressing space key and it should continue to play after space key is pressed again.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_Video_PlayPause</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
import rdkv_performancelib
import PerformanceTestVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_Video_PlayPause');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url;
    print "Check Pre conditions"
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url value\n"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    cobal_launch_status = launch_cobalt(obj)
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and cobal_launch_status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        print "\nPre conditions for the test are set successfully"
        time.sleep(30)
        print "\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url)
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","Cobalt.1.deeplink")
        tdkTestObj.addParameter("value",cobalt_test_url)
        tdkTestObj.executeTestCase(expectedResult)
        cobalt_result = tdkTestObj.getResult()
        time.sleep(10)
        if(cobalt_result == expectedResult):
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
            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            result2 = tdkTestObj.getResult()
            time.sleep(50)
            if "SUCCESS" == (result1 and result2):
                result_val = ""
                tdkTestObj.setResultStatus("SUCCESS")
                if validation_dict["validation_required"]:
                    if validation_dict["password"] == "None":
                        password = ""
                    else:
                        password = validation_dict["password"]
                    credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                    print "\n check whether video is playing"
                    tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                    tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",credentials)
                    tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                    tdkTestObj.executeTestCase(expectedResult)
                    result_val = tdkTestObj.getResultDetails()
                else:
                    print "\n Validation is not required, proceeding the test \n"
                if result_val == "SUCCESS" or not validation_dict["validation_required"]:
                    tdkTestObj.setResultStatus("SUCCESS")
                    if validation_dict["validation_required"]:
                        print "\nVideo playback is happening\n"
                    print "\n Pause video for 10 seconds \n"
                    params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        if validation_dict["validation_required"]:
                            print "\n Check video is paused"
                            tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                            tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",credentials)
                            tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                            tdkTestObj.executeTestCase(expectedResult)
                            result_val = tdkTestObj.getResultDetails()
                        else:
                            result_val = "FAILURE"
                        if result_val != "SUCCESS":
                            print "\n Video is paused"
                            time.sleep(10)
                            print "\n Play the video \n"
                            params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                if validation_dict["validation_required"]:
                                    print "Check whether video is playing"
                                    tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                    tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                    tdkTestObj.addParameter("credentials",credentials)
                                    tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result_val = tdkTestObj.getResultDetails()
                                    if result_val == "SUCCESS" :
                                        print "\nVideo playback is happening\n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Video playback is not happening \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\nPause and Play operation is completed \n"
                                    tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "Unable to play from pause"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "Video is not paused"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "Unable to pause the video"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "Video is not playing"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "Unable to click OK"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Unable to load the cobalt_test_url"
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
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
