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

from tdkbVariables import *;

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


# A utility function to get the public wifi parameters.
#
# Syntax       : GetPublicWiFiParamValues(obj)
#
# Parameters   : obj
#
# Return Value : Execution status

def GetPublicWiFiParamValues(obj):

    expectedresult="SUCCESS";
    status = "SUCCESS";

    actualresult= [];
    orgValue = [];
    paramList = ["Device.X_COMCAST-COM_GRE.Tunnel.1.DSCPMarkPolicy","Device.X_COMCAST-COM_GRE.Tunnel.1.PrimaryRemoteEndpoint","Device.X_COMCAST-COM_GRE.Tunnel.1.SecondaryRemoteEndpoint","Device.WiFi.SSID.5.SSID","Device.WiFi.SSID.6.SSID","Device.WiFi.SSID.5.Enable","Device.WiFi.SSID.6.Enable","Device.WiFi.AccessPoint.5.SSIDAdvertisementEnabled","Device.WiFi.AccessPoint.6.SSIDAdvertisementEnabled","Device.WiFi.SSID.10.SSID","Device.WiFi.SSID.10.Enable","Device.WiFi.AccessPoint.10.SSIDAdvertisementEnabled","Device.WiFi.AccessPoint.10.Security.ModeEnabled","Device.WiFi.AccessPoint.10.X_CISCO_COM_BssMaxNumSta","Device.WiFi.AccessPoint.10.Security.X_CISCO_COM_EncryptionMethod","Device.WiFi.AccessPoint.10.Security.RadiusServerIPAddr","Device.WiFi.AccessPoint.10.Security.RadiusServerPort","Device.WiFi.AccessPoint.10.Security.SecondaryRadiusServerIPAddr","Device.WiFi.AccessPoint.10.Security.SecondaryRadiusServerPort","Device.DeviceInfo.X_COMCAST_COM_xfinitywifiEnable"];
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
# Syntax       : SetPublicWiFiParamValues(obj,paramList)
#
# Parameters   : obj,paramList
#
# Return Value : Execution status

def SetPublicWiFiParamValues(obj,paramList):

        tdkTestObj = obj.createTestStep("WIFIAgent_SetMultiple");

        paramList1 = "Device.X_COMCAST-COM_GRE.Tunnel.1.DSCPMarkPolicy|%s|int|Device.X_COMCAST-COM_GRE.Tunnel.1.PrimaryRemoteEndpoint|%s|string|Device.X_COMCAST-COM_GRE.Tunnel.1.SecondaryRemoteEndpoint|%s|string" %(paramList[0],paramList[1],paramList[2])

        paramList2 = "Device.WiFi.SSID.5.SSID|%s|string|Device.WiFi.SSID.6.SSID|%s|string|Device.WiFi.SSID.5.Enable|%s|bool" %(paramList[3],paramList[4],paramList[5])

        paramList3 = "Device.WiFi.SSID.6.Enable|%s|bool|Device.WiFi.AccessPoint.5.SSIDAdvertisementEnabled|%s|bool|Device.WiFi.AccessPoint.6.SSIDAdvertisementEnabled|%s|bool"%(paramList[6],paramList[7],paramList[8])

        paramList4 = "Device.WiFi.SSID.10.SSID|%s|string|Device.WiFi.SSID.10.Enable|%s|bool|Device.WiFi.AccessPoint.10.SSIDAdvertisementEnabled|%s|bool" %(paramList[9],paramList[10],paramList[11])

        paramList5 = "Device.WiFi.AccessPoint.10.Security.ModeEnabled|%s|string|Device.WiFi.AccessPoint.10.X_CISCO_COM_BssMaxNumSta|%s|int|Device.WiFi.AccessPoint.10.Security.X_CISCO_COM_EncryptionMethod|%s|string" %(paramList[12],paramList[13],paramList[14])

        paramList6 = "Device.WiFi.AccessPoint.10.Security.RadiusServerIPAddr|%s|string|Device.WiFi.AccessPoint.10.Security.RadiusServerPort|%s|unsignedint|Device.WiFi.AccessPoint.10.Security.SecondaryRadiusServerIPAddr|%s|string"%(paramList[15],paramList[16],paramList[17])

        paramList7 = "Device.WiFi.AccessPoint.10.Security.SecondaryRadiusServerPort|%s|unsignedint"%paramList[18]

        paramList8 = "Device.DeviceInfo.X_COMCAST_COM_xfinitywifiEnable|%s|bool" %paramList[19];

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

        tdkTestObj.addParameter("paramList",paramList4);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult4 = tdkTestObj.getResult();
        details4 = tdkTestObj.getResultDetails();

        tdkTestObj.addParameter("paramList",paramList5);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult5 = tdkTestObj.getResult();
        details5 = tdkTestObj.getResultDetails();

        tdkTestObj.addParameter("paramList",paramList6);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult6 = tdkTestObj.getResult();
        details6 = tdkTestObj.getResultDetails();

        tdkTestObj.addParameter("paramList",paramList7);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult7 = tdkTestObj.getResult();
        details7 = tdkTestObj.getResultDetails();

        tdkTestObj.addParameter("paramList",paramList8);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult8 = tdkTestObj.getResult();
        details8 = tdkTestObj.getResultDetails();

        if expectedresult in actualresult1 and expectedresult in actualresult2 and expectedresult in actualresult3 and expectedresult in actualresult4 and expectedresult in actualresult5 and expectedresult in actualresult6 and  expectedresult in actualresult7 and  expectedresult in actualresult8:
            actualresult = "SUCCESS"
            details = "setPublicWiFiParamValues success"
        else:
            actualresult = "FAILURE"
            details = "setPublicWiFiParamValues failed"
        return (tdkTestObj,actualresult,details);

