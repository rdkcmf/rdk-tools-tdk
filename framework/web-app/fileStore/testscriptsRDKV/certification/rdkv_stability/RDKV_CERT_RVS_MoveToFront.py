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
  <name>RDKV_CERT_RVS_MoveToFront</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do stress test with moveToFront for 1000 times with Cobalt and WebKitBrowser.</synopsis>
  <groups_id/>
  <execution_time>720</execution_time>
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
    <test_case_id>RDKV_STABILITY_27</test_case_id>
    <test_objective>The objective of this test is to do stress test with moveToFront for 1000 times with Cobalt and WebKitBrowser.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>moveto_operation_max_count:integer</input_parameters>
    <automation_approch>1. Launch WebKitBrowser using RDKShell
2. Launch Cobalt using RDKShell
3. Get zorder of RDKShell.
4. In a loop of 1000 invoke moveToFront method to change the zorder.
5. Validate CPU load and memory usage
6. Revert the plugins status</automation_approch>
    <expected_output>Device must be stable after 1000 iterations, Applications must move to front.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_MoveToFront</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import StabilityTestVariables
import ast
from rdkv_performancelib import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_MoveToFront');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
webkit_url = "https://www.google.com/"

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    revert = "NO"
    moveto_front_max_count = StabilityTestVariables.moveto_operation_max_count
    plugin_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    plugins_cur_status_dict = get_plugins_status(obj,plugin_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if plugin_status_needed != plugins_cur_status_dict :
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugin_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        #Launch Cobalt
        cobalt_launch_status,cobalt_launch_start_time = launch_plugin(obj,"Cobalt")
        time.sleep(10)
        #Launch WebKitBrowser
        webkit_launch_status,webkit_launch_start_time = launch_plugin(obj,"WebKitBrowser")
        time.sleep(10)
        #Set URL in WebKitBrowser
        print "\nSet a test URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_setValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.addParameter("value",webkit_url);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        time.sleep(10)
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            new_url = tdkTestObj.getResultDetails();
            result = tdkTestObj.getResult()
            if webkit_url in new_url and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                print "\n URL(",new_url,") is set successfully"
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                tdkTestObj.executeTestCase(expectedResult)
                zorder = tdkTestObj.getResultDetails()
                zorder_status = tdkTestObj.getResult()
                if zorder_status != "SUCCESS" :
                    print "\n Error while executing getZorder method \n"
                if all(result_status == "SUCCESS" for result_status in (cobalt_launch_status,webkit_launch_status,zorder_status)):
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check zorder
                    zorder = ast.literal_eval(zorder)["clients"]
                    for count in range(0,moveto_front_max_count):
                        print "\n zorder:",zorder
                        result_dict = {}
                        if zorder[0].lower() == "cobalt":
                            plugin = "WebKitBrowser"
                        elif zorder[0].lower() == "webkitbrowser" or zorder[0].lower() == "residentapp":
                            plugin = "Cobalt"
                        else:
                            print "\n Zorder is not having Cobalt or WebkitBrowser as first plugin, zorder: ",zorder
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                        #moveToFront
                        print "\n Moving {} plugin to front \n".format(plugin)
                        param_val = '{"client": "'+plugin+'"}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
                        tdkTestObj.addParameter("value",param_val)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            #Check zorder
                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                            tdkTestObj.executeTestCase(expectedResult)
                            zorder = tdkTestObj.getResultDetails()
                            zorder_status = tdkTestObj.getResult()
                            if expectedResult in zorder_status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                zorder = ast.literal_eval(zorder)["clients"]
                                print "\n zorder:",zorder
                                if zorder[0].lower() == plugin.lower():
                                    print "\n{} plugin moved to front \n".format(plugin)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n ##### Validating CPU load and memory usage #####\n"
                                    tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    cpuload = tdkTestObj.getResultDetails()
                                    if (result == "SUCCESS"):
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        #validate the cpuload
                                        tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                        tdkTestObj.addParameter('value',float(cpuload))
                                        tdkTestObj.addParameter('threshold',90.0)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        is_high_cpuload = tdkTestObj.getResultDetails()
                                        if is_high_cpuload == "YES" or expectedResult not in result:
                                            print "\n CPU load is high :{}% during iteration:{}".format(cpuload,count+1)
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                        else:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print "\n CPU load is {}% during iteration:{}\n".format(cpuload,count+1)
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print "\n Unable to get cpuload\n"
                                        break
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
                                            print "\n Memory usage is high :{}% during iteration: {}\n".format(memory_usage,count+1)
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                        else:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print "\n Memory usage is {}% during iteration: {}\n".format(memory_usage,count+1)
                                    else:
                                        print "\n Unable to get the memory usage\n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                    result_dict["iteration"] = count+1
                                    result_dict["cpu_load"] = float(cpuload)
                                    result_dict["memory_usage"] = float(memory_usage)
                                    result_dict_list.append(result_dict)
                                else:
                                    print "\n Unable to move {} plugin to front\n".format(plugin)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print "\n Error while executing getZorder method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Error while executing moveToFront method \n"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\nSuccessfully completed the {} iterations \n".format(moveto_front_max_count)
                    cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                    json.dump(cpu_mem_info_dict,json_file)
                    json_file.close()
                else:
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to set test URL in WebKitBrowser"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while executing WebKitBrowser.1.url method \n"
            tdkTestObj.setResultStatus("FAILURE")
        #Deactivate Cobalt and WebKitBrowser
        deactivate_plugins_dict = {"WebKitBrowser":"deactivated","Cobalt":"deactivated"}
        deactivate_status = set_plugins_status(obj,deactivate_plugins_dict)
        if deactivate_status == "SUCCESS":
            print "\n Successfully deactivated the plugins \n"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Error while deactivating plugins \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met\n"
        obj.setLoadModuleStatus("FAILURE")
    if revert == "YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,plugins_cur_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
