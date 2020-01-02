import xml.etree.ElementTree as ET
import tdklib
from time import sleep
import os
import webpaUtility;
from webpaUtility import *

#community strings and ipaddress for snmp validation
commGetStr = ""
ipaddress = ""
commSetStr = ""
# setAllParams

# Syntax      : setAllParams()
# Description : Function to set all parameters in a module
# Parameters  : tr181Obj - tr181 module object
#             : sysObj - sysUtil object
#             : setup_type : Type of execution, TDK/WEBPA/SNMP
#             : module - module to be validated
# Return Value: SUCCESS/FAILURE
def setAllParams(module, setup_type, tr181Obj, sysObj):

    failedParams = [];
    moduleStatus = "SUCCESS"

    print "\n------------------------------------------------------------------------"
    print "SET VALUES OF ALL NAMESPACES IN ", module;
    print "------------------------------------------------------------------------\n"

    tdkTestObj = sysObj.createTestStep('ExecuteCmd');
    deviceType= "sh %s/tdk_utility.sh parseConfigFile DEVICETYPE" %TDK_PATH
    print deviceType;

    #get the community strings and ipaddress for snmp validation
    global commGetStr, ipaddress, commSetStr
    commGetStr = snmplib.getCommunityString(sysObj,"snmpget");
    ipaddress = snmplib.getIPAddress(sysObj);
    commSetStr = snmplib.getCommunityString(sysObj,"snmpset");

    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command", deviceType);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    deviceType = tdkTestObj.getResultDetails().strip();
    deviceType = deviceType.replace("\\n", "");
    if "Invalid Argument passed" not in deviceType:
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
	return moduleStatus,failedParams;

    xmlName = deviceType + module + "Params.xml"
    xmlPath = os.path.dirname(os.path.realpath(__file__))
    paramListXml = xmlPath + "/tdkbModuleConfig" + "/" + xmlName
