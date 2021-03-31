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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>MFRHal_Get_SerializedData_ManufacturerOUI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MfrHal_GetSerializedData</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To retrieve Manufacturer name from DUT</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_MFR_HAL_02</test_case_id>
    <test_objective>To retrieve Manufacturer OUI from DUT</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Initialize the MFR module using mfr_init()</pre_requisite>
    <api_or_interface_used>mfrError_t mfrGetSerializedData( mfrSerializedType_t type,  mfrSerializedData_t *data );</api_or_interface_used>
    <input_parameters>mfrSerializedType_t type = 1 for mfrSERIALIZED_TYPE_MANUFACTUREROUI</input_parameters>
    <automation_approch>1. TM loads the MfrHal agent via the test agent.
2 . MfrHal agent will invoke the api mfrGetSerializedData() with type of serialized data to be retrieved as input.
3. Verify that the data retrieved is not empty.
4. Based on the API call return code, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the serialized data retrieved is not empty</expected_output>
    <priority>High</priority>
    <test_stub_interface>libmfrhalstub.so.0.0.0</test_stub_interface>
    <test_script>MFRHal_Get_SerializedData_ManufacturerOUI</test_script>
    <skipped>No</skipped>
    <release_version>M87</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
mfrhalObj = tdklib.TDKScriptingLibrary("mfrhal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
mfrhalObj.configureTestCase(ip,port,'MFRHal_Get_SerializedData_ManufacturerOUI');

#Get the result of connection with test component and DUT
result =mfrhalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
mfrhalObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
    expectedresult="SUCCESS"

    #Prmitive test case which associated to this Script
    tdkTestObj = mfrhalObj.createTestStep('MfrHal_GetSerializedData');
    #Set the serialized data type to 1(mfrSERIALIZED_TYPE_MANUFACTUREROUI)
    tdkTestObj.addParameter("data_type", 1)

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();

    #Set the result status of execution
    if (actualresult == expectedresult):
        print "Successfully executed MfrHal_GetSerializedData"
        manufacturerOUI = str(tdkTestObj.getResultDetails())
        if (manufacturerOUI):
            print "MfrHal_GetSerializedData: ManufacturerOUI : ", manufacturerOUI
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "ManufacturerOUI data retrieved is empty or incorrect"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "Failed to execute MfrHal_GetSerializedData"
        tdkTestObj.setResultStatus("FAILURE");

    #Unload the module
    mfrhalObj.unloadModule("mfrhal");

else:
    print "Failed to load mfrhal module\n";
    #Set the module loading status
    mfrhalObj.setLoadModuleStatus("FAILURE");
