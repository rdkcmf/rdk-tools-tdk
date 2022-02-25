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
  <name>RDKV_CERT_PVS_Functional_ValidateIPAddress</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to check whether the DUT has a valid IP address.</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_60</test_case_id>
    <test_objective>The objective of this test is to check whether the DUT has a valid IP address.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Check current interface of the device 
2. SSH to the device
3. Get the ip address using linux command based on the interface.
4. Validate the ip address based on ip address type.
</automation_approch>
    <expected_output>1.  DUT should be having a valid IP address</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_ValidateIPAddress</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from ip_change_detection_utility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_ValidateIPAddress');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\n Check Pre conditions"
    revert_plugins_dict = {}
    interface_name_key = ""
    #Check current interface
    current_interface,revert_nw = check_current_interface(obj)
    if revert_nw == "YES":
        revert_plugins_dict["org.rdk.Network"] = "deactivated"
    if current_interface == "ETHERNET":
        interface_name_key = "ETHERNET_INTERFACE"
    elif current_interface == "WIFI":
        interface_name_key = "WIFI_INTERFACE"
    conf_file,file_status = getConfigFileName(obj.realpath)
    interface_config_status,interface_name = getDeviceConfigKeyValue(conf_file,interface_name_key)
    ip_address_type_status,ip_address_type = getDeviceConfigKeyValue(conf_file,"DEVICE_IP_ADDRESS_TYPE")
    if current_interface != "EMPTY" and file_status == "SUCCESS"  and all(value != "" for value in (interface_name,ip_address_type)):
        tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
        tdkTestObj.addParameter("realpath",obj.realpath)
        tdkTestObj.addParameter("deviceIP",obj.IP)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
        if expectedResult in result and ssh_param_dict != {}:
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(10)
            if ip_address_type.lower() == "ipv4":
                ip_address_num = '4'
            else:
                ip_address_num = '6'
            command = "/sbin/ip -o -" + ip_address_num + " addr list " + interface_name.lower() + " | awk '{print $4}' | cut -d/ -f1"
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            output = tdkTestObj.getResultDetails()
            if output != "EXCEPTION" and expectedResult in result and len(output.split('\n')) >= 3:
                ip_address = output.split('\n')[1].strip()
                if ip_address_type == "ipv4":
                    is_valid_ip_address = is_valid_ipv4_address(ip_address)
                else:
                    is_valid_ip_address = is_valid_ipv6_address(ip_address)
                if is_valid_ip_address:
                    print "\n DUT is having a valid {} address: {}".format(ip_address_type,ip_address)
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n {} is not a valid ip address".format(ip_address)
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing command in DUT"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Please configure the details in device configuration file"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
