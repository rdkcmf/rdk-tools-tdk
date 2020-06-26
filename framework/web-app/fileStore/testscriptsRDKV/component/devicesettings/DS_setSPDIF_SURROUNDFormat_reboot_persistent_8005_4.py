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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>8</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_setSPDIF_SURROUNDFormat_reboot_persistent_8005_4</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_AOP_getStereoAuto</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Device Setting –  Get and set stereo mode to SURROUND in SPDIF and check the value is persisting after device reboot</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <script_tags />
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","2.2");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_setSPDIF_SURROUNDFormat_reboot_persistent_8005_4');

loadmodulestatus =obj.getLoadModuleResult();


if "SUCCESS" in loadmodulestatus.upper() :
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize 
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
		#calling DS_GetSupportedStereoModes get list of StereoModes.
		tdkTestObj = obj.createTestStep('DS_GetSupportedStereoModes');
		tdkTestObj.addParameter("port_name","SPDIF0");
		tdkTestObj.executeTestCase(expectedresult);
		actualresult = tdkTestObj.getResult();
		stereomodedetails = tdkTestObj.getResultDetails();
		#Check for SUCCESS/FAILURE return value of DS_GetSupportedStereoModes
		if expectedresult in actualresult:
			print "SUCCESS :Application successfully gets the list of supported StereoModes";
			print "%s" %stereomodedetails
			tdkTestObj.setResultStatus("SUCCESS");

			stereomode="SURROUND";
			if stereomode in stereomodedetails:
				#calling DS_SetStereoMode to get and set the stereo modes
				tdkTestObj = obj.createTestStep('DS_SetStereoMode');
				tdkTestObj.addParameter("port_name","SPDIF0");
				tdkTestObj.addParameter("get_only",0);
				tdkTestObj.addParameter("persist",1);
				tdkTestObj.addParameter("stereo_mode",stereomode);
				tdkTestObj.executeTestCase(expectedresult);
				actualresult = tdkTestObj.getResult();
				stereomodedetails = tdkTestObj.getResultDetails();
				print stereomodedetails
				#Check for SUCCESS/FAILURE return value of DS_SetStereoMode
				if expectedresult not in actualresult:
					print "FAILURE: Application Failed to set and get the SURROUND mode to SPDIF";
					tdkTestObj.setResultStatus("FAILURE");
				else:
					if stereomode in stereomodedetails:
						tdkTestObj.setResultStatus("SUCCESS");
						print "SUCCESS: SURROUND Mode set for SPDIF";
						print "Rebooting the box to check the stereo mode persistence";
						obj.initiateReboot();
                        
						#calling Device Settings - initialize API
						tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
		                                tdkTestObj.executeTestCase(expectedresult);
						actualresult = tdkTestObj.getResult();
						#Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
						if expectedresult in actualresult:
							tdkTestObj.setResultStatus("SUCCESS");
							#calling DS_SetStereoMode to get and set the stereo modes
							tdkTestObj = obj.createTestStep('DS_SetStereoMode');
							tdkTestObj.addParameter("port_name","SPDIF0");
							tdkTestObj.addParameter("get_only",1);
							tdkTestObj.addParameter("persist",1);
							stereomode="SURROUND";
							tdkTestObj.addParameter("stereo_mode",stereomode);
							tdkTestObj.executeTestCase(expectedresult);
							actualresult = tdkTestObj.getResult();
							stereomodedetails = tdkTestObj.getResultDetails();
							print stereomodedetails
							#Check for SUCCESS/FAILURE return value of DS_SetStereoMode
							if expectedresult not in actualresult:
								print "FAILURE: Application Failed to get the SURROUND mode to SPDIF";
								tdkTestObj.setResultStatus("FAILURE");
							else:
								if stereomode in stereomodedetails:
									tdkTestObj.setResultStatus("SUCCESS");
									print "SUCCESS: SURROUND Mode set for SPDIF";
								else:
									tdkTestObj.setResultStatus("FAILURE");
									print "FAILURE: SURROUND Mode not set for SPDIF";
		                                else:
							tdkTestObj.setResultStatus("FAILURE");
							print "FAILURE: Device Setting Initialize failed";
					else:
						tdkTestObj.setResultStatus("FAILURE");
						print "FAILURE: SURROUND Mode not set for SPDIF";
			else:
				tdkTestObj.setResultStatus("FAILURE");
				print "FAILURE: SURROUND Mode not supported for SPDIF";
		else:
            	  	tdkTestObj.setResultStatus("FAILURE");
	                print "FAILURE :Failed to get supported stereo modes";

                #calling DS_ManagerDeInitialize to DeInitialize API 
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize 
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
                
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");