#       paramListXml = TR181_XML_PATH + deviceType + module + "Params.xml"
    print "The name of param list xml file is ", paramListXml;

    tree = ET.parse(paramListXml)
    paramsRoot = tree.getroot()

    paramList = []
    for param in paramsRoot:
        paramList.append(param.find('name').text)

    print "PARAMS TO BE SET ARE: ",paramList

    for param in paramsRoot:
        #Get the value of each param
        paramType = param.find('type').text
        writable = param.find('writable').text
        persistentSet = param.find('persistentSet').text
	#some parameters will have expected set of values and some may not
        if param.find('expectedValues') is not None:
            expectedValues = param.find('expectedValues').text
            #if expectedValues in xml is non-empty
            if expectedValues is not None:
                expectedValues = expectedValues.split(",")
            else:
                expectedValues = ""
        #if expectedValues is not known and that tag itself is not available in xml
	else:
	    expectedValues = ""
	    #the value used for set is chosen from expectedValues. If that tag is not available, look for setValue tag
            if param.find('setValue') is not None:
		setValue = param.find('setValue').text
	    #if the parameter is writable, it will be called for set operation. In that case setValue tag must be present if there is no expectedValues tag
	    elif writable == "true":
		print "ERROR: Neither expectedValues nor setvalue available for the set operation of parameter ",param.find('name').text
                moduleStatus = "FAILURE";
		failedParams.append(paramName);
                return moduleStatus,failedParams;

        if setup_type == "TDK":
            paramName = param.find('name').text
        elif setup_type == "WEBPA":
            paramName = param.find('webpaName').text
            #for some params expected value or default value may differ for webpa
            if param.find('webpaExpectedValues')is not None:
                expectedValues = param.find('webpaExpectedValues').text
                expectedValues = expectedValues.split(",")
        elif setup_type == "SNMP":
            if param.find('oid')is not None:
                paramName = param.find('oid').text
            #if snmp details of one param is not available, skip that param
            else:
                print "OID not available for %s, skipping this parameter" %param.find('name').text
                continue;
	    #get the snmp specific param details
    	    if param.find('snmpExpectedValues')is not None:
    	        expectedValues = param.find('snmpExpectedValues').text
    	        expectedValues = expectedValues.split(",")
	    if param.find('snmpType') is not None:
		paramType = param.find('snmpType').text
        else:
            moduleStatus = "FAILURE";
	    print "Invalid setup_type passed, setupType should be one fom TDK, WEBPA or SNMP"
            return moduleStatus,failedParams;

        expectedresult="SUCCESS";

	#get and save the original value before doing set
        if writable == "true":
	    print "*************Start validation of %s **************" %paramName
            value,actualresult = getParameterValue(tr181Obj, sysObj, setup_type, paramName, paramType, expectedValues)

	    #choose a value to be set from the expected value list
            if expectedresult in actualresult:
                orgValue = value
		#if no expected values are there for the parameter, use the setValue field in xml directly, otherwise chose one setvalue from expectedValues list
		if expectedValues != "":
                    for newValue in expectedValues:
                       if orgValue != newValue:
                            setValue = newValue
    		            break
                #set a new value from expected value list
                detail, actualresult = setParameterValue(tr181Obj, sysObj, setup_type, paramName, setValue, paramType);

                if expectedresult in actualresult:
		    #For WiFi parameters wait for set operation to be reflected
		    if module == "WIFI":
			sleep(60)
                    value,actualresult = getParameterValue(tr181Obj, sysObj, setup_type, paramName, paramType, setValue)
                    if expectedresult in actualresult:

			#revert the value after set
                	detail, actualresult = setParameterValue(tr181Obj, sysObj, setup_type, paramName, orgValue, paramType);
                	if expectedresult in actualresult:
			    moduleStatus = "SUCCESS";
                	    print "Successfully reverted the value"
                            print "*************Set validation of %s is SUCCESS**************\n" %paramName
                	else:
                	    print "Revert operation failed"
    			    moduleStatus = "FAILURE";
			    failedParams.append(paramName);
                            print "*************Set validation with get is FAILURE for %s**************\n" %paramName
                    else:
                	moduleStatus = "FAILURE";
			failedParams.append(paramName);
                else:
                    moduleStatus = "FAILURE";
		    print "Set operation failed for %s" %paramName
		    failedParams.append(paramName);
            else:
                moduleStatus = "FAILURE";
		print "Get operation faied for %s" %paramName
                failedParams.append(paramName);
	    #adding sleep time in between to avoid WEBPA error
            if setup_type == "WEBPA":
    	        print "Sleeping for 90sec"
                sleep(90)

    return moduleStatus,failedParams;



# getAllParams

# Syntax      : getAllParams()
# Description : Function to get and verify all parameters'value in a module with or without factory reset
# Parameters  : tr181Obj - module object
#             : sysObj - sysUtil object
#             : setup_type : Type of execution, TDK/WEBPA/SNMP
#             : module - module to be validated
#             : factoryReset - whether a factory reset was done before get operation or not
# Return Value: SUCCESS/FAILURE

def getAllParams(module, setup_type, factoryReset, tr181Obj, sysObj):

    failedParams = [];
    moduleStatus = "SUCCESS"

    print "\n------------------------------------------------------------------------"
    print "GET VALUES OF ALL NAMESPACES IN ", module;
    print "------------------------------------------------------------------------\n"

    tdkTestObj = sysObj.createTestStep('ExecuteCmd');
    deviceType= "sh %s/tdk_utility.sh parseConfigFile DEVICETYPE" %TDK_PATH
    print deviceType;

    #get the community strings and ipaddress for snmp validation
    global commGetStr, ipaddress, commSetStr
    commGetStr = snmplib.getCommunityString(sysObj,"snmpget");
    ipaddress = snmplib.getIPAddress(sysObj);
    commSetStr = snmplib.getCommunityString(sysObj,"snmpset");

    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command", deviceType);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    deviceType = tdkTestObj.getResultDetails().strip();
    deviceType = deviceType.replace("\\n", "");
    if "Invalid Argument passed" not in deviceType:
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
        return moduleStatus,failedParams;

    xmlName = deviceType + module + "Params.xml"
    xmlPath = os.path.dirname(os.path.realpath(__file__))
    paramListXml = xmlPath + "/tdkbModuleConfig" + "/" + xmlName
    #The xml file path for the particular module
