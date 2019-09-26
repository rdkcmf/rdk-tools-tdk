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

#ifndef __MOCAHAL_STUB_H__
#define __MOCAHAL_STUB_H__


#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "rmh_type.h"
#include "rmh_soc.h"
#include "rdk_moca_hal.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define SUPPORTED_FREQUENCIES_BUFFER 128
#define FREQUENCIES_BUFFER 32
using namespace std;

RMH_Handle rmh;

class RDKTestAgent;
class MocaHalAgent : public RDKTestStubInterface , public AbstractServer<MocaHalAgent>
{
        public:
                //Constructor
                MocaHalAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <MocaHalAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMoCALinkUp", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMoCALinkUp);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_SetEnabled", PARAMS_BY_NAME, JSON_STRING,"enable",JSON_INTEGER,NULL), &MocaHalAgent::MocaHal_SetEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetLOF", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetLOF);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetFrequencyMask", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetFrequencyMask);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetSupportedFrequencies", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetSupportedFrequencies);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetHighestSupportedMoCAVersion", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetHighestSupportedMoCAVersion);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMac", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMac);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetName", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetName);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMoCAVersion", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetName);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetNumNodes", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetNumNodes);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetSupportedModes", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetSupportedModes);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMode", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMode); 
                }

                //Inherited functions
                bool initialize(IN const char* szVersion);

                bool cleanup(const char* szVersion);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                void MocaHal_Initialize(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMoCALinkUp(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_SetEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetLOF(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetFrequencyMask(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetSupportedFrequencies(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetHighestSupportedMoCAVersion(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMac(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetName(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMoCAVersion(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetNumNodes(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetSupportedModes(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMode(IN const Json::Value& req, OUT Json::Value& response);
};
#endif //__MOCAHAL_STUB_H__
