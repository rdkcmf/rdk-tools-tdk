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

#ifndef __DSHAL_STUB_H__
#define __DSHAL_STUB_H__


#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "dsVideoPort.h"
#include "dsVideoDevice.h"
#include "dsAudio.h"
#include "dsDisplay.h"
#include "dsHost.h"
#include "dsMgr.h"
#include "dsFPD.h"


#include "libIBus.h"
#include "libIBusDaemon.h"

#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

using namespace std;

int vpHandle = 0;
int apHandle = 0;
int dispHandle = 0;

class RDKTestAgent;
class DSHalAgent : public RDKTestStubInterface , public AbstractServer<DSHalAgent>
{
        public:
                //Constructor
                DSHalAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <DSHalAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetAudioPort", PARAMS_BY_NAME, JSON_STRING,"portType", JSON_INTEGER,"index", JSON_INTEGER, NULL), &DSHalAgent::DSHal_GetAudioPort);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetVideoPort", PARAMS_BY_NAME, JSON_STRING,"portType", JSON_INTEGER,"index", JSON_INTEGER, NULL), &DSHalAgent::DSHal_GetVideoPort);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetDisplay", PARAMS_BY_NAME, JSON_STRING,"portType", JSON_INTEGER,"index", JSON_INTEGER, NULL), &DSHalAgent::DSHal_GetDisplay);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetSurroundMode", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetSurroundMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetStereoMode", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetStereoMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetStereoMode", PARAMS_BY_NAME, JSON_STRING, "stereoMode", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetStereoMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetAudioEncoding", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetAudioEncoding);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsAudioPortEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsAudioPortEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_EnableAudioPort", PARAMS_BY_NAME, JSON_STRING, "enable", JSON_INTEGER,NULL), &DSHalAgent::DSHal_EnableAudioPort);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsDisplayConnected", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsDisplayConnected);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsDisplaySurround", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsDisplaySurround);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetHDCPProtocol", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetHDCPProtocol);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetHDCPReceiverProtocol", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetHDCPReceiverProtocol);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetHDCPCurrentProtocol", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetHDCPCurrentProtocol);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsVideoPortEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsVideoPortEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_EnableVideoPort", PARAMS_BY_NAME, JSON_STRING, "enable", JSON_INTEGER,NULL), &DSHalAgent::DSHal_EnableVideoPort);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetDisplayAspectRatio", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetDisplayAspectRatio);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetColorDepth", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetColorDepth);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetColorSpace", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetColorSpace);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsVideoPortActive", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsVideoPortActive);
                }

                //Inherited functions
                bool initialize(IN const char* szVersion);

                bool cleanup(const char* szVersion);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                void DSHal_GetAudioPort(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetVideoPort(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetDisplay(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetSurroundMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetStereoMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetStereoMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetAudioEncoding(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsAudioPortEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_EnableAudioPort(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsDisplayConnected(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsDisplaySurround(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetHDCPProtocol(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetHDCPReceiverProtocol(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetHDCPCurrentProtocol(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsVideoPortEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_EnableVideoPort(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetDisplayAspectRatio(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetColorDepth(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetColorSpace(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsVideoPortActive(IN const Json::Value& req, OUT Json::Value& response);
};
#endif //__DSHAL_STUB_H__
