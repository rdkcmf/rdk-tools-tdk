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
#ifndef __WIFIHAL_STUB_H__
#define __WIFIHAL_STUB_H__
#include <json/json.h>
#include <unistd.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <sys/types.h>
#include <sys/wait.h>
#include <fstream>
#include <sstream>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>
extern "C"
{
    #include "wifi_common_hal.h"
    #include "wifi_client_hal.h"
    #include "wifi_ap_hal.h"
}
#define IN
#define OUT
#define TEST_SUCCESS true
#define TEST_FAILURE false

class RDKTestAgent;
class WIFIHAL : public RDKTestStubInterface, public AbstractServer<WIFIHAL>
{
    public:
         WIFIHAL(TcpSocketServer &ptrRpcServer) : AbstractServer <WIFIHAL>(ptrRpcServer)
                {
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_Init", PARAMS_BY_NAME, JSON_STRING, NULL), &WIFIHAL::WIFI_HAL_Init);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_Down", PARAMS_BY_NAME, JSON_STRING, NULL), &WIFIHAL::WIFI_HAL_Down);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_Uninit", PARAMS_BY_NAME, JSON_STRING, NULL), &WIFIHAL::WIFI_HAL_Uninit);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_GetOrSetParamStringValue", PARAMS_BY_NAME, JSON_STRING,"methodName", JSON_STRING,"radioIndex", JSON_INTEGER, "param", JSON_STRING, "paramType",  JSON_STRING,NULL), &WIFIHAL::WIFI_HAL_GetOrSetParamStringValue);
		  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_GetOrSetParamULongValue", PARAMS_BY_NAME, JSON_STRING,"methodName", JSON_STRING,"radioIndex", JSON_INTEGER,"param", JSON_INTEGER, "paramType",  JSON_STRING,NULL), &WIFIHAL::WIFI_HAL_GetOrSetParamULongValue);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_GetOrSetParamBoolValue", PARAMS_BY_NAME, JSON_STRING,"methodName", JSON_STRING,"radioIndex", JSON_INTEGER,"param", JSON_INTEGER, "paramType",  JSON_STRING,NULL), &WIFIHAL::WIFI_HAL_GetOrSetParamBoolValue);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_GetOrSetRadioStandard", PARAMS_BY_NAME, JSON_STRING,"methodName", JSON_STRING,"radioIndex", JSON_INTEGER, "param", JSON_STRING, "paramType",  JSON_STRING, NULL), &WIFIHAL::WIFI_HAL_GetOrSetRadioStandard);
		  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_GetRadioTrafficStats",PARAMS_BY_NAME, JSON_STRING, "radioIndex",JSON_INTEGER,NULL), &WIFIHAL::WIFI_HAL_GetRadioTrafficStats);
		  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_GetSSIDTrafficStats",PARAMS_BY_NAME, JSON_STRING, "radioIndex",JSON_INTEGER,NULL), &WIFIHAL::WIFI_HAL_GetSSIDTrafficStats);
		  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_GetNeighboringWiFiDiagnosticResult",PARAMS_BY_NAME, JSON_STRING, "radioIndex",JSON_INTEGER,NULL), &WIFIHAL::WIFI_HAL_GetNeighboringWiFiDiagnosticResult);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_ConnectEndpoint", PARAMS_BY_NAME, JSON_STRING,"radioIndex", JSON_INTEGER, "ssid",JSON_STRING, "security_mode",JSON_INTEGER, "WEPKey", JSON_STRING, "PreSharedKey", JSON_STRING, "KeyPassphrase", JSON_STRING, "privatekey", JSON_STRING, "eapIdentity", JSON_STRING, "saveSSID", JSON_INTEGER, NULL), &WIFIHAL::WIFI_HAL_ConnectEndpoint);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_LastConnected_Endpoint", PARAMS_BY_NAME, JSON_STRING,NULL), &WIFIHAL::WIFI_HAL_LastConnected_Endpoint);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_DisconnectEndpoint", PARAMS_BY_NAME, JSON_STRING,"radioIndex", JSON_INTEGER,"ssid", JSON_STRING, NULL), &WIFIHAL::WIFI_HAL_DisconnectEndpoint);
                  this->bindAndAddMethod(Procedure("TestMgr_WIFIHAL_SetCliWpsButtonPush", PARAMS_BY_NAME, JSON_STRING,"radioIndex", JSON_INTEGER, NULL), &WIFIHAL::WIFI_HAL_SetCliWpsButtonPush);
                }
        /*inherited functions*/
        bool initialize(IN const char* szVersion);
        bool cleanup(IN const char* szVersion);
        std::string testmodulepre_requisites();
        bool testmodulepost_requisites();

        /*WIFIHAL Stub Wrapper functions*/
	void WIFI_HAL_Init(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_Down(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_Uninit(IN const Json::Value& req, OUT Json::Value& response);
        void WIFI_HAL_GetOrSetParamStringValue(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_GetOrSetParamULongValue(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_GetOrSetParamBoolValue(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_GetOrSetRadioStandard(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_GetRadioTrafficStats(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_GetSSIDTrafficStats(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_GetNeighboringWiFiDiagnosticResult(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_ConnectEndpoint(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_LastConnected_Endpoint(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_DisconnectEndpoint(IN const Json::Value& req, OUT Json::Value& response);
	void WIFI_HAL_SetCliWpsButtonPush(IN const Json::Value& req, OUT Json::Value& response);
};
#endif //__WIFIHAL_STUB_H__

