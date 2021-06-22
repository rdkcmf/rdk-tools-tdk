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
  <version>2</version>
  <name>RDKV_CERT_RVS_ScreenResolution</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getCPULoad</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to set screen resolution to different sizes and validate using screenshots</synopsis>
  <groups_id/>
  <execution_time>720</execution_time>
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
    <test_case_id>RDKV_STABILITY_13</test_case_id>
    <test_objective>The objective of this test is to set screen resolution to different sizes and validate whether resolutions are set, also validate CPU load and memory usage of each iteration.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. If screen capture validation is needed configure CGI server and make sure DUT has support
2. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>resolutions_list: list
</input_parameters>
    <automation_approch>1. As a prerequisite disable Cobalt and enable DeviceInfo, if screen capture validation is needed enable screen capture also.
2. Launch WebKit with test app URL
3. Change the resolution in a for loop and verify whether resolution is changed in each iteration.
4. If screen capture validation is opted compare the images of each resolution in one iteration.
5. Validate CPU load and memory usage of each iteration.
6. Revert the plugins</automation_approch>
    <expected_output>The set and get resolution should be success
The images of different resolutions should be different.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_ScreenResolution</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from StabilityTestUtility import *
from rdkv_stabilitylib import *
import StabilityTestVariables
from rdkv_performancelib import *
import StabilityTestVariables
import os.path
import os


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_ScreenResolution');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
webkit_url = obj.url+'/fileStore/tdkvSampleScripts/ScreenResolutionTest.html'
change_resolution_max_count = StabilityTestVariables.change_resolution_max_count

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    revert_webkit = False
    current_url = ""
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict["WebKitBrowser"] in "resumed":
        revert_webkit = True
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        changed_plugins_status_dict = get_plugins_status(obj,plugins_list)
        if changed_plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    webkit_status,start_time = launch_plugin(obj,"WebKitBrowser")
    time.sleep(10)
    conf_file,file_status = getConfigFileName(obj.realpath)
    sc_config_status,screenshot_validation = getDeviceConfigKeyValue(conf_file,"SC_VALIDATION_NEEDED")
    if screenshot_validation == "":
        print "\n Please configure SC_VALIDATION_NEEDED variable in Device configuration file \n"
    elif screenshot_validation == "YES":
        #Get Screen capture plugin status
        plugin = "org.rdk.ScreenCapture"
        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
        tdkTestObj.addParameter("plugin",plugin);
        tdkTestObj.executeTestCase(expectedResult);
        sc_result = tdkTestObj.getResult();
        sc_status = tdkTestObj.getResultDetails();
        if expectedResult in sc_result:
            tdkTestObj.setResultStatus("SUCCESS")
            if sc_status not in "activated":
                curr_plugins_status_dict["org.rdk.ScreenCapture"] = "deactivated"
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
                tdkTestObj.addParameter("plugin",plugin);
                tdkTestObj.addParameter("status","activate");
                tdkTestObj.executeTestCase(expectedResult);
                result1 = tdkTestObj.getResult();
                if expectedResult in result1:
                    print "\n org.rdk.ScreenCapture is activated \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    status = "FAILURE"
                    print "\n Error while activating org.rdk.ScreenCapture\n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
               print"org.rdk.ScreenCapture is in activated state"
        else:
            print "\n Error while getting org.rdk.ScreenCapture status"
            tdkTestObj.setResultStatus("FAILURE")
            status = "FAILURE"
        upload_url_status,sc_upload_url = getDeviceConfigKeyValue(conf_file,"SC_UPLOAD_URL")
        image_upload_dir = StabilityTestVariables.image_upload_dir
        if sc_upload_url == "" or image_upload_dir == "":
            print "\n Please configure SC_UPLOAD_URL in Device configuration file and configure image_upload_dir in StabilityTestVariables file\n"
            status = "FAILURE"
    else:
        print "\n User opted for NO screen capture validation"
    if all(status_val == "SUCCESS" for status_val in (status,webkit_status,sc_config_status)) :
        image_files = []
        resolutions_list = StabilityTestVariables.resolutions_list
        print "\nPre conditions for the test are set successfully"
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",webkit_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in  result:
                time.sleep(20)
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if webkit_url in new_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    print "\n Get the current screen resolution \n"
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getScreenResolution");
                    tdkTestObj.executeTestCase(expectedResult);
                    curr_resolution = tdkTestObj.getResultDetails();
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        curr_resolution_dict = eval(curr_resolution)
                        curr_resolution_dict.pop('success')
                        print "Current resolution",curr_resolution_dict
                        proceed = True
                        if screenshot_validation.upper() == "YES":
                            base_image_name = str(obj.execID)+'BaseImage.png'
                            params = '{"url":"'+sc_upload_url+'?filename='+base_image_name+'"}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                            tdkTestObj.addParameter("method","org.rdk.ScreenCapture.1.uploadScreenCapture");
                            tdkTestObj.addParameter("value",params);
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult();
                            if expectedResult in  result:
                                time.sleep(5)
                                base_file_name = image_upload_dir+'/'+base_image_name
                                if os.path.exists(base_file_name):
                                    print "Image uploaded successfully"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "Image upload is not working"
                                    proceed = False
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while executing org.rdk.ScreenCapture.1.uploadScreenCapture method\n"
                                proceed = False
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Screen capture validation is skipped \n"
                        if proceed:
                            if curr_resolution_dict in resolutions_list:
                                resolutions_list.remove(curr_resolution_dict)
                            else:
                                resolutions_list.pop()
                            error_in_loop = False
                            for count in range(0,change_resolution_max_count):
                                print "\n########## Iteration :{} ##########\n".format(count+1)
                                if screenshot_validation.upper() == "YES":
                                    image_files = [base_file_name]
                                result_dict = {}
                                for resolution in resolutions_list:
                                    params = '{"w":'+str(resolution['w'])+',"h":'+str(resolution['h'])+'}'
                                    print "\n Setting Resolution {}x{} \n".format(resolution['w'],resolution['h'])
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.setScreenResolution");
                                    tdkTestObj.addParameter("value",params);
                                    tdkTestObj.executeTestCase(expectedResult);
                                    result = tdkTestObj.getResult();
                                    if expectedResult in  result:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        time.sleep(10)
                                        print "\n Validate resolution \n"
                                        tdkTestObj = obj.createTestStep('rdkservice_getValue');
                                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getScreenResolution");
                                        tdkTestObj.executeTestCase(expectedResult);
                                        resolution_details = tdkTestObj.getResultDetails();
                                        result = tdkTestObj.getResult()
                                        if expectedResult in result:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print "\n Resolution details",resolution_details
                                            resolution_dict = eval(resolution_details)
                                            resolution_dict.pop('success')
                                            if resolution_dict == resolution :
                                                print "\n Set and Get resolutions are same \n"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                if screenshot_validation.upper() == "YES":
                                                    image_name = str(obj.execID)+'test_image'+str(resolution['w'])+'x'+str(resolution['h'])+'.png'
                                                    print image_name
                                                    params = '{"url":"'+sc_upload_url+'?filename='+image_name+'"}'
                                                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                                                    tdkTestObj.addParameter("method","org.rdk.ScreenCapture.1.uploadScreenCapture");
                                                    tdkTestObj.addParameter("value",params);
                                                    tdkTestObj.executeTestCase(expectedResult);
                                                    result = tdkTestObj.getResult();
                                                    if expectedResult in  result:
                                                        time.sleep(5)
                                                        file_name = image_upload_dir+'/'+image_name
                                                        if os.path.exists(file_name):
                                                            image_files.append(file_name)
                                                            print "\n Image uploaded successfully \n"
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                        else:
                                                            print "\n Image upload is not working \n"
                                                            error_in_loop = True
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            break
                                                    else:
                                                        print "\n Error while executing org.rdk.ScreenCapture.1.uploadScreenCapture method\n"
                                                        error_in_loop = True
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                            else:
                                                print "\n Both resolutions are not same, current resolution :",resolution_dict
                                                tdkTestObj.setResultStatus("FAILURE")
                                                error_in_loop = True
                                                break
                                        else:
                                            print "\n Failed to get the resolution details \n"
                                            tdkTestObj.setResultStatus("FAILURE");
                                            error_in_loop = True
                                            break
                                    else:
                                        print "\n Unable to set resolution using org.rdk.RDKShell.1.setScreenResolution \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                        error_in_loop = True
                                        break
                                # Exit from outer loop if any issue in inner-loop
                                if error_in_loop:
                                    break
                                
                                if screenshot_validation.upper() == "YES":
                                    comparison_result = compare_images(image_files)
                                    if comparison_result == "DIFFERENT":
                                        print "\n Resolutions are set properly \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n[ERROR] Resolutions are not set properly \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                    for image in image_files:
                                        if image not in base_file_name:
                                            os.remove(image)
                                print "\n ##### Validating CPU load and memory usage #####\n"
				print "Iteration : ", count+1
            			tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            			tdkTestObj.executeTestCase(expectedResult)
            			status = tdkTestObj.getResult()
            			result = tdkTestObj.getResultDetails()
            			if expectedResult in status and result != "ERROR":
            			    tdkTestObj.setResultStatus("SUCCESS")
            			    cpuload = result.split(',')[0]
            			    memory_usage = result.split(',')[1]
                                    result_dict["iteration"] = count+1
                                    result_dict["cpu_load"] = float(cpuload)
                                    result_dict["memory_usage"] = float(memory_usage)
                                    result_dict_list.append(result_dict)
				else:
				    print "\n Error while validating Resource usage"
                		    tdkTestObj.setResultStatus("FAILURE")
                		    break
                            else:
                                print "\nSuccessfully completed the {} iterations \n".format(change_resolution_max_count)
                            cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                            json.dump(cpu_mem_info_dict,json_file)
                            json_file.close()

                            # Delete the image files if exist
                            if image_files:
                                for image in image_files:
                                    if os.path.exists(image):
                                        os.remove(image)
                        else:
                            print "\n Error while uploading the image \n"
                        print "Revert the resolution"
                        params = '{"w":'+str(curr_resolution_dict['w'])+',"h":'+str(curr_resolution_dict['h'])+'}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.setScreenResolution");
                        tdkTestObj.addParameter("value",params);
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult();
                        if expectedResult in  result:
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "Unable to revert the resolution"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Failed to get the resolution details \n"
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "\n Unable to set URL : {} in WebKitBrowser, Current URL :{} \n".format(webkit_url,new_url)
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while setting URL in WebKitBrowser \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Unable to get the Current URL in WebKitBrowser \n"
            tdkTestObj.setResultStatus("FAILURE")
        print "\n Exiting from WebKitBrowser \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","WebKitBrowser")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate WebKitBrowser"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
        if revert_webkit:
            #Set the URL back to previous
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",current_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if result == "SUCCESS":
                print "URL is reverted successfully"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "Failed to revert the URL"
                tdkTestObj.setResultStatus("FAILURE");
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
