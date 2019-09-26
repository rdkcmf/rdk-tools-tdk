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

#include "IARMBUSAgent.h"
#include <cstring>
#include <sstream>
#include <errno.h>

std::ostringstream gsysMgrdata;
std::ostringstream gEventdata;
int LastKeyType;
int LastKeyCode;

char LastEvent[80],g_ManagerName[20];
int gSysState;
int gSysError;
char gSysPayload[20];
IARM_Bus_SYSMgr_SystemState_t gstateId ;

double LastKeyTime;
static char gLastEvent[40];
static char gEventSummary[1024];
int gEventSummaryCount = 0;
int ExpectedKeyCode = 0;
int ExpectedKeyType = 0;
int gRegisteredEventCount = 0;
int LastKeyType_Perf;
int LastKeyCode_Perf;

/* Test for RegisterCall API call */
bool REGISTERCALLSTATUS=0;

/*These global variables are to check the test app with event handler and BusCall APIS*/
int g_evtData[EVTDATA_MAX_SIZE],g_iter=0;
char g_evtName[EVTDATA_MAX_SIZE];
std::string g_tdkPath = getenv("TDK_PATH");

/*Variables for invoking and syncing second app*/
static int syncCount = 0;
static pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static    IARM_Bus_DUMMYMGR_HandlerReady_Param_t handler_param;

/**************************************************************************
 *
 * Function Name : iarmMgrStatus
 * Descrption    : This function will get the existense of pre- requisite app
 *                 and return SUCCESS or FAILURE status to the caller
 *
 * @param retval [in] ownerName - owner(manager) to be checked.
 *		 [out]- bool - SUCCESS / FAILURE
 ***************************************************************************/

bool iarmMgrStatus(char *ownerName )
{
        char output[LINE_LEN] = {'\0'};
    	char strCmd[STR_LEN] = {'\0'};
    	FILE *fp = NULL;
    	bool running = false;

	char appName[20] = {'\0'};
	if (strcmp(ownerName, IARM_BUS_DAEMON_NAME)  == 0)
        {
		strcpy(appName,DAEMON_EXE);	
	}
	else if (strcmp(ownerName, IARM_BUS_IRMGR_NAME)  == 0)
        {
		strcpy(appName,IRMGR_EXE);
	}
	else if (strcmp(ownerName, IARM_BUS_PWRMGR_NAME)  == 0)
        {
		strcpy(appName,PWRMGR_EXE);
	}
	else if (strcmp(ownerName, IARM_BUS_MFRLIB_NAME)  == 0)
        {
		strcpy(appName,MFRMGR_EXE);
	}
	else if (strcmp(ownerName, IARM_BUS_SYSMGR_NAME)  == 0)
        {
		strcpy(appName,SYSMGR_EXE);
	}
	else if (strcmp(ownerName, IARM_BUS_DUMMYMGR_NAME)  == 0)
        {
                strcpy(appName,IARM_BUS_DUMMYMGR_NAME);
        }
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"Invalid Owner Name: %s\n", ownerName);
		return TEST_FAILURE;
	}

    	sprintf(strCmd,"pidof %s 2>&1",appName);
        DEBUG_PRINT(DEBUG_ERROR,"Checking running status of %s using '%s'\n", ownerName, strCmd);
    	fp = popen(strCmd, "r");
    	/* Read the output */
    	if (fp != NULL)
    	{
            if (fgets(output, sizeof(output)-1, fp) != NULL) {
                running = true;
            }
            DEBUG_PRINT(DEBUG_TRACE, "%s process id: %s",appName, output);
            pclose(fp);
    	}
    	else {
            DEBUG_PRINT(DEBUG_ERROR, "Encountered popen error: %s\n", strerror(errno));
    	}

	return running;
}

/***************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper function will be used in the 
 *  		  script
 *****************************************************************************/ 

bool IARMBUSAgent::initialize(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent Initialize\n");
	return TEST_SUCCESS;

}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string IARMBUSAgent::testmodulepre_requisites()
{
#if 0
	DEBUG_PRINT(DEBUG_LOG,"Entering %s function\n", __func__);

	if ((iarmMgrStatus((char*)IARM_BUS_DAEMON_NAME)) == TEST_SUCCESS)
	{
		DEBUG_PRINT(DEBUG_LOG,"[Success] Daemon Mgr running. Exiting %s function\n", __func__);
		return "SUCCESS";
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"[Failed] Daemon Mgr not running. Exiting %s function\n", __func__);
		return "FAILURE<DETAILS> Pre-requisite check failed for Daemon Mgr";
	}
#endif
        return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool IARMBUSAgent::testmodulepost_requisites()
{
        return TEST_SUCCESS;
}

/**************************************************************************
 * Function Name : _ReleaseOwnership
 * Description	: _ReleaseOwnership function will be registered for 
 IARM_BusDaemon_RequestOwnership API .
 ***************************************************************************/
static IARM_Result_t _ReleaseOwnership(void *arg)
{
	DEBUG_PRINT(DEBUG_TRACE,"############### TDK Client _ReleaseOwnership, CLIENT releasing stuff\n");
	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	return retCode;
}

/**************************************************************************
 *
 * Function Name: getResult
 * Descrption	: This function will get the retvalue as input and it returns 
 *		  corresponding SUCCESS or FAILUER status to the 
 *		  wrapper function.
 *
 * @param retval [in] - return value of IARMBUS APIs
 ***************************************************************************/
char* getResult(int retval,char *resultDetails)
{
        DEBUG_PRINT(DEBUG_LOG,"API return value = %d\n", retval);
	if(retval==0)
	{
		strcpy(resultDetails,"SUCCESS");
		return (char*)"SUCCESS";
	}
	else
	{
		switch(retval)
		{
			case 1: strcpy(resultDetails,"INVALID_PARAM");
				break;
			case 2: strcpy(resultDetails,"INVALID_STATE");
				break;
			case 3: strcpy(resultDetails,"IPCORE_FAIL");
				break;
			case 4: strcpy(resultDetails,"OUT_OF_MEMORY");
				break;
			default :
				strcpy(resultDetails,"UNKNOWN_ERROR");
				break; 
		}
		return (char*)"FAILURE";
	}
}

