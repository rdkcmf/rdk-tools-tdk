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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_ReInitialize_AudioPorts</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_ReInitializeAudioPort</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Reinitialize all supported audioPorts</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_202</test_case_id>
    <test_objective>Reinitialize all supported audioPorts</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>List&lt;AudioOutputPort&gt; getPorts();reInitializeAudioOutputPort()</api_or_interface_used>
    <input_parameters>audioPort Instance</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the list of supported audio ports.
3.Device_Settings_Agent will reinitialize all supported audioPorts.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <expected_output>Reinitialization of all supported ports must be successfull</expected_output>
    <priority>High</priority>
    <test_stub_interface></test_stub_interface>
    <test_script>DS_ReInitialize_AudioPorts</test_script>
    <skipped>No</skipped>
    <release_version>M91</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_ReInitialize_AudioPorts');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #calling Device Settings - initialize API
    tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
    expectedresult="SUCCESS"
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    print "[DS Initialize RESULT] : %s" %actualresult;

    #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");

        #calling Device Settings - Get List od Auido Ports.
        tdkTestObj = obj.createTestStep('DS_AOPCONFIG_getPorts');

        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails()
        print "[DS_AOPCONFIG_getPorts RESULT] : %s" %actualresult;
        print "[DS_AOPCONFIG_getPorts DETAILS] : %s" %details;

        #Check for SUCCESS/FAILURE return value of DS_AOPCONFIG_getPorts
        if expectedresult in actualresult:
            portNameList = details.split(',')
            tdkTestObj.setResultStatus("SUCCESS");
            print "SUCCESS: Get DS_AOPCONFIG_getPorts";
            for portName in portNameList:
                 tdkTestObj = obj.createTestStep('DS_ReInitializeAudioPort')
                 tdkTestObj.addParameter("port_name",portName);
                 tdkTestObj.executeTestCase(expectedresult);
                 actualresult = tdkTestObj.getResult();
                 details = tdkTestObj.getResultDetails()
                 if expectedresult in actualresult:
                     tdkTestObj.setResultStatus("SUCCESS");
                     print "ReInitializeAudioPort SUCCESS";
                     print details
                 else:
                     tdkTestObj.setResultStatus("FAILURE");
                     print "ReInitializeAudioPort FAILURE";
                     print details

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "FAILURE: Get DS_AOPCONFIG_getPorts"

        #calling DS_ManagerDeInitialize to DeInitialize API
        tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Deinitalize RESULT] : %s" %actualresult;

        #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    #Unload the deviceSettings module
    obj.unloadModule("devicesettings");
else:
    print"Load module failed";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
