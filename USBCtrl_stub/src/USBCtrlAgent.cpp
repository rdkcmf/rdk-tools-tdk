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

#include "USBCtrlAgent.h"
#include <sys/socket.h>



/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string USBCtrlAgent::testmodulepre_requisites()
{
	DEBUG_PRINT (DEBUG_TRACE, "USBCtrl testmodule pre_requisites --> Entry\n");
	
	DEBUG_PRINT (DEBUG_TRACE, "USBCtrl testmodule pre_requisites --> Exit\n");
	
	return "SUCCESS";

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool USBCtrlAgent::testmodulepost_requisites()
{
	DEBUG_PRINT (DEBUG_TRACE, "USBCtrl testmodule post_requisites --> Entry\n");

	DEBUG_PRINT (DEBUG_TRACE, "USBCtrl testmodule post_requisites --> Exit\n");

	return TEST_SUCCESS;

}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "USBCtrlAgent".
**************************************************************************/

extern "C" USBCtrlAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new USBCtrlAgent(ptrtcpServer);
}

/**************************************************************************
Function name : USBCtrlAgent::initialize

Arguments     : Input arguments are Version string and USBCtrlAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool USBCtrlAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT (DEBUG_TRACE, "USBCtrlAgent Initialization Entry\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : USBCtrl_Init()

Arguments     : Input argument None.
                Output argument is initialization status 

Description   : Initializes the USBCtrl 
**************************************************************************/
void USBCtrlAgent::USBCtrl_Init(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "USBCtrl_Init--->Entry\n");
	
    	try 
	{
		int result = rusbCtrl_init();
		printf("Init Status: %d\n", result);

		if (!result)
		{
        	    	DEBUG_PRINT (DEBUG_ERROR, "USBCtrl initialized\n");
			response["result"] = "SUCCESS";
        	    	response["details"] = "USBCtrl initialized";
	        }
        	else 
		{
        	    	DEBUG_PRINT (DEBUG_ERROR, "USBCtrl initialization failed\n");
			response["result"] = "FAILURE";
        	    	response["details"] = "USBCtrl initialization failed";
        	}
    	}
   	catch(...) 
	{

    		DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in USBCtrl_init\n");

		response["details"]= "Exception Caught in USBCtrl_Init";
	        response["result"]= "FAILURE";
    	}

    	DEBUG_PRINT(DEBUG_TRACE, "USBCtrl_Init -->Exit\n");
    	return;
}


/**************************************************************************
Function name : USBCtrl_Term()

Arguments     : Input argument None.
                Output argument is the termination status

Description   : Terminates the USBCtrl 
**************************************************************************/
void USBCtrlAgent::USBCtrl_Term(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "USBCtrl_Term--->Entry\n");
	
    	try 
	{
		int result = rusbCtrl_term();
                printf("Term Status: %d\n", result);

                if (!result)
                {
                        DEBUG_PRINT (DEBUG_ERROR, "USBCtrl terminated\n");
                        response["result"] = "SUCCESS";
                        response["details"] = "USBCtrl terminated";
                }
                else
                {
                        DEBUG_PRINT (DEBUG_ERROR, "USBCtrl termination failed\n");
                        response["result"] = "FAILURE";
                        response["details"] = "USBCtrl termination failed";
                }

    	}
   	catch(...) 
	{

    		DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in USBCtrl_Term\n");

		response["details"]= "Exception Caught in USBCtrl_Term";
	        response["result"]= "FAILURE";
    	}

    	DEBUG_PRINT(DEBUG_TRACE, "USBCtrl_Term -->Exit\n");
    	return;
}

/***************************************************************************
 * Function name : USBCtrl_ExecuteCmd()
 *
 * Arguments     : Input arguments are command to execute in box
 *
 * Description   : This will execute linux commands in box
 * ***************************************************************************/
void USBCtrlAgent::USBCtrl_ExecuteCmd(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "USBCtrl_ExecuteCmd ---> Entry\n");
        string fileinfo = request["command"].asCString();
        FILE *fp = NULL;
        char readRespBuff[BUFF_LENGTH];
        /*Frame the command  */
        string path = "";
        path.append(fileinfo);
        DEBUG_PRINT(DEBUG_TRACE, "Command Request Framed: %s\n",path.c_str());
        fp = popen(path.c_str(),"r");
        /*Check for popen failure*/
        if(fp == NULL)
        {
                response["result"] = "FAILURE";
                response["details"] = "popen() failure";
                DEBUG_PRINT(DEBUG_ERROR, "popen() failure\n");
                return;
        }
        /*copy the response to a buffer */
        while(fgets(readRespBuff,sizeof(readRespBuff),fp) != NULL)
        {
		DEBUG_PRINT(DEBUG_TRACE, "Command Response:\n");
		cout<<"readRespBuff:"<<readRespBuff<<endl;
        }
        pclose(fp);
	string respResult(readRespBuff);
        DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",respResult.c_str());
        response["result"] = "SUCCESS";
        response["details"] = respResult;
        DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
        DEBUG_PRINT(DEBUG_TRACE, "USBCtrl_ExecuteCmd -->Exit\n");
        return;
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool USBCtrlAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is USBCtrl Agent Object

Description   : This function will be used to destory the MediaUtilsAgent object.
**************************************************************************/
extern "C" void DestroyObject(USBCtrlAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying USBCtrl Agent object\n");
        delete stubobj;
}

