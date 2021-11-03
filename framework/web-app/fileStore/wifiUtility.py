#!/usr/bin/python

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

#Secure 2.4Ghz Public Wifi Access Point index
apIndex_2G_Public_Wifi = 8;
#Secure 5Ghz Public Wifi Access Point index
apIndex_5G_Public_Wifi = 9;

# A utility function to invoke WiFi hal apis based on the method name received
#
# Syntax       : ExecuteWIFIHalCallMethod(obj, primitive, radioIndex, param, methodname)
#
# Parameters   : obj, primitive, radioIndex, param, methodname
#
# Return Value : Execution status of the hal api

def ExecuteWIFIHalCallMethod(obj, primitive, radioIndex, param, methodname):

    tdkTestObj = obj.createTestStep(primitive);
    tdkTestObj.addParameter("radioIndex", radioIndex);
    #'param' is valid for only set operations. It isdummy attribute for get functions
    tdkTestObj.addParameter("param", param);
    tdkTestObj.addParameter("methodName", methodname);
    expectedresult="SUCCESS";

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedresult in actualresult :
        print "TEST STEP : Execute callmethod for %s" %methodname
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT : %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        print "TEST STEP : Execute callmethod for %s" %methodname
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT 1: %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";

    return (tdkTestObj, actualresult, details);

# A utility function to get the radio index from the radio name received
#
# Syntax       : getIndex(obj, radio)
#
# Parameters   : obj, radio
#
# Return Value : Index of the radio

def getIndex(obj, radio):
        #Script to load the configuration file of the component
        tdkTestObj = obj.createTestStep("WIFIHAL_GetOrSetParamULongValue");
        #Giving the method name to invoke the api wifi_getRadioNumberOfEntries()
	methodname = "getRadioNumberOfEntries";
        tdkTestObj.addParameter("methodName",methodname);
        tdkTestObj.addParameter("radioIndex",1); # Dummy index
        expectedresult="SUCCESS"; # Dummy expected value
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();

        if expectedresult in actualresult:
                numEntries = int(details.split(':')[1]);
		print "Number of radio entries found : %d" %numEntries;

                for index in range(numEntries):
			methodname = "getRadioOperatingFrequencyBand";
                        #Script to load the configuration file of the component
                        tdkTestObj = obj.createTestStep("WIFIHAL_GetOrSetParamStringValue");
                        #Giving the method name to invoke the api for getting the Operating Frequency band. ie,wifi_getRadioOpeartingFrequencyBand()
                        tdkTestObj.addParameter("methodName",methodname);
                        # Query for all indices
                        tdkTestObj.addParameter("radioIndex",index);
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        OperatingFrequencyBands = tdkTestObj.getResultDetails();

                        if expectedresult in actualresult:
                                if radio in OperatingFrequencyBands:
					print "Radio: %s Found at index: %d" %(radio,index);
                                        return tdkTestObj, index;

                        else:
				print "TEST STEP : Execute callmethod for %s" %methodname;
			        print "EXPECTED RESULT : Should return the operating frequency band for index %d" %index;
			        print "ACTUAL RESULT : %s " %OperatingFrequencyBands;

        else:
		print "TEST STEP : Execute callmethod for %s" %methodname;
		print "EXPECTED RESULT : Should return the number of radios";
		print "ACTUAL RESULT : %s " %details;

        return tdkTestObj, -1;

# A utility function to get the private access point index for 6G radio
#
# Syntax       : getApIndexfor6G(sysobj, TDK_PATH)
#
# Parameters   : sysobj
#
# Return Value : tdkTestObj, apIndex

def getApIndexfor6G(sysobj, TDK_PATH):
    apIndex = -1;
    cmd= "sh %s/tdk_utility.sh parseConfigFile PRIVATE_6G_AP_INDEX" %TDK_PATH;
    print cmd;
    expectedresult="SUCCESS";
    tdkTestObj = sysobj.createTestStep('ExecuteCmd');
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "");

    if expectedresult in actualresult and details.isdigit():
        apIndex = int(details);
        print "\nTEST STEP 1: Get PRIVATE_6G_AP_INDEX  from property file";
        print "EXPECTED RESULT 1: Should  get PRIVATE_6G_AP_INDEX  from property file"
        print "ACTUAL RESULT 1: PRIVATE_6G_AP_INDEX from property file :", apIndex ;
        print "TEST EXECUTION RESULT :SUCCESS";
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        print "TEST STEP 1: Get PRIVATE_6G_AP_INDEX  from property file";
        print "EXPECTED RESULT 1: Should  get PRIVATE_6G_AP_INDEX  from property file"
        print "ACTUAL RESULT 1: PRIVATE_6G_AP_INDEX from property file :", details ;
        print "TEST EXECUTION RESULT : FAILURE";
        tdkTestObj.setResultStatus("FAILURE");
    return tdkTestObj, apIndex;

