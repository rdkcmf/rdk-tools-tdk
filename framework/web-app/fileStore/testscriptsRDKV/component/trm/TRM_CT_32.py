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
  <id>1699</id>
  <version>5</version>
  <name>TRM_CT_32</name>
  <primitive_test_id/>
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests recording and then live tune to channel 6 on terminal2 when current state of reservation is L1 on terminal1 and L2-R3-R4-R5 on terminal2.
Test Case ID: CT_TRM_32
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
    <test_case_id>CT_TRM_32</test_case_id>
    <test_objective>To attempt to record and then live tune to channel 6 on terminal 2 when current state of reservation is L1 on terminal 1 and L2-R3-R4-R5 on terminal 2.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ReserveTuner
GetAllTunerStates</api_or_interface_used>
    <input_parameters>INTEGER  deviceNo
STRING    recordingId
STRING    locator
DOUBLE  duration	
DOUBLE  startTime
INTEGER hot</input_parameters>
    <automation_approch>1. TM loads TRMAgent via the test agent.
2. TM will invoke “TRMAgent_TunerReserveForLive” for live tune and “TRMAgent_TunerReserveForRecord” for record.
3. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and post HTTP TRM ReserveTuner messages with duration value = 10000 (10s) and startTime=0.
4. Verify that TRM allows Device1 tune to channel1 and device 2 tune channel 2 record channel 3 record channel 4 and record channel 5
5. Verify that TRM does not allow device 2 record channel 6.
6. Verify that TRM allows device 2 tune to channel 6.
7. Verify that all the reservations using TRMAgent_GetAllTunerStates.
8. TRMAgent get the response from the TRM server for all the requests.  
9. Depending on the return values of TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>1. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_TunerReserveForRecord
TestMgr_TRM_TunerReserveForLive
TestMgr_TRM_GetAllTunerStates</test_stub_interface>
    <test_script>TRM_CT_32</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import trm;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_32');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_32');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    duration = 10000
    startTime = 0

    #Fetch max tuners supported
    maxTuner = trm.getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuner ):
        print "Exiting without executing the script"
        obj.unloadModule("trm");
        exit()

    # Pre-condition: Device1:L1 - Device2:L2-R3-R4-R5
    # Device1: Live tune to channel 1
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'01','duration':duration,'startTime':startTime})

    # Device2: Live tune to channel 2
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':'02','duration':duration,'startTime':startTime})

    # Device2: Recording on maxtuner-2 channels
    for streamNo in range(3,maxTuner+1):
        streamId = '0'+str(streamNo)
        recordingId = 'RecordIdCh'+streamId
        trm.reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':0})
    # Pre-condition End

    # Device2: Recording new channel
    streamId = '0'+str(maxTuner+1)
    recordingId = 'RecordIdCh'+streamId
    trm.reserveForRecord(obj,'FAILURE',kwargs={'deviceNo':1,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':0})

    # Device2: Live tune to new channel
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':streamId,'duration':duration,'startTime':startTime})

    # Get all Tuner states
    trm.getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
