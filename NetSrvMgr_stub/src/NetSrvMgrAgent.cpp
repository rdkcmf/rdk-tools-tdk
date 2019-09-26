/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
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

#include "NetSrvMgrAgent.h"
#include <string.h>

#ifdef __cplusplus
extern "C" {
#include "libIBus.h"
#include "libIARMCore.h"
}
#endif
/***************************************************************************
 *Function name : readLogFile
 *Description   : Helper API to check if a log pattern is found in the file specified
 *Input         : Filename - Name of file where the log has to be searched
 *                parameter - pattern to be searched in the log file
 *Output        : true if pattern is found
 *                false if pattern not found or filename does not exist
 *****************************************************************************/
bool readLogFile (const char *filename, const string parameter) {

    DEBUG_PRINT (DEBUG_TRACE, "readLogFile --->Entry\n"); 
    string line;
    bool retVal = TEST_FAILURE;	
    ifstream logFile (filename);
    if (logFile.is_open ()) {
        while (logFile && getline (logFile,line)) {
            if (0 == line.length()) {
                continue;
            }
            if (line.find (parameter) != string::npos) {
                DEBUG_PRINT (DEBUG_LOG,"Parameter found: %s\n",line.c_str ());
                logFile.clear ();
                logFile.seekg (0, ios::beg);
                logFile.close ();
                retVal = TEST_SUCCESS;
                return retVal;
            }
        }
        logFile.clear ();
        logFile.seekg (0, ios::beg);
        logFile.close ();
        DEBUG_PRINT (DEBUG_ERROR,"Error! No Log found for parameter %s\n", parameter.c_str());
    }
    else {
        DEBUG_PRINT (DEBUG_ERROR,"Unable to open file %s\n", filename);
    }

    DEBUG_PRINT (DEBUG_TRACE, "readLogFile --->Entry\n"); 
    return retVal;
}
/******************************************************************************
 *Function name : setParameters
 *Description   : Helper API to check the methodName to be invoked
 *                and set the corresponding parameters
 *Input         : methodName - Netsrv manager IARM method name
 *                request - Json request recieved from test manager
 *Output        : iarmParam -Netsrv manager parameter to be passed to the method
 *                paramSize - size of the netsrvmgr parameter
 *Return        : SUCCESS or FAILURE in case of invalid input parameters
 *******************************************************************************/
