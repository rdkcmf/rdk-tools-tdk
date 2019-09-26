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

#include "AudioCaptureMgrAgent.h"
#include <sys/socket.h>

#ifdef __cplusplus
extern "C" {
#include "libIBus.h"
#include "libIARMCore.h"
}
#endif

std::string filename;

void * readThread(void * data)
{
	std::string socketPath = *(static_cast <std::string *> (data));
	if(socketPath.empty())
	{
		DEBUG_PRINT(DEBUG_LOG,"Read thread returning as socket path is empty\n");
		return NULL;
	}
	DEBUG_PRINT(DEBUG_LOG,"Connecting to socket %s\n", socketPath.c_str());
	struct sockaddr_un addr;
	addr.sun_family = AF_UNIX;
	strncpy(addr.sun_path, socketPath.c_str(), (socketPath.size() + 1));
	int readfd = socket(AF_UNIX, SOCK_STREAM, 0);
	if(0 > readfd)
	{
		DEBUG_PRINT(DEBUG_LOG,"Couldn't create read socket\n");
		return NULL;
	}
	if(0 != connect(readfd, (const struct sockaddr *) &addr, sizeof(addr)))
	{
		DEBUG_PRINT(DEBUG_LOG,"Couldn't connect to the path\n");
		perror("read_thread");
		close(readfd);
		return NULL;
	}
	DEBUG_PRINT(DEBUG_LOG,"Connection established\n");
	unsigned int recvdBytes = 0;
	char buffer[1024];
	
	std::ofstream file_dump(filename.c_str(), std::ios::binary);
	while(true)
	{
		int ret = read(readfd, buffer, 1024);
		if(0 == ret)
		{
			DEBUG_PRINT(DEBUG_LOG,"Zero bytes read\n");
			break;
		}
		else if(0 > ret)
		{
			DEBUG_PRINT(DEBUG_LOG,"Error reading from socket. Exiting\n");
			perror("read error");
			break;
		}
		if((1024*1024*2) > recvdBytes) //Write up to 2 MB to a file
		{
			file_dump.write(buffer, ret);	
		}
		recvdBytes += ret;
	}
	
	close(readfd);
	DEBUG_PRINT(DEBUG_LOG,"Number of Bytes read %d\n", recvdBytes);
	
	file_dump.seekp(0, std::ios_base::end);
	DEBUG_PRINT(DEBUG_LOG,"%d Bytes written to file\n", file_dump.tellp());
	DEBUG_PRINT(DEBUG_LOG,"Exiting read thread ***********\n");
	return NULL;
}

void connectAndReadData(std::string &socketPath)
{
	pthread_t thread;
	int ret = pthread_create(&thread, NULL, readThread, (void *) &socketPath);
	if(0 == ret)
	{
		DEBUG_PRINT(DEBUG_LOG, "Successfully launched read thread.\n");
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG, "Failed to launched read thread.\n");
	}
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string AudioCaptureMgrAgent::testmodulepre_requisites()
{
	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr testmodule pre_requisites --> Entry\n");
	
	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr testmodule pre_requisites --> Exit\n");
	
	return "SUCCESS";

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool AudioCaptureMgrAgent::testmodulepost_requisites()
{
	DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule post_requisites --> Entry\n");

	DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule post_requisites --> Exit\n");

	return TEST_SUCCESS;

}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "AudioCaptureMgrAgent".
**************************************************************************/

extern "C" AudioCaptureMgrAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new AudioCaptureMgrAgent(ptrtcpServer);
}

