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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_TimeTo_SwitchTo_MainUI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to get time required to launch main UI from another window.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_30</test_case_id>
    <test_objective>The objective of this test is to get time required to launch main UI from another window.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Time in Test manager and DUT should be in sync with UTC.
2. wpeframework process must be running in DUT.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch Cobalt or Webkit in device
2. Get the current time
3. Press home key (36) using generateKey
4. Check the wpeframework log for "ResidentApp moveToFront Success".
5. Measure the time taken to get this print
6. Time must be greater than 0 and within threshold+offset</automation_approch>
    <expected_output>Resident App must be launched while clicking home key.
Time taken to launch UI from another window. should be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_SwitchTo_MainUI</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from datetime import datetime
import json
from rdkv_performancelib import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_SwitchTo_MainUI');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if ssh_param_dict != {} and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        #Launch Cobalt
        cobalt_launch_status = launch_cobalt(obj)
        time.sleep(20)
        if cobalt_launch_status == "SUCCESS":
            print "\n Pressing Home button \n"
            params = '{"keys":[ {"keyCode": 36,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            start_time = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult)
            rdkshell_result = tdkTestObj.getResult()
            time.sleep(20)
            if expectedResult in rdkshell_result:
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
                command = 'cat /opt/logs/wpeframework.log | grep -inr ResidentApp.*moveToFront.*Success| tail -1'
                #get the log line containing the main UI loaded info from wpeframework log
                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                tdkTestObj.addParameter("credentials",credentials)
                tdkTestObj.addParameter("command",command)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                output = tdkTestObj.getResultDetails()
                if output != "EXCEPTION" and expectedResult in result:
                    if "ResidentApp moveToFront Success" in output:
                        required_line = output.split('\n')[1]
                        main_ui_launched_time = getTimeStampFromString(required_line)
                        print "\n Home button pressed at :{} (UTC)".format(start_time)
                        print "\n Main UI launched at :{} (UTC)  ".format(main_ui_launched_time)
                        start_time_millisec = getTimeInMilliSec(start_time)
                        main_ui_launched_time_millisec = getTimeInMilliSec(main_ui_launched_time)
                        ui_launchtime = main_ui_launched_time_millisec - start_time_millisec
                        print "\n Time taken for launching Main UI from another window  : {} ms\n".format(ui_launchtime)
                        conf_file,result = getConfigFileName(tdkTestObj.realpath)
                        result1, ui_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"MAIN_UI_SWITCH_TIME_THRESHOLD_VALUE")
                        result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        if result1 == result2 == "SUCCESS":
                            if 0 < int(ui_launchtime) < (int(ui_launch_threshold_value) + int(offset)):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "\n The time taken for launching Main UI from another window is within the expected limit\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "\n The time taken for launching Main UI from another window is not within the expected limit \n"
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "\n Failed to get the threshold value from config file"
                    else:
                        print "\n Required logs are not present in wpeframework.log"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error occurred while executing the command:{} in DUT,\n Please check the SSH details \n".format(command)
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing org.rdk.RDKShell.1.generateKey method\n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to launch Cobalt plugin \n"
            tdkTestObj.setResultStatus("FAILURE")
        print "\n Exiting from Cobalt \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\nPreconditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
