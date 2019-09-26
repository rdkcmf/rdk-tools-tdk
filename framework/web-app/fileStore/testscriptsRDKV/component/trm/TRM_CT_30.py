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
  <id>1702</id>
  <version>2</version>
  <name>TRM_CT_30</name>
  <primitive_test_id/>
  <primitive_test_name>TRM_ReleaseTunerReservation</primitive_test_name>
  <primitive_test_version>5</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests release live reservation on channel 1 and again reserve it for recording when current state of reservation is (L-L-L-R-R).
Test Case ID: CT_TRM_30
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TRM_30</test_case_id>
    <test_objective>To attempt to release live reservation on channel 1 and again reserve it for recording when current state of reservation is (L-L-L-R-R)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ReserveTuner
ReleaseTunerReservation
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
4. Verify that TRM allows Device1 live tune channel1 - Device2 live tune channel2 - Device3 live tune channel 3 - Device4 record channel4 - Device5 record channel5.
5. Verify that TRM allows Device1 release channel 1 using "TRMAgent_ReleaseTunerReservation".
6. Verify that TRM allows Device1 record channel1 again.
7. TRMAgent get the response from the TRM server for all the requests.  
8. Depending on the return values of ReserveTuner TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>1. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_TunerReserveForRecord
TRMAgent_TunerReserveForLive
TRMAgent_ReleaseTunerReservation</test_stub_interface>
    <test_script>TRM_CT_30</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from trm import reserveForRecord,reserveForLive,releaseReservation,getAllTunerStates;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CT_30');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_30');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    # Pre-condition: Device1 L1, Device2 L2, Device3 L3, Device4 R4, Device5 R5
    duration = 10000
    startTime = 0

    # Live tune channel 1
    print "Live tune channel 1"
    deviceNo = 0
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'01','duration':duration,'startTime':startTime})

    # Live tune channel 2
    print "Live tune channel 2"
    deviceNo = 1
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'02','duration':duration,'startTime':startTime})

    # Live tune channel 3
    print "Live tune channel 3"
    deviceNo = 2
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'03','duration':duration,'startTime':startTime})

    # Recording channel 4
    print "Recording channel 4"
    deviceNo = 3
    hot = 0
    recordingId = 'RecordIdCh04'
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'04','duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})

    # Recording channel 5
    print "Recording channel 5"
    deviceNo = 4
    hot = 0
    recordingId = 'RecordIdCh05'
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'05','duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})
    # End of pre-condition

    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    # Release live tune on channel 1
    print "Release live tune on channel 1"
    deviceNo = 0
    releaseReservation(obj,"SUCCESS",kwargs={'deviceNo':deviceNo,'activity':1,'streamId':'01'})

    # Recording channel 1
    print "Recording channel 1"
    deviceNo = 0
    hot = 0
    recordingId = 'RecordIdCh01'
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'01','duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})

    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
