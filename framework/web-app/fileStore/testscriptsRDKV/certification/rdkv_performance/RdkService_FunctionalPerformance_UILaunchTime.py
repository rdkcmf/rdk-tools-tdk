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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RdkService_FunctionalPerformance_UILaunchTime</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The script is to get the time to launch the main UI after reboot.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_08</test_case_id>
    <test_objective>The script is to get the time to launch the main UI after reboot.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Test Manager time should be in sync with UTC</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ui_app_url : string</input_parameters>
    <automation_approch>1. Save the current system time in UTC.
2. Reboot the DUT.
3. Find the timestamp of  "LoadFinished" log of ui_app_url (URL of UI Application)
4. Calculate output by finding the difference between timestamp in step 4 and time got in step 1.</automation_approch>
    <expected_output>The time taken should be within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RdkService_FunctionalPerformance_UILaunchTime</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestVariables import *
import rebootTestUtility
from rebootTestUtility import *
from datetime import datetime
import time
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_FunctionalPerformance_UILaunchTime')

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
        print "\n Rebooted device successfully \n"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo")
        tdkTestObj.addParameter("reqValue","uptime")
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        if expectedResult in result:
            uptime = int(tdkTestObj.getResultDetails())
            if uptime < 240:
                print "\n Device is rebooted and uptime is: {}\n".format(uptime)
                time.sleep(30)
                tdkTestObj.setResultStatus("SUCCESS")
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","ResidentApp.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                ui_app_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if ui_app_url != "" and  result == "SUCCESS" :
                    ui_app_url = ui_app_url.split('?')[0]
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                    tdkTestObj.addParameter("realpath",obj.realpath)
                    tdkTestObj.addParameter("deviceIP",obj.IP)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                    if ssh_param_dict != {} and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        if ssh_param_dict["ssh_method"] == "directSSH":
                            if ssh_param_dict["password"] == "None":
                                password = ""
                            else:
                                password = ssh_param_dict["password"]
                            credentials = ssh_param_dict["host_name"]+','+ssh_param_dict["user_name"]+','+password
                        else:
                            #TODO
                            print "selected ssh method is {}".format(ssh_param_dict["ssh_method"])
                            pass
                        command = 'cat /opt/logs/wpeframework.log | grep -inr LoadFinished.*url.*'+ui_app_url+'| tail -1'
                        #get the log line containing the loadfinished info from wpeframework log
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",credentials)
                        tdkTestObj.addParameter("command",command)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        output = tdkTestObj.getResultDetails()
                        if output != "EXCEPTION" and expectedResult in result:
                            load_finished_list = output.split('\n')
                            load_finished_line = ""
                            for item in load_finished_list:
                                if "LoadFinished:" in item:
                                    load_finished_line = item
                            if load_finished_line != "" and '"httpstatus": 200' in load_finished_line:
                                load_finished_time = getTimeStampFromString(load_finished_line)
                                print "\nDevice reboot initiated at :{} (UTC)\n".format(start_time)
                                print "UI load finished at :{} (UTC) \n".format(load_finished_time)
                                start_time_millisec = getTimeInMilliSec(start_time)
                                loadfinished_time_millisec = getTimeInMilliSec(load_finished_time)
                                ui_uptime = loadfinished_time_millisec - start_time_millisec
                                print "Time taken for the UI to load after reboot : {} ms\n".format(ui_uptime)
                                conf_file,result = getConfigFileName(tdkTestObj.realpath)
                                result, ui_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"UI_LAUNCH_TIME_THRESHOLD_VALUE")
                                if result == "SUCCESS":
                                    if 0 < int(ui_uptime) < int(ui_launch_threshold_value):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "\n The time taken for UI to load after reboot is within the expected limit\n"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "\n The time taken for UI to load after reboot is not within the expected limit \n"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "\n Failed to get the threshold value from config file"
                            else:
                                print "\n ui app url is not loaded in DUT"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error occurred while executing the command:{} in DUT,\n Please check the SSH details \n".format(command)
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n please configure the details in device config file"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing ResidentApp.1.url method"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "\n device is not rebooted, device uptime:{}".format(uptime)
        else:
            print "\n Failed to get the uptime";
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Error occurred during reboot"
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
