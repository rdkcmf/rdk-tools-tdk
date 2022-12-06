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
  <name>RDKV_CERT_AVS_Wifi</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>4</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To test RDK service Wifi api's</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>45</execution_time>
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
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <expected_output></expected_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
import IPChangeDetectionVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_AVS_Wifi');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    conf_file,file_status = getConfigFileName(obj.realpath)
    lightning_app_support_status,lightning_app_support = getDeviceConfigKeyValue(conf_file,"IP_CHANGE_LIGHTNING_APP_SUPPORT")
    config_status = "SUCCESS"
    status = "SUCCESS"
    if lightning_app_support == "":
         print "\n Please configure lightning_app_support key in Device specific configuration file"
         config_status = "FAILURE"
    elif lightning_app_support.upper() == "YES":
         print "Check Pre conditions"
         #No need to revert any values if the pre conditions are already set.
         revert="NO"
         status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
         print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
         if status == "FAILURE":
             set_pre_requisites(obj)
             #Need to revert the values since we are changing plugin status
             revert="YES"
             status,webkit_status,cobalt_status = check_pre_requisites(obj)
         ip_change_app_url = IPChangeDetectionVariables.ip_change_app_url
         user_name = IPChangeDetectionVariables.tm_username
         password = IPChangeDetectionVariables.tm_password
         tm_url = obj.url
         device_name = rdkv_performancelib.deviceName
         #Reading the Device IP Type from the device config file
         conf_file,file_status = getConfigFileName(obj.realpath)
         ip_address_type_status,ip_address_type = getDeviceConfigKeyValue(conf_file,"DEVICE_IP_ADDRESS_TYPE")
         video_test_url = ip_change_app_url+'?tmURL='+obj.url+'&deviceName='+device_name+'&tmUserName='+user_name+'&tmPassword='+password+'&ipAddressType='+ip_address_type
         if any(value == "" for value in (ip_change_app_url,user_name,password,ip_address_type)):
             print "\n Please configure values in IPChangeDetectionVariables and Device specific configuration file \n"
             config_status = "FAILURE"
    if status == "SUCCESS" and config_status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        pre_req_status = "SUCCESS"
        if lightning_app_support.upper() == "YES":
            print "\nGet the URL in WebKitBrowser"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            current_url = tdkTestObj.getResultDetails();
            result = tdkTestObj.getResult()
            if current_url != None and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                time.sleep(10)
                print "Current URL:",current_url
                print "\nSet Lightning video player test app URL"
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.addParameter("value",video_test_url);
                tdkTestObj.executeTestCase(expectedResult);
                time.sleep(30)
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    print "\nValidate if the URL is set successfully or not"
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                    tdkTestObj.executeTestCase(expectedResult);
                    new_url = tdkTestObj.getResultDetails();
                    result = tdkTestObj.getResult()
                    if new_url in video_test_url and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "URL(",new_url,") is set successfully"
                        pre_req_status = "SUCCESS"
                    else:
                        print "Failed to load the URL %s" %(new_url)
                        tdkTestObj.setResultStatus("FAILURE");
                        pre_req_status = "FAILURE"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to set the URL"
                    pre_req_status = "FAILURE"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Unable to get the current URL loaded in webkit"
                pre_req_status = "FAILURE"

        if pre_req_status == "SUCCESS":
            #Prmitive test case which associated to this Script
            tdkTestObj = obj.createTestStep('RdkService_Test');
            tdkTestObj.addParameter("xml_name","Wifi");
            expectedResult = "SUCCESS"
            #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedResult);
            #Get the result of execution
            result = tdkTestObj.getResult();
            print "[TEST EXECUTION RESULT] : %s" %result;
            #Set the result status of execution
            tdkTestObj.setResultStatus(result);

            if lightning_app_support.upper() == "YES":
                #Set the URL back to previous
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
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
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    obj.unloadModule("rdkservices");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

