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
#include "dsHdmiIn.h"


#include "libIBus.h"
#include "libIBusDaemon.h"

#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

using namespace std;

int vpHandle = 0;
int vdHandle = 0;
int apHandle = 0;
int dispHandle = 0;
string error = "";

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
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_HdmiInGetNumberOfInputs", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_HdmiInGetNumberOfInputs);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsOutputHDR", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsOutputHDR);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsAudioMute", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsAudioMute);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetAudioMute", PARAMS_BY_NAME, JSON_STRING, "muted", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetAudioMute);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetAudioDelay", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetAudioDelay);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetAudioDelay", PARAMS_BY_NAME, JSON_STRING, "audioDelay", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetAudioDelay);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetAudioDelayOffset", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetAudioDelayOffset);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetAudioDelayOffset", PARAMS_BY_NAME, JSON_STRING, "offset", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetAudioDelayOffset);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsAudioMSDecode", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsAudioMSDecode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsAudioMS12Decode", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsAudioMS12Decode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetHdmiPreference", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetHdmiPreference);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetHdmiPreference", PARAMS_BY_NAME, JSON_STRING, "hdcpProtocol", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetHdmiPreference);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetBackgroundColor", PARAMS_BY_NAME, JSON_STRING, "color", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetBackgroundColor);
		    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetFPBrightness", PARAMS_BY_NAME, JSON_STRING,"indicator",JSON_INTEGER,"brightness",JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetFPBrightness);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetFPBrightness", PARAMS_BY_NAME, JSON_STRING,"indicator",JSON_INTEGER,NULL), &DSHalAgent::DSHal_GetFPBrightness);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetCPUTemperature", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetCPUTemperature);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetVersion", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetVersion);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetVersion", PARAMS_BY_NAME, JSON_STRING, "version", JSON_INTEGER, NULL), &DSHalAgent::DSHal_SetVersion);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetHDRCapabilities", PARAMS_BY_NAME, JSON_STRING, NULL), &DSHalAgent::DSHal_GetHDRCapabilities);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetSupportedVideoCodingFormats", PARAMS_BY_NAME, JSON_STRING, NULL),&DSHalAgent::DSHal_GetSupportedVideoCodingFormats);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetVideoCodecInfo", PARAMS_BY_NAME, JSON_STRING, "format", JSON_STRING, NULL),&DSHalAgent::DSHal_GetVideoCodecInfo);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetTVHDRCapabilities", PARAMS_BY_NAME, JSON_STRING, NULL),&DSHalAgent::DSHal_GetTVHDRCapabilities);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetFPBlink", PARAMS_BY_NAME, JSON_STRING, "indicator", JSON_INTEGER, "blinkDuration", JSON_INTEGER, "blinkIteration", JSON_INTEGER, NULL),&DSHalAgent::DSHal_SetFPBlink);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetFPColor", PARAMS_BY_NAME, JSON_STRING, "indicator", JSON_INTEGER, "color", JSON_STRING, NULL),&DSHalAgent::DSHal_SetFPColor);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetFPTime", PARAMS_BY_NAME, JSON_STRING, "format", JSON_STRING, "hours", JSON_INTEGER, "minutes", JSON_INTEGER, NULL),&DSHalAgent::DSHal_SetFPTime);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetFPText", PARAMS_BY_NAME, JSON_STRING, "text", JSON_STRING, NULL),&DSHalAgent::DSHal_SetFPText);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetFPTextBrightness", PARAMS_BY_NAME, JSON_STRING, "brightness", JSON_INTEGER, NULL),&DSHalAgent::DSHal_SetFPTextBrightness);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_HdmiInGetStatus", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_HdmiInGetStatus);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetVideoEOTF", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetVideoEOTF);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_HdmiInScaleVideo", PARAMS_BY_NAME, JSON_STRING, "x", JSON_INTEGER, "y", JSON_INTEGER, "width", JSON_INTEGER ,"height", JSON_INTEGER,NULL), &DSHalAgent::DSHal_HdmiInScaleVideo);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_IsHDCPEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_IsHDCPEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_EnableLEConfig", PARAMS_BY_NAME, JSON_STRING, "enable", JSON_INTEGER,NULL), &DSHalAgent::DSHal_EnableLEConfig);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetLEConfig", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetLEConfig);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetSupportedTvResolutions", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetSupportedTvResolutions);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetMatrixCoefficients", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetMatrixCoefficients);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetDolbyVolumeMode", PARAMS_BY_NAME, JSON_STRING, "mode", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetDolbyVolumeMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetDolbyVolumeMode", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetDolbyVolumeMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetSocIDFromSDK", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetSocIDFromSDK);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetResolution", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetResolution);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetResolution", PARAMS_BY_NAME, JSON_STRING, "resolution", JSON_STRING,NULL), &DSHalAgent::DSHal_SetResolution);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetIntelligentEqualizerMode", PARAMS_BY_NAME, JSON_STRING, "mode", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetIntelligentEqualizerMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetIntelligentEqualizerMode", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetIntelligentEqualizerMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetDialogEnhancement", PARAMS_BY_NAME, JSON_STRING, "level", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetDialogEnhancement);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetDialogEnhancement", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetDialogEnhancement);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetEDID", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetEDID);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetEDIDBytes", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetEDIDBytes);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_HdmiInSelectZoomMode", PARAMS_BY_NAME, JSON_STRING, "mode", JSON_INTEGER,NULL), &DSHalAgent::DSHal_HdmiInSelectZoomMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetCurrentOutputSettings", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetCurrentOutputSettings);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_HdmiInSelectPort", PARAMS_BY_NAME, JSON_STRING, "port", JSON_INTEGER,NULL), &DSHalAgent::DSHal_HdmiInSelectPort);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetHdmiInCurrentVideoMode", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetHdmiInCurrentVideoMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetAudioAtmosOutputMode", PARAMS_BY_NAME, JSON_STRING, "enable", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetAudioAtmosOutputMode);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetSinkDeviceAtmosCapability", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetSinkDeviceAtmosCapability);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_SetAudioCompression", PARAMS_BY_NAME, JSON_STRING, "audioCompression", JSON_INTEGER,NULL), &DSHalAgent::DSHal_SetAudioCompression);
                    this->bindAndAddMethod(Procedure("TestMgr_DSHal_GetAudioCompression", PARAMS_BY_NAME, JSON_STRING,NULL), &DSHalAgent::DSHal_GetAudioCompression);
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
                void DSHal_HdmiInGetNumberOfInputs(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsOutputHDR(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsAudioMute(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetAudioMute(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetAudioDelay(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetAudioDelayOffset(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetAudioDelayOffset(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetAudioDelay(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsAudioMSDecode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsAudioMS12Decode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetHdmiPreference(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetHdmiPreference(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetBackgroundColor(IN const Json::Value& req, OUT Json::Value& response);
		void DSHal_SetFPBrightness(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetFPBrightness(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetCPUTemperature(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetVersion(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetVersion(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetHDRCapabilities(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetSupportedVideoCodingFormats(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetVideoCodecInfo(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetTVHDRCapabilities(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetFPBlink(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetFPColor(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetFPTime(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetFPText(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetFPTextBrightness(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_HdmiInGetStatus(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetVideoEOTF(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_HdmiInScaleVideo(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_IsHDCPEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_EnableLEConfig(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetLEConfig(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetSupportedTvResolutions(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetMatrixCoefficients(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetDolbyVolumeMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetDolbyVolumeMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetSocIDFromSDK(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetResolution(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetResolution(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetIntelligentEqualizerMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetIntelligentEqualizerMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetDialogEnhancement(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetDialogEnhancement(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_HdmiInSelectZoomMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetEDID(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetEDIDBytes(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetCurrentOutputSettings(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_HdmiInSelectPort(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetHdmiInCurrentVideoMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetAudioAtmosOutputMode(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetSinkDeviceAtmosCapability(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_GetAudioCompression(IN const Json::Value& req, OUT Json::Value& response);
                void DSHal_SetAudioCompression(IN const Json::Value& req, OUT Json::Value& response);
};
#endif //__DSHAL_STUB_H__
