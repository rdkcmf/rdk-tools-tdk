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

#include "TR069Agent.h"

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string TR069Agent::testmodulepre_requisites()
{
	return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool TR069Agent::testmodulepost_requisites()
{
	return true;
}

/***************************************************************************
 *Function name : GetHostIP
 *Arguments	: interfaceName 
 *Descrption    : Returns the ip address for the interface name passed as argument.
 *                
 *****************************************************************************/
std::string GetHostIP (const char* szInterface)
{
	struct ifaddrs* pIfAddrStruct = NULL;
	struct ifaddrs* pIfAddrIterator = NULL;
	void* pvTmpAddrPtr = NULL;
	char szAddressBuffer [INET_ADDRSTRLEN];
	getifaddrs (&pIfAddrStruct);

	for (pIfAddrIterator = pIfAddrStruct; pIfAddrIterator != NULL; pIfAddrIterator = pIfAddrIterator->ifa_next)
	{
		if (pIfAddrIterator->ifa_addr->sa_family == AF_INET)
		{
			// check it is a valid IP4 Address
			pvTmpAddrPtr = & ( (struct sockaddr_in *)pIfAddrIterator->ifa_addr )-> sin_addr;
			inet_ntop (AF_INET, pvTmpAddrPtr, szAddressBuffer, INET_ADDRSTRLEN);

			if ( (strcmp (pIfAddrIterator -> ifa_name, szInterface) ) == 0)
			{
				break;
			}
		}
	}

	DEBUG_PRINT(DEBUG_TRACE, "Found IP: %s\n",szAddressBuffer);

	if (pIfAddrStruct != NULL)
	{
		freeifaddrs (pIfAddrStruct);
	}

	return szAddressBuffer;

} /* End of GetHostIP */


/**************************************************************************
Function name : TR069Agent::initialize

Arguments     : Input arguments are Version string and TR069Agent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/
bool TR069Agent::initialize(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent Initialize----->Entry\n");

	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent Initialize----->Exit\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : TR069Agent::TR069Agent_GetParameterValue

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void TR069Agent::TR069Agent_GetParameterValue(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_GetParameterValue -->Entry\n");

	string profilePath = req["path"].asCString();	
	FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH];

	DEBUG_PRINT(DEBUG_TRACE, "Requesting Parameter Value is: %s\n",profilePath.c_str());

	/*Frame the command  */
	string path = CMD;
	path.append(profilePath);
	path.append(HTTP);

	DEBUG_PRINT(DEBUG_TRACE, "Curl Request Framed: %s\n",path.c_str());

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
		DEBUG_PRINT(DEBUG_TRACE, "Curl Response:\n");
		cout<<readRespBuff<<endl;
	}

	pclose(fp);

	/*Check for the failure case, if curl request fails  */
	if(NULL != (strcasestr(readRespBuff,"curl:")))
	{
		string curlResp(readRespBuff);
		response["result"] = "FAILURE";
		response["details"] = curlResp;
		DEBUG_PRINT(DEBUG_ERROR, "Curl Error: %s\n",curlResp.c_str());

		return;
	}
	
	string respResult(readRespBuff);
	DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",respResult.c_str());
	int pos = respResult.find("\"value\":");
	string valueString,finalString;

	if (pos != -1)
	{
		valueString = respResult.substr(pos+8);
		finalString = valueString.substr(0,valueString.length()-3);

		DEBUG_PRINT(DEBUG_LOG, "Final Value: %s\n",finalString.c_str());

		response["result"] = "SUCCESS";
		response["details"] = finalString;
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Empty No Response";

		DEBUG_PRINT(DEBUG_ERROR, "Empty No Response\n");
	}


	DEBUG_PRINT(DEBUG_LOG, "Execution success\n");

	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_GetParameterValue -->Exit\n");
	return;

}