/**************************************************************************
 *
 * Function Name	: IARMBUSAgent_Init
 * Descrption	: IARMBUSAgent_Init wrapper function will be used to call IARMBUS 
 API "IARM_Bus_Init".
 *
 * @param [in] req- has "Process_name" which is input to IARM_Bus_Init
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/

void IARMBUSAgent::IARMBUSAgent_Init(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_Init --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["Process_name"]==NULL)
	{
		DEBUG_PRINT(DEBUG_LOG,"FAILURE:Process_name is NULL\n");		
		return;
	}
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_Init directly from IARMBUSAgent_Init\n");
	/*Calling IARMBUS API IARM_Bus_Init with json req as parameter*/
	retval=IARM_Bus_Init((char *)req["Process_name"].asCString());

	/* Constructing json reponse message */
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;

	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_Init --->Exit\n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_Term
 * Descrption	: IARMBUSAgent_Term wrapper function will be used to call IARMBUS API "IARM_Bus_Term".
 *
 * @param [in] req- None
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/
void IARMBUSAgent::IARMBUSAgent_Term(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_Term --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_Term()\n");

	/*Calling IARMBUS API IARM_Bus_Term  */
	retval=IARM_Bus_Term();

	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_Term --->Exit\n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_BusConnect
 * Descrption	: IARMBUSAgent_BusConnect wrapper function will be used to call IARMBUS API "IARM_Bus_Connect".
 * 
 * @param [in] req- None 
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_BusConnect(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BusConnect --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_Connect\n");
	/*Calling IARMBUS API IARM_Bus_Connect  */
	retval=IARM_Bus_Connect();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BusConnect --->Exit\n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_BusDisconnect
 * Descrption	: IARMBUSAgent_BusDisconnect wrapper function will be used to call 
 IARMBUS API "IARM_Bus_Disconnect".
 *
 * @param [in] req-None 
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/
void IARMBUSAgent::IARMBUSAgent_BusDisconnect(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BusDisconnect --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_Disconnect\n");
	/*Calling IARMBUS API IARM_Bus_Disconnect  */
	retval=IARM_Bus_Disconnect();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BusDisconnect --->Exit\n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_IsConnected
 * Description   : IARMBUSAgent_IsConnected wrapper function will be used to call 
 *		  IARMBUS API "IARM_Bus_IsConnected".
 *
 * @param [in] req- has "member_name" which is input to IARM_Bus_IsConnected
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 *****************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_IsConnected(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBus_IsConnected --->Entry \n");
	int isregistered;
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_IsConnected from IARMBus_IsConnected \n");
	if(&req["member_name"]==NULL)
	{
		return;
	}

	/*Calling IARM API IARM_Bus_IsConnected */
	retval=IARM_Bus_IsConnected((char*)req["member_name"].asCString(),&isregistered);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status and success return value*/	
	if(retval == 0)
	{
		response["result"]="SUCCESS";
		if(isregistered==0)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nNot Registered\n");
			response["details"]="Process_Not_Registered";
		}
		else if(isregistered==1)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nRegistered\n");
			response["details"]="Process_Registered";
		}
		else
		{
			response["details"]="NULL";
		}
	}
	else 
	{
		/*Filling json response with FAILURE status and error message*/
		response["result"]="FAILURE";
		switch(retval)
		{
			case 0:	response["details"]="IARM_RESULT_SUCCESS";
				break;
			case 1:	response["details"]="INVALID_PARAM";
				break;
			case 2:	response["details"]="INVALID_STATE";
				break;
			case 3:	response["details"]="IPCCORE_FAIL";
				break;
			case 4:	response["details"]="OUT_OF_MEMORY";
				break;
                        default:
				response["details"]="UNKNOWN_ERROR";
		}
	}
	free(resultDetails);	
	/*Need to fill the response with isregistered variable*/
	DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_IsConnected --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name : IARMBUSAgent_RequestResource
 * Description 	: IARMBUSAgent_RequestResource wrapper function will be used to call 
 *		  IARMBUS API "IARM_BusDaemon_RequestOwnership".
 *
 * @param [in] req- contains "resource_type" which is input to IARM_BusDaemon_RequestOwnership
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ****************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_RequestResource(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RequestResource --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["resource_type"]==NULL)
	{
		return;
	}
	int ResrcType_int=req["resource_type"].asInt(); 

	/* TWC Change : Check for RegisterCall API call */
	if ( REGISTERCALLSTATUS == 0) 
	{
		/*Calling IARMBUS API IARM_BusDaemon_RequestOwnership  */
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterCall from IARMBUSAgent_RequestResource \n");
		retval=IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
		if (retval != IARM_RESULT_SUCCESS)
		{
			DEBUG_PRINT(DEBUG_LOG,"\n\nIARM_Bus_RegisterCall - FAILED \n");
			response["result"]=getResult(retval,resultDetails);
			response["details"]=resultDetails;
			return;
		}
	}

	/*Calling IARMBUS API IARM_BusDaemon_RequestOwnership  */
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_BusDaemon_RequestOwnership from IARMBUSAgent_RequestResource \n");
	retval =IARM_BusDaemon_RequestOwnership((IARM_Bus_ResrcType_t)ResrcType_int);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RequestResource --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_ReleaseResource
 *
 * Description	: IARMBUSAgent_ReleaseResource wrapper function will be used to call IARMBUS 
 *		  API "IARM_BusDaemon_ReleaseOwnership".
 *
 * @param [in] req- has "resource_type" which is input to IARM_BusDaemon_ReleaseOwnership.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ****************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_ReleaseResource(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_ReleaseResource --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["resource_type"]==NULL)
	{
		return;
	}
	int ResrcType_int=req["resource_type"].asInt(); 

	/*Calling IARMBUS API IARM_BusDaemon_ReleaseOwnership  */
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_BusDaemon_ReleaseOwnership from IARMBUSAgent_ReleaseResource \n");
	retval =IARM_BusDaemon_ReleaseOwnership((IARM_Bus_ResrcType_t)ResrcType_int);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_ReleaseResource --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: get_LastReceivedEventDetails
 * Description	: This function is to get the last received Event details 	
 *
 ***************************************************************************/

void IARMBUSAgent::get_LastReceivedEventDetails(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"get_LastReceivedEventDetails --->Entry \n");

	DEBUG_PRINT(DEBUG_TRACE,"Event Mgr: %s Event Name: %s\n", g_ManagerName, LastEvent);

	if(strcmp(LastEvent,"IARM_BUS_IRMGR_EVENT_IRKEY")==0)
	{
		gEventdata << "Event Details: " << "KeyCode: " << std::hex << LastKeyCode << ", KeyType: " << std::hex << LastKeyType;
		response["details"]=gEventdata.str().c_str();
		gEventdata.str("");
		response["result"]="SUCCESS";
	}
	else if((strcmp(LastEvent,"IARM_BUS_PWRMGR_EVENT_MODECHANGED")==0))
	{
                response["details"]="Event Details: Power mode change event";
		response["result"]="SUCCESS";
	}
        else if(strcmp(LastEvent,"IARM_BUS_EVENT_RESOURCEAVAILABLE")==0)
        {
		response["details"]="Event Details: Resource available event";
                response["result"]="SUCCESS";
        }
        else if(strcmp(LastEvent,"IARM_BUS_EVENT_RESOLUTIONCHANGE")==0)
        {
		response["details"]="Event Details: Resolution change event";
                response["result"]="SUCCESS";
        }
        else if((strcmp(LastEvent,"IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE")==0))
        {
		response["details"]="Event Details: System state event";
                response["result"]="SUCCESS";
        }
        else if(strcmp(g_ManagerName,IARM_BUS_SYSMGR_NAME)==0)
        {
		response["details"]="Event Details: Sys manager event";
                response["result"]="SUCCESS";
        }
	else if (strcmp(g_ManagerName, IARM_BUS_DUMMYMGR_NAME)==0)
	{                                                   
		for(int i=0;i<EVTDATA_MAX_SIZE;i++)         
		{                                           
			gEventdata << g_evtData[i] << ":" << g_evtName[i] << ",";
			g_evtData[i]=0;                     
			g_evtName[i]='\0';                  
		}                                           
		response["details"]=gEventdata.str().c_str();
		gEventdata.str("");
		response["result"]="SUCCESS";               
	}                                             
	else
	{
		DEBUG_PRINT(DEBUG_TRACE,"get_LastReceivedEventDetails FAIL****************** \n");
		response["details"]="Failed to get event details";
		response["result"]="FAILURE";
	}

	memset(&(LastEvent) , '\0', (sizeof(char)*20));
	memset(g_ManagerName , '\0', (sizeof(char)*20));
	DEBUG_PRINT(DEBUG_TRACE,"get_LastReceivedEventDetails --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: fill_LastReceivedKey
 * Description	: fill_LastReceivedKey function is to fill the last recived IR 
 *		  key details in the global variable.
 *
 * @param[in]- keyCode,keyType IR key code and type.
 ***************************************************************************/
void fill_LastReceivedKey(const char *EvtHandlerName, char *gLastEvent ,double keyTime, int keyCode = 0 ,int keyType = 0)
{
	DEBUG_PRINT(DEBUG_LOG,"fill_LastReceivedKey --->Entry \n");
	LastKeyCode=keyCode;
	LastKeyType=keyType;
	LastKeyTime=keyTime;
	gLastEvent = LastEvent;
	DEBUG_PRINT(DEBUG_LOG, "LastEvent: %s LastKeyCode: 0x%x LastKeyType: 0x%x LastKeyTime: %lf seconds\r\n",gLastEvent, keyCode, keyType, keyTime);

	if(gRegisteredEventCount > 1) {
		DEBUG_PRINT(DEBUG_LOG, "Registered for more than one event: %d \n ", gRegisteredEventCount);
		char TempEventSummary[200] ;

		if(strcmp(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY") == 0)
			sprintf(TempEventSummary, "%s, %s, %x, %x, %lf::", EvtHandlerName, LastEvent, LastKeyType, LastKeyCode, LastKeyTime);
		else
			sprintf(TempEventSummary, "%s, %s, %lf::", EvtHandlerName, LastEvent, LastKeyTime);

		strcat( gEventSummary, TempEventSummary);
		gEventSummaryCount++;
		DEBUG_PRINT(DEBUG_LOG, "gEventSummary: %s\n\n", gEventSummary);
	}else {
		DEBUG_PRINT(DEBUG_LOG, "Registered for only one event : %d \n ", gRegisteredEventCount);
	}

	DEBUG_PRINT(DEBUG_LOG,"fill_LastReceivedKey --->Exit \n");
}

/***************************************************************************
 * Function Name : _PWRMGRevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of PWR events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _PWRMGRevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	DEBUG_PRINT(DEBUG_ERROR,"Entered _PWRMGRevtHandler\n");

	struct timespec clock_at_recv_PWRMgr;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_PWRMgr) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Failed to get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"Got event received time\n");
	}

	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_PWRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_PWRMGR_EVENT_MODECHANGED:
				{
					IARM_Bus_PWRMgr_EventData_tp *param = (IARM_Bus_PWRMgr_EventData_tp *)data;
					DEBUG_PRINT(DEBUG_LOG,"Event IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",param->data.state.curState, param->data.state.newState);
					double keyTime = 0.0;

					keyTime = ((double)(clock_at_recv_PWRMgr.tv_sec - param->data.state.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_PWRMgr.tv_nsec - param->data.state.clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of PWRMgr was %lf seconds\r\n", keyTime);

					strcpy(LastEvent , "IARM_BUS_PWRMGR_EVENT_MODECHANGED");
					fill_LastReceivedKey(__func__, LastEvent, keyTime);
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"Unindentified event\n");
				}
				break;
		}
	}
	
	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
}

/***************************************************************************

 * Function Name : _IRevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of IR events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */


void _IRevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	DEBUG_PRINT(DEBUG_ERROR,"Entered _IRevtHandler\n");

	struct timespec clock_at_recv_event;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_event) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Failed to get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"Got event received time\n");
	}

	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_IRMGR_EVENT_IRKEY:
				{
					IRMgr_EventData_tp *irEventData = (IRMgr_EventData_tp*)data;
					int keyCode = irEventData->data.irkey.keyCode;
					int keyType = irEventData->data.irkey.keyType;
					
					double keyTime = 0.0;

					/*Convert Received and Expected data to Hexa format for comparision*/
					char TempRecvKeyCode[10], TempRecvKeyType[10], TempExpectedKeyCode[10],TempExpectedKeyType[10];
					sprintf(TempRecvKeyCode, "%x",irEventData->data.irkey.keyCode);
					sprintf(TempRecvKeyType, "%x",irEventData->data.irkey.keyType);
					sprintf(TempExpectedKeyCode, "%x", ExpectedKeyCode);
					sprintf(TempExpectedKeyType, "%x", ExpectedKeyType);
					DEBUG_PRINT(DEBUG_LOG,"Received : %s, %s \n\n", TempRecvKeyCode, TempRecvKeyType);
					DEBUG_PRINT(DEBUG_LOG,"Expected Data: %s, %s \n\n", TempExpectedKeyCode, TempExpectedKeyType);
					
					/* Verify the reeived event */
					if ( (strcmp(TempRecvKeyCode, TempExpectedKeyCode) == 0) && (strcmp(TempRecvKeyType,TempExpectedKeyType) == 0))
					{
						keyTime = ((double)(clock_at_recv_event.tv_sec - irEventData->data.irkey.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - irEventData->data.irkey.clock_when_event_sent.tv_nsec)) / (double)BILLION;
						DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of IR key 0x%x type 0x%x was %lf seconds\r\n",keyCode, keyType, keyTime);

						DEBUG_PRINT(DEBUG_LOG,"Test Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
						strcpy(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY");
						fill_LastReceivedKey(__func__, LastEvent,keyTime,keyCode,keyType);
					} else {
						DEBUG_PRINT(DEBUG_LOG,"Recevived Unexpected IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
					}
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"Unindentified event\n");
				}
				break;
		}

	}

	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
}

/***************************************************************************
 * Function Name : _IBUSevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of IARMBUS events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _IBUSevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	DEBUG_PRINT(DEBUG_ERROR,"Entered _IBUSevtHandler\n");

	struct timespec clock_at_recv_RC;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_RC) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Failed to get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"Got event received time\n");
	}

	double keyTime = 0;
	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_DAEMON_NAME) == 0) {
		switch (eventId) {
			case IARM_BUS_EVENT_RESOLUTIONCHANGE:
				{
					DEBUG_PRINT(DEBUG_LOG,"Resolution Change event received\n");
					IARM_Bus_ResolutionChange_EventData_tp *eventData_bus1 = (IARM_Bus_ResolutionChange_EventData_tp*)data ;
					
					DEBUG_PRINT(DEBUG_LOG,"Received Width & Height : %d, %d \n\n", eventData_bus1->width, eventData_bus1->height);

					keyTime = ((double)(clock_at_recv_RC.tv_sec - eventData_bus1->clock_when_event_sent.tv_sec) + (double)(clock_at_recv_RC.tv_nsec - eventData_bus1->clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for Receviving ResourceAvailable event : %lf seconds\r\n", keyTime);
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOLUTIONCHANGE");
					fill_LastReceivedKey(__func__, LastEvent, keyTime);
				}
				break;
			case IARM_BUS_EVENT_RESOURCEAVAILABLE:
				{
					DEBUG_PRINT(DEBUG_LOG,"ResourceAvailable event received\n");
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOURCEAVAILABLE");
					fill_LastReceivedKey(__func__,LastEvent, keyTime);
				}
			default:
				break;
		}
	}

	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
}

/***************************************************************************
 * Function Name : _DUMMYTestMgrevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of DUMMY events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _DUMMYTestMgrevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	DEBUG_PRINT(DEBUG_LOG, "Entered _DUMMYTestMgrevtHandler\n");

	struct timespec clock_at_recv_event;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_event) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Failed to get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"Got event received time\n");
	}

	double EvtTime = 0.0;
	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_DUMMYMGR_NAME) == 0) {
		/* Handle events here */
		IARM_Bus_DUMMYMGR_EventData_t *eventData = (IARM_Bus_DUMMYMGR_EventData_t *)data;
		
		switch(eventId) {
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYX:
			DEBUG_PRINT(DEBUG_LOG,"Received Event X: %s",eventData->data.dummy0.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"Received Event - X : IARM_BUS_DUMMYMGR_EVENT_DUMMYX \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy0.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy0.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYX");
			fill_LastReceivedKey(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving EVENT_DUMMYX was %lf seconds\r\n",EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYY:
			DEBUG_PRINT(DEBUG_LOG,"Received Event Y: %s",eventData->data.dummy1.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"Received Event - Y : IARM_BUS_DUMMYMGR_EVENT_DUMMYY \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy1.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy1.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYY");
			fill_LastReceivedKey(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving EVENT_DUMMYY was %lf seconds\r\n",EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYZ:
			DEBUG_PRINT(DEBUG_LOG,"Received Event Z: %s",eventData->data.dummy2.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"Received Event - Z : IARM_BUS_DUMMYMGR_EVENT_DUMMYZ \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy2.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy2.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYZ");
			fill_LastReceivedKey(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving EVENT_DUMMYZ was %lf seconds\r\n",EvtTime);
			break;
		}
	}

	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
}


/**************************************************************************
 * Function Name	: fillSystemStateDetails
 * Description	: fillSystemStateDetails function is to fill the last recived  
 *		  system state details in the global variable.
 *
 * @param[in]- keyCode,keyType IR key code and type.
 ***************************************************************************/

void fillSystemStateDetails(int state ,int error, char *payload)
{
	DEBUG_PRINT(DEBUG_TRACE,"fillSystemStateDetails --->Entry \n");
	gSysState=state;
	gSysError=error;
	strcpy(gSysPayload , payload);
	gsysMgrdata << "State:" << state << "::Error:" << error << "::Payload:"	<< payload;
	DEBUG_PRINT(DEBUG_TRACE,"gsysMgrdata=%s\n",gsysMgrdata.str().c_str());
	DEBUG_PRINT(DEBUG_TRACE,"fillSystemStateDetails --->Exit \n");
}

/***************************************************************************
 * Function Name : _evtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

/*Hard-coded event handler*/

void _evtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	DEBUG_PRINT(DEBUG_LOG, "Entered _evtHandler\n");

	struct timespec clock_at_recv_event;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_event) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Failed to get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"Got event received time\n");
	}

	double EvtTime = 0.0;

	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_PWRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_PWRMGR_EVENT_MODECHANGED:
				{
					IARM_Bus_PWRMgr_EventData_tp *param = (IARM_Bus_PWRMgr_EventData_tp *)data;
					DEBUG_PRINT(DEBUG_LOG,"\nEvent IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",param->data.state.curState, param->data.state.newState);
					double keyTime = 0.0;
					keyTime = ((double)(clock_at_recv_event.tv_sec - param->data.state.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - param->data.state.clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of PWRMgr was %lf seconds\r\n", keyTime);

					strcpy(LastEvent , "IARM_BUS_PWRMGR_EVENT_MODECHANGED");
					fill_LastReceivedKey(__func__,LastEvent, keyTime);
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"Unindentified event\n");
				}
				break;
		}
	}
	else if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_IRMGR_EVENT_IRKEY:
				{
					IRMgr_EventData_tp *irEventData = (IRMgr_EventData_tp*)data;
					int keyCode = irEventData->data.irkey.keyCode;
					int keyType = irEventData->data.irkey.keyType;
					
					double keyTime = 0.0;

					DEBUG_PRINT(DEBUG_LOG,"irEventData: %p", data);

					if ( ExpectedKeyCode == irEventData->data.irkey.keyCode && ExpectedKeyType == irEventData->data.irkey.keyType)
					{

						keyTime = ((double)(clock_at_recv_event.tv_sec - irEventData->data.irkey.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - irEventData->data.irkey.clock_when_event_sent.tv_nsec)) / (double)BILLION;
						DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of IR key 0x%x type 0x%x was %lf seconds\r\n",keyCode, keyType, keyTime);
						DEBUG_PRINT(DEBUG_LOG,"Test Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
						strcpy(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY");
						fill_LastReceivedKey(__func__,LastEvent,keyTime,keyCode,keyType);
					} else {
						DEBUG_PRINT(DEBUG_LOG,"Recevived Unexpected IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
					}
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"Unindentified event\n");
				}
				break;
		}
	}
	else if (strcmp(owner, IARM_BUS_DAEMON_NAME) == 0) {
		switch (eventId) {
			case IARM_BUS_EVENT_RESOURCEAVAILABLE:
				{
					DEBUG_PRINT(DEBUG_LOG,"ResourceAvailable event received\n");
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOURCEAVAILABLE");
				}
				break;
			case IARM_BUS_EVENT_RESOLUTIONCHANGE:
				{
					double keyTime = 0.0;
					DEBUG_PRINT(DEBUG_LOG,"Resolution Change event received\n");
					IARM_Bus_ResolutionChange_EventData_tp *eventData_bus1 = (IARM_Bus_ResolutionChange_EventData_tp*)data ;
					DEBUG_PRINT(DEBUG_LOG,"Received Width & Height : %d, %d \n\n", eventData_bus1->width, eventData_bus1->height);
					keyTime = ((double)(clock_at_recv_event.tv_sec - eventData_bus1->clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData_bus1->clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for Receviving ResourceAvailable event : %lf seconds\r\n", keyTime);
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOLUTIONCHANGE");
					fill_LastReceivedKey(__func__,LastEvent, keyTime);
				}
			default:
				break;
		}
	}
	else if (strcmp(owner, IARM_BUS_SYSMGR_NAME) == 0)
        {
		strcpy(g_ManagerName,IARM_BUS_SYSMGR_NAME);
                switch (eventId)
                {
                        case IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE:
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Sys Manager System State event received\n");
                                strcpy(LastEvent , "IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE");
				break;
                        }
                        case IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_REQUEST:
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Sys Manager XUPNP Data Request event received\n");
                                strcpy(LastEvent , "IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_REQUEST");
				break;
                        }
                        case IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_UPDATE:
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Sys Manager XUPNP Data Update event received\n");
                                strcpy(LastEvent , "IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_UPDATE");
				break;
                        }
                        case IARM_BUS_SYSMGR_EVENT_CARD_FWDNLD:
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Sys Manager Card FW Dwld event received\n");
                                strcpy(LastEvent , "IARM_BUS_SYSMGR_EVENT_CARD_FWDNLD");
				break;
                        }
                        case IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE:
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Sys Manager HDCP Profile update event received\n");
                                strcpy(LastEvent , "IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE");
				break;
                        }
                }
        }
	/*The below code block is for handling thr test app scenario*/
	else if (strcmp(owner, IARM_BUS_DUMMYMGR_NAME) == 0) {
		DEBUG_PRINT(DEBUG_TRACE,"Inside DummyMgr event handler\n");
		int dummydata=0;
                char evtname;
		strcpy(g_ManagerName,IARM_BUS_DUMMYMGR_NAME);

		/* Handle events here */
                IARM_Bus_DUMMYMGR_EventData_t *eventData = (IARM_Bus_DUMMYMGR_EventData_t *)data;
		switch(eventId) {
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYX:
                        DEBUG_PRINT(DEBUG_LOG,"Data received from event X: %s",eventData->data.dummy0.dummyData);
			if(strncmp(dummydata_x,eventData->data.dummy0.dummyData,DATA_LEN)==0)
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Data received matches dummydata_x: %s",dummydata_x);
                        }

			evtname='X';
			DEBUG_PRINT(DEBUG_LOG,"Received Event - X : IARM_BUS_DUMMYMGR_EVENT_DUMMYX \r\n");

			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy0.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy0.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYX");
			fill_LastReceivedKey(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receiving EVENT_DUMMYX was %lf seconds\r\n",EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYY:
                        DEBUG_PRINT(DEBUG_LOG,"Data received from event Y: %s",eventData->data.dummy1.dummyData);
			if(strncmp(dummydata_y,eventData->data.dummy1.dummyData,DATA_LEN)==0)
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Data received matches dummydata_y: %s",dummydata_y);
                        }

			evtname='Y';
			DEBUG_PRINT(DEBUG_LOG,"Received Event - Y : IARM_BUS_DUMMYMGR_EVENT_DUMMYY \r\n");
					
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy1.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy1.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYY");
			fill_LastReceivedKey(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving EVENT_DUMMYY was %lf seconds\r\n",EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYZ:
                        DEBUG_PRINT(DEBUG_LOG,"Data received from event Z: %s",eventData->data.dummy2.dummyData);
			if(strncmp(dummydata_z,eventData->data.dummy2.dummyData,DATA_LEN)==0)
                        {
                                DEBUG_PRINT(DEBUG_LOG,"Data received matches dummydata_z: %s",dummydata_z);
                        }

			evtname='Z';
			DEBUG_PRINT(DEBUG_LOG,"Received Event - Z : IARM_BUS_DUMMYMGR_EVENT_DUMMYZ \r\n"); // TWC Change-2

                	/* Removing lock when event is received by stub*/
                	pthread_mutex_lock(&lock);
                	pthread_cond_signal(&cond);
                	pthread_mutex_unlock(&lock);

			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy2.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy2.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYZ");
			fill_LastReceivedKey(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving EVENT_DUMMYZ was %lf seconds\r\n",EvtTime);
			break;
		}

		if (g_iter < EVTDATA_MAX_SIZE)
		{
			g_evtName[g_iter]=evtname;
			g_evtData[g_iter++]=dummydata;
			if(g_iter==EVTDATA_MAX_SIZE)
			{
				g_iter=0;
			}
		}
	}
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_RegisterEventHandler
 * Description	: IARMBUSAgent_RegisterEventHandler wrapper function will be used to call 
 *	          IARMBUS API "IARM_Bus_RegisterEventHandler".
 *
 * @param [in] req- has "event_id" and "owner_name" which are input to IARM_Bus_RegisterEventHandler.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_RegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RegisterEventHandler --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["event_id"]==NULL || &req["owner_name"]==NULL || &req["evt_handler"]==NULL)
	{
		return;
	}

	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();
        char *eventhandler=(char*)req["evt_handler"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"IARM_Bus_RegisterEventHandler [Owner: %s Event Id: %d]\n", ownerName, eventId);
	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
        if (strcmp(eventhandler,"NULL")==0)
        {
                retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, NULL);
        }
        else
        {
                retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandler);
                if( retval && !iarmMgrStatus(ownerName) )
        	{
                	DEBUG_PRINT(DEBUG_ERROR,"Given IARM Mgr is not running\n");
        	}
        }

	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RegisterEventHandler --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_UnRegisterEventHandler
 * Description	: IARMBUSAgent_UnRegisterEventHandler wrapper function will be used to call IARMBUS API 
 *		  "IARM_Bus_UnRegisterEventHandler".
 *
 * @param [in] req- has "event_id" and "owner_name" which are input to IARM_Bus_UnRegisterEventHandler.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_UnRegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_UnRegisterEventHandler --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["event_id"]==NULL || &req["owner_name"]==NULL)
	{
		return;
	}
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"IARM_Bus_UnRegisterEventHandler [Owner: %s Event Id: %d]\n", ownerName, eventId);
	/*Calling IARMBUS API IARM_Bus_UnRegisterEventHandler */
	retval=IARM_Bus_UnRegisterEventHandler(ownerName,(IARM_EventId_t)eventId);
	/*Checking the return value of API*/
        if( retval && !iarmMgrStatus(ownerName) )
        {
        	DEBUG_PRINT(DEBUG_ERROR,"Given IARM Mgr is not running\n");
        }

	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_UnRegisterEventHandler --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_GetContext
 * Description	: IARMBUSAgent_GetContext wrapper function will be used to call IARMBUS API
 *		  "IARM_Bus_GetContext".
 *
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 *
 *****************************************************************************/

