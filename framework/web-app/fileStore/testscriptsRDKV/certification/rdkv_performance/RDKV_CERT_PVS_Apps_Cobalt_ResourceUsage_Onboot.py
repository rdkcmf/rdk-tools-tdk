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
  <version>3</version>
  <name>RDKV_CERT_PVS_Apps_Cobalt_ResourceUsage_Onboot</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getReqValueFromResult</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch YouTube immediately after reboot and get CPU and memory usage.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_32</test_case_id>
    <test_objective>The objective of this test is to launch YouTube immediately after reboot and get CPU and memory usage.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Reboot the device
2. Once the device comes online Launch Cobalt 
3. Get the CPU and mem usage and validate it.
4. Revert everything</automation_approch>
    <expected_output>Cobalt should be launched successfully.
CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_Cobalt_ResourceUsage_Onboot</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import rebootTestUtility
from rebootTestUtility import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_Cobalt_ResourceUsage_Onboot');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status = "SUCCESS"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    initial_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if initial_plugins_status_dict != {}: 
        tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
        tdkTestObj.addParameter("waitTime",rebootwaitTime)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Rebooted device successfully \n"
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
            tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo")
            tdkTestObj.addParameter("reqValue","uptime")
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult()
            if expectedResult in result:
                uptime = int(tdkTestObj.getResultDetails())
                if uptime < 240:
                    print "\n Device is rebooted and uptime is: {}\n".format(uptime)
                    time.sleep(30)
                    tdkTestObj.setResultStatus("SUCCESS")
                    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
                    if initial_plugins_status_dict != curr_plugins_status_dict:
                        revert = "YES"
                    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
                    if curr_plugins_status_dict != plugin_status_needed:
                        status = set_plugins_status(obj,plugin_status_needed)
                        new_plugins_status_dict = get_plugins_status(obj,plugins_list)
                        if new_plugins_status_dict != plugin_status_needed:
                            status = "FAILURE"
                    cobal_launch_status = launch_cobalt(obj)
                    if status == "SUCCESS" and cobal_launch_status == "SUCCESS":
                        time.sleep(10)
                        print "\n Cobalt is launched \n "
                        #get the cpu load
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
                            if is_high_cpuload == "YES" or expectedResult not in result:
                                print "\n CPU load is high :{}%".format(cpuload)
                                tdkTestObj.setResultStatus("FAILURE")
                            else:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n CPU load : {}%\n".format(cpuload)
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
                                print "\n Memory usage is high :{}%\n".format(memory_usage)
                                tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Memory usage :{}%\n".format(memory_usage)
                                tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Unable to get the memory usage\n"
                            tdkTestObj.setResultStatus("FAILURE")
                        #Deactivate cobalt
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
                        print "\n Error while setting preconditions to launch Cobalt after reboot \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Device is not rebooted \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while getting uptime of device \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while rebooting DUT\n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,initial_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
