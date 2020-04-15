/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2018 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

#include "WIFIHAL.h"
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string WIFIHAL::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE,"\n testmodulepre_requisites ----->Entry\n");
    int returnValue;
    char details[200] = {'\0'};
    returnValue = wifi_init();
    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n testmodulepre_requisites ---> Initialize SUCCESS !!! \n");
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFIHAL testmodulepre_requisites --->Exit\n");
        return "SUCCESS";
    }
    else
    {
       DEBUG_PRINT(DEBUG_TRACE,"\n testmodulepre_requisites --->Failed to initialize !!! \n");
       DEBUG_PRINT(DEBUG_TRACE,"\n WIFIHAL testmodulepre_requisites --->Exit\n");
       return "FAILURE";
    }
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool WIFIHAL::testmodulepost_requisites()
{
    return true;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "WIFIHAL".
**************************************************************************/

extern "C" WIFIHAL* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new WIFIHAL(ptrtcpServer);
}

/***************************************************************************
 *Function name : initialize
 *Description    : Initialize Function will be used for registering the wrapper method
 *                with the agent so that wrapper functions will be used in the
 *                script
 *****************************************************************************/

bool WIFIHAL::initialize(IN const char* szVersion)
{
    return TEST_SUCCESS;
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_Init
 * Description          : This function invokes WiFi hal api wifi_init()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_Init (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Init ----->Entry\n");

    int returnValue;
    char details[200] = {'\0'};

    returnValue = wifi_init();
    if(0 == returnValue)
       {
            sprintf(details, "wifi_init operation success");
            response["result"]="SUCCESS";
            response["details"]=details;
            return;
       }
    else
       {
            sprintf(details, "wifi_init operation failed");
            response["result"]="FAILURE";
            response["details"]=details;
            return;
       }
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Init --->Exit\n");
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_Down
 * Description          : This function invokes WiFi hal api wifi_down()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_Down (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Down ----->Entry\n");

    int returnValue;
    char details[200] = {'\0'};
    returnValue = wifi_down();
    if(0 == returnValue)
       {
            sprintf(details, "wifi_down operation success");
            response["result"]="SUCCESS";
            response["details"]=details;
       }
    else
       {
            sprintf(details, "wifi_down operation failed");
            response["result"]="FAILURE";
            response["details"]=details;
            return;
       }
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Down --->Exit\n");
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_Uninit
 * Description          : This function invokes WiFi hal api wifi_uninit()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_Uninit (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Uninit ----->Entry\n");

    int returnValue;
    char details[200] = {'\0'};

    returnValue = wifi_uninit();
    if(0 == returnValue)
       {
            sprintf(details, "wifi_uninit operation success");
            response["result"]="SUCCESS";
            response["details"]=details;
            return;
       }
    else
       {
            sprintf(details, "wifi_uninit operation failed");
            response["result"]="FAILURE";
            response["details"]=details;
            return;
       }
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Uninit --->Exit\n");
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetParamStringValue
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is string
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          param     - the string value to be get/set
                          paramType  - To indicate negative test scenario. it is set as NULL for negative sceanario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetParamStringValue(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFIHAL_GetOrSetParamStringValue --->Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex;
    char output[1000] = {'\0'};
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};
    char param[200] = {'\0'};

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    strcpy(paramType, req["paramType"].asCString());
    strcpy(param, req["param"].asCString());
    if(!strcmp(methodName, "getRadioSupportedFrequencyBands"))
        returnValue = wifi_getRadioSupportedFrequencyBands(radioIndex,output);
    else if(!strcmp(methodName, "getRadioIfName"))
	returnValue = wifi_getRadioIfName(radioIndex,output);
    else if(!strcmp(methodName, "getRadioOperatingFrequencyBand"))
	returnValue = wifi_getRadioOperatingFrequencyBand(radioIndex,output);
    else if(!strcmp(methodName, "getRadioSupportedStandards"))
	returnValue = wifi_getRadioSupportedStandards(radioIndex,output);
    else if(!strcmp(methodName, "getRadioPossibleChannels"))
	returnValue = wifi_getRadioPossibleChannels(radioIndex,output);
    else if(!strcmp(methodName, "getRadioChannelsInUse"))
	returnValue = wifi_getRadioChannelsInUse(radioIndex,output);
    else if(!strcmp(methodName, "getRadioOperatingChannelBandwidth"))
	returnValue = wifi_getRadioOperatingChannelBandwidth(radioIndex,output);
    else if(!strcmp(methodName, "getRegulatoryDomain"))
        returnValue = wifi_getRegulatoryDomain(radioIndex,output);
    else if(!strcmp(methodName, "getSSIDName"))
        returnValue = wifi_getSSIDName(radioIndex,output);
    else if(!strcmp(methodName, "getBaseBSSID"))
        returnValue = wifi_getBaseBSSID(radioIndex,output);
    else if(!strcmp(methodName, "getSSIDMACAddress"))
        returnValue = wifi_getSSIDMACAddress(radioIndex,output);
    else if(!strcmp(methodName, "getRadioStatus"))
        returnValue = wifi_getRadioStatus(radioIndex,output);
    else if(!strcmp(methodName, "getRadioExtChannel"))
        returnValue = wifi_getRadioExtChannel(radioIndex,output);
    else if(!strcmp(methodName, "getHalVersion"))
        returnValue = wifi_getHalVersion(output);
    else if(!strcmp(methodName, "getCliWpsConfigMethodsSupported"))
        returnValue = wifi_getCliWpsConfigMethodsSupported(radioIndex,output);
    else if(!strcmp(methodName, "getCliWpsConfigMethodsEnabled"))
        returnValue = wifi_getCliWpsConfigMethodsEnabled(radioIndex,output);
    else if(!strcmp(methodName, "setCliWpsConfigMethodsEnabled"))
        returnValue = wifi_setCliWpsConfigMethodsEnabled(radioIndex,output);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFIHAL_GetOrSetParamStringValue: Invalid methodName\n");
    }

    printf("return status of the api call: %d\n",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "output : %s", output);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE,"\n WIFIHAL_GetOrSetParamStringValue --->Exit\n");
    return;
}


/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetParamULongValue
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is Unsigned long
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                         radioIndex - radio index value of wifi
                         param     - the ulong value to be get/set
                         paramType  - To indicate negative test scenario. it is set as NULL for negative scenario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetParamULongValue(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamULongValue------>Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex = 1;
    unsigned long uLongVar = 1;
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    uLongVar = (unsigned long)req["param"].asLargestUInt();
    strcpy(paramType, req["paramType"].asCString());

    if(!strcmp(methodName, "getRadioChannel"))
        returnValue = wifi_getRadioChannel(radioIndex,&uLongVar);
    else if(!strcmp(methodName, "getRadioNumberOfEntries"))
        returnValue = wifi_getRadioNumberOfEntries(&uLongVar);
    else if(!strcmp(methodName, "getSSIDNumberOfEntries"))
        returnValue = wifi_getSSIDNumberOfEntries(&uLongVar);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFI_HAL_GetOrSetParamULongValue: Invalid methodName\n");
	return;
    }
    printf("return status of the api call: %d",returnValue);

    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n output: %lu\n",uLongVar);
        sprintf(details, "Value returned is :%lu", uLongVar);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamULongValue --->Exit\n");
    return;
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetParamBoolValue
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is BOOL
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          enable     - the bool value to be get/set
                          paramType  - To indicate negative test scenario. it is set as NULL for negative scenario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetParamBoolValue(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamBoolValue --->Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex;
    unsigned char enable;
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    enable = req["param"].asInt();
    strcpy(paramType, req["paramType"].asCString());

    if(!strcmp(methodName, "getRadioEnable"))
        returnValue = wifi_getRadioEnable(radioIndex,&enable);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFI_HAL_GetOrSetParamULongValue: Invalid methodName\n");
        return;
    }
    printf("return status of the api call: %d",returnValue);

    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n enable: %u\n",enable);
        sprintf(details, "Value returned is :%u", enable);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamBoolValue --->Exit\n");
    return;
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetRadioStandard
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is a string
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          param     - the string value to be get
                          paramType  - To indicate negative test scenario. it is set as NULL for negative scenario, otherwise empty
                          gOnly, nOnly, acOnly - the bool values to be set/get
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetRadioStandard(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamRadioStandard ----->Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex = 1;
    char output[1000] = {'\0'};
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};
    char param[200] = {'\0'};
    unsigned char gOnly, nOnly, acOnly;

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    strcpy(paramType, req["paramType"].asCString());
    strcpy(param, req["param"].asCString());

    if(!strcmp(methodName, "getRadioStandard"))
        returnValue = wifi_getRadioStandard(radioIndex, output, &gOnly, &nOnly, &acOnly);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFI_HAL_GetOrSetRadioStandard: Invalid methodName\n");
        return;
    }
    printf("returnValue: %d",returnValue);
