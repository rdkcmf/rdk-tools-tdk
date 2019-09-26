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

#ifndef RPC_METHODS_H
#define RPC_METHODS_H 

/* System Includes */
#include <json/json.h>

/* Application Includes */
#include "rdktestagentintf.h"
/* Constants */
#define DEVICE_FREE 0
#define DEVICE_BUSY 1
#define FLAG_SET 0
#define FLAG_NOT_SET 1
#define RETURN_SUCCESS 0
#define RETURN_FAILURE -1
#define NULL_LOG "/dev/null"
#define CONFIGURATION_FILE "tdkconfig.ini"
#define PORT_FORWARD_RULE_FILE "forwardRule.ini"


#define STR(x)   #x
#define SHOW_DEFINE(x) STR(x)


/**************************************************************************************
 Description   : This Class provides RPC methods. Test Manager can invoke these 
                      RPC methods to do some operations in the box.
 
 **************************************************************************************/
//class RpcMethods
class RpcMethods : public AbstractServer<RpcMethods>
{
	
    public:
        static FILE *sm_pLogStream;
        static int sm_nConsoleLogFlag;
        static int sm_nAgentPID;
        static int sm_nModuleCount;
        static int sm_nRouteSetFlag;
        static int sm_nGetDeviceFlag;
        static int sm_nStatusQueryFlag;
        static int sm_nDeviceStatusFlag;
		
        static const char* sm_szManagerIP;
        static const char* sm_szBoxName;
        static const char* sm_szBoxInterface;
		
        static std::string sm_strBoxIP;
        static std::string sm_strResultId;
        static std::string sm_strLogFolderPath;
        static std::string sm_strTDKPath;
        static std::string sm_strConsoleLogPath;

