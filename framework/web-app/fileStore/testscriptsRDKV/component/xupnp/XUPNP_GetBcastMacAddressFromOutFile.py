##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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
  <name>XUPNP_GetBcastMacAddressFromOutFile</name>
  <primitive_test_id/>
  <primitive_test_name>XUPNP_ReadXDiscOutputFile</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the broadcast mac address value from xdiscovery output file.
Testcase ID: CT_XUPNP_55</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_XUPNP_55</test_case_id>
    <test_objective>To get the broadcast mac address value from xdiscovery output file.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.start_upnp.sh should be started.
2.Process xcal-device and xdiscovery should be running on GW Box and xdiscovery should be running on IPClient Box</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>string paramName = bcastMacAddress</input_parameters>
    <automation_approch>1.TM loads xupnp_agent via the test agent. 
2.The stub will invokes the RPC method for checking the parameter name in output.json file and send the results.
3. The stub function will verify the presence of parameter name and  sends the results as Json response 
4. TM will receive and display the result.
5. TM will convert the details as a list.
6. Using systemutil ExecuteCommand command get the parameter from cat /.tmp/deviceDtails.cache
7 If the bcastMacAddress obtained from the /.tmp/deviceDetails.cache is present in the list created in step 5 the result is success else failure.</automation_approch>
    <except_output>Checkpoint 1 stub will parse for parameter name in output.json file
Checkpoint 2 the parameter from the ExecuteCommand  should be present in the parameter list obtained from output.json</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_XUPNP_ReadXDiscOutputFile</test_stub_interface>
    <test_script>XUPNP_GetBcastMacAddressFromOutFile</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from iarmbus import IARMBUS_Init,IARMBUS_Connect,IARMBUS_DisConnect,IARMBUS_Term;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def check_WiFiConnected():
    #Test component to be tested
    iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
    iarmObj.configureTestCase(ip,port,'XUPNP_GetBcastMacAddressFromOutFile');
    #Get the result of connection with test component and STB
    iarmLoadStatus = iarmObj.getLoadModuleResult();
    print "Iarmbus module loading status : %s" %iarmLoadStatus ;
    #Set the module loading status
    iarmObj.setLoadModuleStatus(iarmLoadStatus);

    if "SUCCESS" in iarmLoadStatus.upper():
        #Calling IARMBUS API "IARM_Bus_Init"
        result = IARMBUS_Init(iarmObj,"SUCCESS")
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if "SUCCESS" in result:
            #Calling IARMBUS API "IARM_Bus_Connect"
            result = IARMBUS_Connect(iarmObj,"SUCCESS")
            #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
            if "SUCCESS" in result:
                #Test component to be tested
                netsrvObj = tdklib.TDKScriptingLibrary("netsrvmgr","1");
                netsrvObj.configureTestCase(ip,port,'XUPNP_GetBcastMacAddressFromOutFile');
                netsrvLoadStatus =netsrvObj.getLoadModuleResult();
                print "[LIB LOAD STATUS]  :  %s" %netsrvLoadStatus;
                #Set the module loading status
                netsrvObj.setLoadModuleStatus(netsrvLoadStatus);

                if "SUCCESS" in netsrvLoadStatus.upper():
                    #Prmitive test case which associated to this Script
                    tdkTestObj = netsrvObj.createTestStep('NetSrvMgr_WifiMgr_SetGetParameters');

                    #Execute the test case in STB
                    tdkTestObj.addParameter("method_name", "isPaired");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);

                    #Get the result of execution
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    isConnected = 0;
                    print "[TEST EXECUTION RESULT] : %s" %actualresult;
                    if expectedresult in actualresult:
                        print "isPaired executed successfully";
                        if int(details):
                            print "Device is connected in WiFi mode";
                            isConnected = 1;
                        else:
                            print "Device is not connected to WiFi mode";
                    else:
                        print "isPaired failed";
                        tdkTestObj.setResultStatus("FAILURE");
                    netsrvObj.unloadModule("netsrvmgr");
                else:
                    print "Netsrv module load failed"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "iarmbus init failed";
                tdkTestObj.setResultStatus("FAILURE");
            IARMBUS_DisConnect(iarmObj,"SUCCESS")
        else:
            print "iarmbus connect failed";
            tdkTestObj.setResultStatus("FAILURE");
        IARMBUS_Term(iarmObj,"SUCCESS")
        iarmObj.unloadModule("iarmbus");
    else:
        print "iarmbus module load failed"
        tdkTestObj.setResultStatus("FAILURE");
    return isConnected;

