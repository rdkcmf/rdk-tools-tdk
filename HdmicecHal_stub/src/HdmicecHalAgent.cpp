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

#include "HdmicecHal.h"
#include "HdmicecHalAgent.h"

// Function to store input cec frame string into tx array
static void get_cec_frame_tx(char *frame)
{
        char *token = strtok(frame, " ");
        if (token != NULL){
            while (token != NULL) {
                cec_frame_tx[cec_frame_size_tx] = (int)strtol(token,NULL, 16);
                token = strtok(NULL, " ");
                cec_frame_size_tx++;
            }
        }else{
            cec_frame_tx[cec_frame_size_tx] = (int)strtol(frame,NULL, 16);
            cec_frame_size_tx++;
        }
}

// Function to store received cec frame into rx array
static void get_cec_frame_rx(unsigned char *frame, int size)
{
        char token[5];
        for (int i = 0; i < size; i++){
             sprintf(token,"%02X", frame[i]);
             cec_frame_rx[cec_frame_size_rx] = (int)strtol(token,NULL, 16);
             cec_frame_size_rx++;
        }
        received_status = 1;
        DEBUG_PRINT(DEBUG_TRACE, "Rx frames stored successfully\n");
}

// Function to convert rx array to rx cec frame string
static void get_cec_frame_rx_str(unsigned char *frame, int size)
{
        char token[5];
        for (int i = 0; i < size; i++){
            sprintf(token,"%02X ", frame[i]);
            cec_frame_rx_str = cec_frame_rx_str + token;
        }
}

// Function to display cec frame
static void disp_cec_frame(unsigned char *frame, int size)
{
        DEBUG_PRINT(DEBUG_TRACE, "CEC Frame size: %d\n",size);
        DEBUG_PRINT(DEBUG_TRACE, "CEC Frame data: ");
        for (int i = 0; i < size; i++){
            DEBUG_PRINT(DEBUG_TRACE, "%02X\n", frame[i]);
        }
        if(transmit_status){
            DEBUG_PRINT(DEBUG_TRACE, "Populating Rx frames\n");
            get_cec_frame_rx(frame,size);
        }
}

// Function to check tx send status
static void checkTxStatus(int sendStatus)
{
        if (sendStatus == HDMI_CEC_IO_INVALID_STATE)
            sprintf(txStatus,"HDMI_CEC_IO_INVALID_STATE");
        else if (sendStatus == HDMI_CEC_IO_INVALID_ARGUMENT)
            sprintf(txStatus,"HDMI_CEC_IO_INVALID_ARGUMENT");
        else if (sendStatus == HDMI_CEC_IO_LOGICALADDRESS_UNAVAILABLE)
            sprintf(txStatus,"HDMI_CEC_IO_LOGICALADDRESS_UNAVAILABLE");
        else if (sendStatus == HDMI_CEC_IO_SENT_FAILED)
            sprintf(txStatus,"HDMI_CEC_IO_SENT_FAILED");
        else if (sendStatus == HDMI_CEC_IO_GENERAL_ERROR)
            sprintf(txStatus,"HDMI_CEC_IO_GENERAL_ERROR");
        else if (sendStatus == HDMI_CEC_IO_SENT_BUT_NOT_ACKD)
           sprintf(txStatus,"HDMI_CEC_IO_SENT_BUT_NOT_ACKD");
        else{
            transmit_status = 1;
            sprintf(txStatus,"Transmission success");
        }
        if(transmit_status)
            DEBUG_PRINT(DEBUG_TRACE, "%s: %s\n",txStatus,txMethod);
        else
            DEBUG_PRINT(DEBUG_TRACE, "%s: %s call failed\n",txStatus,txMethod);
}

// Function for Tx call back
static void driverTransmitCallback(int handle, void *callbackData,int result)
{
        DEBUG_PRINT(DEBUG_TRACE, "\n\n================ CEC Frame Transmitted ===============\n");
        checkTxStatus(result);
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecSetTxCallback call success\n");
}

// Function for Rx call back
static void driverReceiveCallback(int handle, void *callbackData, unsigned char *buf, int len)
{
        DEBUG_PRINT(DEBUG_TRACE, "\n\n================ CEC Frame Received ==================\n");
        disp_cec_frame((unsigned char*)buf,len);
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecSetRxCallback call success\n");
        m_cv.notify_one();
}


