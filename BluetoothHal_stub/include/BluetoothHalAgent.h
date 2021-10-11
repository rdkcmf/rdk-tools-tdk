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

#define BT_ADAPTER_STR_LEN 64

using namespace std;

class RDKTestAgent;
class BluetoothHalAgent : public RDKTestStubInterface , public AbstractServer<BluetoothHalAgent>
{
        public:
                //Constructor
                BluetoothHalAgent (TcpSocketServer &ptrRpcServer) : AbstractServer <BluetoothHalAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetListOfAdapters", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetListOfAdapters);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_RegisterAgent", PARAMS_BY_NAME, JSON_STRING, "capabilities", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_RegisterAgent);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_UnregisterAgent", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_UnregisterAgent);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetAdapter", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetAdapter);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_SetAdapter", PARAMS_BY_NAME, JSON_STRING, "adapter_number", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_SetAdapter);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetAdapters", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetAdapters);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetAdapterPower", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetAdapterPower);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_SetAdapterPower", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, "power_status", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_SetAdapterPower);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_EnableAdapter", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_EnableAdapter);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_DisableAdapter", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_DisableAdapter);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetAdapterAddr", PARAMS_BY_NAME, JSON_STRING, "adapter_number", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_GetAdapterAddr);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_SetAdapterDiscoverable", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, "discoverable_status", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_SetAdapterDiscoverable);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_SetAdapterDiscoverableTimeout", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, "timeout", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_SetAdapterDiscoverableTimeout);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetAdapterDiscoverableStatus", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetAdapterDiscoverableStatus);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetAdapterName", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetAdapterName);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_SetAdapterName", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, "adapter_name", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_SetAdapterName);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetVersionInfo", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetVersionInfo);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_StartDiscovery", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, "timeout", JSON_INTEGER, "device_type", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_StartDiscovery);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_StopDiscovery", PARAMS_BY_NAME, JSON_STRING, "adapter_path", JSON_STRING, "device_type", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_StopDiscovery);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetListOfScannedDevices", PARAMS_BY_NAME, JSON_STRING, "get_Address_and_Path", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_GetListOfScannedDevices);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_PairDevice", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_PairDevice);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_UnPairDevice", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_UnPairDevice);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetListOfPairedDevices", PARAMS_BY_NAME, JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetListOfPairedDevices);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_IsDeviceConnectable", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_IsDeviceConnectable);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_ConnectDevice", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, "device_type", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_ConnectDevice);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_DisconnectDevice", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, "device_type", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_DisconnectDevice);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetDeviceConnected", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, "device_type", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_GetDeviceConnected);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetDeviceDisconnected", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, "device_type", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_GetDeviceDisconnected);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_FindDevice", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_FindDevice);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_FindService", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, "uuid", JSON_STRING, "xml_data", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_FindService);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetSupportedServices", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, NULL), &BluetoothHalAgent::BluetoothHal_GetSupportedServices);
                    this->bindAndAddMethod (Procedure ("TestMgr_BluetoothHal_GetDeviceTypeClass", PARAMS_BY_NAME, JSON_STRING, "device_id", JSON_STRING, "device_type", JSON_INTEGER, NULL), &BluetoothHalAgent::BluetoothHal_GetDeviceTypeClass);
                }

                //Inherited functions
                bool initialize (IN const char* szVersion);

                bool cleanup (const char*);
                std::string testmodulepre_requisites ();
                bool testmodulepost_requisites ();

                //Stub functions
                void BluetoothHal_GetListOfAdapters (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_RegisterAgent (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_UnregisterAgent (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetAdapter (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_SetAdapter (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetAdapters (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetAdapterPower (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_SetAdapterPower (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_EnableAdapter (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_DisableAdapter (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetAdapterAddr (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_SetAdapterDiscoverable (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_SetAdapterDiscoverableTimeout (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetAdapterDiscoverableStatus (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetAdapterName (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_SetAdapterName (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetVersionInfo (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_StartDiscovery (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_StopDiscovery (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetListOfScannedDevices (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_PairDevice (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_UnPairDevice (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetListOfPairedDevices (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_IsDeviceConnectable (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_ConnectDevice (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_DisconnectDevice (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetDeviceConnected (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetDeviceDisconnected (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_FindDevice (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_FindService (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetSupportedServices (IN const Json::Value& req, OUT Json::Value& response);
                void BluetoothHal_GetDeviceTypeClass (IN const Json::Value& req, OUT Json::Value& response);
};
#endif //__BLUETOOTHHAL_STUB_H__

