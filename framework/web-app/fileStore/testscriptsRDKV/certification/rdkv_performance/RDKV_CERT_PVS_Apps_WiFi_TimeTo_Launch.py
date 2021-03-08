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
  <name>RDKV_CERT_PVS_Apps_WiFi_TimeTo_Launch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to  get the time taken to launch lightning app with WiFi</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_28</test_case_id>
    <test_objective>The objective of this test is to  get the time taken to launch lightning app with Wi-Fi</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with WiFi IP in test manager or WiFi Access point with same IP range is required.
2. Lightning application for ip change detection should be already hosted.
3.Lightning application for video player test should be already hosted.
4. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>video_test_url : string
ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Connect WiFi with lightning app to detect ip change loaded.
2. Launch the lightning app and capture the time taken for launching the app with WiFi
3. Validate the time taken to launch with threshold value
4. Revert everything</automation_approch>
    <expected_output>1. lightning app to detect IP address change should be launched.
2. Should connect to WiFI.
3. Lightning application for video player test should be launched.
4. The time taken to launch application in WiFi must be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_WiFi_TimeTo_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks/>
  </test_cases>
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from ip_change_detection_utility import *
import MediaValidationVariables
from MediaValidationUtility import *
from web_socket_util import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_WiFi_TimeTo_Launch');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = MediaValidationVariables.lightning_video_test_app_url
    videoURL  = MediaValidationVariables.video_src_url
    # Setting VideoPlayer Operations
    setOperation("close",10)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    appArguments = getURLArguments()
    # Getting the complete test app URL
    video_test_url = getTestURL(appURL,appArguments)

    print "Check Pre conditions"
    status = closed_status = "SUCCESS"
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
        webkit_status = get_plugins_status(obj,["WebKitBrowser"])
        webkit_status = webkit_status["WebKitBrowser"]
        if webkit_status != "resumed":
            status = set_plugins_status(obj,{"WebKitBrowser":"resumed"})
            revert_plugins_dict["WebKitBrowser"] = "deactivated"
    if status == "SUCCESS":
        if revert_if == "YES":
            closed_status = close_lightning_app(obj)
        if closed_status == "SUCCESS":
            print "\nGet the URL in WebKitBrowser"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            current_url = tdkTestObj.getResultDetails();
            result = tdkTestObj.getResult();
            if current_url != None and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                webkit_console_socket = createEventListener(obj.IP,MediaValidationVariables.webinspect_port,[],"/devtools/page/1",False)
                time.sleep(10)
                print "\nCurrent URL:",current_url
                print "\nSet Lightning Application URL"
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.addParameter("value",video_test_url);
                start_time = str(datetime.utcnow()).split()[1]
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
                                print "\n app not launched in 60 seconds \n"
                                break
                            if (len(webkit_console_socket.getEventsBuffer())== 0):
                                time.sleep(1)
                                continue_count += 1
                                continue
                            console_log = webkit_console_socket.getEventsBuffer().pop(0)
                            if "URL Info:" in console_log or "Connection refused" in console_log:
                                test_result = getConsoleMessage(console_log)
                                break;
                        if "URL Info:" in test_result:
                            print "\n Application launched successfully \n "
                            micosec_frm_start_time = int(start_time.split(".")[-1])
                            start_time = start_time.replace(start_time.split(".")[-1],"")
                            start_time = start_time.replace(".",":")
                            start_time = start_time + str(micosec_frm_start_time/1000)
                            print "\nApplication URL set in webkit browser at :{} (UTC)".format(start_time)
                            start_time_millisec = getTimeInMilliSeconds(start_time)
                            end_time = getTimeFromMsg(test_result)
                            print "\nApplication launched at: {} (UTC)".format(end_time)
                            end_time_millisec = getTimeInMilliSeconds(end_time)
                            app_launch_time = end_time_millisec - start_time_millisec
                            print "\nTime taken to launch the application: {} milliseconds \n".format(app_launch_time)
                            conf_file,result = getConfigFileName(tdkTestObj.realpath)
                            result1, app_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"APP_LAUNCH_THRESHOLD VALUE")
                            result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                            if all(value != "" for value in (app_launch_threshold_value,offset)):
                                if 0 < int(app_launch_time) < (int(app_launch_threshold_value) + int(offset)):
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "\n The time taken to launch the app is within the expected limit\n"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "\n The time taken to launch the app is not within the expected limit \n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "\n Failed to get the threshold value from config file"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "\n Error occured during application launch \n"
                        #Set the URL back to previous
                        webkit_console_socket.disconnect()
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
                print "Unable to get the current URL loaded in webkit"
        else:
            print "\n Preconditions are not met \n"
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    if revert_if == "YES" and status == "SUCCESS":
        status,complete_url = get_lightning_app_url(obj)
        status = launch_lightning_app(obj,complete_url)
        time.sleep(60)
        interface_status = set_default_interface(obj,"ETHERNET")
        if interface_status == "SUCCESS":
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