bool setParameters (const Json::Value& req, 
		    char* method_name,
		    void** iarmParam,
		    int* paramSize) {

    DEBUG_PRINT (DEBUG_TRACE, "setParameters --->Entry\n");	
    string methodName = method_name;
  
    if (IARM_BUS_WIFI_MGR_API_getAvailableSSIDs == methodName) {
	/*
	 * Allocate the corresponding parameter and pass its pointer back
	 */
  	IARM_Bus_WiFiSrvMgr_SsidList_Param_t* param = (IARM_Bus_WiFiSrvMgr_SsidList_Param_t*)malloc(sizeof(IARM_Bus_WiFiSrvMgr_SsidList_Param_t) + WIFI_MGR_PARAM_LIST_BUFFER_SIZE);
	memset (param, 0, sizeof (IARM_Bus_WiFiSrvMgr_SsidList_Param_t) + WIFI_MGR_PARAM_LIST_BUFFER_SIZE);
	
        *iarmParam = (void*)param;
	*paramSize= sizeof (IARM_Bus_WiFiSrvMgr_SsidList_Param_t) + WIFI_MGR_PARAM_LIST_BUFFER_SIZE;
    }
    else if (methodName.find("Props") != string::npos) {

	IARM_BUS_WiFi_DiagsPropParam_t* param = (IARM_BUS_WiFi_DiagsPropParam_t*)malloc(sizeof(IARM_BUS_WiFi_DiagsPropParam_t) + WIFI_MGR_PARAM_LIST_BUFFER_SIZE);
	memset (param, 0, sizeof(IARM_BUS_WiFi_DiagsPropParam_t) + WIFI_MGR_PARAM_LIST_BUFFER_SIZE);
	if (methodName.find("set") != string::npos) {

	    /*
	     * TODO
	     */
	}
	
        *iarmParam = (void*)param;
	*paramSize = sizeof(IARM_BUS_WiFi_DiagsPropParam_t) + WIFI_MGR_PARAM_LIST_BUFFER_SIZE;
    }
    else if (IARM_BUS_COMMON_API_SysModeChange == methodName) {

	IARM_Bus_CommonAPI_SysModeChange_Param_t* param = (IARM_Bus_CommonAPI_SysModeChange_Param_t*)malloc(sizeof(IARM_Bus_CommonAPI_SysModeChange_Param_t));
	memset (param, 0, sizeof(IARM_Bus_CommonAPI_SysModeChange_Param_t));
 	if (NULL == &req["new_mode"]) {
            DEBUG_PRINT (DEBUG_ERROR, "Inavlid Parameter\n");
            return TEST_FAILURE;
	}
        param->newMode = (IARM_Bus_Daemon_SysMode_t)req["new_mode"].asInt();
        DEBUG_PRINT (DEBUG_TRACE, "Setting to mode: %d\n", param->newMode);
	
        *iarmParam = (void*)param;
	*paramSize = sizeof (IARM_Bus_CommonAPI_SysModeChange_Param_t);
    }
    else if (IARM_BUS_WIFI_MGR_API_isStopLNFWhileDisconnected == methodName) {

	bool* param = (bool*)malloc(sizeof(bool));
	*param = false;
	
     	*iarmParam = (void*)param;
	*paramSize = sizeof (bool);
    }
    else {
	
	IARM_Bus_WiFiSrvMgr_Param_t* param = (IARM_Bus_WiFiSrvMgr_Param_t*)malloc (sizeof (IARM_Bus_WiFiSrvMgr_Param_t) + WIFI_MAX_DATA_LEN);
	memset (param, 0, sizeof (IARM_Bus_WiFiSrvMgr_Param_t) + WIFI_MAX_DATA_LEN);
	if (IARM_BUS_WIFI_MGR_API_setEnabled == methodName) {

	    if (&req["enable"] == NULL) {
		DEBUG_PRINT (DEBUG_ERROR, "Inavlid Parameter\n");
        	return TEST_FAILURE;
	    }
	    param->data.setwifiadapter.enable = req["enable"].asBool();
	}
	else if (IARM_BUS_WIFI_MGR_API_connect == methodName) {

	    strcpy (param->data.connect.ssid, (&req["ssid"])?req["ssid"].asCString():"");
	    strcpy (param->data.connect.passphrase, (&req["passphrase"])?req["passphrase"].asCString():"");
	    if (&req["security_mode"]) {
	    	param->data.connect.security_mode = (SsidSecurity)req["security_mode"].asInt();
	    }
	    DEBUG_PRINT (DEBUG_TRACE, "Connecting to SSID: %s, with password: %s\n", param->data.connect.ssid, param->data.connect.passphrase);
	}
	else if (IARM_BUS_WIFI_MGR_API_saveSSID == methodName) {

	    strcpy (param->data.connect.ssid, (&req["ssid"])?req["ssid"].asCString():"");
	    strcpy (param->data.connect.passphrase, (&req["passphrase"])?req["passphrase"].asCString():"");
          
            DEBUG_PRINT (DEBUG_TRACE, "Saving SSID: %s & password: %s\n", param->data.connect.ssid, param->data.connect.passphrase);
	}
	
     	*iarmParam = (void*)param;
	*paramSize = sizeof (IARM_Bus_WiFiSrvMgr_Param_t) + WIFI_MAX_DATA_LEN;
    }

	 
    DEBUG_PRINT (DEBUG_TRACE, "setParameters --->Exit\n");

    return TEST_SUCCESS;
}	

/***************************************************************************
 *Function name : getParameterDetails
 *Description   : Helper API to check the methodName and return the correct 
 *		  output from network service manager parameters
 *Input         : jsonresponse - Json response to be sent ot Test Manager
 *                methodName - Network service manager IARM method name 
 *                netSrvParam - NetSrvMagr parameter returned by method 
 *Output        : SUCCESS or FAILUER status as per the values in netSrvParam
 *****************************************************************************/
