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
  <version>4</version>
  <name>RDKV_CERT_RVS_Cobalt_WebKitBrowser_Switch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch Cobalt, play a video and press home button then launch WebKitBrowser, set URL and press home button and repeat the same for 1000 times.</synopsis>
  <groups_id/>
  <execution_time>5000</execution_time>
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
    <test_case_id>RDKV_STABILITY_41</test_case_id>
    <test_objective>The objective of this test is to launch Cobalt, play a video and press home button then launch WebKitBrowser, set URL and press home button and repeat the same for 1000 times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>lifecycle_max_count: integer</input_parameters>
    <automation_approch>In a loop of 1000:
1. Launch Cobalt using launch method of RDKShell
2. Set video URL using deeplink method of Cobalt.
3. Validate video playback using proc entries
4. Press home button using generateKey method of RDKShell
5. Launch WebKitBrowser
6. Set URL using WebKitBrowser.1.url method
7. Verify whether URL is set using above method
8. Press home button 
9. Validate CPU load and memory usage using DeviceInfo.1.systeminfo method
</automation_approch>
    <expected_output>DUT must be stable after every iteration. CPU load and memory usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_WebKitBrowser_Switch</test_script>
    <skipped>No</skipped>
    <release_version>M90</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import StabilityTestVariables
import json
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_WebKitBrowser_Switch');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    status = "SUCCESS"
    error_in_loop = False
    plugin_operations_dict = {}
    plugin_validation_dict = {}
    cobalt_test_url = StabilityTestVariables.cobalt_test_url
    webkit_test_url = StabilityTestVariables.webkit_test_url
    max_iterations = StabilityTestVariables.switch_plugins_max_count
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and  all(value != "" for value in (cobalt_test_url,webkit_test_url,max_iterations)) and validation_dict != {}:
        enterkey_keycode = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
        generatekey_method = 'org.rdk.RDKShell.1.generateKey'
        cobalt_operations_list = [{'Cobalt.1.deeplink':cobalt_test_url},{generatekey_method:enterkey_keycode},{generatekey_method:enterkey_keycode}]
        webkit_operations_list = []
        webkit_validation_details = ['WebKitBrowser.1.url',webkit_test_url]
        webkit_operations_dict = {webkit_validation_details[0]:webkit_validation_details[1]}
        webkit_operations_list.append(webkit_operations_dict)
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
            cobalt_validation_details = ["video_validation", validation_dict["ssh_method"], credentials, validation_dict["video_validation_script"]]
        else:
            cobalt_validation_details = ["no_validation"]
        cobalt_operations = json.dumps(cobalt_operations_list)
        webkit_operations = json.dumps(webkit_operations_list)
        cobalt_validation = json.dumps(cobalt_validation_details)
        webkit_validation = json.dumps(webkit_validation_details)
        plugin_operations_dict["Cobalt"] = cobalt_operations
        plugin_operations_dict["WebKitBrowser"] = webkit_operations
        plugin_validation_dict["Cobalt"] = cobalt_validation
        plugin_validation_dict["WebKitBrowser"] = webkit_validation
        for count in range(0,max_iterations):
            result_dict = {}
            for plugin in ["Cobalt","WebKitBrowser"]:
                tdkTestObj = obj.createTestStep('rdkservice_validatePluginFunctionality')
                tdkTestObj.addParameter("plugin",plugin)
                tdkTestObj.addParameter("operations",plugin_operations_dict[plugin])
                tdkTestObj.addParameter("validation_details",plugin_validation_dict[plugin])
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails();
                if expectedResult in result and details == "SUCCESS" :
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Press Home
                    resident_app = "ResidentApp"
                    params = '{"keys":[ {"keyCode": 36,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    rdkshell_result = tdkTestObj.getResult()
                    time.sleep(10)
                    if expectedResult in rdkshell_result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                        tdkTestObj.executeTestCase(expectedResult)
                        zorder = tdkTestObj.getResultDetails()
                        zorder_status = tdkTestObj.getResult()
                        if expectedResult in zorder_status :
                            zorder = ast.literal_eval(zorder)["clients"]
                            print "zorder: ",zorder
                            if zorder[0].lower() == resident_app.lower():
                                print "\n Home screen is reached"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Home screen is not reached"
                                tdkTestObj.setResultStatus("FAILURE")
                                error_in_loop = True
                                break
                        else:
                            print "\n Error while getting zorder value"
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    else:
                        print "\n Error while pressing Home button"
                        tdkTestObj.setResultStatus("FAILURE")
                        error_in_loop = True
                        break
                else:
                    print "\n Error while validating the {} plugin functionality".format(plugin)
                    tdkTestObj.setResultStatus("FAILURE")
                    error_in_loop = True
                    break
            else:
                #Validate resource usage
                print "\n Validate Resource usage for iteration:{}".format(count+1)
                tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                tdkTestObj.executeTestCase(expectedResult)
                resource_usage = tdkTestObj.getResultDetails()
                result = tdkTestObj.getResult()
                if expectedResult in result and resource_usage != "ERROR":
                    tdkTestObj.setResultStatus("SUCCESS")
                    cpuload = resource_usage.split(',')[0]
                    memory_usage = resource_usage.split(',')[1]
                    result_dict["iteration"] = count+1
                    result_dict["cpu_load"] = float(cpuload)
                    result_dict["memory_usage"] = float(memory_usage)
                    result_dict_list.append(result_dict)
                else:
                    print "\n Error while validating Resource usage"
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            if error_in_loop:
                print "\n Error occurred, stopping the test"
                break
        else:
            print "\n Successfully Completed {} iterations".format(max_iterations)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    status = set_plugins_status(obj,curr_plugins_status_dict)
    time.sleep(10)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability")
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE")
