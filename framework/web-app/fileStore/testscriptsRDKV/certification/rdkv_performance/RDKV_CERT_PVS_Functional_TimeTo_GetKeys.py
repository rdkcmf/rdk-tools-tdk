##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_TimeTo_GetKeys</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the time taken to get Keys from RDK Shell</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_108</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to get Keys from RDK Shell</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Enable WebKitInstance plugin.
2. Set URL for keytest in WebKitInstance.
3. In a loop of minimum 15 iterations send a key using generatekey method of RDKShell to the system.
4. Validate the key press using webinspect console logs.
5. Validate the time taken to get keys from RDK Shell.
6. Revert plugins status after completing the test</automation_approch>
    <expected_output>The time taken to get keys from RDK Shell must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_GetKeys</test_script>
    <skipped>No</skipped>
    <release_version>M98</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from web_socket_util import *
from rdkv_performancelib import *
import PerformanceTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_GetKeys');
#Execution summary variable
Summ_list=[]

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    key_test_url = obj.url+'/fileStore/lightning-apps/KeyStressTest.html'
    webkit_console_socket = None
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    webkit_instance = PerformanceTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
    if webkit_instance in "WebKitBrowser":
        webinspect_port = PerformanceTestVariables.webinspect_port
    elif webkit_instance in "LightningApp":
        webinspect_port = PerformanceTestVariables.lightning_app_webinspect_port
    else:
        webinspect_port = PerformanceTestVariables.html_app_webinspect_port
    plugins_list = [webkit_instance,"Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {webkit_instance:"resumed","Cobalt":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS" :
        webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
        print "\nPre conditions for the test are set successfully"
        print "\nGet the URL "
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and  expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet Key test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",key_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            time.sleep(10)
            result = tdkTestObj.getResult();
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    new_url = tdkTestObj.getResultDetails();
                    if new_url == key_test_url:
                        tdkTestObj.setResultStatus("SUCCESS")
                        end_get_key_time = ""
                        total_time = 0
                        count = 0
                        for i in range(0,15):
                            params = '{"keys":[ {"keyCode": 50,"modifiers": [],"delay":1.0,"callsign":'+webkit_instance+',"client":'+webkit_instance+'}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            start_get_key_time = str(datetime.utcnow()).split()[1]
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(10)
                                if (len(webkit_console_socket.getEventsBuffer())== 0):
                                    print "\n No events occurred corresponding to key press\n"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    event_log = webkit_console_socket.getEventsBuffer().pop(0)
                                    print "\n key codes are received successfully \n"
                                    end_get_key_time = event_log.split('$$$')[0]
                                    print "end time",end_get_key_time
                                    start_get_key_time_in_millisec = getTimeInMilliSec(start_get_key_time)
                                    end_get_key_time_in_millisec = getTimeInMilliSec(end_get_key_time)
                                    time_taken = end_get_key_time_in_millisec - start_get_key_time_in_millisec
                                    print "time taken",time_taken
                                    total_time = total_time + time_taken
                                    count = count + 1
                            else:
                                print "\nError while executing generate key method\n"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        if end_get_key_time:
                            conf_file,file_status = getConfigFileName(obj.realpath)
                            config_status,get_key_threshold = getDeviceConfigKeyValue(conf_file,"GET_KEY_THRESHOLD_VALUE")
                            Summ_list.append('GET_KEY_THRESHOLD_VALUE :{}ms'.format(get_key_threshold))
                            if count == 15:
                                avg_get_key_time = total_time/15
                            else:
                                print "\n 15 Iterations for receiving the keys is not successful"
                                tdkTestObj.setResultStatus("FAILURE")
                            print "\n Time taken to get keys : {}(ms)".format(avg_get_key_time)
                            Summ_list.append('Time taken to get keys :{}ms'.format(avg_get_key_time))
                            print "\n Threshold value to get keys: {}(ms)".format(get_key_threshold)
                            print "\n Validate the time:"
                            if avg_get_key_time  < get_key_threshold:
                                print "\n Time taken for getting the keys is within the expected range \n"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Time taken for getting keys is not within the expected range \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "All keys not received successfully"
                            tdkTestObj.setResultStatus("FAILURE")
                        #Set the URL back to previous
                        tdkTestObj = obj.createTestStep('rdkservice_setValue');
                        tdkTestObj.addParameter("method",set_method);
                        tdkTestObj.addParameter("value",current_url);
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult();
                        if result == "SUCCESS":
                            print "URL is reverted successfully"
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            print "Failed to revert the URL"
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        print "Unable to launch the URL"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print "Unable to get the URL after setting it"
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "Failed to set the URL"
        else:
            print "Unable to get the current URL in webkit"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
                                                         