#    paramListXml = TR181_XML_PATH + deviceType + module + "Params.xml"
    print "The name of param list xml file is ", paramListXml;

    tree = ET.parse(paramListXml)
    paramsRoot = tree.getroot()

    paramList = []
    for param in paramsRoot:
        paramList.append(param.find('name').text)

    print "PARAMS TO BE GET ARE: ",paramList

    for param in paramsRoot:
	#for some params default value is not applicable, skip
	if factoryReset == "true" and param.find('defaultValue') is None:
	    continue;
        #Get the value of each param
        if param.find('defaultValue') is not None:
            defaultValue = param.find('defaultValue').text
	    #if default value given xml is empty
	    if defaultValue is None:
		defaultValue = ""
        paramType = param.find('type').text
	#some parameters will have expected set of values and some may not
        if param.find('expectedValues')is not None:
            expectedValues = param.find('expectedValues').text
	    #if expectedValues in xml is non-empty
	    if expectedValues is not None:
                expectedValues = expectedValues.split(",")
	    else:
		expectedValues = ""
	#if expectedValues is not known and that tag itself is not available in xml
        else:
            expectedValues = ""

        if setup_type == "TDK":
            paramName = param.find('name').text
        elif setup_type == "WEBPA":
            paramName = param.find('webpaName').text
	    #for some params expected value or default value may differ for webpa
	    if param.find('webpaExpectedValues')is not None:
                expectedValues = param.find('webpaExpectedValues').text
                expectedValues = expectedValues.split(",")
            if param.find('webpaDefaultValue')is not None:
                defaultValue = param.find('webpaDefaultValue').text
        elif setup_type == "SNMP":
            if param.find('oid')is not None:
                paramName = param.find('oid').text
            #if snmp details of one param is not available, skip that param
            else:
                print "OID not available for %s, skipping this parameter" %param.find('name').text
                continue;
            if param.find('snmpExpectedValues')is not None:
                expectedValues = param.find('snmpExpectedValues').text
                expectedValues = expectedValues.split(",")
            if param.find('snmpDefaultValue')is not None:
                defaultValue = param.find('snmpDefaultValue').text
            if param.find('snmpType') is not None:
                paramType = param.find('snmpType').text
        else:
            moduleStatus = "FAILURE";
	    print "Invalid setup_type passed, setupType should be one fom TDK, WEBPA or SNMP"
            return moduleStatus,failedParams;
        expectedresult="SUCCESS";

	print "*************Start validation of %s **************" %paramName
	#if get operation is to be done with factory reset, cross check parameter's get value with default value list other wise with expectedvalues list
        if factoryReset == "false":
            value,actualresult = getParameterValue(tr181Obj, sysObj, setup_type, paramName, paramType, expectedValues)
        else:
            value,actualresult = getParameterValue(tr181Obj, sysObj, setup_type, paramName, paramType, defaultValue)

        if expectedresult in actualresult:
            print "*************Get validation of %s is SUCCESS**************\n" %paramName
        else:
            print "*************Get validation of %s is FAILURE**************\n" %paramName
            moduleStatus = "FAILURE";
            failedParams.append(paramName);

    return moduleStatus,failedParams;


def getParameterValue(tr181Obj, sysObj, setup_type, paramName, paramType, expectedValues):

# getParameterValue

