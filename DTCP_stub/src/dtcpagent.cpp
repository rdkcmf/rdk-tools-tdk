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

#include "dtcpagent.h"
#include <list>
#include <sstream>
#include <exception>

#ifdef USE_SOC_INIT
void soc_uninit();
void soc_init(int, char *, int);
#endif

static list<DTCP_SESSION_HANDLE> srcSessionHandlerList;
static list<DTCP_SESSION_HANDLE> sinkSessionHandlerList;

bool dtcpProcessReleasePacket()
{
    bool status = true;
    int returnCode = DTCP_SUCCESS;
    DTCP_SESSION_HANDLE srcHandle;
    DTCP_SESSION_HANDLE sinkHandle;
    const int tsLength = 192;
    string testTSStream = "4c 18 5a 50 47 17 bc 13 3a 8d ba 2a 67 b0 26 ea b9 67 28 8f c8 31 b7 1a 59 77 76 f7 dc 5a 83 73 dd dd 69 9a 9e f4 28 2c 62 c9 ae c2 0e e8 07 97 9a 4b 1d 8a 83 29 b5 ee 75 28 31 d4 3a 5e 6b e6 71 4f ee 9a f7 76 ee 3d 0f a6 6b cf 00 97 00 00 18 01 88 2b 00 0a 5d c0 49 16 41 1a 4d 03 0a 19 48 ba 19 58 80 22 8a 85 43 22 14 f9 d3 07 53 d1 41 13 c4 93 71 e9 53 b7 7b 04 55 9e d0 d1 7c 1c 57 89 1e 71 c1 b6 9d 72 c1 78 c5 47 10 7e 94 40 7d 70 3b 15 71 3c 6e c0 94 01 d7 b8 86 ba ba a7 29 94 a8 c3 2f 9a 93 30 61 28 32 ed 03 3e 12 ad 0f b0 80 f4 53 96 d0 d5 31 6c 39 16 f4 e4 af f8"; // 192 bytes

    /*Get the source handler from the list*/
    if(!srcSessionHandlerList.empty())
    {
        srcHandle = srcSessionHandlerList.back();
        DEBUG_PRINT(DEBUG_LOG,"Fetched source session handler (%p) from the source list\n",(void*)srcHandle);
    }
    else
    {
        DEBUG_PRINT(DEBUG_LOG, "Source Session List is empty\n");
        return false;
    }

    /*Get the sink handler from the list*/
    if(!sinkSessionHandlerList.empty())
    {
        sinkHandle = sinkSessionHandlerList.back();
        DEBUG_PRINT(DEBUG_LOG,"Fetched sink session handler (%p) from the sink list\n",(void*)sinkHandle);
    }
    else
    {
        DEBUG_PRINT(DEBUG_LOG, "Sink Session List is empty\n");
        return false;
    }

    //Start processing src packet
    DTCPIP_Packet *packetSrc=new DTCPIP_Packet;

    //Input for source packet processing
    packetSrc->session = srcHandle;
    packetSrc->emi = 0x0C;
    packetSrc->isEOF = false;
    packetSrc->dataInPhyPtr = NULL;
    packetSrc->dataLength = tsLength;
    packetSrc->dataInPtr = new uint8_t [packetSrc->dataLength+1];
    istringstream bufferStr(testTSStream);
    unsigned int i = 0;
    do
    {
        unsigned int value;
        bufferStr >> std::hex >> value;
        packetSrc->dataInPtr[i] = value & 0xff;
        i++;
    } while (bufferStr);
    DEBUG_PRINT(DEBUG_TRACE,"TS Clear Stream Input: ");
    for (unsigned int i = 0; i < packetSrc->dataLength; i++) {
        printf("%x ", packetSrc->dataInPtr[i]);
    }
    printf("\n\n");

    //Initialize src output parameters
    packetSrc->dataOutPtr = NULL;
    packetSrc->dataOutPhyPtr = NULL;
    packetSrc->pcpHeader = NULL;
    packetSrc->pcpHeaderLength = 0;
    packetSrc->pcpHeaderOffset = 0;

    //Process source packet
    DEBUG_PRINT(DEBUG_TRACE,"Start DTCPMgrProcessPacket Encryption...\n\n");
    int rcProcessSrc = DTCPMgrProcessPacket(srcHandle, packetSrc);
    DEBUG_PRINT(DEBUG_TRACE,"Src DTCPMgrProcessPacket returnCode = %d\n",(int)rcProcessSrc);
    if((DTCP_SUCCESS == rcProcessSrc) && (packetSrc->dataOutPtr != NULL))
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n----- Encrypted packet Info Start ----\n");
        DEBUG_PRINT(DEBUG_TRACE,"pcpHeaderOffset = %d\n",packetSrc->pcpHeaderOffset);
        DEBUG_PRINT(DEBUG_TRACE,"pcpHeaderLength = %d\n",packetSrc->pcpHeaderLength);
        DEBUG_PRINT(DEBUG_TRACE,"pcpHeader: ");
        for (unsigned int i = 0; i < packetSrc->pcpHeaderLength; i++) {
            printf("%x ", packetSrc->pcpHeader[i]);
        }
        printf("\n");
        DEBUG_PRINT(DEBUG_TRACE,"dataLength = %d\n",packetSrc->dataLength);
        DEBUG_PRINT(DEBUG_TRACE,"\ndataOutPtr (first 192 bytes): ");
        for (int i = 0; i < tsLength; i++) {
            printf("%x ", packetSrc->dataOutPtr[i]);
        }
        DEBUG_PRINT(DEBUG_TRACE,"\n----- Encrypted packet Info End -----\n\n");
        //Checkpoint
        if (('\0' != packetSrc->pcpHeader[0]) && (0 == packetSrc->pcpHeaderLength))
        {
            DEBUG_PRINT(DEBUG_TRACE,"Error calculating pcpHeaderLength. pcpHeader is NULL\n");
            status = false;
        }
        else if (('\0' == packetSrc->pcpHeader[0]) && (0 != packetSrc->pcpHeaderLength))
        {
            DEBUG_PRINT(DEBUG_TRACE,"Error calculating pcpHeaderLength. pcpHeader is NOT NULL\n");
            status = false;
        }
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE,"Src DTCPMgrProcessPacket failed\n");
        status = false;
	return status;
    }

    //Start processing sink packet
    DTCPIP_Packet *packetSink=new DTCPIP_Packet;

    //Input for sink packet processing
    packetSink->session = sinkHandle;
    packetSink->dataInPhyPtr = NULL;
    packetSink->dataLength = packetSrc->pcpHeaderLength + packetSrc->dataLength;
    packetSink->dataInPtr = new uint8_t [packetSink->dataLength+1];
    unsigned int x = 0;
    //Copy 14 bytes of Src pcpHeader for decryption
    for(x = 0; x < packetSrc->pcpHeaderLength; x++)
    {
        packetSink->dataInPtr[x] = packetSrc->pcpHeader[x];
    }
    //Copy all bytes from Src dataOutPtr for decryption
    for(unsigned int i = 0; i < packetSrc->dataLength; i++,x++)
    {
        packetSink->dataInPtr[x] = packetSrc->dataOutPtr[i];
    }
    DEBUG_PRINT(DEBUG_TRACE,"Encrypted TS Stream (first 192 bytes): ");
    for (int i = 0; i < tsLength; i++) {
        printf("%x ", packetSink->dataInPtr[i]);
    }
    printf("\n\n");

    //Initialize sink output parameters
    packetSink->dataOutPtr = NULL;
    packetSink->dataOutPhyPtr = NULL;
    packetSink->emi = 0x00;

    //Process Sink Packet
    DEBUG_PRINT(DEBUG_TRACE,"Start DTCPMgrProcessPacket Decryption...\n\n");
    int rcProcessSink = DTCPMgrProcessPacket(sinkHandle, packetSink);
    DEBUG_PRINT(DEBUG_TRACE, "Sink DTCPMgrProcessPacket returnCode = %d\n",(int)rcProcessSink);
    if((DTCP_SUCCESS == rcProcessSink) && (packetSink->dataOutPtr != NULL))
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n----- Decrypted packet Info Start -----\n");
        DEBUG_PRINT(DEBUG_TRACE,"emi = %d\n",packetSink->emi);
        DEBUG_PRINT(DEBUG_TRACE,"dataLength = %d\n",packetSink->dataLength);
        DEBUG_PRINT(DEBUG_TRACE,"dataOutPtr = ");
        for (int i = 0; i < tsLength; i++) {
            printf("%x ", packetSink->dataOutPtr[i]);
        }
        DEBUG_PRINT(DEBUG_TRACE,"\n----- Decrypted packet Info End -----\n\n");
        //Updating emi on sink side is not implemented on RDK currently
        /*
        if(packetSink->emi != packetSrc->emi)
        {
            DEBUG_PRINT(DEBUG_TRACE, "Incorrect emi value in processed sink packet\n");
            status = false;
        }
        */
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE,"Sink DTCPMgrProcessPacket failed\n");
        status = false;
    }

    if (DTCP_SUCCESS == rcProcessSrc)
    {
        //Release packetSrc->dataOutPtr and pcpHeader allocated by dtcp manager
        returnCode = DTCPMgrReleasePacket(packetSrc);
        DEBUG_PRINT(DEBUG_TRACE, "Src DTCPMgrReleasePacket returnCode = %d\n",(int)returnCode);
        if (DTCP_SUCCESS != returnCode)
        {
            DEBUG_PRINT(DEBUG_TRACE, "Src DTCPMgrReleasePacket failed\n");
            status = false;
        }
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "Src DTCPMgrReleasePacket not invoked. Src ProcessPacket failed\n");
        status = false;
    }

    if (DTCP_SUCCESS == rcProcessSink)
    {
        //Release packetSink->dataOutPtr allocated by dtcp manager
        returnCode = DTCPMgrReleasePacket(packetSink);
        DEBUG_PRINT(DEBUG_TRACE, "Sink DTCPMgrReleasePacket returnCode = %d\n",(int)returnCode);
        if (DTCP_SUCCESS != returnCode)
        {
            DEBUG_PRINT(DEBUG_TRACE, "Sink DTCPMgrReleasePacket failed\n");
            status = false;
        }
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "Sink DTCPMgrReleasePacket not invoked. Sink ProcessPacket failed\n");
        status = false;
    }

    //Release packetSink->dataInPtr allocated by caller
    if (packetSink->dataInPtr) {
        delete [] packetSink->dataInPtr;
        packetSink->dataInPtr = NULL;
    }

    //Release packetSrc->dataInPtr allocated by caller
    if (packetSrc->dataInPtr) {
        delete [] packetSrc->dataInPtr;
        packetSrc->dataInPtr = NULL;
    }

    return status;
}
/**************************************************************************
Function name : DTCPAgent::initialize

Arguments     : Input arguments are Version string and DTCPAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool DTCPAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_ERROR, "DTCPAgent Initialization\n");

    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string DTCPAgent::testmodulepre_requisites()
{
/*    //Initialize SOC
    #ifdef USE_SOC_INIT
    soc_init(1, (char*)"tdk_agent", 1);
    #endif
*/
    std::list<DTCP_SESSION_HANDLE>::iterator it;
    if(!srcSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of source session handler list\n");
        for(it = srcSessionHandlerList.begin(); it != srcSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Source Handler: %p ",(void*)*it);
        }
    }

    if(!sinkSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of sink session handler list\n");
        for(it = sinkSessionHandlerList.begin(); it != sinkSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Sink Handler: %p ",(void*)*it);
        }
    }

    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool DTCPAgent::testmodulepost_requisites()
{
/*
    // Uninitialize SOC
    #ifdef USE_SOC_INIT
    soc_uninit();
    #endif
*/
    std::list<DTCP_SESSION_HANDLE>::iterator it;
    if(!srcSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of source session handler list\n");
        for(it = srcSessionHandlerList.begin(); it != srcSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Source Handler: %p ",(void*)*it);
        }
    }

    if(!sinkSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of sink session handler list\n");
        for(it = sinkSessionHandlerList.begin(); it != sinkSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Sink Handler: %p ",(void*)*it);
        }
    }

    return TEST_SUCCESS;
}