bool getParameterDetails (Json::Value& response, 
		          string methodName, 
		          void* param) {
    DEBUG_PRINT (DEBUG_TRACE, "getParameterDetails --->Entry\n");

    bool retVal = TEST_FAILURE;
    char outputDetails[WIFI_MAX_DATA_LEN] = {'\0'};
    char outputParam[WIFI_SSID_SIZE] = {'\0'};
    
    if ((IARM_BUS_WIFI_MGR_API_getAvailableSSIDs == methodName) && (((IARM_Bus_WiFiSrvMgr_SsidList_Param_t*)param)->status)) {

	sprintf (outputDetails, "%s", ((IARM_Bus_WiFiSrvMgr_SsidList_Param_t*)param)->curSsids.jdata);
	response["result"] = "SUCCESS";	
	response["details"] = outputDetails;
	retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getCurrentState == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

	sprintf (outputDetails, "%d", ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.wifiStatus);
        response["result"] = "SUCCESS";
	response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getPairedSSID == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

	sprintf (outputDetails, "%s", ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.getPairedSSID.ssid);
        response["result"] = "SUCCESS";
	response["details"] = outputDetails;
	retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getLNFState == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

	sprintf (outputDetails, "%d",((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.wifiLNFStatus);
        response["result"] = "SUCCESS";
	response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_setEnabled == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

	sprintf (outputDetails, "%d", ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.setwifiadapter.enable);
    	response["result"] = "SUCCESS";
	response["details"] = outputDetails;
    	retVal = TEST_SUCCESS;
    }	    
    else if ((IARM_BUS_WIFI_MGR_API_connect == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

            response["result"] = "SUCCESS";
            response["details"] = "IARM_BUS_WIFI_MGR_API_connect successful";
	    retVal = TEST_SUCCESS;
    }	   
    else if ((IARM_BUS_WIFI_MGR_API_initiateWPSPairing == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

        response["result"] = "SUCCESS";
        response["details"] = "IARM_BUS_WIFI_MGR_API_initiateWPSPairing successful";
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_saveSSID == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

        response["result"] = "SUCCESS";
        response["details"] = "IARM_BUS_WIFI_MGR_API_saveSSID successful";
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_clearSSID == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

        response["result"] = "SUCCESS";
        response["details"] = "IARM_BUS_WIFI_MGR_API_clearSSID successful";
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_isPaired == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

	sprintf (outputDetails, "%d", ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.isPaired);
        response["result"] = "SUCCESS";
	response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getConnectedSSID == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

     	sprintf (outputDetails, 
		 "Connected SSID info: tSSID: %s BSSID: %s PhyRate: %f Noise: %f SignalStrength(rssi): %f",
		 ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.getConnectedSSID.ssid,
		 ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.getConnectedSSID.bssid,
		 ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.getConnectedSSID.rate,
		 ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.getConnectedSSID.noise,
		 ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.getConnectedSSID.signalStrength);
		
        response["result"] = "SUCCESS";
        response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getConnectionType == methodName) && (((IARM_Bus_WiFiSrvMgr_Param_t*)param)->status)) {

	sprintf (outputDetails, "%d", ((IARM_Bus_WiFiSrvMgr_Param_t*)param)->data.connectionType);
        response["result"] = "SUCCESS";
	response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    else if (IARM_BUS_WIFI_MGR_API_isStopLNFWhileDisconnected == methodName) {

	sprintf (outputDetails, "%d", *((bool*)param));
	response["result"] = "SUCCESS";
	response["details"] = outputDetails;
	retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getRadioProps == methodName) && (((IARM_BUS_WiFi_DiagsPropParam_t*)param)->status)) {

 	strcpy (outputDetails, "Radio Props: "); 
	sprintf (outputParam, "Enable: %d ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.enable);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "Status: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.status);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "Name: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.name);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "MaxBitRate: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.maxBitRate);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "SupportedFrequencyBands: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.supportedFrequencyBands);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "OperatingFrequencyBand: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.operatingFrequencyBand);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "AutoChannelEnable: %d ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.autoChannelEnable);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "AutoChannelRefreshPeriod: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.autoChannelRefreshPeriod);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "AutoChannelSupported: %d ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.autoChannelSupported);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "ChannelsInUse: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.channelsInUse);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "Channel: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.channel);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "ExtensionChannel: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.extensionChannel);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "GuardInterval: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.guardInterval);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "mcs: %d ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.mcs);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "OperatingChannelBandwidth: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.operatingChannelBandwidth);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "OperatingStandards: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.operatingStandards);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "PossibleChannels: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.possibleChannels);
	strcat (outputDetails, outputParam);
	sprintf (outputParam, "RegulatoryDomain: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio.params.regulatoryDomain);
	strcat (outputDetails, outputParam);
	
	response["result"] = "SUCCESS";
	response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
	DEBUG_PRINT (DEBUG_TRACE, "%s\n", outputDetails);

    }	
    else if (IARM_BUS_WIFI_MGR_API_setRadioProps == methodName) {

	response["result"] = "SUCCESS";
	response["details"] = "IARM_BUS_WIFI_MGR_API_setRadioProps successful";
        retVal = TEST_SUCCESS;          
    }
    else if ((IARM_BUS_WIFI_MGR_API_getRadioStatsProps == methodName) && (((IARM_BUS_WiFi_DiagsPropParam_t*)param)->status)) {

	strcpy (outputDetails, "Radio Stats Props: ");
        sprintf (outputParam, "Bytes Sent: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.bytesSent);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Bytes Received: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.bytesReceived);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Packets Sent: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.packetsSent);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Packets Received: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.packetsReceived);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Errors Sent: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.errorsSent);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Errors Received: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.errorsReceived);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Discard Packets Sent: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.discardPacketsSent);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Discard Packets Received: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.discardPacketsReceived);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "PLCP Error Count: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.plcErrorCount);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "FCS Error Count: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.fcsErrorCount);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Invalid MAC Count: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.invalidMACCount);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Packets Other Received: %u ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.radio_stats.params.packetsOtherReceived);
        strcat (outputDetails, outputParam);
	
        response["result"] = "SUCCESS";
        response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getSSIDProps == methodName) && (((IARM_BUS_WiFi_DiagsPropParam_t*)param)->status)) {

        strcpy (outputDetails, "SSID Props: ");
	sprintf (outputParam, "Enable: %d ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.ssid.params.enable);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Status: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.ssid.params.status);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Name: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.ssid.params.name);
        strcat (outputDetails, outputParam);	
	sprintf (outputParam, "BSSID: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.ssid.params.bssid);
        strcat (outputDetails, outputParam);
	sprintf (outputParam, "MAC Address: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.ssid.params.macaddr);
        strcat (outputDetails, outputParam);
	sprintf (outputParam, "SSID: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.ssid.params.ssid);
        strcat (outputDetails, outputParam);
	
        response["result"] = "SUCCESS";
        response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    else if (IARM_BUS_COMMON_API_SysModeChange == methodName) {

	response["result"] = "SUCCESS";
        response["details"] = "IARM_BUS_COMMON_API_SysModeChange Successful";
        retVal = TEST_SUCCESS;
    }
    else if ((IARM_BUS_WIFI_MGR_API_getEndPointProps == methodName) && (((IARM_BUS_WiFi_DiagsPropParam_t*)param)->status)) {

	strcpy (outputDetails, "Profile : EndPoint.1: ");
        sprintf (outputParam, "Enable: %d ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.endPointInfo.enable);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Status: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.endPointInfo.status);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "SSID Reference: %s ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.endPointInfo.SSIDReference);
        strcat (outputDetails, outputParam);
        strcat (outputDetails, "Profile : EndPoint.1.Stats: ");
        sprintf (outputParam, "SignalStrength: %d ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.endPointInfo.stats.signalStrength);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "Retransmissions: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.endPointInfo.stats.retransmissions);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "LastDataUplinkRate: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.endPointInfo.stats.lastDataUplinkRate);
        strcat (outputDetails, outputParam);
        sprintf (outputParam, "LastDataDownlinkRate: %lu ", ((IARM_BUS_WiFi_DiagsPropParam_t*)param)->data.endPointInfo.stats.lastDataDownlinkRate);
        strcat (outputDetails, outputParam);

        response["result"] = "SUCCESS";
        response["details"] = outputDetails;
        retVal = TEST_SUCCESS;
    }
    if (TEST_FAILURE == retVal) {
	response["result"] = "FAILURE";
        response["details"] = methodName + " failed";
    }
    DEBUG_PRINT (DEBUG_TRACE, "getParameterDetails --->Exit\n");

    return retVal;
}

/**************************************************************************
Function name : NetSrvMgrAgent::initialize

Arguments     : Input arguments are Version string and NetSrvMgrAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool NetSrvMgrAgent::initialize (IN const char* szVersion) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent Initialization Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent Initialization Exit\n");

    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                1.
 *****************************************************************************/

std::string NetSrvMgrAgent::testmodulepre_requisites() {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule pre_requisites --> Entry\n");
#if 1
    string g_tdkPath = getenv("TDK_PATH");
    string NM_testmodule_PR_cmd, NM_testmodule_PR_log,line;
    ifstream logfile;
    NM_testmodule_PR_cmd= g_tdkPath + "/" + PRE_REQUISITE_FILE;
    NM_testmodule_PR_log= g_tdkPath + "/" + PRE_REQUISITE_LOG_PATH;
    string pre_req_chk= "source " + NM_testmodule_PR_cmd;
    try {
            system((char *)pre_req_chk.c_str());
    }
    catch(...) {
            DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of pre-requisite script\n");
            DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
            return "FAILURE<DETAILS>Exception occured execution of pre-requisite script";
    }
    logfile.open(NM_testmodule_PR_log.c_str());
    if(logfile.is_open()) {
        	if(getline(logfile,line)) {
                    logfile.close();
                    DEBUG_PRINT(DEBUG_LOG,"\nPre-Requisites set\n");
                    DEBUG_PRINT(DEBUG_TRACE, "testmodulepre_requisites --> Exit\n");
                    return line;
            }
            logfile.close();
            DEBUG_PRINT(DEBUG_ERROR,"\nPre-Requisites not set\n");
            return "FAILURE<DETAILS>Proper result is not found in the log file";
    }
    else {
    	DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the log file.\n");
            return "FAILURE<DETAILS>Unable to open the log file";
    }
#endif
    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule pre_requisites --> Exit\n");
    
    return "SUCCESS<DETAILS>SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description   : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool NetSrvMgrAgent::testmodulepost_requisites() {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule post_requisites --> Entry\n");

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule post_requisites --> Exit\n");

    return TEST_SUCCESS;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the list of 
		available SSIDs.

Description   : Retrieve the available SSIDs from Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

void NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs --->Entry\n");

    try {
	    
	char ssidList[WIFI_MGR_PARAM_LIST_BUFFER_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_SsidList_Param_t param;

 	memset (&param, 0, sizeof(param));
	iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
	    		        IARM_BUS_WIFI_MGR_API_getAvailableSSIDs,
	    		        (void *)&param,
	    		        sizeof(IARM_Bus_WiFiSrvMgr_SsidList_Param_t));
	    

	if (iarmResult != IARM_RESULT_SUCCESS || !(param.status)) {

	    DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetAvailableSSIDs for wifi manager failed\n");
	    response["result"] = "FAILURE";
	    response["details"] = "IARM_Bus_Call to GetAvailableSSIDs for wifi manager failed";
 	}
	else {

	    DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetAvailableSSIDs for wifi manager successful\n");

	    response["result"] = "SUCCESS";
	    if (0 >= param.curSsids.jdataLen) {
	        response["details"] = "No SSIDs are available";
	    }
	    else {     
	        memcpy (ssidList, param.curSsids.jdata, param.curSsids.jdataLen);
	        DEBUG_PRINT (DEBUG_TRACE, "Available SSIDs for Wifi Service Manager : %s\n", param.curSsids.jdata); 
	        response["details"] = ssidList;
	    }
	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs -->Exit\n");
    return;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetCurrentState

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the current 
		state of Wifi Service Manager.

Description   : Retrieve the current state of Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

void NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetCurrentState(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetCurrentState --->Entry\n");

    try {
	    
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t  *param = NULL;

	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	    		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for getting wifi manager current state\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for getting wifi manager current state";
	}
	else {

	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
	  			        IARM_BUS_WIFI_MGR_API_getCurrentState,
				        (void *)param,
				        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
		

	    if (iarmResult != IARM_RESULT_SUCCESS || !(param->status)) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetCurrentState of wifi manager failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to GetCurrentState of wifi manager failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetCurrentState of wifi manager successful\n");
		if (param->data.wifiStatus < 0 || param->data.wifiStatus > WIFI_MAX_STATUS_CODE) {
		    
		    DEBUG_PRINT (DEBUG_TRACE, "Invalid Wifi manager status\n");
		    response["result"] = "FAILURE";
                    response["details"] = "Invalid Wifi manager status";
		}
		else {

		    DEBUG_PRINT (DEBUG_TRACE, "Current State of Wifi Service Manager : %s\n", aWifiStatus[param->data.wifiStatus].c_str()); 
			
		    response["result"] = "SUCCESS";
		    response["details"] = aWifiStatus[param->data.wifiStatus];
		}
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetCurrentState\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetCurrentState";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetCurrentState -->Exit\n");
    return;
}
/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetLAFState

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the LAF 
		state of Wifi Service Manager.

Description   : Retrieve the LAF state of Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

void NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetLAFState(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetLAFState --->Entry\n");

    try {
	    
	char lafState[WIFI_MGR_PARAM_BUFFER_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t  *param = NULL;

	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	    		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for getting wifi manager LAF state\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for getting wifi manager LAF state";
	}
	else {

	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
					IARM_BUS_WIFI_MGR_API_getLNFState,
				        (void *)param,
				        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
		

	    if (iarmResult != IARM_RESULT_SUCCESS || !(param->status)) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetLAFState of wifi manager failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to GetLAFState of wifi manager failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetLAFState of wifi manager successful\n");
		/*
		 *Check if Status code retured is a valid one
		 */
	        if (param->data.wifiLNFStatus < 0 || param->data.wifiLNFStatus > WIFI_MAX_LNF_STATUS_CODE) {

                    DEBUG_PRINT (DEBUG_TRACE, "Invalid Wifi LAF status\n");
                    response["result"] = "FAILURE";
                    response["details"] = "Invalid Wifi LAF status";
                }
                else {

	            DEBUG_PRINT (DEBUG_TRACE, "LAF State of Wifi Service Manager : %s\n", aWifiLAFStatus[param->data.wifiLNFStatus].c_str()); 
		
	            response["result"] = "SUCCESS";
	            response["details"] = aWifiLAFStatus[param->data.wifiLNFStatus];
		}
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetLAFState\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetLAFState";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetLAFState -->Exit\n");
    return;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetPairedSSID

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the paired
		SSID for Wifi Service Manager.

Description   : Retrieve the paired SSID for Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

void NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetPairedSSID(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetPairedSSID --->Entry\n");

    try {
	    
	//char currentState[WIFI_MGR_PARAM_BUFFER_SIZE] = {'\0'};
	char aSsid[WIFI_SSID_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t  *param = NULL;

	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	    		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for getting paired SSID for wifi manager\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for getting paired SSID for wifi manager";
	}
	else {

	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
					IARM_BUS_WIFI_MGR_API_getPairedSSID,
				        (void *)param,
				        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
		

	    if (iarmResult != IARM_RESULT_SUCCESS || !(param->status)) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetPairedSSID of wifi manager failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to GetPairedSSID of wifi manager failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetPairedSSID of wifi manager successful\n");

		strcpy (aSsid, param->data.getPairedSSID.ssid);
		response["result"] = "SUCCESS";
		/*
		 *Check if a valid SSID
		 */
		if ('\0' != aSsid[0]) {

	            DEBUG_PRINT (DEBUG_TRACE, "Paired SSID for Wifi Service Manager : %s\n", aSsid); 
	            response["details"] = aSsid;
		}
		else {
	 	    DEBUG_PRINT (DEBUG_TRACE, "No ssid assigned\n");
                    response["details"] = "No ssid assigned";
		}
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetPairedSSID\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetPairedSSID";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetPairedSSID -->Exit\n");
    return;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_SetEnabled

Arguments     : Input argument - Enable : True/False to enable/disable
		Wifi adapter.
                Output argument is "SUCCESS" or "FAILURE"

Description   : Enable/Disable the Wifi adapter
**************************************************************************/

void NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_SetEnabled (IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_SetEnabled --->Entry\n");

    try {
	    
	char details[WIFI_MGR_PARAM_BUFFER_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t *param = NULL;
	
	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	  		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for enabling/disabling wifi adapter\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for enabling/disabling wifi adapter";
	}
	else {
	    
	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    param->data.setwifiadapter.enable = req["enable"].asBool();
            iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME,
                                        IARM_BUS_WIFI_MGR_API_setEnabled,
                                        (void *)param,
                                        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));

	    /*
	     *No need to check param->status since its not set
	     *in this case
	     */
	    if (iarmResult != IARM_RESULT_SUCCESS) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to SetEnabled for Wifi adapter failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to SetEnabled for Wifi adapter failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to SetEnabled successful\n");

		DEBUG_PRINT (DEBUG_TRACE, "Wifi adapter SetEnable status: %d\n", param->data.setwifiadapter.enable);
		sprintf(details,"Wifi adapter SetEnable status:%d", param->data.setwifiadapter.enable);
		response["result"] = "SUCCESS";
	        response["details"] = details;
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_SetEnabled\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_SetEnabled";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_SetEnabled -->Exit\n");
    return ;
}

/**************************************************************************
* Function name : NetSrvMgrAgent_WifiMgr_SetGetParameters
*
* Arguments     : methodName - Wifi Manager IARMBus_Call methods.
*		  Input parameters - to be passed to the Wifi manager		
*                 Output argument is "SUCCESS" or "FAILURE" and the output 
*                 parameters retreived from Wifi Manager.
*
* Description   : Set/Get the Wifi Service Manager parameters and
*                 pass result back to Test Manager.
****************************************************************************/

void NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_SetGetParameters(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_SetGetParameters --->Entry\n");

    try {

	bool retVal = TEST_FAILURE;
        IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
        char* methodName;
	char resultDetails[WIFI_MGR_PARAM_LIST_BUFFER_SIZE] = {'\0'};
        void* param = NULL;  //To be set based on the wifi manager method
	int paramSize = 0;

	
	if (NULL == &req["method_name"]) {

	    DEBUG_PRINT (DEBUG_ERROR, "Method name cannot be NULL\n");
	    response["result"] = "FAILURE";
            response["details"] = "Invalid Wifi Manager method";
	}
	/*
	 * Set the Input paramerts for Wifi Manager methods
	 */
	else {
	    methodName = (char*)req["method_name"].asCString();
	    DEBUG_PRINT (DEBUG_TRACE, "Setting parameters for %s\n", methodName);
	    retVal = setParameters (req, methodName, &param, &paramSize);
	    if ((TEST_SUCCESS != retVal) || (0 == paramSize)) {
	        DEBUG_PRINT (DEBUG_ERROR, "Invalid Parameters for IARM_Bus_Call %d\n", retVal);
	        response["result"] = "FAILURE";
                response["details"] = "Invalid Parameters for IARM_Bus_Call";
	    }
	    else {
	        /*  
	         * IARM_Bus_Call to access Wifi Manager methods
	         */
                iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME,
                                            methodName,
                                            (void *)param,
                                            paramSize);
                if (iarmResult != IARM_RESULT_SUCCESS) {

                    DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to %s for wifi manager failed\n", methodName);
                    sprintf (resultDetails, "IARM_Bus_Call to %s for wifi manager failed", methodName);
                    response["result"] = "FAILURE";
	            response["details"] = resultDetails;
                }
	        else {
	            retVal = getParameterDetails (response, methodName, param);
	            if (TEST_SUCCESS != retVal) {
	        	DEBUG_PRINT (DEBUG_ERROR, "%s for Wifi Manager failed \n", methodName);
	            }
	            else {
	                DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to %s for wifi manager successfull\n", methodName);
	                DEBUG_PRINT (DEBUG_TRACE, "Result :\n%s\n", (char*)response["details"].asCString()); 
	            }
	        }
		/*
		 * Free the memmory allocated for parameters
		 */
		free(param);
	    }
        }
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_SetGetParameters\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_SetGetParameters";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_SetGetParameters -->Exit\n");
    return;
}
/***************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_SaveSSID

Arguments     : Input argument - SSID : SSID to be saved for future sessions
		                 Passphrase : Passphrase for saved SSID
                Output argument is "SUCCESS" or "FAILURE"

Description   : Save an SSID for future sessions
****************************************************************************/

void NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_BroadcastEvent (IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_BroadcastEvent --->Entry\n");

    try {
	    
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	bool retVal;
	char *owner;
	//IARM_EventId_t  eventId;
	int eventId = 0;
	string eventLog;
	void* eventData;
	int eventDataSize = 0;
	//IARM_Bus_WiFiSrvMgr_Param_t param;
	if ((NULL == &req["owner"]) || (NULL == &req["event_id"]) || (NULL == &req["event_log"])){

            DEBUG_PRINT (DEBUG_ERROR, "Owner and event name cannot be NULL\n");
            response["result"] = "FAILURE";
            response["details"] = "Invalid parameters";
        }
	else {
	    owner = (char*)req["owner"].asCString();
	    eventId = req["event_id"].asInt();
	    eventLog = req["event_log"].asString();
	
	    /*
	     *Assign the event data as per the owner and event ID
	     */
	    /*if (0 == strcmp(owner, IARM_BUS_AUTHSERVICE_NAME)) {
		switch (eventId) {
		    case IARM_BUS_AUTHSERVICE_EVENT_SWITCH_TO_PRIVATE: {
			IARM_BUS_AuthService_EventData_t* param = (IARM_BUS_AuthService_EventData_t*)malloc(sizeof(IARM_BUS_AuthService_EventData_t));
        	   	memset (param, 0, sizeof (IARM_BUS_AuthService_EventData_t));

			param->value = req["value"].asInt();
        		eventData = (void*)param;
        		eventDataSize= sizeof (IARM_BUS_AuthService_EventData_t);
		    }
		    break;
        	    default:
            	    break;
        	}
	    }
	    else*/
            if (0 == strcmp(owner, IARM_BUS_IRMGR_NAME)) {
		switch (eventId) {
                    case IARM_BUS_IRMGR_EVENT_IRKEY: {
			IARM_Bus_IRMgr_EventData_t* param = (IARM_Bus_IRMgr_EventData_t*)malloc(sizeof(IARM_Bus_IRMgr_EventData_t));
                        memset (param, 0, sizeof (IARM_Bus_IRMgr_EventData_t));

			param->data.irkey.keyCode = req["key_code"].asInt();
			param->data.irkey.keyType = req["key_type"].asInt();
			param->data.irkey.isFP = req["isFP"].asInt();
			eventData = (void*)param;
                        eventDataSize= sizeof (IARM_Bus_IRMgr_EventData_t);
		    }
		    break;
                    default:
                    break;
                }
	    }
	    else if (0 == strcmp(owner, IARM_BUS_NM_SRV_MGR_NAME)) {
		switch (eventId) {
                    case IARM_BUS_NETWORK_MANAGER_EVENT_SWITCH_TO_PRIVATE: {
			IARM_BUS_NetworkManager_EventData_t* param = (IARM_BUS_NetworkManager_EventData_t*)malloc(sizeof(IARM_BUS_NetworkManager_EventData_t));
                        memset (param, 0, sizeof (IARM_BUS_NetworkManager_EventData_t));
			 	
			param->value = req["value"].asInt();
                        eventData = (void*)param;
                        eventDataSize= sizeof (IARM_BUS_NetworkManager_EventData_t);
		    }
		    break;
		    case IARM_BUS_NETWORK_MANAGER_EVENT_STOP_LNF_WHILE_DISCONNECTED: {
			bool* param = (bool*)malloc(sizeof(bool));
        		
			*param = req["value"].asInt();
			eventData = (void*)param;
                        eventDataSize= sizeof (bool);
		    }
                    break;
                    case IARM_BUS_NETWORK_MANAGER_EVENT_AUTO_SWITCH_TO_PRIVATE_ENABLED: {
                        bool* param = (bool*)malloc(sizeof(bool));

                        *param = req["value"].asInt();
                        eventData = (void*)param;
                        eventDataSize= sizeof (bool);
                    }
                    break;
		    default:
                    break;
                } 
	    }
	
	    iarmResult = IARM_Bus_BroadcastEvent(owner, (IARM_EventId_t)eventId, eventData, eventDataSize);
	    if (IARM_RESULT_SUCCESS != iarmResult) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_BroadcastEvent failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_BroadcastEvent failed";
 	    }
	    else {
              	/*
                 *Delay for broadcast event msg to be updated
                 */
              	sleep (7);
		retVal = readLogFile(NM_LOG_FILE, eventLog);
	        if (TEST_SUCCESS == retVal) {
	            response["result"] = "SUCCESS";
	            response["details"] = "Event received by NetSrv manager";
	        }
	        else {
	            response["result"] = "FAILURE";
	            response["details"] = "Event not received by NetSrv manager";
	        }
	    }
	}
	/*
	 * Free Allocated memory
	 */
    	free (eventData);
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_BroadcastEvent\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_BroadcastEvent";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_BroadcastEvent -->Exit\n");
    return;
}

/************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "NetSrvMgrAgent".
**************************************************************************/

extern "C" NetSrvMgrAgent* CreateObject (TcpSocketServer &ptrtcpServer) {

    return new NetSrvMgrAgent (ptrtcpServer);
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool NetSrvMgrAgent::cleanup (IN const char* szVersion) {

    DEBUG_PRINT (DEBUG_TRACE, "Cleaningup\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is NetSrvMgrAgent Object

Description   : This function will be used to destory the NetSrvMgrAgent object.
**************************************************************************/
extern "C" void DestroyObject (NetSrvMgrAgent *stubobj) {

    DEBUG_PRINT (DEBUG_LOG, "Destroying NetSrvMgrAgent object\n");
    delete stubobj;
}

