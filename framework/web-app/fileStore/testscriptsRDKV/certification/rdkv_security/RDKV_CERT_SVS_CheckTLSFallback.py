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
  <version>15</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_SVS_CheckTLSFallback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkvsecurity_executeInTM</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks the TLS Fallback settings</synopsis>
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
    <test_case_id>RDKV_SECURITY_05</test_case_id>
    <test_objective>Checks the TLS Fallback settings</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Sslscan tool should be installed in the TM machine
2. Configure the values supported SSL/TLS protocols (variable $SUPPORTED_SSL_TLS_PROTOCOLS), default SSL/TLS protocols (variable $DEFAULT_SSL_TLS_PROTOCOLS), test URL (variable $TEST_URL)and SSLscan path (variable $SSL_SCAN_PATH) available in fileStore/tdkvRDKServiceConfig/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Execute the sslscan with parameters to list the protocols and fallback settings of the DUT
3. If supported SSL/TLS protocols  configured check whether configured  protocols are enabled
4. Check  if Fallback feature is supported
5. Pass/fail the test based on the enabled/disabled state of Fallback feature</automation_approch>
    <expected_output> If supported SSL/TLS protocol configured, Fallback must be enabled</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_security</test_stub_interface>
    <test_script>RdkvSecurity_CheckTLSFallback</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_securitylib import *;
import rdkv_securitylib;
import re;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_security","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_SVS_CheckTLSFallback');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
result = obj.getLoadModuleResult();

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    configKeyList = ["SSL_SCAN_PATH","SUPPORTED_SSL_TLS_PROTOCOLS","TEST_WEB_APP_URL","DEFAULT_SSL_TLS_PROTOCOLS"]
    configValues = {}
    tdkTestObj = obj.createTestStep('rdkvsecurity_getDeviceConfig')
    #Get each configuration from device config file
    for configKey in configKeyList:
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey",configKey)
        tdkTestObj.executeTestCase(expectedResult)
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configKey != "SUPPORTED_SSL_TLS_PROTOCOLS" and configValues[configKey] != "":
            print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
            tdkTestObj.setResultStatus("SUCCESS")
        elif "FAILURE" not in configValues[configKey] and configKey == "SUPPORTED_SSL_TLS_PROTOCOLS":
            print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "FAILURE: Failed to retrieve %s configuration from device config file" %(configKey)
            if configKey != "SUPPORTED_SSL_TLS_PROTOCOLS" and configValues[configKey] == "":
                print "\n Please configure the %s key in the device config file" %(configKey)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
            break
    if "FAILURE" != result:
         tdkTestObj = obj.createTestStep('rdkvsecurity_executeInTM');
         command = configValues["SSL_SCAN_PATH"]+"/sslscan "+configValues["TEST_WEB_APP_URL"]
         tdkTestObj.addParameter("command", command);
         tdkTestObj.executeTestCase(expectedResult);
         Result = tdkTestObj.getResultDetails()
         if "FAILURE" not in Result:
             tdkTestObj.setResultStatus("SUCCESS")
             ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
             if not configValues["SUPPORTED_SSL_TLS_PROTOCOLS"]:
                  defaultProtocols = configValues["DEFAULT_SSL_TLS_PROTOCOLS"].split(",")
                  print "No supported protocols configured"
                  print "Checking any default protocols are enabled......"
                  print "[DEFAULT_PROTOCOLS: %s]" %(defaultProtocols)
                  tdkTestObj.setResultStatus("SUCCESS")
                  enabled=0;
                  for protocol in defaultProtocols:
                      for line in Result.splitlines():
                          if protocol in line:
                              if "enabled" in line:
                                  print "FAILURE: %s - Enabled but configured as disabled" %(protocol)
                                  tdkTestObj.setResultStatus("FAILURE");
                                  enabled = 1;
                                  break;
                              elif "disabled" in line:
                                  print "SUCCESS: %s - disabled" %(protocol)
                                  tdkTestObj.setResultStatus("SUCCESS");
                                  break;
                  if enabled == 0:
                      print "All the default protocols are disabled"
                      tdkTestObj.setResultStatus("SUCCESS");
                  elif enabled == 1:
                      print "Some of the protocols are enabled but configured as disabled"
                      print "Checking TLS Fallback settings....."
                      for line in  Result.splitlines():
                        fallbackfound = 0;
                        if "TLS Fallback SCSV" in line and "support" in line:
                            fallbackfound = 1;
                            line = ansi_escape.sub('', line)
                            print "[RESPONSE FROM DEVICE]: %s" %(line)
                            print "SUCCESS: TLS Fallback SCSV guard is enabled,Fallback will not happen"
                            tdkTestObj.setResultStatus("SUCCESS");
                            break;
                        elif "TLS Fallback SCSV" in line and "not support" in line:
                            fallbackfound = 1;
                            line = ansi_escape.sub('', line)
                            print "[RESPONSE FROM DEVICE]: %s" %(line)
                            print "FAILURE: TLS Fallback SCSV guard is not enabled Fallback might happen"
                            tdkTestObj.setResultStatus("FAILURE");
                            break;
                      if fallbackfound == 0:
                          print "FAILURE: TLS Fallback Settings not found"
                          tdkTestObj.setResultStatus("FAILURE");

             else:
                 supportedProtocols = configValues["SUPPORTED_SSL_TLS_PROTOCOLS"].split(",")
                 print "[CONFIGURED SUPPORTED PROTOCOLS: %s]"  %(supportedProtocols)
                 print "Checking configured protocols are enabled or not......"
                 disabled = 0;enabled = 0;
                 for protocol in supportedProtocols:
                      for line in Result.splitlines():
                          if protocol in line:
                              if "enabled" in line:
                                  print "SUCCESS: %s - Enabled" %(protocol)
                                  enabled = 1
                                  tdkTestObj.setResultStatus("SUCCESS");
                                  break;
                              elif "disabled" in line:
                                  print "FAILURE: %s - disabled but configured as enabled" %(protocol)
                                  tdkTestObj.setResultStatus("FAILURE");
                                  disabled = 1
                                  break;
                 if disabled == 1 and enabled == 0:
                     tdkTestObj.setResultStatus("FAILURE");
                     print "FAILURE: Some of the protocols are disabled but configured as enabled"
                 if enabled == 1:
                     print "Checking TLS Fallback settings....."
                     for line in  Result.splitlines():
                         fallbackfound = 0;
                         if "TLS Fallback SCSV" in line and "support" in line:
                             fallbackfound = 1;
                             line = ansi_escape.sub('', line)
                             print "[RESPONSE FROM DEVICE]: %s" %(line)
                             print "SUCCESS: TLS Fallback SCSV guard is enabled,Fallback will not happen"
                             tdkTestObj.setResultStatus("SUCCESS");
                             break;
                         elif "TLS Fallback SCSV" in line and "not support" in line:
                             fallbackfound = 1;
                             line = ansi_escape.sub('', line)
                             print "[RESPONSE FROM DEVICE]: %s" %(line)
                             print "FAILURE: TLS Fallback SCSV guard is not enabled Fallback might happen"
                             tdkTestObj.setResultStatus("FAILURE");
                             break;
                     if fallbackfound == 0:
                         print "FAILURE: TLS Fallback Settings not found"
                         tdkTestObj.setResultStatus("FAILURE");
         else:
             print "FAILURE: SSlScan failed"
             tdkTestObj.setResultStatus("FAILURE");
    else:
        print "FAILURE: Failed to retrieve configuration values from device config file"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_security");

else:
    obj.setLoadModuleStatus("FAILURE");
    print "FAILURE: Failed to load module"

