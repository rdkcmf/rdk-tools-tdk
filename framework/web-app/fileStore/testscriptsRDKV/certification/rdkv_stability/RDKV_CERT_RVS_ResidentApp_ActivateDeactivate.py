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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_ResidentApp_ActivateDeactivate</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to activate and deactivate Resident app for given number of times.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>600</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_15</test_case_id>
    <test_objective>The objective of this test is to activate and deactivate Resident app for given number of times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>activate_deactivate_max_count:integer</input_parameters>
    <automation_approch>1. Get the URL from ResidentApp and current status of ResidentApp
2. Toggle the status of ResidentApp for given number of times(Activate and deactivate).
3. Verify the CPU and mem load in each iteration
4. After maximum iterations, verify the resident app is loaded with main URL.
5. Revert everything</automation_approch>
    <expected_output>After given number of iterations ResidentApp should be loaded with main URL.
CPU load and memory usage must be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_ResidentApp_ActivateDeactivate</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_ResidentApp_ActivateDeactivate');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    activate_deactivate_max_count = StabilityTestVariables.activate_deactivate_max_count
    plugin = "ResidentApp"
    revert = "NO"
    status = "SUCCESS"
    plugins_list = ["ResidentApp","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != {}:
        if curr_plugins_status_dict["DeviceInfo"] != "activated":
            revert = "YES"
            device_info_plugin = "DeviceInfo"
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
            tdkTestObj.addParameter("plugin",device_info_plugin);
            tdkTestObj.addParameter("status","activate");
            tdkTestObj.executeTestCase(expectedResult);
            result1 = tdkTestObj.getResult();
            if expectedResult in result1:
                print "\n Deviceinfo is activated \n"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Error while activating DeviceInfo\n"
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
        else:
            print "\n DeviceInfo is activated"
        #Get the ResidentApp url
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","ResidentApp.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        ui_app_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if ui_app_url != "" and  result == "SUCCESS" :
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            status = "FAILURE"
    else:
        print "\n Unable to get plugins status"
        status = "FAILURE"
    if status == "SUCCESS":
        error_in_loop = False
        plugin_status = curr_plugins_status_dict[plugin]
        for count in range(0,activate_deactivate_max_count):
            print "\n########## Iteration :{} ##########\n".format(count+1)
            result_dict = {}
            for inner_count in range (0,2):
                if plugin_status == "deactivated":
                    new_status = "activate"
                    method = "org.rdk.RDKShell.1.launch"
                    params = '{"callsign": "'+plugin+'", "type":"", "uri":"", "x":0, "y":0, "w":1920, "h":1080}'
                    expected_status = ["activated","resumed"]
                else:
                    new_status = "deactivate"
                    method = "org.rdk.RDKShell.1.destroy"
                    params = '{"callsign": "'+plugin+'"}'
                    expected_status = ["deactivated"]
                print "\n Setting {} plugin to {} \n".format(plugin,new_status)
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(5)
                    #check status
                    print "\n Checking current status of {} plugin \n".format(plugin)
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin",plugin)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        plugin_status = tdkTestObj.getResultDetails()
                        print "\n Current status of {} plugin : {}\n".format(plugin,plugin_status)
                        if plugin_status in expected_status:
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "{} Status not set to {} , current status: {}".format(plugin,new_status,plugin_status)
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    else:
                        print "Error while getting {} plugin status".format(plugin)
                        tdkTestObj.setResultStatus("FAILURE")
                        error_in_loop = True
                        break
                else:
                    print "Error while setting {} plugin status to {}".format(plugin,new_status)
                    tdkTestObj.setResultStatus("FAILURE")
                    error_in_loop = True
                    break
            if error_in_loop:
                print "\n Stopping the test !!!"
                break
            print "\n##### Inner iterations for  activation and deactivation of plugin completed ##### \n"
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
            print "\nSuccessfully completed the {} iterations \n".format(activate_deactivate_max_count)
            print "\n Check Resident App is loaded with main URL\n"
            #Get the ResidentApp url
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","ResidentApp.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            curr_ui_app_url = tdkTestObj.getResultDetails();
            result = tdkTestObj.getResult()
            if ui_app_url == curr_ui_app_url and  result == "SUCCESS" :
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "[ERROR] Resident App is not having the initial URL: {},\n Current URL :{} \n".format(ui_app_url,curr_ui_app_url)
                tdkTestObj.setResultStatus("FAILURE")
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n Preconditions are not met\n"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES" or plugin_status != curr_plugins_status_dict[plugin] :
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE");

