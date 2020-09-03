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

#ifndef __HDMICECHAL_STUB_H__
#define __HDMICECHAL_STUB_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <mutex>
#include <chrono>
#include <vector>
#include <sstream>
#include <condition_variable>

#include "libIBus.h"
#include "libIBusDaemon.h"
#include "ccec/drivers/hdmi_cec_driver.h"
#include "ccec/drivers/CecIARMBusMgr.h"

#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define MAX_LENGTH 128

char txMethod[30];
char txStatus[50];

int cec_frame_size_tx = 0;
int cec_frame_size_rx = 0;
uint8_t cec_frame_tx[MAX_LENGTH];
uint8_t cec_frame_rx[MAX_LENGTH];

std::string cec_frame_rx_str;
std::string cec_frame_header;
std::string cec_frame_result;

const int TIMEOUT = 60;
int driverHandle = 0;
int transmit_status = 0;
int received_status = 0;
int cec_header_flag = 0;
int cec_device_ready = 0;
bool cec_receive_flag = 1;

std::mutex              m_idle;
std::condition_variable m_cv;
std::condition_variable m_cv_init;


using namespace std;

class RDKTestAgent;
class HdmicecHalAgent : public RDKTestStubInterface , public AbstractServer<HdmicecHalAgent>
{
        public:
                //Constructor
                HdmicecHalAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <HdmicecHalAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod(Procedure("TestMgr_HdmicecHal_GetLogicalAddress", PARAMS_BY_NAME, JSON_STRING, "dev_type", JSON_INTEGER, NULL), &HdmicecHalAgent::HdmicecHal_GetLogicalAddress);
                    this->bindAndAddMethod(Procedure("TestMgr_HdmicecHal_GetPhysicalAddress", PARAMS_BY_NAME, JSON_STRING, NULL), &HdmicecHalAgent::HdmicecHal_GetPhysicalAddress);
                    this->bindAndAddMethod(Procedure("TestMgr_HdmicecHal_Tx", PARAMS_BY_NAME, JSON_STRING, "header", JSON_STRING, "opcode", JSON_STRING, "receive_frames", JSON_INTEGER, NULL), &HdmicecHalAgent::HdmicecHal_Tx);
                    this->bindAndAddMethod(Procedure("TestMgr_HdmicecHal_TxAsync", PARAMS_BY_NAME, JSON_STRING, "header", JSON_STRING, "opcode", JSON_STRING, "receive_frames", JSON_INTEGER, NULL), &HdmicecHalAgent::HdmicecHal_TxAsync);
                    this->bindAndAddMethod(Procedure("TestMgr_HdmicecHal_SetTxCallback", PARAMS_BY_NAME, JSON_STRING, NULL), &HdmicecHalAgent::HdmicecHal_SetTxCallback);
                    this->bindAndAddMethod(Procedure("TestMgr_HdmicecHal_SetRxCallback", PARAMS_BY_NAME, JSON_STRING, NULL), &HdmicecHalAgent::HdmicecHal_SetRxCallback);
                }

                //Inherited functions
                bool initialize(IN const char* szVersion);
                bool cleanup(const char* szVersion);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                void HdmicecHal_GetLogicalAddress(IN const Json::Value& req, OUT Json::Value& response);
                void HdmicecHal_GetPhysicalAddress(IN const Json::Value& req, OUT Json::Value& response);
                void HdmicecHal_Tx(IN const Json::Value& req, OUT Json::Value& response);
                void HdmicecHal_TxAsync(IN const Json::Value& req, OUT Json::Value& response);
                void HdmicecHal_SetTxCallback(IN const Json::Value& req, OUT Json::Value& response);
                void HdmicecHal_SetRxCallback(IN const Json::Value& req, OUT Json::Value& response);

};
#endif //__HDMICECHAL_STUB_H__
