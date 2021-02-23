##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
  <name>RDKV_CERT_RVS_WebKitBrowser_SetURL</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to stress load the system by setting the URL in a loop and validating CPU load and memory usage.</synopsis>
  <groups_id/>
  <execution_time>120</execution_time>
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
    <test_case_id>RDKV_STABILITY_09</test_case_id>
    <test_objective>The objective of this test is to stress load the system by setting the URL in a loop and validating CPU load and memory usage.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>test_url_1 
test_url_2
max_count</input_parameters>
    <automation_approch>1. As a prerequisite disable all plugins and enable WebKit and DeviceInfo plugins
2. Start a loop upto max_count value and inside the loop:
a) set test_url_1 in  WebKit and validate.
b) set test_url_2 in  WebKit and validate.
c) Validate cpu load and memory usage
3. Revert the plugins</automation_approch>
    <expected_output>URLs should be set and CPU load and memory usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_WebKitBrowser_SetURL</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import StabilityTestVariables
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_WebKitBrowser_SetURL');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}


#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    channel_change_url = StabilityTestVariables.channel_change_url
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    test_url_1 = StabilityTestVariables.loop_test_url_1
    test_url_2 = StabilityTestVariables.loop_test_url_2
    max_count = StabilityTestVariables.url_loop_count
    if status == "SUCCESS" and all(url != "" for url in (test_url_1,test_url_2)) :
	print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
	    for count in range(0,max_count):
		result_dict = {}
                print "\nSetting test URL 1"
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.addParameter("value",test_url_1);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
		if result == "SUCCESS":
		    tdkTestObj.setResultStatus("SUCCESS")
		    time.sleep(5)
                    print "\nValidate if the URL is set successfully or not"
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult()
                    new_url = tdkTestObj.getResultDetails();
                    if test_url_1 in new_url and expectedResult in result:
			print "URL :{} is set in WebKitBrowser".format(test_url_1)
		     	tdkTestObj.setResultStatus("SUCCESS");
			print "\nSetting test URL 2"
                        tdkTestObj = obj.createTestStep('rdkservice_setValue');
                        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                        tdkTestObj.addParameter("value",test_url_2);
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
			    tdkTestObj.setResultStatus("SUCCESS")
			    time.sleep(5)
                            print "\nValidate if the URL is set successfully or not"
                            tdkTestObj = obj.createTestStep('rdkservice_getValue');
                            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult()
                            new_url = tdkTestObj.getResultDetails();
                            if test_url_2 in new_url and expectedResult in result:
				print "URL :{} is set in WebKitBrowser".format(test_url_2)
                                tdkTestObj.setResultStatus("SUCCESS")
                                #Get the CPU Load
                                tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                cpuload = tdkTestObj.getResultDetails()
                                if (result == "SUCCESS"):
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    #validate the cpuload
                                    tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                    tdkTestObj.addParameter('value',float(cpuload))
                                    tdkTestObj.addParameter('threshold',90.0)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    is_high_cpuload = tdkTestObj.getResultDetails()
                                    if is_high_cpuload == "YES"  or expectedResult not in result:
                                        print "\n cpu load is high :{}% during iteration:{}".format(cpuload,count+1)
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                    else:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "\n cpu load is:{}% during iteration:{}\n".format(cpuload,count+1)
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print "\n Unable to get cpuload\n"
                                    break
                                tdkTestObj = obj.createTestStep('rdkservice_getMemoryUsage')
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                memory_usage = tdkTestObj.getResultDetails()
                                if (result == "SUCCESS"):
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    #validate memory usage
                                    tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
                                    tdkTestObj.addParameter('value',float(memory_usage))
                                    tdkTestObj.addParameter('threshold',90.0)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    is_high_memory_usage = tdkTestObj.getResultDetails()
                                    result = tdkTestObj.getResult()
                                    if is_high_memory_usage == "YES" or expectedResult not in result:
                                        print "\n memory usage is high :{}% during iteration: {}\n".format(memory_usage,count+1)
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                    else:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "\n memory usage is {}% during iteration: {}\n".format(memory_usage,count+1)
                                else:
                                    print "\n Unable to get the memory usage\n"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                result_dict["iteration"] = count+1
                                result_dict["cpu_load"] = float(cpuload)
                                result_dict["memory_usage"] = float(memory_usage)
                                result_dict_list.append(result_dict)
                            else:
                                print "\n Unable to set URL:{} current URL: {} ".format(test_url_2,new_url)
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Error while setting the URL:{} current URL: {} ".format(test_url_2,new_url)
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Unable to set URL:{} current URL: {} ".format(test_url_1,new_url)
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Error while setting the URL:{} current URL: {} ".format(test_url_1,new_url)
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "\n Successfully completed {} iterations \n".format(max_count)
            cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
            json.dump(cpu_mem_info_dict,json_file)
            json_file.close()
            #Set the URL back to previous
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",current_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if result == "SUCCESS":
                print "\n URL is reverted successfully"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "\n Failed to revert the URL"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "\n Unable to get the current URL loaded in webkit"
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE");