void IARMBUSAgent::IARMBUSAgent_GetContext(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_GetContext --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_INVALID_STATE;
	char *resultDetails;
	void **context=NULL;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_GetContext from IARMBUSAgent_GetContext \n");
	/*Calling IARMBUS API IARM_Bus_GetContext */
	retval=IARM_Bus_GetContext(context);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_GetContext --->Exit \n");
	return;
}


/**************************************************************************
 * Function Name : IARMBUSAgent_RegisterCall
 * Description	: IARMBUSAgent_RegisterCall wrapper function will be used to call 
 *		  IARMBUS API "IARM_Bus_RegisterCall".
 *
 * @param [in] req- has "owner_name" which is input to IARM_Bus_RegisterCall
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_RegisterCall(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RegisterCall --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterCall from IARMBUSAgent_RegisterCall \n");
	if(&req["owner_name"]==NULL)
	{
		return;
	}
	char *ownerName=(char*)req["owner_name"].asCString();

	/*Calling IARMBUS API IARM_Bus_RegisterCall  */
        DEBUG_PRINT(DEBUG_LOG,"IARM_Bus_RegisterCall for %s\n", ownerName);
	retval=IARM_Bus_RegisterCall(ownerName,_ReleaseOwnership);

	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);

	/* TWC-change : RegisterCall API called */
	REGISTERCALLSTATUS = 1;

	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RegisterCall --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name : IARMBUSAgent_RegisterEvent
 * Description	: IARMBUSAgent_RegisterEvent wrapper function will be used to call 
 *		  IARMBUS API "IARM_Bus_RegisterEvent".
 *
 * @param [in] req- has "max_event" which is input to IARM_Bus_RegisterEvent
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/

