/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2019 RDK Management
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

#include "RDKLoggerAgent.h"

bool b_rdk_logger_enabled = false;
string g_tdkPath = getenv("TDK_PATH");
string tdkDebugIniFile = g_tdkPath + "/" + DEBUG_CONF;

/* Helper functions */

/**
 * Converts a log level name to the correspodning log level enum value.
 *
 * @param name Log level name, which must be uppercase.
 * @param Corresponding enumeration value or -1 on error.
 */
static int logNameToEnum(const char *name)
{
    int i = 0;
    while (i < ENUM_RDK_LOG_COUNT)
    {
        if (strcmp(name, rdk_logLevelStrings[i]) == 0)
        {
            return i;
        }
        i++;
    }

    return -1;
}

/**
 * Checks if a particular log is enabled for a module.
 *
 * @param module Module in which this message belongs to.
 * @param level  Log level of the log message Log level of the log message supported for a module
 * @return     	 true if log level is supported for a module
 *		 false if log level is not supported for a module
 */

bool dbgFinder( const char *module, const char *level)
{
    string    line;
    ifstream  debugFile;

    debugFile.open(tdkDebugIniFile);
    if(debugFile.is_open())
    {
        while(debugFile.good())
        {
            getline(debugFile,line);
	    // Ignore commented lines
            if (line[0] == '#')
            	continue;
	    // Check if module name and log level combination is present		
            if ((line.find(module, 0) != string::npos) && (line.find(level, 0) != string::npos))
            {
                debugFile.close();
                return true;
            }
        }
        debugFile.close();
    }
    else
    {
	DEBUG_PRINT(DEBUG_ERROR,"\n%s: Unable to open conf file %s\n", __FUNCTION__,tdkDebugIniFile.c_str());
    }

    return false;
}

/**
 * Checks if a particular log is logged by RDK_LOG command.
 *
 * @param search Log message logged by RDK_LOG.
 * @return       true if log msg is found
 *               false if log msg is not found
 * Filename is derived from the console log file name generated 
 * on each testcase execution.
 **/

bool CheckLog(const char* search)
{
    string line;
    ifstream logFile;
    string tdkLogFile = "";

    /* Extracting path to logs folder */
    tdkLogFile.append(g_tdkPath);
    tdkLogFile.append("/logs/");
    tdkLogFile.append(TDKAGENT_LOG);

#ifdef SYSTEMD_JOURNAL
    //Redirect rdklogger journal logging to tdk log file
    DEBUG_PRINT(DEBUG_TRACE, "Redirecting rdklogger journal logging to tdk log file\n");
    FILE *fp = NULL;
    char readRespBuff[512] = { '\0' };
    string cmd= "journalctl -a -u tdk";
    fp = popen(cmd.c_str(),"r");
    if (fp == NULL)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Redirecting journal failed");
        return false;
    }
    while(fgets(readRespBuff,sizeof(readRespBuff),fp) != NULL)
        {
            cout<<readRespBuff<<endl;
        }
    pclose(fp);
#endif

    logFile.open(tdkLogFile, ios::in);
    if(logFile.is_open())
    {
        while(logFile.good())
        {
            getline(logFile,line);
            if (line.find(search, 0) != string::npos) 
            {
		DEBUG_PRINT(DEBUG_TRACE,"Success! RDKLogger test log \"%s\" found in file %s\n",search,tdkLogFile.c_str());
		logFile.close();
             	return true;
            }
        }
        logFile.close();
        DEBUG_PRINT(DEBUG_ERROR,"Error! RDKLogger test log \"%s\" not found in file %s\n",search,tdkLogFile.c_str());
    }
    else
    {
	DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open file %s\n", tdkLogFile.c_str());
    }

    return false;
}

