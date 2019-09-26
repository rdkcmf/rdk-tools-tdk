#!/usr/bin/python

##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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
import tdklib
from time import sleep
import os
import ConfigParser
import os.path
import webpaUtility;
from webpaUtility import *

def getAllParamValues(moduleList,setup_type,deviceType,factory_reset_flag,obj):

# MethodName  : getAllParamValues
# Description : To get the values all namespaces for each module and validate it.
# input params: ModuleList - List of modules which are going to test
#             : obj - object containing the module
#	      : deviceType - Gives the details of DUT
#	      : setup_type - TDK/WEBPA
#	      : factory_reset_flag - True/False
# Return      : Returns SUCCESS/FAILURE.
    moduleStatusList = [];
    failedParamsList = {};

    for module in moduleList:
        failedParams = [];
        moduleStatus = "SUCCESS"

        print "\n------------------------------------------------------------------------"
        print "GET VALUES OF ALL NAMESPACES IN ", module;
        print "------------------------------------------------------------------------\n"

        #Get the device configuration file name
        deviceConfig = deviceType + "_tdkbtr181Parameters_" + module + ".config"
        print "The name of device config file is ", deviceConfig;

        #Get the current directory path
        configFilePath = os.path.dirname(os.path.realpath(__file__))
        configFilePath = configFilePath + "/tdkbModuleConfig"

        #Check if the device config file is present. If not, take generic config file
        if os.path.exists(configFilePath+'/'+deviceConfig) == False:
            deviceConfig = "tdkbtr181Parameters_" + module + ".config"
        print "Config file is ", deviceConfig

        #Parse the device configuration file
        config = ConfigParser.ConfigParser()
        config.read(configFilePath+'/'+deviceConfig)

        #Variable having the number of params for each module
        countVariable = module+"_PARAMETER_COUNT";
        paramCount = config.get(deviceConfig, countVariable)
        print "Count of params in ", module, "is ", paramCount, "\n";

        for i in range(1,int(paramCount)+1):
            #Variable having the value of each param
	    #For WiFi module the index is different for WEBPA
            if module == "WIFI" and setup_type == "WEBPA":
                variable = module + "_WEBPA_PARAMETER_" + str(i);
            else:
                variable=module+"_PARAMETER_"+str(i);

            #Get the value of each param
            configParam = config.get(deviceConfig, variable)
            nameSpace = configParam.split("|")[0];
            valueType = configParam.split("|")[1];
            #Take default values as expected values in case of factory reset, else take expected range of values
            if factory_reset_flag == "True":
                expectedValue = configParam.split("|")[2].lstrip();
            else:
                expectedValue = configParam.split("|")[3].lstrip();
            expectedresult="SUCCESS";
	    #Get the value for each given namespace using TDK or WEBPA
            tdkTestObj,value,actualresult = getParameterValue(obj,setup_type,deviceType,nameSpace);

            if expectedresult in actualresult and value in expectedValue and value != "":
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "TEST STEP", i, ": Get the value of param", nameSpace;
                print "TEST STEP ", i, "Should get the value of param as default value", expectedValue;
                print "ACTUAL RESULT ", i, " : %s" %value;
                print "TEST EXECUTION RESULT: SUCCESS"
                print "--------------------------------------------------------------------------------------\n"
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
                print "TEST STEP ", i, ": Get the value of param", nameSpace;
                print "TEST STEP ", i, "Should get the value of param as default value", expectedValue;
                print "ACTUAL RESULT ", i ,": %s" %value;
                print "TEST EXECUTION RESULT: FAILURE"
                print "--------------------------------------------------------------------------------------\n"
                moduleStatus = "FAILURE";
                failedParams.append(nameSpace);
        moduleStatusList.append(moduleStatus);
        failedParamsList[module]=failedParams;

    return moduleStatusList,failedParamsList;

############################################# End of Function #################################################

def getParameterValue(obj,setup_type,deviceType,paramName):

# getParameterValue

# Syntax      : getParameterValue()
# Description : Function to get the value of parameter
# Parameters  : obj - module object
#	      : setup_type : Type of execution, TDK/WEBPA
#	      : deviceType : details of DUT
#             : paramName - Parameter name
# Return Value: SUCCESS/FAILURE

    expectedresult="SUCCESS";
    status = "SUCCESS";

    actualresult= [];
    orgValue = [];

    if setup_type == "TDK":
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_Get");
        tdkTestObj.addParameter("ParamName",paramName)
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        value = tdkTestObj.getResultDetails();
    else:
        # Modify the input parameter to the format webpa is expecting
        param = {'name':paramName}

        # Invoke webpa utility to post the query for get operation
        queryResponse = webpaQuery(obj,param)
        parsedResponse = parseWebpaResponse(queryResponse, 1)
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_Get");
        tdkTestObj.executeTestCase(expectedresult);
        if "SUCCESS" in parsedResponse[0]:
                value = parsedResponse[1];
                actualresult = "SUCCESS"
        else:
                value = "WEBPA query failed"
                actualresult = "FAILURE"

    return (tdkTestObj,value,actualresult);

############################################# End of Function #################################################
