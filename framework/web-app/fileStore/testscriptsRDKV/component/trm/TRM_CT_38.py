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
  <id>1710</id>
  <version>1</version>
  <name>TRM_CT_38</name>
  <primitive_test_id>613</primitive_test_id>
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests hot record channel 1 with start time 2s from now for 10s and again request hot record channel1 with start time 4s from now for 5s. 
Test Case ID: CT_TRM_38
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
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TRM_38</test_case_id>
    <test_objective>To attempt to hot record channel 1 with start time 2s from now for 10s and again request hot record channel1 with start time 4s from now for 5s</test_objective>
    <test_type>Positive</test_type>
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
4. Verify that TRM allows Device1 schedule a hot recording 2s from now for 10s on channel 1 with duration value = 10000 (10s) and startTime=2.
5. Verify that TRM allows Device1 to schedule a hot recording 4s from now for 5s on channel 1 with duration value = 5000 (5s) and startTime=4.
6. Verify all the reservations using TRMAgent_GetAllTunerStates.
7. TRMAgent get the response from the TRM server for all the requests.  
8. Depending on the return values of TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>1. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_TunerReserveForRecord
TestMgr_TRM_GetAllTunerStates</test_stub_interface>
    <test_script>TRM_CT_38</test_script>
    <skipped>No</skipped>
    <release_version>M31</release_version>
    <remarks>Since DELIA-11551, TRM now allows multiple terminals to reserve tuner for recording of same serviceLocator and with overlapping time.</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from trm import reserveForRecord, getAllTunerStates;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CT_38');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_38');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    # Schedule future recordings on same channel
    # Hot recording channel 1 with start time 2s from now for 10s
    print "Schedule recording on channel 1 with start time 2s from now for 10s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'01','duration':10000,'startTime':2,'recordingId':'RecordIdDevice1','hot':1})
    # Hot recording channel 1 with start time 4s from now for 5s
    print "Schedule recording on channel 1 with start time 4s from now for 5s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':'01','duration':5000,'startTime':4,'recordingId':'RecordIdDevice2','hot':1})
    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    # Schedule hot recordings on same channel
    # Send first recording request from device 3 starting now for 10s
    streamId = '01'
    print "Schedule hot recordings on channel 1 starting now for 10s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':2,'streamId':streamId,'duration':10000,'startTime':0,'recordingId':'RecordId03','hot':1})
    # Send second recording request from device 4 starting 5s from now for 10s
    print "Schedule recording on channel 1 starting 5s from now for 10s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':3,'streamId':streamId,'duration':10000,'startTime':5,'recordingId':'RecordId04','hot':0})
    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
