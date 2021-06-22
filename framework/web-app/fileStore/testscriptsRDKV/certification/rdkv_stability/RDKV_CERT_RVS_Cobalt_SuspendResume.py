##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <name>RDKV_CERT_RVS_Cobalt_SuspendResume</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getCPULoad</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to suspend and resume the Cobalt plugin for a given number of times.</synopsis>
  <groups_id/>
  <execution_time>420</execution_time>
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
    <test_case_id>RDKV_STABILITY_07</test_case_id>
    <test_objective>The objective of this test is to suspend and resume the Cobalt plugin for a given number of times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>suspend_resume_max_count : int</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable Cobalt only.
2. Suspend Cobalt using RDKShell plugin .
3. Resume Cobalt using RDKShell plugin.
4. Check if the CPU load and Memory usage is within the expected value.
5. Repeat steps 2 to 4 for given number of times.
6. Revert all values.</automation_approch>
    <expected_output>Suspend and Resume should happen and the cpu load and memory usage must be within the expected values.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_SuspendResume</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from rdkv_stabilitylib import *
import StabilityTestVariables
from rdkv_performancelib import *
import StabilityTestVariables


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_SuspendResume');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
max_count = StabilityTestVariables.suspend_resume_max_count

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"resumed","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully"
        time.sleep(10)
        iteration = 0
        completed = True
        while iteration < max_count:
            print "\nSuspend the Cobalt plugin :\n"
            params = '{"callsign":"Cobalt"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.suspend")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            time.sleep(5)
            result = tdkTestObj.getResult()
            if result == expectedResult:
                tdkTestObj.setResultStatus("SUCCESS")
                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                tdkTestObj.addParameter("plugin","Cobalt")
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                cobalt_status = tdkTestObj.getResultDetails()
                if cobalt_status == 'suspended' and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\nCobalt plugin Suspended Successfully\n"
                    print "\nResume the Cobalt plugin\n"
                    params = '{"callsign": "Cobalt", "type":"", "uri":"", "x":0, "y":0, "w":1920, "h":1080}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    time.sleep(5)
                    result = tdkTestObj.getResult()
                    if result == expectedResult:
                        tdkTestObj.setResultStatus("SUCCESS")
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                        tdkTestObj.addParameter("plugin","Cobalt")
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        cobalt_status = tdkTestObj.getResultDetails()
                        if cobalt_status == 'resumed' and expectedResult in result:
                            print "\nCobalt plugin Resumed Successfully\n"
                            result_dict = {}
                            iteration += 1
			    print "\n ##### Validating CPU load and memory usage #####\n"
                            print "Iteration : ", iteration
                            tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
                            tdkTestObj.executeTestCase(expectedResult)
                            status = tdkTestObj.getResult()
                            result = tdkTestObj.getResultDetails()
                            if expectedResult in status and result != "ERROR":
                                tdkTestObj.setResultStatus("SUCCESS")
                                cpuload = result.split(',')[0]
                                memory_usage = result.split(',')[1]
                                result_dict["iteration"] = iteration
                                result_dict["cpu_load"] = float(cpuload)
                                result_dict["memory_usage"] = float(memory_usage)
                                result_dict_list.append(result_dict)
			    else:
				completed = False
				print "\n Error while validating Resource usage"
                		tdkTestObj.setResultStatus("FAILURE")
                		break
                        else:
                            print "Cobalt plugin is not in Resumed state, current Cobalt Status: ",cobalt_status
                            tdkTestObj.setResultStatus("FAILURE")
                            completed = False
                            break
                    else:
                        print "Unable to set Cobalt plugin to resumed state"
                        tdkTestObj.setResultStatus("FAILURE")
                        completed = False
                        break
                else:
                    print "Cobat is not in Suspended state, current Cobalt Status: ",cobalt_status
                    tdkTestObj.setResultStatus("FAILURE")
                    completed = False
                    break
            else:
                print "Unable to set Cobalt plugin to suspended state"
                tdkTestObj.setResultStatus("FAILURE")
                completed = False
                break
        if(completed):
            print "\nsuccessfully completed the {} iterations\n".format(iteration)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