# Syntax      : getParameterValue()
# Description : Function to get the value of parameter
# Parameters  : tr181Obj - tr181 module object
#             : sysObj - sysUtil object
#             : setup_type : Type of execution, TDK/WEBPA
#             : paramType : Type of the Parameter
#             : paramName - Parameter name
# Return Value: SUCCESS/FAILURE

    expectedresult="SUCCESS";

    actualresult= [];

    if setup_type == "TDK":
        tdkTestObj = tr181Obj.createTestStep("TDKB_TR181Stub_Get");
        tdkTestObj.addParameter("ParamName",paramName)
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        value = tdkTestObj.getResultDetails();
    elif setup_type == "WEBPA" :
        # Modify the input parameter type to the format webpa is expecting
        param = {'name':paramName}

        # Invoke webpa utility to post the query for get operation
        queryResponse = webpaQuery(sysObj,param)
        parsedResponse = parseWebpaResponse(queryResponse, 1)
        tdkTestObj = sysObj.createTestStep('ExecuteCmd');
        tdkTestObj.executeTestCase(expectedresult);
        if "SUCCESS" in parsedResponse[0]:
                value = parsedResponse[1];
                actualresult = "SUCCESS"
        else:
                value = parsedResponse
                actualresult = "FAILURE"
    else:
	oid = paramName
	#mapping with the data type strings expected in SNMP response(STRING,INTEGER).This will be used as delimiter in response parsing
        typeDict={"string":"STRING","int":"INTEGER","unsignedint":"INTEGER","uint":"INTEGER","bool":"INTEGER","Gauge32":"Gauge32"}
	#send snmp query
	actResponse =snmplib.SnmpExecuteCmd("snmpget", commGetStr, "-v 2c", oid, ipaddress);
        tdkTestObj = sysObj.createTestStep('ExecuteCmd');
	tdkTestObj.executeTestCase(expectedresult);

	#check if the delimiter for paramtype is available in typeDict dictionary
        if typeDict.get(paramType, "nothing") == "nothing":
            tdkTestObj.setResultStatus("FAILURE");
            actualresult = "FAILURE"
            value = "Invalid datatype for SNMP get"
            return (value, actualresult)

	#delimiter for response parsing, based on param type strings like STRING:,INTEGER:
	delimiter = typeDict.get(paramType)+":"
	if delimiter in actResponse:
	    value = actResponse.split(delimiter)[1].strip().replace('"', '')
	    actualresult = "SUCCESS"
	else:
            value = actResponse
            actualresult = "FAILURE"

    #if there are is no expected value tag, then check if getvalue is non-empty, otherwise getvalue should be in exepectedValues list
    if (expectedresult in actualresult) and (expectedValues == "" and value!="") or (value in expectedValues and value!="") or (value!="" and ',' in value) or (expectedValues == "" and value ==""):
	#if the get value has comma, split the value at commas and check each value against expected values
        if expectedValues != "" and ',' in value:
            value = value.split(',')
            for val in value:
                if val not in expectedValues:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE");
                    actualresult = "FAILURE"
                    print "TEST STEP : Get the value of param", paramName;
                    print "EXPECTED RESULT: Should get one of the values from ", expectedValues;
                    print "ACTUAL RESULT : %s" %value;
                    print "TEST EXECUTION RESULT: FAILURE"
                    print "--------------------------------------------------------------------------------------"
    		    return (value,actualresult);
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP: Get the value of param", paramName;
        print "EXPECTED RESULT: Should get one of the values from ", expectedValues;
        print "ACTUAL RESULT  : %s" %value;
        print "TEST EXECUTION RESULT: SUCCESS"
        print "--------------------------------------------------------------------------------------"

    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
	actualresult = "FAILURE"
        print "TEST STEP : Get the value of param", paramName;
        print "EXPECTED RESULT: Should get one of the values from ", expectedValues;
        print "ACTUAL RESULT : %s" %value;
        print "TEST EXECUTION RESULT: FAILURE"
        print "--------------------------------------------------------------------------------------"

    return (value,actualresult);

############################################# End of Function #################################################


def setParameterValue(tr181Obj, sysObj, setup_type, paramName, setValue, paramType):

# setParameterValue

