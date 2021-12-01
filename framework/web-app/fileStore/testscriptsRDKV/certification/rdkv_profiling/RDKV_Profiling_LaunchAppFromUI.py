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
  <name>RDKV_Profiling_LaunchAppFromUI</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch an application from app store and validate the profiling metrics after that.</synopsis>
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
    <test_case_id>RDKV_PROFILING_09</test_case_id>
    <test_objective>The objective of this test is to launch an application from app store and validate the profiling metrics after that.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>app_launch_key_sequence: List of strings
post_app_launch_key_sequence: List of strings</input_parameters>
    <automation_approch>1. Launch vimeo application from app store by keypress using generateKey method of RDKShell plugin
2. Validate the profiling data from Grafana tool with the threshold values for the pre-configured process list.
3. Execute the smem tool and collect the log
4. Execute pmap tool for the list of given process and collect the log
5. Check for alerts from Grafana tool
6. Close the application by pressing home button</automation_approch>
    <expected_output>Profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_LaunchAppFromUI</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import ast
from rdkv_performancelib import *
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
obj.configureTestCase(ip,port,'RDKV_Profiling_LaunchAppFromUI')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    resident_app = "ResidentApp"
    is_front = False
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','tr69hostif']
    conf_file,result = get_configfile_name(obj)
    time.sleep(30)
    #Validate system wide profiling data before launching app from UI
    end_datetime_string = str(datetime.utcnow()).split('.')[0]
    print "\n Validating system wide profiling mettrics from grafana before launching app from UI\n"
    for result,validation_result,system_wide_methods,tdkTestObj in get_systemwide_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string):
        if expectedResult in (result and validation_result):
            print "Successfully validated the {}\n".format(system_wide_methods)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Error while validating the {}\n".format(system_wide_methods)
            tdkTestObj.setResultStatus("FAILURE")
    #Validate process wise profiling data before launching app from UI
    print "\n Validating process wise profiling metrics from grafana before launching app from UI\n"
    for result,validation_result,process_wise_methods_list,tdkTestObj in get_processwise_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string,process_list):
        if expectedResult in (result and validation_result):
            print "Successfully validated the {}\n".format(process_wise_methods_list)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Error while validating the {}\n".format(process_wise_methods_list)
            tdkTestObj.setResultStatus("FAILURE")
    #Check zorder to check ResidentApp is in the front
    tdkTestObj = obj.createTestStep('rdkservice_getValue')
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
    tdkTestObj.executeTestCase(expectedResult)
    zorder = tdkTestObj.getResultDetails()
    zorder_status = tdkTestObj.getResult()
    if expectedResult in zorder_status :
        tdkTestObj.setResultStatus("SUCCESS")
        zorder = ast.literal_eval(zorder)["clients"]
        if resident_app.lower() in zorder and zorder[0].lower() == resident_app.lower():
            is_front = True
            print "\n ResidentApp is in front"
        elif resident_app.lower() in zorder and zorder[0].lower() != resident_app.lower():
            param_val = '{"client": "'+resident_app+'"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
            tdkTestObj.addParameter("value",param_val)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                #Check zorder to check ResidentApp is in the front
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                tdkTestObj.executeTestCase(expectedResult)
                zorder = tdkTestObj.getResultDetails()
                zorder_status = tdkTestObj.getResult()
                if expectedResult in zorder_status :
                    zorder = ast.literal_eval(zorder)["clients"]
                    if zorder[0].lower() == resident_app.lower():
                        print "\n Successfully moved ResidentApp to front"
                        is_front = True
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "\n Unable to move ResidentApp to front"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while getting the zorder"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing moveToFront method"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n ResidentApp is not present in zorder"
            tdkTestObj.setResultStatus("FAILURE")
        if is_front:
            #Set focus to ResidentApp
            print "\n Set focus to ResidentApp"
            client = '{"client": "ResidentApp"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.setFocus")
            tdkTestObj.addParameter("value",client)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                #Navigate in ResidentApp UI
                for key in app_launch_key_sequence:
                    params = '{"keys":[ {"keyCode": '+str(navigation_key_dictionary[key])+',"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        print "Pressed {} key".format(key)
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(5)
                    else:
                        print "\n Error while pressing {} key".format(key)
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Successfully completed navigations in ResidentApp UI"
                    time.sleep(60)
                    print "\n Validate data from Grafana"
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
                #Close the Application
                home_key_params = '{"keys":[ {"keyCode": 36,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",home_key_params)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    print "\n Pressed home button"
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(10)
                    #Post condition
                    for key in post_app_launch_key_sequence:
                        params = '{"keys":[ {"keyCode": '+str(navigation_key_dictionary[key])+',"modifiers": [],"delay":1.0}]}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            print "\n Pressed {} key".format(key)
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(5)
                        else:
                            print "\n Error while pressing {} key".format(key)
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                else:
                    print "\n Error while pressing home button"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while setting focus to ResidentApp"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to move ResidentApp to front"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Error while getting zorder"
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_profiling")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
