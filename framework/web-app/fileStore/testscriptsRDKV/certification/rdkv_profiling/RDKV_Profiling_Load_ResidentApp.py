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
  <name>RDKV_Profiling_Load_ResidentApp</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate profiling data from Grafana tool after loading ResidentApp.</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
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
    <test_case_id>RDKV_PROFILING_03</test_case_id>
    <test_objective>The objective of this test is to validate profiling data from Grafana tool after loading ResidentApp.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Reboot the DUT.
2. Wait for 90 seconds
3. Check the uptime
4. Check the zorder from RDKShell to see ResidenApp is loaded.
5. Validate the profiling data from Grafana tool with the threshold values for the pre-configured process list.
6. Execute the smem tool and collect the log
7. Execute pmap tool for the list of given process and collect the log
8. Check for alerts from Grafana tool.
</automation_approch>
    <expected_output>ResidentApp should be launched successfully and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Load_ResidentApp</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import ast
from StabilityTestUtility import *
import RDKVProfilingVariables
from RDKVProfilingVariables import *
import json
from rdkv_profilinglib import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True)

start_datetime_string = str(datetime.utcnow()).split('.')[0]

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Load_ResidentApp')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','tr69hostif']
    resident_app = "ResidentApp"
    conf_file,result = get_configfile_name(obj)
    rebootwaitTime = 180
    tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
    tdkTestObj.addParameter("waitTime",rebootwaitTime)
    #get the current system time before reboot
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
            if uptime < 300:
                tdkTestObj.setResultStatus("SUCCESS")
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                tdkTestObj.executeTestCase(expectedResult)
                zorder = tdkTestObj.getResultDetails()
                zorder_status = tdkTestObj.getResult()
                if expectedResult in zorder_status :
                    zorder = ast.literal_eval(zorder)["clients"]
                    if resident_app.lower() in zorder:
                        print "\n ResidentApp is launched"
                        if result == "SUCCESS":
                            #Validate system wide profiling data
                            for result,validation_result,system_wide_methods,tdkTestObj in get_systemwidemethods(obj,conf_file):
                                if expectedResult in (result and validation_result):
                                    print "Successfully validated the {}\n".format(system_wide_methods)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "Error while validating the {}\n".format(system_wide_methods)
                                    tdkTestObj.setResultStatus("FAILURE")
                            #Validate process wise profiling data
                            for result,validation_result,process,process_wise_methods_list,tdkTestObj in get_processwisemethods(obj,process_list,conf_file):
                                if expectedResult in (result and validation_result):
                                    print "Successfully validated the {} process {}\n".format(process,process_wise_methods_list)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "Error while validating the {} process {}\n".format(process,process_wise_methods_list)
                                    tdkTestObj.setResultStatus("FAILURE")
                            #smem data collection
                            result,tdkTestObj = get_smemdata(obj,ip,conf_file)
                            if "SUCCESS" in result:
                                print "\nSMEM tool execution success and transferred the log"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\nSMEM tool execution or log transfer failed"
                                tdkTestObj.setResultStatus("FAILURE")
                            #pmap data collection
                            #Automatic process selection to get pmap data will be added in the later releases
                            result,tdkTestObj = get_pmapdata(obj,ip,conf_file,process_list)
                            if "SUCCESS" in result:
                                print "\npmap tool execution success and transferred the log"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\npmap tool execution or log transfer failed"
                                tdkTestObj.setResultStatus("FAILURE")
                            #check for alerts from Grafana tool
                            print "\nCheck for profiling alerts...."
                            tdkTestObj = obj.createTestStep("rdkv_profiling_get_alerts")
                            tdkTestObj.addParameter('tmUrl',obj.url)
                            tdkTestObj.addParameter('resultId',obj.resultId)
                            tdkTestObj.executeTestCase(expectedResult)
                            details = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            validation_result = json.loads(details).get("test_step_status")
                            if expectedResult in (result and validation_result):
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error while getting device config file"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Resident app is not launched properly"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while getting zorder"
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
    obj.unloadModule("rdkv_profiling")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
