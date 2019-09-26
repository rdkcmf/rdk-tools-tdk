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
  <id>1664</id>
  <version>2</version>
  <name>TRM_CT_34</name>
  <primitive_test_id>636</primitive_test_id>
  <primitive_test_name>TRM_CancelRecording</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests recording channel 6 when current state of reservation is (R1-R2-R3-R4-R5), cancel recording channel 1 and again start recording channel 6.
Test Case ID: CT_TRM_34
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
    <test_case_id>CT_TRM_34</test_case_id>
    <test_objective>To attempt to start recording channel 6 when current state of reservation is (R1-R2-R3-R4-R5) then cancel recording1 and again start recording channel 6.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ReserveTuner
CancelRecording</api_or_interface_used>
    <input_parameters>INTEGER  deviceNo
STRING    recordingId
STRING    locator
DOUBLE  duration	
DOUBLE  startTime
INTEGER hot</input_parameters>
    <automation_approch>1. TM loads TRMAgent via the test agent.
2. TM will invoke “TRMAgent_TunerReserveForLive” for live tune and “TRMAgent_TunerReserveForRecord” for record.
3. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and post HTTP TRM ReserveTuner messages with duration value = 10000 (10s) and startTime=0.
4. Verify that TRM allows device 1 to 5 to record channels 1 to 5
5. Verify that TRM does not allow device 6 to record channel 6.
6. Verify that TRM allows cancelling recording on channel 1 using TRMAgent_CancelRecording
7. Verify that TRM allows device 6 to record channel 6 again
8. TRMAgent get the response from the TRM server for all the requests.  
9. Depending on the return values of TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>1. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_TunerReserveForRecord
TestMgr_TRM_CancelRecording</test_stub_interface>
    <test_script>TRM_CT_34</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import trm;
from time import sleep;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_34');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_34');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    # Fetch max tuners supported
    maxTuner = trm.getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuner ):
        print "Exiting without executing the script"
        obj.unloadModule("trm");
        exit()

    # Step1: Start recording on all the tuners available
    for deviceNo in range(0,maxTuner):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        recordingId = 'RecordIdCh'+streamId
        trm.reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Step2: Record a new channel when all tuners are already busy recording
    streamId = '0'+str(maxTuner+1)
    recordingId = 'RecordIdCh'+streamId
    trm.reserveForRecord(obj,'FAILURE',kwargs={'deviceNo':maxTuner,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Step3: Cancel recording on channel 1
    trm.cancelRecording(obj,'SUCCESS',kwargs={'streamId':'01'})

    # Step4: Record the new channel again
    trm.reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':maxTuner,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Add sleep to release all reservations
    sleep(20)

    #unloading trm module
    obj.unloadModule("trm");
