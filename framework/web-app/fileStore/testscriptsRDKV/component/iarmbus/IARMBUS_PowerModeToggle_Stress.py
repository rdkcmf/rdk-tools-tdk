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
  <version>11</version>
  <name>IARMBUS_PowerModeToggle_Stress</name>
  <primitive_test_id>8</primitive_test_id>
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <primitive_test_version>8</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test multiple toggles between STB Standby and Power-on states.
Mapped from Testcase ID: CT_DS119 in devicesettings Testcase
Testcase ID: CT_IARMBUS_113</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_IARMBUS_113</test_case_id>
    <test_objective>Check multiple (50 times) toggles between STB Standby and Power-on</test_objective>
    <test_type>Positive(Stress)</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1.”IARMDaemonMain” process should be running.

2.“pwrMgrMain” process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_Call(const char *,  const char *, void *, size_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_RegisterCall : 
const char * - IARM_BUS_PWRMGR_API_GetPowerState
IARM_BusCall_t - _GetPowerStatecallback
IARM_Bus_Call : 
const char *- IARM_BUS_PWRMGR_NAME,     const char * - IARM_BUS_PWRMGR_API_GetPowerState  , void * -param, size_t - sizeof(param)
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent.
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon. 
3.pwrMgrMain registers a RPC methods for setting the power state and this RPC can be invoked by IARMBUS_Agent application.
4.IARMBUS_Agent Invoke the RPC method of pwrMgrMain application to set the power state of STB.
5.IARMBUS_Agent Invoke the RPC method of pwrMgrMain application to get the power state of STB. 
6.Repeat steps 2 to 5 for power state values STANDBY (1) and ON (2) for 50 times.
7.IARMBUS_Agent deregister from the IARM Bus Daemon.
8.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BusCall</test_stub_interface>
    <test_script>IARMBUS_PowerModeToggle_Stress</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks>This is skipped till RDKTT-152 is fixed.</remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import change_powermode

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

iarmObj.configureTestCase(ip,port,'IARMBUS_PowerModeToggle_Stress');
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[IARMBUS LIB LOAD STATUS] : %s"%iarmLoadStatus ;
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);
expectedresult="SUCCESS"

if expectedresult in iarmLoadStatus.upper():
    # Repeat PowerMode change for 50 times
    for x in range(0,50):
        # Toggle between state values STANDBY (1) / ON (2)
        for powermode in range(1,3):
            actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
            print "IARMBUS_Init result: [%s]"%actualresult;
            #Check for return value of IARMBUS_Init
            if expectedresult in actualresult:
                #Calling "IARM_Bus_Connect"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});
                print "IARMBUS_Connect result: [%s]"%actualresult;

                #Check for return value of IARMBUS_Connect
                if expectedresult in actualresult:
                    #Calling change_powermode
                    result = change_powermode(iarmObj,powermode);
                    print "Set PowerMode to %d: %s"%(powermode,result);

                    #Calling IARMBus_DisConnect API
                    actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});
                    print "IARMBUS_DisConnect result: [%s]"%actualresult;

                #calling IARMBUS API "IARM_Bus_Term"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term', 'SUCCESS',verifyList ={});
                print "IARMBUS_Term result: [%s]"%actualresult;
    #End of loop for power mode toggle
    #End of loop for 50 times
    #Make sure the DUT must in Power ON state after the loop
    actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
    print "IARMBUS_Init result: [%s]"%actualresult;
    #Check for return value of IARMBUS_Init
    if expectedresult in actualresult:
                #Calling "IARM_Bus_Connect"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});
                print "IARMBUS_Connect result: [%s]"%actualresult;

                #Check for return value of IARMBUS_Connect
                if expectedresult in actualresult:
                    #Calling change_powermode
                    change_powermode(iarmObj,2);
                    print "Set PowerMode to %d: %s"%(powermode,result);

                    #Calling IARMBus_DisConnect API
                    actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});
                    print "IARMBUS_DisConnect result: [%s]"%actualresult;

                #calling IARMBUS API "IARM_Bus_Term"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term', 'SUCCESS',verifyList ={});
                print "IARMBUS_Term result: [%s]"%actualresult
    #Unload the iarmbus module
    iarmObj.unloadModule("iarmbus");
