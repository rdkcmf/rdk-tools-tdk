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
  <version>4</version>
  <name>RDKV_CERT_PVS_Functional_TimeTo_Ethernet_InterfaceUp</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of the test is to find the time to get the eth0 interface IP after reboot</synopsis>
  <groups_id/>
  <execution_time>7</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_07</test_case_id>
    <test_objective>The objective of the test is to find the time to get the eth0/wlan0 interface IP after reboot.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Test Manager time should be in sync with UTC
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Save the current time in UTC.
2. Reboot the DUT.
3. Find the timestamp of  "eth0 up" from nlmon.log
4. Calculate output by finding the difference between timestamp in step 4 and time got in step 1.</automation_approch>
    <expected_output>The time taken should be within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_Ethernet_InterfaceUp</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
from StabilityTestVariables import *
import rebootTestUtility
from rebootTestUtility import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_Ethernet_InterfaceUp');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
    tdkTestObj.addParameter("waitTime",rebootwaitTime)
    #get the current system time before reboot
    start_time = str(datetime.utcnow()).split()[1]
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print "Rebooted device successfully"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo")
        tdkTestObj.addParameter("reqValue","uptime")
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        if expectedResult in result:
            uptime = int(tdkTestObj.getResultDetails())
            if uptime < 240:
                tdkTestObj.setResultStatus("SUCCESS")
                print "Device is rebooted and uptime is: {}".format(uptime)
                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                tdkTestObj.addParameter("realpath",obj.realpath)
                tdkTestObj.addParameter("deviceIP",obj.IP)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                if expectedResult in result and ssh_param_dict != {}:
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(10)
                    command = 'cat /opt/logs/nlmon.log | grep -inr "eth0 up"| head -n 1'
                    check_print = '/lib/rdk/networkLinkEvent.sh'
                    #get the log line containing the interface_up info from nlmon.log
                    tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                    tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                    tdkTestObj.addParameter("command",command)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    output = tdkTestObj.getResultDetails()
                    if output != "EXCEPTION" and expectedResult in result:
                        interface_up_list = output.split('\n')
                        interface_up_line = ""
                        for item in interface_up_list:
                             if check_print in item:
                                interface_up_line = item
                        if interface_up_line != "":
                            interface_up_time = getTimeStampFromString(interface_up_line)
                            print "\nDevice reboot initiated at :{} (UTC)".format(start_time)
                            print "eth0 interface became up  at :{} (UTC)  ".format(interface_up_time)
                            start_time_millisec = getTimeInMilliSec(start_time)
                            interface_up_time_millisec = getTimeInMilliSec(interface_up_time)
                            interface_uptime = interface_up_time_millisec - start_time_millisec
                            print "Time taken for the eth0 interface to up after reboot : {} ms\n".format(interface_uptime)
                            conf_file,result = getConfigFileName(tdkTestObj.realpath)
                            result1, if_uptime_threshold_value = getDeviceConfigKeyValue(conf_file,"IF_UPTIME_THRESHOLD_VALUE")
                            result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                            if all(value != "" for value in (if_uptime_threshold_value,offset)):
                                if 0 < int(interface_uptime) < (int(if_uptime_threshold_value) + int(offset)) :
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "\n The time taken for eth0 interface to up after reboot is within the expected limit\n"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "\n The time taken for eth0 interface to up after reboot is not within the expected limit \n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to get the threshold value from config file"
                        else:
                            print "eth0 interface is not up in DUT"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "Error occurred while executing the command:{} in DUT, \n Please check the SSH details \n".format(command)
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "please configure the details in device configuration file"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "Device is not rebooted, uptime:{}".format(uptime)
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Failed to get the uptime"
    else:
        print "Error occurred during reboot"
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"

