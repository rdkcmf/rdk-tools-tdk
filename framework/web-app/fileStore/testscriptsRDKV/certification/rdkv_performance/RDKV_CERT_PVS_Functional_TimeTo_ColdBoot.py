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
  <name>RDKV_CERT_PVS_Functional_TimeTo_ColdBoot</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken for cold boot.</synopsis>
  <groups_id/>
  <execution_time>360</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_93</test_case_id>
    <test_objective>The objective of this test is to validate the time taken for cold boot.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Keep the DUT idle for given time using sleep method of python
2. Reboot the DUT
3. Validate the time taken for cold boot using the logs from wpeframework.log
  </automation_approch>
    <expected_output>The time taken for cold boot should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_ColdBoot</test_script>
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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_ColdBoot')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    print "Check Pre conditions"
    conf_file,file_status = get_configfile_name(obj)
    result1, wait_time = getDeviceConfigKeyValue(conf_file,"COLDBOOT_IDLE_WAIT_TIME")
    result2, reboot_wait_time = getDeviceConfigKeyValue(conf_file,"REBOOT_WAIT_TIME")
    result3, threshold_uptime = getDeviceConfigKeyValue(conf_file,"THRESHOLD_UPTIME")
    result4, cold_boot_time_threshold_value = getDeviceConfigKeyValue(conf_file,"COLDBOOT_TIME_THRESHOLD_VALUE")
    result5, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
    if all(value != "" for value in (wait_time,reboot_wait_time,threshold_uptime,cold_boot_time_threshold_value,offset)):
        #Keep device idle 
        time.sleep(int(wait_time))
        #Reboot device
        tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
        tdkTestObj.addParameter("waitTime",int(reboot_wait_time))
        #get the current system time before reboot
        start_time = str(datetime.utcnow()).split()[1]
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
                    command = 'cat /opt/logs/wpeframework.log | grep -inr Started.*wpeframework | head -n 1'
                    #get the log line containing the wpeframework started info from wpeframework log
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
                            wpeframework_started_time = getTimeStampFromString(required_log)
                            print "\n Device reboot initiated at :{}".format(start_time)
                            print "\n WPEFramework started at :{}".format(wpeframework_started_time)
                            start_time_millisec = getTimeInMilliSec(start_time)
                            wpeframwork_start_time_millisec = getTimeInMilliSec(wpeframework_started_time)
                            timeto_coldboot = wpeframwork_start_time_millisec - start_time_millisec
                            print "\n Time taken for the cold boot : {} ms".format(timeto_coldboot)
                            print "\n Threshold value for time taken for cold boot: {} ms".format(cold_boot_time_threshold_value)
                            if 0 < int(timeto_coldboot) < (int(cold_boot_time_threshold_value) + int(offset)) :
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n The time taken for cold boot is within the expected limit"
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print "\n The time taken for cold boot is not within the expected limit"
                        else:
                            print "\n wpeframework started logs are not available"
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
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
