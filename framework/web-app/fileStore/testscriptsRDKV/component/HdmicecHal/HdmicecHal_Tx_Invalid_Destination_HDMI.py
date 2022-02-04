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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>HdmicecHal_Tx_Invalid_Destination_HDMI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>HdmicecHal_Tx</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to transmit CEC frame to invalid destination device and check whether transmission is not getting acknowledged or not</synopsis>
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
    <test_case_id>TC_HdmicecHal_12</test_case_id>
    <test_objective>Test script to transmit CEC frame to invalid destination device and check whether transmission is not getting acknowledged or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG,XI3,XI6,Video_Accelerator</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. Required a setup with CEC enabled TV connection
3.  HdmiCecOpen should open a CEC driver instance successfully and iarmbus event should be obtained from device ready call back.
</pre_requisite>
    <api_or_interface_used>int HdmiCecOpen(int *handle)
int HdmiCecClose(int handle)
int HdmiCecSetTxCallback(int handle, HdmiCecTxCallback_t cbfunc, void *data)
int HdmiCecSetRxCallback(int handle, HdmiCecRxCallback_t cbfunc, void *data)
int HdmiCecTx(int handle, const unsigned char *buf, int len, int *result)</api_or_interface_used>
    <input_parameters>handle - driver handle
header - cec frame header
opcode - cec frame opcode</input_parameters>
    <automation_approch>1.Load the Hdmicec Hal module
2. Register Tx and Rx call back functions
3. To check whether the device is connected to CEC enabled TV, send a valid CEC frame and check whether able to transmit and receive successfully
4. If yes, form a CEC frame with invalid header and valid opcode
5. Should receive the send status as HDMI_CEC_IO_SENT_BUT_NOT_ACKD
6. Based on the send status update the test result as SUCCESS/FAILURE
7. Unload the module</automation_approch>
    <expected_output>Should get HDMI_CEC_IO_SENT_BUT_NOT_ACKD as send status for a invalid destination</expected_output>
    <priority>High</priority>
    <test_stub_interface>libhdmicechalstub.so.0.0.0</test_stub_interface>
    <test_script>HdmicecHal_Tx_Invalid_Destination_HDMI</test_script>
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
obj.configureTestCase(ip,port,'HdmicecHal_Tx_Invalid_Destination_HDMI');

def checkCECSupportedTVConnection(tdkTestObj):
    expectedResult = "SUCCESS"
    CECSupported = "FALSE"

    print "Check whether CEC enabled TV by transmitting a frame"
    version_opcode = "9F"
    version_operand = "9E"
    print "Opcode to be sent: GET_CEC_VERSION: ",version_opcode
    print "Operand to be received: CEC_VERSION: ",version_operand
    tdkTestObj.addParameter("opcode",version_opcode);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print str(details).split(";")[0]
        version_operand_received = str(details).split(";")[0].split(":")[1].strip()
        if version_operand in version_operand_received:
            CECSupported = "TRUE"
    else:
        tdkTestObj.setResultStatus("FAILURE");

    return CECSupported

def getSrcLogicalAddress(tdkTestObj):
    logicalAddress = 0;
    status = "FALSE"
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print details
        logicalAddress = int(str(details).split(":",1)[1].split(",")[1].split(":")[1].strip())
        # Decimal value of 0x0F = 15
        logicalAddressClosed = 15
        if logicalAddress != logicalAddressClosed:
            status = "TRUE"
    else:
        tdkTestObj.setResultStatus("FAILURE");

    return status,logicalAddress

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # Setup with CEC enabled TV connection is mandatory for this test

    # Here, CEC frame is transmitted with invalid destination logical
    # address,expecting packets not to be acknowledged.

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

        tdkTestObj1 = obj.createTestStep('HdmicecHal_GetLogicalAddress');
        tdkTestObj2 = obj.createTestStep('HdmicecHal_Tx');
        ConnStatus,logicalAddress = getSrcLogicalAddress(tdkTestObj1)
        CECSupport = checkCECSupportedTVConnection(tdkTestObj2)
        if CECSupport == "TRUE" and ConnStatus == "TRUE":

            print "\nTEST STEP : Transmit CEC Frame to invalid destination"
            print "EXEPECTED RESULT : Should receive not acknowledged send status"
            tdkTestObj = obj.createTestStep('HdmicecHal_Tx');
            expectedResult = "FAILURE"
            # Logical address of TV is 0, but using invalid address as 1
            header = str(logicalAddress) + "1"
            version_opcode = "9F"
            print "Frame to be sent: %s %s" %(header,version_opcode)
            tdkTestObj.addParameter("header",header);
            tdkTestObj.addParameter("opcode",version_opcode);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedResult in actualResult and "HDMI_CEC_IO_SENT_BUT_NOT_ACKD" in details:
                tdkTestObj.setResultStatus("SUCCESS");
                txInfo  = str(details).split(";")
                print "Value Retuned :",details
                print "ACTUAL RESULT : CEC frame transmitted but no destination to acknowledge"
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print details
                print "ACTUAL RESULT : CEC frame transmitted & acknowledged"
                print "[TEST EXECUTION RESULT] : FAILURE\n"
        else:
            if CECSupport == "FALSE":
                print "Please test with CEC Enabled TV connected device"
                tdkTestObj1.setResultStatus("FAILURE");
            else:
                print "No HdmiCec driver instance"
                tdkTestObj2.setResultStatus("FAILURE");
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