// Function to decode header byte and display From/To Address
static void messageAddressDecoder()
{
       char header[50];
       int from = (((cec_frame_rx[HEADER_OFFSET]) & 0xF0) >> 4);
       int to   = (((cec_frame_rx[HEADER_OFFSET]) & 0x0F) >> 0);
       sprintf(header,"From: %s, To: %s",address_[from],address_[to]);
       cec_frame_header = header;
       DEBUG_PRINT(DEBUG_TRACE, "From : %s\n",address_[from]);
       DEBUG_PRINT(DEBUG_TRACE, "To   : %s\n",address_[to]);
}

// Function to decode opcode & operand and display the result
static void messageOpcodeAndOperandDecoder()
{
        char result[100];
        std::stringstream vendor_id;
        std::vector<uint8_t> language;
        switch(cec_frame_rx[OPCODE_OFFSET]){
            case CEC_VERSION:
                DEBUG_PRINT(DEBUG_TRACE, "Decoding CEC Version\n");
                sprintf(result,"Version: %s",version_[cec_frame_rx[OPRAND_OFFSET]]);
                DEBUG_PRINT(DEBUG_TRACE, "Version: %s\n",version_[cec_frame_rx[OPRAND_OFFSET]]);
                break;
            case REPORT_POWER_STATUS:
                DEBUG_PRINT(DEBUG_TRACE, "Decoding Power Status\n");
                sprintf(result,"Power Status: %s",power_modes_[cec_frame_rx[OPRAND_OFFSET]]);
                DEBUG_PRINT(DEBUG_TRACE, "Power Status: %s\n",power_modes_[cec_frame_rx[OPRAND_OFFSET]]);
                break;
            case DEVICE_VENDOR_ID:
                DEBUG_PRINT(DEBUG_TRACE, "Decoding Device Vendor ID\n");
                for (int i = OPRAND_OFFSET; i < (OPRAND_OFFSET + MAX_LEN_VENDOR_ID); i++)
                    vendor_id << std::hex << (int)cec_frame_rx[i];
                sprintf(result, "VendorID: %s",vendor_id.str().c_str());
                DEBUG_PRINT(DEBUG_TRACE, "VendorID: %s\n",vendor_id.str().c_str());
                break;
            case SET_MENU_LANGUAGE:
                DEBUG_PRINT(DEBUG_TRACE, "Decoding Menu Language\n");
                for (int i = OPRAND_OFFSET; i < (OPRAND_OFFSET + MAX_LEN_LANG); i++)
                    language.push_back(cec_frame_rx[i]);
                sprintf(result,"Menu language: %s",std::string(language.begin(), language.end()).c_str());
                DEBUG_PRINT(DEBUG_TRACE, "Menu language: %s\n",std::string(language.begin(), language.end()).c_str());
                break;
            case FEATURE_ABORT:
                DEBUG_PRINT(DEBUG_TRACE, "Feature Abort Message\n");
                sprintf(result,"Feature Abort");
                break;
            default:
                sprintf(result,"Unhandled Message Received");
                DEBUG_PRINT(DEBUG_TRACE, "Unhandled Message Received \n");
                break;
        }
        cec_frame_result = result;
}

// Function to decode CEC frames
static void messageDecoder()
{
       DEBUG_PRINT(DEBUG_TRACE, "\n\n================ CEC Frame Decoder ===============\n");
       messageAddressDecoder();
       messageOpcodeAndOperandDecoder();
}

// Function for iarmbus event
static void cecEventHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
        DEBUG_PRINT(DEBUG_TRACE, "\n\n================ CEC IARMBUS EVENT ===============\n");
        if( !strcmp(owner, IARM_BUS_CECMGR_NAME))
        {
            switch (eventId)
            {
                case IARM_BUS_CECMGR_EVENT_STATUS_UPDATED:
                {
                    cec_device_ready = 1;
                    DEBUG_PRINT(DEBUG_TRACE, "IARM_BUS_CECMGR_EVENT_STATUS_UPDATED device ready event received\n");
                }
                break;
            }
        }
}

// Function to generate CEC header byte
static void generate_cec_header(char *frame)
{
         DEBUG_PRINT(DEBUG_TRACE, "Generating CEC Header\n");
         int logicalAddress = 0;
         int ret = HdmiCecGetLogicalAddress(driverHandle,0,&logicalAddress);
         if (ret != 0){
             cec_header_flag = -1;
             DEBUG_PRINT(DEBUG_TRACE, "HdmiCecGetLogicalAddress call failed. Unable to generate Header Frame\n");
         }
         else{
             char from[5];
             sprintf(from,"%X",logicalAddress);
             strcpy(frame,from);  // Logical Address of STB
             strcat(frame,"0");   // Logical Address of TV is 0
             DEBUG_PRINT(DEBUG_TRACE, "CEC header framed successfully\n");
         }
}

