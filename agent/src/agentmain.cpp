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


/* System Includes */
#include <stdio.h>
#include <error.h>
#include <csignal>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <fstream>
#include <net/if.h>
#include <setjmp.h>
#include <ifaddrs.h>
#include <iostream>
#include <pthread.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <execinfo.h>

/* Application Includes */
#include "rpcmethods.h"
#include "rdktestagentintf.h"

/* Constants */
#define DEVICE_INFO_SUCCESS 0
#define DEVICE_INFO_FAILURE 1

#define ANY_ADDR "::"
#define RDK_TEST_AGENT_PORT 8087
#define RDK_DEVICE_INFO_PORT 8089
#define RDK_DEVICE_STATUS_PORT 8088
#define RDK_AGENT_MONITOR_PORT 8090

#define INFO_STRING_SIZE 100
#define STATUS_QUERY_TIMEOUT 120
#define BT_BUFFER_SIZE 255

#define CRASH_STATUS_FILE "crashStatus.ini"
#define FLUSH_IP_TABLE "sh $TDK_PATH/flush_iptables.sh"

using namespace std;
using namespace Json;

jmp_buf g_JumpBuffer;  //  Declaring global jmp_buf variable to be used by both main and signal handler

static volatile bool s_bAgentMonitorRun = true;  //  Variable to run agent monitor. Set to false to stop monitoring.
static volatile bool s_bAgentRun = true;              // Variable to run agent. Set to false to stop agent.
static volatile bool s_bAgentReset = true;           // Variable to enable agent reset.

std::fstream go_ConfigFile;
std::fstream go_PortforwardFile;

pthread_t deviceStatusThreadId;
pthread_t deviceDetailsThreadId;
pthread_t crashDetailsThreadId;
pthread_t agentExecuterThreadId;
TcpSocketServer go_Server(ANY_ADDR, RDK_TEST_AGENT_PORT);

extern RDKTestAgent *m_pAgent;
/* Structure to hold process details */
struct sProcessInfo 
{
    char **pProcessName;
    int nProcessNameSize;
};

/* To enable port forwarding. In gateway boxes only  */
#ifdef PORT_FORWARD

    /* Map to hold details of client devices */
    typedef std::map <std::string, std::string> ClientDeviceMap;
    ClientDeviceMap o_gClientDeviceMap;
    ClientDeviceMap::iterator o_gClientDeviceMapIter;

#endif /* PORT_FORWARD */


/* Initialization */
int RpcMethods::sm_nAgentPID = 0;
int RpcMethods::sm_nRouteSetFlag = FLAG_NOT_SET;
int RpcMethods::sm_nGetDeviceFlag = FLAG_NOT_SET;
int RpcMethods::sm_nConsoleLogFlag = FLAG_NOT_SET;
int RpcMethods::sm_nStatusQueryFlag = FLAG_NOT_SET;

string RpcMethods::sm_strBoxIP = "";
const char* RpcMethods::sm_szBoxName = NULL;
const char* RpcMethods::sm_szManagerIP = NULL;
const char* RpcMethods::sm_szBoxInterface = NULL;
FILE* RpcMethods::sm_pLogStream = NULL;
std::string RpcMethods::sm_strLogFolderPath = "";
std::string RpcMethods::sm_strTDKPath = "";

/********************************************************************************************************************
 Purpose:                To get a substring seperated by a delimiter.
 
 Parameters:   
                         strLine [IN]    - Line of string to get seperated.
                         strDelimiter [IN]  - delimiter 
 
 Return:                 string    - substring

*********************************************************************************************************************/
std::string GetSubString (std::string strLine, std::string strDelimiter)
{
    size_t nPos = 0;
    std::string strToken;

    while ( (nPos = strLine.find (strDelimiter)) != std::string::npos)
    {
        strToken = strLine.substr (0, nPos);
        strLine.erase (0, nPos + strDelimiter.length());
    }
	
    return strLine;
	
} /* End of GetSubString */


