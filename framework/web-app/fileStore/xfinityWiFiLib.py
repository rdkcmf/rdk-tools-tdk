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

# A utility function to get the public wifi parameters.
#
# Syntax       : getPublicWiFiParamValues(obj)
#
# Parameters   : obj
#
# Return Value : Execution status

def getPublicWiFiParamValues(obj):

    expectedresult="SUCCESS";
    status = "SUCCESS";

    actualresult= [];
    orgValue = [];
    paramList = ["Device.X_COMCAST-COM_GRE.Tunnel.1.DSCPMarkPolicy","Device.X_COMCAST-COM_GRE.Tunnel.1.PrimaryRemoteEndpoint","Device.X_COMCAST-COM_GRE.Tunnel.1.SecondaryRemoteEndpoint","Device.WiFi.SSID.5.Enable","Device.WiFi.SSID.6.Enable","Device.DeviceInfo.X_COMCAST_COM_xfinitywifiEnable"];
    #Parse and store the values retrieved in a list
    for index in range(len(paramList)):
        tdkTestObj = obj.createTestStep("WIFIAgent_Get");
        tdkTestObj.addParameter("paramName",paramList[index])
        tdkTestObj.executeTestCase(expectedresult);
        actualresult.append(tdkTestObj.getResult())
        details = tdkTestObj.getResultDetails();
        if "VALUE:" in details:
                orgValue.append( details.split("VALUE:")[1].split(' ')[0] );

    for index in range(len(paramList)):
        if expectedresult not in actualresult[index]:
            status = "FAILURE";
            break;

    return (tdkTestObj,status,orgValue);

################################ End of Function #####################################

# A utility function to enable the public wifi parameters.
#
# Syntax       : setPublicWiFiParamValues(obj,paramList)
#
# Parameters   : obj,paramList
#
# Return Value : Execution status

def setPublicWiFiParamValues(obj,paramList):

        tdkTestObj = obj.createTestStep("WIFIAgent_SetMultiple");
	paramList1 = "Device.X_COMCAST-COM_GRE.Tunnel.1.DSCPMarkPolicy|%s|int|Device.X_COMCAST-COM_GRE.Tunnel.1.PrimaryRemoteEndpoint|%s|string|Device.X_COMCAST-COM_GRE.Tunnel.1.SecondaryRemoteEndpoint|%s|string" %(paramList[0],paramList[1],paramList[2])

	paramList2 = "Device.WiFi.SSID.5.SSID|xwifi-2.4|string|Device.WiFi.SSID.6.SSID|xwifi-5|string|Device.WiFi.SSID.5.Enable|%s|bool|Device.WiFi.SSID.6.Enable|%s|bool" %(paramList[3],paramList[4])

	paramList3 = "Device.DeviceInfo.X_COMCAST_COM_xfinitywifiEnable|%s|bool" %paramList[5]

        expectedresult="SUCCESS";
        tdkTestObj.addParameter("paramList",paramList1);
        tdkTestObj.executeTestCase(expectedresult);
	actualresult1 = tdkTestObj.getResult();
        details1 = tdkTestObj.getResultDetails();

	tdkTestObj.addParameter("paramList",paramList2);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult2 = tdkTestObj.getResult();
        details2 = tdkTestObj.getResultDetails();

	tdkTestObj.addParameter("paramList",paramList3);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult3 = tdkTestObj.getResult();
        details3 = tdkTestObj.getResultDetails();
	if expectedresult in actualresult1 and expectedresult in actualresult2 and expectedresult in actualresult3:
	    actualresult = "SUCCESS"
	    details = "setPublicWiFiParamValues success"
	else:
	    actualresult = "FAILURE"
            details = "setPublicWiFiParamValues failed"
        return (tdkTestObj,actualresult,details);

################################### End of Function #####################################

