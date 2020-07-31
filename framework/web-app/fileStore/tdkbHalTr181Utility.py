##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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

import tdklib;
from time import sleep;
import xml.etree.ElementTree as ET
import os
from tdkbVariables import *;
import webpaUtility;
from webpaUtility import *;
from wifiUtility import *;

tr181_actualresult = "FAILURE";
hal_actualresult = "FAILURE";
expectedresult="SUCCESS";
failedparams = [];

# prerequisite

# Syntax      : prerequisite()
# Description : Function to check prerequisite for comparison utility to work
# Parameters  : sysobj - sysutil object
#             : setup_type : Type of execution, TDK/WEBPA/SNMP
# Return Value: 1-SUCCESS/ 0-FAILURE

def prerequisite(sysobj,setup_type):
    pre_req_status = 1;
    if setup_type == "SNMP":
        global commGetStr, ipaddress, commSetStr
        #Get the IP address and Community string value for SNMP GET
        commGetStr = snmplib.getCommunityString(sysobj,"snmpget");
        ipaddress = snmplib.getIPAddress(sysobj);
        if commGetStr != "" and ipaddress != "":
            pre_req_status = 1;
        else:
            pre_req_status = 0;

    elif setup_type == "WEBPA":
        #Verify Pre-requisite for WEBPA is Proper
        tdkTestObj,preRequisiteStatus = webpaPreRequisite(sysobj);
        if "SUCCESS" not in preRequisiteStatus:
            moduleStatus = "FAILURE";
            print "Webpa Pre-requisite failed , Please check parodus and webpa processes are running in device"
            pre_req_status = 0;
        else:
            pre_req_status = 1;
    return pre_req_status;

# getXMLNameUsingDeviceType

# Syntax      : getXMLNameUsingDeviceType()
# Description : Function to get the XML Name using Device Type and Script Module Name
# Parameters  : sysobj - sysutil object
#             : scriptmodule : Module to be Tested, ex:MTAHAL
# Return Value: xmlname - Name of the XML file

def getXMLNameUsingDeviceType(sysobj,scriptmodule):
    tdkTestObj = sysobj.createTestStep('ExecuteCmd');
    deviceType= "sh %s/tdk_utility.sh parseConfigFile DEVICETYPE" %TDK_PATH
    print deviceType;
    tdkTestObj.addParameter("command", deviceType);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    deviceType = tdkTestObj.getResultDetails().strip();
    deviceType = deviceType.replace("\\n", "");
    xmlname = "";
    if "Invalid Argument passed" not in deviceType:
        xmlname = deviceType + scriptmodule + ".xml"
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1: Get the device type";
        print "EXPECTED RESULT 1: Should Get the device type";
        print "ACTUAL RESULT 1: Device Type: %s" %deviceType;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1: Get the device type";
        print "EXPECTED RESULT 1: Should Get the device type";
        print "ACTUAL RESULT 1: Device Type: %s" %deviceType;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE"
        xmlname = "Error"

    return xmlname;


# parseXML

# Syntax      : parseXML()
# Description : Function to parse the module XML File
# Parameters  : xmlName - Name of the XML module file
#             : scriptmodule : Module to be Tested, ex:MTAHAL
#             : setup_type : Type of execution, TDK/WEBPA/SNMP
# Return Value: paramList - List of Parameters to get value
#             : halList   - List of HAL APIs to get value
#             : tr181_expectedvalue : List of expected values for TR181 Parameter
#             : hal_expectedvalue : List of expected values for HAL API's

def parseXML(xmlName,scriptmodule,setup_type):
    xmlPath = os.path.dirname(os.path.realpath(__file__))
    elementXml = xmlPath + "/tdkbModuleConfig" + "/" + xmlName
    print "The name of param list xml file is ", elementXml;

    tree = ET.parse(elementXml)
    elementRoot = tree.getroot()

    paramList = []
    halList = []
    tr181_expectedvalue = []
    hal_expectedvalue = []

    for param in elementRoot:
        flag_parse = 0;
        module_name = (param.find('module').text);
        if module_name == scriptmodule:
            if setup_type == "TDK":
                if param.find('parametername') is not None:
                    flag_parse = 1;
                    paramList.append(param.find('parametername').text);
                    halList.append(param.find('primitive').text);
            elif setup_type == "WEBPA":
                if param.find('webpaparamname') is not None:
                    flag_parse = 1;
                    paramList.append(param.find('webpaparamname').text);
                    halList.append(param.find('primitive').text);
            elif setup_type == "SNMP":
                if param.find('oid') is not None:
                    flag_parse = 1;
                    paramList.append(param.find('oid').text);
                    halList.append(param.find('primitive').text);

            if param.find('matchflag') is not None:
                if param.find('matchflag').text == "false" and flag_parse == 1:
                    tr181_expectedvalue.append(param.find('tr181_expectedvalue').text);
                    hal_expectedvalue.append(param.find('hal_expectedvaue').text);
                else:
                    tr181_expectedvalue.append("");
                    hal_expectedvalue.append("");

    return paramList,halList,tr181_expectedvalue,hal_expectedvalue;

