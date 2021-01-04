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
  <version>2</version>
  <name>RdkService_FunctionalPerformance_SuspendAndResume</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The script is to find the time taken to suspend and resume WebKitBrowser.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_14</test_case_id>
    <test_objective>The script is to find the time taken to suspend and resume WebKitBrowser.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. The time in Test Manager should be in sync with UTC </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Threshold value of suspending time.
Threshold value of resuming time,</input_parameters>
    <automation_approch>1. Resume the WebKitBrowser plugin.
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
    <test_script>RdkService_FunctionalPerformance_SuspendAndResume</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
obj.configureTestCase(ip,port,'RdkService_FunctionalPerformance_SuspendAndResume');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed"}
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
    if status == "SUCCESS" and ssh_param_dict != {}:
        print "\nPre conditions for the test are set successfully"
        print "\nSuspend the WebkitBrowser plugin :\n"
        params = '{"callsign":"WebKitBrowser"}'
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.suspend")
        tdkTestObj.addParameter("value",params)
        start_suspend = str(datetime.utcnow()).split()[1]
        tdkTestObj.executeTestCase(expectedResult)
        time.sleep(5)
        result = tdkTestObj.getResult()
        if result == expectedResult:
            tdkTestObj.setResultStatus("SUCCESS")
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","WebKitBrowser")
            tdkTestObj.executeTestCase(expectedResult)
            webkit_status = tdkTestObj.getResultDetails()
            if webkit_status == 'suspended':
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                print "\nWebKitbrowser Suspended Successfully\n"
                print "\nResume the WebkitBrowser plugin\n"
                params = '{"callsign": "WebKitBrowser", "type":"", "uri":"", "x":0, "y":0, "w":1920, "h":1080}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
                tdkTestObj.addParameter("value",params)
                start_resume = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                time.sleep(5)
                result = tdkTestObj.getResult()
                if result == expectedResult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin","WebKitBrowser")
                    tdkTestObj.executeTestCase(expectedResult)
                    webkit_status = tdkTestObj.getResultDetails()
                    if webkit_status == 'resumed':
                        print "\nWebKitbrowser Resumed Successfully\n"
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(10)
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
                        #command to get the state change related logs
                        command = 'cat /opt/logs/wpeframework.log | grep -inr WebKitBrowser.*Information.*StateChange | tail -2'
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",credentials)
                        tdkTestObj.addParameter("command",command)
                        tdkTestObj.executeTestCase(expectedResult)
                        output = tdkTestObj.getResultDetails()
                        if output != "EXCEPTION":
                            if len(output.split('\n')) == 4 :
                                suspended_log = output.split('\n')[1]
                                resumed_log = output.split('\n')[2]
                                print suspended_log + '\n' +  resumed_log + '\n'
                                if '"State": 1' in suspended_log and '"State": 2' in resumed_log:
                                    conf_file,file_status = getConfigFileName(obj.realpath)
                                    suspend_config_status,suspend_threshold = getDeviceConfigKeyValue(conf_file,"SUSPEND_TIME_THRESHOLD_VALUE")
                                    resume_config_status,resume_threshold = getDeviceConfigKeyValue(conf_file,"RESUME_TIME_THRESHOLD_VALUE")
                                    if all(status != "" for status in (suspend_threshold,resume_threshold)):
                                        start_suspend_in_millisec = getTimeInMilliSec(start_suspend)
                                        suspended_time = getTimeStampFromString(suspended_log)
                                        suspended_time_in_millisec = getTimeInMilliSec(suspended_time)
                                        print "\n Suspended initiated at: " +start_suspend + "(UTC)"
                                        print "\n Suspended at : "+suspended_time+ "(UTC)"
                                        time_taken_for_suspend = suspended_time_in_millisec - start_suspend_in_millisec
                                        print "\n Time taken to Suspend WebKitBrowser Plugin: " + str(time_taken_for_suspend) + "(ms)"
                                        print "\n Validate the time taken for suspending the plugin \n"
                                        if 0 < time_taken_for_suspend < int(suspend_threshold) :
                                            suspend_status = True
                                            print "\n Time taken for suspending WebKitBrowser plugin is within the expected range \n"
                                        else:
                                            suspend_status = False
                                            print "\n Time taken for suspending WebKitBrowser plugin is greater than the expected range \n"
                                        start_resume_in_millisec = getTimeInMilliSec(start_resume)
                                        resumed_time = getTimeStampFromString(resumed_log)
                                        resumed_time_in_millisec =  getTimeInMilliSec(resumed_time)
                                        print "\n Resume initiated at: " + start_resume + "(UTC)"
                                        print "\n Resumed at: " + resumed_time + "(UTC)"
                                        time_taken_for_resume = resumed_time_in_millisec - start_resume_in_millisec
                                        print "\n Time taken to Resume WebKitBrowser Plugin: " + str(time_taken_for_resume) + "(ms)"
                                        print "\n Validate the time taken for resuming the plugin \n"
                                        if 0 < time_taken_for_resume < int(resume_threshold) :
                                            resume_status = True
                                            print "\n Time taken for resuming WebKitBrowser plugin is within the expected range \n"
                                        else:
                                            resume_status = False
                                            print "\n Time taken for resuming WebKitBrowser plugin is greater than the expected range \n"
                                        if all(status for status in (suspend_status,resume_status)):
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "Threshold values are not configured in Device configuration file"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "Error occured during suspending and resuming WebKitBrowser"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Unable to get the Suspend and Resume details from wpeframework log"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\nError occurred while executing the command:{} in DUT,\n Please check the SSH details\n ".format(command)
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "WebKitBrowser is not in Resumed state, current WebKitBrowser Status: ",webkit_status
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "Unable to set WebKitBrowser plugin to resumed state"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "WebKitBrowser is not in Suspended state, current WebKitBrowser Status: ",webkit_status
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Unable to set WebKitBrowser plugin to suspended state"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
