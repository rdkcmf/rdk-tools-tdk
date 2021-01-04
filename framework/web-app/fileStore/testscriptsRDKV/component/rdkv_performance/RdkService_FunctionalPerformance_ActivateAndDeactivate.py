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
  <version>4</version>
  <name>RdkService_FunctionalPerformance_ActivateAndDeactivate</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to find the time taken for activating and deactivating WebKitPlugin.</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_13</test_case_id>
    <test_objective>The objective of this test is to find the time taken for activating and deactivating the Plugin and check whether the time taken is within the expected range.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. The time in Test Manager should be in sync with UTC </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Threshold value of activating time.
Threshold value of deactivating time,
</input_parameters>
    <automation_approch>1. Check the current status of plugin
2.a) If it is deactivated, store the current time as start_activate time and activate the plugin.
Verify the status, store the current time as start_deactivate and deactivate the plugin.
b) If it is activated store the current time as start_deactivate time and deactivate the plugin.
Verify the status, store the current time as start_activate and activate the plugin.
3. Find the related logs from wpeframework.log and get the timestamp corresponding to activate and deactivate
4. Find the time taken to activate by finding the difference between timestamp from log and start_activate
5.   Find the time taken to deactivate by finding the difference between timestamp from log and start_deactivate.
6. Verify the time values are within the expected range</automation_approch>
    <expected_output>The time taken should be within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RdkService_FunctionalPerformance_ActivateAndDeactivate</test_script>
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
obj.configureTestCase(ip,port,'RdkService_FunctionalPerformance_ActivateAndDeactivate');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    plugin = "WebKitBrowser"
    status_dict = get_plugins_status(obj,[plugin])
    if ssh_param_dict != {}:
        completed = True
        for count in range(0,2):
            if status_dict[plugin] == "deactivated":
                new_status = "activate"
                expected_values = ["activated","resumed"]
            else:
                new_status = "deactivate"
                expected_values = ["deactivated"]
            print "\n Setting {} plugin status to {}".format(plugin,new_status)
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin",plugin)
            tdkTestObj.addParameter("status",new_status)
            if new_status == "activate":
                start_activate = str(datetime.utcnow()).split()[1]
            else:
                start_deactivate = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                #check status
                print "\nChecking current status of plugin \n"
                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                tdkTestObj.addParameter("plugin",plugin)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    status = tdkTestObj.getResultDetails()
                    print "\nCurrent status of {} plugin : {}\n".format(plugin,status)
                    if status in expected_values:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print "\n Successfully set {} plugin to {}\n".format(plugin,status)
                        status_dict[plugin] = status
                        time.sleep(10)
                    else:
                        print "\n [Error] {} plugin not set to {}\n".format(plugin,new_status)
                        tdkTestObj.setResultStatus("FAILURE")
                        completed = False
                        break
                else:
                    print "\n {Error] Unable to get the {} plugin status \n".format(plugin)
                    tdkTestObj.setResultStatus("FAILURE")
                    completed = False
                    break
            else:
                print "\n {Error] Unable to set the {} plugin status \n".format(plugin)
                tdkTestObj.setResultStatus("FAILURE")
                completed = False
                break

        if completed:
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
            #command to get the activated and deactivated logs 
            command = 'cat /opt/logs/wpeframework.log | grep -e "Shutdown: Deactivated" -e "Startup: Activated plugin" |  tail -2'
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",credentials)
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            output = tdkTestObj.getResultDetails()
            if output != "EXCEPTION":
                if len(output.split('\n')) == 4 :
                    if new_status == "deactivate":
                        activated_log = output.split('\n')[1]
                        deactivated_log = output.split('\n')[2]
                    else:
                        activated_log = output.split('\n')[2]
                        deactivated_log = output.split('\n')[1]
                    print '\n'+ activated_log + '\n' +  deactivated_log + '\n' 
                    if 'Activated plugin ['+plugin+']:['+plugin+']' in activated_log and 'Deactivated plugin ['+plugin+']:['+plugin+']' in deactivated_log:
                        conf_file,file_status = getConfigFileName(obj.realpath)
                        activate_config_status,activate_threshold = getDeviceConfigKeyValue(conf_file,"ACTIVATE_TIME_THRESHOLD_VALUE")
                        deactivate_config_status,deactivate_threshold = getDeviceConfigKeyValue(conf_file,"DEACTIVATE_TIME_THRESHOLD_VALUE")
                        if all(status != "" for status in (activate_threshold,deactivate_threshold)):
                            start_activate_in_millisec = getTimeInMilliSec(start_activate)
                            activated_time = getTimeStampFromString(activated_log)
                            activated_time_in_millisec = getTimeInMilliSec(activated_time)
                            print "\n Activate initiated at: " +start_activate + "(UTC)"
                            print "\n Activated at : "+activated_time+ "(UTC)"
                            time_taken_for_activate = activated_time_in_millisec - start_activate_in_millisec
                            print "\n Time taken to Activate {} Plugin: {} (ms)".format(plugin,time_taken_for_activate)
                            print "\n Validate the time taken for activation \n"
                            if 0 < time_taken_for_activate < int(activate_threshold) :
                                activate_status = True
                                print "\n Time taken for activating {} plugin is within the expected range \n".format(plugin)
                            else:
                                activate_status = False
                                print "\n Time taken for activating {} plugin is greater than the expected range \n".format(plugin)
                            start_deactivate_in_millisec = getTimeInMilliSec(start_deactivate)
                            deactivated_time = getTimeStampFromString(deactivated_log)
                            deactivated_time_in_millisec =  getTimeInMilliSec(deactivated_time)
                            print "\n Deactivate initiated at: " + start_deactivate + "(UTC)"
                            print "\n Deactivated at: " + deactivated_time + "(UTC)"
                            time_taken_for_deactivate = deactivated_time_in_millisec - start_deactivate_in_millisec
                            print "\n Time taken to Deactivate {} Plugin: {} (ms) \n".format(plugin,time_taken_for_deactivate)
                            print "\n Validate the time taken for deactivation: \n"
                            if 0 < time_taken_for_deactivate < int(deactivate_threshold) :
                                deactivate_status = True
                                print "\n Time taken for deactivating {} plugin is within the expected range \n".format(plugin)
                            else:
                                deactivate_status = False
                                print "\n Time taken for deactivating {} plugin is greater than the expected range \n".format(plugin)
                            if all(status for status in (activate_status,deactivate_status)):
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "Threshold values are not configured in Device configuration file"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Activate and deactivate is not working"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Logs are not available in wpeframework log"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Exception occured during SSH session, please check the configuration file"
                tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