// Function to clear all flags and arrays
static void clearCECFlagsAndFrameInfo()
{
    DEBUG_PRINT(DEBUG_TRACE, "Clearing CEC callback flags & CEC frame info ...\n");
    transmit_status = 0;
    received_status = 0;
    cec_header_flag = 0;
    cec_device_ready  = 0;
    cec_frame_size_tx = 0;
    cec_frame_size_rx = 0;
    cec_receive_flag  = 1;
    cec_frame_rx_str.clear();
    cec_frame_header.clear();
    cec_frame_result.clear();
    memset(cec_frame_tx, 0, sizeof(cec_frame_tx));
    memset(cec_frame_rx, 0, sizeof(cec_frame_rx));
}

bool IARM_Bus_event_registration()
{
#ifndef NO_DEVICE_READY_EVENT
    DEBUG_PRINT(DEBUG_TRACE, "Init IARMBUS lib ...\n");
    IARM_Result_t retval;
    retval = IARM_Bus_Init("agent");
    if(retval == 0)
        DEBUG_PRINT(DEBUG_TRACE, "IARM_Bus_Init call success\n");
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "IARM_Bus_Init call failure\n");
        return false;
    }
    retval = IARM_Bus_Connect();
    if(retval == 0)
        DEBUG_PRINT(DEBUG_TRACE, "IARM_Bus_Connect call success\n");
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "IARM_Bus_Connect call failure\n");
        return false;
    }
    DEBUG_PRINT(DEBUG_TRACE, "Agent connected with IARMBUS\n");
    retval = IARM_Bus_RegisterEventHandler(IARM_BUS_CECMGR_NAME, IARM_BUS_CECMGR_EVENT_STATUS_UPDATED, cecEventHandler);
    DEBUG_PRINT(DEBUG_TRACE, "Registered IARMBUS event handler fn:cecEventHandler\n");
    if(retval == 0)
    {
        DEBUG_PRINT(DEBUG_TRACE, "Registered IARMBUS event handler fn:cecEventHandler\n");
        return true;
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "Registration failed for IARMBUS event handler fn:cecEventHandler\n");
        return false;
    }
#endif
    DEBUG_PRINT(DEBUG_TRACE, "Platform doesnot support IARMBUS event handler fn:cecEventHandler\n");
    return true;
}

bool Event_Listener()
{
#ifndef NO_DEVICE_READY_EVENT
    std::unique_lock<std::mutex> m(m_idle);
    if (m_cv_init.wait_for(m, std::chrono::seconds(TIMEOUT), []{ return cec_device_ready == 1; })){
        DEBUG_PRINT(DEBUG_TRACE, "Finished IARMBUS event waiting. DONE\n");
        return true;
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "IARMBUS event waiting timeout\n");
        DEBUG_PRINT(DEBUG_TRACE, "IARM_BUS_CECMGR_EVENT_STATUS_UPDATED device ready event not received\n");
        return false;
    }
#endif
    DEBUG_PRINT(DEBUG_TRACE, "Platform doesnot support IARM_BUS_CECMGR_EVENT_STATUS_UPDATED event\n");
    return true;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string HdmicecHalAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule pre_requisites --> Entry\n");

    if(!(IARM_Bus_event_registration()))
    {
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule pre_requisites failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule pre_requisites --> Exit\n");  
        return "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "HdmiCecOpen ...\n");
    int init = HdmiCecOpen(&driverHandle);
    if (init ==  HDMI_CEC_IO_SUCCESS){
        if(Event_Listener())
        {
            DEBUG_PRINT(DEBUG_TRACE, "HdmiCecOpen call success\n");
            DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule pre_requisites --> Exit\n");
            return "SUCCESS";
        }
        else{
            DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule pre_requisites failed\n");
            DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule pre_requisites --> Exit\n");
            return "FAILURE";
        }
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecOpen call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description   : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool HdmicecHalAgent::testmodulepost_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule post_requisites --> Entry\n");
    clearCECFlagsAndFrameInfo();
    DEBUG_PRINT(DEBUG_TRACE, "HdmiCecClose ...\n");
    int term = HdmiCecClose(driverHandle);

#ifndef NO_DEVICE_READY_EVENT
    IARM_Bus_UnRegisterEventHandler(IARM_BUS_CECMGR_NAME, IARM_BUS_CECMGR_EVENT_STATUS_UPDATED);
    IARM_Bus_Disconnect();
    IARM_Bus_Term();
#endif

    if (term == HDMI_CEC_IO_SUCCESS){
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecClose call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule post_requisites --> Exit\n");
        return "SUCCESS";
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecClose call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal testmodule post_requisites --> Exit\n");
        return "FAILURE";
    }
}

/**************************************************************************
Function Name   : CreateObject
Arguments       : NULL
Description     : This function is used to create a new object of the class
                  "HdmicecHalAgent"
**************************************************************************/
extern "C" HdmicecHalAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new HdmicecHalAgent(ptrtcpServer);
}