#Test component to be tested
xUpnpObj = tdklib.TDKScriptingLibrary("xupnp","2.0");
xUpnpObj.configureTestCase(ip,port,'XUPNP_GetBcastMacAddressFromOutFile');
#Get the result of connection with test component and STB
xupnpLoadStatus = xUpnpObj.getLoadModuleResult();
print "XUPNP module loading status : %s" %xupnpLoadStatus;
#Set the module loading status
xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
sysUtilObj.configureTestCase(ip,port,'XUPNP_GetBcastMacAddressFromOutFile');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

if ("SUCCESS" in xupnpLoadStatus.upper()) and ("SUCCESS" in sysUtilLoadStatus.upper()):
        tdkTestObj = xUpnpObj.createTestStep('XUPNP_ReadXDiscOutputFile');
        expectedresult="SUCCESS";
        #Configuring the test object for starting test execution
        tdkTestObj.addParameter("paramName","bcastMacAddress");
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "GetBcastMacAddress Result : %s"%actualresult;
        #Check for SUCCESS return value of XUPNP_ReadXDiscOutputFile
        if "SUCCESS" in actualresult.upper():
		tdkTestObj.setResultStatus("SUCCESS");
		details = details.replace('\\t','').replace('\\','').replace('\"','')
		details_list = details.split(',')
        	print "GetBcastMacAddress Details : %s"%details_list;
		bcast_mac_list = [ detail.split(':',1)[1] for detail in details_list]
		print "bcastlist: %s"%bcast_mac_list

                #Check if Device support wifi
                tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
                cmd = "cat /etc/device.properties | grep WIFI_SUPPORT=true"
                print cmd;
                tdkTestObj.addParameter("command", cmd);
                tdkTestObj.executeTestCase("SUCCESS");
                actualresult = tdkTestObj.getResult();
                WIFI_SUPPORT = tdkTestObj.getResultDetails();
                wifi_connected = 0;
                if WIFI_SUPPORT:
                    print "Device supports wifi"
                    print "Check if device is connected in wifi mode"
                    wifi_connected = check_WiFiConnected();
                else:
                    print "Device doesnot support wifi"

		#Get the BcasMacAddress value from /tmp/.deviceDetails.cache and compare
                mac_details = 0;
		tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
                if wifi_connected:
                    cmd = "cat /tmp/.deviceDetails.cache | grep wifi_mac | cut -d '=' -f2 | tr -d '\\n'"
                else:
                    cmd = "cat /tmp/.deviceDetails.cache | grep moca_mac | cut -d '=' -f2 | tr -d '\\n'"
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    mac_details = tdkTestObj.getResultDetails();
                    if ( not mac_details ):
                        print "Device is not connected via MoCA, getting eth_mac instead";
                        cmd = "cat /tmp/.deviceDetails.cache | grep eth_mac | cut -d '=' -f2 | tr -d '\\n'"

		print cmd;
                if( not mac_details):
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    actualresult = tdkTestObj.getResult();
                    mac_details = tdkTestObj.getResultDetails();
                bcast_mac = mac_details.lower()
                print "BcastMacAddress from /tmp/.deviceDetails.cache: %s" %bcast_mac
                if expectedresult in actualresult and (bcast_mac in bcast_mac_list):
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Actual Result: BcastMacAddress retrieved from  /tmp/.deviceDetails.cache and output.json are same"
                        print "[TEST EXECUTION RESULT] : SUCCESS"
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Actual Result :BcastMacAddress retrieved from /tmp/.deviceDetails.cache and output.json are not same"
                        print "[TEST EXECUTION RESULT] : FAILURE"
	else:
		tdkTestObj.setResultStatus("FAILURE");
                print "BcastMacAddress not retrieved from output.json"

        #Unload xupnp module
        xUpnpObj.unloadModule("xupnp");
        sysUtilObj.unloadModule("systemutil");
