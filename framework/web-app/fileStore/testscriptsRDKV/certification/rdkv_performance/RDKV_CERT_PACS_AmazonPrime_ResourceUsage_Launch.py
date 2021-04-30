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
  <name>RDKV_CERT_PACS_AmazonPrime_ResourceUsage_Launch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the CPU load and memory usage when launching Amazon Prime</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_40</test_case_id>
    <test_objective>The objective of this test is to get the CPU load and memory usage when launching Amazon Prime</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch Amazon using RDKShell.
2. Get the zorder and moveToFront if Amazon is not in front.
3. Validate CPU load and memory usage </automation_approch>
    <expected_output>CPU load and memory usage must be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_AmazonPrime_ResourceUsage_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_AmazonPrime_ResourceUsage_Launch');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugin = "Amazon"
    plugins_list = ["WebKitBrowser","Cobalt","Amazon","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"Amazon":"deactivated","WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if  plugin_status_needed != new_plugins_status:
            status = "FAILURE"
    if status == "SUCCESS":
        #Launch amazon and move to front
        launch_status, statrt_time = launch_plugin(obj,plugin)
        if launch_status == "SUCCESS":
            movedToFront = True
            tdkTestObj = obj.createTestStep('rdkservice_getValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
            tdkTestObj.executeTestCase(expectedResult)
            zorder = tdkTestObj.getResultDetails()
            zorder_status = tdkTestObj.getResult()
            if expectedResult in zorder_status:
                tdkTestObj.setResultStatus("SUCCESS")
                zorder = ast.literal_eval(zorder)["clients"]
                if zorder[0].lower() == plugin.lower():
                    print "\n{} plugin is in foreground\n".format(plugin)
                else:
                    param_val = '{"client": "'+plugin+'"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
                    tdkTestObj.addParameter("value",param_val)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        movedToFront = False
                        tdkTestObj.setResultStatus("FAILURE")
                if movedToFront:        
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
                else:
                    print "\n Unable to move plugin to front \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing getZorder \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error occured during plugin launch Stopping the test \n"
        #Deactivate Amazon
        print "\n Exiting from Amazon \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Amazon")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Amazon"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
