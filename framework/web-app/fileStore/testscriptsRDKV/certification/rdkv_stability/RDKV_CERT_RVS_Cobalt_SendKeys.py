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
  <version>4</version>
  <name>RDKV_CERT_RVS_Cobalt_SendKeys</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this script is to send random keys to Cobalt for given time and checks if Cobalt is still working.</synopsis>
  <groups_id/>
  <execution_time>620</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_06</test_case_id>
    <test_objective>The objective of this script is to send random keys to Cobalt for given time and checks if Cobalt is still working.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be running in DUT.
2. TV must be connected to the DUT. </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_randomkey_test_url: string
cobalt_randomkey_test_duration : int</input_parameters>
    <automation_approch>1. As a prerequisite disable all other plugins and enable Cobalt and DeviceInfo plugins.
2. Load a video URL in Cobalt which has greater duration than the test duration.
3. Send random keys in every 5 seconds to DUT using RDKShell plugin.
4. Validate video playback using proc entries.
5. Validate CPU load and memory usage 
6.. Revert all values before exiting.</automation_approch>
    <expected_output>Video must be playing even after sending random keys. CPU load and memory usage must be in expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_SendKeys</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
import rdkv_performancelib
import StabilityTestVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_SendKeys');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
test_interval = 5


#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    cobalt_test_url = StabilityTestVariables.cobalt_randomkey_test_url;
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    cobal_launch_status = launch_cobalt(obj)
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and cobal_launch_status == "SUCCESS" and validation_dict != {} :
        print "\nPre conditions for the test are set successfully"
        time.sleep(30)
        print "\n Set the URL : {} using Cobalt deeplink method".format(cobalt_test_url)
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","Cobalt.1.deeplink")
        tdkTestObj.addParameter("value",cobalt_test_url)
        tdkTestObj.executeTestCase(expectedResult)
        cobalt_result = tdkTestObj.getResult()
        time.sleep(10)
        if(cobalt_result == expectedResult):
            tdkTestObj.setResultStatus("SUCCESS")
            print "Clicking OK to play video"
            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            result1 = tdkTestObj.getResult()
            time.sleep(40)
            #Click OK to skip Ad
            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            result2 = tdkTestObj.getResult()
            time.sleep(50)
            if "SUCCESS" == (result1 and result2):
                tdkTestObj.setResultStatus("SUCCESS")
                test_time_in_mins = int(StabilityTestVariables.cobalt_randomkey_test_duration)
                test_time_in_millisec = test_time_in_mins * 60 * 1000
                time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                iteration = 0
                completed = True
                while int(round(time.time() * 1000)) < time_limit:
                    print "Sending random keys to Cobalt"
                    params = '{"keys":[ {"keyCode": 37,"modifiers": [],"delay":2.0},{"keyCode": 38,"modifiers": [],"delay":2.0},{"keyCode": 39,"modifiers": [],"delay":2.0},{"keyCode": 40,"modifiers": [],"delay":2.0}]}' 
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "Sending random keys to Cobalt plugin is not working"
                        tdkTestObj.setResultStatus("FAILURE")
                        completed = False
                        break
                    if validation_dict["validation_required"]:
                        if validation_dict["password"] == "None":
                            password = ""
                        else:
                            password = validation_dict["password"]
                        credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                        tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                        tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",credentials)
                        tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                        tdkTestObj.executeTestCase(expectedResult)
                        result_val = tdkTestObj.getResultDetails()
                        if result_val == "SUCCESS" :
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\nVideo playback is happening\n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print "Video playback is not happening"
                            completed =  False
                            break
                    result_dict = {}
                    iteration += 1
		    print "\n ##### Validating CPU load and memory usage #####\n"
            	    print "Iteration : ", iteration
            	    tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            	    tdkTestObj.executeTestCase(expectedResult)
            	    status = tdkTestObj.getResult()
            	    result = tdkTestObj.getResultDetails()
            	    if expectedResult in status and result != "ERROR":
            	        tdkTestObj.setResultStatus("SUCCESS")
            	        cpuload = result.split(',')[0]
            	        memory_usage = result.split(',')[1]
                        result_dict["iteration"] = iteration
                        result_dict["cpu_load"] = float(cpuload)
                        result_dict["memory_usage"] = float(memory_usage)
                        result_dict_list.append(result_dict)
		    else:
			completed = False
			print "\n Error while validating Resource usage"
                	tdkTestObj.setResultStatus("FAILURE")
                	break
                    time.sleep(test_interval)
                if(completed):
                    print "\nsuccessfully completed the {} times in {} minutes".format(iteration,test_time_in_mins)
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
            else:
                print "Unable to press OK button"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Unable to launch the url"
            tdkTestObj.setResultStatus("FAILURE")
        #Close Cobalt
        print "\n Exiting from Cobalt \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
 