bool createTdkDebugIniFile(bool enableMPELog=true)
{
        // Make a copy of debug.ini file for testing
        ifstream  src(DEBUG_CONF_FILE, ios::binary);
        ofstream  dst(tdkDebugIniFile, ios::binary);

        if(!src || !dst)
        {
            DEBUG_PRINT(DEBUG_TRACE, "Error opening files!\n");
            return false;
        }

        if (!enableMPELog)
        {
            //Disable MPEOS debug support
            string strTemp;
            while(getline(src,strTemp)){
                if (strTemp.find("EnableMPELog = TRUE") != std::string::npos) {
                    dst << "EnableMPELog = FALSE" << endl;
                }
                else {
                    dst << strTemp << endl;
                }
            }
        }
        else
        {
            dst << src.rdbuf();
        }

        src.close();
        dst.close();

        // Now edit temp debug.ini file to add modules and env variables
        // for simulating test scenarios
        fstream debugFile;
        string line;
        debugFile.open (tdkDebugIniFile, ios::in | ios::out | ios::app);
        if (debugFile.is_open())
        {
            debugFile << "LOG.RDK.TEST1 = ALL DEBUG TRACE" << endl;
            debugFile << "LOG.RDK.TEST2 = NONE ALL" << endl;
            debugFile << "LOG.RDK.TEST3 = ALL NONE" << endl;
            debugFile << "LOG.RDK.TEST4 = TRACE" << endl;
            debugFile << "LOG.RDK.TEST5 = !TRACE" << endl;
            debugFile << "LOG.RDK.TEST6 = " << endl;

            //Print temp debug.ini file contents
            debugFile.clear();                  // clear fail and eof bits
            debugFile.seekg(0, ios::beg);       // back to the start!

            DEBUG_PRINT(DEBUG_TRACE, "\n==== Start %s ====================\n", tdkDebugIniFile.c_str());
            while(debugFile.good())
            {
                    getline(debugFile,line);
                    // Ignore commented lines
                    if (line[0] == '#')
                        continue;
                    DEBUG_PRINT(DEBUG_TRACE, "%s", line.c_str());
            }
            DEBUG_PRINT(DEBUG_TRACE, "\n====== End %s ====================\n\n", tdkDebugIniFile.c_str());
            // end of printing temp debug.ini

            debugFile.close();
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n%s: Unable to create test conf file %s\n",__FUNCTION__,tdkDebugIniFile.c_str());
                return false;
        }

        return true;
}

