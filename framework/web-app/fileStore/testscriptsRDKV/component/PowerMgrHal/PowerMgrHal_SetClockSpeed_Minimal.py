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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>PowerMgrHal_SetClockSpeed_Minimal</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_SetClockSpeed</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to set CPU_SPEED_MINIMAL value as cpu speed using PLAT_API_SetClockSpeed API</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PowerMgrHal_09</test_case_id>
    <test_objective>Test Script to set CPU_SPEED_MINIMAL value as cpu speed using PLAT_API_SetClockSpeed API</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI6</test_setup>
    <pre_requisite>1.TDK Agent should be up and running
2.Initialize CPE Power management module</pre_requisite>
    <api_or_interface_used>int PLAT_INIT(void)
int PLAT_API_DetemineClockSpeeds(uint32_t *cpu_rate_Normal, uint32_t *cpu_rate_Scaled, uint32_t *cpu_rate_Minimal);
int PLAT_API_GetClockSpeed(uint32_t *speed)
int PLAT_API_SetClockSpeed(uint32_t speed)</api_or_interface_used>
    <input_parameters>speed - minimal  cpu clock speed</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialise the powerMgr hal module using PLAT_INIT API
3. Get the normal,scaled and minimal clock speeds using PLAT_API_DetemineClockSpeeds API. 
4. Get the current clock speed using PLAT_API_GetClockSpeed
5. Calculate the time taken for executing the command "uptime" with current clock speed
6.Invoke PLAT_API_SetClockSpeed  API to set minimal clock speed
7. Calculate the time taken for executing the command "uptime" with minimal clock speed
8.Based on the API return value and comparing the command execution time taken with normal and minimal clock speeds, update the test status as SUCCESS/FAILURE
9.Revert the clock speed to normal
10.Unload the module</automation_approch>
    <expected_output>API should set the cpu speed value. Command execution taken taken with minimal clock speed  should be greater than time taken with normal clock speed</expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_SetClockSpeed_Minimal</test_script>
    <skipped>No</skipped>
    <release_version>M77</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("pwrmgrhal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'PowerMgrHal_SetClockSpeed_Minimal');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # Test script gets the time taken for "uptime" command execution with noraml
    # and minimal clock speeds. Time taken with minimal clock speed > than time
    # taken with normal clock speed. Since normal clock speed value > than minimal
    # clock speed value

    # Sample stub output:
    # PLAT_API_DetemineClockSpeeds
    #   CPU_SPEED_NORMAL=%d, CPU_SPEED_SCALED=%d, CPU_SPEED_MINIMAL=%d
    # PLAT_API_GetClockSpeed
    #   Default Frequency=%d

    print "\nTEST STEP1 : Get the CPU clock speed using PLAT_API_DetemineClockSpeeds API"
    print "EXEPECTED OUTPUT : Should get the cpu minimal speed"
    tdkTestObj = obj.createTestStep('PowerMgrHal_DetemineClockSpeeds');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        cpu_speed_minimal = int(str(str(details).split(",")[2].split("=")[1]))
        print "Value Returned : ",str(details).split(",")[2]
        print "ACTUAL RESULT  : PLAT_API_DetemineClockSpeeds call is success"

        print "\nTEST STEP2 : Get the CPU clock speed using PLAT_API_GetClockSpeed"
        print "EXEPECTED OUTPUT : Should get the current clock speed of CPU"
        tdkTestObj = obj.createTestStep('PowerMgrHal_GetClockSpeed');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            cpu_speed_actual = int(str(str(details).split("=")[1]))
            print "Value Returned : ",details
            print "ACTUAL RESULT  : PLAT_API_GetClockSpeed call is success"

            #Get the time taken to excute uptime cmd in nano-seconds with Normal clock speed
            print "\nTEST STEP3 : Get the uptime command execution time with Normal clock speed"
            print "EXEPECTED OUTPUT : Should get the time taken for uptime cmd in nano seconds"
            tdkTestObj = obj.createTestStep('PowerMgrHal_GetCmdTimeTaken');
            cmd = "uptime"
            tdkTestObj.addParameter("cmd",cmd);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                cmd_time_actual = int(str(str(details).split(":")[1].split("(")[0].strip()))
                print "Value Returned : %s" %(str(details).split(";")[0])
                print "ACTUAL RESULT  : %s command execution using system call is success" %(cmd)

                # PLAT_API_SetClockSpeed  API is applicable for ARM platform only. Not supposed to execute on MIPS platform
                print "\nTEST STEP4 : Set the CPU clock speed using PLAT_API_SetClockSpeed API"
                print "EXPECTED RESULT : Should set the cpu minimal speed value"
                tdkTestObj = obj.createTestStep('PowerMgrHal_SetClockSpeed');
                print "CPU Minimal speed to be set : %d" %(cpu_speed_minimal)
                tdkTestObj.addParameter("speed",int(cpu_speed_minimal));
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "ACTUAL RESULT  : ",details
                    print "[TEST EXECUTION RESULT] : SUCCESS"

                    #Get the time taken to excute uptime cmd in nano-seconds with Minimal clock speed
                    print "\nTEST STEP5 : Get the uptime command execution time with Minimal clock speed"
                    print "EXEPECTED OUTPUT : Should get the time taken for uptime cmd in nano seconds"
                    tdkTestObj = obj.createTestStep('PowerMgrHal_GetCmdTimeTaken');
                    cmd = "uptime"
                    tdkTestObj.addParameter("cmd",cmd);
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        cmd_time_minimal = int(str(str(details).split(":")[1].split("(")[0].strip()))
                        print "Value Returned : %s" %(str(details).split(";")[0])
                        print "ACTUAL RESULT  : %s command execution using system call is success" %(cmd)

                        print "\nTEST STEP6 : Compare the Normal & Minimal clock speed command execution time taken"
                        print "EXEPECTED OUTPUT : Time taken with Minimal clock should be > than Normal clock time taken"
                        if cmd_time_minimal > cmd_time_actual:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "ACTUAL RESULT  : Time taken with minimal clock speed is greater as expected"
                            print "[TEST EXECUTION RESULT] : SUCCESS\n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "ACTUAL RESULT  : Time taken with minimal clock speed is not as expected"
                            print "[TEST EXECUTION RESULT] : FAILURE\n"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "ACTUAL RESULT  : %s command execution using system call is failed" %(cmd)
                        print "[TEST EXECUTION RESULT] : FAILURE\n"

                    print "\nTEST STEP7 : Revert the CPU clock speed using PLAT_API_SetClockSpeed API"
                    print "EXPECTED RESULT : Should set the cpu normal speed value"
                    tdkTestObj = obj.createTestStep('PowerMgrHal_SetClockSpeed');
                    print "CPU Normal speed to be set : %d" %(cpu_speed_actual)
                    tdkTestObj.addParameter("speed",int(cpu_speed_actual));
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "ACTUAL RESULT  : CPU clock speed reverted to normal successfully"
                        print "[TEST EXECUTION RESULT] : SUCCESS\n"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "ACTUAL RESULT  : CPU clock speed revert to normal failed"
                        print "[TEST EXECUTION RESULT] : FAILURE\n"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "ACTUAL RESULT  : ",details
                    print "[TEST EXECUTION RESULT] : FAILURE\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT  : ",details
                print "[TEST EXECUTION RESULT] : FAILURE\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "ACTUAL RESULT  : ",details
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT  : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("pwrmgrhal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