void IARMBUSAgent::IARMBUSAgent_RegisterEvent(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RegisterEvent --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEvent from IARMBUSAgent_RegisterEvent \n");
	if(&req["max_event"]==NULL)
	{
		return;
	}
	int maxevent=req["max_event"].asInt();
	/*Calling IARMBUS API IARM_Bus_RegisterEvent  */
	retval=IARM_Bus_RegisterEvent((IARM_EventId_t)maxevent);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RegisterEvent --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_BroadcastEvent
 * Description	: IARMBUSAgent_BroadcastEvent wrapper function will be used to call IARMBUS 
 *		  API "IARM_Bus_BroadcastEvent".
 * @param [in] req- has three types of inputs for three types events such as IR,POWER and 
 *	BUS_DAEMON events.req contains 	
 *	owner_name - Owner of the event.
 *	event_id - The event which is going to be broadcasted.
 *	keyType[IR] , keyCode[IR] - IR key codes.
 *	newState [POWER] - Decoder state will change to state which is mentioned newState. 
 *	resource_type [BUS_BAEMON] - type of resource.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BroadcastEvent --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["event_id"]==NULL ||&req["owner_name"]==NULL || &req["keyType"]==NULL || &req["keyCode"]==NULL || 
	   &req["newState"]==NULL ||&req["resource_type"]==NULL)
	{
		return;
	}
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();

	DEBUG_PRINT(DEBUG_ERROR,"Broadcast event id: %d from %s\n", eventId, ownerName);

	if(strcmp(ownerName,IARM_BUS_IRMGR_NAME)==0)
	{	
		IARM_Bus_IRMgr_EventData_t eventData;
		eventData.data.irkey.keyType = req["keyType"].asInt();
		eventData.data.irkey.keyCode = req["keyCode"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_BroadcastEvent from IARMBUSAgent_BroadcastEvent \n");
		/*Calling IARMBUS API IARM_Bus_BroadcastEvent  */
		retval=IARM_Bus_BroadcastEvent(ownerName,(IARM_EventId_t)eventId,(void*)&eventData,sizeof(eventData));
	}
	else if(strcmp(ownerName,IARM_BUS_PWRMGR_NAME)==0)
	{
		IARM_Bus_PWRMgr_EventData_t eventData;
		eventData.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t)req["newState"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_BroadcastEvent from IARMBUSAgent_BroadcastEvent \n");
		/*Calling IARMBUS API IARM_Bus_BroadcastEvent  */
		retval=IARM_Bus_BroadcastEvent(ownerName,(IARM_EventId_t)eventId,(void*)&eventData,sizeof(eventData));
	}
	else if(strcmp(ownerName,IARM_BUS_DAEMON_NAME)==0)
	{
		IARM_Bus_EventData_t  eventData;
		eventData.resrcType = (IARM_Bus_ResrcType_t)req["resource_type"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_BroadcastEvent from IARMBUSAgent_BroadcastEvent \n");
		/*Calling IARMBUS API IARM_Bus_BroadcastEvent  */
		retval=IARM_Bus_BroadcastEvent(ownerName,(IARM_EventId_t)eventId,(void*)&eventData,sizeof(eventData));
	}
	else if(strcmp(ownerName,IARM_BUS_SYSMGR_NAME)==0)
	{
		IARM_Bus_SYSMgr_EventData_t eventData;
		if (eventId == IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE)
		{
			gstateId=(IARM_Bus_SYSMgr_SystemState_t)req["newState"].asInt();
			eventData.data.systemStates.stateId = (IARM_Bus_SYSMgr_SystemState_t)req["newState"].asInt();
			eventData.data.systemStates.state = req["state"].asInt();
			eventData.data.systemStates.error = req["error"].asInt();
			strcpy(eventData.data.systemStates.payload , req["payload"].asCString());
		}
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_BroadcastEvent from IARMBUSAgent_BroadcastEvent \n");
		/*Calling IARMBUS API IARM_Bus_BroadcastEvent  */
		retval=IARM_Bus_BroadcastEvent(ownerName,(IARM_Bus_SYSMgr_EventId_t)eventId,(void*)&eventData,sizeof(eventData));
	}
  
	/*Checking the return value of API*/
        if( retval && !iarmMgrStatus(ownerName) )
        {
        	DEBUG_PRINT(DEBUG_ERROR,"Given IARM Mgr is not running\n");
        }

	/*Filling json response with SUCCESS status*/
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BroadcastEvent --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_BusCall
 * Description	: IARMBUSAgent_BusCall wrapper function will be used to call IARMBUS API "IARM_Bus_Call".
 * @param [in] req- has three types of inputs for three types events such as IR,POWER and BUS_DAEMON events.
 *	req contains 	
 *	owner_name - Owner of the event.
 *       methodName - Name of the RPC method
 *	event_id - The event which is going to be broadcasted.
 *	set_timeout[IR] - keyRepeatInterval.
 *	newState [POWER] - Decoder state will change to state which is mentioned newState. 
 * 	resource_type [BUS_BAEMON] - type of resource.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 *
 ***************************************************************************/	

void IARMBUSAgent::IARMBUSAgent_BusCall(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BusCall --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
        if(&req["method_name"]==NULL ||&req["owner_name"]==NULL || &req["set_timeout"]==NULL || &req["newState"]==NULL ||
           &req["resource_type"]==NULL ||&req["testapp_API0_data"]==NULL ||&req["testapp_API1_data"]==NULL)
	{
		return;
	}
	char *ownerName=(char*)req["owner_name"].asCString();
	char *methodName=(char*)req["method_name"].asCString();

	DEBUG_PRINT(DEBUG_ERROR,"BusCall method: %s owner: %s\n", methodName, ownerName);

	if(strcmp(ownerName,IARM_BUS_IRMGR_NAME)==0)
	{	
		char *RepeatInterval=(char*)malloc(sizeof(char)*5);
		IARM_Bus_IRMgr_SetRepeatInterval_Param_t param_Set;
		param_Set.timeout=(unsigned int)req["set_timeout"].asInt();
		IARM_Bus_IRMgr_GetRepeatInterval_Param_t param_Get;
		DEBUG_PRINT(DEBUG_LOG,"IR-calling IARM_Bus_Call from IARM_Bus_Call \n");
		/*Calling IARMBUS API IARM_Bus_Call  */
		if(strcmp(methodName,"GetRepeatInterval")==0)
		{		
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Get,sizeof(param_Get));
			if(retval==0)
			{
				sprintf(RepeatInterval,"%d",param_Get.timeout);
				response["details"]= RepeatInterval;
				DEBUG_PRINT(DEBUG_LOG,"IR-Current RepeatInterval is :%s\n",RepeatInterval);
			}
		}
		else
		{	
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Set,sizeof(param_Set));
			if(retval==0)
			{
				sprintf(RepeatInterval,"%d",param_Set.timeout);
				response["details"]= RepeatInterval;
				DEBUG_PRINT(DEBUG_LOG,"SetRepeatInterval:%s\n",response["details"].asCString()) ;
			}	
		}
		/*Checking the return value of API*/
		/*Filling json response with SUCCESS status*/	
		response["result"]=getResult(retval,resultDetails);
		if(retval!=0)
		{
			response["details"]=resultDetails;
		}
                free(RepeatInterval);
	}
	else if(strcmp(ownerName,IARM_BUS_PWRMGR_NAME)==0)
	{
		IARM_Bus_PWRMgr_GetPowerState_Param_t param_Get;
		IARM_Bus_PWRMgr_SetPowerState_Param_t param_Set;
		param_Set.newState = (IARM_Bus_PWRMgr_PowerState_t)req["newState"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"PWR-calling IARM_Bus_Call from IARM_Bus_Call \n");
		DEBUG_PRINT(DEBUG_LOG,"PWR-New power state is :%d\n",param_Set.newState);
		if(strcmp(methodName,"GetPowerState")==0)
		{		
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Get,sizeof(param_Get));
			switch(param_Get.curState)
			{
				case 0:	response["details"]="POWERSTATE_OFF";
					break;
				case 1:	response["details"]="POWERSTATE_STANDBY";
					break;
				case 2:	response["details"]="POWERSTATE_ON";
					break;
				default:
					response["details"]="Unknown State";			 			
			}
			DEBUG_PRINT(DEBUG_LOG,"PWR-Current power state is:%d-%s\n",param_Get.curState,response["details"].asCString());
		}
          	else if (strcmp(methodName,"WareHouseReset")==0)
                {
                  	IARM_Bus_PWRMgr_WareHouseReset_Param_t param_WareHouse;
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_WareHouse,sizeof(param_WareHouse));
                  	DEBUG_PRINT(DEBUG_LOG,"WareHouseReset returned %d\n", retval);
                  	if( 0 == retval)
                        {
                          response["details"]="IARM_RESULT_SUCCESS";
                        }
                  	else 
                        {
                          response["details"]="IARM_RESULT_IPCCORE_FAIL";
                        }
                }
		else
		{
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Set,sizeof(param_Set));
			DEBUG_PRINT(DEBUG_LOG,"State after bus call is:%d\n",param_Set.newState);
			switch(param_Set.newState)
			{
				case 0:	response["details"]="POWERSTATE_OFF";
					break;
				case 1:	response["details"]="POWERSTATE_STANDBY";
					break;
				case 2:	response["details"]="POWERSTATE_ON";
					break;
				default:
					response["details"]="Unknown State";			 			
			}
		}
		/*Checking the return value of API*/
		/*Filling json response with SUCCESS status*/
		response["result"]=getResult(retval,resultDetails);
		if(retval!=0)
		{
			response["details"]=resultDetails;
		}
	}
	else if(strcmp(ownerName,IARM_BUS_DAEMON_NAME)==0)
	{
		IARM_Bus_EventData_t  eventData;
		eventData.resrcType = (IARM_Bus_ResrcType_t)req["resource_type"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"BUS-calling IARM_Bus_Call from IARM_Bus_Call \n");
		/*Calling IARMBUS API IARM_Bus_Call  */
		retval=IARM_Bus_Call(ownerName,methodName,(void*)&eventData,sizeof(eventData));
		/*Checking the return value of API*/
		/*Filling json response with SUCCESS status*/	
		response["result"]=getResult(retval,resultDetails);
		response["details"]=resultDetails;
	}
	else if(strcmp(ownerName,IARM_BUS_MFRLIB_NAME)==0)
	{
		if(strcmp(methodName,IARM_BUS_MFRLIB_API_GetSerializedData)==0)
		{
			char* mfrdetails=(char*)malloc(sizeof(char)*MAX_SERIALIZED_BUF);
			memset(mfrdetails , '\0', (sizeof(char)*MAX_SERIALIZED_BUF));
			/*Calling IARMBUS API IARM_Bus_Call  */
			IARM_Bus_MFRLib_GetSerializedData_Param_t param;
			param.bufLen = MAX_SERIALIZED_BUF;
			DEBUG_PRINT(DEBUG_LOG, "Valid type values: MANUFACTURER=0,MANUFACTUREROUI=1,MODELNAME=2,DESCRIPTION=3,\nPRODUCTCLASS=4,SERIALNUMBER=5,HARDWAREVERSION=6,SOFTWAREVERSION=7,\nPROVISIONINGCODE=8,FIRSTUSEDATE=9,DEVICEMAC=10,MOCAMAC=11,HDMIHDCP=12\n");
			param.type = (mfrSerializedType_t)req["mfr_param_type"].asInt();
			DEBUG_PRINT(DEBUG_LOG,"MFR-calling IARM_Bus_Call of type: %d\n", param.type);
			retval=IARM_Bus_Call(ownerName,IARM_BUS_MFRLIB_API_GetSerializedData,(void*)&param, sizeof(param));
                  	DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_Call return code:%d\n",retval);
			memcpy(mfrdetails,param.buffer,param.bufLen);
			DEBUG_PRINT(DEBUG_LOG,"Value: %s\n",mfrdetails);
			/*Checking the return value of API*/
			/*Filling json response with SUCCESS status*/
			response["result"]=getResult(retval,resultDetails);
			response["details"]=mfrdetails;
			free(mfrdetails);
		}
		else if(strcmp(methodName,IARM_BUS_MFRLIB_API_WriteImage)==0)
                {
                        IARM_Bus_MFRLib_WriteImage_Param_t param;
                        const char* imgname=(char*)req["imagename"].asCString();
                        const char* imgpath=(char*)req["imagepath"].asCString();
                        strcpy(param.name,imgname);
                        strcpy(param.path,imgpath);
                        strcpy(param.callerModuleName,"TDK_agent");
                        param.interval = 2;
                        param.type = mfrIMAGE_TYPE_CDL;
                        strcpy(param.cbData,"Test Success");
			DEBUG_PRINT(DEBUG_TRACE,"imagename=%s imagepath=%s\n",imgname,imgpath);
                        retval=IARM_Bus_Call(ownerName,methodName,(void*)&param, sizeof(param));
                  	DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_Call return code:%d\n",retval);
                        response["result"]=getResult(retval,resultDetails);
                        response["details"]=resultDetails;
                }
		else if ((strcmp(methodName,IARM_BUS_MFRLIB_API_ScrubAllBanks)==0) || (strcmp(methodName,IARM_BUS_MFRLIB_API_DeletePDRI)==0))
		{
			char param;
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param, sizeof(param));
                  	DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_Call return code:%d\n",retval);
                        response["result"]=getResult(retval,resultDetails);
                        response["details"]=resultDetails;
		}	
	}
	else if(strcmp(ownerName,IARM_BUS_SYSMGR_NAME)==0)
	{
		if(strcmp(methodName,"GetSystemStates")==0)
		{
			IARM_Bus_SYSMgr_GetSystemStates_Param_t param;
			retval=IARM_Bus_Call(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_API_GetSystemStates,&param,sizeof(param));
			response["result"]=getResult(retval,resultDetails);
			switch(gstateId) {
				case IARM_BUS_SYSMGR_SYSSTATE_CHANNELMAP:
					fillSystemStateDetails(param.channel_map.state,param.channel_map.error,param.channel_map.payload);
					break;
				case IARM_BUS_SYSMGR_SYSSTATE_DISCONNECTMGR:
					fillSystemStateDetails(param.disconnect_mgr_state.state,param.disconnect_mgr_state.error,param.disconnect_mgr_state.payload);
					break;
				case IARM_BUS_SYSMGR_SYSSTATE_TUNEREADY:
					fillSystemStateDetails(param.TuneReadyStatus.state,param.TuneReadyStatus.error,param.TuneReadyStatus.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_EXIT_OK :
					fillSystemStateDetails(param.exit_ok_key_sequence.state,param.exit_ok_key_sequence.error,param.exit_ok_key_sequence.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_CMAC :
					fillSystemStateDetails(param.cmac.state,param.cmac.error,param.cmac.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_MOTO_ENTITLEMENT :
					fillSystemStateDetails(param.card_moto_entitlements.state,param.card_moto_entitlements.error,param.card_moto_entitlements.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_MOTO_HRV_RX :
					fillSystemStateDetails(param.card_moto_hrv_rx.state,param.card_moto_hrv_rx.error,param.card_moto_hrv_rx.payload);
					break;
				case IARM_BUS_SYSMGR_SYSSTATE_DAC_INIT_TIMESTAMP :
					fillSystemStateDetails(param.dac_init_timestamp.state,param.dac_init_timestamp.error,param.dac_init_timestamp.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_CARD_CISCO_STATUS :
					fillSystemStateDetails(param.card_cisco_status.state,param.card_cisco_status.error,param.card_cisco_status.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_VIDEO_PRESENTING :
					fillSystemStateDetails(param.video_presenting.state,param.video_presenting.error,param.video_presenting.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_HDMI_OUT :
					fillSystemStateDetails(param.hdmi_out.state,param.hdmi_out.error,param.hdmi_out.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_HDCP_ENABLED :
					fillSystemStateDetails(param.hdcp_enabled.state,param.hdcp_enabled.error,param.hdcp_enabled.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_HDMI_EDID_READ :
					fillSystemStateDetails(param.hdmi_edid_read.state,param.hdmi_edid_read.error,param.hdmi_edid_read.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_FIRMWARE_DWNLD :
					fillSystemStateDetails(param.firmware_download.state,param.firmware_download.error,param.firmware_download.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_TIME_SOURCE :
					fillSystemStateDetails(param.time_source.state,param.time_source.error,param.time_source.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_TIME_ZONE :
					fillSystemStateDetails(param.time_zone_available.state,param.time_zone_available.error,param.time_zone_available.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_CA_SYSTEM :
					fillSystemStateDetails(param.ca_system.state,param.ca_system.error,param.ca_system.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_ESTB_IP :
					fillSystemStateDetails(param.estb_ip.state,param.estb_ip.error,param.estb_ip.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_ECM_IP :
					fillSystemStateDetails(param.ecm_ip.state,param.ecm_ip.error,param.ecm_ip.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_LAN_IP :
					fillSystemStateDetails(param.lan_ip.state,param.lan_ip.error,param.lan_ip.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_MOCA :
					fillSystemStateDetails(param.moca.state,param.moca.error,param.moca.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_DOCSIS :
					fillSystemStateDetails(param.docsis.state,param.docsis.error,param.docsis.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_DSG_BROADCAST_CHANNEL :
					fillSystemStateDetails(param.dsg_broadcast_tunnel.state,param.dsg_broadcast_tunnel.error,param.dsg_broadcast_tunnel.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_DSG_CA_TUNNEL :
					fillSystemStateDetails(param.dsg_ca_tunnel.state,param.dsg_ca_tunnel.error,param.dsg_ca_tunnel.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_CABLE_CARD :
					fillSystemStateDetails(param.cable_card.state,param.cable_card.error,param.cable_card.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_CABLE_CARD_DWNLD :
					fillSystemStateDetails(param.cable_card_download.state,param.cable_card_download.error,param.cable_card_download.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_CVR_SUBSYSTEM :
					fillSystemStateDetails(param.cvr_subsystem.state,param.cvr_subsystem.error,param.cvr_subsystem.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_DOWNLOAD :
					fillSystemStateDetails(param.download.state,param.download.error,param.download.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_VOD_AD :
					fillSystemStateDetails(param.vod_ad.state,param.vod_ad.error,param.vod_ad.payload);
					break;
				case IARM_BUS_SYSMGR_SYSSTATE_CABLE_CARD_SERIAL_NO:
					fillSystemStateDetails(param.card_serial_no.state,param.card_serial_no.error,param.card_serial_no.payload);
					break;
				case IARM_BUS_SYSMGR_SYSSTATE_ECM_MAC:
					fillSystemStateDetails(param.ecm_mac.state,param.ecm_mac.error,param.ecm_mac.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_DAC_ID :
					fillSystemStateDetails(param.dac_id.state,param.dac_id.error,param.dac_id.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_PLANT_ID :
					fillSystemStateDetails(param.plant_id.state,param.plant_id.error,param.plant_id.payload);
					break;
				case IARM_BUS_SYSMGR_SYSSTATE_STB_SERIAL_NO:
					fillSystemStateDetails(param.stb_serial_no.state,param.stb_serial_no.error,param.stb_serial_no.payload);
					break;
				case   IARM_BUS_SYSMGR_SYSSTATE_BOOTUP :
					fillSystemStateDetails(param.bootup.state,param.bootup.error,param.bootup.payload);
					break;
				default:
					response["details"]="System State received";
					break;
			}
			response["details"]=gsysMgrdata.str().c_str();
			gsysMgrdata.str("");
			gstateId =IARM_BUS_SYSMGR_SYSSTATE_CHANNELMAP;
		}
		else if(strcmp(methodName,"SetHDCPProfile")==0)
		{
			IARM_BUS_SYSMGR_HDCPProfileInfo_Param_t param;
			param.HdcpProfile=req["newState"].asInt();
			DEBUG_PRINT(DEBUG_LOG,"Set HDCP Profile=%d\n", param.HdcpProfile);
			retval=IARM_Bus_Call(IARM_BUS_SYSMGR_NAME,methodName,&param,sizeof(param));
			DEBUG_PRINT(DEBUG_LOG,"SetHDCPProfile return code: %d\n", retval);
			response["result"]=getResult(retval,resultDetails);
			response["details"]=resultDetails;
		}
		else if(strcmp(methodName,"GetHDCPProfile")==0)
		{
			IARM_BUS_SYSMGR_HDCPProfileInfo_Param_t param;
			retval=IARM_Bus_Call(IARM_BUS_SYSMGR_NAME,methodName,&param,sizeof(param));
			DEBUG_PRINT(DEBUG_LOG,"GetHDCPProfile return code: %d Profile=%d\n", retval,param.HdcpProfile);
			response["result"]=getResult(retval,resultDetails);
			if (retval == 0)
			{
				memset(resultDetails, '\0', (sizeof(char)*16));
				sprintf(resultDetails,"%d",param.HdcpProfile);
				response["details"]=resultDetails;
			}
			response["details"]=resultDetails;
		}
		else
		{
			response["result"]="FAILURE";
                        response["details"]="INVALID RPC Call";
		}
	}
	/*This is for testing the test app with bus call*/
        else if(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME)==0)
        {
		char *dummydata = (char*)malloc(sizeof(char*)*15);
		memset(dummydata , '\0', (sizeof(char)*15));
		char *dummydatadetails = (char*)malloc((sizeof(char*)*30));
		memset(dummydatadetails , '\0', (sizeof(char)*30));
		if(strcmp(methodName,"DummyAPI0")==0)
		{
			IARM_Bus_DUMMYMGR_DummyAPI0_Param_t param;
			param.iData0 =req["testapp_API0_data"].asInt();
			retval = IARM_Bus_Call(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_API_DummyAPI0, &param, sizeof(param));
			sprintf(dummydata,"%x",param.iRet0);
			DEBUG_PRINT(DEBUG_LOG,"dummydata:%s",dummydata);
			strcpy(dummydatadetails,"DummyAPI0:");
			strcat(dummydatadetails,dummydata);
			DEBUG_PRINT(DEBUG_LOG,"dummydatadetails:%s",dummydatadetails);
			DEBUG_PRINT(DEBUG_ERROR,"ret value of API-0:%x\n",param.iRet0);
			response["result"]="SUCCESS";
			response["details"]=dummydatadetails;
		}
		if(strcmp(methodName,"DummyAPI1")==0)
		{
			IARM_Bus_DUMMYMGR_DummyAPI1_Param_t param;
			param.iData1 =req["testapp_API1_data"].asInt();
			retval = IARM_Bus_Call(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_API_DummyAPI1, &param, sizeof(param));
			sprintf(dummydata,"%x",param.iRet1);
			DEBUG_PRINT(DEBUG_LOG,"dummydata:%s",dummydata);
			strcat(dummydatadetails,"DummyAPI1:");
			DEBUG_PRINT(DEBUG_LOG,"dummydatadetails:%s",dummydatadetails);
			strcat(dummydatadetails,dummydata);
			DEBUG_PRINT(DEBUG_ERROR,"ret value of API-1:%x\n",param.iRet1);
			response["result"]="SUCCESS";
			response["details"]=dummydatadetails;
		}
		free(dummydata);
		free(dummydatadetails);
        }

        if( retval && !iarmMgrStatus(ownerName) )
        {
        	DEBUG_PRINT(DEBUG_ERROR,"Given IARM Mgr is not running\n");
        }

	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_BusCall --->Exit \n");
	return;
}

/**************************************************************************
 * Function Name	: InvokeSecondApplication
 * Description	: This function is to invoke the second application which does broadcasting 
 different types of events,Requesting and releasing resources.

 ***************************************************************************/
void IARMBUSAgent::InvokeSecondApplication(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"InvokeSecondApplication --->Entry \n");
        if (&req["appname"]==NULL)
        {
                return;
        }

	const char* appname=(char*)req["appname"].asCString();
	const char* argv1=(char*)req["argv1"].asCString();
	const char* apptype=(char*)req["apptype"].asCString();
        int iterationcount=req["iterationcount"].asInt();
        char argv2[8] = {'\0'};
        sprintf(argv2,"%d",iterationcount);

	std::string cmdStr;
	cmdStr = g_tdkPath + "/" + appname + " " + argv1 + + " " + argv2;

	syncCount = 0;
        memset(dummydata_x,'\0',DATA_LEN);
        memset(dummydata_x,'x',DATA_LEN-1);
        strncpy(dummydata_x,argv2,strlen(argv2));
        memset(dummydata_y,'\0',DATA_LEN);
        memset(dummydata_y,'y',DATA_LEN-1);
        strncpy(dummydata_y,argv2,strlen(argv2));
        memset(dummydata_z,'\0',DATA_LEN);
        memset(dummydata_z,'z',DATA_LEN-1);
        strncpy(dummydata_z,argv2,strlen(argv2));

	if (strcmp (apptype, "background") == 0)
	{
		cmdStr = cmdStr + " &";
		DEBUG_PRINT(DEBUG_TRACE, "Executing Second Application : %s\n", cmdStr.c_str());
		try
		{
			system((char *)cmdStr.c_str());
		}
		catch(...)
		{
			DEBUG_PRINT(DEBUG_ERROR,"Exception occured during system call\n");
			DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
			response["result"]="FAILURE";
			return;
		}
	}
	else
	{
                DEBUG_PRINT(DEBUG_TRACE, "Executing Second Application : %s\n", cmdStr.c_str());
		try
		{
			system((char *)cmdStr.c_str());
		}
		catch(...)
		{
			DEBUG_PRINT(DEBUG_ERROR,"Exception occured during system call\n");
			DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
			response["result"]="FAILURE";
			return ;
		}
	}
	DEBUG_PRINT(DEBUG_TRACE,"InvokeSecondApplication --->Exit \n");
	response["result"]="SUCCESS";
	return;
}

/**************************************************************************
 * Function Name : SyncSecondApplication
 * Description	 : RPC method to sync second application
***************************************************************************/
void IARMBUSAgent::SyncSecondApplication(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SyncSecondApplication --->Entry \n");
	syncCount = syncCount+1;

	/* Invoking handler to release lock */
        DEBUG_PRINT(DEBUG_TRACE,"Invoking dummy mgr handler to release lock\n");
        IARM_Bus_Call(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_API_HANDLER_READY, &handler_param, sizeof(handler_param));

	const char* lockenabled =(char*)req["lockenabled"].asCString();

        DEBUG_PRINT(DEBUG_TRACE,"lock: %s\n", lockenabled);
        if (strcmp (lockenabled, "true") == 0)
	{
		if((syncCount % 2) == 1)
		{
			pthread_mutex_lock(&lock);
			pthread_cond_wait(&cond,&lock);
			pthread_mutex_unlock(&lock);
		}
	}

        DEBUG_PRINT(DEBUG_TRACE,"SyncSecondApplication --->Exit \n");
        response["result"]="SUCCESS";
	return;
}


/**************************************************************************
 * Function Name	: fill_LastReceivedKey_Perf
 * Description	: fill_LastReceivedKey_Perf function is to fill the last recived IR 
 *		  key details in the global variable.
 *
 * @param[in]- keyCode,keyType IR key code and type.
 ***************************************************************************/

void fill_LastReceivedKey_Perf(const char *EvtHandlerName, char *gLastEvent ,double keyTime, int keyCode = 0 ,int keyType = 0)
{
	DEBUG_PRINT(DEBUG_LOG,"fill_LastReceivedKey_Perf --->Entry \n");
	LastKeyCode_Perf=keyCode;
	LastKeyType_Perf=keyType;
	LastKeyTime=keyTime;
	gLastEvent = LastEvent;
	DEBUG_PRINT(DEBUG_LOG, "LastEvent: %s LastKeyCode: 0x%x LastKeyType : 0x%x LastKeyTime: %lf seconds\r\n",gLastEvent, keyCode, keyType, keyTime);

	if(gRegisteredEventCount > 1) {
		DEBUG_PRINT(DEBUG_LOG, "Registered for more than one event : %d \n ", gRegisteredEventCount);
		char TempEventSummary[200] ;

		if(strcmp(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY") == 0)
			sprintf(TempEventSummary, "%s, %s, %x, %x, %lf::", EvtHandlerName, LastEvent, LastKeyType_Perf, LastKeyCode_Perf, LastKeyTime);
		else
			sprintf(TempEventSummary, "%s, %s, %lf::", EvtHandlerName, LastEvent, LastKeyTime);

		strcat( gEventSummary, TempEventSummary);
		gEventSummaryCount++;
		DEBUG_PRINT(DEBUG_LOG, "gEventSummary: %s\n\n", gEventSummary);
	}else {
		DEBUG_PRINT(DEBUG_LOG, "Registered for only one event : %d \n ", gRegisteredEventCount);
	}

	DEBUG_PRINT(DEBUG_LOG,"fill_LastReceivedKey_Perf --->Exit \n");
}


/***************************************************************************
 * Function Name : _evtHandler_Perf
 * Description 	: This function is the event handler call back function for handling the 
 different type of events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

/*Hard-coded event handler*/

void _evtHandler_Perf(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
        DEBUG_PRINT(DEBUG_LOG, "Entered _evtHandler_Perf\n");

	struct timespec clock_at_recv_event;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_event) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Failed to get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"Got event received time\n");
	}

	double EvtTime = 0.0;

	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_PWRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_PWRMGR_EVENT_MODECHANGED:
				{
					IARM_Bus_PWRMgr_EventData_tp *param = (IARM_Bus_PWRMgr_EventData_tp *)data;
					DEBUG_PRINT(DEBUG_LOG,"Event IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",param->data.state.curState, param->data.state.newState);
					double keyTime = 0.0;
					keyTime = ((double)(clock_at_recv_event.tv_sec - param->data.state.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - param->data.state.clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of PWRMgr was %lf seconds\r\n", keyTime);

					strcpy(LastEvent , "IARM_BUS_PWRMGR_EVENT_MODECHANGED");
					fill_LastReceivedKey_Perf(__func__,LastEvent, keyTime);
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"Unindentified event\n");
				}
				break;
		}
	}
	else if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_IRMGR_EVENT_IRKEY:
				{
					IRMgr_EventData_tp *irEventData = (IRMgr_EventData_tp*)data;
					int keyCode = irEventData->data.irkey.keyCode;
					int keyType = irEventData->data.irkey.keyType;
					double keyTime = 0.0;

					DEBUG_PRINT(DEBUG_LOG,"irEventData : %p", data);

					if ( ExpectedKeyCode == irEventData->data.irkey.keyCode && ExpectedKeyType == irEventData->data.irkey.keyType)
					{

						keyTime = ((double)(clock_at_recv_event.tv_sec - irEventData->data.irkey.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - irEventData->data.irkey.clock_when_event_sent.tv_nsec)) / (double)BILLION;
						DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of IR key 0x%x type 0x%x was %lf seconds\r\n",keyCode, keyType, keyTime);
						DEBUG_PRINT(DEBUG_LOG,"Test Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
						strcpy(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY");
						fill_LastReceivedKey_Perf(__func__,LastEvent,keyTime,keyCode,keyType);
					} else {
						DEBUG_PRINT(DEBUG_LOG,"Recevived Unexpected IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
					}
					
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"Unindentified event\n");
				}
				break;
		}

	}
	else if (strcmp(owner, IARM_BUS_DAEMON_NAME) == 0) {
		switch (eventId) {
			case IARM_BUS_EVENT_RESOURCEAVAILABLE:
				{
					DEBUG_PRINT(DEBUG_LOG,"ResourceAvailable event received\n");
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOURCEAVAILABLE");
				}
				break;
			case IARM_BUS_EVENT_RESOLUTIONCHANGE:
				{
					double keyTime = 0.0;
					DEBUG_PRINT(DEBUG_LOG,"Resolution Change event received\n");
					IARM_Bus_ResolutionChange_EventData_tp *eventData_bus1 = (IARM_Bus_ResolutionChange_EventData_tp*)data ;
					DEBUG_PRINT(DEBUG_LOG,"Received Width & Height : %d, %d \n\n", eventData_bus1->width, eventData_bus1->height);
					keyTime = ((double)(clock_at_recv_event.tv_sec - eventData_bus1->clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData_bus1->clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for Receviving ResourceAvailable event : %lf seconds\r\n", keyTime);
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOLUTIONCHANGE");
					fill_LastReceivedKey_Perf(__func__,LastEvent, keyTime);
				}
			default:
				break;
		}

	}
	else if (strcmp(owner, IARM_BUS_DUMMYMGR_NAME) == 0) {
		DEBUG_PRINT(DEBUG_LOG,"Inside DummyMgr event handler\n");

		/* Handle events here */
		IARM_Bus_DUMMYMGR_EventData_t *eventData = (IARM_Bus_DUMMYMGR_EventData_t *)data;
		switch(eventId) {
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYX:

			DEBUG_PRINT(DEBUG_LOG,"Received event X: %s",eventData->data.dummy0.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"Received Event - X : IARM_BUS_DUMMYMGR_EVENT_DUMMYX \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy0.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy0.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYX");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYX was %lf seconds\r\n",EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYY:

			DEBUG_PRINT(DEBUG_LOG,"Received event Y: %s",eventData->data.dummy1.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"Received Event - Y : IARM_BUS_DUMMYMGR_EVENT_DUMMYY \r\n");
					
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy1.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy1.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYY");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYY was %lf seconds\r\n",EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYZ:

			DEBUG_PRINT(DEBUG_LOG,"Received event Z: %s",eventData->data.dummy2.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"Received Event - Z : IARM_BUS_DUMMYMGR_EVENT_DUMMYZ \r\n");
						
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy2.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy2.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYZ");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYZ was %lf seconds\r\n",EvtTime);
			break;
		}
	}
}


/***************************************************************************

 * Function Name : _evtHandlerRept1
 * Description 	: This function is the event handler call back function for handling the 
 different type of IR events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _evtHandlerRept1(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{

	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	/* Get the request details*/
	char *ownerName=(char*) owner;

	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d \n", owner, eventId);

	/* Register Corresponding Event Hander for the Event*/
	if(strcmp(ownerName,IARM_BUS_IRMGR_NAME)==0)
	{	
		DEBUG_PRINT(DEBUG_LOG,"Registered for for IR Key Events ... \n");
		_IRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_PWRMGR_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for PWRMGR Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_PWRMGRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_DAEMON_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for IARMBUS DAEMON Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_IBUSevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for DUMMY TEST MANAGER Events ... \n");
		_DUMMYTestMgrevtHandler(owner, eventId, data, len);
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"Registering for All Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_evtHandler_Perf(owner, eventId, data, len);
	}

	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);

}
void _evtHandlerRept2(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{

	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	/* Get the request details*/
	char *ownerName=(char*) owner;

	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	/* Register Corresponding Event Hander for the Event*/
	if(strcmp(ownerName,IARM_BUS_IRMGR_NAME)==0)
	{	
		DEBUG_PRINT(DEBUG_LOG,"Registered for for IR Key Events ... \n");
		_IRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_PWRMGR_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for PWRMGR Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_PWRMGRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_DAEMON_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for IARMBUS DAEMON Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_IBUSevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for DUMMY TEST MANAGER Events ... \n");
		_DUMMYTestMgrevtHandler(owner, eventId, data, len);
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"Registering for All Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_evtHandler_Perf(owner, eventId, data, len);
	}

	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
}

void _evtHandlerRept3(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{

	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	/* Get the request details*/
	char *ownerName=(char*) owner;

	DEBUG_PRINT(DEBUG_LOG,"owner : %s, eventId : %d ", owner, eventId);

	/* Register Corresponding Event Hander for the Event*/
	if(strcmp(ownerName,IARM_BUS_IRMGR_NAME)==0)
	{	
		DEBUG_PRINT(DEBUG_LOG,"Registered for for IR Key Events ... \n");
		_IRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_PWRMGR_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for PWRMGR Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_PWRMGRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_DAEMON_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for IARMBUS DAEMON Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_IBUSevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME)==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"Registered for DUMMY TEST MANAGER Events ... \n");
		_DUMMYTestMgrevtHandler(owner, eventId, data, len);
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"Registering for All Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_evtHandler_Perf(owner, eventId, data, len);
	}

	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
}

/*******************************************************************************************************
 *Function name	: RegisterMultipleEventHandlers
 *Descrption	: RegisterMultipleEventHandlers wrapper function will be used to Register multiple event handler for single event
 *******************************************************************************************************/ 
void IARMBUSAgent::RegisterMultipleEventHandlers(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"Entering %s function", __func__);

	int retval = 0;
	char details[512];
	memset(details, '\0', sizeof(512));
	//IARM_Result_t retCode = IARM_RESULT_SUCCESS;

	if( &req["event_id"]==NULL ||&req["owner_name"]==NULL)
	{
		return;
	}

	/* Get the request details*/
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"Requesting Resource...\n");
	retval=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);

	DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEventHandler from RegisterEventHandler ... \n");
	DEBUG_PRINT(DEBUG_LOG,"ownerName : %s,  eventId : %d \n", ownerName,(IARM_EventId_t)eventId );

	DEBUG_PRINT(DEBUG_LOG,"Registering for IR Key Events ... \n");
	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
	retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept1);

	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEventHandler ... -FAILURE \n");
		/*Filling json response with SUCCESS status*/
		strcpy(details, "IARM_Bus_RegisterEventHandler() FAILED");
		response["result"]="FAILURE";
		response["details"]=details;
		return;
	}

	gRegisteredEventCount++;

	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
	retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept2);

	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEventHandler ... -FAILURE \n");
		/*Filling json response with SUCCESS status*/
		strcpy(details, "IARM_Bus_RegisterEventHandler() FAILED");
		response["result"]="FAILURE";
		response["details"]=details;
		return;
	}

	gRegisteredEventCount++;

	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
	retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept3);

	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"calling IARM_Bus_RegisterEventHandler ... -FAILURE \n");
		/*Filling json response with SUCCESS status*/
		strcpy(details, "IARM_Bus_RegisterEventHandler() FAILED");
		response["result"]="FAILURE";
		response["details"]=details;
		return;
	}

	DEBUG_PRINT(DEBUG_LOG,"Releasing Resource...\n");
	retval = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);

	gRegisteredEventCount ++;
		
	/*Filling json response with SUCCESS status*/
	sprintf(details, "%s Successfully Executed", __func__);
	response["result"]="SUCCESS";
	response["details"]=details;
	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
        return;
}


void IARMBUSAgent::InvokeEventTransmitterApp(IN const Json::Value& req, OUT Json::Value& response)
{
	char details[512];
	memset(details, '\0', sizeof(512));
	DEBUG_PRINT(DEBUG_LOG,"Entering %s function", __func__);

	if(&req["event_id"]==NULL ||&req["owner_name"]==NULL ||&req["evttxappname"]==NULL)
	{
		/*Filling json response with SUCCESS status*/
		strcpy(details, "Invalid Parameters-check owner_name, event_id, evttxappname");
		response["result"]="FAILURE";
		response["details"]=details;
		return;
	}

	pid_t idChild = vfork();

	char * appname=(char*)req["evttxappname"].asCString();
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();
	std::string testenvPath = getenv("OPENSOURCETEST_PATH");
	testenvPath.append("../");

	std::string path = getenv("TDK_PATH");
	path.append("/");
	path.append(appname);
	DEBUG_PRINT(DEBUG_ERROR,"AppPath:%s, appname:%s\n",path.c_str(), appname);

	if(idChild == 0)
	{
		if(strcmp(ownerName,IARM_BUS_IRMGR_NAME)==0)
		{	
			DEBUG_PRINT(DEBUG_LOG,"Condition matched... Owner name as IRMgr\n");
			//std::cout<<"\n KeyCode :"<< req.get("keyCode","").asString() <<" KeyType: \n"<<req.get("keyType","").asString();
			//DEBUG_PRINT(DEBUG_LOG,"\n KeyCode : %s, KeyType: %s \n",req.get("keyCode","").asString() ,req.get("keyType","").asString());
			//std::string kC=req.get("keyCode","").asString();
			//std::string kT=req.get("keyType","").asString();
			//std::cout<<kC<<kT;
			
			//int keyType = (unsigned int) atoi(kT.c_str());
			int keyType = (unsigned int) req["keyType"].asInt();
			//printf("**************************************");
			//int keyCode = (unsigned int) atoi(kC.c_str());
			int keyCode = (unsigned int)req["keyCode"].asInt();
			//printf("**************************************");
			//std::cout<<"\n KeyCode : "<< keyCode <<" KeyType: \n"<<keyType;
			ExpectedKeyCode = keyCode;
			ExpectedKeyType = keyType;
			DEBUG_PRINT(DEBUG_LOG,"ExpectedKeyCode : %d, ExpectedKeyType: %d \n", keyCode, keyType);
         		std::string skeyCode;          // string which will contain the result
         		std::string skeyType;          // string which will contain the result
         		std::string seventId;          // string which will contain the result
 
         		std::ostringstream convert;   // stream used for the conversion
         		std::ostringstream convert2;   // stream used for the conversion
         		std::ostringstream convert3;   // stream used for the conversion
 
         		convert << keyCode;      // insert the textual representation of 'Number' in the characters in the stream
         		convert2 << keyType;      // insert the textual representation of 'Number' in the characters in the stream
         		convert3 << eventId;      // insert the textual representation of 'Number' in the characters in the stream
 
         		skeyCode = convert.str(); // set 'Result' to the contents of the stream
         		skeyType = convert2.str(); // set 'Result' to the contents of the stream
         		seventId = convert3.str(); // set 'Result' to the contents of the stream
 
			DEBUG_PRINT(DEBUG_LOG,"ExpectedKeyCode : %d, ExpectedKeyType: %d \n", keyCode, keyType);
			DEBUG_PRINT(DEBUG_LOG,"appName : %s, ownerName : %s,  eventId : %s, keyType: %s, keyCode: %s \n", appname,ownerName,seventId.c_str(),skeyType.c_str(),skeyCode.c_str());
 			DEBUG_PRINT(DEBUG_LOG,"KeyCode : %d, KeyType: %d \n", keyCode, keyType);
 			// Parameters to execl must be strings
 			execl(path.c_str(), appname, "-o", ownerName, "-i", seventId.c_str(),"-t", skeyType.c_str(), "-c", skeyCode.c_str(), (char *)NULL);
		}
		else if(strcmp(ownerName,IARM_BUS_PWRMGR_NAME)==0)
		{
			int newState = (unsigned int) req["newState"].asInt();
        		std::string snewState;          // string which will contain the result
         		std::ostringstream convert;   // stream used for the conversion
         		convert << newState;      // insert the textual representation of 'Number' in the characters in the stream
         		snewState = convert.str(); // set 'Result' to the contents of the stream

			DEBUG_PRINT(DEBUG_LOG,"newState : %d \n", newState);
			execl(path.c_str(),appname, "-n", snewState.c_str(), (char*)NULL);
		}
		else if(strcmp(ownerName,IARM_BUS_DAEMON_NAME)==0)
		{
			int resrcType = (unsigned int) req["resource_type"].asInt();
        		std::string sresrcType;          // string which will contain the result
         		std::ostringstream convert;   // stream used for the conversion
         		convert << resrcType;      // insert the textual representation of 'Number' in the characters in the stream
         		sresrcType = convert.str(); // set 'Result' to the contents of the stream

			DEBUG_PRINT(DEBUG_LOG,"resource_type : %d \n", resrcType);
			execl(path.c_str(),appname, "-o", ownerName, "-r", sresrcType.c_str(), (char*)NULL);
		}
		else if(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME)==0)
		{
         		std::string seventId;          // string which will contain the result
         		std::ostringstream convert3;   // stream used for the conversion
         		convert3 << eventId;      // insert the textual representation of 'Number' in the characters in the stream
         		seventId = convert3.str(); // set 'Result' to the contents of the stream

			execl(path.c_str(), appname, "-o", ownerName, "-i", seventId.c_str(), (char*)NULL);
		}
	}
	else if(idChild <0)
	{
		DEBUG_PRINT(DEBUG_LOG,"failed fork\n");
		response["result"]="FAILURE";
		response["details"]="second application Execution failed";
		return;
	}

	sprintf(details, "%s Successfully Executed", __func__);
	response["details"]=details;
	response["result"]="SUCCESS";
	DEBUG_PRINT(DEBUG_LOG,"Exiting %s function", __func__);
	return;	

}

/**************************************************************************
 * Function Name	: Get_LastReceivedEventPerforamceDetails
 * Description	: This function is to get the last received Event details 	
 *
 ***************************************************************************/


void IARMBUSAgent::GetLastReceivedEventPerformanceDetails(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"%s --->Entry \n", __func__);
	char details[400]="Event Details:";
	const char *KeyCodedetails=" :: KeyCode : " ;
	const char *KeyTypedetails=" :: KeyType : ";
	const char *KeyTimedetails=" :: Time : ";
	char *KeyCodedetails1 =(char*)malloc(sizeof(char)*150); 
	memset(KeyCodedetails1 , '\0', (sizeof(char)*150));
	char *KeyTypedetails1 =(char*)malloc(sizeof(char)*100);
	memset(KeyTypedetails1 , '\0', (sizeof(char)*100));
	char *KeyTimedetails1 =(char*)malloc(sizeof(char)*120);
	memset(KeyTimedetails1 , '\0', (sizeof(char)*120));

        DEBUG_PRINT(DEBUG_LOG,"**lasttime %lf lastev %s\n",LastKeyTime,LastEvent);
        
	if(strcmp(LastEvent,"IARM_BUS_IRMGR_EVENT_IRKEY")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"lastcode %d lasttype %d lasttime %lf lastev %s\n",LastKeyCode,LastKeyType,LastKeyTime,LastEvent);
		strcat(details,LastEvent);
		sprintf(KeyCodedetails1,"%d" , LastKeyCode);
                sprintf(KeyTypedetails1,"%d" , LastKeyType);
                sprintf(KeyTimedetails1,"%lf" , LastKeyTime);

		strcat(details,KeyCodedetails);
                strcat(details,KeyCodedetails1);
                strcat(details,KeyTypedetails);
		strcat(details,KeyTypedetails1);
		strcat(details,KeyTimedetails);
		strcat(details,KeyTimedetails1);
		strcpy(KeyCodedetails1,details);
		response["details"]=KeyCodedetails1;
		response["result"]="SUCCESS";
	
	}
	else if((strcmp(LastEvent,"IARM_BUS_PWRMGR_EVENT_MODECHANGED")==0)||
			(strcmp(LastEvent,"IARM_BUS_EVENT_RESOURCEAVAILABLE")==0)|| 
			(strcmp(LastEvent,"IARM_BUS_EVENT_RESOLUTIONCHANGE")==0))
	{
		strcat(details,LastEvent);
                sprintf(KeyTimedetails1,"%lf" , LastKeyTime);
		strcat(details,KeyTimedetails);
		strcat(details,KeyTimedetails1);
		response["details"]=details;
		response["result"]="SUCCESS";
	}
	else if((strcmp(LastEvent,"IARM_BUS_DUMMYMGR_EVENT_DUMMYX")==0)||
			(strcmp(LastEvent,"IARM_BUS_DUMMYMGR_EVENT_DUMMYY")==0)|| 
			(strcmp(LastEvent,"IARM_BUS_DUMMYMGR_EVENT_DUMMYZ")==0))
	{
		strcat(details,LastEvent);
                sprintf(KeyTimedetails1,"%lf" , LastKeyTime);
		strcat(details,KeyTimedetails);
		strcat(details,KeyTimedetails1);
		response["details"]=details;
		response["result"]="SUCCESS";
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"NO EVENTS RECEIVED BY HANDLER : %s", LastEvent);
		response["details"]="NO EVENTS RECEIVED BY HANDLER";
		response["result"]="FAILURE";
	}

	//ajan 
	char *lastKeyTimeStr =(char*)malloc(sizeof(char)*150);
	memset(lastKeyTimeStr , '\0', (sizeof(char)*150));
	sprintf(lastKeyTimeStr,"%lf" , LastKeyTime);

	char *pefDataInfo =(char*)malloc(sizeof(char)*150);
	memset(pefDataInfo , '\0', (sizeof(char)*150));
	sprintf(pefDataInfo,"%d:%d" , LastKeyCode,LastKeyType);

	response["performanceDataReading"]=lastKeyTimeStr;
	response["performanceDataName"]="TimeToGetIRKeyEvent";
	response["performanceDataUnit"]="ms";
	response["performanceDataInfo"]=pefDataInfo;


	/* TODO : Currently response is overwritten but need to change appropriately*/
	/* Check if more than one event recieved */
	if (gEventSummaryCount > 1)
	{
		response["details"]=gEventSummary;
		response["result"]="SUCCESS";
	}

	memset(&(gEventSummary) , '\0', (sizeof(char)*1024));
	gEventSummaryCount = 0;
	gRegisteredEventCount = 0;

	memset(&(LastEvent) , '\0', (sizeof(char)*20));
	memset(&(gLastEvent) , '\0', (sizeof(char)*20));
	LastKeyCode = 0;
	LastKeyType = 0;
	LastKeyTime = 0;
	free(KeyCodedetails1);
	free(KeyTypedetails1);
	free(KeyTimedetails1);

	DEBUG_PRINT(DEBUG_LOG,"%s --->Exit \n", __func__);
	return;
}

/**************************************************************************
 * Function Name        : IARMBUSAgent_RemoveEventHandler
 * Description  : IARMBUSAgent_RegisterEventHandler wrapper function will be used to call
 *                IARMBUS API "IARM_Bus_RemoveEventHandler".
 *
 * @param [in] req- has "event_id" , "evt_handler" and "owner_name" which are input to IARM_Bus_RegisterEventHandler.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/

void IARMBUSAgent::IARMBUSAgent_RemoveEventHandler(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RemoveEventHandler --->Entry \n");
        IARM_Result_t retval=IARM_RESULT_SUCCESS;
        char *resultDetails;
        resultDetails=(char *)malloc(sizeof(char)*16);
        memset(resultDetails , '\0', (sizeof(char)*16));
        if(&req["event_id"]==NULL || &req["owner_name"]==NULL || &req["evt_handler"]==NULL)
        {
		DEBUG_PRINT(DEBUG_ERROR,"NULL param passed \n");
                return;
        }

        int eventId=req["event_id"].asInt();
        char *ownerName=(char*)req["owner_name"].asCString();
        char *eventhandler=(char*)req["evt_handler"].asCString();

        DEBUG_PRINT(DEBUG_LOG,"IARM_Bus_RemoveEventHandler [Owner: %s EventId: %d eventhandler: %s]\n", ownerName, eventId, eventhandler);
        /*Calling IARMBUS API IARM_Bus_RemoveEventHandler */
	if (strcmp(eventhandler,"NULL")==0)
	{
        		retval=IARM_Bus_RemoveEventHandler(ownerName,(IARM_EventId_t)eventId, NULL);
	}
	else if (strcmp(eventhandler,"evtHandler")==0)
	{
	        	retval=IARM_Bus_RemoveEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandler);
	}
	else if (strcmp(eventhandler,"evtHandler1")==0)
	{
	        	retval=IARM_Bus_RemoveEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept1);
	}
	else if (strcmp(eventhandler,"evtHandler2")==0)
	{
	        	retval=IARM_Bus_RemoveEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept2);
	}
	else if (strcmp(eventhandler,"evtHandler3")==0)
	{
	        	retval=IARM_Bus_RemoveEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept3);
	}
  
        /*Checking the return value of API*/
        if( retval && !iarmMgrStatus(ownerName) )
        {
        	DEBUG_PRINT(DEBUG_ERROR,"Given IARM Mgr is not running\n");
        }

        /*Filling json response with SUCCESS status*/
        response["result"]=getResult(retval,resultDetails);
        response["details"]=resultDetails;
        free(resultDetails);
        DEBUG_PRINT(DEBUG_TRACE,"IARMBUSAgent_RemoveEventHandler --->Exit \n");
        return;
}

/**************************************************************************
 * Function Name	: CreateObject
 * Description	: This function will be used to create a new object for the
 *		  class "IARMBUSAgent".
 *
 **************************************************************************/

extern "C" IARMBUSAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
	return new IARMBUSAgent(ptrtcpServer);
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will be used to clean the log details. 
 *
 **************************************************************************/

bool IARMBUSAgent::cleanup(IN const char* szVersion)
{
	/* TWC-change : ReInitialize variable*/
	REGISTERCALLSTATUS = 0;

	return TEST_SUCCESS;
}


/**************************************************************************
 * Function Name : DestroyObject
 * Description   : This function will be used to destory the object. 
 *
 **************************************************************************/
extern "C" void DestroyObject(IARMBUSAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG,"Destroying IARMBUS Agent object\n");
        delete stubobj;
}
