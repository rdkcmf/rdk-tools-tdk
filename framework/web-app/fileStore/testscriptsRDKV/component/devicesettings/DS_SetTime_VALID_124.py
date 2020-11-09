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
  <version>7</version>
  <name>DS_SetTime_VALID_124</name>
  <primitive_test_id>80</primitive_test_id>
  <primitive_test_name>DS_SetTime</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script Sets and gets a valid Time in the text display of given Front panel Indicator
Test Case ID : CT_DS124</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS124</test_case_id>
    <test_objective>Sets a valid time in the text display of given Front panel Indicator.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()   
FrontPanelTextDisplay::getInstance("Text")
FrontPanelTextDisplay::setTime()
Device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>SetTime : int – hrs, int – mins
E.g.: hrs=04 mins=44s
</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will set a new time by passing “hrs” and “mins” value.
3.TM makes RPC calls for setting the Time format from Device_Settings_Agent.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <except_output>Checkpoint 1. Check for the return value of setTime </except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_FP_setTime
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_SetTime_VALID_124</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks>XONE-10478</remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from devicesettings import dsManagerInitialize, dsManagerDeInitialize

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'DS_SetTime_VALID_124');
loadmodulestatus =obj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #calling Device Settings - initialize API
        result = dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #setting time
                tdkTestObj = obj.createTestStep('DS_SetTime');
                hrs = 04
                mins = 44
                print "Hours=%d Minutes=%d" %(hrs,mins);
                tdkTestObj.addParameter("time_hrs",hrs);
                tdkTestObj.addParameter("time_mins",mins);
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "SetTime Result: [%s]"%actualresult
                #Check for return value of DS_SetTime
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                #calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(obj)
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
