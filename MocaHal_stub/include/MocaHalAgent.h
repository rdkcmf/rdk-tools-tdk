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
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMoCAVersion", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMoCAVersion);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetNumNodes", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetNumNodes);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetSupportedModes", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetSupportedModes);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMode", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMode); 
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetSoftwareVersion", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetSoftwareVersion);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetSupportedBand", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetSupportedBand);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMaxBitRate", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMaxBitRate);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetNodeId", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetNodeId);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetLinkUptime", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetLinkUptime);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetTxBroadcastPhyRate", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetTxBroadcastPhyRate);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetTxPowerLimit", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetTxPowerLimit);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_SetLOF", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_SetLOF);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetPreferredNCEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetPreferredNCEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_SetPreferredNCEnabled", PARAMS_BY_NAME, JSON_STRING,"enable",JSON_INTEGER,NULL), &MocaHalAgent::MocaHal_SetPreferredNCEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMaxPacketAggregation", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMaxPacketAggregation);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMaxFrameSize", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMaxFrameSize);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetLowBandwidthLimit", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetLowBandwidthLimit);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetTurboEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetTurboEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_SetTurboEnabled", PARAMS_BY_NAME, JSON_STRING,"enable",JSON_INTEGER,NULL), &MocaHalAgent::MocaHal_SetTurboEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetPrivacyEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetPrivacyEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetTxPowerControlEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetTxPowerControlEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetTxBeaconPowerReductionEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetTxBeaconPowerReductionEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetNCNodeId", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetNCNodeId);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetBackupNCNodeId", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetBackupNCNodeId);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetMixedMode", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetMixedMode);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetNetworkNodeIds", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetNetworkNodeIds);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetRemoteNodeIds", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetRemoteNodeIds);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetNCMac", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetNCMac);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetTxMapPhyRate", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetTxMapPhyRate);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_RemoteNode_GetMac", PARAMS_BY_NAME, JSON_STRING, "nodeId",JSON_INTEGER,NULL), &MocaHalAgent::MocaHal_RemoteNode_GetMac);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_RemoteNode_GetPreferredNC", PARAMS_BY_NAME, JSON_STRING, "nodeId",JSON_INTEGER,NULL), &MocaHalAgent::MocaHal_RemoteNode_GetPreferredNC);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetLinkDownCount", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetLinkDownCount);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetResetCount", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetResetCount);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetTxGCDPhyRate", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetTxGCDPhyRate);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetRFChannelFreq", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetRFChannelFreq);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetPrimaryChannelFreq", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetPrimaryChannelFreq);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_GetSecondaryChannelFreq", PARAMS_BY_NAME, JSON_STRING,NULL), &MocaHalAgent::MocaHal_GetSecondaryChannelFreq);
                    this->bindAndAddMethod(Procedure("TestMgr_MocaHal_RemoteNode_GetActiveMoCAVersion", PARAMS_BY_NAME, JSON_STRING, "nodeId",JSON_INTEGER,NULL), &MocaHalAgent::MocaHal_RemoteNode_GetActiveMoCAVersion);
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
                void MocaHal_GetSoftwareVersion(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetSupportedBand(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMaxBitRate(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetNodeId(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetLinkUptime(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetTxBroadcastPhyRate(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetTxPowerLimit(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_SetLOF(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_SetPreferredNCEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetPreferredNCEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMaxPacketAggregation(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMaxFrameSize(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetLowBandwidthLimit(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetTurboEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_SetTurboEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetPrivacyEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetTxPowerControlEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetTxBeaconPowerReductionEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetNCNodeId(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetBackupNCNodeId(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetMixedMode(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetNetworkNodeIds(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetRemoteNodeIds(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetNCMac(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetTxMapPhyRate(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_RemoteNode_GetMac(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_RemoteNode_GetPreferredNC(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetLinkDownCount(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetResetCount(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetTxGCDPhyRate(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetRFChannelFreq(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetPrimaryChannelFreq(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_GetSecondaryChannelFreq(IN const Json::Value& req, OUT Json::Value& response);
                void MocaHal_RemoteNode_GetActiveMoCAVersion(IN const Json::Value& req, OUT Json::Value& response);
};
#endif //__MOCAHAL_STUB_H__