/**************************************************************************
Function name : RDKLoggerAgent::initialize

Arguments     : Input arguments are Version string and RDKLoggerAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool RDKLoggerAgent::initialize(IN const char* szVersion)
{
        DEBUG_PRINT(DEBUG_ERROR, "RDKLoggerAgent Initialization\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string RDKLoggerAgent::testmodulepre_requisites()
{
	DEBUG_PRINT(DEBUG_TRACE, "RDKlogger testmodule pre_requisites --> Entry\n");

	// Make a copy of debug.ini file for testing
        if (false == createTdkDebugIniFile())
        {
                return "FAILURE<DETAILS>Failed to create test conf file";
        }

        // Initialize the temp conf file
	rdk_Error ret = rdk_logger_init(tdkDebugIniFile.c_str());
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. ErrCode = %d\n", ret);
		DEBUG_PRINT(DEBUG_TRACE, "RDKlogger testmodule pre_requisites --> Exit\n");
		return "FAILURE<DETAILS>Failed to init rdk logger";
        }

	b_rdk_logger_enabled = true;
	DEBUG_PRINT(DEBUG_TRACE, "Init rdk logger success\n");
	DEBUG_PRINT(DEBUG_TRACE, "RDKlogger testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool RDKLoggerAgent::testmodulepost_requisites()
{
	DEBUG_PRINT(DEBUG_TRACE, "RDKlogger testmodule post_requisites --> Entry\n");

	// Remove the local copy of debug.ini file
	if( remove( tdkDebugIniFile.c_str() ) != 0 )
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n%s: Error deleting file %s\n", __FUNCTION__,tdkDebugIniFile.c_str());
		DEBUG_PRINT(DEBUG_TRACE, "RDKlogger testmodule post requisites --> Exit");
		return TEST_FAILURE;
	}
  	else
	{
		DEBUG_PRINT(DEBUG_TRACE, "%s file successfully deleted\n", tdkDebugIniFile.c_str());
	}

#if 0
        // De-Initialize rdklogger
        rdk_Error ret = rdk_logger_deinit();
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to de-init rdk logger. ErrCode = %d\n", ret);
                DEBUG_PRINT(DEBUG_TRACE, "RDKlogger testmodule post requisites --> Exit");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "rdk logger de-init successful\n");
        }
#endif

        DEBUG_PRINT(DEBUG_TRACE, "RDKlogger testmodule post requisites --> Exit");
       	return TEST_SUCCESS;
}


/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Init

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to initialize RDK debug manager module.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_Init(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Init --->Entry\n");

        if (true == b_rdk_logger_enabled)
	{
        	response["result"] = "SUCCESS";
        	response["details"] = "rdk logger init success";
	}
	else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Init -->Exit\n");
                return;
        }

     	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Init -->Exit\n");

       	return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Log

Arguments     : Input argument is "module", "level". 
		Output argument: 
		"SUCCESS" if logging is successful
		"FAILURE" if logging failed.

Description   : Receives the request from Test Manager to add a log message.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/

void RDKLoggerAgent::RDKLoggerAgent_Log(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log --->Entry\n");

        int logLevel = -1;
        char rdkMod[20] = {'\0'};
	char testMsg[64] = {'\0'};

        string module = req["module"].asString();
        string level = req["level"].asString();

        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());
        logLevel = logNameToEnum(level.c_str());
	sprintf(testMsg, "Test log from RDKLogger mod=%s lvl=%s", module.c_str(), level.c_str());

	RDK_LOG ( (rdk_LogLevel) logLevel, rdkMod, testMsg );

        if (true == CheckLog(testMsg))
        {
                response["result"] = "SUCCESS";
                response["details"] = "rdk logging success";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log -->Exit\n");
                return;
        }
        else
        {
                response["result"] = "FAILURE";
                response["details"] = "rdk logging failed";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log -->Exit\n");
                return;
        }
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Dbg_Enabled_Status

Arguments     : Input argument is "module" and "level". 
		Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check if a specified log level 
		of a module is enabled.
                Gets the response from RDKLogger element and send it to the Test Manager. 
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_Dbg_Enabled_Status(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Dbg_Enabled_Status --->Entry\n");

	int logLevel = -1;
	char rdkMod[20] = {'\0'};
	char stringDetails[10] = {'\0'};

	string module = req["module"].asString();
	string level = req["level"].asString();

        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());
        logLevel = logNameToEnum(level.c_str());
	
	bool rdkStatus = rdk_dbg_enabled( rdkMod, (rdk_LogLevel)logLevel);
	bool dbgFindStatus = dbgFinder( rdkMod, level.c_str());

        if (dbgFindStatus == rdkStatus)
        {
        	if (TRUE == rdkStatus)
		{
                	DEBUG_PRINT(DEBUG_TRACE, "%s %s Enabled.\n", rdkMod, level.c_str());
			snprintf(stringDetails, strlen("Enabled") + 1, "%s", "Enabled");
		}
		else
		{
			DEBUG_PRINT(DEBUG_TRACE, "%s %s Disabled.\n", rdkMod, level.c_str());
			snprintf(stringDetails, strlen("Disabled") + 1, "%s", "Disabled");
		}
		response["result"] = "SUCCESS";
		response["details"] = stringDetails;
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Dbg_Enabled_Status -->Exit\n");
		return;
        }

	DEBUG_PRINT(DEBUG_ERROR, "Failed to get %s %s log status\n", rdkMod, level.c_str()); 
	DEBUG_PRINT(DEBUG_TRACE, "rdk_dbg_enabled result = %d dbgFinder result = %d\n", rdkStatus, dbgFindStatus);

	response["result"] = "FAILURE";
	response["details"] = "Failed to get dbg enable status";

	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Dbg_Enabled_Status -->Exit\n");
	return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGet

Arguments     : Input argument is "module". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the logging level value of the 
		specified environment variable
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_EnvGet(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGet --->Entry\n");

        char rdkMod[20] = {'\0'};
        char stringDetails[SIZE] = {'\0'};
        const char* envVar = NULL;

        string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

        envVar = rdk_logger_envGet(rdkMod);
        if ((envVar != NULL) && (envVar[0] != 0))
        {
                DEBUG_PRINT(DEBUG_TRACE, "%s logging levels: %s\n", rdkMod, envVar);
                snprintf(stringDetails, strlen(envVar) + 1, "%s", envVar);
                response["details"] = stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "%s logging disabled!\n", rdkMod);
		response["result"] = "FAILURE";
                response["details"] = "Logging disabled for module";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGet -->Exit\n");
                return;
        }

        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGet -->Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGetNum

Arguments     : Input argument is "module". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the registered number of the
                specified environment variable
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_EnvGetNum(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetNum --->Entry\n");

        char rdkMod[20] = {'\0'};
	char stringDetails[5] = {'\0'};
	int modNum = -1;

	string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

    	modNum = rdk_logger_envGetNum(rdkMod);
	DEBUG_PRINT(DEBUG_TRACE, "Module: %s Module number = %d\n", rdkMod, modNum);
    	if (modNum < 0)
    	{
                response["result"] = "FAILURE";
                response["details"] = "Unknown module specified";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetNum -->Exit\n");
                return;
    	}

      	sprintf(stringDetails, "%d", modNum);
      	response["details"] = stringDetails;

        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetNum -->Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGetValueFromNum

Arguments     : Input argument is "number". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the logging level value of the 
		specified environment variable based on its registered number
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_EnvGetValueFromNum(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetValueFromNum --->Entry\n");

        char stringDetails[SIZE] = {'\0'};
        const char *envVarValue = NULL;
        int modNum = -1;

        /** Get the logging level from registered number **/
	modNum = req["number"].asInt();
        envVarValue = rdk_logger_envGetValueFromNum(modNum);
        if ((envVarValue != NULL) && (envVarValue[0] != '\0'))
        {
                DEBUG_PRINT(DEBUG_TRACE, "Registered Number = %d, Logging level value = %s\n", modNum, envVarValue);
                snprintf(stringDetails, strlen(envVarValue) + 1, "%s", envVarValue);
                response["details"] = stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "No logging level value for number = %d\n", modNum);
		response["result"] = "FAILURE";
		response["details"] = "No logging level value for number";
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetValueFromNum -->Exit\n");
		return;
        }

        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetValueFromNum -->Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGetModFromNum

