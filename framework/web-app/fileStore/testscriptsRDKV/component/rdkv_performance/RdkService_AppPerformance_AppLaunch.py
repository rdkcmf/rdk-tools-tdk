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
  <version>1</version>
  <name>RdkService_AppPerformance_AppLaunch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script is to get the time taken to launch the lightning application with webkit</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_02</test_case_id>
    <test_objective>This script is to get the time taken to launch the lightning application with webkit</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Test Manager time should be in sync with UTC time.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.
</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable webkitbrowser plugin.
2. Set the application URL in webkitbrowser
3. Get the time taken to load the application</automation_approch>
    <expected_output>The application should launch within 60 seconds.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RdkService_AppPerformance_AppLaunch</test_script>
    <skipped>No</skipped>
    <release_version>M82</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
from web_socket_util import *
import MediaValidationVariables
from MediaValidationUtility import *
import MediaValidationUtility
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_AppPerformance_AppLaunch');

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    appURL    = MediaValidationVariables.lightning_video_test_app_url
    videoURL  = MediaValidationVariables.video_src_url

    setOperation("close",5)
    operations = getOperations()
    video_test_url = getTestURL(appURL,videoURL,operations)

    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_ux_status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        set_pre_requisites(obj)
        #Need to revert the values since we are changing plugin status
        revert="YES"
        status,ux_status,webkit_status,cobalt_status = check_pre_requisites(obj)
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        if current_url != None:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,MediaValidationVariables.webinspect_port,[],"/devtools/page/1",False)
            time.sleep(10)
            print "Current URL:",current_url
            print "\nSet Lightning Application URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",video_test_url);
	    start_time = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            new_url = tdkTestObj.getResultDetails();
            if new_url in video_test_url:
                tdkTestObj.setResultStatus("SUCCESS");
                print "URL(",new_url,") is set successfully"
                continue_count = 0
                test_result = ""
                while True:
                    if continue_count > 60:
                        print "app not launched in 60 seconds"
                        break
                    if (len(webkit_console_socket.getEventsBuffer())== 0):
                        time.sleep(1)
                        continue_count += 1
                        continue
                    console_log = webkit_console_socket.getEventsBuffer().pop(0)
                    if "URL Info:" in console_log or "Connection refused" in console_log:
                        test_result = getConsoleMessage(console_log)
                        break;
                webkit_console_socket.disconnect()
                if "URL Info:" in test_result:
                    micosec_frm_start_time = int(start_time.split(".")[-1])
                    start_time = start_time.replace(start_time.split(".")[-1],"")
                    start_time = start_time.replace(".",":")
                    start_time = start_time + str(micosec_frm_start_time/1000)
                    print "\nApplication URL set in webkit browser at :{} (UTC)".format(start_time)
                    start_time_millisec = getTimeInMilliSeconds(start_time)
                    end_time = getTimeFromMsg(test_result)
                    print "\nApplication launched at: {} (UTC)".format(end_time)
                    end_time_millisec = getTimeInMilliSeconds(end_time)
                    app_launch_time = end_time_millisec - start_time_millisec
                    print "\nTime taken to launch the application: {} milliseconds \n".format(app_launch_time)
                    conf_file,result = getConfigFileName(tdkTestObj.realpath)
                    result, app_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"APP_LAUNCH_THRESHOLD VALUE")
                    if result == "SUCCESS":
                        if int(app_launch_time) < int(app_launch_threshold_value):
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "\n The time taken to launch the app is within the expected limit\n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "\n The time taken to launch the app is greater than the expected limit \n"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get the threshold value from config file"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "error occured during application launch"
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
            else:
                print "Failed to load the URL %s" %(new_url)
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_ux_status,curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

