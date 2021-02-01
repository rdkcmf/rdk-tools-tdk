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
  <name>RDKService_PremiumApp_Cobalt_TimeTo_SuspendResume</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The script is to find the time taken to suspend and resume Cobalt</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_22</test_case_id>
    <test_objective>The script is to find the time taken to suspend and resume Cobalt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. The time in Test Manager should be in sync with UTC </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Threshold value of suspending time.
Threshold value of resuming time,</input_parameters>
    <automation_approch>1. Resume the Cobalt plugin.
2. Store the current time in start_resume variable and suspend the plugin using RDKShell.
3. Verify the status.
4. Store the current time in start_resume variable and resume the plugin using RDKShell.
5. Verify the status.
6. Find the corresponding logs and get the timestamps for suspending and resuming the pluginfrom wpeframework log.
7. Calculate the time taken to suspend by finding the difference between start_suspend and timestamp
8. Calculate the time taken to resume by  finding the difference between start_resume and timestamp
9. Verify the time values are within the expected range</automation_approch>
    <expected_output>The time taken should be within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKService_PremiumApp_Cobalt_TimeTo_SuspendResume</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from rdkv_performancelib import *
from datetime import datetime
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKService_PremiumApp_Cobalt_TimeTo_SuspendResume');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"Cobalt":"resumed"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict == plugin_status_needed:
            status = "SUCCESS"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    result = tdkTestObj.getResult()
    if status == "SUCCESS" and ssh_param_dict != {} and expectedResult in result:
        print "\nPre conditions for the test are set successfully"
        time.sleep(10)
        suspend_status,start_suspend = suspend_plugin(obj,"Cobalt")
        if suspend_status == expectedResult:
            time.sleep(5)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            cobalt_status = tdkTestObj.getResultDetails()
            if cobalt_status == 'suspended' and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(20)
                print "\nCobalt Suspended Successfully\n"
                resume_status,start_resume = launch_plugin(obj,"Cobalt")
                if resume_status == expectedResult:
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin","Cobalt")
                    tdkTestObj.executeTestCase(expectedResult)
                    cobalt_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if cobalt_status == 'resumed' and expectedResult in result:
                        print "\nCobalt Resumed Successfully\n"
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(20)
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
                        #command to get the event logs
                        command = 'cat /opt/logs/wpeframework.log | grep -e RDKShell.*onSuspended.*Cobalt -e RDKShell.*onLaunched.*Cobalt | tail -4'
                        suspended_event = 'RDKShell onSuspended event received for Cobalt'
                        resumed_event = 'RDKShell onLaunched event received for Cobalt'
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",credentials)
                        tdkTestObj.addParameter("command",command)
                        tdkTestObj.executeTestCase(expectedResult)
                        output = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if output != "EXCEPTION" and expectedResult in result:
                            if len(output.split('\n')) == 6 :
                                suspended_log = output.split('\n')[1]
                                resumed_log = output.split('\n')[3]
                                print suspended_log + '\n' +  resumed_log + '\n'
                                if suspended_event in suspended_log and resumed_event in resumed_log:
                                    conf_file,file_status = getConfigFileName(obj.realpath)
                                    suspend_config_status,suspend_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_SUSPEND_TIME_THRESHOLD_VALUE")
                                    resume_config_status,resume_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_RESUME_TIME_THRESHOLD_VALUE")
                                    if all(status != "" for status in (suspend_threshold,resume_threshold)):
                                        start_suspend_in_millisec = getTimeInMilliSec(start_suspend)
                                        suspended_time = getTimeStampFromString(suspended_log)
                                        suspended_time_in_millisec = getTimeInMilliSec(suspended_time)
                                        print "\n Suspended initiated at: " +start_suspend + "(UTC)"
                                        print "\n Suspended at : "+suspended_time+ "(UTC)"
                                        time_taken_for_suspend = suspended_time_in_millisec - start_suspend_in_millisec
                                        print "\n Time taken to Suspend Cobalt Plugin: " + str(time_taken_for_suspend) + "(ms)"
                                        print "\n Validate the time taken for suspending the plugin \n"
                                        if 0 < time_taken_for_suspend < int(suspend_threshold) :
                                            suspend_status = True
                                            print "\n Time taken for suspending Cobalt plugin is within the expected range \n"
                                        else:
                                            suspend_status = False
                                            print "\n Time taken for suspending Cobalt plugin not within the expected range \n"
                                        start_resume_in_millisec = getTimeInMilliSec(start_resume)
                                        resumed_time = getTimeStampFromString(resumed_log)
                                        resumed_time_in_millisec =  getTimeInMilliSec(resumed_time)
                                        print "\n Resume initiated at: " + start_resume + "(UTC)"
                                        print "\n Resumed at: " + resumed_time + "(UTC)"
                                        time_taken_for_resume = resumed_time_in_millisec - start_resume_in_millisec
                                        print "\n Time taken to Resume Cobalt Plugin: " + str(time_taken_for_resume) + "(ms)"
                                        print "\n Validate the time taken for resuming the plugin \n"
                                        if 0 < time_taken_for_resume < int(resume_threshold) :
                                            resume_status = True
                                            print "\n Time taken for resuming Cobalt plugin is within the expected range \n"
                                        else:
                                            resume_status = False
                                            print "\n Time taken for resuming Cobalt plugin is not within the expected range \n"
                                        if all(status for status in (suspend_status,resume_status)):
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Threshold values are not configured in Device configuration file \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error occured during suspending and resuming Cobalt \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Unable to get the Suspend and Resume details from wpeframework log"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\nError occurred while executing the command:{} in DUT, Please check the SSH details\n ".format(command)
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Cobalt is not in Resumed state, current Cobalt Status: ",cobalt_status
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to set Cobalt plugin to resumed state \n"
            else:
                print "\n Cobalt is not in Suspended state, current Cobalt Status: ",cobalt_status
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to set Cobalt plugin to suspended state"
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

