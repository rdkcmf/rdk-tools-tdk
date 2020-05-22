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

#ifndef __DEEPSLEEPHAL_STUB_H__
#define __DEEPSLEEPHAL_STUB_H__

#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <chrono>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "deepSleepMgr.h"

#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

using namespace std;

class RDKTestAgent;
class DeepSleepHalAgent : public RDKTestStubInterface , public AbstractServer<DeepSleepHalAgent>
{
        public:
                //Constructor
                DeepSleepHalAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <DeepSleepHalAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod(Procedure("TestMgr_DeepSleepHal_SetDeepSleep", PARAMS_BY_NAME, JSON_STRING, "timeout", JSON_INTEGER, NULL), &DeepSleepHalAgent::DeepSleepHal_SetDeepSleep);
                }


                //Inherited functions
                bool initialize(IN const char* szVersion);
                bool cleanup(const char* szVersion);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                void DeepSleepHal_SetDeepSleep(IN const Json::Value& req, OUT Json::Value& response);

};
#endif //__DEEPSLEEPHAL_STUB_H__


