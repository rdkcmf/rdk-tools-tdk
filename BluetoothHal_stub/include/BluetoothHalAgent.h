/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2021 RDK Management
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

#ifndef __BLUETOOTHHAL_STUB_H__
#define __BLUETOOTHHAL_STUB_H__


#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#include "btrCore.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

using namespace std;

class RDKTestAgent;
class BluetoothHalAgent : public RDKTestStubInterface , public AbstractServer<BluetoothHalAgent>
{
        public:
                //Constructor
                BluetoothHalAgent (TcpSocketServer &ptrRpcServer) : AbstractServer <BluetoothHalAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetListOfAdapters", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothHalAgent::BluetoothHal_GetListOfAdapters);
                }

                //Inherited functions
                bool initialize (IN const char* szVersion);

                bool cleanup (const char*);
                std::string testmodulepre_requisites ();
                bool testmodulepost_requisites ();

                //Stub functions
                void BluetoothHal_GetListOfAdapters (IN const Json::Value& req, OUT Json::Value& response);
               
};
#endif //__BLUETOOTHHAL_STUB_H__
