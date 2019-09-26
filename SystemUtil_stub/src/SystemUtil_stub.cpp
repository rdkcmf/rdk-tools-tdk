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

#include "SystemUtil_stub.h"

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string SystemUtilAgent::testmodulepre_requisites()
{
	return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool SystemUtilAgent::testmodulepost_requisites()
{
	return true;
}

/**************************************************************************
Function name : SystemUtilAgent::initialize

Arguments     : Input arguments are Version string and SystemUtilAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/
bool SystemUtilAgent::initialize(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent Initialize----->Entry\n");
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent Initialize----->Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_GetifconfigValue

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_GetifconfigValue(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_GetifconfigValue -->Entry\n");

	string interface = req["interface"].asCString();
	
	FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH] = { '\0' };
	string popenBuff;
	/*Frame the command  */
	string path = IFCONFIG;
	path.append(interface);

	DEBUG_PRINT(DEBUG_TRACE, "ifconfig Request Framed: %s\n",path.c_str());

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
		DEBUG_PRINT(DEBUG_TRACE, "ifconfig Response:\n");
		cout<<readRespBuff<<endl;
		popenBuff += readRespBuff;
	}

	pclose(fp);	

	string respResult(readRespBuff);
	DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",popenBuff.c_str());
	response["result"] = "SUCCESS";
	response["details"] = popenBuff;
	DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_GetifconfigValue -->Exit\n");
	return;

}

/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_GetpingValue

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_GetpingValue(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_GetpingValue -->Entry\n");

        FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH] = { '\0' };
        string address  = req["address"].asCString();
        bool ping6enabled = req["ping6enable"].asInt();
	string path;
	string popenBuff;
        if (true == ping6enabled)
	{
		/*Frame the command  */
	        path = PING6;
	}
	else
	{
		/*Frame the command  */
	        path = PING;
	}

        if (address == "CMTS")
        {
                /*Frame the command  */
		path.append(CMTS);
        }
        else
        {
                /*Frame the command  */
                path.append(address);
        }

        DEBUG_PRINT(DEBUG_TRACE, "Ping Request Framed: %s\n",path.c_str());

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
                DEBUG_PRINT(DEBUG_TRACE, "Ping Response:\n");
                cout<<readRespBuff<<endl;
		popenBuff += readRespBuff;
        }

        pclose(fp);

        string respResult(readRespBuff);
        DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",popenBuff.c_str());
        response["result"] = "SUCCESS";
        response["details"] = popenBuff;
        DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_GetpingValue -->Exit\n");
        return;

}

/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_Getrouteinfo

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_GetrouteInfo(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_GetrouteInfo -->Entry\n");

        FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH] = { '\0' };
        bool ip6enabled = req["ip6enable"].asInt();
	string path;
	string popenBuff;

        if (true == ip6enabled)
	{
		/*Frame the command  */
	        path = IP6CMD;
	}
	else
	{
		/*Frame the command  */
	        path = IPCMD;
	}

	/*Frame the command  */
	path.append(ROUTE);

	DEBUG_PRINT(DEBUG_TRACE, "Route Request Framed: %s\n",path.c_str());

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
                DEBUG_PRINT(DEBUG_TRACE, "Route Response:\n");
                cout<<readRespBuff<<endl;
		popenBuff += readRespBuff;
        }

        pclose(fp);

        string respResult(readRespBuff);
        DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",popenBuff.c_str());
        response["result"] = "SUCCESS";
        response["details"] = popenBuff;
        DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_GetrouteInfo -->Exit\n");
        return;

}

/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_TouchFile

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_TouchFile(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_TouchFile -->Entry\n");

	string fileinfo = req["fileinfo"].asCString();
	
	FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH] = { '\0' };

	/*Frame the command  */
	string path = TOUCH;
	path.append(fileinfo);

	DEBUG_PRINT(DEBUG_TRACE, "touch Request Framed: %s\n",path.c_str());

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
		DEBUG_PRINT(DEBUG_TRACE, "Touch Response:\n");
		cout<<readRespBuff<<endl;
	}

	pclose(fp);	

	string respResult(readRespBuff);
	DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",respResult.c_str());
	response["result"] = "SUCCESS";
	response["details"] = respResult;
	DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_TouchFile -->Exit\n");
	return;

}


