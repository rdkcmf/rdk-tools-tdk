##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
  <version>9</version>
  <name>DS_GetCPUTemperature_126</name>
  <primitive_test_id/>
  <primitive_test_name>DS_GetCPUTemperature</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script gets the STB CPU Temperature.
Test Case ID : CT_DS_126</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS126</test_case_id>
    <test_objective>Get the value of CPU temperature.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize() 
device::Host::getCPUTemperature()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2. Device_Settings_Agent will get the value of cpu temperature.
3. Device_Settings_Agent will return SUCCESS or FAILURE based on whether API execution is successful and value is within limit, more than 0 and less than 125C.</automation_approch>
    <except_output>Checkpoint 1.Check that cpu temperature value is more than 0 and less than 125C.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_HOST_getCPUTemperature
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_GetCPUTemperature_126</test_script>
    <skipped>No</skipped>
    <release_version>M23</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from devicesettings import dsManagerInitialize,dsManagerDeInitialize;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load DS module
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'DS_GetCPUTemperature_126');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus(dsLoadStatus);

if 'SUCCESS' in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling Device Setting - Get CPU Temperature
                dsTestObj = dsObj.createTestStep('DS_GetCPUTemperature');
                expectedresult = "SUCCESS"
                dsTestObj.executeTestCase(expectedresult);
                actualresult = dsTestObj.getResult();
                details = dsTestObj.getResultDetails();
                print "Result : [%s] "%actualresult,
                #Check for SUCCESS/FAILURE return value of DS_GetCPUTemperature
                if expectedresult in actualresult:
                        print "Details : [+%sC]" %details;
                        if ((float(details) <= float(0)) or (float(details) > float(125))):
                                print "Temperature out of range";
                                dsTestObj.setResultStatus("FAILURE");
                        else:
                                dsTestObj.setResultStatus("SUCCESS");
                else:
                        dsTestObj.setResultStatus("FAILURE");
                        print "Details : [%s]" %details;
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
