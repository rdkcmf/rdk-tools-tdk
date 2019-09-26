##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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
  <name>ACM_AudioPropertiesPersists</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>AudioCaptureMgr_Session_Open</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if audio properties persists over session</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_ACM_14</test_case_id>
    <test_objective>To check if audio properties persists over session</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v3</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_OPEN, (void *) &amp;param, sizeof(param))
IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_GET_AUDIO_PROPS, (void *) &amp;param, sizeof(param))
IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_SET_AUDIO_PROPS, (void *) &amp;param, sizeof(param))
IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_CLOSE, (void *) &amp;param, sizeof(param))</api_or_interface_used>
    <input_parameters>iarmbus_acm_arg_t param</input_parameters>
    <automation_approch>1. TM loads the AudioCaptureMgr agent via the test agent.
2. AudioCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_OPEN
3. AudioCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_GET_OUTPUT_PROPS
4. AudioCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_SET_OUTPUT_PROPS with audio properties parameter different from what obtained in step 3.
5. AudioCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_GET_OUTPUT_PROPS
6. Check if the audio properties returned are same as the properties set in step 4 
7. AudioCaptureMgr agent will invoke the IARM_Bus_Call for IARMBUS_AUDIOCAPTUREMGR_CLOSE
8. Repeat steps 2-3 and check if audio properties do not change and return SUCCESS/FAILURE</automation_approch>
    <except_output>Checkpoint 1.Verify the IARMBUS calls are SUCCESS 
Checkpoint 2.Verify the value returned for audio properties are same over sessions</except_output>
    <priority>High</priority>
    <test_stub_interface>libaudiocapturemgrstub.so</test_stub_interface>
    <test_script>ACM_AudioPropertiesPersists</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from iarmbus import IARMBUS_Init,IARMBUS_Connect,IARMBUS_DisConnect,IARMBUS_Term;
import ast;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
iarmObj.configureTestCase(ip,port,'ACM_AudioPropertiesPersists');
#Get the result of connection with test component and STB
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "Iarmbus module loading status : %s" %iarmLoadStatus ;
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);

