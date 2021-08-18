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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>System_Device_Details_Check</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>ExecuteCommand</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check whether all parameters of deviceDetails are obtained as expected</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Hybrid-5</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>IPClient-6</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>sysutil_01</test_case_id>
    <test_objective>To check whether all parameters of deviceDetails are obtained as expected</test_objective>
    <test_type>Positive</test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.Read parameters from file /tmp/.deviceDetails.cache 
2.Check using regex for each parameter
3.TM will set result status based on regex result</automation_approch>
    <expected_output>All parameters must match the expected pattern</expected_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script>System_Device_Details_Check</test_script>
    <skipped>No</skipped>
    <release_version>M79</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import re;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Function to check the regular expression for the specified parameters
def checkValue(parameter):
    return {
        'mac': bool(re.match("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]){2}$", Value)),
	'rf4ce_mac': bool(re.match("^([0-9A-Fa-f]{2}[:-]){7}([0-9A-Fa-f]){2}$", Value)),
        'ip': bool(re.match("^([0-9a-f]*[:-])+([0-9a-f])*$", Value)),
        'build_type': bool(Value == 'VBN'),
        'DACInitTimestamp': bool(re.match("^[a-zA-Z]{3}:([0-9]+[:-])+[0-9]+$", Value)),
        'serial_number': bool((len(Value) == 12) & bool(re.match("[A-Z0-9]*", Value))),
        'cableCardVersion': bool(re.match("^[0-9]{2}.[0-9]{2}$", Value)),
        'model': bool(re.match("[A-Z0-9]*", Value)),
        'imageVersion': bool(Value),
        'friendly_id': bool(MANUFACTURER.lower() in Value.lower()),
    }[parameter]

#Test component to be tested
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
sysUtilObj.configureTestCase(ip,port,'System_Device_Details_Check');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

if "SUCCESS" in sysUtilLoadStatus.upper():
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
    cmd = "cat /tmp/.deviceDetails.cache | wc -l"
    print cmd;
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase("SUCCESS");
    actualresult = tdkTestObj.getResult();
    parameters = tdkTestObj.getResultDetails()
    parameters = parameters.split("\\")[0];
    #print "%d parameters"%(int(parameters))
    failedparams = {};

    #Check if wifi is supported
    tdkTestObj.addParameter("command", "cat /etc/device.properties | grep WIFI_SUPPORT=true | wc -l");
    tdkTestObj.executeTestCase("SUCCESS");
    isWifipresent = tdkTestObj.getResultDetails().split("\\")[0];
    if not int(isWifipresent):
        print "Device doesnot have wifi\n"
    else:
        print "Device supports wifi\n"

    #Get MANUFACTURER
    tdkTestObj.addParameter("command", "cat /etc/device.properties  | grep  MFG | cut -d \"=\" -f 2");
    tdkTestObj.executeTestCase("SUCCESS");
    MANUFACTURER = tdkTestObj.getResultDetails().split("\\")[0];

    for parameter in range(1,int(parameters)+1):
        cmd = "awk 'NR==%d' /tmp/.deviceDetails.cache"%parameter
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase("SUCCESS");
        actualresult = tdkTestObj.getResult();
        Value = tdkTestObj.getResultDetails().split("\\")[0];
        print Value
        parameterName = parameter = Value.split("=")[0];
        Value = Value.split("=")[1];
        if 'mac' in parameter.lower():
                if parameter == 'wifi_mac':
                        if not int(isWifipresent):
                                print "wifi_mac should be empty for this device"
                                result = not Value;
                        else:
                                result = checkValue('mac')
                elif parameter == 'rf4ce_mac':
                        result = checkValue('rf4ce_mac')
		else:
			result = checkValue('mac')
        elif 'ip' in parameter.lower():
                result = checkValue('ip')
        elif 'model' in parameter:
                result = checkValue('model')
        else :
                result = checkValue(parameter)

        if result:
                print "Verification of %s is SUCCESS\n Value = %s\n"%(parameterName,Value);
        else:
                print "Verification of %s is FAILED\n Value = %s\n"%(parameterName,Value);
                failedparams[parameterName]=Value;


    if not failedparams:
        print "SUCCESS:All parameters verified"
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        print "FAILURE:Failed parameters :",failedparams;
        tdkTestObj.setResultStatus("FAILURE");

sysUtilObj.unloadModule("systemutil");
