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
  <name>RDKV_CERT_RVS_SSH</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do ssh to device for 30 times and see if any crash occurs</synopsis>
  <groups_id/>
  <execution_time>240</execution_time>
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
    <test_case_id>RDKV_STABILITY_30</test_case_id>
    <test_objective>The objective of this test is to do ssh to device for 30 times and see if any crash occurs</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. SSH to device should work</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ssh_max_count :int</input_parameters>
    <automation_approch>1. In a loop of minimum 30 do ssh to DUT
2. Execute uptime command in DUT
3. Validate CPU load and memory usage in each iteration.
</automation_approch>
    <expected_output>No crash should occur during SSH to DUT</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_SSH</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import StabilityTestVariables
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_SSH');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    do_ssh_max_count = StabilityTestVariables.ssh_max_count
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if ssh_param_dict != {} and expectedResult in result :
        tdkTestObj.setResultStatus("SUCCESS")
        command = 'uptime'
        for count in range(0,do_ssh_max_count):
            output = ''
            result_dict = {}
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            output = tdkTestObj.getResultDetails()
            if output != "EXCEPTION" and expectedResult in result and 'users' in output:
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Output of {} command :{}\n".format(command,output.split('\n')[1])
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
                print "\n Error occured during SSH to the device \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\nSuccessfully completed the {} iterations \n".format(do_ssh_max_count)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n Please configure SSH details in device config file\n"
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_stability")
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE")
