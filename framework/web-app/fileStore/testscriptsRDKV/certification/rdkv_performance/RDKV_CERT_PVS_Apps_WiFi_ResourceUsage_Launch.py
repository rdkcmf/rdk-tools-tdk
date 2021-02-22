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
  <name>RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the CPU and Memory usage while launching an application with WiFi.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_27</test_case_id>
    <test_objective>The objective of this test is to get the CPU and Memory usage while launching an application with WiFi.</test_objective>
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
    <automation_approch>1. Launch Lightning application to detect IP address change, then connect to WiFi
2.Launch Lightning application for video player 
3. Validate CPU and memory usage are within expected range
4. Revert everything</automation_approch>
    <expected_output>1. Lightning application for detecting IP address change must be lauched.
2. Should connect to WiFI.
3. Lightning application for video player must be lauched.
4. CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from ip_change_detection_utility import *
import MediaValidationVariables
from MediaValidationUtility import *
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch');

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
        webkit_status = get_plugins_status(obj,["WebKitBrowser"])
        webkit_status = webkit_status["WebKitBrowser"]
        if webkit_status != "resumed":
            status = set_plugins_status(obj,{"WebKitBrowser":"resumed"})
            revert_plugins_dict["WebKitBrowser"] = "deactivated"
    if status == "SUCCESS":
        if revert_if == "YES":
            closed_status = close_lightning_app(obj)
        plugin = "DeviceInfo"
        device_info_activated = True
        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
        tdkTestObj.addParameter("plugin",plugin);
        tdkTestObj.executeTestCase(expectedResult);
        device_info_result = tdkTestObj.getResult();
        device_info_status = tdkTestObj.getResultDetails();
        if expectedResult in device_info_result:
            tdkTestObj.setResultStatus("SUCCESS")
            if device_info_status not in "activated":
                revert_plugins_dict["DeviceInfo"] = "deactivated"
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
                tdkTestObj.addParameter("plugin",plugin);
                tdkTestObj.addParameter("status","activate");
                tdkTestObj.executeTestCase(expectedResult);
                result1 = tdkTestObj.getResult();
                if expectedResult in result1:
                    print "\n Deviceinfo is activated \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    device_info_activated = False
                    print "\n Error while activating DeviceInfo\n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
               print"Device info is in activated state"
        else:
            device_info_activated = False
            print "\n Error while getting DeviceInfo status"
            tdkTestObj.setResultStatus("FAILURE")
        if device_info_activated:
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
                            #get the cpu load
                            print "\n Application launched successfully \n "
                            tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            cpuload = tdkTestObj.getResultDetails()
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                #validate the cpuload
                                tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                tdkTestObj.addParameter('value',float(cpuload))
                                tdkTestObj.addParameter('threshold',90.0)
                                tdkTestObj.executeTestCase(expectedResult)
                                is_high_cpuload = tdkTestObj.getResultDetails()
                                result = tdkTestObj.getResult()
                                if is_high_cpuload == "YES" or expectedResult not in result:
                                    print "\n cpu load is high :{}%".format(cpuload)
                                    tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n cpu load : {}%\n".format(cpuload)
                            else:
                                print "Unable to get cpuload"
                                tdkTestObj.setResultStatus("FAILURE")
                            #get the memory usage
                            tdkTestObj = obj.createTestStep('rdkservice_getMemoryUsage')
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            memory_usage = tdkTestObj.getResultDetails()
                            if (result == "SUCCESS"):
                                tdkTestObj.setResultStatus("SUCCESS")
                                #validate memory usage
                                tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
                                tdkTestObj.addParameter('value',float(memory_usage))
                                tdkTestObj.addParameter('threshold',90.0)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult();
                                is_high_memory_usage = tdkTestObj.getResultDetails()
                                if is_high_memory_usage == "YES" or expectedResult not in result:
                                    print "\nmemory usage is high :{}%\n".format(memory_usage)
                                    tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\nmemory usage :{}%\n".format(memory_usage)
                                    tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Unable to get the memory usage\n"
                                tdkTestObj.setResultStatus("FAILURE")
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
