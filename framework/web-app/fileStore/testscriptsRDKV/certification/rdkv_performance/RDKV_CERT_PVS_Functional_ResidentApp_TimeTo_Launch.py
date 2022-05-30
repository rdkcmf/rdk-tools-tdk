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
  <name>RDKV_CERT_PVS_Functional_ResidentApp_TimeTo_Launch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to launch ResidentApp</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_94</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to launch ResidentApp</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Reboot the DUT
2. Check the wpeframework.log for the application launched log
3. Validate the time taken to launch the ResidentApp</automation_approch>
    <expected_output>The time taken should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_ResidentApp_TimeTo_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M96</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
from rdkv_performancelib import *
from datetime import datetime
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_ResidentApp_TimeTo_Launch')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    print "\n Check Pre conditions"
    conf_file,file_status = get_configfile_name(obj)
    result1, reboot_wait_time = getDeviceConfigKeyValue(conf_file,"REBOOT_WAIT_TIME")
    result2, threshold_uptime = getDeviceConfigKeyValue(conf_file,"THRESHOLD_UPTIME")
    result3, launch_time_threshold_value = getDeviceConfigKeyValue(conf_file,"RESIDENTAPP_LAUNCH_TIME_THRESHOLD_VALUE")
    Summ_list.append('RESIDENTAPP_LAUNCH_TIME_THRESHOLD_VALUE :{}ms'.format(launch_time_threshold_value))
    result4, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
    if all(value != "" for value in (reboot_wait_time,threshold_uptime,launch_time_threshold_value,offset)):
        #Reboot device
        tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
        tdkTestObj.addParameter("waitTime",int(reboot_wait_time))
        #get the current system time before reboot
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Rebooted the device successfully"
            uptime = get_device_uptime(obj)
            if uptime != -1 and uptime < int(threshold_uptime):
                print "\n Device is rebooted and uptime is: {}\n".format(uptime)
                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                tdkTestObj.addParameter("realpath",obj.realpath)
                tdkTestObj.addParameter("deviceIP",obj.IP)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                if ssh_param_dict != {} and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    command = 'cat /opt/logs/wpeframework.log | grep -inr Application.*ResidentApp.*took.*milliseconds | head -n 1'
                    #get the log line containing the ResidentApp launch info from wpeframework log
                    tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                    tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                    tdkTestObj.addParameter("command",command)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    output = tdkTestObj.getResultDetails()
                    if output != "EXCEPTION" and expectedResult in result:
                        required_log = output.split('\n')[1]
                        if required_log != "":
                            log_list = required_log.split(' ')
                            time_taken = int(float(log_list[log_list.index('took')+1]))
                            print "\n Time taken for launching ResidentApp : {} ms".format(time_taken)
                            Summ_list.append('Time taken for launching ResidentApp :{}ms'.format(time_taken))
                            print "\n Threshold value for time taken for launching ResidentApp: {} ms".format(launch_time_threshold_value)
                            if 0 < int(time_taken) < (int(launch_time_threshold_value) + int(offset)) :
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n The time taken for launching ResidentApp is within the expected limit"
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print "\n The time taken for launching ResidentApp is not within the expected limit"
                        else:
                            print "\n ResidentApp launched logs are not available"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while executing commands in device"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Please configure the SSH parameters in device config file"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while validating uptime"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while rebooting the device"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Please configure the variables in device config file"
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance")
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