/**************************************************************************
Function name : AudioCaptureMgrAgent::initialize

Arguments     : Input arguments are Version string and AudioCaptureMgrAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool AudioCaptureMgrAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr Initialization Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr Initialization Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : AudioCaptureMgr_SessionOpen

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the session id

Description   : Opens the AudioCaptureMgr session and retrieve the session id.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_SessionOpen(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_SessionOpen --->Entry\n");
	
    	try 
	{
	        IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
		iarmbus_acm_arg_t param;
		char sessionId[STR_LEN_20] = {'\0'};

	        //memset (&param, 0, sizeof(param));
		param.details.arg_open.source = 0;
		param.details.arg_open.output_type = REALTIME_SOCKET;
		iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_OPEN, (void *) &param, sizeof(param));

		if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
		{
        	    	DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to open AudioCaptureMgr session failed\n");
			response["result"] = "FAILURE";
        	    	response["details"] = "IARM_Bus_Call to open AudioCaptureMgr session failed";
	        }
        	else 
		{
	            	DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to open AudioCaptureMgr session successful\n");
			session = param.session_id;
        	    	response["result"] = "SUCCESS";
			sprintf(sessionId,"%d",param.session_id);
        		response["details"] = sessionId;
        	}
    	}
   	catch(...) 
	{

    		DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_SessionOpen\n");

		response["details"]= "Exception Caught in AudioCaptureMgr_SessionOpen";
	        response["result"]= "FAILURE";
    	}

    	DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_SessionOpen -->Exit\n");
    	return;
}

/**************************************************************************
Function name : AudioCaptureMgr_SessionClose

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE"

Description   : Closes the AudioCaptureMgr session
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_SessionClose(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_SessionClose --->Entry\n");
	
    	try 
	{
	        IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
		iarmbus_acm_arg_t param;

		param.session_id = session;
		iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_CLOSE, (void *) &param, sizeof(param));

		if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
		{
        	    	DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to close AudioCaptureMgr session failed\n");
			response["result"] = "FAILURE";
        	    	response["details"] = "IARM_Bus_Call to close AudioCaptureMgr session failed";
	        }
        	else 
		{

	            	DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to close AudioCaptureMgr session successful\n");

        	    	response["result"] = "SUCCESS";
			session = -1;
			socketPath.clear();
       		        response["details"] = "Session close procedure complete";
        	}
    	}
   	catch(...) 
	{

    		DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_SessionClose\n");

		response["details"]= "Exception Caught in AudioCaptureMgr_SessionClose";
	        response["result"]= "FAILURE";
    	}

    	DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_SessionClose -->Exit\n");
    	return;
}

/**************************************************************************
Function name : AudioCaptureMgr_GetSessionDetails

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the session details.

Description   : Retrieve the session details.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_GetSessionDetails(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_GetSessionDetails --->Entry\n");

	char sessionDetails[STR_LEN_50] = {'\0'};	
	if (session == -1)
	{
            	DEBUG_PRINT (DEBUG_ERROR, "AudioCaptureMgr session not open\n");
		response["result"] = "FAILURE";
	}
	else
	{
            	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr session details retrieved successfully\n");
       	    	response["result"] = "SUCCESS";
		sprintf(sessionDetails,"%d",session);
        }
        
	response["details"] = sessionDetails;

    	DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_GetSessionDetails -->Exit\n");
    	return;
}

/**************************************************************************
Function name : AudioCaptureMgr_GetDefaultAudioProperties

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and default audio 
		properties.

Description   : Retrieve the default audio properties.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_GetDefaultAudioProperties(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_GetDefaultAudioProperties --->Entry\n");
	
	try
        {
                IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
                iarmbus_acm_arg_t param;
		char audioProperties[STR_LEN_100] = {'\0'};
		string validity = req["session"].asCString();

		if(validity == "VALID")
                {	
                	param.session_id = session;
                }
		else if(validity == "INVALID")
		{
                	param.session_id = -1;
		}
		else
		{
			response["result"]="FAILURE";
                        response["details"]="Parameter not correct";
            		DEBUG_PRINT (DEBUG_ERROR, "Parameter not correct\n");
                        return;
		}
                iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_GET_DEFAULT_AUDIO_PROPS, (void *) &param, sizeof(param));

                if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
                {
                        DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to get default audio properties failed\n");
                        response["result"] = "FAILURE";
                        response["details"] = "IARM_Bus_Call to get default audio properties failed";
                }
                else
                {

                        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to get default audio proprties successful\n");
			sprintf (audioProperties,
	                "{\'Format\': 0x%x, \'DelayComp\': %d, \'FifoSize\': %d, \'Threshold\': %d}",
			param.details.arg_audio_properties.format,
                        param.details.arg_audio_properties.delay_compensation_ms,
                        param.details.arg_audio_properties.fifo_size,
                        param.details.arg_audio_properties.threshold);

                        props = param.details.arg_audio_properties; 

			response["result"] = "SUCCESS";
                        response["details"] = audioProperties;
                }
        }
        catch(...)
        {

                DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_GetDefaultAudioProperties\n");

                response["details"]= "Exception Caught in AudioCaptureMgr_GetDefaultAudioProperties";
                response["result"]= "FAILURE";
        }


    	DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_GetDefaultAudioProperties -->Exit\n");
    	return;
}

/**************************************************************************
Function name : AudioCaptureMgr_GetAudioProperties

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and audio 
		properties.

Description   : Retrieve the audio properties.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_GetAudioProperties(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_GetAudioProperties --->Entry\n");
	
	try
        {
                IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
                iarmbus_acm_arg_t param;
		char audioProperties[STR_LEN_100] = {'\0'};
		string validity = req["session"].asCString();

                if(validity == "VALID")
                {
                        param.session_id = session;
                }
                else if(validity == "INVALID")
                {
                        param.session_id = -1;
                }
                else
                {
                        response["result"]="FAILURE";
                        response["details"]="Parameter not correct";
                        DEBUG_PRINT (DEBUG_ERROR, "Parameter not correct\n");
                        return;
                }

                iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_GET_AUDIO_PROPS, (void *) &param, sizeof(param));

                if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
                {
                        DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to get audio properties failed\n");
                        response["result"] = "FAILURE";
                        response["details"] = "IARM_Bus_Call to get audio properties failed";
                }
                else
                {

                        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to get audio proprties successful\n");
			sprintf (audioProperties,
	                "{\'Format\': 0x%x, \'DelayComp\': %d, \'FifoSize\': %d, \'Threshold\': %d}",
			param.details.arg_audio_properties.format,
                        param.details.arg_audio_properties.delay_compensation_ms,
                        param.details.arg_audio_properties.fifo_size,
                        param.details.arg_audio_properties.threshold);
                       
			props = param.details.arg_audio_properties;

			response["result"] = "SUCCESS";
                        response["details"] = audioProperties;
                }
        }
        catch(...)
        {

                DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_GetAudioProperties\n");

                response["details"]= "Exception Caught in AudioCaptureMgr_GetAudioProperties";
                response["result"]= "FAILURE";
        }


    	DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_GetAudioProperties -->Exit\n");
    	return;
}

/**************************************************************************
Function name : AudioCaptureMgr_SetAudioProperties

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and audio
                properties.

Description   : Sets the audio properties.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_SetAudioProperties(IN const Json::Value& req, OUT Json::Value& response) {

        DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_SetAudioProperties --->Entry\n");


        try
        {
                IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
                iarmbus_acm_arg_t param;
                char audioProperties[STR_LEN_100] = {'\0'};
		string validity = req["session"].asCString();

		if(&req["delay"]==NULL && &req["fifoSize"]==NULL && &req["threshold"]==NULL)
	        {
        	        response["result"]="FAILURE";
                	response["details"]="Audio property values not available to set";
	                return;
        	}
		
		if(validity == "VALID")
                {
                        param.session_id = session;
                }
                else if(validity == "INVALID")
                {
                        param.session_id = -1;
                }
                else
                {
                        response["result"]="FAILURE";
                        response["details"]="Parameter not correct";
                        DEBUG_PRINT (DEBUG_ERROR, "Parameter not correct\n");
                        return;
                }

		param.details.arg_audio_properties = props;
		if(req["delay"].asInt() != -1)
		{
			printf("IN DELAY\n");
			param.details.arg_audio_properties.delay_compensation_ms = req["delay"].asInt();
		}
		if(req["fifoSize"].asInt() != -1)
		{
			printf("IN FIFO\n");
			printf("%d\n",  req["fifoSize"].asInt());
			param.details.arg_audio_properties.fifo_size = req["fifoSize"].asInt();
		}
		if(req["threshold"].asInt() != -1)
		{
			printf("IN THRESHOLD\n");

			param.details.arg_audio_properties.threshold = req["threshold"].asInt();
		}
			
                iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_SET_AUDIO_PROPERTIES, (void *) &param, sizeof(param));

                if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
                {
                        DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to set audio properties failed\n");
                        response["result"] = "FAILURE";
                        response["details"] = "IARM_Bus_Call to set audio properties failed";
                }
                else
                {

                        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to set audio properties successful\n");
                        response["result"] = "SUCCESS";
                        response["details"] = "Audio properties set successfully";
                }
        }
        catch(...)
        {

                DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_SetAudioProperties\n");

                response["details"]= "Exception Caught in AudioCaptureMgr_SetAudioProperties";
                response["result"]= "FAILURE";
        }


        DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_SetAudioProperties -->Exit\n");
        return;
}

/**************************************************************************
Function name : AudioCaptureMgr_GetOutputProperties

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and output
                properties.

Description   : Retrieve the output properties.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_GetOutputProperties(IN const Json::Value& req, OUT Json::Value& response) {

        DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_GetOutputProperties --->Entry\n");

        try
        {
                IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
                iarmbus_acm_arg_t param;
                char outputProperties[STR_LEN_20] = {'\0'};
		string validity = req["session"].asCString();

                if(validity == "VALID")
                {
                        param.session_id = session;
                }
                else if(validity == "INVALID")
                {
                        param.session_id = -1;
                }
                else
                {
                        response["result"]="FAILURE";
                        response["details"]="Parameter not correct";
                        DEBUG_PRINT (DEBUG_ERROR, "Parameter not correct\n");
                        return;
                }

                iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_GET_OUTPUT_PROPS, (void *) &param, sizeof(param));

                if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
                {
                        DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to get output properties failed\n");
                        response["result"] = "FAILURE";
                        response["details"] = "IARM_Bus_Call to get output properties failed";
                }
                else
                {

                        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to get output proprties successful\n");
			socketPath = std::string(param.details.arg_output_props.output.file_path);
                        sprintf(outputProperties, "%s", socketPath.c_str());

                        response["result"] = "SUCCESS";
                        response["details"] = outputProperties;
                }
        }
        catch(...)
        {

                DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_GetOutputProperties\n");

                response["details"]= "Exception Caught in AudioCaptureMgr_GetOutputProperties";
                response["result"]= "FAILURE";
        }


        DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_GetOutputProperties -->Exit\n");
        return;
}

/**************************************************************************
Function name : AudioCaptureMgr_Start

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE"

Description   : Starts the AudioCaptureMgr.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_Start(IN const Json::Value& req, OUT Json::Value& response) {

    	DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_Start --->Entry\n");
	
    	try 
	{
	        IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
		iarmbus_acm_arg_t param;
		if(socketPath.empty())
		{
        	    	DEBUG_PRINT (DEBUG_ERROR, "Socket path is empty\n");
        	        response["result"]="FAILURE";
                	response["details"]="Socket path is empty";
	                return;

		}

		char cmdstring[200] = {'\0'};
		std::string g_tdkPath = getenv("TDK_PATH");
        	filename = g_tdkPath + "tmp";
		DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to start AudioCaptureMgr successful\n");
		sprintf (cmdstring, "mkdir -p %s", filename.c_str());
		system(cmdstring);
		filename += "/acm_ipout_dump";
		DEBUG_PRINT(DEBUG_LOG,"Filename: %s\n", filename.c_str());

		connectAndReadData(socketPath);
		param.session_id = session;
		iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_START, (void *) &param, sizeof(param));

		if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
		{
        	    	DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to start AudioCaptureMgr failed\n");
			response["result"] = "FAILURE";
        	    	response["details"] = "IARM_Bus_Call to start AudioCaptureMgr failed";
	        }
        	else 
		{

        	    	response["result"] = "SUCCESS";
        		response["details"] = filename;
        	}
    	}
   	catch(...) 
	{

    		DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_Start\n");

		response["details"]= "Exception Caught in AudioCaptureMgr_Start";
	        response["result"]= "FAILURE";
    	}

    	DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_Start -->Exit\n");
    	return;
}

/**************************************************************************
Function name : AudioCaptureMgr_Stop

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE"

Description   : Stops the AudioCaptureMgr.
**************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_Stop(IN const Json::Value& req, OUT Json::Value& response) {

        DEBUG_PRINT (DEBUG_TRACE, "AudioCaptureMgr_Stop --->Entry\n");

        try
        {
                IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
                iarmbus_acm_arg_t param;
                
		param.session_id = session;
                iarmResult = IARM_Bus_Call(IARMBUS_AUDIOCAPTUREMGR_NAME, IARMBUS_AUDIOCAPTUREMGR_STOP, (void *) &param, sizeof(param));

                if (iarmResult != IARM_RESULT_SUCCESS || param.result !=0)
                {
                        DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to stop AudioCaptureMgr failed\n");
                        response["result"] = "FAILURE";
                        response["details"] = "IARM_Bus_Call to stop AudioCaptureMgr failed";
                }
                else
                {
                        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to stop AudioCaptureMgr successful\n");

                        response["result"] = "SUCCESS";
                        response["details"] = "AudioCaptureMgr stop procedure complete";
                }
        }
        catch(...)
        {

                DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in AudioCaptureMgr_Stop\n");

                response["details"]= "Exception Caught in AudioCaptureMgr_Stop";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_Stop -->Exit\n");
        return;
}

/***************************************************************************
 * Function name : AudioCaptureMgr_ExecuteCmd()
 *
 * Arguments     : Input arguments are command to execute in box
 *
 * Description   : This will execute linux commands in box
 * ***************************************************************************/
void AudioCaptureMgrAgent::AudioCaptureMgr_ExecuteCmd(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_ExecuteCmd ---> Entry\n");
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
        DEBUG_PRINT(DEBUG_TRACE, "AudioCaptureMgr_ExecuteCmd -->Exit\n");
        return;
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool AudioCaptureMgrAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is MediaUtilsAgent Object

Description   : This function will be used to destory the MediaUtilsAgent object.
**************************************************************************/
extern "C" void DestroyObject(AudioCaptureMgrAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying AudioCaptureMgr Agent object\n");
        delete stubobj;
}

