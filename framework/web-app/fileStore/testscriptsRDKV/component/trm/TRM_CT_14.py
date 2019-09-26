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
  <id>1619</id>
  <version>2</version>
  <name>TRM_CT_14</name>
  <primitive_test_id>613</primitive_test_id>
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests recording reserve tuner requests more than TRM can handle.
Test Case ID: CT_TRM_14
Test Type: Negative</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TRM_14</test_case_id>
    <test_objective>To send more than max number of reserve tuners requests for recording than TRM can handle</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ReserveTuner</api_or_interface_used>
    <input_parameters>INTEGER  deviceNo
STRING    recordingId
STRING    locator
DOUBLE  duration	
DOUBLE  startTime
INTEGER hot</input_parameters>
    <automation_approch>1. TM loads TRMAgent via the test agent.  
2. TM will invoke “TRMAgent_TunerReserveForRecord” in TRMAgent for 6 different channels from 6 different terminals. 
3. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and post 6 HTTP TRM ReserveTuner for record request messages with different devicename, locator and recording Id values. Pass same duration value =10000 (10s), startTime=0 and hot=0 for all the recordings.
4. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and get the response from the TRM server.  
5. Depending on the return values of ReserveTuner TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>1. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_TunerReserveForRecord</test_stub_interface>
    <test_script>TRM_CT_14</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from trm import getMaxTuner,reserveForRecord,getAllTunerStates
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_14');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_14');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    #Fetch max tuner supported
    maxTuner = getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuner ):
        print "Exiting without executing the script"
    else:
        tdkTestObj = obj.createTestStep('TRM_TunerReserveForRecord');
        # Get all Tuner states for fetching live local tuning locator
        initStates = getAllTunerStates(obj,'SUCCESS')
        if 'Live' in initStates:
            for deviceNo in range(0,maxTuner):
		streamId = '0'+str(deviceNo+1)
		recordingId = 'RecordIdCh'+streamId
		locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()
		if locator in initStates:
		    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})
		    break;

        for deviceNo in range(0,maxTuner+1):
            # Frame different request URL for each client box
            streamId = '0'+str(deviceNo+1)
            recordingId = 'RecordIdCh'+streamId
            locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()

            if locator in initStates:
		continue
            elif ( maxTuner == deviceNo ):
                expectedRes = "FAILURE"
            else:
                expectedRes = "SUCCESS"
            reserveForRecord(obj,expectedRes,kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})
        # End for loop
        # Add sleep to release all reservations
        sleep(20)

    #unloading trm module
    obj.unloadModule("trm");
