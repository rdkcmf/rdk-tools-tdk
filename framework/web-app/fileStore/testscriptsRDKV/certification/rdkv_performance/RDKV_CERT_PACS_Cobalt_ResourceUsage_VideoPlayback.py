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
  <name>RDKV_CERT_PACS_Cobalt_ResourceUsage_VideoPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play video in Cobalt and get CPU load and memory usage.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_34</test_case_id>
    <test_objective>The objective of this test is to play video in Cobalt and get CPU load and memory usage.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell.
2.  Load a video using Deeplink method
3. Validate CPU load and memory usage
4. Revert the plugin status</automation_approch>
    <expected_output>Video must be playing and CPU load and memory usage should be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_ResourceUsage_VideoPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M87</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
import PerformanceTestVariables
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_ResourceUsage_VideoPlayback');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    plugins_list = ["Cobalt","WebKitBrowser","DeviceInfo"]
    plugin_status_needed = {"DeviceInfo":"activated","Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
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
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result1 = tdkTestObj.getResult()
                time.sleep(50)
                #Clicking OK to skip Ad
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result2 = tdkTestObj.getResult()
                time.sleep(60)
                if "SUCCESS" == (result1 and result2):
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
                    if result_val == "SUCCESS":
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
                            result = tdkTestObj.getResult()
                            is_high_cpuload = tdkTestObj.getResultDetails()
                            if is_high_cpuload == "YES"  or expectedResult not in result:
                                print "\ncpu load is high :{}% \n".format(cpuload)
                                tdkTestObj.setResultStatus("FAILURE")
                            else:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\ncpu load: {}% \n".format(cpuload)
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
                            result = tdkTestObj.getResult()
                            is_high_memory_usage = tdkTestObj.getResultDetails()
                            if is_high_memory_usage == "YES" or expectedResult not in result:
                                print "\n memory usage is high :{}%\n".format(memory_usage)
                                tdkTestObj.setResultStatus("FAILURE")
                            else:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n memory usage is {}%\n".format(memory_usage)
                        else:
                            print "\n Unable to get the memory usage\n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Stopping the test \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "Unable to press OK button"
                    tdkTestObj.setResultStatus("FAILURE")
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
        print "\n[Error] Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert == "YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