/**************************************************************************
Function name : TR069Agent::TR069Agent_VerifyParameterValue

Arguments     : Input arguments are json request object and json response object

Description   : This method verifies the value for the parameter name and returns SUCCESS or FAILURE. 
***************************************************************************/
void TR069Agent::TR069Agent_VerifyParameterValue(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_VerifyParameterValue -->Entry\n");

	string profilePath = req["path"].asCString();

	if (profilePath ==  "Device.IP.ActivePortNumberOfEntries")
	{
		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		int noOfActivePorts = 0;

		fp = popen(GET_NUM_OF_ACTIVE_PORTS,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%d",&noOfActivePorts);
		}

		string activePorts = req["paramValue"].asCString();
		int value = atoi(activePorts.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "NumberOfActiveports: %d\n",noOfActivePorts);

		if (value == noOfActivePorts)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");
		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}

		pclose(fp);
	}
	else if(profilePath == "Device.DeviceInfo.X_COMCAST-COM_FirmwareFilename")
	{
		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		char imageName[128] = {'\0'};

		fp = popen(GET_IMAGE_VERSION,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%s",imageName);
		}

		pclose(fp);

		string firmwareName(imageName);
		string value = req["paramValue"].asCString();

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and FirmwareName: %s\n",value.c_str(),firmwareName.c_str());
		
		int len = firmwareName.size();		

		if (value.compare(0,len,firmwareName) == 0)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.MemoryStatus.Total")
	{
		struct sysinfo sys_info;

		sysinfo (&sys_info);
		unsigned int freeMemory = (unsigned int)(sys_info.totalram *(unsigned long long)sys_info.mem_unit / 1024);
		string freeValue = req["paramValue"].asCString();
		unsigned int value = atoi(freeValue.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and TotalMemory: %d\n",value,freeMemory);

		if(freeMemory == value)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.MemoryStatus.Free")
	{
		struct sysinfo sys_info;

		sysinfo (&sys_info);
		unsigned int freeMemory = (unsigned int)(sys_info.freeram *(unsigned long long)sys_info.mem_unit / 1024);
		string freeValue = req["paramValue"].asCString();
		unsigned int value = atoi(freeValue.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and freeMemory: %d\n",value,freeMemory);

		if(freeMemory >= value)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.Processor.1.Architecture")
	{
		struct utsname  utsName;
		uname(&utsName);

		string architecture(utsName.machine);

		string value = req["paramValue"].asCString();

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and Processor Architecture: %s\n",value.c_str(),architecture.c_str());

		if(value == architecture)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.IP.InterfaceNumberOfEntries")
	{
		int noOfIPInterfaces = 0;
		string cmd="ifconfig | grep \"Link encap\" | wc -l";
		char buffer[128];
		std::string result = "";
		FILE* pipe = popen(cmd.c_str(), "r");
		string num = req["paramValue"].asCString();
		int value = atoi(num.c_str());
		while(!feof(pipe)) {
			if(fgets(buffer, 128, pipe) != NULL)
				result += buffer;
		}
		if (!result.empty())
		{
			noOfIPInterfaces=atoi(result.c_str());
		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Failed to get network interface details";
			DEBUG_PRINT(DEBUG_ERROR, "Failed to get network interface details\n");
			return;

		}
		pclose(pipe);

		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and Number of IP Interfaces: %d\n",value,noOfIPInterfaces);

		if(value == noOfIPInterfaces)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if((profilePath == "Device.IP.IPv4Enable") || (profilePath == "Device.IP.IPv4Status" ))
	{

		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		int numIf = 0;

		fp = popen(GET_IPV4_ENABLE_STATUS,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%d",&numIf);
		}

		pclose(fp);

		string num = req["paramValue"].asCString();

		if (numIf == 0)
		{
			if (profilePath == "Device.IP.IPv4Enable")
			{

				if (num == "false")
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}	
			}

			if (profilePath == "Device.IP.IPv4Status")
			{
				if (num == "Disabled")	
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}
			}
		}
		else
		{
			if (profilePath == "Device.IP.IPv4Enable")
			{
				if (num == "true")
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}
			}

			if (profilePath == "Device.IP.IPv4Status")
			{
				if (num == "Enabled")
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}
			}

		}
	}
	else if(profilePath == "Device.DeviceInfo.X_COMCAST-COM_STB_IP")
	{
		string value = req["paramValue"].asCString();
		string ip = GetHostIP("eth1");	

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and IPAddress: %s\n",value.c_str(),ip.c_str());

		if(value == ip)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.X_COMCAST-COM_STB_MAC")
	{
		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		char macAddr[128] = {'\0'};

		fp = popen(GET_STB_MAC,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%s",macAddr);
		}

		pclose(fp);

		string macAddre(macAddr);
		string value = req["paramValue"].asCString();

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and MACAddress: %s\n",value.c_str(),macAddre.c_str());

		if(value == macAddre)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.UpTime")
	{
		struct sysinfo sys_info;

		sysinfo (&sys_info);
		int time = (int) sys_info.uptime;
		string timeValue = req["paramValue"].asCString();
		int value = atoi(timeValue.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and upTime: %d\n",value,time);

		/*if(time == value)*/
		if(time >= value)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Verification Failure";

		DEBUG_PRINT(DEBUG_LOG, "Profile Path not supported\n");
	}

	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_VerifyParameterValue -->Exit\n");
	return;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "TR069Agent".
 **************************************************************************/

extern "C" TR069Agent* CreateObject(TcpSocketServer &ptrtcpServer)
{
	DEBUG_PRINT(DEBUG_TRACE, "Creating TR069 Agent Object\n");

	return new TR069Agent(ptrtcpServer);
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool TR069Agent::cleanup(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
	DEBUG_PRINT(DEBUG_TRACE, "cleaningup done\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is TR069Agent Object

Description   : This function will be used to destory the TR069Agent object.
 **************************************************************************/
extern "C" void DestroyObject(TR069Agent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying TR069Agent object\n");
	delete stubobj;
}