/****************************************************************************
 *Function name : initialize
 *Description   : Initialize Function will be used for registering the wrapper
 *                method with the agent so that wrapper functions will be used
 *                in the script
 *****************************************************************************/
bool HdmicecHalAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT (DEBUG_TRACE, "HdmicecHal Initialization Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "HdmicecHal Initialization Exit\n");
    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name  : HdmicecHal_GetLogicalAddress
 *Description    : This function is to invoke HdmiCecGetLogicalAddress API
 *****************************************************************************/
void HdmicecHalAgent::HdmicecHal_GetLogicalAddress(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_GetLogicalAddress --->Entry\n");
    if(&req["dev_type"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Device Type";
        return;
    }

    char details[100];

    int logicalAddress = 0;
    int devType = (int) req["dev_type"].asInt();
    int ret = HdmiCecGetLogicalAddress(driverHandle,devType,&logicalAddress);
    if (ret == 0){
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecGetLogicalAddress call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "LogicalAddress : 0x%X (dec: %u)\n",logicalAddress,logicalAddress);
        sprintf(details,"LogicalAddress: hex:0x%X, dec: %u",logicalAddress,logicalAddress);
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_GetLogicalAddress ---> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="HdmiCecGetLogicalAddress call failed";
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecGetLogicalAddress call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_GetLogicalAddress ---> Exit\n");
    }
    return;
}

/***************************************************************************
 *Function name  : HdmicecHal_GetPhysicalAddress
 *Description    : This function is to invoke HdmiCecPhysicalAddress API
 *****************************************************************************/
void HdmicecHalAgent::HdmicecHal_GetPhysicalAddress(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_GetPhysicalAddress --->Entry\n");
    char details[100];

    unsigned int physicalAddress = 0;
    HdmiCecGetPhysicalAddress(driverHandle,&physicalAddress);
    DEBUG_PRINT(DEBUG_TRACE, "HdmiCecGetPhysicalAddress call success\n");
    DEBUG_PRINT(DEBUG_TRACE, "PhysicalAddress : 0x%X (dec: %u)\n",physicalAddress,physicalAddress);
    sprintf(details,"PhysicalAddress: hex: 0x%X, dec: %u",physicalAddress,physicalAddress);
    response["result"]="SUCCESS";
    response["details"]=details;
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_GetPhysicalAddress ---> Exit\n");
    return;
}

/***************************************************************************
 *Function name  : HdmicecHal_SetTxCallback
 *Description    : This function is to invoke HdmiCecSetTxCallback API
 *****************************************************************************/
void HdmicecHalAgent::HdmicecHal_SetTxCallback(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_SetTxCallback --->Entry\n");
    char details[100];

    int ret = HdmiCecSetTxCallback(driverHandle, driverTransmitCallback, 0);
    if (ret == 0){
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecSetTxCallback call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "TxCallback registered with fn:driverTransmitCallback()\n");
        sprintf(details,"TxCallback registered with fn:driverTransmitCallback()");
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_SetTxCallback ---> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="HdmiCecSetTxCallback call failed";
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecSetTxCallback call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_SetTxCallback ---> Exit\n");
    }
    return;
}

/***************************************************************************
 *Function name  : HdmicecHal_SetRxCallback
 *Description    : This function is to invoke HdmiCecSetRxCallback API
 *****************************************************************************/
void HdmicecHalAgent::HdmicecHal_SetRxCallback(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_SetRxCallback --->Entry\n");
    char details[100];

    int ret = HdmiCecSetRxCallback(driverHandle, driverReceiveCallback, 0);
    if (ret == 0){
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecSetRxCallback call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "RxCallback registered with fn:driverReceiveCallback()\n");
        sprintf(details,"RxCallback registered with fn:driverReceiveCallback()");
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_SetRxCallback ---> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="HdmiCecSetRxCallback call failed";
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecSetRxCallback call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_SetRxCallback ---> Exit\n");
    }
    return;
}

