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
/***************************************************************************
 *Function name : MocaHal_GetSoftwareVersion
 *Description    : This function is to get the software version of moca driver
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetSoftwareVersion(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSoftwareVersion --->Entry\n");
    char swVersion[16] = {'\0'};
    int returnStatus = SoC_IMPL__RMH_Self_GetSoftwareVersion(rmh,swVersion,sizeof(swVersion));
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = swVersion;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetSoftwareVersion call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSoftwareVersion -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetSoftwareVersion call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSoftwareVersion -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetSupportedBand
 *Description    : This function is to get the supported band
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetSupportedBand(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedBand --->Entry\n");
    char supportedBand[8]= {'\0'};
    RMH_Band band ;
    int returnStatus = SoC_IMPL__RMH_Self_GetSupportedBand(rmh,&band);
    if(!returnStatus)
    {
        sprintf(supportedBand,"%x",band);
        response["result"] = "SUCCESS";
        response["details"] = supportedBand;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetSupportedBand call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedBand -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GettSupportedBand call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSupportedBand -->Exit\n");
        return ;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetMaxBitrate
 *Description    : This function is to get the mocahal max bit rate
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMaxBitRate(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxBitRate --->Entry\n");
   unsigned int bitRate;
   int returnStatus = SoC_IMPL__RMH_Self_GetMaxBitrate(rmh,&bitRate);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = bitRate;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMaxBitRate call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxBitRate -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMaxBitRate call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxBitRate -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetNodeId
 *Description    : This function is to get the node Id of the device
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetNodeId(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNodeId --->Entry\n");
   unsigned int nodeId;
   int returnStatus = SoC_IMPL__RMH_Network_GetNodeId(rmh,&nodeId);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = nodeId;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetNodeId call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNodeId -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetNodeId call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNodeId -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetLinkUptime
 *Description    : This function is to get the amount of time the node has been part of the MoCA network 
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetLinkUptime(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLinkUptime --->Entry\n");
   unsigned int upTime;
   int returnStatus = SoC_IMPL__RMH_Network_GetLinkUptime(rmh,&upTime);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = upTime;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetLinkUptime call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLinkUptime -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetLinkUptime call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLinkUptime -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetTxBroadcastPhyRate
 *Description    : This function is to get the PHY rate at which broadcast packets are transmitted from the node
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetTxBroadcastPhyRate(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxBroadcastPhyRate --->Entry\n");
   unsigned int phyRate;
   int returnStatus = SoC_IMPL__RMH_Network_GetTxBroadcastPhyRate(rmh,&phyRate);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = phyRate;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetTxBroadcastPhyRate call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxBroadcastPhyRate -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetTxBroadcastPhyRate call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxBroadcastPhyRate -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetTxPowerLimit
 *Description    : This function is to get the maximum transmitter power level for the device 
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetTxPowerLimit(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxPowerLimit --->Entry\n");
   int powerLevel;
   int returnStatus = SoC_IMPL__RMH_Self_GetTxPowerLimit(rmh,&powerLevel);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = powerLevel;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetTxPowerLimit call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxPowerLimit -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetTxPowerLimit call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxPowerLimit -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_SetLOF
 *Description    : This function is to set the last operating frequency of the device.
 *****************************************************************************/
