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
  <name>RDKV_CERT_SVS_Check_WPASupplicant_File_For_WiFiPassword</name>
  <primitive_test_id/>
  <primitive_test_name>rdkvsecurity_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Checks whether WPA supplicant file contains wifi password</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_SECURITY_25</test_case_id>
    <test_objective>Checks whether WPA supplicant file contains wifi password</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>WiFi related configurations should be configured in the device configuration file available in fileStore/tdkvRDKServiceConfig/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Activates the Wfi and Network plugin
2. Connect the DUT to Wifi 
3.Checks whether WPA supplicant file contains wifi password
4.Pass/fail the test based on the availability of Wifi passwords in WPA_supplicant file and password excryption status
5. Disconnects from Wifi</automation_approch>
    <expected_output>WPA supplicant file should not contain wifi password if "encrypted_wifi_password_support" configured as "yes"</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_security</test_stub_interface>
    <test_script>RDKV_CERT_SVS_Check_WPASupplicant_File_For_WiFiPassword</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import time

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_security","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_SVS_Check_WPASupplicant_File_For_WiFiPassword');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result.upper());

expectedResult = "SUCCESS"
Plugin_List = ["org.rdk.Wifi","org.rdk.Network"]
if expectedResult in result.upper():
    for plugin in Plugin_List:
        tdkTestObj = obj.createTestStep('rdkvsecurity_getPluginStatus'); 
        tdkTestObj.addParameter("plugin",plugin)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult();
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            status = tdkTestObj.getResultDetails()
            print "\nCurrent status of {} plugin : {}\n".format(plugin,status)
            if status == "deactivated":
                print "Activating plugin %s" %(plugin)
                params = '{"callsign":"'+plugin+'"}'
                tdkTestObj = obj.createTestStep('rdkvsecurity_setValue')
                tdkTestObj.addParameter("method","Controller.1.activate")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    tdkTestObj = obj.createTestStep('rdkvsecurity_getPluginStatus');
                    tdkTestObj.addParameter("plugin",plugin)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult();
                    status = tdkTestObj.getResultDetails()
                    if expectedResult in result and status == "activated":
                        Test_Step_Status = True
                        print "SUCCESS: Activated plugin : {}\n".format(plugin)
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        Test_Step_Status = False
                        print "FAILURE: Plugin is not in activated state"
                        tdkTestObj.setResultStatus("FAILURE");
                        break
                else:
                    Test_Step_Status = False
                    print "FAILURE: Plugin Activation Failed"
                    tdkTestObj.setResultStatus("FAILURE");
                    break
            elif status == "activated":
                Test_Step_Status = True
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: %s Plugin is in Activated state" %(plugin)
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "FAILURE: Could not retrieve the status of the %s plugin" %(plugin)
            break
    if Test_Step_Status:
        print "Retrieving Configuration values from config file......."
        configKeyList = ["PREFERRED_NETWORK_PARAMETER","WIFI_SSID_NAME","WIFI_PASSPHRASE","WIFI_SECURITY_MODE","SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "ENCRYPTED_WIFI_PASSWORD_SUPPORT"]
        configValues = {}
        tdkTestObj = obj.createTestStep('rdkvsecurity_getDeviceConfig')
        #Get each configuration from device config file
        for configKey in configKeyList:
            tdkTestObj.addParameter("basePath",obj.realpath)
            tdkTestObj.addParameter("configKey",configKey)
            tdkTestObj.executeTestCase(expectedResult)
            configValues[configKey] = tdkTestObj.getResultDetails()
            if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
                print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                 print "FAILURE: Failed to retrieve %s configuration from device config file" %(configKey)
                 if configValues[configKey] == "":
                     print "\n Please configure the %s key in the device config file" %(configKey)
                 tdkTestObj.setResultStatus("FAILURE")
                 result = "FAILURE"
                 break
        if "FAILURE" != result:
            if "directSSH" == configValues["SSH_METHOD"] :
                if configValues["SSH_PASSWORD"] == "None":
                    configValues["SSH_PASSWORD"] = ""
                credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
                command = configValues["PREFERRED_NETWORK_PARAMETER"]
                print "COMMAND: %s" %(command)
                tdkTestObj = obj.createTestStep('rdkvsecurity_executeInDUT')
                tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                tdkTestObj.addParameter("credentials", credentials);
                tdkTestObj.addParameter("command", command);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS: Successfully enabled preferred network type"
                    params = '{"incremental":false,"ssid":"","frequency":""}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.Wifi.1.startScan")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        time.sleep(10)
                        ssid = configValues["WIFI_SSID_NAME"]
                        print "\n Connecting to SSID : {}\n".format(ssid)
                        params = '{"ssid":"'+ ssid +'", "passphrase": "'+configValues["WIFI_PASSPHRASE"]+'", "securityMode":'+configValues["WIFI_SECURITY_MODE"]+'}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.Wifi.1.connect")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(20)
                            print "\n Checking whether DUT is connected to SSID \n"
                            tdkTestObj = obj.createTestStep('rdkvsecurity_getReqValueFromResult')
                            tdkTestObj.addParameter("method","org.rdk.Wifi.1.getConnectedSSID")
                            tdkTestObj.addParameter("reqValue","ssid")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if expectedResult in result:
                                connected_ssid = tdkTestObj.getResultDetails()
                                print " \n Connected SSID Name: {}\n ".format(connected_ssid)
                                if ssid == connected_ssid:
                                    print "SUCCESS: Successfully Connected to SSID \n "
                                    print "Checking WPA_Supplicant file present in DUT"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    command = '[ -f "/opt/wifi/wpa_supplicant.conf" ] && echo 1 || echo 0'
                                    print "COMMAND : %s" %(command)
                                    tdkTestObj = obj.createTestStep('rdkvsecurity_executeInDUT')
                                    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                                    tdkTestObj.addParameter("credentials", credentials);
                                    tdkTestObj.addParameter("command", command);
                                    tdkTestObj.executeTestCase(expectedResult);
                                    output = tdkTestObj.getResultDetails();
                                    output = str(output).split("\n")[1] 
                                    if expectedResult in result and int(output) == 1:
                                        print "SUCCESS: WPA_Supplicant file exists checking whether it contains WiFi passphrase........"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        command = 'grep -F '+str(configValues["WIFI_PASSPHRASE"])+' /opt/wifi/wpa_supplicant.conf'
                                        print "COMMAND: %s" %(command)
                                        tdkTestObj = obj.createTestStep('rdkvsecurity_executeInDUT');
                                        tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                                        tdkTestObj.addParameter("credentials", credentials);
                                        tdkTestObj.addParameter("command", command);
                                        tdkTestObj.executeTestCase(expectedResult);
                                        output = tdkTestObj.getResultDetails();
                                        output = str(output).split("\n")[1]
                                        if "no" in configValues["ENCRYPTED_WIFI_PASSWORD_SUPPORT"].lower():
                                            if str(configValues["WIFI_PASSPHRASE"]) in output:
                                                print "SUCCESS: WiFi passphrase is not encrypted and saved as a plain text in WPA_Supplicant file"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            elif str(configValues["WIFI_PASSPHRASE"]) not in output:
                                                print "FAILURE: WiFi passphrase not saved as a plain text in WPA_Supplicant file"
                                                tdkTestObj.setResultStatus("FAILURE") 
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                        elif "yes" in configValues["ENCRYPTED_WIFI_PASSWORD_SUPPORT"].lower():
                                            if str(configValues["WIFI_PASSPHRASE"]) not in output:
                                                print "SUCCESS: WiFi passphrase not saved as a plain text in WPA_Supplicant file"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            elif str(configValues["WIFI_PASSPHRASE"]) in output:    
                                                print "FAILURE: WiFi passphrase is not encrypted and saved as a plain text in WPA_Supplicant file"
                                                tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "FAILURE: WPA_Supplicant file not exists in DUT"
                                        tdkTestObj.setResultStatus("FAILURE")
                                        
                                    params = '{}'
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method","org.rdk.Wifi.1.disconnect")
                                    tdkTestObj.addParameter("value",params)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()  
                                    if expectedResult in result:
                                       tdkTestObj.setResultStatus("SUCCESS")
                                       print "SUCCESS: Successfully disconnected from Wifi"
                                    else:
                                        print "\nFAILURE: Error while executing org.rdk.Wifi.1.disconnect method \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\nFAILURE: DUT is not connected to SSID"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\nFAILURE: Error while executing org.rdk.Wifi.1.getConnectedSSID method \n"
                                tdkTestObj.setResultStatus("FAILURE")        
                        else:
                            print "\nFAILURE: Error while executing org.rdk.Wifi.1.connect method \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\nFAILURE: Error while executing org.rdk.Wifi.1.startScan method \n"
                        tdkTestObj.setResultStatus("FAILURE")        

                else:
                    print "FAILURE: Enabling preferred network type failed"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "FAILURE: Currently only supports directSSH ssh method"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "FAILURE: Failed to get configuration values"
            tdkTestObj.setResultStatus("FAILURE");

    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "FAILURE: Plugins activation step failed"

    #Unload the module
    obj.unloadModule("rdkv_security");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "FAILURE: Failed to load module"
