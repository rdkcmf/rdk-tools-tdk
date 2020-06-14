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

#include "PowerMgrHalAgent.h"
std::chrono::time_point<std::chrono::high_resolution_clock> start;
std::chrono::time_point<std::chrono::high_resolution_clock> stop;
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string PowerMgrHalAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal testmodule pre_requisites --> Entry\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgr init ....\n");
    int init = PLAT_INIT();
    if (init == 0){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_INIT call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_INIT call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool PowerMgrHalAgent::testmodulepost_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal testmodule post_requisites --> Entry\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgr term ...\n");
    PLAT_TERM();
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal testmodule post_requisites --> Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name   : CreateObject
Arguments       : NULL
Description     : This function is used to create a new object of the class "DSHalAgent".
**************************************************************************/
extern "C" PowerMgrHalAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new PowerMgrHalAgent(ptrtcpServer);
}

/***************************************************************************
 *Function name : initialize
 *Description    : Initialize Function will be used for registering the wrapper method
 *                with the agent so that wrapper functions will be used in the
 *                script
 *****************************************************************************/
bool PowerMgrHalAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT (DEBUG_TRACE, "PowerMgrHal Initialization Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "PowerMgrHal Initialization Exit\n");
    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name  : PowerMgrHal_GetPowerState
 *Description    : This function is to invoke PLAT_API_GetPowerState
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_GetPowerState(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetPowerState --->Entry\n");
    char details[50];
    string pwr_state;

    IARM_Bus_PWRMgr_PowerState_t state;
    int ret = PLAT_API_GetPowerState(&state);
    if (ret == 0){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetPowerState call success\n");
        if (state == IARM_BUS_PWRMGR_POWERSTATE_OFF)
            pwr_state = "OFF";
        else if (state == IARM_BUS_PWRMGR_POWERSTATE_STANDBY)
            pwr_state = "STANDBY";
        else if (state == IARM_BUS_PWRMGR_POWERSTATE_ON)
            pwr_state = "ON";
        else if (state == IARM_BUS_PWRMGR_POWERSTATE_STANDBY_LIGHT_SLEEP)
            pwr_state = "LIGHT_SLEEP";
        else if (state == IARM_BUS_PWRMGR_POWERSTATE_STANDBY_DEEP_SLEEP)
            pwr_state = "DEEP_SLEEP";
        else
            pwr_state = "NONE";

        DEBUG_PRINT(DEBUG_TRACE, "Power State:%s\n",pwr_state.c_str());
        sprintf(details, "Power State:%s",pwr_state.c_str());

        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetPowerState --> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="PLAT_API_GetPowerState call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetPowerState call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetPowerState --> Exit\n");
    }
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_SetPowerState
 *Description    : This function is to invoke PLAT_API_SetPowerState
                   This function just updates the global variable with the
                   state set but not the device state as far as brcm is 
                   concerned
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_SetPowerState(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetPowerState --->Entry\n");
    if(&req["state"] == NULL )
    {
        response["result"]="FAILURE";
        response["details"]="No Input State";
        return;
    }
    char pwr_state[20];
    strcpy(pwr_state,req["state"].asCString());

    IARM_Bus_PWRMgr_PowerState_t state;
    if (!strcmp(pwr_state,"OFF"))
        state = IARM_BUS_PWRMGR_POWERSTATE_OFF;
    else if (!strcmp(pwr_state,"STANDBY"))
        state = IARM_BUS_PWRMGR_POWERSTATE_STANDBY;
    else if (!strcmp(pwr_state,"ON"))
        state = IARM_BUS_PWRMGR_POWERSTATE_ON;
    else if (!strcmp(pwr_state,"LIGHT_SLEEP"))
        state = IARM_BUS_PWRMGR_POWERSTATE_STANDBY_LIGHT_SLEEP;
    else if (!strcmp(pwr_state,"DEEP_SLEEP"))
        state = IARM_BUS_PWRMGR_POWERSTATE_STANDBY_DEEP_SLEEP;
    else{
        response["result"] = "FAILURE";
        response["details"] = "Invalid Power State";
        return;
    }
    DEBUG_PRINT(DEBUG_TRACE, "Power State to be set:%s\n",pwr_state);

    int ret = PLAT_API_SetPowerState(state);
    if (ret == 0){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_SetPowerState call success\n");
        response["result"]="SUCCESS";
        response["details"]="PLAT_API_SetPowerState call success";
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetPowerState --> Exit\n");
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_SetPowerState call failed\n");
        response["result"]="FAILURE";
        response["details"]="PLAT_API_SetPowerState call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetPowerState --> Exit\n");
    }
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_GetTemperature
 *Description    : This function is to invoke PLAT_API_GetTemperature
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_GetTemperature(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTemperature --->Entry\n");
#ifdef ENABLE_THERMAL_PROTECTION
    char details[100];
    string temp_state;

    IARM_Bus_PWRMgr_ThermalState_t state;
    float current_Temp = 0;
    float current_WifiTemp = 0;
    int ret = PLAT_API_GetTemperature(&state, &current_Temp, &current_WifiTemp);
    if (ret == 1){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetTemperature call success\n");
        if ( state == IARM_BUS_PWRMGR_TEMPERATURE_NORMAL )
            temp_state = "NORMAL";
        else if (state == IARM_BUS_PWRMGR_TEMPERATURE_HIGH)
            temp_state = "HIGH";
        else if (state == IARM_BUS_PWRMGR_TEMPERATURE_CRITICAL )
            temp_state = "CRITICAL";
        else
            temp_state = "NONE";

        DEBUG_PRINT(DEBUG_TRACE, "Current_Temp=%f, Wifi_Temp=%f, State=%s\n",current_Temp,current_WifiTemp,temp_state.c_str());
        sprintf(details,"Current_Temp=%f, Wifi_Temp=%f, State=%s",current_Temp,current_WifiTemp,temp_state.c_str());
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTemperature ---> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="PLAT_API_GetTemperature call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetTemperature call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTemperature --> Exit\n");
    }
#else
    response["result"]="FAILURE";
    response["details"]="Thermal Protection Not Supported";
    DEBUG_PRINT(DEBUG_TRACE, "Thermal Protection Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTemperature ---> Exit\n");
#endif
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_GetTempThresholds
 *Description    : This function is to invoke PLAT_API_GetTempThresholds
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_GetTempThresholds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTempThresholds --->Entry\n");
#ifdef ENABLE_THERMAL_PROTECTION
    char details[100];

    float high, critical;
    int ret = PLAT_API_GetTempThresholds(&high,&critical);
    if (ret == 1){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetTempThresholds call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "Thermal threshold : high=%f, critical=%f\n",high,critical);
        sprintf(details,"Thermal threshold : high=%f, critical=%f",high,critical);
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTempThresholds ---> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="PLAT_API_GetTempThresholds call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetTempThresholds call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTempThresholds ---> Exit\n");
    }
