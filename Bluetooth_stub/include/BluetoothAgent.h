/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2017 RDK Management
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

#ifndef __BLUETOOTH_STUB_H__
#define __BLUETOOTH_STUB_H__


#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#include "btmgr.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define DEVICE_NAME_BUFFER 50
#define DISCOVERED_DEVICE_BUFFER 50
#define PAIRED_DEVICE_BUFFER 50
#define CONNECTED_DEVICE_BUFFER 50
#define DEVICE_HANDLE_BUFFER 20
#define DEVICE_PROPERTIES_BUFFER 100

using namespace std;

BTRMGR_Result_t rc = BTRMGR_RESULT_SUCCESS;

class RDKTestAgent;
class BluetoothAgent : public RDKTestStubInterface , public AbstractServer<BluetoothAgent>
{
        public:
                //Constructor
                BluetoothAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <BluetoothAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_GetNumberOfAdapters", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_GetNumberOfAdapters);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_GetAdapterName", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_GetAdapterName);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_SetAdapterName", PARAMS_BY_NAME, JSON_STRING,"name",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_SetAdapterName);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_GetAdapterPowerStatus", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_GetAdapterPowerStatus);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_SetAdapterPowerStatus", PARAMS_BY_NAME, JSON_STRING,"powerstatus",JSON_INTEGER,NULL), &BluetoothAgent::Bluetooth_SetAdapterPowerStatus);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_IsAdapterDiscoverable", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_IsAdapterDiscoverable);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_SetAdapterDiscoverable", PARAMS_BY_NAME, JSON_STRING,"discoverablestatus",JSON_INTEGER,"timeout",JSON_INTEGER,NULL), &BluetoothAgent::Bluetooth_SetAdapterDiscoverable);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_StartDeviceDiscovery", PARAMS_BY_NAME, JSON_STRING,"devicetype",JSON_INTEGER,NULL), &BluetoothAgent::Bluetooth_StartDeviceDiscovery);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_StopDeviceDiscovery", PARAMS_BY_NAME, JSON_STRING,"devicetype",JSON_INTEGER,NULL), &BluetoothAgent::Bluetooth_StopDeviceDiscovery);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_GetDiscoveredDevices", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_GetDiscoveredDevices);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_ConnectToDevice", PARAMS_BY_NAME, JSON_STRING,"devicetype",JSON_INTEGER,"devicehandle",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_ConnectToDevice);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_DisconnectFromDevice", PARAMS_BY_NAME, JSON_STRING,"devicehandle",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_DisconnectFromDevice);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_GetConnectedDevices", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_GetConnectedDevices); 
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_PairDevice", PARAMS_BY_NAME, JSON_STRING,"devicehandle",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_PairDevice);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_UnpairDevice", PARAMS_BY_NAME, JSON_STRING,"devicehandle",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_UnpairDevice);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_GetPairedDevices", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_GetPairedDevices);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_GetDeviceProperties", PARAMS_BY_NAME, JSON_STRING,"devicehandle",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_GetDeviceProperties);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_StartAudioStreamingOut", PARAMS_BY_NAME, JSON_STRING,"devicetype",JSON_INTEGER,"devicehandle",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_StartAudioStreamingOut);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_StopAudioStreamingOut", PARAMS_BY_NAME,JSON_STRING,"devicehandle",JSON_STRING,NULL), &BluetoothAgent::Bluetooth_StopAudioStreamingOut);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_IsAudioStreamingOut", PARAMS_BY_NAME,JSON_STRING,NULL), &BluetoothAgent::Bluetooth_IsAudioStreamingOut);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_ResetAdapter", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_ResetAdapter);
                    this->bindAndAddMethod(Procedure("TestMgr_Bluetooth_SendRequest", PARAMS_BY_NAME, JSON_STRING,NULL), &BluetoothAgent::Bluetooth_SendRequest);
                }

                //Inherited functions
                bool initialize(IN const char* szVersion);

                bool cleanup(const char*);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                void Bluetooth_GetNumberOfAdapters(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_GetAdapterName(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_SetAdapterName(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_GetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_SetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_IsAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_SetAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_StartDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_StopDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_GetDiscoveredDevices(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_ConnectToDevice(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_DisconnectFromDevice(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_GetConnectedDevices(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_PairDevice(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_UnpairDevice(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_GetPairedDevices(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_GetDeviceProperties(IN const Json::Value& req, OUT Json::Value& response);         
                void Bluetooth_StartAudioStreamingOut(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_StopAudioStreamingOut(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_IsAudioStreamingOut(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_ResetAdapter(IN const Json::Value& req, OUT Json::Value& response);
                void Bluetooth_SendRequest(IN const Json::Value& req, OUT Json::Value& response);
               
};
#endif //__BLUETOOTH_STUB_H__
