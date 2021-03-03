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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Cobalt_VideoPlayback_StandbyToOn</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to put STB in to StandBy when YouTube video is playing and resume from standby for given number of times</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3000</execution_time>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_18</test_case_id>
    <test_objective>The objective of this test is to put STB in to StandBy when YouTube video is playing and resume from standby for given number of times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>wpeframework process should be up and running in DUT.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>max_power_state_changes : integer
cobalt_test_url : string</input_parameters>
    <automation_approch> 1. Launch YouTube and play a video.
In a loop of minimum 1000 times:
2. Set and get preferred Standby mode to LIGHTSLEEP
3. Set device to standby mode
4. Set device to ON state
5. Verify if the video playback is happening. 
6. Validate CPU load and memory usage
7. Revert everything.</automation_approch>
    <expected_output>Video must be playing even after setting power state from StandBy to ON.
CPU load and memory usage must be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_VideoPlayback_StandbyToOn</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_VideoPlayback_StandbyToOn');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
max_powerstate_changes = StabilityTestVariables.max_power_state_changes

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    cobalt_test_url = StabilityTestVariables.cobalt_test_url;
    print "Check Pre conditions"
    if cobalt_test_url == "":
        print "\n Please configure the cobalt_test_url value\n"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    conf_file,result = getConfigFileName(obj.realpath)
    result, ssh_required = getDeviceConfigKeyValue(conf_file,"SSH_VALIDATION")
    if ssh_required.upper() == "YES":
        tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
        tdkTestObj.addParameter("realpath",obj.realpath)
        tdkTestObj.addParameter("deviceIP",obj.IP)
        tdkTestObj.executeTestCase(expectedResult)
        ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
        result = tdkTestObj.getResult()
        if expectedResult in result and ssh_param_dict != {}:
            tdkTestObj.setResultStatus("SUCCESS")
            if ssh_param_dict["ssh_method"] == "directSSH":
                if ssh_param_dict["password"] == "None":
                    password = ""
                else:
                    password = ssh_param_dict["password"]
                ssh_credentials = ssh_param_dict["host_name"]+','+ssh_param_dict["user_name"]+','+password
            else:
                #TODO
                print "selected ssh method is {}".format(ssh_param_dict["ssh_method"])
                pass
        else:
            tdkTestObj.setResultStatus("FAILURE")
            status = "FAILURE"
    if status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "" and ssh_required != "":
        print "\nPre conditions for the test are set successfully \n"
        if validation_dict["validation_required"]:
            if validation_dict["validation_method"] == "proc_entry":
                if validation_dict["ssh_method"] == "directSSH":
                    if ssh_required.upper() == "YES":
                        credentials = ssh_credentials
                    else:
                        if validation_dict["password"] == "None":
                            password = ""
                        else:
                            password = validation_dict["password"]
                        credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                else:
                    #TODO
                    print "selected ssh method is {}".format(validation_dict["ssh_method"])
                    pass
            else:
                print "\n Validation method other than proc_entry is currently not supported \n"
                validation_dict["validation_required"] = False
        print "\n Get the current power state: \n"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
        tdkTestObj.addParameter("reqValue","powerState")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        current_power_state = initial_power_state = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "Get the current Preferred Standby Mode \n"
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
            tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
            tdkTestObj.addParameter("reqValue","preferredStandbyMode")
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            initial_preferred_standby = preferred_standby = tdkTestObj.getResultDetails()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                cobal_launch_status = launch_cobalt(obj)
                time.sleep(30)
                if cobal_launch_status == "SUCCESS":
                    print "\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url)
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
                        #Skip if Ad is playing by pressing OK
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result2 = tdkTestObj.getResult()
                        time.sleep(60)
                        if "SUCCESS" == (result1 and result2):
                            result_val = ""
                            tdkTestObj.setResultStatus("SUCCESS")
                            if validation_dict["validation_required"]:
                                tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                tdkTestObj.addParameter("credentials",credentials)
                                tdkTestObj.addParameter("procfile",validation_dict["validation_file"])
                                tdkTestObj.addParameter("mincdb",validation_dict["min_cdb"])
                                tdkTestObj.executeTestCase(expectedResult)
                                result_val = tdkTestObj.getResultDetails()
                                if result_val == "SUCCESS" :
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\nVideo playback is happening\n"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print "\n Video playback is not happening \n"
                            else:
                                print "\n Video validation is skipped \n "
                            if result_val == "SUCCESS" or not validation_dict["validation_required"]:
                                for count in range(0,max_powerstate_changes):
                                    print "\n********************ITERATION: {} ********************\n".format(count+1)
                                    print "\n Set Preferred standby mode as LIGHT_SLEEP \n"
                                    params = '{"standbyMode":"LIGHT_SLEEP"}'
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                                    tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
                                    tdkTestObj.addParameter("value",params)
                                    tdkTestObj.executeTestCase(expectedResult);
                                    result = tdkTestObj.getResult();
                                    if expectedResult in result:
                                        print "\n Setting Preferred Standby Mode is success \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "Get the Preferred Standby Mode \n"
                                        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                                        tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
                                        tdkTestObj.addParameter("reqValue","preferredStandbyMode")
                                        tdkTestObj.executeTestCase(expectedResult);
                                        result = tdkTestObj.getResult();
                                        preferred_standby = tdkTestObj.getResultDetails()
                                        if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
                                            print "\n Preferred standby mode is LIGHT_SLEEP \n"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            if current_power_state in ("STANDBY","DEEP_SLEEP","LIGHT_SLEEP"):
                                                new_power_state = "ON"
                                            else:
                                                new_power_state = "STANDBY"
                                            params = '{"powerState":"'+new_power_state+'", "standbyReason":"APIUnitTest"}'
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                                            tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                                            tdkTestObj.addParameter("value",params);
                                            tdkTestObj.executeTestCase(expectedResult);
                                            result = tdkTestObj.getResult();
                                            if expectedResult in result:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                time.sleep(10)
                                                print "\n Verify the Power state \n"
                                                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                                                tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                                                tdkTestObj.addParameter("reqValue","powerState")
                                                tdkTestObj.executeTestCase(expectedResult)
                                                result = tdkTestObj.getResult()
                                                current_power_state = tdkTestObj.getResultDetails()
                                                if expectedResult in result and current_power_state == new_power_state:
                                                    print "\n Successfully set power state to : {}\n".format(new_power_state)
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    if ssh_required.upper() == "YES":
                                                        #validate power statechange using wpeframework log
                                                        command = 'cat /opt/logs/wpeframework.log | grep -inr "onSystemPowerStateChanged.*power state changed to.*" |  tail -1'
                                                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                                        tdkTestObj.addParameter("credentials",ssh_credentials)
                                                        tdkTestObj.addParameter("command",command)
                                                        tdkTestObj.executeTestCase(expectedResult)
                                                        result = tdkTestObj.getResult()
                                                        output = tdkTestObj.getResultDetails()
                                                        if output != "EXCEPTION" and expectedResult in result and current_power_state in output:
                                                            print "\n Log from wpeframework.log ",output.split("onSystemPowerStateChanged")[-1],"\n"
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                        else:
                                                            print "\n Power state change related event prints are not available in wpeframework log \n"
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            break
                                                    else:
                                                        print "\n Validation using wpeframework.log file is skipped \n"
                                                    if current_power_state == "ON":
                                                        if validation_dict["validation_required"]:
                                                            time.sleep(20)
                                                            tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                                            tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                                            tdkTestObj.addParameter("credentials",credentials)
                                                            tdkTestObj.addParameter("procfile",validation_dict["validation_file"])
                                                            tdkTestObj.addParameter("mincdb",validation_dict["min_cdb"])
                                                            tdkTestObj.executeTestCase(expectedResult)
                                                            result_val = tdkTestObj.getResultDetails()
                                                            if result_val == "SUCCESS" :
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print "\nVideo playback is happening\n"
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                print "\n Video playback is not happening \n"
                                                                break
                                                        else:
                                                            print "\n Video validation is skipped \n"
                                                    result_dict = {}
                                                    #get the cpu load
                                                    tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                                                    tdkTestObj.executeTestCase(expectedResult)
                                                    result = tdkTestObj.getResult()
                                                    cpuload = tdkTestObj.getResultDetails()
                                                    if result == "SUCCESS":
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        #validate the cpuload
                                                        tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                                        tdkTestObj.addParameter('value',float(cpuload))
                                                        tdkTestObj.addParameter('threshold',90.0)
                                                        tdkTestObj.executeTestCase(expectedResult)
                                                        result = tdkTestObj.getResult()
                                                        is_high_cpuload = tdkTestObj.getResultDetails()
                                                        if is_high_cpuload == "YES"  or expectedResult not in result:
                                                            print "\n CPU load is high :{}% after :{} times\n".format(cpuload,count+1)
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            break
                                                        else:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print "\n CPU load: {}% after {} times\n".format(cpuload,count+1)
                                                    else:
                                                        print "Unable to get cpuload"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                                    #get the memory usage
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
                                                        result = tdkTestObj.getResult()
                                                        is_high_memory_usage = tdkTestObj.getResultDetails()
                                                        if is_high_memory_usage == "YES" or expectedResult not in result:
                                                            print "\n Memory usage is high :{}% after {} times\n".format(memory_usage,count+1)
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            break
                                                        else:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print "\n Memory usage is {}% after {} times\n".format(memory_usage,count+1)
                                                    else:
                                                        print "\n Unable to get the memory usage\n"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                                    result_dict["iteration"] = count+1
                                                    result_dict["cpu_load"] = float(cpuload)
                                                    result_dict["memory_usage"] = float(memory_usage)
                                                    result_dict_list.append(result_dict)
                                                else:
                                                    print "\n Unable to set the powerstate to : {}, current power state:{}\n".format(new_power_state,current_power_state)
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    break
                                            else:
                                                print "\n Error while executing org.rdk.System.1.setPowerState method \n"
                                                tdkTestObj.setResultStatus("FAILURE")
                                                break
                                        else:
                                            print "\n Error while setting Preferred Standby Mode to LIGHT_SLEEP \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                    else:
                                        print "\n Error while executing org.rdk.System.1.setPreferredStandbyMode method \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    print "\n Successfully completed {} iterations \n".format(max_powerstate_changes)
                                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                                json.dump(cpu_mem_info_dict,json_file)
                                json_file.close()
                            else:
                                print "\n Error while playing Video \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error while pressing OK key \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while setting URL in Cobalt using Deeplink method\n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while lauching Cobalt \n"
                    tdkTestObj.setResultStatus("FAILURE")
                #Exiting from Cobalt
                print "\n Exit from Cobalt \n"
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
                #Revert preferred standby mode
                if initial_preferred_standby != preferred_standby:
                    print "\n Reverting the Preferred Standby mode \n"
                    params = '{"standbyMode":"'+initial_preferred_standby+'"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if expectedResult in result:
                        print "\n setPreferredStandbyMode is success \n"
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "\n Error while setting PreferredStandbyMode\n"
                        tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to get the Preferred StandBy mode \n"
                tdkTestObj.setResultStatus("FAILURE")
            #Revert power state
            if current_power_state != initial_power_state:
                print "Reverting the Power state \n"
                print "\n Set power state to {} \n".format(initial_power_state)
                params = '{"powerState":"'+initial_power_state+'", "standbyReason":"APIUnitTest"}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState");
                tdkTestObj.addParameter("value",params);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    print "Reverted the power state to {}\n".format(initial_power_state)
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n Error while reverting the power state to {}\n".format(initial_power_state)
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to get Power state of DUT \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