        /* Constructor */
        RpcMethods(TcpSocketServer &ptrStatusServer) : AbstractServer <RpcMethods>(ptrStatusServer)
        {
           
         //this->bindAndAddMethod(Procedure("executeTestCase", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCExecuteTestCase);
         this->bindAndAddMethod(Procedure("getStatus", PARAMS_BY_NAME, JSON_STRING,"managerIP",JSON_STRING,"boxName",JSON_STRING,NULL), &RpcMethods::RPCGetStatus);
         this->bindAndAddMethod(Procedure("loadModule", PARAMS_BY_NAME, JSON_STRING,"execID",JSON_STRING,"deviceID",JSON_STRING,"testcaseID",JSON_STRING,"execDevID",JSON_STRING,"resultID",JSON_STRING,"param1",JSON_STRING,"performanceBenchMarkingEnabled",JSON_STRING,"performanceSystemDiagnosisEnabled",JSON_STRING,NULL), &RpcMethods::RPCLoadModule);
         this->bindAndAddMethod(Procedure("unloadModule", PARAMS_BY_NAME, JSON_STRING,"param1",JSON_STRING,"ScriptSuiteEnabled",JSON_STRING,NULL), &RpcMethods::RPCUnloadModule);
         this->bindAndAddMethod(Procedure("enableReboot", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCEnableReboot);
         this->bindAndAddMethod(Procedure("restorePreviousState", PARAMS_BY_NAME, JSON_STRING,"execID",JSON_STRING,"deviceID",JSON_STRING,"testcaseID",JSON_STRING,"execDevID",JSON_STRING,"resultID",JSON_STRING,NULL), &RpcMethods::RPCRestorePreviousState);
         this->bindAndAddMethod(Procedure("getHostStatus", PARAMS_BY_NAME, JSON_STRING,"managerIP",JSON_STRING,"boxName",JSON_STRING,NULL), &RpcMethods::RPCGetHostStatus);
         this->bindAndAddMethod(Procedure("callEnableTDK", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCCallEnableTDK);
         this->bindAndAddMethod(Procedure("callDisableTDK", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCCallDisableTDK);
         this->bindAndAddMethod(Procedure("resetAgent", PARAMS_BY_NAME, JSON_STRING,"enableReset",JSON_STRING,NULL), &RpcMethods::RPCResetAgent);
         this->bindAndAddMethod(Procedure("rebootBox", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCRebootBox);
         this->bindAndAddMethod(Procedure("getRDKVersion", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCGetRDKVersion);
         this->bindAndAddMethod(Procedure("getAgentConsoleLogPath", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCGetAgentConsoleLogPath);
         this->bindAndAddMethod(Procedure("performanceSystemDiagnostics", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCPerformanceSystemDiagnostics);
         this->bindAndAddMethod(Procedure("performanceBenchMarking", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCPerformanceBenchMarking);
         this->bindAndAddMethod(Procedure("executeLoggerScript", PARAMS_BY_NAME, JSON_STRING,"argument",JSON_STRING,NULL), &RpcMethods::RPCExecuteLoggerScript);
         this->bindAndAddMethod(Procedure("removeLogs", PARAMS_BY_NAME, JSON_STRING,"argument",JSON_STRING,NULL), &RpcMethods::RPCRemoveLogs);
         this->bindAndAddMethod(Procedure("PushLog", PARAMS_BY_NAME, JSON_STRING,"STBfilename",JSON_STRING,"TMfilename",JSON_STRING,NULL), &RpcMethods::RPCPushLog);
         this->bindAndAddMethod(Procedure("uploadLog", PARAMS_BY_NAME, JSON_STRING,"STBfilename",JSON_STRING,"TMfilename",JSON_STRING,"logUploadURL",JSON_STRING,NULL), &RpcMethods::RPCUploadLog);
         this->bindAndAddMethod(Procedure("getImageName", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCGetImageName);
         this->bindAndAddMethod(Procedure("executeTestCase", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCExecuteTestCase);
	 this->bindAndAddMethod(Procedure("diagnosticsTest", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCDiagnosticsTest);
         
         //this->bindAndAddMethod(Procedure("executeTestCase", PARAMS_BY_NAME, JSON_STRING,"params",JSON_STRING,"method",JSON_STRING,NULL), &RpcMethods::RPCExecuteTestCase);


         /* Below methods are applicable only for Gateway boxes */
         #ifdef PORT_FORWARD

         this->bindAndAddMethod(Procedure("getConnectedDevices", PARAMS_BY_NAME, JSON_STRING,NULL), &RpcMethods::RPCGetConnectedDevices);
         this->bindAndAddMethod(Procedure("setClientRoute", PARAMS_BY_NAME, JSON_STRING,"MACaddr",JSON_STRING,"agentPort",JSON_STRING,"statusPort",JSON_STRING,"logTransferPort",JSON_STRING,"agentMonitorPort",JSON_STRING,NULL), &RpcMethods::RPCSetClientRoute);
         this->bindAndAddMethod(Procedure("getClientMocaIpAddress", PARAMS_BY_NAME, JSON_STRING,"MACaddr",JSON_STRING,NULL), &RpcMethods::RPCGetClientMocaIpAddress);

        #endif /* End of PORT_FORWARD */  

        }
        


	void RPCExecuteTestCase (const Json::Value& request, Json::Value& response);
        void RPCGetStatus (const Json::Value& request, Json::Value& response);
        void RPCLoadModule (const Json::Value& request, Json::Value& response);
        void RPCUnloadModule (const Json::Value& request, Json::Value& response);
        void RPCEnableReboot (const Json::Value& request, Json::Value& response);
        void RPCRestorePreviousState (const Json::Value& request, Json::Value& response);
        void RPCGetHostStatus (const Json::Value& request, Json::Value& response);
        void RPCCallEnableTDK(const Json::Value& request, Json::Value& response);
        void RPCCallDisableTDK(const Json::Value& request, Json::Value& response);
        void RPCResetAgent (const Json::Value& request, Json::Value& response);
        void RPCRebootBox (const Json::Value& request, Json::Value& response);
        void RPCGetRDKVersion (const Json::Value& request, Json::Value& response);
        void RPCGetAgentConsoleLogPath(const Json::Value& request, Json::Value& response);
        void RPCPerformanceSystemDiagnostics (const Json::Value& request, Json::Value& response);
        void RPCPerformanceBenchMarking (const Json::Value& request, Json::Value& response);
        void RPCExecuteLoggerScript (const Json::Value& request, Json::Value& response);
	void RPCRemoveLogs (const Json::Value& request, Json::Value& response);
	void RPCPushLog (const Json::Value& request, Json::Value& response);
	void RPCUploadLog (const Json::Value& request, Json::Value& response);
	void RPCGetImageName (const Json::Value& request, Json::Value& response);
        void RPCDiagnosticsTest (const Json::Value& request, Json::Value& response);

	/* Below methods are applicable only for Gateway boxes */
        #ifdef PORT_FORWARD

        void RPCGetConnectedDevices (const Json::Value& request, Json::Value& response);
        void RPCSetClientRoute (const Json::Value& request, Json::Value& response);
        void RPCGetClientMocaIpAddress (const Json::Value& request, Json::Value& response);

        #endif /* End of PORT_FORWARD */

    private:
        RDKTestAgent *m_pAgent;
        int m_iLoadStatus;
        int m_iUnloadStatus;

        void SignalFailureDetails();
        std::string LoadLibrary (char* pszLibName);
        std::string UnloadLibrary (char* pszLibName);
        char* GetHostIPInterface (const char* pszIPaddr);
        bool DeleteModuleFromFile (std::string strLibName);
        void CallReboot();
        void ResetCrashStatus();
        void SetCrashStatus (const char* pszExecId, const char* pszDeviceId, const char* pszTestCaseId, const char* pszExecDevId, const char* pszResultId);
	 
}; /* End of RpcMethods */

#endif /* End of RPC_METHODS_H */

