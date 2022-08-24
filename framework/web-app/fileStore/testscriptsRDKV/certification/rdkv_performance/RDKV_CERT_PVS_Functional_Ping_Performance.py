##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_Ping_Performance</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to check the packet loss and calculate the trip time using ping</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_101</test_case_id>
    <test_objective>The objective of this test is to check the packet loss and calculate the trip time using ping</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.Ip or host name
2. Threshold value for trip time</input_parameters>
    <automation_approch>1.Ping the host name
2. Check for packet loss
3. Validate the trip time</automation_approch>
    <expected_output>There should be no packet loss and trip time should be less than the average trip time</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Ping_Performance</test_script>
    <skipped>No</skipped>
    <release_version>M97</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import ip_change_detection_utility
from datetime import datetime
from ip_change_detection_utility import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True );

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Ping_performance');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

# Execution Summary Variable
Summ_list=[]

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    revert = "NO"
    ping_test_destination = PerformanceTestVariables.ping_test_destination
    revert="NO"
    plugins_list = ["org.rdk.System"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    plugins_list = ["org.rdk.Network"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"org.rdk.Network":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    print "\nPre conditions for the test are set successfully"
    params = '{"endpoint": "'+ping_test_destination+'", "packets": 10}'
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    tdkTestObj.addParameter("method","org.rdk.Network.1.ping");
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    ping_details = tdkTestObj.getResultDetails()
    print ping_details
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        ping_details = tdkTestObj.getResultDetails()
        ping_details_dict = eval(ping_details)
        packet_loss = ping_details_dict["packetLoss"]
        if int(packet_loss) == 0 :
            print "No packet loss"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print"Packet loss is greater than zero"
            tdkTestObj.setResultStatus("FAILURE")
        triptime = ping_details_dict["tripAvg"]
        conf_file,result = getConfigFileName(tdkTestObj.realpath)
        result1, triptime_threshold_value = getDeviceConfigKeyValue(conf_file,"TRIPTIME_THRESHOLD_VALUE")
        if triptime_threshold_value != "":
            print "\n Average Trip Time: ",triptime
            Summ_list.append('Time taken for average Trip:{}'.format(triptime))
            print "\n Threshold value for trip time:",triptime_threshold_value
            Summ_list.append('Threshold value for triptime:{}'.format(triptime_threshold_value))
            if float(triptime) < float(triptime_threshold_value):
                 print "\n The trip time is lesser than threshold time\n"
            else:
                 tdkTestObj.setResultStatus("FAILURE")
                 print "\n The trip time is higher than threshold time \n"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Failed to get the threshold value from config file"
    else:
        print "Not able to ping"
        tdkTestObj.setResultStatus("FAILURE")
  
  
    getSummary(Summ_list,obj)
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

