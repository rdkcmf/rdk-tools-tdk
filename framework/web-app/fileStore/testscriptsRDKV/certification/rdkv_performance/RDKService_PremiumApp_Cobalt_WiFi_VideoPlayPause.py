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
  <name>RDKService_PremiumApp_Cobalt_WiFi_VideoPlayPause</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play and pause a video in Cobalt after connecting to Wifi.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_23</test_case_id>
    <test_objective>The objective of this test is to play and pause a video in Cobalt after connecting to WiFi</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with WiFi IP in test manager or WiFi Access point with same IP range is required.
2. Lightning application should be already hosted.
3. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url : string</input_parameters>
    <automation_approch>1. Check the current active interface of DUT and if it is already WIFI then follow steps 3 to 9
2. a) If current active interface is ETHERNET, enable the WIFI interface.
b) Connect to SSID
c) Launch Lightning app for detecting IP change in WebKitBrowser
d) Set WIFI as default interface.
e) Suspend WebkitBrowser and Resume after video play and pause.
3. Set the URL of video to be played.
4. Validate if the video is playing using proc entries.
5. Generate key press corresponding to space key which will pause the video and wait 10 seconds.
6. Validate if the video is paused using proc entries.
7. Generate key press corresponding to space key which will play the video.
8. Validate if the video is playing using proc entries.
9. Revert all values and default interface</automation_approch>
    <expected_output>Interface should be set as WiFi if it was ETHERNET.
Video must pause after pressing space key and it should continue to play after space key is pressed again.
</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKService_PremiumApp_Cobalt_WiFi_VideoPlayPause</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from ip_change_detection_utility import *
import PerformanceTestVariables
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKService_PremiumApp_Cobalt_WiFi_VideoPlayPause');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert_plugins_dict = {}
    revert_if  = revert_device_info = revert_plugins = "NO"
    #Check current interface
    current_interface,revert_nw = check_current_interface(obj)
    if revert_nw == "YES":
        revert_plugins_dict = {"org.rdk.Network":"deactivated"}
    if current_interface == "EMPTY":
        status = "FAILURE"
    elif current_interface == "ETHERNET":
        revert_if = "YES"
        wifi_connect_status,plugins_status_dict,revert_plugins = switch_to_wifi(obj)
        if revert_plugins == "YES":
            revert_plugins_dict.update(plugins_status_dict)
        if wifi_connect_status == "FAILURE":
            status = "FAILURE"
    else:
        print "\n Current interface is WIFI \n"
    validation_dict = get_validation_params(obj)
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "":
        if revert_if == "YES":
            status,start_suspend = suspend_plugin(obj,"WebKitBrowser")
        if status == "SUCCESS":
            cobal_launch_status = launch_cobalt(obj)
            time.sleep(30)
            print "\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url)
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","Cobalt.1.deeplink")
            tdkTestObj.addParameter("value",cobalt_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_result = tdkTestObj.getResult()
            time.sleep(10)
            if(cobalt_result in expectedResult and cobal_launch_status in expectedResult):
                tdkTestObj.setResultStatus("SUCCESS")
                revert_plugins_dict["Cobalt"] = "deactivated"
                print "Clicking OK to play video"
                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result1 = tdkTestObj.getResult()
                time.sleep(50)
                #Skip if Ad is playing by pressing OK
                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result2 = tdkTestObj.getResult()
                time.sleep(30)
                if "SUCCESS" == (result1 and result2):
                    result_val = "SUCCESS"
                    tdkTestObj.setResultStatus("SUCCESS")
                    if validation_dict["validation_required"]:
                        if validation_dict["validation_method"] == "proc_entry":
                            if validation_dict["ssh_method"] == "directSSH":
                                if validation_dict["password"] == "None":
                                    password = ""
                                else:
                                    password = validation_dict["password"]
                                credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                            else:
                                #TODO
                                print "selected ssh method is {}".format(validation_dict["ssh_method"])
                                pass
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
                        print "\n Validation is not required, proceeding the test \n"
                    if result_val == "SUCCESS":
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
                                tdkTestObj.addParameter("procfile",validation_dict["validation_file"])
                                tdkTestObj.addParameter("mincdb",validation_dict["min_cdb"])
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
                                    time.sleep(10)
                                    if validation_dict["validation_required"]:
                                        print "Check whether video is playing"
                                        tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                        tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                        tdkTestObj.addParameter("credentials",credentials)
                                        tdkTestObj.addParameter("procfile",validation_dict["validation_file"])
                                        tdkTestObj.addParameter("mincdb",validation_dict["min_cdb"])
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
        else:
            print "\n Precondition to suspend WebKitBrowser didn't work \n"
    else:
        print "\n[Error] Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert_if == "YES" and status == "SUCCESS":
        resume_status,start_resume = launch_plugin(obj,"WebKitBrowser")
        time.sleep(60)
        interface_status = set_default_interface(obj,"ETHERNET")
        if interface_status == "SUCCESS" and resume_status == "SUCCESS":
            print "\n Successfully reverted to ETHERNET \n"
            status = close_lightning_app(obj)
        else:
            print "\n Error while reverting to ETHERNET \n"
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