# getHALAPIValue

# Syntax      : getHALAPIValue()
# Description : Function to Get the HAL API value
# Parameters  : obj - HAL Module Object
#             : Primitive : Primitive Data Type to get HAL API value
#             : hal_ExpRes : Expected value for HAL API
#             : scriptmodule: Module Name to be tested
# Return Value: actualresult : Status of HAL API Get operation
#             : details : Value of HAL API
#             : tdkTestObj : HAL Object Module

def getHALAPIValue(obj,primitive,hal_ExpRes,scriptmodule):
    exp_value_flag = 0;
    primitive_values = primitive.split(":");
    if(len(primitive_values) >= 1):
        tdkTestObj = obj.createTestStep(primitive_values[0]);
    if(len(primitive_values) >= 2):
        if scriptmodule == "WIFIHAL":
            tdkTestObj.addParameter("methodName",primitive_values[1]);
        elif scriptmodule == "CMHAL" or scriptmodule == "MTAHAL":
            tdkTestObj.addParameter("paramName",primitive_values[1]);
    if(len(primitive_values) >= 3) and scriptmodule == "WIFIHAL":
        tdkTestObjTemp, idx = getIndex(obj, primitive_values[2]);
        apIndex = idx;
        tdkTestObj.addParameter("radioIndex", apIndex);
        tdkTestObj.addParameter("param", "0");

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().replace("\\n", "");
    if details.startswith('Value returned'):
        details = details.partition(":")[2];

    if hal_ExpRes != "":
        if str(details).upper() == str(hal_ExpRes).upper():
		    exp_value_flag = 1;
        else:
            exp_value_flag = 0;
    else:
        exp_value_flag = 1;

    if expectedresult in actualresult and exp_value_flag == 1:
        print "TEST STEP : Execute callmethod for %s" %primitive
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT : %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        actualresult = "FAILURE"
        print "TEST STEP : Execute callmethod for %s" %primitive
        print "EXPECTED RESULT : Should successfully execute callmethod"
        print "ACTUAL RESULT 1: %s " %details
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";

    return actualresult,details,tdkTestObj;

# getTR181ParameterValue

# Syntax      : getTR181ParameterValue()
# Description : Function to Get the TR181 Parameter Value
# Parameters  : obj : TDKBTR181 Module Object
#             : sysobj : SYSUTIL Module Object
#             : param_name : TR181 Parameter Name
#             : tr181_ExpRes : Expected Value of TR181 Parameter
#             : setup_type : Type of execution, TDK/WEBPA/SNMP
# Return Value: tr181_result : Status of TR181 Parameter Get operation
#             : tr181_result : Value of TR181 Parameter