Arguments     : Input argument is "number". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the module name of the
                specified environment variable based on its registered number
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_EnvGetModFromNum(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetModFromNum --->Entry\n");

        char stringDetails[50] = {'\0'};
        int modNum = -1;
	const char *envMod = NULL;

	modNum = req["number"].asInt();
        envMod = rdk_logger_envGetModFromNum(modNum);
        if ((envMod != NULL) && (envMod[0] != '\0'))
        {
                DEBUG_PRINT(DEBUG_TRACE, "Registered Number = %d, Module = %s\n", modNum, envMod);
                snprintf(stringDetails, strlen(envMod) + 1, "%s", envMod);
                response["details"] = stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "No module for number(%d)\n", modNum);
		response["result"] = "FAILURE";
		response["details"] = "No module for number";
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetModFromNum -->Exit\n");
		return;
        }

        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetModFromNum -->Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_CheckMPELogEnabled

Arguments     : Input argument : None
		Output argument : "SUCCESS" if EnableMPELog is TRUE
			  	  "FAILURE" if EnableMPELog is FALSE

Description   : Receives the request from Test Manager to check if EnableMPELog value is true or false
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_CheckMPELogEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_CheckMPELogEnabled --->Entry\n");

        const char* envVar = NULL;

        envVar = rdk_logger_envGet("EnableMPELog");
        if ((envVar != NULL) && (envVar[0] != 0))
        {
                DEBUG_PRINT(DEBUG_TRACE, "EnableMPELog value: %s\n", envVar);
        	if (0 != strcmp("TRUE", envVar))
        	{
			response["result"] = "FAILURE";
			response["details"] = "EnableMPELog not enabled";
			DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_CheckMPELogEnabled -->Exit\n");
			return;
        	}
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR, "Failed to get EnableMPELog value\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed to get EnableMPELog value";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_CheckMPELogEnabled -->Exit\n");
                return;
        }

        response["result"] = "SUCCESS";
	response["details"] = "EnableMPELog enabled";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_CheckMPELogEnabled --> Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Log_All

Arguments     : Input argument is "module"
                Output argument:
 		"SUCCESS" if all 5 logs are logged 
		"FAILURE" if any one logging fails.

