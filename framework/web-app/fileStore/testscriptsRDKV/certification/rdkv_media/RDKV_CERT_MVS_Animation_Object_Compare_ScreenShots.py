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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_MVS_Animation_Object_Compare_ScreenShots</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to launch a lightning Objects Animation application to render a rectangle and validate animation operation using screen shot comparison</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_Media_Validation_42</test_case_id>
    <test_objective>Test Script to launch a lightning Objects Animation application to render a rectangle and validate animation operation using screen shot comparison</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Animation app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning Animation App URL: string
thunder_port :string
animation_duration:int
image_upload_dir:string
sc_upload_url:string</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the Animation app url with the input parameters
4. App performs animation to render single rectangle object for provided duration.
5. Using screenshot plugin, capture screenshots  at regular interval and upload to the configured url
6. compare the captured screenshots among them and check whether they are same or different
7.If the screenshots are different, then its because of animation which moves the object. If the screenshots matches, then object is not animated properly. update the test result as SUCCESS, if screenshots are different or else FAILURE if screenshots matches.
8. Revert all values</automation_approch>
    <expected_output>Animation should happen, screenshots should be captured and uploaded and screenshots comparison should result different.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Animation_Object_Compare_ScreenShots</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
from rdkv_performancelib import *
from rdkv_stabilitylib import *
import MediaValidationVariables
from MediaValidationUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Animation_Object_Compare_ScreenShots')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\nCheck Pre conditions..."
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    # Setting the pre-requites for media test. Launching the wekit browser via RDKShell and
    # moving it to the front, openning a socket connection to the webkit inspect page and
    # disabling proc validation
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,False)

    #No need to revert any values if the pre conditions are already set.
    sc_revert="NO"
    #Check Screencapture plugin status and activate if its deactivated
    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
    tdkTestObj.addParameter("plugin","org.rdk.ScreenCapture");
    tdkTestObj.executeTestCase(expectedResult);
    sc_result = tdkTestObj.getResult();
    sc_status = tdkTestObj.getResultDetails();
    if expectedResult in sc_result:
        tdkTestObj.setResultStatus("SUCCESS")
        if sc_status not in "activated":
            curr_sc_status = "deactivate"
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
            tdkTestObj.addParameter("plugin","org.rdk.ScreenCapture");
            tdkTestObj.addParameter("status","activate");
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                sc_revert = "YES"
                sc_status = "activated"
                print "\nScreenCapture plugin is activated\n"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                sc_result = "FAILURE"
                print "\nError while activating ScreenCapture plugin\n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
               print "\nScreenCapture plugin is in activated state"
    else:
        print "\n Error while getting ScreenCapture plugin status"
        tdkTestObj.setResultStatus("FAILURE")


    #Reading the SC uplaod info from the device config file
    config_status = "SUCCESS"
    conf_file,result = getDeviceConfigFile(obj.realpath)
    upload_url_status,sc_upload_url = readDeviceConfigKeyValue(conf_file,"SC_UPLOAD_URL")
    image_upload_dir = MediaValidationVariables.image_upload_dir
    if sc_upload_url == "" or image_upload_dir == "":
        config_status = "FAILURE"
        print "Please configure upload url & dir required for screenshots\n"

    if pre_requisite_status== "SUCCESS" and config_status == "SUCCESS" and "SUCCESS" in sc_result:
        tdkTestObj.setResultStatus("SUCCESS");
        print "\nPre conditions for the test are set successfully";

        print "\nSet Lightning animation test app url..."
        #Setting device config file
        conf_file,result = getDeviceConfigFile(obj.realpath)
        setDeviceConfigFile(conf_file)
        appURL    = MediaValidationVariables.lightning_objects_animation_test_app_url
        # Setting Animation test app URL arguments
        setURLArgument("ip",ip)
        setURLArgument("port",MediaValidationVariables.thunder_port)
        setURLArgument("object","Rect")
        setURLArgument("showfps","false")
        setURLArgument("count","1")
        setURLArgument("duration","180")
        setURLArgument("autotest","true")
        appArguments = getURLArguments()
        # Getting the complete test app URL
        animation_test_url = getTestURL(appURL,appArguments)

        # Setting the animation test url in webkit browser using RDKShell
        launch_status = launchPlugin(obj,"WebKitBrowser",animation_test_url)
        if "SUCCESS" in launch_status:
            time.sleep(15)
            sc_images_list    = []
            sc_capture_status = "SUCCESS"
            for count in range(0,5):
                image_name = str(obj.execID)+'_screen_'+str(count+1)+'.png'
                print "\n########## Iteration :%d ##########\n" %((count+1))
                params = '{"url":"'+sc_upload_url+'?filename='+image_name+'"}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","org.rdk.ScreenCapture.1.uploadScreenCapture");
                tdkTestObj.addParameter("value",params);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    time.sleep(15)
                    base_file_name = image_upload_dir+'/'+image_name
                    if os.path.exists(base_file_name):
                        sc_images_list.append(base_file_name)
                        print "Image %s uploaded successfully" %(image_name)
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        sc_capture_status = "FAILURE"
                        print "Image %s upload is not working" %(image_name)
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    sc_capture_status = "FAILURE"
                    print "\n Error while executing uploadScreenCapture method\n"
                    tdkTestObj.setResultStatus("FAILURE")
                    break

            tdkTestObj = obj.createTestStep('rdkv_media_test');
            tdkTestObj.executeTestCase(expectedResult);
            if sc_capture_status == "SUCCESS":
                comparison_result = compare_images(sc_images_list)
                if comparison_result == "DIFFERENT":
                    print "\n All the captured images are different"
                    print "Object Animation is validated using screenshot comparison successfully\n"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\nCaptured images are not different"
                    print "Object Animation did not happen as expected, screenshot comparison failed\n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
            # Remove the png files
            if sc_images_list:
                for image in sc_images_list:
                    if os.path.exists(image):
                        os.remove(image)

            print "\nSet post conditions..."
            tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
            tdkTestObj.executeTestCase(expectedResult);
            # Setting the post-requites for media test.Removing app utl from webkit browser and
            # moving residentApp to front if its active
            post_requisite_status = setMediaTestPostRequisites(obj)
            if post_requisite_status == "SUCCESS":
                print "Post conditions for the test are set successfully\n"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "Post conditions are not met\n"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to load the Animation Test URL in Webkit\n"
    else:
        print "Pre conditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE");
    #Revert the values
    if sc_revert=="YES":
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
        tdkTestObj.addParameter("plugin","org.rdk.ScreenCapture");
        tdkTestObj.addParameter("status",curr_sc_status);
        tdkTestObj.executeTestCase(expectedResult);
        if expectedResult in tdkTestObj.getResult():
            print "\nScreenCapture plugin status reverted"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\nFailed to revert ScreenCapture plugin status"
            tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
