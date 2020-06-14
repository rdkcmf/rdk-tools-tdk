/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
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

#ifndef __POWERMGRHAL_STUB_H__
#define __POWERMGRHAL_STUB_H__

#include <json/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <chrono>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "plat_power.h"
#include "pwrMgr.h"
#include "libIBusDaemon.h"

#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

using namespace std;

class RDKTestAgent;
class PowerMgrHalAgent : public RDKTestStubInterface , public AbstractServer<PowerMgrHalAgent>
{
        public:
                //Constructor
                PowerMgrHalAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <PowerMgrHalAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_Reset", PARAMS_BY_NAME, JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_Reset);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_GetPowerState", PARAMS_BY_NAME, JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_GetPowerState);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_SetPowerState", PARAMS_BY_NAME, JSON_STRING, "state", JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_SetPowerState);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_GetTemperature", PARAMS_BY_NAME, JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_GetTemperature);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_GetTempThresholds", PARAMS_BY_NAME, JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_GetTempThresholds);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_SetTempThresholds", PARAMS_BY_NAME, JSON_STRING, "high", JSON_INTEGER, "critical", JSON_INTEGER, NULL), &PowerMgrHalAgent::PowerMgrHal_SetTempThresholds);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_DetemineClockSpeeds", PARAMS_BY_NAME, JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_DetemineClockSpeeds);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_GetClockSpeed", PARAMS_BY_NAME, JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_GetClockSpeed);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_SetClockSpeed", PARAMS_BY_NAME, JSON_STRING, "speed", JSON_INTEGER, NULL), &PowerMgrHalAgent::PowerMgrHal_SetClockSpeed);
                    this->bindAndAddMethod(Procedure("TestMgr_PowerMgrHal_GetCmdTimeTaken", PARAMS_BY_NAME, JSON_STRING, "cmd", JSON_STRING, NULL), &PowerMgrHalAgent::PowerMgrHal_GetCmdTimeTaken);
                }


                //Inherited functions
                bool initialize(IN const char* szVersion);
                bool cleanup(const char* szVersion);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                void PowerMgrHal_Reset(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_GetPowerState(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_SetPowerState(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_GetTemperature(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_GetTempThresholds(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_SetTempThresholds(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_DetemineClockSpeeds(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_GetClockSpeed(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_SetClockSpeed(IN const Json::Value& req, OUT Json::Value& response);
                void PowerMgrHal_GetCmdTimeTaken(IN const Json::Value& req, OUT Json::Value& response);

};
#endif //__POWERMGRHAL_STUB_H__