def getTR181ParameterValue(obj,sysobj,param_name,tr181_ExpRes,setup_type):
    exp_value_flag = 0;
    if setup_type == "TDK":
        tdkTestObj = obj.createTestStep("TDKB_TR181Stub_Get");
        tdkTestObj.addParameter("ParamName",param_name)
        tdkTestObj.executeTestCase(expectedresult);
        tr181_actualresult = tdkTestObj.getResult();
        tr181_result = tdkTestObj.getResultDetails().replace("\\n", "");
        print "TR181 tr181_result is %s"%tr181_result
    elif setup_type == "WEBPA":
        param = {'name':param_name}
        # Invoke webpa utility to post the query for get operation
        queryResponse = webpaQuery(sysobj,param);
        print "WEBPA queryResponse is ",queryResponse;
        parsedResponse = parseWebpaResponse(queryResponse, 1)
        tdkTestObj = sysobj.createTestStep('ExecuteCmd');
        tdkTestObj.executeTestCase(expectedresult);
        if "SUCCESS" in parsedResponse[0]:
            tr181_result = parsedResponse[1];
            tr181_actualresult = "SUCCESS"
        else:
            tr181_result = parsedResponse
            tr181_actualresult = "FAILURE"

    elif setup_type == "SNMP":
        oidvalues = param_name.split(":")
        paramType = oidvalues[0];
        oid = oidvalues[1];
        #mapping with the data type strings expected in SNMP response(STRING,INTEGER).This will be used as delimiter in response parsing
        typeDict={"string":"STRING","int":"INTEGER","unsignedint":"INTEGER","uint":"INTEGER","bool":"INTEGER","Gauge32":"Gauge32"}
        #send snmp query
        actResponse =snmplib.SnmpExecuteCmd("snmpget", commGetStr, "-v 2c", oid, ipaddress);
        tdkTestObj = sysobj.createTestStep('ExecuteCmd');
        tdkTestObj.executeTestCase(expectedresult);

        #check if the delimiter for paramtype is available in typeDict dictionary
        if typeDict.get(paramType, "nothing") == "nothing":
            tdkTestObj.setResultStatus("FAILURE");
            tr181_actualresult = "FAILURE"
            tr181_result = "Invalid datatype for SNMP get"
            #return (value, actualresult)
        else:
            #delimiter for response parsing, based on param type strings like STRING:,INTEGER:
            delimiter = typeDict.get(paramType)+":"
            if delimiter in actResponse:
                tr181_result = actResponse.split(delimiter)[1].strip().replace('"', '')
                tr181_actualresult = "SUCCESS"
            else:
                tr181_result = actResponse

    if tr181_ExpRes != "":
        if str(tr181_result).upper() == str(tr181_ExpRes).upper():
		    exp_value_flag = 1;
        else:
            exp_value_flag = 0;
    else:
        exp_value_flag = 1;

    if expectedresult in tr181_actualresult and exp_value_flag == 1:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1: Get the Value from TR181 parameter";
        print "EXPECTED RESULT 1: Should get the Value TR181 parameter";
        print "ACTUAL RESULT 1: Value is:%s" %tr181_result;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        tr181_actualresult = "FAILURE"
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1: Get the Value TR181 parameter";
        print "EXPECTED RESULT 1: Should get the Value TR181 parameter";
        print "ACTUAL RESULT 1: Value is:%s" %tr181_result;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";

    return tr181_actualresult,tr181_result;

# compareTR181andHALValues

# Syntax      : compareTR181andHALValues()
# Description : Function to Compare the TR181 Parameter Value with HAL API Value
# Parameters  : hal_result : Value of HAL API
#             : tr181_result : Value of TR181 Parameter
#             : tdkTestObj : TDKBTR181 Object to mark SUCCESS/FAILURE for comparison
#             : param_name : TR181 Parameter Name to addd it to failedparams list
# Return Value: failedparams : List of Failed Parameters

def compareTR181andHALValues(hal_result,tr181_result,tdkTestObj,param_name):
    global failedparams;

    print "HAL Result is %s"%hal_result
    print "TR181 Result is %s"%tr181_result
    if str(hal_result).upper().strip() == str(tr181_result).upper().strip():
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1: Compare TR181 Parameter value and value retrieved from HAL";
        print "EXPECTED RESULT 1: The values should match";
        print "ACTUAL RESULT 1: The values are matching ";
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1: Compare TR181 Parameter value and value retrieved from HAL";
        print "EXPECTED RESULT 1: The values should match";
        print "ACTUAL RESULT 1: The values are NOT matching ";
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";
        failedparams.append(param_name);

    return failedparams;

# getTR181andHALAPIValue

# Syntax      : getTR181andHALAPIValue()
# Description : Main Function to for TR181 HAL Value Comparision Utility
# Parameters  : obj : TDKBTR181 Module Object
#             : objhal : HAL Module Object
#             : sysobj : SYSUTIL Module object
#             : param_name : Name of the TR181 Parameter
#             : hal_primitive : Primitive Data type to get HAL API value
#             : scriptmodule : HAL Module Name
#             : setup_type : Type of operation : TDK/SNMP/WEBPA
# Return Value: failedparams : List of Failed Parameters

def getTR181andHALAPIValue(obj,objhal,sysobj,param_name,hal_primitive,tr181_ExpRes,hal_ExpRes,scriptmodule,setup_type):
    global failedparams;
    tr181_actualresult, tr181_result = getTR181ParameterValue(obj,sysobj,param_name,tr181_ExpRes,setup_type);
    hal_actualresult, hal_result , tdkTestObj = getHALAPIValue(objhal,hal_primitive,hal_ExpRes,scriptmodule);

    if tr181_actualresult == "SUCCESS" and hal_actualresult == "SUCCESS":
        if (tr181_ExpRes == "" ) and (hal_ExpRes == ""):
            failedparams = compareTR181andHALValues(hal_result,tr181_result,tdkTestObj,param_name);
    else:
        failedparams.append(param_name);
    return failedparams;