/********************************************************************************************************************
 Purpose:               To get the Host's IP Address by querrying the network Interface.
 
 Parameters:   
                        szInterface [IN]    - Interface used to communicate.
 
 Return:                string    - IP address of corresponding interface.

*********************************************************************************************************************/
std::string GetHostIP (const char* szInterface)
{
    struct ifaddrs* pIfAddrStruct = NULL;
    struct ifaddrs* pIfAddrIterator = NULL;
    void* pvTmpAddrPtr = NULL;
    bool pvReturnValue;
    char szAddressBufferIpv4 [INET_ADDRSTRLEN];
    char szAddressBufferIpv6 [INET6_ADDRSTRLEN];
    getifaddrs (&pIfAddrStruct);

    std::string strFilePath;
    std::string strManagerIP;

    int nReturnValue = DEVICE_INFO_SUCCESS;

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(CONFIGURATION_FILE);

    /* Open the configuration file and extracts Test manager IP address */
    go_ConfigFile.open (strFilePath.c_str(), ios::in);
    if (go_ConfigFile.is_open())
    {
        DEBUG_PRINT (DEBUG_LOG, "\nConfiguration file %s found \n", SHOW_DEFINE (CONFIGURATION_FILE));

        /* Parsing configuration file to get manager IP */
        pvReturnValue = !!getline (go_ConfigFile, strManagerIP);
        go_ConfigFile.close();
        if (pvReturnValue)
        {
            strManagerIP = GetSubString (strManagerIP, "@");
            RpcMethods::sm_szManagerIP = strManagerIP.c_str();
	    
            /* To check whether test manager IP is IPV6 or IPV4*/
	    if (strManagerIP.find(":")!= std::string::npos)
            {
                 DEBUG_PRINT (DEBUG_LOG, "Test Manager ip is IPV6 version \n");
                 for (pIfAddrIterator = pIfAddrStruct; pIfAddrIterator != NULL; pIfAddrIterator = pIfAddrIterator->ifa_next)
                 {
                     if (pIfAddrIterator->ifa_addr->sa_family == AF_INET6)
                     {
                         // check it is a valid IPV6 Address
                         pvTmpAddrPtr = & ( (struct sockaddr_in6 *)pIfAddrIterator->ifa_addr )-> sin6_addr;
                         inet_ntop (AF_INET6, pvTmpAddrPtr, szAddressBufferIpv6, INET6_ADDRSTRLEN);
                         
                         if (strncmp("fe80",szAddressBufferIpv6,4)==0)
                         {
                             DEBUG_PRINT (DEBUG_LOG, "Skipping STB IPV6 Link Local address \n");
                             continue;
                         }
                         if ( (strcmp (pIfAddrIterator -> ifa_name, szInterface) ) == 0)
                         {
                             break;
                         }
                     }
                 }	
                 DEBUG_PRINT (DEBUG_TRACE, "Found STB IPV6 Address: %s\n", szAddressBufferIpv6);
                 if (pIfAddrStruct != NULL)
                 {
                     freeifaddrs (pIfAddrStruct);
                 }
                 return szAddressBufferIpv6;
             }

             else
             {
                 DEBUG_PRINT (DEBUG_LOG, "Test Manager ip is IPV4 version \n");

                 for (pIfAddrIterator = pIfAddrStruct; pIfAddrIterator != NULL; pIfAddrIterator = pIfAddrIterator->ifa_next) 
                 {
                     if (pIfAddrIterator->ifa_addr->sa_family == AF_INET) 
                     {
                         // check it is a valid IP4 Address
                         pvTmpAddrPtr = & ( (struct sockaddr_in *)pIfAddrIterator->ifa_addr )-> sin_addr;
                         inet_ntop (AF_INET, pvTmpAddrPtr, szAddressBufferIpv4, INET_ADDRSTRLEN);
                 
                         if ( (strcmp (pIfAddrIterator -> ifa_name, szInterface) ) == 0)
                         {
                             break;
                         }		
                      }
                 }
                 DEBUG_PRINT (DEBUG_TRACE, "Found STB IPV4 Address: %s\n", szAddressBufferIpv4);
                 if (pIfAddrStruct != NULL) 
                 {
                     freeifaddrs (pIfAddrStruct);
                 }
                 return szAddressBufferIpv4;
             }
        }
        else
        {
            DEBUG_PRINT (DEBUG_ERROR, "Failed to extract Test Manager IP Address");
        }

    }
    else
    {
        DEBUG_PRINT (DEBUG_TRACE, "\nAlert!!! Configuration file %s not found \n", SHOW_DEFINE(CONFIGURATION_FILE));
    }

} /* End of GetHostIP */


