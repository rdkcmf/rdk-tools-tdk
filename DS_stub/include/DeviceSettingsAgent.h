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

#ifndef __DEVICESETTINGS_AGENT_H__
#define __DEVICESETTINGS_AGENT_H__
#include <json/json.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <unistd.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "host.hpp"
#include "videoOutputPort.hpp"
#include "videoOutputPortType.hpp"
#include "videoOutputPortConfig.hpp"
#include "videoDeviceConfig.hpp"
#include "videoResolution.hpp"
#include "manager.hpp"
#include "dsUtl.h"
#include "dsError.h"
#include "list.hpp"
#include "frontPanelConfig.hpp"
#include "frontPanelIndicator.hpp"
#include "frontPanelTextDisplay.hpp"
#include "audioEncoding.hpp"
#include "audioCompression.hpp"
#include "audioStereoMode.hpp"
#include "manager.hpp"
#include "audioOutputPort.hpp"
#include "audioOutputPortType.hpp"
#include "audioOutputPortConfig.hpp"
#include "pixelResolution.hpp"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#include "libIBus.h"
#include "libIBusDaemon.h"
#include "mfrMgr.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define STR_LEN   128
#define LINE_LEN  1024
#define MFRMGR    "mfrMgrMain"

class PowerChangeNotify: public device::PowerModeChangeListener
{
	public:
		void powerModeChanged(int newMode)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nPower Mode Changed to:%d",newMode);
			return;
		}
};

class DispChangeNotify:public device::DisplayConnectionChangeListener
{
	public:
		void displayConnectionChanged(device::VideoOutputPort &port, int newConnectionStatus)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nDisplay Connections status: CONNECTED(0):DISCONNECTED(1):%d",newConnectionStatus);
			return;
		}
};