/***************************************************************************
 *Function name  : HdmicecHal_Tx
 *Description    : This function is to invoke HdmiCecTx API to transmit
                   CEC frame synchronously and get trasmission status and
                   received frame using Tx and Rx call backs
 *****************************************************************************/
void HdmicecHalAgent::HdmicecHal_Tx(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_Tx --->Entry\n");
    if(&req["opcode"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Opcode Frame";
        return;
    }
    if(&req["receive_frames"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Receive Frame Flag";
        return;
    }
    char details[500];
    char frame[200];

    /* check whether CEC header is provided or not. If header is
       not provided generated header with src and destination
       logical addresses
    */
    if(&req["header"] != NULL && strlen(req["header"].asCString()) > 0){
        strcpy(frame,req["header"].asCString());
        DEBUG_PRINT(DEBUG_TRACE, "Using provided CEC header\n");
    }
    else{
         generate_cec_header(frame);
         if (cec_header_flag != 0){
             response["result"]="FAILURE";
             response["details"]="Unable to generate Header Frame";
             return;
         }
    }
    strcat(frame," ");
    strcat(frame,req["opcode"].asCString());

    /* If a opcode is intended for sending purpose only, then
       receive_frames should be set as 0. If a opcode is expected
       to receive cec frames from target device, then receive_frames
       should be set as 1. By default its set as 1 in TM
    */
    cec_receive_flag = req["receive_frames"].asInt();

    // convert string CEC frame to array & display
    get_cec_frame_tx(frame);
    disp_cec_frame((unsigned char*)cec_frame_tx,cec_frame_size_tx);
    sprintf(txMethod,"HdmiCecTx");
    DEBUG_PRINT(DEBUG_TRACE, "Receive CEC Frame : %s\n",cec_receive_flag?"TRUE":"FALSE");

    int sendStatus = HDMI_CEC_IO_SUCCESS;
    int ret = HdmiCecTx(driverHandle, cec_frame_tx, cec_frame_size_tx, &sendStatus);
    DEBUG_PRINT(DEBUG_TRACE, "Ret: %x HdmiCecTx call DONE  sendStatus: %x\n",ret,sendStatus);
    if (ret == HDMI_CEC_IO_SUCCESS ){
        checkTxStatus(sendStatus);
        if (transmit_status){
            DEBUG_PRINT(DEBUG_TRACE, "HdmiCecTx call success\n");
            std::unique_lock<std::mutex> m(m_idle);
            if (m_cv.wait_for(m, std::chrono::seconds(TIMEOUT), []{ return received_status == 1; })){
                DEBUG_PRINT(DEBUG_TRACE, "Finished Rx waiting. DONE\n");
                messageDecoder();

                get_cec_frame_rx_str((unsigned char*)cec_frame_rx,cec_frame_size_rx);
                sprintf(details, "Received CEC Frame: %s;Header: %s;Result: %s",cec_frame_rx_str.c_str(),cec_frame_header.c_str(),cec_frame_result.c_str());
                response["result"]="SUCCESS";
                response["details"]=details;
                DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_Tx --> Exit\n");
            }
            else if (cec_receive_flag == false){
                DEBUG_PRINT(DEBUG_TRACE, "CEC Frame Transmitted Successfully !!\n");
                response["result"]="SUCCESS";
                response["details"]="CEC Frame Transmitted Successfully";
                DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_Tx --> Exit\n");
            }
            else{
                DEBUG_PRINT(DEBUG_TRACE, "\nRx waiting timeout. DONE\n");
                response["result"]="FAILURE";
                response["details"]="Rx waiting timeout";
                DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_Tx --> Exit\n");
            }
        }
        else{
            sprintf(details, "%s: %s call failed",txStatus,txMethod);
            response["result"]="FAILURE";
            response["details"]=details;
            DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_Tx --> Exit\n");
        }
    }
    else {
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecTx call failed\n");
        response["result"]="FAILURE";
        response["details"]="HdmiCecTx call failed";
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_Tx --> Exit\n");
    }
    clearCECFlagsAndFrameInfo();
    return;
}


/***************************************************************************
 *Function name  : HdmicecHal_TxAsync
 *Description    : This function is to invoke HdmiCecTxAsync API to transmit
                   CEC frame asynchronously and get trasmission status and
                   received frame using Tx and Rx call backs
 *****************************************************************************/
void HdmicecHalAgent::HdmicecHal_TxAsync(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_TxAsync --->Entry\n");
    if(&req["opcode"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Opcode Frame";
        return;
    }
    if(&req["receive_frames"] == NULL)
    {
        response["result"]="FAILURE";
        response["details"]="No Input Receive Frame Flag";
        return;
    }
    char details[500];
    char frame[200];

    /* check whether CEC header is provided or not. If header is
       not provided generated header with src and destination
       logical addresses
    */
    if(&req["header"] != NULL && strlen(req["header"].asCString()) > 0){
        strcpy(frame,req["header"].asCString());
        DEBUG_PRINT(DEBUG_TRACE, "Using provided CEC header\n");
    }
    else{
         generate_cec_header(frame);
         if (cec_header_flag != 0){
             response["result"]="FAILURE";
             response["details"]="Unable to generate Header Frame";
             return;
         }
    }
    strcat(frame," ");
    strcat(frame,req["opcode"].asCString());

    /* If a opcode is intended for sending purpose only, then
       receive_frames should be set as 0. If a opcode is expected
       to receive cec frames from target device, then receive_frames
       should be set as 1. By default its set as 1 in TM
    */
    cec_receive_flag = req["receive_frames"].asInt();

    // convert string CEC frame to array & display
    get_cec_frame_tx(frame);
    disp_cec_frame((unsigned char*)cec_frame_tx,cec_frame_size_tx);
    sprintf(txMethod,"HdmiCecTxAsync");
    DEBUG_PRINT(DEBUG_TRACE, "Receive CEC Frame : %s\n",cec_receive_flag?"TRUE":"FALSE");

    int ret = HdmiCecTxAsync(driverHandle, cec_frame_tx, cec_frame_size_tx);
    DEBUG_PRINT(DEBUG_TRACE, "Ret: %x HdmiCecTxAsync call DONE\n",ret);
    if (ret == HDMI_CEC_IO_SUCCESS ){
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecTxAsync call success\n");
        std::unique_lock<std::mutex> m(m_idle);
        if (m_cv.wait_for(m, std::chrono::seconds(TIMEOUT), []{ return received_status == 1; })){
            DEBUG_PRINT(DEBUG_TRACE, "Finished Rx waiting. DONE\n");
            messageDecoder();

            get_cec_frame_rx_str((unsigned char*)cec_frame_rx,cec_frame_size_rx);
            sprintf(details, "Received CEC Frame: %s;Header: %s;Result: %s",cec_frame_rx_str.c_str(),cec_frame_header.c_str(),cec_frame_result.c_str());
            response["result"]="SUCCESS";
            response["details"]=details;
            DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_TxAsync --> Exit\n");
        }
        else{
            DEBUG_PRINT(DEBUG_TRACE, "\nRx waiting timeout. DONE\n");
            if (transmit_status && cec_receive_flag == false){
                DEBUG_PRINT(DEBUG_TRACE, "CEC Frame Transmitted Successfully !!\n");
                response["result"]="SUCCESS";
                response["details"]="CEC Frame Transmitted Successfully";
                DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_Tx --> Exit\n");
            }
            else if (transmit_status && cec_receive_flag == true){
                response["result"]="FAILURE";
                response["details"]="Rx waiting timeout";
                DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_TxAsync --> Exit\n");
            }
            else{
                sprintf(details, "%s: %s call failed",txStatus,txMethod);
                response["result"]="FAILURE";
                response["details"]=details;
                DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_TxAsync --> Exit\n");
            }
        }
    }
    else {
        DEBUG_PRINT(DEBUG_TRACE, "HdmiCecTxAsync call failed\n");
        response["result"]="FAILURE";
        response["details"]="HdmiCecTxAsync call failed";
        DEBUG_PRINT(DEBUG_TRACE, "HdmicecHal_TxAsync --> Exit\n");
    }
    clearCECFlagsAndFrameInfo();
    return;
}


/**************************************************************************
Function Name   : cleanup
Arguments       : NULL
Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool HdmicecHalAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Exit\n");
    return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject
Arguments     : Input argument is HdmicecHalAgent Object
Description   : This function will be used to destory the HdmicecHalAgent object.
**************************************************************************/
extern "C" void DestroyObject(HdmicecHalAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying HdmicecHalAgent Agent object\n");
        delete stubobj;
}

