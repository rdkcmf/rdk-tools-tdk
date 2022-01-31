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
  <name>RDKV_CERT_PVS_Functional_TimeTo_LaunchUI</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to launch the main UI when device is connected to Ethernet.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_52</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to launch the main UI when device is connected to Ethernet.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Time in test manager and time in DUT should be in sync with UTC.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Save the current system time in UTC.
2. Reboot the DUT.
3. Find the timestamp of "URLChanged" logs with  ui_app_url (URL of UI Application) from wpeframework.log file
4. Calculate output by finding the difference between saved system time and timestamp from log.
 </automation_approch>
    <expected_output>The time taken to launch UI must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_LaunchUI</test_script>
    <skipped>No</skipped>
    <release_version>M90</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from datetime import datetime
from ip_change_detection_utility import *
import StabilityTestVariables
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_LaunchUI');
#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    rebootwaitTime = StabilityTestVariables.rebootwaitTime
    connect_status, revert_dict, revert_plugin_status = connect_to_interface(obj, "ETHERNET")
    if connect_status == "SUCCESS":
        tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
        tdkTestObj.addParameter("waitTime",rebootwaitTime)
        #get the current system time before reboot
        start_time = str(datetime.utcnow()).split()[1]
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Rebooted device successfully"
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
            tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo")
            tdkTestObj.addParameter("reqValue","uptime")
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult()
            if expectedResult in result:
                uptime = int(tdkTestObj.getResultDetails())
                if uptime < 240:
                    print "\n Device is rebooted and uptime is: {}".format(uptime)
                    time.sleep(60)
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","ResidentApp.1.url");
                    tdkTestObj.executeTestCase(expectedResult);
                    ui_app_url = tdkTestObj.getResultDetails();
                    result = tdkTestObj.getResult()
                    if ui_app_url != "" and  result == "SUCCESS" :
                        print "\n Main UI URL :",ui_app_url
                        ui_app_url = ui_app_url.split('#')[0]
                        print "\n URL to check in device logs: ",ui_app_url
                        tdkTestObj.setResultStatus("SUCCESS")
                        tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                        tdkTestObj.addParameter("realpath",obj.realpath)
                        tdkTestObj.addParameter("deviceIP",obj.IP)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                        if ssh_param_dict != {} and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            command = 'cat /opt/logs/wpeframework.log | grep -inr URLChanged.*url.*'+ui_app_url+'| tail -1'
                            #get the log line containing the urlfinished info from wpeframework log
                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                            tdkTestObj.addParameter("command",command)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            output = tdkTestObj.getResultDetails()
                            if output != "EXCEPTION" and expectedResult in result:
                                url_finished_line = output.split('\n')[1]
                                if url_finished_line != "":
                                    url_finished_time = getTimeStampFromString(url_finished_line)
                                    print "\n Device reboot initiated at :{} ".format(start_time)
                                    Summ_list.append('Device reboot initiated at :{}'.format(start_time))
                                    print "\n UI load finished at :{} ".format(url_finished_time)
                                    Summ_list.append('UI load finished at :{}'.format(url_finished_time))
                                    start_time_millisec = getTimeInMilliSec(start_time)
                                    urlfinished_time_millisec = getTimeInMilliSec(url_finished_time)
                                    ui_uptime = urlfinished_time_millisec - start_time_millisec
                                    print "\n Time taken for the UI to load after reboot : {} ms".format(ui_uptime)
                                    Summ_list.append('Time taken for the UI to load after reboot :{}ms'.format(ui_uptime))
                                    conf_file,result = getConfigFileName(tdkTestObj.realpath)
                                    result1, ui_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"MAIN_UI_LAUNCH_TIME_THRESHOLD_VALUE")
                                    Summ_list.append('MAIN_UI_LAUNCH_TIME_THRESHOLD_VALUE :{}ms'.format(ui_launch_threshold_value))
                                    result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                    if all(value != "" for value in (ui_launch_threshold_value,offset)):
                                        print "\n Threshold value for time taken for UI to load after reboot: {} ms".format(ui_launch_threshold_value)
                                        if 0 < int(ui_uptime) < (int(ui_launch_threshold_value) + int(offset)) :
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "\n The time taken for UI to load after reboot is within the expected limit"
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "\n The time taken for UI to load after reboot is not within the expected limit"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "\n Failed to get the threshold value from config file"
                                else:
                                    print "\n UI App URL is not loaded in DUT"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error occurred while executing the command:{} in DUT,\n Please check the SSH details".format(command)
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Please configure the details in device config file"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while executing ResidentApp.1.url method"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print "\n Device is not rebooted, device uptime:{}".format(uptime)
            else:
                print "\n Failed to get the uptime";
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error occurred during reboot"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    revert_if = revert_dict.pop("revert_if")
    current_connection = revert_dict.pop("current_if")
    if revert_if:
        result_status, revert_dict_new, revert_plugins = connect_to_interface(obj, current_connection)
        time.sleep(30)
        if result_status == "FAILURE":
            obj.setLoadModuleStatus("FAILURE")
    if revert_plugin_status == "YES":
        status = set_plugins_status(obj,revert_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE");