class RDKTestAgent;
class DeviceSettingsAgent : public RDKTestStubInterface , public AbstractServer<DeviceSettingsAgent> 
{
	public:
		/*Ctor*/
		DeviceSettingsAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <DeviceSettingsAgent>(ptrRpcServer)
                {
                  this->bindAndAddMethod(Procedure("TestMgr_DS_managerInitialize", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::DSmanagerInitialize);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_managerDeinitialize", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::DSmanagerDeinitialize);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setBrightness", PARAMS_BY_NAME, JSON_STRING, "brightness",JSON_INTEGER, "get_only",JSON_INTEGER, "indicator_name",JSON_STRING,NULL), &DeviceSettingsAgent::FPI_setBrightness);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setState", PARAMS_BY_NAME, JSON_STRING,"state", JSON_INTEGER, "indicator_name", JSON_STRING,NULL), &DeviceSettingsAgent::FPI_setState);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setColor", PARAMS_BY_NAME, JSON_STRING,"color",JSON_INTEGER, "indicator_name", JSON_STRING,NULL), &DeviceSettingsAgent::FPI_setColor);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setBlink", PARAMS_BY_NAME, JSON_STRING,"blink_interval",JSON_INTEGER, "blink_iteration",JSON_INTEGER,"indicator_name", JSON_STRING,NULL), &DeviceSettingsAgent::FPI_setBlink);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_FP_getSupportedColors", PARAMS_BY_NAME, JSON_STRING,"indicator_name",JSON_STRING,NULL), &DeviceSettingsAgent::FPI_getSupportedColors);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getBrightnessLevels", PARAMS_BY_NAME, JSON_STRING,"indicator_name", JSON_STRING,NULL), &DeviceSettingsAgent::FPI_getBrightnessLevels);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getColorMode", PARAMS_BY_NAME, JSON_STRING,"indicator_name", JSON_STRING,NULL), &DeviceSettingsAgent::FPI_getColorMode);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setText", PARAMS_BY_NAME, JSON_STRING,"text_display", JSON_STRING,"text", JSON_STRING,NULL), &DeviceSettingsAgent::FPTEXT_setText);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setTimeForamt", PARAMS_BY_NAME, JSON_STRING,"text",JSON_STRING, "time_format",JSON_INTEGER, NULL),&DeviceSettingsAgent::FPTEXT_setTimeFormat); 
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setTime", PARAMS_BY_NAME, JSON_STRING,"time_hrs", JSON_INTEGER, "time_mins",JSON_INTEGER, NULL), &DeviceSettingsAgent::FPTEXT_setTime);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setScroll", PARAMS_BY_NAME, JSON_STRING,"text", JSON_STRING, "viteration",JSON_INTEGER,"hiteration", JSON_INTEGER, "hold_duration",JSON_INTEGER, NULL), &DeviceSettingsAgent::FPTEXT_setScroll);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getTextColorMode", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::FPTEXT_getTextColorMode);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getTextBrightnessLevels", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::FPTEXT_getTextBrightnessLevels);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_setTextBrightness", PARAMS_BY_NAME, JSON_STRING, "brightness",JSON_INTEGER,NULL), &DeviceSettingsAgent::FPTEXT_setTextBrightness);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getTextBrightness", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::FPTEXT_getTextBrightness);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_enableDisplay", PARAMS_BY_NAME, JSON_STRING,"enable",JSON_INTEGER, NULL), &DeviceSettingsAgent::FPTEXT_enableDisplay);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getIndicatorFromName", PARAMS_BY_NAME, JSON_STRING,"indicator_name", JSON_STRING,NULL), &DeviceSettingsAgent::FPCONFIG_getIndicatorFromName);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getIndicatorFromId", PARAMS_BY_NAME, JSON_STRING,"indicator_id", JSON_INTEGER, NULL), &DeviceSettingsAgent::FPCONFIG_getIndicatorFromId);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getIndicators", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::FPCONFIG_getIndicators);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getTextDisplayFromName", PARAMS_BY_NAME, JSON_STRING,"text_name", JSON_STRING,NULL), &DeviceSettingsAgent::FPCONFIG_getTextDisplayFromName);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getTextDisplayFromId", PARAMS_BY_NAME, JSON_STRING,"text_id",JSON_INTEGER, NULL), &DeviceSettingsAgent::FPCONFIG_getTextDisplayFromId);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getTextDisplays", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::FPCONFIG_getTextDisplays);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_FP_getColors", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::FPCONFIG_getColors);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOPCONFIG_getPortType", PARAMS_BY_NAME, JSON_STRING, "port_id", JSON_INTEGER,NULL), &DeviceSettingsAgent::AOPCONFIG_getPortType);

                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOPCONFIG_getPortFromName", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::AOPCONFIG_getPortFromName);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOPCONFIG_getPortFromId", PARAMS_BY_NAME, JSON_STRING,"port_id", JSON_INTEGER, NULL), &DeviceSettingsAgent::AOPCONFIG_getPortFromId);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOPCONFIG_getPorts", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::AOPCONFIG_getPorts);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOPCONFIG_getSupportedTypes", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::AOPCONFIG_getSupportedTypes);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOPCONFIG_release", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::AOPCONFIG_release);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOPCONFIG_load", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::AOPCONFIG_load);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_getSupportedEncodings", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::AOPTYPE_getSupportedEncodings);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_getSupportedCompressions", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::AOPTYPE_getSupportedCompressions);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_getSupportedStereoModes", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::AOPTYPE_getSupportedStereoModes);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_setLevel", PARAMS_BY_NAME, JSON_STRING,"port_name",JSON_STRING, "audio_level", JSON_REAL,NULL), &DeviceSettingsAgent::AOP_setLevel);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_setDB", PARAMS_BY_NAME, JSON_STRING,"port_name",JSON_STRING,"db_level", JSON_REAL,NULL), &DeviceSettingsAgent::AOP_setDB);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_setEncoding", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,"encoding_format", JSON_STRING,NULL), &DeviceSettingsAgent::AOP_setEncoding);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_setCompression", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,"compression_format", JSON_INTEGER, "get_only", JSON_INTEGER,NULL), &DeviceSettingsAgent::AOP_setCompression);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_setStereoMode", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,"stereo_mode", JSON_STRING,"get_only", JSON_INTEGER,NULL), &DeviceSettingsAgent::AOP_setStereoMode);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_loopThru", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING, "loop_thru", JSON_INTEGER,NULL), &DeviceSettingsAgent::AOP_loopThru);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_mutedStatus", PARAMS_BY_NAME, JSON_STRING,"port_name",JSON_STRING,"mute_status",  JSON_INTEGER,NULL), &DeviceSettingsAgent::AOP_mutedStatus);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_setStereoAuto", PARAMS_BY_NAME, JSON_STRING,"port_name",JSON_STRING,"autoMode", JSON_INTEGER,NULL), &DeviceSettingsAgent::AOP_setStereoAuto);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_getStereoAuto", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::AOP_getStereoAuto);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_getGain", PARAMS_BY_NAME, JSON_STRING, "port_name", JSON_STRING,NULL), &DeviceSettingsAgent::AOP_getGain);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_AOP_getOptimalLevel", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::AOP_getOptimalLevel);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_setResolution", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,"resolution", JSON_STRING,"get_only", JSON_INTEGER,NULL), &DeviceSettingsAgent::VOP_setResolution);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_getDefaultResolution", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_getDefaultResolution);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_isDisplayConnected", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_isDisplayConnected);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_getHDCPStatus", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_getHDCPStatus);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_getAspectRatio", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_getAspectRatio);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_getDisplayDetails", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_getDisplayDetails);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_isContentProtected", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_isContentProtected);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_setEnable", PARAMS_BY_NAME, JSON_STRING,"port_name",JSON_STRING, "enable", JSON_INTEGER,NULL), &DeviceSettingsAgent::VOP_setEnable);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_isActive", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_isActive);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_setDisplayConnected", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,"connected",JSON_INTEGER,NULL), &DeviceSettingsAgent::VOP_setDisplayConnected);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_hasSurround", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_hasSurround);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOP_getEDIDBytes", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOP_getEDIDBytes);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPTYPE_isHDCPSupported", PARAMS_BY_NAME, JSON_STRING,"port_name",JSON_STRING,NULL), &DeviceSettingsAgent::VOPTYPE_isHDCPSupported);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPTYPE_enableHDCP", PARAMS_BY_NAME, JSON_STRING, "port_name",JSON_STRING, "protectContent",JSON_INTEGER, "hdcpKey",JSON_STRING, "keySize", JSON_INTEGER,"useMfrKey", JSON_INTEGER,NULL), &DeviceSettingsAgent::VOPTYPE_enableHDCP);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPTYPE_isDynamicResolutionSupported", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOPTYPE_isDynamicResolutionSupported);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_Resolutions", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOPTYPE_getSupportedResolutions);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPTYPE_getPorts", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VOPTYPE_getPorts);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPTYPE_setRestrictedResolution", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING, "resolution",JSON_INTEGER, NULL), &DeviceSettingsAgent::VOPTYPE_setRestrictedResolution);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPTYPE_getRestrictedResolution", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOPTYPE_getRestrictedResolution);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getPixelResolution", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOPCONFIG_getPixelResolution);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getSSMode", PARAMS_BY_NAME,  JSON_STRING, "ss_id",JSON_INTEGER, NULL), &DeviceSettingsAgent::VOPCONFIG_getSSMode);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getVideoResolution", PARAMS_BY_NAME, JSON_STRING, "port_id", JSON_INTEGER,NULL), &DeviceSettingsAgent::VOPCONFIG_getVideoResolution);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getFrameRate", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOPCONFIG_getFrameRate);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getPortType", PARAMS_BY_NAME, JSON_STRING,"port_id", JSON_INTEGER, NULL), &DeviceSettingsAgent::VOPCONFIG_getPortType);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getPortFromName", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VOPCONFIG_getPortFromName);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getPortFromId", PARAMS_BY_NAME,  JSON_STRING,"port_id", JSON_INTEGER,NULL), &DeviceSettingsAgent::VOPCONFIG_getPortFromId);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VOPCONFIG_getSupportedTypes", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VOPCONFIG_getSupportedTypes);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VD_setDFC", PARAMS_BY_NAME, JSON_STRING,"zoom_setting", JSON_STRING,NULL), &DeviceSettingsAgent::VD_setDFC);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VD_setPlatformDFC", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VD_setPlatformDFC);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VD_getSupportedDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VD_getSupportedDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VD_getHDRCapabilities", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VD_getHDRCapabilities);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDevices", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDevices);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDefaultDFC", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDefaultDFC);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VR_isInterlaced", PARAMS_BY_NAME, JSON_STRING,"port_name", JSON_STRING,NULL), &DeviceSettingsAgent::VR_isInterlaced);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_setPowerMode", PARAMS_BY_NAME,  JSON_STRING,"new_power_state",JSON_INTEGER,NULL), &DeviceSettingsAgent::HOST_setPowerMode);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_addPowerModeListener", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_addPowerModeListener);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_removePowerModeListener", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_removePowerModeListener);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_addDisplayConnectionListener", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_addDisplayConnectionListener);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_removeDisplayConnectionListener", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_removeDisplayConnectionListener);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getCPUTemperature", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_getCPUTemperature);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_setVersion", PARAMS_BY_NAME, JSON_STRING,"versionNo", JSON_INTEGER,NULL), &DeviceSettingsAgent::HOST_setVersion);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_setPreferredSleepMode", PARAMS_BY_NAME, JSON_STRING,"sleepMode", JSON_STRING,NULL), &DeviceSettingsAgent::HOST_setPreferredSleepMode);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getPreferredSleepMode", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_getPreferredSleepMode);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getAvailableSleepModes", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_getAvailableSleepModes);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_VDCONFIG_getDFCs", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::VDCONFIG_getDFCs);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getAudioOutputPorts", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_getAudioOutputPorts);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getVideoOutputPorts", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_getVideoOutputPorts);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getHostEDID", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_getHostEDID);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getVideoDevices", PARAMS_BY_NAME, JSON_STRING,NULL), &DeviceSettingsAgent::HOST_getVideoDevices);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getAudioOutputPortFromId", PARAMS_BY_NAME, JSON_STRING, "port_id", JSON_INTEGER, NULL), &DeviceSettingsAgent::HOST_getAudioOutputPortFromId);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getVideoOutputPortFromId", PARAMS_BY_NAME, JSON_STRING, "port_id", JSON_INTEGER, NULL), &DeviceSettingsAgent::HOST_getVideoOutputPortFromId);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getVideoOutputPortFromName", PARAMS_BY_NAME, JSON_STRING, "port_name", JSON_STRING, NULL), &DeviceSettingsAgent::HOST_getVideoOutputPortFromName);
                  this->bindAndAddMethod(Procedure("TestMgr_DS_HOST_getAudioOutputPortFromName", PARAMS_BY_NAME, JSON_STRING, "port_name", JSON_STRING, NULL), &DeviceSettingsAgent::HOST_getAudioOutputPortFromName);
                }

		/*inherited functions*/
		bool initialize(IN const char* szVersion);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		void DSmanagerInitialize(IN const Json::Value& req, OUT Json::Value& response);
		void DSmanagerDeinitialize(IN const Json::Value& req, OUT Json::Value& response);
		void FPI_setBrightness(IN const Json::Value& req, OUT Json::Value& response);
		void FPI_setState(IN const Json::Value& req, OUT Json::Value& response);
		void FPI_setColor(IN const Json::Value& req, OUT Json::Value& response);
		void FPI_setBlink(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_setScroll(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_setLevel(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_setDB(IN const Json::Value& req, OUT Json::Value& response);
		void VD_setDFC(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_setEncoding(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_setCompression(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_setStereoMode(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_setPowerMode(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_setResolution(IN const Json::Value& req, OUT Json::Value& response);
		void FPCONFIG_getIndicators(IN const Json::Value& req, OUT Json::Value& response);
		void FPI_getSupportedColors(IN const Json::Value& req, OUT Json::Value& response);
		void FPCONFIG_getTextDisplays(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_setText(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_setTimeFormat(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_setTime(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_loopThru(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_mutedStatus(IN const Json::Value& req, OUT Json::Value& response);
		void AOPTYPE_getSupportedEncodings(IN const Json::Value& req, OUT Json::Value& response);
		void AOPTYPE_getSupportedCompressions(IN const Json::Value& req, OUT Json::Value& response);
		void AOPTYPE_getSupportedStereoModes(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_addPowerModeListener(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_removePowerModeListener(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_isDisplayConnected(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_addDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_removeDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_Resolutions(IN const Json::Value& req, OUT Json::Value& response);
		void VOPTYPE_enableHDCP(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_getHDCPStatus(IN const Json::Value& req, OUT Json::Value& response);
		void VOPTYPE_isDynamicResolutionSupported(IN const Json::Value& req, OUT Json::Value& response);
		void VOPTYPE_isHDCPSupported(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_getDisplayDetails(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_isContentProtected(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_setEnable(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getCPUTemperature(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_setVersion(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_setPreferredSleepMode(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getPreferredSleepMode(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getAvailableSleepModes(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getVideoOutputPorts(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getAudioOutputPorts(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getVideoDevices(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getVideoOutputPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getVideoOutputPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getAudioOutputPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getAudioOutputPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		void HOST_getHostEDID(IN const Json::Value& req, OUT Json::Value& response);
		void FPI_getBrightnessLevels(IN const Json::Value& req, OUT Json::Value& response);
		void FPI_getColorMode(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_getTextColorMode(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_getTextBrightnessLevels(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_setTextBrightness(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_getTextBrightness(IN const Json::Value& req, OUT Json::Value& response);
		void FPTEXT_enableDisplay(IN const Json::Value& req, OUT Json::Value& response);
		void FPCONFIG_getIndicatorFromName(IN const Json::Value& req, OUT Json::Value& response);
		void FPCONFIG_getIndicatorFromId(IN const Json::Value& req, OUT Json::Value& response);
		void FPCONFIG_getTextDisplayFromName(IN const Json::Value& req, OUT Json::Value& response);
		void FPCONFIG_getTextDisplayFromId(IN const Json::Value& req, OUT Json::Value& response);
		void FPCONFIG_getColors(IN const Json::Value& req, OUT Json::Value& response);
		void AOPCONFIG_getPortType(IN const Json::Value& req, OUT Json::Value& response);
		void AOPCONFIG_getPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		void AOPCONFIG_getPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		void AOPCONFIG_getPorts(IN const Json::Value& req, OUT Json::Value& response);
		void AOPCONFIG_getSupportedTypes(IN const Json::Value& req, OUT Json::Value& response);
		void AOPCONFIG_release(IN const Json::Value& req, OUT Json::Value& response);
		void AOPCONFIG_load(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_setStereoAuto(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_getStereoAuto(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_getGain(IN const Json::Value& req, OUT Json::Value& response);
		void AOP_getOptimalLevel(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_getDefaultResolution(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_isActive(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_setDisplayConnected(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_hasSurround(IN const Json::Value& req, OUT Json::Value& response);
		void VOP_getEDIDBytes(IN const Json::Value& req, OUT Json::Value& response);
		void VOPTYPE_getSupportedResolutions(IN const Json::Value& req, OUT Json::Value& response);
		void VOPTYPE_getPorts(IN const Json::Value& req, OUT Json::Value& response);
		void VOPTYPE_setRestrictedResolution(IN const Json::Value& req, OUT Json::Value& response);
		void VOPTYPE_getRestrictedResolution(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getPixelResolution(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getSSMode(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getVideoResolution(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getFrameRate(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getPortType(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		void VOPCONFIG_getSupportedTypes(IN const Json::Value& req, OUT Json::Value& response);
		void VD_setPlatformDFC(IN const Json::Value& req, OUT Json::Value& response);
		void VD_getSupportedDFCs(IN const Json::Value& req, OUT Json::Value& response);
		void VD_getHDRCapabilities(IN const Json::Value& req, OUT Json::Value& response);
		void VDCONFIG_getDevices(IN const Json::Value& req, OUT Json::Value& response);
                void VDCONFIG_getDFCs(IN const Json::Value& req, OUT Json::Value& response);
                void VDCONFIG_getDefaultDFC(IN const Json::Value& req, OUT Json::Value& response);
                void VR_isInterlaced(IN const Json::Value& req, OUT Json::Value& response);
                void VOP_getAspectRatio(IN const Json::Value& req, OUT Json::Value& response);

                bool cleanup(IN const char* szVersion);

                /*DeviceSettingsAgent Wrapper functions*/
};
#endif //__DEVICESETTINGS_AGENT_H__