void MocaHalAgent::MocaHal_SetLOF(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetLOF --->Entry\n");
    unsigned int freq = req["freq"].asInt();
    int returnStatus = SoC_IMPL__RMH_Self_SetLOF(rmh,freq);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetLOF call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetLOF -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetLOF call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetLOF -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_SetPreferredNCEnabled
 *Description    : This function is to set the device preferred NC enabled/disabled
 *****************************************************************************/
void MocaHalAgent::MocaHal_SetPreferredNCEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetPreferredNCEnabled --->Entry\n");
    bool val = req["enable"].asInt();
    int returnStatus = SoC_IMPL__RMH_Self_SetPreferredNCEnabled(rmh,val);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetPreferredNCEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetPreferredNCEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetPreferredNCEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetPreferredNCEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetPreferredNCEnabled
 *Description    : This function is to check if the device is preferred NC enabled
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetPreferredNCEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPreferredNCEnabled --->Entry\n");
    bool status;
    int returnStatus = SoC_IMPL__RMH_Self_GetPreferredNCEnabled(rmh,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = status;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetPreferredNCEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPreferredNCEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetPreferredNCEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPreferredNCEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetMaxPacketAggregation
 *Description    : This function is to get the maximum number of packets the device will aggregate.
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMaxPacketAggregation(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxPacketAggregation --->Entry\n");
   unsigned int val;
   int returnStatus = SoC_IMPL__RMH_Self_GetMaxPacketAggregation(rmh,&val);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = val;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMaxPacketAggregation call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxPacketAggregation -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMaxPacketAggregation call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxPacketAggregation -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetMaxFrameSize
 *Description    : This function is to get the maximum number of bytes the node can receive.
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMaxFrameSize(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxFrameSize --->Entry\n");
   unsigned int val;
   int returnStatus = SoC_IMPL__RMH_Self_GetMaxFrameSize(rmh,&val);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = val;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMaxFrameSize call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxFrameSize -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMaxFrameSize call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMaxFrameSize -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_GetLowBandwidthLimit
 *Description    : This function is to get the lower threshold for the PHY link bandwidth
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetLowBandwidthLimit(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLowBandwidthLimit --->Entry\n");
   unsigned int val;
   int returnStatus = SoC_IMPL__RMH_Self_GetLowBandwidthLimit(rmh,&val);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = val;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetLowBandwidthLimit call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLowBandwidthLimit -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetLowBandwidthLimit call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLowBandwidthLimit -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_SetTurboEnabled
 *Description    : This function is used to Enable or disable turbo mode on the device
 *****************************************************************************/
void MocaHalAgent::MocaHal_SetTurboEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetTurboEnabled --->Entry\n");
    bool val = req["enable"].asInt();
    int returnStatus = SoC_IMPL__RMH_Self_SetTurboEnabled(rmh,val);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetTurboEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetTurboEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_SetTurboEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_SetTurboEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetTurboEnabled
 *Description    : This function is to check if turbo mode is enabled/disabled
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetTurboEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTurboEnabled --->Entry\n");
    bool status;
    int returnStatus = SoC_IMPL__RMH_Self_GetTurboEnabled(rmh,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = status;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetTurboEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTurboEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetTurboEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTurboEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetPrivacyEnabled
 *Description    : This function is to check if privacy is enabled/disabled for the device
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetPrivacyEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPrivacyEnabled --->Entry\n");
    bool status;
    int returnStatus = SoC_IMPL__RMH_Self_GetPrivacyEnabled(rmh,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = status;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetPrivacyEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPrivacyEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetPrivacyEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPrivacyEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetTxPowerControlEnabled
 *Description    : This function is to check if transmit power control is enabled or disabled for the device.
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetTxPowerControlEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxPowerControlEnabled --->Entry\n");
    bool status;
    int returnStatus = SoC_IMPL__RMH_Power_GetTxPowerControlEnabled(rmh,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = status;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetTxPowerControlEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxPowerControlEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetTxPowerControlEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxPowerControlEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetTxBeaconPowerReductionEnabled
 *Description    : This function is to check if beacon power reduction is enabled on the device..
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetTxBeaconPowerReductionEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxBeaconPowerReductionEnabled --->Entry\n");
    bool status;
    int returnStatus = SoC_IMPL__RMH_Power_GetTxBeaconPowerReductionEnabled(rmh,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = status;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetTxBeaconPowerReductionEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxBeaconPowerReductionEnabled -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetTxBeaconPowerReductionEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxBeaconPowerReductionEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetNCNodeId
 *Description    : This function is to get the node Id of the network coordinator
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetNCNodeId(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNCNodeId --->Entry\n");
   unsigned int nodeId;
   int returnStatus = SoC_IMPL__RMH_Network_GetNCNodeId(rmh,&nodeId);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = nodeId;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetNCNodeId call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNCNodeId -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetNCNodeId call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNCNodeId -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetBackupNCNodeId
 *Description    : This function is to get the node Id of the backup network coordinator
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetBackupNCNodeId(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetBackupNCNodeId--->Entry\n");
   unsigned int nodeId;
   int returnStatus = SoC_IMPL__RMH_Network_GetBackupNCNodeId(rmh,&nodeId);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = nodeId;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetBackupNCNodeId call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetBackupNCNodeId -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetBackupNCNodeId call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetBackupNCNodeId -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetMixedMode
 *Description    : This function is to check if the MoCA network contains both 1.1 and 2.0 nodes.
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetMixedMode(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMixedMode --->Entry\n");
    bool status;
    int returnStatus = SoC_IMPL__RMH_Network_GetMixedMode(rmh,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = status;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetMixedMode call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMixedMode -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetMixedMode call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetMixedMode -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetNetworkNodeIds
 *Description    : This function is to return the list of node ids in the network
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetNetworkNodeIds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNetworkNodeIds --->Entry\n");
    std::string nodeIdList;
    RMH_NodeList_Uint32_t nodeList ;
    uint32_t nodeId;
    int returnStatus = SoC_IMPL__RMH_Network_GetNodeIds(rmh,&nodeList);
    if(!returnStatus)
    {
        for (nodeId = 0; nodeId < RMH_MAX_MOCA_NODES; nodeId++) {
            if (nodeList.nodePresent[nodeId]) {
                nodeIdList = nodeIdList + to_string(nodeList.nodeValue[nodeId]) + ",";
            }
        }
        response["result"] = "SUCCESS";
        response["details"] = nodeIdList;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetNetworkNodeIds call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNetworkNodeIds -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetNetworkNodeIds call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNetworkNodeIds -->Exit\n");
        return ;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetRemoteNodeIds
 *Description    : This function is to return the list of node ids in the network except self node id
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetRemoteNodeIds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetRemoteNodeIds --->Entry\n");
    std::string rmNodeIdList;
    RMH_NodeList_Uint32_t remoteNodeList;
    uint32_t nodeId;
    int returnStatus = SoC_IMPL__RMH_Network_GetRemoteNodeIds(rmh,&remoteNodeList);
    if(!returnStatus)
    {
        for (nodeId = 0; nodeId < RMH_MAX_MOCA_NODES; nodeId++) {
            if (remoteNodeList.nodePresent[nodeId]) {
                rmNodeIdList = rmNodeIdList + to_string(remoteNodeList.nodeValue[nodeId]) + ",";
            }
        }

        response["result"] = "SUCCESS";
        response["details"] = rmNodeIdList;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetRemoteNodeIds call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetRemoteNodeIds -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetRemoteNodeIds call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetRemoteNodeIds -->Exit\n");
        return ;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetNCMac
 *Description    : This function is to get the Mac address of the network coordinator.
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetNCMac(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNCMac --->Entry\n");
    char ncMacAddress[24]= {'\0'};
    RMH_MacAddress_t ncmac ;
    int returnStatus = SoC_IMPL__RMH_Network_GetNCMac(rmh,&ncmac);
    if(!returnStatus)
    {
        sprintf(ncMacAddress,"%s",RMH_MacToString(ncmac,ncMacAddress, sizeof(ncMacAddress)));
        response["result"] = "SUCCESS";
        response["details"] = ncMacAddress;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetNCMac call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNCMac -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetNCMac call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetNCMac -->Exit\n");
        return ;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetTxMapPhyRate
 *Description    : This function is to get the PHY rate at which MAP packets are transmitted from the node
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetTxMapPhyRate(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxMapPhyRate --->Entry\n");
   unsigned int mapPhyRate;
   int returnStatus = SoC_IMPL__RMH_Network_GetTxMapPhyRate(rmh,&mapPhyRate);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = mapPhyRate;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetTxMapPhyRate call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxMapPhyRate -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetTxMapPhyRate call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxMapPhyRate -->Exit\n");
        return;
    } 
}
/***************************************************************************
 *Function name : MocaHal_RemoteNode_GetMac
 *Description    : This function is to get the mac address of the remote node
 *****************************************************************************/
void MocaHalAgent::MocaHal_RemoteNode_GetMac(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetMac --->Entry\n");
    unsigned int nodeId = req["nodeId"].asInt();
    char macAddress[24]= {'\0'};
    RMH_MacAddress_t macAddr;
    int returnStatus = SoC_IMPL__RMH_RemoteNode_GetMac(rmh,nodeId,&macAddr);
    if(!returnStatus)
    {
        sprintf(macAddress,"%s",RMH_MacToString(macAddr, macAddress, sizeof(macAddress)));
        response["result"] = "SUCCESS";
        response["details"] = macAddress;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_RemoteNode_GetMac call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetMac -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_RemoteNode_GetMac call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetMac -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_RemoteNode_GetPreferredNC
 *Description    : This function is to check if the node indicated by nodeId is a preferred NC or not.
 *****************************************************************************/
void MocaHalAgent::MocaHal_RemoteNode_GetPreferredNC(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetPreferredNC --->Entry\n");
    bool status;
    unsigned int nodeId = req["nodeId"].asInt();
    int returnStatus = SoC_IMPL__RMH_RemoteNode_GetPreferredNC(rmh,nodeId,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = status;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_RemoteNode_GetPreferredNC call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetPreferredNC -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_RemoteNode_GetPreferredNC call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetPreferredNC -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetLinkDownCount
 *Description    : This function is to get the number of times the MoCA link has gone down since the last boot
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetLinkDownCount(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLinkDownCount --->Entry\n");
   unsigned int linkDownCount;
   int returnStatus = SoC_IMPL__RMH_Network_GetLinkDownCount(rmh,&linkDownCount);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = linkDownCount;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetLinkDownCount call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLinkDownCount -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetLinkDownCount call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetLinkDownCount -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetResetCount
 *Description    : This function is to get the number of times the MoCA link got reset
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetResetCount(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetResetCount --->Entry\n");
   unsigned int resetCount;
   int returnStatus = SoC_IMPL__RMH_Network_GetResetCount(rmh,&resetCount);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = resetCount;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetResetCount call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetResetCount -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetResetCount call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetResetCount -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetTxGCDPhyRate
 *Description    : This function is to get the GCD PHY rate at packets are transmitted from the node
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetTxGCDPhyRate(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxGCDPhyRate --->Entry\n");
   unsigned int gcdPhyRate;
   int returnStatus = SoC_IMPL__RMH_Network_GetTxGCDPhyRate(rmh,&gcdPhyRate);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = gcdPhyRate;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetTxGCDPhyRate call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxGCDPhyRate -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetTxGCDPhyRate call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetTxGCDPhyRate -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetRFChannelFreq
 *Description    : This function is to get the frequency which the MoCA network is operating on 
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetRFChannelFreq(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetRFChannelFreq --->Entry\n");
   unsigned int rfChannelFreq;
   int returnStatus = SoC_IMPL__RMH_Network_GetRFChannelFreq(rmh,&rfChannelFreq);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = rfChannelFreq;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetRFChannelFreq call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetRFChannelFreq -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetRFChannelFreq call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetRFChannelFreq -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetPrimaryChannelFreq
 *Description    : This function is to get the primary channel frequency
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetPrimaryChannelFreq(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPrimaryChannelFreq --->Entry\n");
   unsigned int primaryChannelFreq;
   int returnStatus = SoC_IMPL__RMH_Network_GetPrimaryChannelFreq(rmh,&primaryChannelFreq);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = primaryChannelFreq;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetPrimaryChannelFreq call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPrimaryChannelFreq -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetPrimaryChannelFreq call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetPrimaryChannelFreq -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_GetSecondaryChannelFreq
 *Description    : This function is to get the secondary channel frequency
 *****************************************************************************/
void MocaHalAgent::MocaHal_GetSecondaryChannelFreq(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSecondaryChannelFreq --->Entry\n");
   unsigned int secondaryChannelFreq;
   int returnStatus = SoC_IMPL__RMH_Network_GetSecondaryChannelFreq(rmh,&secondaryChannelFreq);
   if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = secondaryChannelFreq;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_GetSecondaryChannelFreq call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSecondaryChannelFreq -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MocaHal_GetSecondaryChannelFreq call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_GetSecondaryChannelFreq -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : MocaHal_RemoteNode_GetActiveMoCAVersion
 *Description    : This function is to get active supported version of MoCA by the remote node specificed by nodeId
 *****************************************************************************/
void MocaHalAgent::MocaHal_RemoteNode_GetActiveMoCAVersion(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetActiveMoCAVersion --->Entry\n");
    unsigned int nodeId = req["nodeId"].asInt();
    char activeVersion[8]= {'\0'};
    RMH_MoCAVersion version;
    int returnStatus = SoC_IMPL__RMH_RemoteNode_GetActiveMoCAVersion(rmh,nodeId,&version);
    if(!returnStatus)
    {
        sprintf(activeVersion,"%x",version);
        response["result"] = "SUCCESS";
        response["details"] = activeVersion;
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_RemoteNode_GetActiveMoCAVersion call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetActiveMoCAVersion -->Exit\n");
        return ;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_LOG, "MocaHal_RemoteNode_GetActiveMoCAVersion call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MocaHal_RemoteNode_GetActiveMoCAVersion -->Exit\n");
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
