##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>HdmicecHal_Tx_No_HDMI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>HdmicecHal_Tx</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to transmit CEC frame from a setup with no TV connection or non CEC TV and check whether packets are getting transmitted properly and not acknowledged</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_HdmicecHal_13</test_case_id>
    <test_objective>Test Script to transmit CEC frame from a setup with no TV connection or non CEC TV and check whether packets are getting transmitted properly and not acknowledged</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG,XI3,XI6,Video_Accelerator</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. Required a setup without TV connection or setup with non CEC enabled TV 
3.  HdmiCecOpen should open a CEC driver instance successfully and iarmbus event should be obtained from device ready call back.
</pre_requisite>
    <api_or_interface_used>int HdmiCecOpen(int *handle)
int HdmiCecClose(int handle)
int HdmiCecSetTxCallback(int handle, HdmiCecTxCallback_t cbfunc, void *data)
int HdmiCecSetRxCallback(int handle, HdmiCecRxCallback_t cbfunc, void *data)
int HdmiCecTx(int handle, const unsigned char *buf, int len, int *result)</api_or_interface_used>
    <input_parameters>handle - driver handle
opcode - cec frame opcode</input_parameters>
    <automation_approch>1.Load the Hdmicec Hal module
2.Register Tx and Rx call back functions
3.Transmit the CEC frame to get version number
4.Should receive the transmission status using Tx call back functions
5.Should get the send status as HDMI_CEC_IO_SENT_BUT_NOT_ACKD, because there is no target device
6.Based on the send status, update the test result as SUCCESS/FAILURE
7.Unload the module</automation_approch>
    <expected_output>Should transmit the packets and get the send status as HDMI_CEC_IO_SENT_BUT_NOT_ACKD</expected_output>
    <priority>High</priority>
    <test_stub_interface>libhdmicechalstub.so.0.0.0</test_stub_interface>
    <test_script>HdmicecHal_Tx_No_HDMI</test_script>
    <skipped>No</skipped>
    <release_version>M79</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("hdmicechal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'HdmicecHal_Tx_No_HDMI');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # Setup without TV connection or setup with non CEC TV is required for
    # this test

    # This test is to check whether packets are getting transmitted properly
    # and expecting not acknowledged sent status, since there is no target
    # device or no CEC feature in target device

    print "\nTEST STEP : Register HdmiCec Tx & Rx call back"
    print "EXEPECTED RESULT : Functions should get registered"
    tdkTestObj = obj.createTestStep('HdmicecHal_SetTxCallback');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult1 = tdkTestObj.getResult();
    details1 = tdkTestObj.getResultDetails();
    tdkTestObj = obj.createTestStep('HdmicecHal_SetRxCallback');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult2 = tdkTestObj.getResult();
    details2 = tdkTestObj.getResultDetails();
    if expectedResult in actualResult1 and expectedResult in actualResult2:
        tdkTestObj.setResultStatus("SUCCESS");
        print details1
        print details2
        print "ACTUAL RESULT  : HdmiCecSetTxCallback & HdmiCecSetRxCallback calls success\n"

        print "\nTEST STEP : Transmit CEC Frame to get CEC Version"
        print "EXEPECTED RESULT : Should receive not acknowledged send status"
        tdkTestObj = obj.createTestStep('HdmicecHal_Tx');
        expectedResult = "FAILURE"
        version_opcode = "9F"
        print "Opcode to be sent: GET_CEC_VERSION: ",version_opcode
        tdkTestObj.addParameter("opcode",version_opcode);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult and "HDMI_CEC_IO_SENT_BUT_NOT_ACKD" in details:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Value Retuned  :",details
            print "ACTUAL RESULT  : CEC Version frame transmitted but not acknowledged"
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Value Retuned  :",details
            print "ACTUAL RESULT  : CEC Version frame transmitted & acknowledged"
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print details1
        print details2
        print "ACTUAL RESULT  : HdmiCecSetTxCallback / HdmiCecSetRxCallback call failed"
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("hdmicechal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");