################################### End of Function #####################################


# A utility function to get the platform specific parameters.
#
# Syntax       : parsePublicWiFiConfigValues(sysobj)
#
# Parameters   : obj
#
# Return Value : Execution status
#################################################################################

def parsePublicWiFiConfigValues(sysobj):

   tdkTestObj_Sys_ExeCmd = sysobj.createTestStep('ExecuteCmd');
   details1 = "sh %s/tdk_utility.sh parseConfigFile DSCPMARKPOLICY" %TDK_PATH;
   details2 = "sh %s/tdk_utility.sh parseConfigFile PRIMARYREMOTEENDPOINT" %TDK_PATH;
   details3 = "sh %s/tdk_utility.sh parseConfigFile SECONDARYREMOTEENDPOINT" %TDK_PATH;
   details4 = "sh %s/tdk_utility.sh parseConfigFile PUBLIC_WIFI_SSID_NAME " %TDK_PATH;
   details5 = "sh %s/tdk_utility.sh parseConfigFile PUBLIC_WIFI_MODE_ENABLED" %TDK_PATH;
   details6 = "sh %s/tdk_utility.sh parseConfigFile PUBLIC_WIFI_BSS_MAX_NUM_STA" %TDK_PATH;
   details7 = "sh %s/tdk_utility.sh parseConfigFile PUBLIC_WIFI_ENCRYPTION_METHOD" %TDK_PATH;
   details8 = "sh %s/tdk_utility.sh parseConfigFile PUBLIC_WIFI_RADIUS_SERVER_IPADDR" %TDK_PATH;
   details9 = "sh %s/tdk_utility.sh parseConfigFile PUBLIC_WIFI_RADIUS_SERVER_PORT" %TDK_PATH;

   print details1;
   print details2;
   print details3;
   print details4;
   print details5;
   print details6;
   print details7;
   print details8;
   print details9;

   expectedresult="SUCCESS";
   tdkTestObj_Sys_ExeCmd.addParameter("command", details1);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult1 = tdkTestObj_Sys_ExeCmd.getResult();
   DSCPMarkPolicy = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details2);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult2 = tdkTestObj_Sys_ExeCmd.getResult();
   PrimaryRemoteEndpoint = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details3);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult3 = tdkTestObj_Sys_ExeCmd.getResult();
   SecondaryRemoteEndpoint = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details4);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult4 = tdkTestObj_Sys_ExeCmd.getResult();
   SSIDName = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details5);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult5 = tdkTestObj_Sys_ExeCmd.getResult();
   ModeEnabled = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details6);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult6 = tdkTestObj_Sys_ExeCmd.getResult();
   BssMaxNumSta = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details7);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult7 = tdkTestObj_Sys_ExeCmd.getResult();
   EncryptionMethod = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details8);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult8 = tdkTestObj_Sys_ExeCmd.getResult();
   RadiusServerIPAddr = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   tdkTestObj_Sys_ExeCmd.addParameter("command", details9);
   tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
   actualresult9 = tdkTestObj_Sys_ExeCmd.getResult();
   RadiusServerPort = tdkTestObj_Sys_ExeCmd.getResultDetails().replace("\\n", "");

   if expectedresult in actualresult1 and expectedresult in actualresult2 and expectedresult in actualresult3 and expectedresult in actualresult4 and expectedresult in actualresult5 and expectedresult in actualresult6 and  expectedresult in actualresult7 and  expectedresult in actualresult8 and expectedresult in actualresult9 and DSCPMarkPolicy != "" and PrimaryRemoteEndpoint!= "" and SecondaryRemoteEndpoint!= ""  and SSIDName != "" and ModeEnabled != "" and BssMaxNumSta!= "" and EncryptionMethod != "" and RadiusServerIPAddr != "" and RadiusServerPort != "":
      actualresult = "SUCCESS"
      details = "getSetValues success"
   else:
       actualresult = "FAILURE"
       details = "getSetValues failed"

   setvalues = [DSCPMarkPolicy,PrimaryRemoteEndpoint,SecondaryRemoteEndpoint,SSIDName,ModeEnabled,BssMaxNumSta,EncryptionMethod,RadiusServerIPAddr,RadiusServerPort];

   return setvalues,tdkTestObj_Sys_ExeCmd,actualresult;