#else
    response["result"]="FAILURE";
    response["details"]="Thermal Protection Not Supported";
    DEBUG_PRINT(DEBUG_TRACE, "Thermal Protection Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetTempThresholds ---> Exit\n");
#endif
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_SetTempThresholds
 *Description    : This function is to invoke PLAT_API_SetTempThresholds
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_SetTempThresholds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetTempThresholds --->Entry\n");
    if(&req["high"] == NULL || &req["critical"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Temp Thresholds";
        return;
    }
#ifdef ENABLE_THERMAL_PROTECTION
    float high, critical;
    high = (float) req["high"].asInt();
    critical = (float) req["critical"].asInt();

    int ret = PLAT_API_SetTempThresholds(high,critical);
    if (ret == 1){
        response["result"]="SUCCESS";
        response["details"]="PLAT_API_SetTempThresholds call success";
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_SetTempThresholds call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetTempThresholds ---> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="PLAT_API_SetTempThresholds call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_SetTempThresholds call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetTempThresholds ---> Exit\n");
    }
#else
    response["result"]="FAILURE";
    response["details"]="Thermal Protection Not Supported";
    DEBUG_PRINT(DEBUG_TRACE, "Thermal Protection Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetTempThresholds ---> Exit\n");
#endif
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_DetemineClockSpeeds
 *Description    : This function is to invoke PLAT_API_DetemineClockSpeeds
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_DetemineClockSpeeds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_DetemineClockSpeeds --->Entry\n");
#ifdef ENABLE_THERMAL_PROTECTION
    char details[200];

    uint32_t PLAT_CPU_SPEED_NORMAL = 0;
    uint32_t PLAT_CPU_SPEED_SCALED = 0;
    uint32_t PLAT_CPU_SPEED_MINIMAL = 0;
    int ret = PLAT_API_DetemineClockSpeeds(&PLAT_CPU_SPEED_NORMAL,&PLAT_CPU_SPEED_SCALED,&PLAT_CPU_SPEED_MINIMAL);
    if (ret == 1){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_DetemineClockSpeeds call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "CPU_SPEED_NORMAL=%d, CPU_SPEED_SCALED=%d, CPU_SPEED_MINIMAL=%d\n",PLAT_CPU_SPEED_NORMAL,PLAT_CPU_SPEED_SCALED,PLAT_CPU_SPEED_MINIMAL);
        sprintf(details,"CPU_SPEED_NORMAL=%d, CPU_SPEED_SCALED=%d, CPU_SPEED_MINIMAL=%d",PLAT_CPU_SPEED_NORMAL,PLAT_CPU_SPEED_SCALED,PLAT_CPU_SPEED_MINIMAL);
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_DetemineClockSpeeds ---> Exit\n");
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_DetemineClockSpeeds call failed\n");
        response["result"]="FAILURE";
        response["details"]="PLAT_API_DetemineClockSpeeds call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_DetemineClockSpeeds ---> Exit\n");
    }
