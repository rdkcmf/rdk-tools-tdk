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
  <id>1488</id>
  <version>3</version>
  <name>TRM_ValidateTunerReservation</name>
  <primitive_test_id/>
  <primitive_test_name>TRM_ValidateTunerReservation</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests validate tuner reservation.
Test Case ID: CT_TRM_08
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
    <test_case_id>CT_TRM_08</test_case_id>
    <test_objective>To request to validate tuner reservation</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ValidateTunerReservation</api_or_interface_used>
    <input_parameters>INTEGER  deviceNo</input_parameters>
    <automation_approch>1. TM loads TRMAgent via the test agent.  
2. TM will invoke “TRMAgent_ValidateTunerReservation” in TRMAgent. 
3. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and post HTTP TRM ReserveTuner for Live request followed by  ValidateTunerReservation request message after waiting for 2 sec.
4. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and get the response from the TRM server.  
5. Depending on the return value of ValidateTunerReservation TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1. Check for the return value of tuner reservation validate response msg.
Checkpoint 2. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_ValidateTunerReservation</test_stub_interface>
    <test_script>TRM_ValidateTunerReservation</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from trm import reserveForLive,reserveForRecord,validateReservation

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_ValidateTunerReservation');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_ValidateTunerReservation');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    print "Start live tuning channel 1"
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'01','duration':10000,'startTime':0})

    time.sleep(2)

    print "Validate live reservation"
    validateReservation(obj,"SUCCESS",kwargs={'deviceNo':0,'activity':1,'streamId':'01'})

    print "Start recording channel 2"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'02','duration':10000,'startTime':0,'recordingId':'"RecordIdCh02','hot':0})

    time.sleep(2)

    print "Validate recording reservation"
    validateReservation(obj,"SUCCESS",kwargs={'deviceNo':0,'activity':2,'streamId':'02'})

    #unloading trm module
    obj.unloadModule("trm");