//add apply settings steps here

    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n output: %s\n",output);
        sprintf(details, "Value returned is :output=%s,gOnly=%d,nOnly=%d,acOnly=%d", output,gOnly,nOnly,acOnly);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WiFiCallMethodForRadioStandard --->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFIHAL_GetRadiotrafficStats
 * Description          : This function invokes WiFi hal get api which are
                          related to wifi_getRadiotrafficStats()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetRadioTrafficStats (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetRadiotrafficStats ----->Entry\n");
    wifi_radioTrafficStats_t trafficStats;
    int radioIndex = 1;
    int returnValue;
    char details[1000] = {'\0'};
    radioIndex = req["radioIndex"].asInt();
    returnValue = wifi_getRadioTrafficStats(radioIndex, &trafficStats);
    if(0 == returnValue)
    {
        sprintf(details, "Value returned is :radio_BytesSent=%lu,radio_BytesReceived=%lu,radio_PacketsSent=%lu,radio_PacketsReceived=%lu,radio_ErrorsSent=%lu,radio_ErrorsReceived=%lu,radio_DiscardPacketsSent=%lu,radio_DiscardPacketsReceived=%lu,radio_PLCPErrorCount=%lu,radio_FCSErrorCount=%lu,radio_InvalidMACCount=%lu,radio_PacketsOtherReceived=%lu,radio_NoiseFloor=%d,radio_ChannelUtilization=%lu,radio_ActivityFactor=%d,radio_CarrierSenseThreshold_Exceeded=%d,radio_RetransmissionMetirc=%d,radio_MaximumNoiseFloorOnChannel=%d,radio_MinimumNoiseFloorOnChannel=%d,radio_MedianNoiseFloorOnChannel=%d,radio_StatisticsStartTime=%lu",trafficStats.radio_BytesSent,trafficStats.radio_BytesReceived,trafficStats.radio_PacketsSent,trafficStats.radio_PacketsReceived,trafficStats.radio_ErrorsSent,trafficStats.radio_ErrorsReceived,trafficStats.radio_DiscardPacketsSent,trafficStats.radio_DiscardPacketsReceived,trafficStats.radio_PLCPErrorCount,trafficStats.radio_FCSErrorCount,trafficStats.radio_InvalidMACCount,trafficStats.radio_PacketsOtherReceived,trafficStats.radio_NoiseFloor,trafficStats.radio_ChannelUtilization,trafficStats.radio_ActivityFactor,trafficStats.radio_CarrierSenseThreshold_Exceeded,trafficStats.radio_RetransmissionMetirc,trafficStats.radio_MaximumNoiseFloorOnChannel,trafficStats.radio_MinimumNoiseFloorOnChannel,trafficStats.radio_MedianNoiseFloorOnChannel,trafficStats.radio_StatisticsStartTime);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_getRadioTrafficStats operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WiFiCallMethodForGetRadioTrafficStats  --->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetSSIDTrafficStats
 * Description          : This function invokes WiFi hal api wifi_getSSIDTrafficStats

 * @param [in] req-     : radioIndex - radio index of the wifi
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetSSIDTrafficStats(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetSSIDTrafficStats ----->Entry\n");

    wifi_ssidTrafficStats_t ssidTrafficStats;
    int radioIndex = 1;
    int returnValue;
    char details[1000] = {'\0'};

    radioIndex = req["radioIndex"].asInt();

    returnValue = wifi_getSSIDTrafficStats(radioIndex, &ssidTrafficStats);
    if(0 == returnValue)
    {
        sprintf(details, "Value returned is :ssid_BytesSent=%lu,ssid_BytesReceived=%lu,ssid_PacketsSent=%lu,ssid_PacketsReceived=%lu,ssid_RetransCount=%lu,ssid_FailedRetransCount=%lu,ssid_RetryCount=%lu,ssid_MultipleRetryCount=%lu,ssid_ACKFailureCount=%lu,ssid_AggregatedPacketCount=%lu,ssid_ErrorsSent=%lu,ssid_ErrorsReceived=%lu,ssid_UnicastPacketsSent=%lu,ssid_UnicastPacketsReceived=%lu,ssid_DiscardedPacketsSent=%lu,ssid_DiscardedPacketsReceived=%lu,ssid_MulticastPacketsSent=%lu,ssid_MulticastPacketsReceived=%lu,ssid_BroadcastPacketsSent=%lu,ssid_BroadcastPacketsRecevied=%lu,ssid_UnknownPacketsReceived=%lu\n",ssidTrafficStats.ssid_BytesSent,ssidTrafficStats.ssid_BytesReceived,ssidTrafficStats.ssid_PacketsSent,ssidTrafficStats.ssid_PacketsReceived,ssidTrafficStats.ssid_RetransCount,ssidTrafficStats.ssid_FailedRetransCount,ssidTrafficStats.ssid_RetryCount,ssidTrafficStats.ssid_MultipleRetryCount,ssidTrafficStats.ssid_ACKFailureCount,ssidTrafficStats.ssid_AggregatedPacketCount,ssidTrafficStats.ssid_ErrorsSent,ssidTrafficStats.ssid_ErrorsReceived,ssidTrafficStats.ssid_UnicastPacketsSent,ssidTrafficStats.ssid_UnicastPacketsReceived,ssidTrafficStats.ssid_DiscardedPacketsSent,ssidTrafficStats.ssid_DiscardedPacketsReceived,ssidTrafficStats.ssid_MulticastPacketsSent,ssidTrafficStats.ssid_MulticastPacketsReceived,ssidTrafficStats.ssid_BroadcastPacketsSent,ssidTrafficStats.ssid_BroadcastPacketsRecevied,ssidTrafficStats.ssid_UnknownPacketsReceived);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_getSSIDTrafficStats operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetSSIDTrafficStats ---->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetNeighboringWiFiDiagnosticResult
 * Description          : This function invokes WiFi hal api wifi_getNeighboringWiFiDiagnosticResult

 * @param [in] req-     : radioIndex - radio index of the wifi
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetNeighboringWiFiDiagnosticResult(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetNeighboringWiFiDiagnosticResult ----->Entry\n");

    wifi_neighbor_ap_t *neighbor_ap = NULL;
    unsigned int output_array_size = 0;
    unsigned int output_array_index;
    int radioIndex = 1;
    int returnValue;
    int dataLength;
    int basicInfoSize = 50;

    radioIndex = req["radioIndex"].asInt();

    returnValue = wifi_getNeighboringWiFiDiagnosticResult(radioIndex, &neighbor_ap, &output_array_size);
    printf("return status from api call: %d",returnValue);
    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n No of SSIDs with provided channels : %u\n",output_array_size);
        if (output_array_size > 0)
        {
            DEBUG_PRINT(DEBUG_TRACE,"\n Going to allocate %d bytes memory for details",basicInfoSize*output_array_size);
            char *details = (char*)malloc(basicInfoSize*output_array_size);
            if (details == NULL)
            {
                response["result"]="FAILED";
                response["details"]="Failed to capture Neighboring WiFi Diagnostic Results";
                DEBUG_PRINT(DEBUG_TRACE,"\n Memory Allocation failed\n");
                return;
            }
            else{
                char *details_ptr  = details;
                memset(details_ptr,'\0',basicInfoSize*output_array_size);

                for (output_array_index=0; output_array_index<output_array_size; output_array_index++)
                {
                    if (details[0] != '\0' )
                    {
                        sprintf(details_ptr,"|");
                        details_ptr++;
                    }
                    DEBUG_PRINT(DEBUG_TRACE, "ap_SSID=%s,ap_BSSID=%s,ap_Mode=%s,ap_Channel=%d,ap_SignalStrength=%d,ap_SecurityModeEnabled=%s,ap_EncryptionMode=%s,ap_OperatingFrequencyBand=%s,ap_SupportedStandards=%s,ap_OperatingStandards=%s,ap_OperatingChannelBandwidth=%s,ap_BeaconPeriod=%d,ap_Noise=%d,ap_BasicDataTransferRates=%s,ap_SupportedDataTransferRates=%s,ap_DTIMPeriod=%d,ap_ChannelUtilization=%d\n",neighbor_ap->ap_SSID,neighbor_ap->ap_BSSID,neighbor_ap->ap_Mode,neighbor_ap->ap_Channel,neighbor_ap->ap_SignalStrength,neighbor_ap->ap_SecurityModeEnabled,neighbor_ap->ap_EncryptionMode,neighbor_ap->ap_OperatingFrequencyBand,neighbor_ap->ap_SupportedStandards,neighbor_ap->ap_OperatingStandards,neighbor_ap->ap_OperatingChannelBandwidth,neighbor_ap->ap_BeaconPeriod,neighbor_ap->ap_Noise,neighbor_ap->ap_BasicDataTransferRates,neighbor_ap->ap_SupportedDataTransferRates,neighbor_ap->ap_DTIMPeriod,neighbor_ap->ap_ChannelUtilization);
                    dataLength = sprintf(details_ptr, "SSID=%s,Band=%s",neighbor_ap->ap_SSID,neighbor_ap->ap_OperatingFrequencyBand);

                    details_ptr = details_ptr + dataLength;
                    neighbor_ap++;
                }
                response["result"]="SUCCESS";
                response["details"]=details;
                free(details);
                return;
            }
        }
        else{
                response["result"]="SUCCESS";
                response["details"]="No Neighboring SSID found";
                return;
        }
    }
    else
    {
        response["result"]="FAILURE";
        response["details"]="wifi_getNeighboringWiFiDiagnosticResult operation failed";
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetNeighboringWiFiDiagnosticResult ---->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_ConnectEndpoint
 * Description          : This function invokes WiFi hal api wifi_connectEndpoint()
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                         ssid     - ssid name of the router to which to be connected
  		         security_mode - Security modes this AccessPoint instance is capable of
			 WEPKey - Key to be used when the mode is WEP-64 or WEP-128
			 PreSharedKey - Key to be used when the mode is WPA or WPA2
			 KeyPassphrase - Passphrase of the SSID
			 eapIdentity - Extensible Authentication Protocol used when the mode is Enterprise type
			 privatekey - Key to be used when the mode is Enterprise type
			 saveSSID - Used to save the SSID details
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_ConnectEndpoint(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_ConnectEndpoint ----->Entry\n");
    int radioIndex = 1;
    int returnValue;
    char details[200] = {'\0'};
    char AP_ssid[30];
    wifiSecurityMode_t AP_security_mode;
    int security_mode = 0;
    char AP_security_WEPKey[30] = {'\0'};
    char AP_security_PreSharedKey[30] = {'\0'};;
    char AP_security_KeyPassphrase[30] = {'\0'};;
    int saveSSID = 1;
    char eapIdentity[20] = "0";
    char carootcert[20] = "0";
    char clientcert[20] = "0";
    char privatekey[20] = "0";;

    radioIndex = req["radioIndex"].asInt();
    strcpy(AP_ssid,req["ssid"].asCString());
    security_mode = req["security_mode"].asInt();
    strcpy(AP_security_WEPKey,req["WEPKey"].asCString());
    strcpy(AP_security_PreSharedKey,req["PreSharedKey"].asCString());
    strcpy(AP_security_KeyPassphrase,req["KeyPassphrase"].asCString());
    strcpy(privatekey,req["privatekey"].asCString());
    strcpy(eapIdentity,req["eapIdentity"].asCString());
    saveSSID = req["saveSSID"].asInt();

    switch(security_mode)
        {
        case 0: AP_security_mode = WIFI_SECURITY_NONE;
                break;
        case 1: AP_security_mode = WIFI_SECURITY_WEP_64;
                break;
        case 2: AP_security_mode = WIFI_SECURITY_WEP_128;
                break;
        case 3: AP_security_mode = WIFI_SECURITY_WPA_PSK_TKIP;
                break;
        case 4: AP_security_mode = WIFI_SECURITY_WPA_PSK_AES;
                break;
        case 5: AP_security_mode = WIFI_SECURITY_WPA2_PSK_TKIP;
                break;
        case 6: AP_security_mode = WIFI_SECURITY_WPA2_PSK_AES;
                break;
        case 7: AP_security_mode = WIFI_SECURITY_WPA_ENTERPRISE_TKIP;
                break;
        case 8: AP_security_mode = WIFI_SECURITY_WPA_ENTERPRISE_AES;
                break;
        case 9: AP_security_mode = WIFI_SECURITY_WPA2_ENTERPRISE_TKIP;
                break;
        case 10: AP_security_mode = WIFI_SECURITY_WPA2_ENTERPRISE_AES;
                break;
        case 11: AP_security_mode = WIFI_SECURITY_WPA_WPA2_PSK;
                break;
        case 12: AP_security_mode = WIFI_SECURITY_WPA_WPA2_ENTERPRISE;
                break;
        case 15: AP_security_mode = WIFI_SECURITY_NOT_SUPPORTED;
                break;

        }
    printf("radioIndex: %d\n",radioIndex);
    printf("AP_ssid: %s\n",AP_ssid);
    printf("security_mode: %d\n",security_mode);
    printf("AP_security_WEPKey: %s\n",AP_security_WEPKey);
    printf("AP_security_PreSharedKey: %s\n",AP_security_PreSharedKey);
    printf("AP_security_KeyPassphrase: %s\n", AP_security_KeyPassphrase);
    printf("saveSSID: %d\n",saveSSID);

    returnValue = wifi_connectEndpoint(radioIndex, AP_ssid,AP_security_mode,AP_security_WEPKey,AP_security_PreSharedKey,AP_security_KeyPassphrase,saveSSID,eapIdentity,carootcert,clientcert,privatekey);
    printf("return status from api call: %d",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "wifi_connectEndpoint operation success");
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_connectEndpoint operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_ConnectEndpoint --->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetStats
 * Description          : This function invokes WiFi hal api wifi_getStats()
 *
 * @param [in] req-     : radioIndex  - radio index of the wifi
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetStats(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetStats ------>Entry\n");
    int radioIndex = 1;
    char details[1000] = {'\0'};

    radioIndex = req["radioIndex"].asInt();

    wifi_sta_stats_t  currStationStat;
    memset(&currStationStat,0,sizeof(wifi_sta_stats_t));

    wifi_getStats(radioIndex,&currStationStat);

    sprintf(details, "Current Station: sta_SSID=%s,sta_BSSID=%s,sta_BAND=%s,sta_PhyRate=%f,sta_Noise=%f,sta_RSSI=%f,sta_AvgRSSI=%f,sta_LastDataDownlinkRate=%u,sta_LastDataUplinkRate=%u,sta_Retransmissions=%u",currStationStat.sta_SSID,currStationStat.sta_BSSID,currStationStat.sta_BAND,currStationStat.sta_PhyRate,currStationStat.sta_Noise,currStationStat.sta_RSSI,currStationStat.sta_AvgRSSI,currStationStat.sta_LastDataDownlinkRate,currStationStat.sta_LastDataUplinkRate,currStationStat.sta_Retransmissions);
    response["result"]="SUCCESS";
    response["details"]=details;
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetStats --->Exit\n");
    return;

}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetDualBandSupport
 * Description          : This function invokes WiFi hal api wifi_getDualBandSupport()
 *
 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetDualBandSupport(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetDualBandSupport ------>Entry\n");
    int isDualBand;
    char details[30] = {'\0'};

    isDualBand = wifi_getDualBandSupport();

    sprintf(details,"Is Dual Band Supported : %d",isDualBand);
    response["result"]="SUCCESS";
    response["details"]=details;
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetDualBandSupport ------>Exit\n");
    return;
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetSpecificSSIDInfo
 * Description          : This function invokes WiFi hal api wifi_getSpecificSSIDInfo()
 *
 * @param [in] req-     : ssid   - ssid name of the router to which to be connected
                          band   - frequency band
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetSpecificSSIDInfo(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetSpecificSSIDInfo ------>Entry\n");
    int returnValue;
    char details[1000] = {'\0'};
    char ssid[30];
    int freq_Band = 0;    // WIFI_HAL_FREQ_BAN_NONE

    strcpy(ssid,req["ssid"].asCString());
    freq_Band = req["band"].asInt();
    printf("AP_ssid: %s\n",ssid);
    printf("Frequency_Band: %d\n",freq_Band);

    unsigned int output_array_size;
    WIFI_HAL_FREQ_BAND band;
    wifi_neighbor_ap_t  *filtered_ap_array;

    switch(freq_Band)
    {
        case 0: band = WIFI_HAL_FREQ_BAN_NONE;
                break;
        case 1: band = WIFI_HAL_FREQ_BAND_24GHZ;
                break;
        case 2: band = WIFI_HAL_FREQ_BAND_5GHZ;
                break;
    }

    returnValue=wifi_getSpecificSSIDInfo(ssid,band,&filtered_ap_array,&output_array_size);
    printf("return status from api call: %d",returnValue);
    if(0 == returnValue)
    {
        sprintf(details, "ap_SSID=%s,ap_BSSID=%s,ap_Mode=%s,ap_Channel=%u,ap_SignalStrength=%d,ap_SecurityModeEnabled=%s,ap_EncryptionMode=%s,ap_OperatingFrequencyBand=%s,ap_SupportedStandards=%s,ap_OperatingStandards=%s,ap_OperatingChannelBandwidth=%s,ap_BeaconPeriod=%u,ap_Noise=%d,ap_BasicDataTransferRates=%s,ap_SupportedDataTransferRates=%s,ap_DTIMPeriod=%u,ap_ChannelUtilization=%u",filtered_ap_array->ap_SSID,filtered_ap_array->ap_BSSID,filtered_ap_array->ap_Mode,filtered_ap_array->ap_Channel,filtered_ap_array->ap_SignalStrength,filtered_ap_array->ap_SecurityModeEnabled,filtered_ap_array->ap_EncryptionMode,filtered_ap_array->ap_OperatingFrequencyBand,filtered_ap_array->ap_SupportedStandards,filtered_ap_array->ap_OperatingStandards,filtered_ap_array->ap_OperatingChannelBandwidth,filtered_ap_array->ap_BeaconPeriod,filtered_ap_array->ap_Noise,filtered_ap_array->ap_BasicDataTransferRates,filtered_ap_array->ap_SupportedDataTransferRates,filtered_ap_array->ap_DTIMPeriod,filtered_ap_array->ap_ChannelUtilization);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_getSpecificSSIDInfo operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetSpecificSSIDInfo --->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_SetRadioScanningFreqList
 * Description          : This function invokes WiFi hal api wifi_setRadioScanningFreqList()
 *
 * @param [in] req-     : radioIndex - radio index value of wifi
                          freqList   - list of frequency to be set
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_SetRadioScanningFreqList(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_SetRadioScanningFreqList ------>Entry\n");
    int returnValue;
    char details[100] = {'\0'};
    char freq_list[100];
    int radioIndex=1;

    strcpy(freq_list,req["freqList"].asCString());
    radioIndex = req["radioIndex"].asInt();
    printf("Radio Index: %d\n",radioIndex);
    printf("Frequency List: %s\n",freq_list);

    returnValue=wifi_setRadioScanningFreqList(radioIndex,freq_list);
    printf("return status from api call: %d",returnValue);
    if(0 == returnValue)
    {
        sprintf(details, "Radio Scanning Frequency set operation success");
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_setRadioScanningFreqList operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_SetRadioScanningFreqList --->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_ClearSSIDInfo
 * Description          : This function invokes WiFi hal api wifi_clearSSIDInfo()
 *
 * @param [in] req-     : ssid   - ssid name of the router to which to be connected
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_ClearSSIDInfo(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_ClearSSIDInfo ------>Entry\n");
    int returnValue;
    int radioIndex = 1;
    char details[100] = {'\0'};

    radioIndex = req["radioIndex"].asInt();

    returnValue = wifi_clearSSIDInfo(radioIndex);
    printf("return status from api call: %d",returnValue);
    if(0 == returnValue)
    {
        sprintf(details, "Clearing ssid info operation success");
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_clearSSIDInfo operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_ClearSSIDInfo --->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_LastConnected_Endpoint
 * Description          : This function invokes WiFi hal api wifi_lastConnected_Endpoint()
 *
 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_LastConnected_Endpoint(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_LastConnected_Endpoint ------>Entry\n");
    int returnValue;
    char details[500] = {'\0'};

    wifi_pairedSSIDInfo_t pairedSSIDInfo;
    memset(&pairedSSIDInfo,0,sizeof(wifi_pairedSSIDInfo_t));

    returnValue=wifi_lastConnected_Endpoint(&pairedSSIDInfo);

    printf("return status from api call: %d",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "Value returned is :ap_ssid=%s,ap_bssid=%s,ap_security=%s,ap_passphrase=%s",pairedSSIDInfo.ap_ssid,pairedSSIDInfo.ap_bssid,pairedSSIDInfo.ap_security,pairedSSIDInfo.ap_passphrase);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_lastConnected_Endpoint operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_LastConnected_Endpoint --->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_DisconnectEndpoint
 * Description          : This function invokes WiFi hal api wifi_disconnectEndpoint()
 *
 * @param [in] req-    : methodName - identifier for the hal api name
			 ssid - ssid to be disconnected

 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_DisconnectEndpoint(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_DisconnectEndpoint ------>Entry\n");
    int radioIndex = 1;
    int returnValue;
    char details[500] = {'\0'};
    char AP_ssid[10] = "1";

    radioIndex = req["radioIndex"].asInt();
    strcpy(AP_ssid,req["ssid"].asCString());

    returnValue=wifi_disconnectEndpoint(radioIndex,AP_ssid);

    printf("return status from api call: %d",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "wifi_disconnectEndpoint operation success");
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_disconnectEndpoint operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_DisconnectEndpoint --->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_SetCliWpsButtonPush
 * Description          : This function invokes WiFi hal api wifi_setCliWpsButtonPush()
 *
 * @param [in] req-    :  radioIndex - radio index value of wifi
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_SetCliWpsButtonPush(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_SetCliWpsButtonPush------>Entry\n");
    int radioIndex = 1;
    int returnValue;
    char details[500] = {'\0'};
    radioIndex = req["radioIndex"].asInt();

    returnValue=wifi_setCliWpsButtonPush(radioIndex);

    printf("return status from api call: %d",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "wifi_setCliWpsButtonPush operation success");
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_setCliWpsButtonPush operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_SetCliWpsButtonPush--->Error in execution\n");
        return;
    }
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool WIFIHAL::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_LOG,"WIFIHAL shutting down\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is WIFIHAL Object

Description   : This function will be used to destory the WIFIHAL object.
**************************************************************************/
extern "C" void DestroyObject(WIFIHAL *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying WIFIHAL Agent object\n");
        delete stubobj;
}