/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_ExecuteCmd

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_ExecuteCmd(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_ExecuteCmd -->Entry\n");

	string fileinfo = req["command"].asCString();
	
	FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH] = { '\0' };

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
		cout<<readRespBuff<<endl;
	}

	pclose(fp);	

	string respResult(readRespBuff);
	DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",respResult.c_str());
	response["result"] = "SUCCESS";
	response["details"] = respResult;
	DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_ExecuteCmd -->Exit\n");
	return;

}


/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_Getoutput_json_file

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_Getoutput_json_file(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_Getoutput_json_file -->Entry\n");

        FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH] = { '\0' };
	string path = "cat $XDISCOVERY_PATH/xdiscovery.conf|grep outputJsonFile=|grep -v \"#\"|awk -F \"=\" '{print $2}'";
	string popenBuff;


	DEBUG_PRINT(DEBUG_TRACE, "Extracting output.json file location Request Framed: %s\n",path.c_str());

        fp = popen(path.c_str(),"r");

        /*Check for popen failure*/
        if(fp == NULL)
        {
                response["result"] = "FAILURE";
                response["details"] = "popen() failure";
                DEBUG_PRINT(DEBUG_ERROR, "popen() failure for : %s\n",path.c_str());

                return;
        }

        /*copy the response to a buffer */
        while(fgets(readRespBuff,sizeof(readRespBuff),fp) != NULL)
        {
		popenBuff += readRespBuff;
        }

        pclose(fp);

        DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",popenBuff.c_str());
        response["result"] = "SUCCESS";
        response["details"] = popenBuff;
        response["log-path"] = popenBuff;
        DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_Getoutput_json_file -->Exit\n");
        return;

}

/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_ExecuteBinary

Description   : This method execute the binary and redirect logs to the specified file .
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_ExecuteBinary(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_ExecuteBinary -->Entry\n");
        string scriptFile = req["shell_script"].asCString();
        string logFile = req["log_file"].asCString();
        string toolPath = req["tool_path"].asCString();
        string ExecutionLogFile,ShellScript,testenvPath;
        int Status;
        try
        {
                pid_t idChild = vfork();
                if(idChild == 0)
                {
                      testenvPath = getenv ("TDK_PATH");
                      ExecutionLogFile.append(testenvPath);
                      ExecutionLogFile.append("/");
                      ExecutionLogFile.append(logFile);
                      ShellScript.append(testenvPath);
                      ShellScript.append("/");
                      ShellScript.append(scriptFile);
                      int fd = open(ExecutionLogFile.c_str(), O_WRONLY|O_CREAT, 0666);
                      dup2(fd, 1);
                      close(fd);
                      execlp("/bin/sh","sh",ShellScript.c_str(),toolPath.c_str(),NULL);
                }
                else if(idChild <0)
                {
                    DEBUG_PRINT(DEBUG_ERROR,"\nFork failed");
                    response["result"]="FAILURE";
                    response["result"]="Binary Execution Failed";
                }
                else
                {
                   waitpid(idChild,&Status,0);
                   DEBUG_PRINT(DEBUG_LOG, "Binary Execution success\n");
                   response["result"]="SUCCESS";
                   response["details"]="Binary Execution Success";
                }

        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured while binary execution\n");
                response["result"]="FAILURE";
                response["details"]="Binary Execution Failed";
        }

        DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_ExecuteBinary -->Exit\n");
        return;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "SystemUtilAgent".
 **************************************************************************/

extern "C" SystemUtilAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
	DEBUG_PRINT(DEBUG_TRACE, "Creating SysUtil Agent Object\n");

	return new SystemUtilAgent(ptrtcpServer);
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool SystemUtilAgent::cleanup(IN const char* szVersion)
{
        DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
	return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is SystemUtilAgent Object

Description   : This function will be used to destory the SystemUtilAgent object.
 **************************************************************************/
extern "C" void DestroyObject(SystemUtilAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying SystemUtilAgent object\n");
	delete stubobj;
}