Description   : Receives the request from Test Manager to add 5 log messages
		of levels INFO, NOTICE, WARNING, ERROR and FATAL for a module
		configured with ALL threshold in conf file.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_Log_All(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_All --->Entry\n");

        char rdkMod[20] = {'\0'};
        char testMsg[64] = {'\0'};
	int  level = RDK_LOG_FATAL;

        string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

        /** Loop through the control word and printout the enabled levels. */
        while (level <= RDK_LOG_INFO)
        {
            sprintf(testMsg, "Test ALL from RDKLogger mod=%s lvl=%s", module.c_str(), rdk_logLevelStrings[level]);
            RDK_LOG((rdk_LogLevel)level, rdkMod, testMsg);
            if (true != CheckLog(testMsg))
            {
                sprintf(testMsg, "rdklogger ALL failed to log %s msg", rdk_logLevelStrings[level]);
                response["result"] = "FAILURE";
                response["details"] = testMsg;
                DEBUG_PRINT(DEBUG_ERROR, "%s\n",testMsg);
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_All -->Exit\n");
                return;
            }
            level++;
        }

	response["result"] = "SUCCESS";
     	response["details"] = "rdk logging all success";
    	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_All -->Exit\n");
     	return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Log_None

Arguments     : Input argument is "module"
                Output argument:
		"SUCCESS" if none of 15 logs is logged
		"FAILURE" if any one logging is successful

Description   : Receives the request from Test Manager to add 15 log messages
                of levels TRACE1..TRACE9, DEBUG, INFO, NOTICE, WARNING, ERROR, FATAL for a module
                configured with NONE threshold in conf file.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_Log_None(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_None --->Entry\n");

        char	rdkMod[20] = {'\0'};
        char 	testMsg[64] = {'\0'};
	int 	level = ENUM_RDK_LOG_BEGIN;

        string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

    	/** Loop through the control word and printout the enabled levels. */
    	while (level < ENUM_RDK_LOG_COUNT)
    	{
	    sprintf(testMsg, "Test NONE from RDKLogger mod=%s lvl=%s", module.c_str(), rdk_logLevelStrings[level]);
	    RDK_LOG((rdk_LogLevel)level, rdkMod, testMsg);
            if (true == CheckLog(testMsg))
            {
		sprintf(testMsg, "rdklogger NONE logged %s msg", rdk_logLevelStrings[level]);
                response["result"] = "FAILURE";
                response["details"] = testMsg;
                DEBUG_PRINT(DEBUG_ERROR, "%s\n",testMsg);
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_None -->Exit\n");
                return;
            }
            level++;
    	}

        response["result"] = "SUCCESS";
        response["details"] = "No rdk logging with NONE threshold";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_None -->Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Log_Trace

Arguments     : Input argument is "module"
                Output argument: 
		"SUCCESS" if all 9 trace logs are logged
		"FAILURE" if any one trace log is not logged

Description   : Receives the request from Test Manager to add 9 log messages
                of levels TRACE1..TRACE9 for a module
                configured with TRACE threshold in conf file.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/

void RDKLoggerAgent::RDKLoggerAgent_Log_Trace(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_Trace --->Entry\n");

        char rdkMod[20] = {'\0'};
        char testMsg[64] = {'\0'};
	int  level = RDK_LOG_TRACE1;

        string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

        /** Loop through the trace control word and printout the enabled levels. */
        while (level < ENUM_RDK_LOG_COUNT)
        {
            sprintf(testMsg, "Test TRACE from RDKLogger mod=%s lvl=%s", module.c_str(), rdk_logLevelStrings[level]);
            RDK_LOG((rdk_LogLevel)level, rdkMod, testMsg);
            if (true != CheckLog(testMsg))
            {
                sprintf(testMsg, "rdklogger TRACE failed to log %s msg", rdk_logLevelStrings[level]);
                response["result"] = "FAILURE";
                response["details"] = testMsg;
                DEBUG_PRINT(DEBUG_ERROR, "%s\n",testMsg);
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_Trace -->Exit\n");
                return;
            }
            level++;
        }

        response["result"] = "SUCCESS";
        response["details"] = "rdk logging trace success";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_Trace -->Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Log_InverseTrace

Arguments     : Input argument is "module"
                Output argument:
		"SUCCESS" if none of trace logs are logged
		"FAILURE" if any one trace log is logged

Description   : Receives the request from Test Manager to add 9 log messages
                of levels TRACE1..TRACE9 for a module configured with !TRACE threshold 
		in conf file.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/

void RDKLoggerAgent::RDKLoggerAgent_Log_InverseTrace(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_InverseTrace --->Entry\n");

        char rdkMod[20] = {'\0'};
        char testMsg[64] = {'\0'};
	int  level = RDK_LOG_TRACE1;

        string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

        /** Loop through the trace control word and printout the enabled levels. */
        while (level < ENUM_RDK_LOG_COUNT)
        {
            sprintf(testMsg, "Test !TRACE from RDKLogger mod=%s lvl=%s", module.c_str(), rdk_logLevelStrings[level]);
            RDK_LOG((rdk_LogLevel)level, rdkMod, testMsg);
            if (true == CheckLog(testMsg))
            {
                sprintf(testMsg, "rdklogger Inverse TRACE logged %s msg", rdk_logLevelStrings[level]);
                response["result"] = "FAILURE";
                response["details"] = testMsg;
                DEBUG_PRINT(DEBUG_ERROR, "%s\n",testMsg);
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_InverseTrace -->Exit\n");
                return;
            }
            level++;
        }

        response["result"] = "SUCCESS";
        response["details"] = "rdk logging inverse trace success";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_InverseTrace -->Exit\n");
        return;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Log_Msg

Arguments     : Input arguments:
		"module": RDK module name
		"level": Logging level
		"msg": printf style string containing the log message

                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to add a log message.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
void RDKLoggerAgent::RDKLoggerAgent_Log_Msg(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_Msg --->Entry\n");

        int logLevel = -1;
        char rdkMod[20] = {'\0'};

        string module = req["module"].asString();
        string level = req["level"].asString();
	string msg = req["msg"].asString();

        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());
        logLevel = logNameToEnum(level.c_str());

        RDK_LOG ((rdk_LogLevel) logLevel, rdkMod, msg.c_str());

	if (true == CheckLog(msg.c_str()))
	{
        	response["result"] = "SUCCESS";
        	response["details"] = "rdk logging success";
        	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_Msg -->Exit\n");
        	return;
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "rdk logging failed";
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_Msg -->Exit\n");
		return;
	}
}

void RDKLoggerAgent::RDKLoggerAgent_SetLogLevel(IN const Json::Value& req, OUT Json::Value& response)
{
	response["result"] = "FAILURE";
	response["details"] = "Failed to call rdk_dbg_priv_SetLogLevel";
	return;
}

void RDKLoggerAgent::RDKLoggerAgent_GetLogLevel(IN const Json::Value& req, OUT Json::Value& response)
{
	response["result"] = "FAILURE";
	response["details"] = "Failed to call rdk_dbg_priv_LogQueryOpSysIntf";
	return;
}

#if 0
bool RDKLoggerAgent::RDKLoggerAgent_Log_MPEOSDisabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_MPEOSDisabled --->Entry\n");
        rdk_Error ret = RDK_SUCCESS;

        // Remove the local copy of debug.ini file created in testmodulepre_requisites
        if( remove( tdkDebugIniFile.c_str() ) != 0 )
        {
                DEBUG_PRINT(DEBUG_ERROR,"Error deleting file %s\n", tdkDebugIniFile.c_str());
                response["result"] = "FAILURE";
                response["details"] = "Error deleting temp debug.ini file";

                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_MPEOSDisabled --> Exit");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "%s file successfully deleted\n", tdkDebugIniFile.c_str());
        }

        // De-Initialize rdklogger with EnableMPELog enabled in testmodulepre_requisites
        ret = rdk_logger_deinit();
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to de-init rdk logger. ErrCode = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to de-init rdk logger";

                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_MPEOSDisabled --> Exit");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "rdk logger de-init successful\n");
        }

        // create a new local copy of debug.ini file with MPEOS debug support disabled
        if (false == createTdkDebugIniFile(false))
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to create test conf file with MPEOS debug support disabled\n");
                response["result"] = "FAILURE";
                response["details"] = "Failed to create conf file with MPEOS debug support disabled";

                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_MPEOSDisabled --> Exit");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Creation of test conf file with MPEOS debug support disabled successful\n");
        }

        // Initialize the temp conf file with MPEOS debug support disabled
        ret = rdk_logger_init(tdkDebugIniFile.c_str());
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger with EnableMPELog false. ErrCode = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger with MPEOS disabled";

                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_MPEOSDisabled --> Exit");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "rdk logger init successful\n");
        }

        //Log test message with MPEOS disabled
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST1", "Log message with EnableMPELog False\n");
        if (false == CheckLog("Log message with EnableMPELog False"))
        {
                response["result"] = "SUCCESS";
                response["details"] = "rdk logging failed with MPEOS disabled";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_MPEOSDisabled -->Exit\n");
                return TEST_SUCCESS;
        }
        else
        {
                response["result"] = "FAILURE";
                response["details"] = "rdk logging success with MPEOS disabled";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log_MPEOSDisabled -->Exit\n");
                return TEST_FAILURE;
        }
}
#endif

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "RDKLoggerAgent".
**************************************************************************/

extern "C" RDKLoggerAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new RDKLoggerAgent(ptrtcpServer);
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool RDKLoggerAgent::cleanup(IN const char* szVersion)
{
        DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
        return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is RDKLoggerAgent Object

Description   : This function will be used to destory the RDKLoggerAgent object.
**************************************************************************/
extern "C" void DestroyObject(RDKLoggerAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying RDKLogger Agent object\n");
        delete stubobj;
}
