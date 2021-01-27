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
  <name>RdkService_AppPerformance_CPUMem_Usage</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the CPU load and Memory usage while launching an application</synopsis>
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
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_17</test_case_id>
    <test_objective>The objective of this test is to get the CPU and Memory usage while launching an application</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.
</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable webkitbrowser plugin.
2. Set the application URL in webkitbrowser
3. Get the cpu load and memory usage after launching the application
4. Revert the status of plugins</automation_approch>
    <expected_output>CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RdkService_AppPerformance_CPUMem_Usage</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from web_socket_util import *
import MediaValidationVariables
from MediaValidationUtility import *
from StabilityTestUtility import *
from rdkv_performancelib import *


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_AppPerformance_CPUMem_Usage');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = MediaValidationVariables.lightning_video_test_app_url
    videoURL  = MediaValidationVariables.video_src_url
    # Setting VideoPlayer Operations
    setOperation("close",5)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    appArguments = getURLArguments()
    # Getting the complete test app URL
    video_test_url = getTestURL(appURL,appArguments)

    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated"}
    if curr_plugins_status_dict != plugin_status_needed:
        status = "FAILURE"
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,MediaValidationVariables.webinspect_port,[],"/devtools/page/1",False)
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
                            print "app not launched in 60 seconds"
                            break
                        if (len(webkit_console_socket.getEventsBuffer())== 0):
                            time.sleep(1)
                            continue_count += 1
                            continue
                        console_log = webkit_console_socket.getEventsBuffer().pop(0)
                        if "URL Info:" in console_log or "Connection refused" in console_log:
                            test_result = getConsoleMessage(console_log)
                            break;
                    webkit_console_socket.disconnect()
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
                        print "error occured during application launch"
                    #Set the URL back to previous
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
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
