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

#ifndef __AUDIOCAPTUREMGR_STUB_H__
#define __AUDIOCAPTUREMGR_STUB_H__


#include <json/json.h> 
#include <fstream>
#include <stddef.h>
#include <string>
#include <sys/time.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#include "audiocapturemgr_iarm.h"
#include <pthread.h>
#include "libIBus.h"
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define BUFF_LENGTH 512
#define STR_LEN_20 20
#define STR_LEN_50 50
#define STR_LEN_100 100

using namespace std;

/*using namespace audiocapturemgr;
audio_properties_t properties;*/

class RDKTestAgent;
class AudioCaptureMgrAgent : public RDKTestStubInterface , public AbstractServer<AudioCaptureMgrAgent>
{
        public:
                AudioCaptureMgrAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <AudioCaptureMgrAgent>(ptrRpcServer)
                {
                  // ServiceManager APIs
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_Session_Open", PARAMS_BY_NAME,JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_SessionOpen);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_Session_Close", PARAMS_BY_NAME,JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_SessionClose);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_GetSessionDetails", PARAMS_BY_NAME,JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_GetSessionDetails);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_GetDefaultAudioProperties", PARAMS_BY_NAME,JSON_STRING, "session",JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_GetDefaultAudioProperties);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_GetAudioProperties", PARAMS_BY_NAME,JSON_STRING, "session",JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_GetAudioProperties);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_SetAudioProperties", PARAMS_BY_NAME,JSON_STRING, "session",JSON_STRING, "delay",JSON_INTEGER, "fifoSize", JSON_INTEGER, "threshold",JSON_INTEGER, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_SetAudioProperties);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_GetOutputProperties", PARAMS_BY_NAME,JSON_STRING, "session",JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_GetOutputProperties);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_Start", PARAMS_BY_NAME,JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_Start);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_Stop", PARAMS_BY_NAME,JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_Stop);
                  this->bindAndAddMethod(Procedure("TestMgr_AudioCaptureMgr_ExecuteCmd", PARAMS_BY_NAME,JSON_STRING, "command",JSON_STRING, NULL), &AudioCaptureMgrAgent::AudioCaptureMgr_ExecuteCmd);
		}

                //Inherited functions
                bool initialize(IN const char* szVersion);

                bool cleanup(const char*);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
		void AudioCaptureMgr_SessionOpen(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_SessionClose(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_GetSessionDetails(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_GetDefaultAudioProperties(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_GetAudioProperties(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_SetAudioProperties(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_GetOutputProperties(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_Start(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_Stop(IN const Json::Value& req, OUT Json::Value& response);
		void AudioCaptureMgr_ExecuteCmd(IN const Json::Value& req, OUT Json::Value& response);
};

using namespace audiocapturemgr;
session_id_t session = -1;
audio_properties_ifce_t props;
std::string socketPath;
static const char * instance_name = NULL;
#endif //__AUDIOCAPTUREMGR_STUB_H__

