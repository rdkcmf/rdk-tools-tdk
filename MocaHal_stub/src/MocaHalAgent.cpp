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

#include "MocaHalAgent.h"
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                1.
 *****************************************************************************/

std::string MocaHalAgent::testmodulepre_requisites() 
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal testmodule pre_requisites --> Entry\n");
    rmh=RMH_Initialize(NULL, NULL);
    if (rmh)
    {
        DEBUG_PRINT(DEBUG_LOG, "MocaHal handle initialize success\n");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal handle initialize failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
   
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool MocaHalAgent::testmodulepost_requisites()
{
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal testmodule post_requisites --> Entry\n");
        int returnStatus;
        returnStatus = SoC_IMPL__RMH_Destroy(rmh);
        if (!returnStatus)
        {
            DEBUG_PRINT(DEBUG_LOG, "MocaHal handle destroyed successfully\n");
            DEBUG_PRINT(DEBUG_TRACE, "MocaHal testmodule post_requisites --> Exit\n");
            return true;
        }
        else
        {
           DEBUG_PRINT(DEBUG_ERROR, "MocaHal handle NOT destroyed\n");
           DEBUG_PRINT(DEBUG_TRACE, "MocaHal testmodule post_requisites --> Exit\n");
           return false;
        }
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "MocaHalAgent".
**************************************************************************/

extern "C" MocaHalAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new MocaHalAgent(ptrtcpServer);
}

/***************************************************************************
 *Function name : initialize
 *Description    : Initialize Function will be used for registering the wrapper method
 *                with the agent so that wrapper functions will be used in the
 *                script
 *****************************************************************************/

bool MocaHalAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT (DEBUG_TRACE, "MocaHal Initialization Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "MocaHal Initialization Exit\n");
    return TEST_SUCCESS;
}
/***************************************************************************
 *Function name : MocaHal_GetMoCALinkUp
 *Description    : This function is to get the mocahal uplink status
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMoCALinkUp(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMoCALinkUp --->Entry\n");
    bool output ;
    int returnStatus;
    returnStatus = SoC_IMPL__RMH_Self_GetMoCALinkUp(rmh,&output);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = output;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMoCALinkUp call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMoCALinkUp -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMoCALinkUp call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMoCALinkUp -->Exit\n");
        return;
    }

}
/***************************************************************************
 *Function name : MocaHal_SetEnabled
 *Description    : This function is to set the mocahal enabled or disabled
 *****************************************************************************/
void MocaHalAgent::MocaHal_SetEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetEnabled --->Entry\n");
    bool input = req["enable"].asInt();
    int returnStatus = SoC_IMPL__RMH_Self_SetEnabled(rmh,input);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetEnabled
 *Description    : This function is to get the mocahal enabled value
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetEnabled --->Entry\n");
    bool output;
    int returnStatus = SoC_IMPL__RMH_Self_GetEnabled(rmh,&output);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = output;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetEnabled -->Exit\n");
        return;
    }
    
}
/***************************************************************************
 *Function name : MocaHal_GetLOF
 *Description    : This function is to get the mocahal last operating frequency
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetLOF(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLOF --->Entry\n");
   unsigned int freq;
   int returnStatus = SoC_IMPL__RMH_Self_GetLOF(rmh,&freq);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = freq;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetLOF call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLOF -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetLOF call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLOF -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetFrequencyMask
 *Description    : This function is to get the mocahal frequency mask
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetFrequencyMask(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetFrequencyMask --->Entry\n");
    unsigned int mask;
    char freqmask[8]= {'\0'};
    int returnStatus = SoC_IMPL__RMH_Self_GetFrequencyMask(rmh,&mask);
    if(!returnStatus)
    {
        sprintf(freqmask,"%x",mask);
        response["result"] = "SUCCESS";
        response["details"] = freqmask;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetFrequencyMask call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetFrequencyMask -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetFrequencyMask call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetFrequencyMask -->Exit\n");
        return ;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetSupportedFrequencies
 *Description    : This function is to get the supported frequencies
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetSupportedFrequencies(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedFrequencies --->Entry\n");
    unsigned int freqArray[FREQUENCIES_BUFFER];
    unsigned int supportedArraySize;
    char freqArrayBuffer[SUPPORTED_FREQUENCIES_BUFFER] = {'\0'};
    char temp[FREQUENCIES_BUFFER] = {'\0'};
    char result[SUPPORTED_FREQUENCIES_BUFFER] = {'\0'};
    int returnStatus = SoC_IMPL__RMH_Self_GetSupportedFrequencies(rmh,freqArray,sizeof(freqArray),&supportedArraySize);

    if(!returnStatus)
    {
        int i;
        for(i=0; i<supportedArraySize; i++)
        {
            sprintf(temp,"%d",freqArray[i]);
            strcat(freqArrayBuffer,temp);
            strcat(freqArrayBuffer,",");
        }
        sprintf(result,"%s",freqArrayBuffer);
        response["result"] = "SUCCESS";
        response["details"] = result;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetSupportedFrequencies call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedFrequencies -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetSupportedFrequencies call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedFrequencies -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetHighestSupportedMoCAVersion
 *Description    : This function is to get the Highest Supported MoCAVersion
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetHighestSupportedMoCAVersion(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetHighestSupportedMoCAVersion --->Entry\n");    
    char highestVersion[8]= {'\0'};
    RMH_MoCAVersion version ;
    int returnStatus = SoC_IMPL__RMH_Self_GetHighestSupportedMoCAVersion(rmh,&version);
    if(!returnStatus)
    {
        sprintf(highestVersion,"%x",version);
        response["result"] = "SUCCESS";
        response["details"] = highestVersion;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetHighestSupportedMoCAVersion call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetHighestSupportedMoCAVersion -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetHighestSupportedMoCAVersion call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetHighestSupportedMoCAVersion -->Exit\n");
        return ;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetMac
 *Description    : This function is to get the Mac address
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMac(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMac --->Entry\n");
    char macAddress[24]= {'\0'};
    RMH_MacAddress_t mac ;
    int returnStatus = SoC_IMPL__RMH_Interface_GetMac(rmh,&mac);
    if(!returnStatus)
    {
        sprintf(macAddress,"%s",RMH_MacToString(mac,macAddress, sizeof(macAddress)));
        response["result"] = "SUCCESS";
        response["details"] = macAddress;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMac call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMac -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMac call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMac -->Exit\n");
        return ;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetName
 *Description    : This function is to get the interface name
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetName(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetName --->Entry\n");
    char iname [16] = {'\0'};
    int returnStatus = SoC_IMPL__RMH_Interface_GetName(rmh,iname,sizeof(iname));
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = iname;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetName call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetName -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetName call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetName -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetMoCAVersion
 *Description    : This function is to get the current moca version
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMoCAVersion(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMoCAVersion --->Entry\n");
    char currentVersion[8]= {'\0'};
    RMH_MoCAVersion version ;
    int returnStatus = SoC_IMPL__RMH_Network_GetMoCAVersion(rmh,&version);
    if(!returnStatus)
    {
        sprintf(currentVersion,"%x",version);
        response["result"] = "SUCCESS";
        response["details"] = currentVersion;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMoCAVersion call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMoCAVersion -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMoCAVersion call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMoCAVersion -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetNumNodes 
 *Description    : This function is to get the the number of nodes
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetNumNodes(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNumNodes --->Entry\n");
    unsigned int nodes;
    char numNodes[8]= {'\0'};
    int returnStatus = SoC_IMPL__RMH_Network_GetNumNodes(rmh,&nodes);
    if(!returnStatus)
    {
        sprintf(numNodes,"%x",nodes);
        response["result"] = "SUCCESS";
        response["details"] = numNodes;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetNumNodes call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNumNodes  -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetNumNodes call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNumNodes -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetSupportedModes
 *Description    : This function is to get the supported power modes
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetSupportedModes(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedModes --->Entry\n");
    unsigned int modes=0;
    char powerModes[8]= {'\0'};
    int returnStatus = SoC_IMPL__RMH_Power_GetSupportedModes(rmh,&modes);
    if(!returnStatus)
    {
        sprintf(powerModes,"%x",modes);
        response["result"] = "SUCCESS";
        response["details"] = powerModes;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetSupportedModes call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedModes  -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetSupportedModes call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedModes -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetMode
 *Description    : This function is to get the power mode
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMode(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMode --->Entry\n");
    RMH_PowerMode mode;
    char powerMode[8]= {'\0'};
    int returnStatus = SoC_IMPL__RMH_Power_GetMode(rmh,&mode);
    if(!returnStatus)
    {
        sprintf(powerMode,"%u",mode);
        response["result"] = "SUCCESS";
        response["details"] = powerMode;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMode call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMode  -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMode call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMode -->Exit\n");
        return;
    }
}
/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool MocaHalAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is MocaHalAgent Object

Description   : This function will be used to destory the MocaHalAgent object.
**************************************************************************/
extern "C" void DestroyObject(MocaHalAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying MocaHal Agent object\n");
        delete stubobj;
}