# Syntax      : setParameterValue()
# Description : Function to get the value of parameter
# Parameters  : tr181Obj - tr181 module object
#             : sysObj - sysUtil object
#             : setup_type : Type of execution, TDK/WEBPA
#             : paramName - Parameter name
#             : setValue - value to be set
#             : paramType - Parameter type
# Return Value: SUCCESS/FAILURE

    expectedresult="SUCCESS";

    actualresult= [];

    if setup_type == "TDK":
        tdkTestObj = tr181Obj.createTestStep("TDKB_TR181Stub_Set");
        tdkTestObj.addParameter("ParamName",paramName)
        tdkTestObj.addParameter("ParamValue", setValue);
        tdkTestObj.addParameter("Type",paramType);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        detail = tdkTestObj.getResultDetails();
    elif setup_type == "WEBPA" :
	#dummy testobj for marking test status
        tdkTestObj = sysObj.createTestStep('ExecuteCmd');
        tdkTestObj.executeTestCase(expectedresult);

        # Modify the input parameter type to the format webpa is expecting
        param = {'name':paramName}
        typeDict={"string":0,"int":1,"unsignedint":2,"uint":2, "bool":3}
	#check if the param type passed is valid
	if typeDict.get(paramType, "nothing") == "nothing":
	    tdkTestObj.setResultStatus("FAILURE");
	    actualresult = "FAILURE"
	    detail = "Invalid datatype for WEBPA set"
	    print "Invalid datatype for WEBPA set"
	    return (detail, actualresult)

        # Invoke webpa utility to post the query for set operation
        queryParam = {"name":paramName, "value":setValue, "dataType":typeDict.get(paramType)}
        queryResponse = webpaQuery(tr181Obj, queryParam, "set")
        parsedResponse = parseWebpaResponse(queryResponse, 1, "set")

        if "SUCCESS" in parsedResponse[0]:
                detail = "WEBPA set succes";
                actualresult = "SUCCESS"
        else:
                detail = "WEBPA query failed"
                actualresult = "FAILURE"
    else:
        tdkTestObj = sysObj.createTestStep('ExecuteCmd');
        tdkTestObj.executeTestCase(expectedresult);

	#delimiter for different parameter type
        delimitDict={"string":"STRING","int":"INTEGER","unsignedint":"INTEGER","uint":"INTEGER","bool":"INTEGER","Gauge32":"Gauge32"}

	#parameter type mapping for snmp query
        typeDict={"string":"s","int":"i","unsignedint":"i","uint":"i","bool":"i","Gauge32":"u"}
        if delimitDict.get(paramType, "nothing") == "nothing":
            tdkTestObj.setResultStatus("FAILURE");
            actualresult = "FAILURE"
            detail = "Invalid datatype for SNMP set"
	    print "Invalid datatype for SNMP set"
            return (value, actualresult)

	oid = paramName+" "+typeDict.get(paramType)+" "+setValue
        actResponse =snmplib.SnmpExecuteCmd("snmpset", commSetStr, "-t 10 -v 2c", oid , ipaddress);

	#If snmp query is success, response should have one of the pattern(delimiter) like STRING:, INTEGER:
        delimiter = delimitDict.get(paramType)+":"
        if delimiter in actResponse:
            detail = "SNMP set operation is success"
            actualresult = "SUCCESS"
        else:
            detail = "SNMP set failed"
            actualresult = "FAILURE"

    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP: Set the value of param", paramName;
        print "EXPECTED RESULT: Should set the value of param as ", setValue;
        print "ACTUAL RESULT  : %s" %detail
        print "TEST EXECUTION RESULT: SUCCESS"
        print "--------------------------------------------------------------------------------------"
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP : Set the value of param", paramName;
        print "EXPECTED RESULT: Should set the value of param as ", setValue;
        print "ACTUAL RESULT : %s" %detail
        print "TEST EXECUTION RESULT: FAILURE"
        print "--------------------------------------------------------------------------------------"

    return (detail, actualresult);

############################################# End of Function #################################################

