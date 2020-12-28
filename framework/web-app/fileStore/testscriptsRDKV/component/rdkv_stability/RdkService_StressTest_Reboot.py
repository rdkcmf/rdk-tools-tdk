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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>3</version>
  <name>RdkService_StressTest_Reboot</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_rebootDevice</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>To reboot the device for the given number of times and check the status of device after each reboot.</synopsis>
  <groups_id/>
  <execution_time>3000</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Video_Accelerator</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_02</test_case_id>
    <test_objective>To reboot the device for the given number of times and check the status of device after each reboot.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Number of reboots to be performed
2. Time delay for the device to come up after each reboot</input_parameters>
    <automation_approch>1. As a pre requisite, reboot the device once
2. Get the current status of all plugins
3. Reboot the device for given number of times.
4. Check for uptime, interface status, plugin status and controller UI status after each reboot.</automation_approch>
    <expected_output>The device should come online properly after each reboot.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RdkService_StressTest_Reboot</test_script>
    <skipped>No</skipped>
    <release_version>M82</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from StabilityTestVariables import *
import rebootTestUtility
from rebootTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_StressTest_Reboot');

result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result.upper();
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():

    #Reboot the device as a pre-requisite before starting the stress test
    print "REBOOTING DEVICE AS A PRE_REQUISITE"
    tdkTestObj = obj.createTestStep('rdkservice_rebootDevice');
    tdkTestObj.addParameter("waitTime",rebootwaitTime);
    tdkTestObj.executeTestCase(expectedResult);
    result =tdkTestObj.getResultDetails();
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print "Rebooted device successfully"

        print "STARTING THE SCRIPT TO DO REBOOT STRESS TEST\n"

        print "Get the count and status of plugins before starting the reboot test"
        tdkTestObj = obj.createTestStep('rdkservice_getNoOfPlugins');
        tdkTestObj.executeTestCase(expectedResult);
        NoofPluginsBeforeReboot = tdkTestObj.getResultDetails();
        if int(NoofPluginsBeforeReboot) > 0:
            tdkTestObj.setResultStatus("SUCCESS")
            print "Number of plugin before starting the reboot test:",NoofPluginsBeforeReboot

            tdkTestObj = obj.createTestStep('rdkservice_getAllPluginStatus');
            tdkTestObj.executeTestCase(expectedResult);
            PluginStatusBeforeReboot = tdkTestObj.getResultDetails();

            if PluginStatusBeforeReboot:
                tdkTestObj.setResultStatus("SUCCESS")
                print "Status of plugins before reboot\n", PluginStatusBeforeReboot

                for count in range(repeatCount):
                    iter_no = "ITER_No_%d"%(count+1)
                    rebootTestUtility.iter_no = iter_no
                    rebootTestUtility.count = count
                    print "------------------------------------------------------------"
                    print "ITER_No_%d"%(count+1)
                    print "------------------------------------------------------------"

                    #REBOOT THE DEVICE
                    tdkTestObj = obj.createTestStep('rdkservice_rebootDevice');
                    tdkTestObj.addParameter("waitTime",rebootwaitTime);
                    tdkTestObj.executeTestCase(expectedResult);
                    result =tdkTestObj.getResultDetails();
                    if expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print "Rebooted device successfully"

                        #GET THE UPTIME AFTER REBOOT"
                        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                        tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo");
                        tdkTestObj.addParameter("reqValue","uptime");
                        tdkTestObj.executeTestCase(expectedResult);
                        uptime_after = tdkTestObj.getResultDetails();
                        uptime_status = validateUptime(uptime_after,ValidateUptime)
                        if uptime_status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")

                        #GET THE NUMBER OF PLUGINS AFTER REBOOT
                        tdkTestObj = obj.createTestStep('rdkservice_getNoOfPlugins');
                        tdkTestObj.executeTestCase(expectedResult);
                        NoofPluginsAfterReboot = tdkTestObj.getResultDetails();
                        no_of_plugins = validateNoOfPlugins(NoofPluginsBeforeReboot,NoofPluginsAfterReboot,ValidateNoOfPlugins);
                        if no_of_plugins == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")

                        #GET THE STATUS OF PLUGINS AFTER REBOOT
                        tdkTestObj = obj.createTestStep('rdkservice_getAllPluginStatus');
                        tdkTestObj.executeTestCase(expectedResult);
                        PluginStatusAfterReboot = tdkTestObj.getResultDetails();
                        plugin_status = validatePluginStatus(PluginStatusBeforeReboot,PluginStatusAfterReboot,ValidatePluginStatus)
                        if plugin_status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")

			#GET THE STATUS OF ETHERNET INTERFACE
                        if_status = getIFStatus(EthernetInterface,ValidateInterface)
                        if if_status == "ENABLED":
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")

                        #CHECK THE CONTROLLER UI STATUS
                        ui_status = getUIStatus(ValidateControllerUI);
                        if ui_status == "ACCESSIBLE":
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")

                        if uptime_status == "SUCCESS":
                            print "->UPTIME : SUCCESS, Current uptime is less than 200 seconds";
                        else:
                            print "->UPTIME : FAILURE, Current uptime is greater than 200 seconds";
                        print "->INTERFACE : " + if_status
                        print "->CONTROLLER UI : "+ ui_status
                        print "->No. OF PLUGINS : "+ no_of_plugins
                        print "->PLUGIN STATUS : "+ plugin_status

                        time.sleep(10);
                        count = count +1
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print "Failed to reboot the device"
                getSummary(count);
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "Failed to get the plugin status before reboot"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Failed to get the number of plugins before reboot"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "Failed to reboot the device"
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
