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
#

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------
import os
import sys

def getInstanceNumber(paramName,index):
                try:
                    instanceNumber = 0
                    paramList = paramName.split(".")
                    instanceNumber = paramList[index]
                except:
                        return 0
                return instanceNumber

def readtdkbConfigFile(self):

# Reads config file and returns the value.

# Syntax      : OBJ.readtdkbConfigFile()
# Description : Reads config file and returns the value.
# Parameters  : configFile - Name of config file.
# Return Value: value given in the config file

        configFile = self.realpath + "fileStore/" + "tdkb.config"
        print "Configuration File Found : ", configFile
        sys.stdout.flush()
        HostName="";

        # Checking if file exists
        fileCheck = os.path.isfile(configFile)
        if (fileCheck):
                for line in open(configFile).readlines():
                        if "HOST_NAME" in line:
                                HostName=line.split("=")[1].strip();
                                print "Host name is %s" %HostName;
                if HostName == "":
                    return "NULL"
        else:
                print "Configuration File does not exist."
                sys.stdout.flush()
                exit()
        return HostName;

########## End of Function ##########

def getMultipleParameterValues(obj,paramList):

# getMultipleParameterValues

# Syntax      : getMultipleParameterValues()
# Description : Function to get the values of multiple parameters at single shot
# Parameters  : obj - module object
#             : paramList - List of parameter names
# Return Value: SUCCESS/FAILURE

    expectedresult="SUCCESS";
    status = "SUCCESS";

    actualresult= [];
    orgValue = [];

    #Parse and store the values retrieved in a list
    for index in range(len(paramList)):
            tdkTestObj = obj.createTestStep("TADstub_Get");
            tdkTestObj.addParameter("paramName",paramList[index])
            tdkTestObj.executeTestCase(expectedresult);
            actualresult.append(tdkTestObj.getResult())
            details = tdkTestObj.getResultDetails();
            if details:
                    orgValue.append(details);

    for index in range(len(paramList)):
            if expectedresult not in actualresult[index]:
                    status = "FAILURE";
                    break;

    return (tdkTestObj,status,orgValue);

######### End of Function ##########

def changeAdminPassword(pamobj,password):
  
# changeAdminPassword

# Syntax      : changeAdminPassword
# Description : Function to change admin password
# Parameters  : sysobj - module object
# Return Value: SUCCESS/FAILURE


     tdkTestObj = pamobj.createTestStep('pam_Setparams');
     tdkTestObj.addParameter("ParamName","Device.Users.User.3.Password");
     tdkTestObj.addParameter("Type","string");
     tdkTestObj.addParameter("ParamValue",password);
     expectedresult="SUCCESS";
     tdkTestObj.executeTestCase(expectedresult);
     actualresult = tdkTestObj.getResult();
     details = tdkTestObj.getResultDetails();
     if expectedresult in actualresult:
         tdkTestObj.setResultStatus("SUCCESS");
         print "TEST STEP : Change the admin password";
         print "EXPECTED RESULT : Should change the admin password";
         print "ACTUAL RESULT : Admin password is changed, %s" %details;
         print "[TEST EXECUTION RESULT] :%s" %actualresult;
     else:
         tdkTestObj.setResultStatus("FAILURE");
         print "TEST STEP : Change the admin password";
         print "EXPECTED RESULT  : Should change the admin password";
         print "ACTUAL RESULT : Failed to change the admin password, %s" %details;
         print "[TEST EXECUTION RESULT] :%s" %actualresult;

######### End of Function ##########