/********************************************************************************************************************
 Purpose:               A function to send information from the box to manager. It will extract 
                        manager IP address from configuration file
 
 Parameters:   
                        strStringToSend [IN] - data to send
                        nStringSize [IN]  - size of data
 
 Return:                int    -  Success/Failure

 Other Methods used:     
                        GetSubString()

*********************************************************************************************************************/
int SendInfo (char* strStringToSend, int nStringSize)
{
    int nValue = 0;
    int nDestination; 
    int nInfoSockDesc;    
    bool pvReturnValue;    
    std::string strFilePath;
    std::string strManagerIP;
    
    int nReturnValue = DEVICE_INFO_SUCCESS;
    struct sockaddr_in o_Addr;
    struct sockaddr_in6 o_Addr6;

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(CONFIGURATION_FILE);
   
    /* Open the configuration file and extracts Test manager IP address */
    go_ConfigFile.open (strFilePath.c_str(), ios::in);
    if (go_ConfigFile.is_open())
    {
        DEBUG_PRINT (DEBUG_LOG, "\nConfiguration file %s found \n", SHOW_DEFINE (CONFIGURATION_FILE));
		
        /* Parsing configuration file to get manager IP */
        pvReturnValue = !!getline (go_ConfigFile, strManagerIP); 
        go_ConfigFile.close();
        if (pvReturnValue)
        {
            strManagerIP = GetSubString (strManagerIP, "@");
            RpcMethods::sm_szManagerIP = strManagerIP.c_str();
            DEBUG_PRINT (DEBUG_LOG, "Test Manager IP is %s \n", RpcMethods::sm_szManagerIP);

            /* To check whether test manager IP is IPV6 or IPV4*/
            if (strManagerIP.find(":")!= std::string::npos)
            {
                nInfoSockDesc = socket (AF_INET6, SOCK_STREAM, 0);
                if (nInfoSockDesc < 0)
                {
                    perror("\nAlert!!! Failed to create socket ");
		
                    return DEVICE_INFO_FAILURE;     // Return when failed to create socket
                }	

                inet_pton (AF_INET6, RpcMethods::sm_szManagerIP, o_Addr6.sin6_addr.s6_addr);
                o_Addr6.sin6_family = AF_INET6;
                o_Addr6.sin6_port = htons (RDK_DEVICE_INFO_PORT);
                /* Connecting to Test Manager */

                nValue = connect (nInfoSockDesc, (struct sockaddr *) &o_Addr6, sizeof(o_Addr6));
                if (nValue < 0)
                {
                    perror("\nAlert!!! Failed to connect Test Manager ");
                    	
                    return DEVICE_INFO_FAILURE;     // Return when failed to connect to Test Manager
                }

                /* Sending data to Test Manager */
                nValue = write (nInfoSockDesc, (void *)strStringToSend, nStringSize);
                if (nValue < 0)
                {
                    perror("\nAlert!!! Failed to send data to Test Manager ");
                    	
                    return DEVICE_INFO_FAILURE;     // Return when failed to send data to Test Manager
                    
                }
                    
                close (nInfoSockDesc);
                DEBUG_PRINT (DEBUG_LOG, "\n\n Successfully sent the details to Test Manager \n"); 
                return nReturnValue;
            }
            else
            {
                nInfoSockDesc = socket (AF_INET, SOCK_STREAM, 0);
                if (nInfoSockDesc < 0)
                {
                    perror("\nAlert!!! Failed to create socket ");

                    return DEVICE_INFO_FAILURE;     // Return when failed to create socket
                }
                    
                inet_pton (AF_INET,RpcMethods::sm_szManagerIP, (void *)&nDestination);
                o_Addr.sin_family = AF_INET;
                o_Addr.sin_port = htons (RDK_DEVICE_INFO_PORT);
                o_Addr.sin_addr.s_addr = nDestination;
                /* Connecting to Test Manager */
                nValue = connect (nInfoSockDesc, (struct sockaddr *) &o_Addr, sizeof(o_Addr));
                if (nValue < 0)
                {
                    perror("\nAlert!!! Failed to connect Test Manager ");
                    	
                    return DEVICE_INFO_FAILURE;     // Return when failed to connect to Test Manager
                    
                }

                /* Sending data to Test Manager */
                nValue = write (nInfoSockDesc, (void *)strStringToSend, nStringSize);
                if (nValue < 0)
                {
                    perror("\nAlert!!! Failed to send data to Test Manager ");
                    	
                    return DEVICE_INFO_FAILURE;     // Return when failed to send data to Test Manager
                    
                }
                    
                close (nInfoSockDesc);
                
                DEBUG_PRINT (DEBUG_LOG, "\n\n Successfully sent the details to Test Manager \n"); 
                    
                return nReturnValue;
            } 
        }
        else
        {
            DEBUG_PRINT (DEBUG_ERROR, "Failed to extract Test Manager IP Address");

            return DEVICE_INFO_FAILURE;     // Return when failed to extract Test Manager IP Address
		 
        }

    }
    else
    {
        DEBUG_PRINT (DEBUG_TRACE, "\nAlert!!! Configuration file %s not found \n", SHOW_DEFINE(CONFIGURATION_FILE));
        	
        return DEVICE_INFO_FAILURE;     // Return when failed to open configuration file
        
    }

} /* End of SendInfo */


/********************************************************************************************************************
 Purpose:               Function to print back trace on crash
 
 Parameters:            Nil
                             
 Return:                void

*********************************************************************************************************************/
static void printBackTrace(void)
{
    DEBUG_PRINT (DEBUG_LOG, "%s() --> Entry\n",__FUNCTION__);
    void * buffer[BT_BUFFER_SIZE];
    int calls = backtrace(buffer, BT_BUFFER_SIZE);
    backtrace_symbols_fd(buffer, calls, STDOUT_FILENO);
    DEBUG_PRINT (DEBUG_LOG, "%s() --> Exit\n",__FUNCTION__);

} /* End of printBackTrace */



/********************************************************************************************************************
 Purpose:               Signal Handler. Handles signals and jump to the jumpbuffer to keep application active.
 
 Parameters:   
                        nCode [IN] - Signal number
                             
 Return:                void

 Other Methods used:     
                        SendInfo()

*********************************************************************************************************************/
static void SignalHandler (int nCode)
{
    switch(nCode)
    {
        case SIGINT    :
        case SIGTERM :
            s_bAgentMonitorRun = false;
            s_bAgentRun = false;
            s_bAgentReset = false;
            break;
			
        case SIGABRT :
            DEBUG_PRINT (DEBUG_LOG, "\nAlert!!! Agent caught an Abort signal! Attempting recovery..\n");
            printBackTrace();
            s_bAgentRun = false;
            longjmp (g_JumpBuffer,0);
            break;
			
        case SIGSEGV :
            DEBUG_PRINT (DEBUG_LOG, "\nAlert!!! Segmentation fault signal caught! Attempting recovery..\n");
            printBackTrace();
            s_bAgentRun = false;
            longjmp (g_JumpBuffer,0);
            break;

        /* User Defined signal for setting device state to FREE */
        case SIGUSR2 :
            RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
            break;
			
        default :
            break;
			
    }
	
} /* End of SignalHandler */



