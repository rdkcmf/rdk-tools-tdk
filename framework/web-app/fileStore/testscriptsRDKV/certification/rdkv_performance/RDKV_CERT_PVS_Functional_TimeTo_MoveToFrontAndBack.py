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
  <name>RDKV_CERT_PVS_Functional_TimeTo_MoveToFrontAndBack</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to move an app to front and back.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_46</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to move an app to front and back.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.Wpeframework process should be up and running in the device.
2. Time in test manager and DUT must be in sync with UTC</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch Cobalt plugin
2. Check the zorder 
3. Based on the zorder of Cobalt decide on moveToFront or moveToBack and perform the operation
4. Check the logs corresponding to the operation and parse the time stamp
5. Same steps to be followed for both operation
6. Validate the time taken for operations using time stamp</automation_approch>
    <expected_output>The time taken to moveToFront and moveToBack must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_MoveToFrontAndBack</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import ast
from datetime import datetime
from rdkv_performancelib import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_MoveToFrontAndBack');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    start_time_dict = {}
    event_time_dict = {}
    method = ""
    plugin = "Cobalt"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    conf_file,file_status = getConfigFileName(obj.realpath)
    moveToFront_config_status,moveToFront_threshold = getDeviceConfigKeyValue(conf_file,"MOVETO_FRONT_THRESHOLD_VALUE")
    moveToBack_config_status,moveToBack_threshold = getDeviceConfigKeyValue(conf_file,"MOVETO_BACK_THRESHOLD_VALUE")
    offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    revert = "NO"
    status = "SUCCESS"
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    if expectedResult == (result and status) and ssh_param_dict != {} and all(value != "" for value in (moveToFront_threshold,moveToBack_threshold,offset)):
        validation_dict = {}
        tdkTestObj.setResultStatus("SUCCESS")
        cobalt_launch_status,cobalt_launch_start_time = launch_plugin(obj,plugin)
        time.sleep(20)
        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
        tdkTestObj.addParameter("plugin",plugin)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        status = tdkTestObj.getResultDetails()
        if expectedResult == (cobalt_launch_status and result) and status in "resumed":
            tdkTestObj.setResultStatus("SUCCESS")
            for count in range(0,2):
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                tdkTestObj.executeTestCase(expectedResult)
                zorder = tdkTestObj.getResultDetails()
                zorder_status = tdkTestObj.getResult()
                if expectedResult in zorder_status :
                    zorder = ast.literal_eval(zorder)["clients"]
                    print "zorder: ",zorder
                    if  plugin.lower() in [element.lower() for element in zorder]:
                        tdkTestObj.setResultStatus("SUCCESS")
                        if zorder[0].lower() == plugin.lower():
                            method = "moveToBack"
                        else:
                            method = "moveToFront"
                        validation_dict["moveToFront"] = int(moveToFront_threshold)
                        validation_dict["moveToBack"] = int(moveToBack_threshold)
                        param_val = '{"client": "'+plugin+'"}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1."+method)
                        tdkTestObj.addParameter("value",param_val)
                        start_time_dict[method] = str(datetime.utcnow()).split()[1]
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            time.sleep(10)
                            command = 'cat /opt/logs/wpeframework.log | grep -inr '+method+'Wrapper |  tail -1'
                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                            tdkTestObj.addParameter("command",command)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            output = tdkTestObj.getResultDetails()
                            if output != "EXCEPTION" and expectedResult in result and len(output.split('\n')) > 2:
                                required_log = output.split('\n')[1]
                                if  "response" in required_log and json.loads(required_log.split("=")[-1]).get("success"):
                                    print "\n Successfully done {} of {}, logs:{} \n".format(method,plugin,required_log)
                                    print "\n {} started at: {} UTC".format(method,start_time_dict[method])
                                    start_time_dict[method] = int(getTimeInMilliSec(start_time_dict[method]))
                                    event_time = getTimeStampFromString(required_log)
                                    print "\n {} happened at: {} UTC".format(method,event_time)
                                    event_time_dict[method] = int(getTimeInMilliSec(event_time))
                                    time_taken = event_time_dict[method] -  start_time_dict[method]
                                    print "\n Time taken for {}: {}(ms) ".format(method,time_taken)
                                    if 0 < time_taken < ( validation_dict[method] + int(offset)):
                                        print "\n Time taken for {} is within the expected range".format(method)
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n  Time taken for {} is not within the expected range".format(method)
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n The {} method is not executed successfully"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print "\n Error in command execution in DUT"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Error while executing {} ".format(method)
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n {} plugin is not present in zorder list".format(plugin)
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Error while getting zorder"
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while set and get {} plugin status".format(plugin)
            tdkTestObj.setResultStatus("FAILURE")
        print "\n Exiting from Cobalt \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin",plugin)
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Unable to deactivate {}".format(plugin)
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        tdkTestObj.setResultStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