/**************************************************************************
Function name : DTCPAgent::DTCPAgent_Test_Execute

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to run test dtcp  module.
**************************************************************************/
void DTCPAgent::DTCPAgent_Test_Execute(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute --->Entry\n");

    //Initialize SOC
    #ifdef USE_SOC_INIT
    soc_init(1, (char*)"tdk_agent", 1);
    #endif
    string functionName = req["funcName"].asString();
    dtcp_result_t returnCode = DTCP_SUCCESS;
    DEBUG_PRINT(DEBUG_LOG,"Received function name: %s\n", functionName.c_str());

    try
    {
        if (functionName.compare("DTCPMgrInitialize")==0)
        {
            stringstream details;
            returnCode = DTCPMgrInitialize();
            DEBUG_PRINT(DEBUG_LOG, "%s() returnCode = %d\n",functionName.c_str(),(int)returnCode);

            if (returnCode != DTCP_SUCCESS)
            {
                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrInitialize() failed to intialize.\n");
                response["result"] = "FAILURE";
                details << "DTCPMgrInitialize() failed. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrInitialize() successfully intialized.\n");
                response["result"] = "SUCCESS";
                details << "DTCPMgrInitialize() success. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
        }
        else if (functionName.compare("DTCPMgrStartSource")==0)
        {
            string ifname = req["strParam1"].asString();
            int portNo = req["intParam2"].asInt();
            stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [ifname:%s portNo:%d]\n",ifname.c_str(),portNo);
            returnCode = DTCPMgrStartSource(&ifname[0],portNo);
            DEBUG_PRINT(DEBUG_LOG, "%s() returnCode = %d\n",functionName.c_str(),(int)returnCode);

            if (returnCode != DTCP_SUCCESS)
            {
                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrStartSource() failed to Start Source.\n");
                response["result"] = "FAILURE";
                details << "DTCPMgrStartSource() failed. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrStartSource() successfully Start Source.\n");
                response["result"] = "SUCCESS";
                details << "DTCPMgrStartSource() success. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
        }
        else if (functionName.compare("DTCPMgrStopSource")==0)
        {
            returnCode = DTCPMgrStopSource();
            DEBUG_PRINT(DEBUG_LOG, "%s() returnCode = %d\n",functionName.c_str(),(int)returnCode);
            stringstream details;

            if (returnCode != DTCP_SUCCESS)
            {
                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrStopSource() failed to Stopped Source.\n");
                response["result"] = "FAILURE";
                details << "DTCPMgrStopSource() failed. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrStopSource() successfully Stopped Source.\n");
                response["result"] = "SUCCESS";
                details << "DTCPMgrStopSource() success. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
        }
        else if (functionName.compare("DTCPMgrCreateSourceSession")==0)
        {
            string sinkip = req["strParam1"].asString();
            int keylabel = req["intParam2"].asInt();
            int pcppacketsz = req["intParam3"].asInt();
            int maxpacketsz = req["intParam4"].asInt();
            stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [SinkIp:%s keyLabel:%d pcpPacketSize:%d maxPacketSize:%d]\n",sinkip.c_str(),keylabel,pcppacketsz,maxpacketsz);
            DTCP_SESSION_HANDLE handle;

            returnCode = DTCPMgrCreateSourceSession(&sinkip[0],keylabel,pcppacketsz,maxpacketsz,&handle);
            DEBUG_PRINT(DEBUG_LOG, "%s() returnCode = %d\n",functionName.c_str(),(int)returnCode);

            if(returnCode != DTCP_SUCCESS)
            {
                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrCreateSourceSession() failed to create source handler.\n");
                response["result"] = "FAILURE";
                details << "DTCPMgrCreateSourceSession() failure. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrCreateSourceSession() successfully Created Source handler.\n");
                response["result"] = "SUCCESS";
                details << "DTCPMgrCreateSourceSession() success. ReturnCode:" << returnCode;
                response["details"] = details.str();
                /*Pushing the source session handler on to the sourceList */
                srcSessionHandlerList.push_back(handle);
                DEBUG_PRINT(DEBUG_LOG, "Source Handler (%p) pushed into list\n",(void*)handle);
            }
        }
        else if (functionName.compare("DTCPMgrCreateSinkSession")==0)
        {
            string srcip = req["strParam1"].asString();
            int portNo = req["intParam2"].asInt();
            bool uniqueKey = req["intParam3"].asInt();
            int maxpacketsz = req["intParam4"].asInt();
            stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [SrcIp:%s srcPort:%d uniqueKey:%d maxPacketSize:%d]\n",srcip.c_str(),portNo,uniqueKey,maxpacketsz);
            DTCP_SESSION_HANDLE handle;

            returnCode = DTCPMgrCreateSinkSession(&srcip[0],portNo,uniqueKey,maxpacketsz,&handle);
            DEBUG_PRINT(DEBUG_LOG, "%s() returnCode = %d\n",functionName.c_str(),(int)returnCode);

            if(returnCode != DTCP_SUCCESS)
            {
                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrCreateSinkSession() failed to create sink handler.\n");
                response["result"] = "FAILURE";
                details << "DTCPMgrCreateSinkSession() failed. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrCreateSinkSession() successfully Created Sink handler.\n");
                response["result"] = "SUCCESS";
                details << "DTCPMgrCreateSinkSession() success. ReturnCode:" << returnCode;
                response["details"] = details.str();
                /*Pushing the sink session handler on to the sinkList */
                sinkSessionHandlerList.push_back(handle);
                DEBUG_PRINT(DEBUG_LOG, "Sink Handler (%p) pushed into list\n",(void*)handle);
            }
        }
        else if ((functionName.compare("DTCPMgrProcessPacket")==0) || (functionName.compare("DTCPMgrReleasePacket")==0))
        {
            if (dtcpProcessReleasePacket())
            {
                DEBUG_PRINT(DEBUG_TRACE, "Successfully Processed and Released Packet\n");
                response["result"] = "SUCCESS";
                response["details"] = "Successfully Processed and Released Packet";
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to Process / Release Packet\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed to Process / Release Packet";
            }
        }
        else if (functionName.compare("DTCPMgrDeleteDTCPSession")==0)
        {
            int iDeviceType = req["intParam3"].asInt();
            stringstream details;
            DEBUG_PRINT(DEBUG_LOG,"Get last element in list of DeviceType=%d\n",iDeviceType);

            /*Check for handler to be deleted is for source session*/
            if(iDeviceType == DTCP_SOURCE)
            {
                if(!srcSessionHandlerList.empty())
                {
                    /*Get the source handler from the list*/
                    DTCP_SESSION_HANDLE pDtcpSession = srcSessionHandlerList.back();
                    DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the source list\n",(void*)pDtcpSession);
                    returnCode = DTCPMgrDeleteDTCPSession(pDtcpSession);
                    if(DTCP_SUCCESS == returnCode)
                    {
                        srcSessionHandlerList.remove(pDtcpSession);
                        DEBUG_PRINT(DEBUG_LOG,"DTCP session handler deleted and entry removed from source handler list\n");
                        response["result"] = "SUCCESS";
                        details << "DTCPMgrDeleteDTCPSession() success. ReturnCode:" << returnCode;
                        response["details"] = details.str();
                    }
                    else
                    {
                        DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrDeleteDTCPSession() failed to delete the Session handler.\n");
                        response["result"] = "FAILURE";
                        details << "DTCPMgrDeleteDTCPSession() failed. ReturnCode:"<< returnCode;
                        response["details"] = details.str();
                    }
                }
                else
                {
                    DEBUG_PRINT(DEBUG_LOG, "Source Session List is empty\n");
                    response["result"]="FAILURE";
                    response["details"]="Source Session not created";
                }
            }
            else if(iDeviceType == DTCP_SINK)
            {
                if(!sinkSessionHandlerList.empty())
                {
                    /*Get the sink handler from the list*/
                    DTCP_SESSION_HANDLE pDtcpSession = sinkSessionHandlerList.back();
                    DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the sink list\n",(void*)pDtcpSession);
                    returnCode = DTCPMgrDeleteDTCPSession(pDtcpSession);
                    if(DTCP_SUCCESS == returnCode)
                    {
                        sinkSessionHandlerList.remove(pDtcpSession);
                        DEBUG_PRINT(DEBUG_LOG,"DTCP session handler deleted and entry removed from sink handler list\n");
                        response["result"] = "SUCCESS";
                        details << "DTCPMgrDeleteDTCPSession() success. ReturnCode:" << returnCode;
                        response["details"] = details.str();
                    }
                    else
                    {
                        DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrDeleteDTCPSession() failed to delete the Session handler.\n");
                        response["result"] = "FAILURE";
                        details << "DTCPMgrDeleteDTCPSession() failed. ReturnCode:"<< returnCode;
                        response["details"] = details.str();
                    }
                }
                else
                {
                    DEBUG_PRINT(DEBUG_LOG, "Sink Session List is empty\n");
                    response["result"]="FAILURE";
                    response["details"]="Sink Session List not created";
                }
            }
            else
            {
                DEBUG_PRINT(DEBUG_LOG, "DeviceType %d is invalid\n",iDeviceType);
                response["result"]="FAILURE";
                response["details"]="DeviceType is invalid";
            }
        }
        else if (functionName.compare("DTCPMgrGetNumSessions")==0)
        {
            stringstream details;
            int iDeviceType = req["intParam2"].asInt();

            DEBUG_PRINT(DEBUG_LOG,"Input [DeviceType:%d]\n",iDeviceType);

            int numSessions = DTCPMgrGetNumSessions((DTCPDeviceType)iDeviceType);
            DEBUG_PRINT(DEBUG_LOG,"%s() numSessions %d\n",functionName.c_str(),numSessions);

            if ((numSessions < 0) || (((iDeviceType < DTCP_SOURCE) || (iDeviceType > DTCP_UNKNOWN)) && (numSessions > 0)))
                response["result"] = "FAILURE";
            else
                response["result"] = "SUCCESS";

            details << numSessions;
            response["details"] = details.str();
        }
        else if (functionName.compare("DTCPMgrGetSessionInfo")==0)
        {
            int iDeviceType = req["intParam3"].asInt();
            stringstream details;
            DEBUG_PRINT(DEBUG_LOG,"Get last element in list of DeviceType=%d\n",iDeviceType);

            DTCP_SESSION_HANDLE pDtcpSession;
            if(iDeviceType == DTCP_SOURCE)
            {
                if(!srcSessionHandlerList.empty())
                {
                    /*Get the source handler from the list*/
                    pDtcpSession = srcSessionHandlerList.back();
                    DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the source list\n",(void*)pDtcpSession);
                }
                else
                {
                    DEBUG_PRINT(DEBUG_LOG, "Source Session List is empty\n");
                    response["result"]="FAILURE";
                    response["details"]="Source Session not created";
                    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit\n");
                    return;
                }
            }
            else if(iDeviceType == DTCP_SINK)
            {
                if(!sinkSessionHandlerList.empty())
                {
                    /*Get the sink handler from the list*/
                    pDtcpSession = sinkSessionHandlerList.back();
                    DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the sink list\n",(void*)pDtcpSession);
                }
                else
                {
                    DEBUG_PRINT(DEBUG_LOG, "Sink Session List is empty\n");
                    response["result"]="FAILURE";
                    response["details"]="Sink Session List not created";
                    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit\n");
                    return;
                }
            }
            else
            {
                DEBUG_PRINT(DEBUG_LOG, "DeviceType %d is invalid\n",iDeviceType);
                response["result"]="FAILURE";
                response["details"]="DeviceType is invalid";
                DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit\n");
                return;
            }

            DTCPIP_Session sessionInfo;
            sessionInfo.remote_ip = new char [IPADDR_LEN+1];
            returnCode = DTCPMgrGetSessionInfo(pDtcpSession,&sessionInfo);

            if(returnCode != DTCP_SUCCESS)
            {
                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrGetSessionInfo() failed to fetch Session Info.\n");
                response["result"] = "FAILURE";
                details << "DTCPMgrGetSessionInfo() failed. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrGetSessionInfo() successfully fetched session Info for handle %p\n",(void*)pDtcpSession);
                DEBUG_PRINT(DEBUG_TRACE, "session_handle:%p device_type:%d remote_ip:%s uniqueKey:%d\n",(void*)sessionInfo.session_handle,sessionInfo.device_type,sessionInfo.remote_ip,sessionInfo.uniqueKey);
                if ((pDtcpSession != sessionInfo.session_handle) || (iDeviceType != sessionInfo.device_type))
                    response["result"] = "FAILURE";
                else
                    response["result"] = "SUCCESS";
                /*Send session info to script. */
                details << "DeviceType:" << sessionInfo.device_type << " RemoteIp:" << sessionInfo.remote_ip << " UniqueKey:"<< sessionInfo.uniqueKey;
                response["details"] = details.str();
            }
            delete [] sessionInfo.remote_ip;
        }
        else if (functionName.compare("DTCPMgrSetLogLevel")==0)
        {
            int level= req["intParam2"].asInt();
            stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [LogLevel:%d]\n",level);
            returnCode = DTCPMgrSetLogLevel(level);
            DEBUG_PRINT(DEBUG_LOG, "%s() returnCode = %d\n",functionName.c_str(),(int)returnCode);

            if(returnCode != DTCP_SUCCESS)
            {
                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrSetLogLevel() failed.\n");
                response["result"] = "FAILURE";
                details << "DTCPMgrSetLogLevel() failed. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
            else
            {
                DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrSetLogLevel() successfully set.\n");
                response["result"] = "SUCCESS";
                details << "DTCPMgrSetLogLevel() success. ReturnCode:" << returnCode;
                response["details"] = details.str();
            }
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR,"Unsupported function call\n");
            response["details"]= "Unsupported function call";
            response["result"]="FAILURE";
        }
    }
    catch(exception &e)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured during function call\n");
        DEBUG_PRINT(DEBUG_LOG,"Exception caught is %s\n", e.what() );
        response["details"]= "Exception occured during function call";
        response["result"]="FAILURE";
    }

    // Uninitialize SOC
    #ifdef USE_SOC_INIT
    soc_uninit();
    #endif

    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit\n");
    return;
}
/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "DTCPAgent".
**************************************************************************/

extern "C" DTCPAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
    return new DTCPAgent(ptrtcpServer);
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool DTCPAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
    return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is DTCPAgent Object

Description   : This function will be used to destory the DTCPAgent object.
**************************************************************************/
extern "C" void DestroyObject(DTCPAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_LOG, "Destroying DTCPAgent Agent object\n");
    delete stubobj;
}