/********************************************************************************************************************
 Purpose:               To send box details such as box ip address and box name to test manager using SendInfo()
                             after reading box name from configuration file.
 
 Parameters:   
                             null
 
 Return:                 int    -  Success/Failure

 Other Methods used:    
                                    SendInfo() 
                                    GetSubString()

*********************************************************************************************************************/
int SendDetailsToManager()
{
    bool pvReturnValue;
    char szBoxInfo[INFO_STRING_SIZE];
    int nSendInfoStatus = 0;
    std::string strBoxName;
    std::string strFilePath;

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(CONFIGURATION_FILE);
    
    go_ConfigFile.open (strFilePath.c_str(), ios::in);
    if (go_ConfigFile.is_open())
    {
        DEBUG_PRINT (DEBUG_LOG, "\nConfiguration file %s found \n", SHOW_DEFINE (CONFIGURATION_FILE));
			
        /* Parsing configuration file to get box name */
        for (int i=0; i<2; i++)
        {
            pvReturnValue = !!getline (go_ConfigFile, strBoxName);

            if (!pvReturnValue)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Unable to find device name \n");

                nSendInfoStatus =  DEVICE_INFO_FAILURE;     // Info failure when failed to retrieve device name
                break;
            }
			
        }

        go_ConfigFile.close();

        /* Sending details to Test Manager */
        if (pvReturnValue)
        {
            strBoxName = GetSubString (strBoxName, "@");		
            RpcMethods::sm_szBoxName = strBoxName.c_str();
            DEBUG_PRINT (DEBUG_LOG, "Box Name is %s \n", RpcMethods::sm_szBoxName);
			        
            /* Sending the box name and box ip address to Test Manager */
            szBoxInfo[0] = '\0';
            strcat(szBoxInfo, RpcMethods::sm_szBoxName);
            strcat(szBoxInfo, ",");
            strcat(szBoxInfo, RpcMethods::sm_strBoxIP.c_str());
            nSendInfoStatus = SendInfo (szBoxInfo, strlen(szBoxInfo)); 
        }	
        
    }
    else
    {
        DEBUG_PRINT (DEBUG_LOG, "\nAlert!!! Configuration file %s not found", SHOW_DEFINE(CONFIGURATION_FILE));
        nSendInfoStatus = DEVICE_INFO_FAILURE;
    }

    return nSendInfoStatus;
	
} /* End of SendDetailsToManager */



