##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
  <name>TR069_Get_DeviceCPUTemperature_87</name>
  <primitive_test_id>585</primitive_test_id>
  <primitive_test_name>Tr069_Get_Profile_Parameter_Values</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: To fetch the device CPU temperature by querying the tr69Hostif through curl.  Query string "Device.DeviceInfo.X_RDKCENTRAL-COM.CPUTemp". 
TestCaseID: CT_TR69_87
TestType: Positive</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TR69_87</test_case_id>
    <test_objective>To fetch the device CPU temperature by querying the tr69Hostif through curl. 
Query string "Device.DeviceInfo.X_RDKCENTRAL-COM.CPUTemp". No set operation avaliable for this parameter.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.X_RDKCENTRAL-COM.CPUTemp"}]}' http://127.0.0.1:10999</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. TM loads tr69Test agent and devicesetting agent via the test agent.
2. Tr69Test agent will frame the curl request message "Device.DeviceInfo.X_RDKCENTRAL-COM.CPUTemp" to fetch cpu temperature.
3. Tr69Test agent will get the curl response which be a valid string on SUCCESS.
4. If tr69Test agent will get empty string as curl response, if FAILURE.
5. If step3 is success, get CPU temperature from DeviceSettingsAgent and compare the value fetched in step 3. 
6. TM Unloads tr69Test agent and devicesetting agent.</automation_approch>
    <except_output>Checkpoint 1. Need to get valid string value on SUCCESS. Empty on FAILURE.
Checkpoint 2. Temperature value difference between DS and TR69 should be less than 1C.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtr69stub.so
libdevicesettingsstub.so</test_stub_interface>
    <test_script>TR069_Get_DeviceCPUTemperature_87</test_script>
    <skipped>No</skipped>
    <release_version>M23</release_version>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from devicesettings import dsManagerInitialize,dsManagerDeInitialize,dsGetCPUTemp;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Load DS module
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'TR069_Get_DeviceCPUTemperature_87');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus(dsLoadStatus);

if 'SUCCESS' in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
		#Test component to be tested
		tr69Obj = tdklib.TDKScriptingLibrary("tr069module","2.0");
		tr69Obj.configureTestCase(ip,port,'TR069_Get_DeviceCPUTemperature_87');
		tr69LoadStatus = tr69Obj.getLoadModuleResult();
		print "[TR069 LIB LOAD STATUS]  :  %s" %tr69LoadStatus;
		tr69Obj.setLoadModuleStatus(tr69LoadStatus);
		if 'SUCCESS' in tr69LoadStatus.upper():
			#Parameter is the profile path to be queried
			profilePath = "Device.DeviceInfo.X_RDKCENTRAL-COM.CPUTemp"
			#Calling Tr069_Get_Profile_Parameter_Values
        		tr69TestObj = tr69Obj.createTestStep('Tr069_Get_Profile_Parameter_Values');
        		expectedresult = "SUCCESS"
       			tr69TestObj.addParameter("path",profilePath);
        		tr69TestObj.executeTestCase(expectedresult);
        		actualresult = tr69TestObj.getResult();
        		tr69Details = tr69TestObj.getResultDetails();
        		print "Result : [%s] Details : [%s]" %(actualresult,tr69Details);
        		#Check for SUCCESS/FAILURE return value of Tr069_Get_Profile_Parameter_Values
        		if expectedresult in actualresult:
				#Calling Device Setting - Get CPU Temperature
               			dsResult,dsDetails = dsGetCPUTemp(dsObj,'SUCCESS')
                		#Verify that temperature reported from ds and tr69 are not very different (max 1C difference)
                		tolerance = float(tr69Details) - float(dsDetails)
                		print "Temperature value difference between DS and TR69 is %",abs(tolerance),"C"
				if ( abs(tolerance) <= float(1) ):
        				tr69TestObj.setResultStatus("SUCCESS");
				else:
                        		print "TR69 CPU Temperature value failed verification"
					tr69TestObj.setResultStatus("FAILURE");
        		else:
				tr69TestObj.setResultStatus("FAILURE");
			#Unload the tr069module
			tr69Obj.unloadModule("tr069module");
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