#else
    response["result"]="FAILURE";
    response["details"]="Thermal Protection Not Supported";
    DEBUG_PRINT(DEBUG_TRACE, "Thermal Protection Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_DetemineClockSpeeds ---> Exit\n");
#endif
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_GetClockSpeed
 *Description    : This function is to invoke PLAT_API_GetClockSpeed
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_GetClockSpeed(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetClockSpeed --->Entry\n");
#ifdef ENABLE_THERMAL_PROTECTION
    char details[50];

    uint32_t cur_Cpu_Speed = 0;
    int ret = PLAT_API_GetClockSpeed(&cur_Cpu_Speed);
    if (ret == 1){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetClockSpeed call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "Default Frequency=%d\n",cur_Cpu_Speed);
        sprintf(details,"Default Frequency=%d",cur_Cpu_Speed);
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetClockSpeed ---> Exit\n");
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_GetClockSpeed call failed\n");
        response["result"]="FAILURE";
        response["details"]="PLAT_API_GetClockSpeed call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetClockSpeed ---> Exit\n");
    }
#else
    response["result"]="FAILURE";
    response["details"]="Thermal Protection Not Supported";
    DEBUG_PRINT(DEBUG_TRACE, "Thermal Protection Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetClockSpeed ---> Exit\n");
#endif
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_SetClockSpeed
 *Description    : This function is to invoke PLAT_API_SetClockSpeed
                   It is applicable for ARM platform only. Not supposed to
                   try in MIPS Platforms.
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_SetClockSpeed(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetClockSpeed --->Entry\n");
    if(&req["speed"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Clock Speed";
        return;
    }
#ifdef ENABLE_THERMAL_PROTECTION
    uint32_t speed;
    speed = (uint32_t) req["speed"].asInt();

    int ret = PLAT_API_SetClockSpeed(speed);
    if (ret == 1){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_SetClockSpeed call success\n");
        response["result"]="SUCCESS";
        response["details"]="PLAT_API_SetClockSpeed call success";
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetClockSpeed ---> Exit\n");
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_API_SetClockSpeed call failed\n");
        response["result"]="FAILURE";
        response["details"]="PLAT_API_SetClockSpeed call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetClockSpeed ---> Exit\n");
    }
#else
    response["result"]="FAILURE";
    response["details"]="Thermal Protection Not Supported";
    DEBUG_PRINT(DEBUG_TRACE, "Thermal Protection Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_SetClockSpeed ---> Exit\n");
#endif
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_GetCmdTimeTaken
 *Description    : This function is to get the time taken for executing the
                   input cmd in nano seconds. This function does not invoke
                   any HAL API
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_GetCmdTimeTaken(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetCmdTimeTaken --->Entry\n");
    if(&req["cmd"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Command";
        return;
    }
    char *command = (char*)req["cmd"].asCString();
    char details[100];

    DEBUG_PRINT(DEBUG_TRACE, "Going to execute the cmd : %s",command);
    start = std::chrono::high_resolution_clock::now();
    int ret = system(command);
    stop = std::chrono::high_resolution_clock::now();
    int timeTaken = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count();
    if (ret == 0){
        DEBUG_PRINT(DEBUG_TRACE, "Command execution using system call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "Time Taken for %s cmd : %d (nano seconds)\n",command,timeTaken);
        sprintf(details,"Time Taken for %s cmd : %d (nano seconds)",command,timeTaken);
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetCmdTimeTaken ---> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="Command execution using system call failed";
        DEBUG_PRINT(DEBUG_TRACE, "Command execution failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_GetCmdTimeTaken ---> Exit\n");
    }
    return;
}

/***************************************************************************
 *Function name  : PowerMgrHal_Reset
 *Description    : This function is to invoke PLAT_Reset. This function
                   reboots the device by invoking rebootNow script
 *****************************************************************************/
void PowerMgrHalAgent::PowerMgrHal_Reset(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_Reset --->Entry\n");
    //input paramter is not in use
    IARM_Bus_PWRMgr_PowerState_t state = IARM_BUS_PWRMGR_POWERSTATE_ON;
    DEBUG_PRINT(DEBUG_TRACE, "Calling PLAT_Reset : going to reboot the device\n");
    PLAT_Reset(state);
    response["result"]="SUCCESS";
    response["details"]="PLAT_Reset call success";
    DEBUG_PRINT(DEBUG_TRACE, "PowerMgrHal_Reset ---> Exit\n");
    return;
}

/**************************************************************************
Function Name   : cleanup
Arguments       : NULL
Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool PowerMgrHalAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject
Arguments     : Input argument is PowerMgrHalAgent Object
Description   : This function will be used to destory the DSHalAgent object.
**************************************************************************/
extern "C" void DestroyObject(PowerMgrHalAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying PowerMgrHal Agent object\n");
        delete stubobj;
}
