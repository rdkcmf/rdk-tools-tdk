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
  <name>RDKV_Profiling_Load_LightningApp</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate profiling data from Grafana tool after launching a Lightning App.</synopsis>
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
    <test_case_id>RDKV_PROFILING_02</test_case_id>
    <test_objective>The objective of this test is to validate profiling data from Grafana tool after launching a Lightning App.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running.
2. User should configure the input parameters in PerformanceTestVariables.py file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>lightning_app_instance: string
lightning_app_url : string</input_parameters>
    <automation_approch>1. Launch LightningApp plugin using RDKShell.
2. Set the URL of Lightning App.
3. Check whether application is launched.
4. Validate the profiling data from Grafana tool based on threshold values.
5. Execute the smem tool and collect the log
6. Check for alerts from Grafana tool
7. Revert the URL and plugin status.</automation_approch>
    <expected_output>Lightning App should be launched and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Load_LightningApp</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
import RDKVProfilingVariables
from RDKVProfilingVariables import *
import json
from rdkv_profilinglib import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True);

start_datetime_string = str(datetime.utcnow()).split('.')[0]

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Load_LightningApp');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    status = "SUCCESS"
    url_method = lightning_app_instance + '.1.url'
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    #WebKitBrowser will be changed to LightningApp in the upcoming releases.
    plugins_list = [lightning_app_instance,"Cobalt"]
    plugin_status_needed = {lightning_app_instance:"resumed","Cobalt":"deactivated"}
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','tr69hostif']
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    conf_file,result = getConfigFileName(obj.realpath)
    time.sleep(30)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        #Validate system wide profiling data before loading lightning app
        end_datetime_string = str(datetime.utcnow()).split('.')[0]
        print "\n Validating system wide profiling mettrics from grafana before loading lightning app\n"
        for result,validation_result,system_wide_methods,tdkTestObj in get_systemwide_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string):
            if expectedResult in (result and validation_result):
                print "Successfully validated the {}\n".format(system_wide_methods)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Error while validating the {}\n".format(system_wide_methods)
                tdkTestObj.setResultStatus("FAILURE")
        #Validate process wise profiling data before loading lightning app
        print "\n Validating process wise profiling metrics from grafana before loading lightning app \n"
        for result,validation_result,process_wise_methods_list,tdkTestObj in get_processwise_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string,process_list):
            if expectedResult in (result and validation_result):
                print "Successfully validated the {}\n".format(process_wise_methods_list)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Error while validating the {}\n".format(process_wise_methods_list)
                tdkTestObj.setResultStatus("FAILURE")
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in ",lightning_app_instance
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",url_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            time.sleep(10)
            print "\nCurrent URL:",current_url
            print "\nSet Lightning Application URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",url_method);
            tdkTestObj.addParameter("value",lightning_app_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",url_method);
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult();
                if new_url in lightning_app_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "\n URL(",new_url,") is set successfully \n"
                    time.sleep(60)
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
                    #Set the URL back to previous
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method",url_method);
                    tdkTestObj.addParameter("value",current_url);
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if result == "SUCCESS":
                        print "URL is reverted successfully \n"
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print "Failed to revert the URL"
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "Failed to load the URL, current URL: %s" %(new_url)
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "Failed to set the URL"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in WebKitBrowser"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_profiling");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
