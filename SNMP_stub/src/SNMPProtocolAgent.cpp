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

#include "SNMPProtocolAgent.h"

#define BUFFERMEMSIZE 512
static std::string Command;

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string SNMPProtocolAgent::testmodulepre_requisites()
{
	return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool SNMPProtocolAgent::testmodulepost_requisites()
{
	return true;
}

/**************************************************************************
Function name : SNMPProtocolAgent::initialize

Arguments     : Input arguments are Version string and SNMPProtocolAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/
bool SNMPProtocolAgent::initialize(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE, "SNMPProtocolAgent Initialize----->Entry\n");
	DEBUG_PRINT(DEBUG_TRACE, "SNMPProtocolAgent Initialize----->Exit\n");

	return TEST_SUCCESS;
}

/**************************************************************************
 *
 * Function Name : SNMPProtocolAgent::GetCommString
 * Descrption    : This api is to retrieve the community string value
 *
 * @param [out] response- filled with SUCCESS or FAILURE and community string.
 ***************************************************************************/
void SNMPProtocolAgent::GetCommString(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"GetCommString ------> Entry\n");
    char comm_string[50] = {'\0'};
    std::string folder_path;
    std::string TDKPath;
    char command[200]={'\0'};
    FILE *fp = NULL;
    /* Extracting TDK path*/
    TDKPath = getenv ("TDK_PATH");
    folder_path.append(TDKPath);
    folder_path.append("/");
    folder_path.append("tdk_platform.properties");
    printf("Folder path is %s\n",folder_path.c_str());
    sprintf(command,"cat %s | grep COMMUNITY | cut -d = -f2",folder_path.c_str());
    fp = popen(command, "r");
    if (fp == NULL)
    {
        response["result"] = "FAILURE";
        response["details"] = "popen() failure";
        DEBUG_PRINT(DEBUG_ERROR, "popen() failure\n");

        return;
    }
    /*copy the response to a buffer */
    while (fgets(comm_string, sizeof(comm_string)-1, fp) != NULL)
    {
       strtok(comm_string, "\n");
       printf("community string is %s \n",comm_string);
    }
    response["result"] = "SUCCESS";
    response["details"] = comm_string;

    DEBUG_PRINT(DEBUG_TRACE,"GetCommString ------> Exit");
    return;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "SNMPProtocolAgent".
 **************************************************************************/

extern "C" SNMPProtocolAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
	DEBUG_PRINT(DEBUG_TRACE, "Creating SNMP Protocol Agent Object\n");

	return new SNMPProtocolAgent(ptrtcpServer);
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool SNMPProtocolAgent::cleanup(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
	DEBUG_PRINT(DEBUG_TRACE, "cleaningup done\n");
	return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is SNMPProtocolAgent Object

Description   : This function will be used to destory the SNMPProtocolAgent object.
 **************************************************************************/
extern "C" void DestroyObject(SNMPProtocolAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying SNMPProtocolAgent object\n");
	delete stubobj;
}

