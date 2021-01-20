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
  <name>RdkService_ActivateDeactivate_StabilityTest</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this script is to activate and deactivate 3 plugins for 100 times and get the status of Controller and validate CPU load and memory usage.</synopsis>
  <groups_id/>
  <execution_time>120</execution_time>
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
    <test_case_id>RDKV_STABILITY_10</test_case_id>
    <test_objective>The objective of this script is to activate and deactivate 3 plugins for 100 times and get the status of Controller and validate CPU load and memory usage.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>3 plugins </input_parameters>
    <automation_approch>1. Get the plugins from StabilityVariables file
2. Get the current status of plugins
3. Change the status of plugins in a loop, validate controller plugin status and validate the cpu and memory load in the loop.</automation_approch>
    <expected_output>Plugin status should be expected ones and cpu load and memory usage must be in expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RdkService_ActivateDeactivate_StabilityTest</test_script>
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
from rdkv_performancelib import *
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_ActivateDeactivate_StabilityTest');

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
    plugins_list = []
    revert = "NO"
    device_info_status_dict = get_plugins_status(obj,["DeviceInfo"])
    if device_info_status_dict["DeviceInfo"] != "activated" :
        revert = "YES"
        set_plugins_status(obj,{"DeviceInfo":"activated"})
    plugins = StabilityTestVariables.activate_deactivate_plugins
    if plugins != "":
        for plugin in plugins.split(","):
            plugins_list.append(plugin)
        print "\n Plugins used for the test: ",plugins_list
        print "\n Get the current status of plugins \n"
        curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
        print "\n Initial status dictionary :",curr_plugins_status_dict
        new_status_dict = {}
        error_in_loop = False
        for count in range(0,activate_deactivate_max_count):
            print "\n########## Iteration :{} ##########\n".format(count+1)
            result_dict = {}
            for inner_count in range(0,2):
                print "\n##### Inner iteration : {}.{} #####\n".format(count+1,inner_count+1)
                for plugin in curr_plugins_status_dict:
                    if curr_plugins_status_dict[plugin] == "deactivated" :
                        new_status_dict[plugin] = 'activate'
                    else:
                        new_status_dict[plugin] = 'deactivate'
                for plugin in new_status_dict:
                    if new_status_dict[plugin] == 'activate':
                        expected_status = ['activated','resumed']
                    else:
                        expected_status = ['deactivated']
                    print "\n Setting {} plugin to {} \n".format(plugin,new_status_dict[plugin])
                    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                    tdkTestObj.addParameter("plugin",plugin)
                    tdkTestObj.addParameter("status",new_status_dict[plugin])
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
                            status = tdkTestObj.getResultDetails()
                            print "\n Current status of {} plugin : {}\n".format(plugin,status)
                            if status in expected_status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                curr_plugins_status_dict[plugin] = status
                            else:
                                print "{} Status not set to {} , current status: {}".format(plugin,new_status_dict[plugin],status)
                                tdkTestObj.setResultStatus("FAILURE")
                                error_in_loop = True
                                break
                        else:
                            print "Error while getting {} plugin status".format(plugin)
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    else:
                        print "Error while setting {} plugin status to {}".format(plugin,new_status_dict[plugin])
                        tdkTestObj.setResultStatus("FAILURE")
                        error_in_loop = True
                        break
                if error_in_loop:
                    print "\n Stopping the test !!!"
                    break
            if error_in_loop:
                break
            print "\n##### Inner iterations for  activation and deactivation of plugins completed ##### \n"
            #check status of controller
            print "\n ##### Checking current status of Controller plugin #####\n"
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Controller")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                status = tdkTestObj.getResultDetails()
                print "\n Current status of Controller plugin : {}\n".format(status)
                if status == "activated":
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "Controller plugin is not in activated state, current status: ",status
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "Error while getting status of Controller plugin"
                tdkTestObj.setResultStatus("FAILURE")
                break
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
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n[Error] Please configure the plugins !!!\n"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,device_info_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE");