/********************************************************************************************************************
 Purpose:               To Check if device had a crash during last power cycle. If it had, send Test casedetails such as execution ID, 
                        device ID and Test case ID to test manager using SendInfo()
 
 Parameters:   
                        null
 
 Return:                int    -  Success/Failure

 Other Methods used:    
                        SendInfo() 
                        GetSubString()

*********************************************************************************************************************/
void* ReportCrash (void*)
{
    bool pvReturnValue;
    int nCount = 0;
    int nCrashFlag = FLAG_SET;
    std::string strExecId;
    std::string strFilePath;
    std::string strResultId;
    std::string strDeviceId;
    std::string strTestcaseId;
    std::string strCrashStatus;
    std::string strExecDeviceId;
    std::fstream o_CrashStatusFile;
    char szCrashDetails [INFO_STRING_SIZE];
    int nSendInfoStatus = RETURN_SUCCESS;

    DEBUG_PRINT (DEBUG_TRACE, "\nStarting Crash Details Processing..\n");

    /* Extracting path to file */	
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(CRASH_STATUS_FILE);
  	
    o_CrashStatusFile.open (strFilePath.c_str(), ios::in);
    if (o_CrashStatusFile.is_open())
    {
        DEBUG_PRINT (DEBUG_LOG, "\nConfiguration file %s found", SHOW_DEFINE (CRASH_STATUS_FILE) );
		
        /* Parsing configuration file to get crash status */
        pvReturnValue = !!getline (o_CrashStatusFile, strCrashStatus); 
        if (!pvReturnValue)
        {
            DEBUG_PRINT (DEBUG_ERROR, "Failed to retrieve status on crash");
            nCrashFlag = FLAG_NOT_SET ;
        }
        else
        {
            strCrashStatus = GetSubString (strCrashStatus, ":");
        }

        if ((strCrashStatus == "YES") && (nCrashFlag == FLAG_SET))
        {
            DEBUG_PRINT (DEBUG_LOG, "\nAlert !!! Crash occured in previous execution. Trying to send test details to Test Manager... \n");
            DEBUG_PRINT (DEBUG_LOG, "Test Details :  ");
	
            /* Parsing configuration file to get execution ID */
            pvReturnValue = !!getline (o_CrashStatusFile, strExecId); 
            if (!pvReturnValue)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to retrieve execution ID \n");
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strExecId = GetSubString (strExecId, ":");
                if (strExecId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
		
            /* Parsing configuration file to get Device ID */
            pvReturnValue = !!getline (o_CrashStatusFile, strDeviceId);
            if (!pvReturnValue)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to retrieve Device ID \n");
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strDeviceId = GetSubString (strDeviceId, ":");
                if (strDeviceId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
            
            /* Parsing configuration file to get Testcase ID */
            pvReturnValue = !!getline (o_CrashStatusFile, strTestcaseId); 
            if (!pvReturnValue)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to retrieve Testcase ID \n");
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strTestcaseId = GetSubString (strTestcaseId, ":");
                if (strTestcaseId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
			
            /* Parsing configuration file to get Execution Device ID */
            pvReturnValue = !!getline (o_CrashStatusFile, strExecDeviceId); 
            if (!pvReturnValue)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to retrieve Execution Device ID \n");
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strExecDeviceId = GetSubString (strExecDeviceId, ":");
                if (strExecDeviceId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
					
            /* Parsing configuration file to get Result ID */
            pvReturnValue = !!getline (o_CrashStatusFile, strResultId);
            if (!pvReturnValue)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to retrieve Result ID \n");
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strResultId = GetSubString (strResultId, ":");
                if (strResultId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
			
            o_CrashStatusFile.close();

            /* Sending the test details to Test Manager */
            if (nCrashFlag == FLAG_SET)
            {
                DEBUG_PRINT (DEBUG_LOG, "\n    Execution ID : %s \n", strExecId.c_str());
                DEBUG_PRINT (DEBUG_LOG, "    Result ID     : %s \n", strResultId.c_str());
                DEBUG_PRINT (DEBUG_LOG, "    Device ID    : %s \n", strDeviceId.c_str());
                DEBUG_PRINT (DEBUG_LOG, "    Testcase ID  : %s \n", strTestcaseId.c_str());
                DEBUG_PRINT (DEBUG_LOG, "    Execution Device ID  : %s \n", strExecDeviceId.c_str());
				
                szCrashDetails[0] = '\0';
                strcat(szCrashDetails, "CRASH_");			
                strcat(szCrashDetails, strExecId.c_str());
                strcat(szCrashDetails, ",");
                strcat(szCrashDetails, strDeviceId.c_str());
                strcat(szCrashDetails, ",");
                strcat(szCrashDetails, strTestcaseId.c_str());
                strcat(szCrashDetails, ",");
                strcat(szCrashDetails, strExecDeviceId.c_str());
                strcat(szCrashDetails, ",");
                strcat(szCrashDetails, strResultId.c_str());
            
                /* Waiting to get a status query */
                while (RpcMethods::sm_nStatusQueryFlag == FLAG_NOT_SET)
                {
                    sleep(1);	
                    nCount ++;
                    if (nCount == STATUS_QUERY_TIMEOUT)
                    {
                        break;
                    }
                }
		
                nSendInfoStatus = SendInfo (szCrashDetails, strlen (szCrashDetails)); 
                if (nSendInfoStatus == DEVICE_INFO_SUCCESS)
                {
                    DEBUG_PRINT (DEBUG_LOG, "Sent crash details to Test Manager successfully");
				
                }
            }
            else
            {
                DEBUG_PRINT (DEBUG_LOG, "Not found \n");
            }

            /* Delete the configuration file */
            if (remove (strFilePath.c_str()) != 0 )
            {
                DEBUG_PRINT (DEBUG_LOG, "\nAlert : Unable to delete %s file \n", SHOW_DEFINE(CRASH_STATUS_FILE) );
            }
            else
            {
                DEBUG_PRINT (DEBUG_LOG, "\n%s successfully deleted \n", SHOW_DEFINE(CRASH_STATUS_FILE) );
            }
			
        }

        else
        {
            DEBUG_PRINT (DEBUG_LOG, "Unable to report crash to Test Manager \n");
        }
		
    }

    pthread_exit (NULL);	

} /* End of ReportCrash */



/********************************************************************************************************************
 Purpose:             To check the device status, whether the execution is in progress or box is free for execution. (Thread Function)
 
 Parameters:          null
 
 Return:              null

*********************************************************************************************************************/
void *CheckStatus (void *)
{
    DEBUG_PRINT (DEBUG_TRACE, "\nStarting Device Status Monitoring..\n");
    TcpSocketServer go_Status(ANY_ADDR, RDK_DEVICE_STATUS_PORT);
    RpcMethods o_Status(go_Status);

    if (!o_Status.StartListening())
    {
        DEBUG_PRINT (DEBUG_ERROR, "Alert!!! Device Status Monitoring Listen failed \n");
    }

    while (s_bAgentRun)
    {
          sleep(1);
    }

    /* clean up and exit */
    DEBUG_PRINT (DEBUG_TRACE, "\nExiting Device Status Monitoring..\n");
    pthread_exit (NULL);
} /* End of CheckStatus */



/********************************************************************************************************************
 Purpose:               To check whether a status query is received, if not send the device details to test manager. (Thread Function)
 
 Parameters:            null
 
 Return:                null

 Other Methods used: 
                        GetSubString()
                        GetHostIP()
                        SendDetailsToManager()

*********************************************************************************************************************/
void *ProcessDeviceDetails (void *)
{
    int nCount = 0;
    bool pvReturnValue;
    std::string strFilePath;
    int nDeviceInfoStatus = 0;
    std::string strBoxInterface;	

    DEBUG_PRINT (DEBUG_TRACE, "\nStarting Device Details Processing..\n");
		
    /* Waiting to get a status query */
    while (RpcMethods::sm_nStatusQueryFlag == FLAG_NOT_SET)
    {
        sleep(1);	
        nCount ++;

        if (nCount == STATUS_QUERY_TIMEOUT)
        {
            break;
        }
    }

    /* If status query flag not set, then send box name and IP address to Test Manager */
    if (RpcMethods::sm_nStatusQueryFlag == FLAG_NOT_SET)
    {
        /* Extracting path to file */
        strFilePath = RpcMethods::sm_strTDKPath;
        strFilePath.append(CONFIGURATION_FILE);
	
        go_ConfigFile.open (strFilePath.c_str(), ios::in);
        if (go_ConfigFile.is_open())
        {
            DEBUG_PRINT (DEBUG_LOG, "\nConfiguration file %s found \n", SHOW_DEFINE(CONFIGURATION_FILE) );

            /* Finding the box interface from configuration file */
            for (int i=0; i<3; i++)
            {
                pvReturnValue = !!getline (go_ConfigFile, strBoxInterface);
                if (!pvReturnValue)
                {
                    DEBUG_PRINT (DEBUG_ERROR, "Unable to find device network interface \n");
                    break;
                }

            }

            go_ConfigFile.close();

            /* Communicate with Test Manager after retrieveng device IP address */
            if (pvReturnValue)
            {
                strBoxInterface = GetSubString (strBoxInterface, "@");	
                RpcMethods::sm_szBoxInterface = strBoxInterface.c_str();
                DEBUG_PRINT (DEBUG_LOG, "\nBox interface is %s \n",RpcMethods::sm_szBoxInterface);
            
                /* Getting box IP address of corresponding interface */
                RpcMethods::sm_strBoxIP = GetHostIP (RpcMethods::sm_szBoxInterface);
			
                /* Sending box details to test manager */
                nDeviceInfoStatus = SendDetailsToManager();
                if (nDeviceInfoStatus == DEVICE_INFO_FAILURE)
                {
                    DEBUG_PRINT (DEBUG_TRACE, "\nAlert!!! Agent not able to communicate with Test Manager");
                }
			
            }
			
        }
        else
        {
            DEBUG_PRINT (DEBUG_LOG, "\nAlert!!! Configuration file %s not found \n", SHOW_DEFINE(CONFIGURATION_FILE) );
        }
			
    }
		
    pthread_exit (NULL);
	
} /* End of ProcessDeviceDetails */



/********************************************************************************************************************
 Description:           Agent Application. It enables RPC communication with test manager. 
 
 Parameters:            null
 
 Return:                int - Success/Failure

 Other Methods used: 
                        GetSubString()
                        GetHostIP()
                        SendDetailsToManager()

*********************************************************************************************************************/
int Agent()
{
    std::string strFilePath;
    int nReturnValue = RETURN_SUCCESS;
    int nCrashReportStatus = RETURN_SUCCESS;
    
    RpcMethods o_Agent(go_Server);
    
    if (!o_Agent.StartListening())
    {
        DEBUG_PRINT (DEBUG_ERROR, "Alert!!! Test Agent Listen failed \n");
		
        return RETURN_FAILURE;   // Returns failure if Listen failed
        
    }

    /* To set route to client devices. For gateway boxes only */
    #ifdef PORT_FORWARD

    size_t nPos = 0;
    char * pszCommand;
    std::string strCommand;
    std::string strClientMACAddr;
    std::string strDelimiter = "=";

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(PORT_FORWARD_RULE_FILE);

    /* Set iptable rules that was set in previous power cycle from the details in file */
    go_PortforwardFile.open(strFilePath.c_str(), ios::in);
    if (go_PortforwardFile.is_open())
    {
        DEBUG_PRINT (DEBUG_LOG, "\n%s found \n", SHOW_DEFINE(PORT_FORWARD_RULE_FILE) );
        while (getline (go_PortforwardFile, strCommand))
        {
            while ( (nPos = strCommand.find (strDelimiter)) != std::string::npos)
            {
                strClientMACAddr = strCommand.substr (0, nPos);
                strCommand.erase (0, nPos + strDelimiter.length());
            }

            DEBUG_PRINT (DEBUG_LOG, "\nSetting route for %s \n",strClientMACAddr.c_str());
            pszCommand = new char[strCommand.length() + 1];
            strcpy (pszCommand, strCommand.c_str());
            DEBUG_PRINT (DEBUG_LOG, "\nCommand is  %s \n",strCommand.c_str());
            system (pszCommand); // Executing port forward script
            o_gClientDeviceMap.insert (std::make_pair (strClientMACAddr, pszCommand));
        }
		
        go_PortforwardFile.close();
    }
	
    #endif /* End of PORT_FORWARD  */

    RpcMethods::sm_strConsoleLogPath = "";
    RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
    RpcMethods::sm_nStatusQueryFlag = FLAG_NOT_SET;
    
    /* Starting new thread for Device Status Monitoring */
    nReturnValue = pthread_create (&deviceStatusThreadId, NULL, CheckStatus, NULL);
    if(nReturnValue != RETURN_SUCCESS)
    {
        DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Failed to start Device Status Monitoring\n");
    }
			
    /* Starting new thread for sending box information to Test Manager */
    nReturnValue = pthread_create (&deviceDetailsThreadId, NULL, ProcessDeviceDetails, NULL);
    if (nReturnValue != RETURN_SUCCESS)
    {
        DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Failed to start Box Details Processing\n");
    }

    /* Report if a crash occured on previous execution */
    nReturnValue = pthread_create (&crashDetailsThreadId, NULL, ReportCrash, NULL);
    if (nReturnValue != RETURN_SUCCESS)
    {
        DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Failed to start Crash Details Processing\n");
    }
		
    /* Agent going for test execution */	
    sleep(1);
    DEBUG_PRINT (DEBUG_LOG, "\n\nAgent Ready for Execution... \n");

    /* Agent Recovery from seg fault and abort signal */
    nReturnValue = 0;
    nReturnValue = setjmp (g_JumpBuffer); // Setting the jump buffer for agent recovery
    if (nReturnValue)
    {
        DEBUG_PRINT (DEBUG_LOG, "Agent Recovering...\n");
    }

    /* Msg loop */
    while (s_bAgentRun)
    {
        try
        {
            waitpid (-1, NULL, WNOHANG | WUNTRACED);
					
              sleep(1);
        }
        catch(...)
        {
            /* Agent Recovery from termination */
            DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Termination caught.. Agent Attempting Recovery...\n");
        }
        
    }

    pthread_join (deviceStatusThreadId, NULL);

    /* To set route to client devices. For gateway boxes only */
    #ifdef PORT_FORWARD
		
    system (FLUSH_IP_TABLE);
		
    #endif /* End of PORT_FORWARD  */
	
    return RETURN_SUCCESS;
	
} /* End of Agent */


/********************************************************************************************************************
 Description:         To execute Agent. It helps to restart agent on receiving a ResetAgent message from TM.
 
 Parameters:          pProcessDetails - pointer to structure have process info
 
 Return:              void

 Other Methods used:  Agent()
 
*********************************************************************************************************************/
void *AgentExecuter (void *pProcessDetails)
{
    int nReturnValue = RETURN_SUCCESS;
    int nPID = RETURN_SUCCESS;

    struct sProcessInfo *pProcessInfo = (struct sProcessInfo *) pProcessDetails;

    /* Restart the agent if s_bAgentReset is true */
    while(s_bAgentReset)
    {
        nPID = fork();
        if (nPID == RETURN_SUCCESS)
        {
            waitpid (-1, NULL, WNOHANG | WUNTRACED);

            /* Modifying child process name to tdk_agent */
            strncpy (pProcessInfo -> pProcessName[0], "tdk_agent", pProcessInfo -> nProcessNameSize);

            /* Starting agent */
            nReturnValue = Agent();
            if(nReturnValue == RETURN_FAILURE)
            {
                s_bAgentReset = false;
            }

            sleep(3);
            exit(0);
			
        }
        else if (nPID < RETURN_SUCCESS)
        {
            DEBUG_PRINT (DEBUG_ERROR, "\n Alert!!!Failed to spawn process for Agent execution \n");
        }
        else
        {
            RpcMethods::sm_nAgentPID = nPID;
            waitpid (RpcMethods::sm_nAgentPID, NULL, 0);	
            sleep(2);
        }
    }

}/* End of AgentExecuter */



/********************************************************************************************************************
 Description:           Start and monitor agent execution. Invoke the corresponding rpc method on 
                        receiving "AgentReset" message from Test Manager. It also starts TFTP server
                        for log transferring. 
 
 Parameters:            pProcessName - pointer to process name
                        nProcessNameSize - length of process name
 
 Return:                int - Success/Failure

 Other Methods used:    AgentExecuter()
 
*********************************************************************************************************************/
int AgentMonitor (char **pProcessName, int nProcessNameSize)
{
    int nPID = RETURN_SUCCESS;
    int nReturnValue = RETURN_SUCCESS;
    struct sProcessInfo *pProcessInfo;

    DEBUG_PRINT (DEBUG_LOG, "\nStarting Agent Monitoring..\n");
    /* Populating structure members for process info */
    pProcessInfo = (struct sProcessInfo*) malloc (sizeof (struct sProcessInfo) );
    pProcessInfo -> pProcessName = pProcessName;
    pProcessInfo -> nProcessNameSize = nProcessNameSize;

    /* Registering signals to signal handler */
    if (signal (SIGTERM, SignalHandler) == SIG_ERR)
    {
        DEBUG_PRINT (DEBUG_ERROR, "Alert!!! Error signal SIGTERM will not be handled \n");
    }
	
    if (signal (SIGINT, SignalHandler) == SIG_ERR)
    {
        DEBUG_PRINT (DEBUG_ERROR, "Alert!!! Error signal SIGINT will not be handled \n");
    }

    TcpSocketServer go_Monitor(ANY_ADDR, RDK_AGENT_MONITOR_PORT); 
    RpcMethods o_Monitor(go_Monitor);

    if (!o_Monitor.StartListening())
    {
        DEBUG_PRINT (DEBUG_ERROR, "Alert!!! Agent Monitoring Listen failed \n");

        return RETURN_FAILURE;   // Returns failure if Listen failed
		
    }

    /* Starting a thread for agent execution */
    nReturnValue = pthread_create (&agentExecuterThreadId, NULL, AgentExecuter, (void *)(pProcessInfo));
    if(nReturnValue != RETURN_SUCCESS)
    {
        DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Failed to start execute Agent  \n");

        return RETURN_FAILURE;   // Returns failure if failed to start agent execution thread
		
    }
	
    while (s_bAgentMonitorRun)
    {
        waitpid (-1, NULL, WNOHANG | WUNTRACED);
		
        sleep(1);
    }

    /* clean up and exit */
    DEBUG_PRINT (DEBUG_LOG, "\nExiting Agent Monitoring..\n");
    free (pProcessInfo);
    pProcessInfo = NULL;
    return RETURN_SUCCESS;

} /* End of AgentMonitor */



/********************************************************************************************************************
 Description:           main function. Starts agent monitoring.
 
 Parameters:            null
 
 Return:                int - Success/Failure

 Other Methods used:    AgentMonitor()
 
*********************************************************************************************************************/
int main(int argc, char **argv)
{
    int nPgid = 0;
    char* pszPath;
    std::string strEnvPath;
    std::string strFolderPath;
    int nReturnValue = RETURN_SUCCESS;

    int nProcessNameSize = strlen(argv[0]);        // To fetch how many chars have been allocated

    /* Modifying process name to tdk_agent_monitor  */
    strncpy(argv[0], "tdk_agent_monitor", nProcessNameSize); 

    /* Set Process group id as pid of parent agent process */
    if (setpgid (0, 0) != RETURN_SUCCESS)
    {
        perror("\nUnable to set process group id as pid of agent process\n");
    }
	
    nPgid = getpgid(0);
    DEBUG_PRINT (DEBUG_LOG, "\nProcess Group Id : %d\n", nPgid);

    RpcMethods::sm_nConsoleLogFlag = FLAG_NOT_SET;
    
    /* check whether the argument is given */
    if (argc ==2)
    {       /* checks wether the given argument is equvalent to the desired string*/
            if( 0 != strcmp (argv[1],"--enable-console-log") )
            {
                    /* enables the sm_nConsoleLogFlag and write to NULL_LOG file*/
                    RpcMethods::sm_nConsoleLogFlag = FLAG_SET;
                    RpcMethods::sm_pLogStream = freopen(NULL_LOG, "w", stdout);
            }
    }
    else
    {
         /* enables the sm_nConsoleLogFlag and write to NULL_LOG file*/
         RpcMethods::sm_nConsoleLogFlag = FLAG_SET;
         RpcMethods::sm_pLogStream = freopen(NULL_LOG, "w", stdout);
    }


    /* Checking environment variable TDK_PATH */
    pszPath = getenv ("TDK_PATH");
    if (pszPath != NULL)
    {
        DEBUG_PRINT (DEBUG_LOG, "TDK_PATH : %s", pszPath);
    }
    else
    {
        DEBUG_PRINT (DEBUG_ERROR, "Alert!!! TDK_PATH not exported \n");
		
        return RETURN_FAILURE;   // Returns failure if TDK_PATH not exported
    }

    /* Extracting path to logs folder */
    strEnvPath = getenv ("TDK_PATH");
    strFolderPath.append(strEnvPath);
    strFolderPath.append("/");
    RpcMethods::sm_strTDKPath = strFolderPath;
    strFolderPath.append("logs");
    RpcMethods::sm_strLogFolderPath = strFolderPath;
    RpcMethods::sm_strLogFolderPath.append("/");

    /* Creating logs directory */
    nReturnValue = mkdir (strFolderPath.c_str(), 0777);
    if (nReturnValue != RETURN_SUCCESS)
    {
        DEBUG_PRINT (DEBUG_TRACE, "Alert!!! Unable to create logs folder \n");
    }

    /* Starting agent monitor */
    nReturnValue = AgentMonitor (argv, nProcessNameSize);

    /* closes the file */
    if(RpcMethods::sm_nConsoleLogFlag == FLAG_SET)
    {
         fclose(RpcMethods::sm_pLogStream);
    }

    DEBUG_PRINT (DEBUG_LOG, "\nAgent Shutttingdown...\n");
	
    return nReturnValue;
	
} /* End of main */



/* End of agentmain */