def getAudioProperties():
	properties = {};
	#Prmitive test case which associated to this Script
        tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_GetAudioProperties');

        #Execute the test case in STB
        expectedresult="SUCCESS"
	tdkTestObj.executeTestCase(expectedresult);

	#Get the result of execution
	actualresult = tdkTestObj.getResult();
	print "[TEST EXECUTION RESULT] : %s" %actualresult;


	#Set the result status of execution
	if expectedresult in actualresult:
		properties = ast.literal_eval(tdkTestObj.getResultDetails());
		print "Audio Properties: %s"%properties;
		tdkTestObj.setResultStatus("SUCCESS");
		print "Audio Properties retrieved";
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Failed to retrieve Audio Properties";

	return properties;

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
                        acmObj = tdklib.TDKScriptingLibrary("audiocapturemgr","1");
                        acmObj.configureTestCase(ip,port,'ACM_AudioPropertiesPersists');

                        #Get the result of connection with test component and STB
                        acmLoadStatus = acmObj.getLoadModuleResult();
                        print "[LIB LOAD STATUS]  :  %s" %acmLoadStatus;
                        #Set the module loading status
                        acmObj.setLoadModuleStatus(acmLoadStatus);

                        if "SUCCESS" in acmLoadStatus.upper():
                                #Prmitive test case which associated to this Script
                                tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_Session_Open');

                                #Execute the test case in STB
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);

                                #Get the result of execution
                                actualresult = tdkTestObj.getResult();
                                print "[TEST EXECUTION RESULT] : %s" %actualresult;


                                #Set the result status of execution
                                if expectedresult in actualresult:
                                	sessionId = tdkTestObj.getResultDetails();
        	                        print "Session ID: %s"%sessionId;
					if sessionId == -1:
                                        	tdkTestObj.setResultStatus("FAILURE");
						print "Failed to open AudioCaptureMgr session";
					else:
                                        	tdkTestObj.setResultStatus("SUCCESS");
						print "AudioCaptureMgr session opened successfully";
						
						props = getAudioProperties();

						if props != {}:
							#Prmitive test case which associated to this Script
		        	                        tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_SetAudioProperties');
							delay = props['DelayComp'] + 10;
							threshold = props['Threshold'] + 10;
							fifoSize = props['FifoSize'] + 10;
							#tdkTestObj.addParameter("delay", 190);
							tdkTestObj.addParameter("delay", delay);
							tdkTestObj.addParameter("threshold", threshold);
							tdkTestObj.addParameter("fifoSize", fifoSize);
		

		                                	#Execute the test case in STB
	                		                expectedresult="SUCCESS"
        	                        		tdkTestObj.executeTestCase(expectedresult);

			                                #Get the result of execution
                			                actualresult = tdkTestObj.getResult();
                                			print "[TEST EXECUTION RESULT] : %s" %actualresult;


	                          			#Set the result status of execution
        	                        		if expectedresult in actualresult:
								props = getAudioProperties();
								if props != {}:
									if (props['DelayComp'] == delay and props['Threshold'] == threshold and props['FifoSize'] == fifoSize):
                                			        		tdkTestObj.setResultStatus("SUCCESS");
                                        	        			print "Audio Properties set correctly";
									else:
                                                				tdkTestObj.setResultStatus("FAILURE");
                                        	        			print "Audio Properties not set correctly";
									
							else:
                                                		tdkTestObj.setResultStatus("FAILURE");
		                                        	print "Failed to set Audio Properties";
							

						#Prmitive test case which associated to this Script
			                        tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_Session_Close');

			                        #Execute the test case in STB
                	        		expectedresult="SUCCESS"
		        	                tdkTestObj.executeTestCase(expectedresult);

                               			#Get the result of execution
		                                actualresult = tdkTestObj.getResult();
                       			        print "[TEST EXECUTION RESULT] : %s" %actualresult;

		                                #Set the result status of execution
                       			        if expectedresult in actualresult:
                               		                tdkTestObj.setResultStatus("SUCCESS");
                                               		print "AudioCaptureMgr session closed successfully";

							#Prmitive test case which associated to this Script
							tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_Session_Open');

							#Execute the test case in STB
							expectedresult="SUCCESS"
							tdkTestObj.executeTestCase(expectedresult);

							#Get the result of execution
							actualresult = tdkTestObj.getResult();
							print "[TEST EXECUTION RESULT] : %s" %actualresult;


							#Set the result status of execution
							if expectedresult in actualresult:
								props1 = getAudioProperties();
								if props1 != {}:
									if (props1['DelayComp'] == delay and props1['Threshold'] == threshold and props1['FifoSize'] == fifoSize):
										tdkTestObj.setResultStatus("SUCCESS");
										print "Audio Properties persists over session";
									else:
										tdkTestObj.setResultStatus("FAILURE");
										print "Audio Properties do not persist";
								#Prmitive test case which associated to this Script
								tdkTestObj = acmObj.createTestStep('AudioCaptureMgr_Session_Close');

								#Execute the test case in STB
								expectedresult="SUCCESS"
								tdkTestObj.executeTestCase(expectedresult);

								#Get the result of execution
								actualresult = tdkTestObj.getResult();
								print "[TEST EXECUTION RESULT] : %s" %actualresult;
							else:
								 tdkTestObj.setResultStatus("FAILURE");
								 print "Failed to open new session";
						else:
                                               		tdkTestObj.setResultStatus("FAILURE");
	                                                print "Failed to close AudioCaptureMgr session";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
					print "Call to open AudioCaptureMgr session failed";

                                acmObj.unloadModule("audiocapturemgr");

                        else :
                                print "Failed to Load audiocapturemgr Module "

                        #Calling IARM_Bus_DisConnect API
                        result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
                #calling IARMBUS API "IARM_Bus_Term"
                result = IARMBUS_Term(iarmObj,"SUCCESS")
        #Unload iarmbus module
        iarmObj.unloadModule("iarmbus");

