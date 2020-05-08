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

#include "DeviceSettingsAgent.h"

/*creating Objects for power and display classes*/
PowerChangeNotify power_obj;
DispChangeNotify display_obj;

//Check if given process is running
bool checkRunningProcess(const char *processName)
{
    char output[LINE_LEN] = {'\0'};
    char strCmd[STR_LEN] = {'\0'};
    FILE *fp = NULL;
    bool running = false;

    sprintf(strCmd,"pidof %s",processName);
    fp = popen(strCmd, "r");
    /* Read the output */
    if (fp != NULL)
    {
        if (fgets(output, sizeof(output)-1, fp) != NULL) {
            running = true;
        }
        DEBUG_PRINT(DEBUG_TRACE, "%s process id: %s\n",processName, output);
        pclose(fp);
    }
    else {
        DEBUG_PRINT(DEBUG_ERROR, "Failed to get status of process %s\n",processName);
    }

    return running;
}

/***************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper functions will be used in the 
 *  		  script
 *****************************************************************************/ 

bool DeviceSettingsAgent::initialize(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE,"DeviceSettingsAgent Initialize");
	/*initializing IARMBUS library */
	IARM_Result_t retval;
	retval=IARM_Bus_Init("agent");
	DEBUG_PRINT(DEBUG_LOG,"\nInit retval:%d\n",retval);
	if(retval==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Application Successfully initializes the IARMBUS library\n");
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Application failed to initializes the IARMBUS library\n");
	}	
	DEBUG_PRINT(DEBUG_LOG,"\n Calling IARM_BUS_Connect\n");
	/*connecting application with IARM BUS*/
	IARM_Bus_Connect();
	DEBUG_PRINT(DEBUG_LOG,"\n Application Successfully connected with IARMBUS \n");

	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *                
 *****************************************************************************/

std::string DeviceSettingsAgent::testmodulepre_requisites()
{
	return "SUCCESS";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the 
 *                pre-requisites that are set
 *                
 *****************************************************************************/

bool DeviceSettingsAgent::testmodulepost_requisites()
{
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: DSmanagerInitialize
 *Descrption	: This function is to initialize device settings library.
 *****************************************************************************/ 
void DeviceSettingsAgent::DSmanagerInitialize(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n managerInitialize ---->Entry\n");
	try
	{
		device::Manager::Initialize();
		response["result"]= "SUCCESS"; 
		response["details"]="device::Manager::Initialize SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in DSmanagerinitialize\n");
		response["result"]= "FAILURE";
		response["details"]="device::Manager::Initialize FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n managerInitialize ---->Exit\n");
	return;
}
/***************************************************************************
 *Function name	: DSmanagerDeinitialize
 *Descrption	: This function is to DeInitialize device settings library.
 *****************************************************************************/ 
void DeviceSettingsAgent::DSmanagerDeinitialize(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n managerDeinitialize ---->Entry\n");
	try
	{
		device::Manager::DeInitialize();
		response["result"]= "SUCCESS"; 
		response["details"]="device::Manager::DeInitialize SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in DSmanagerDeinitialize\n");
		response["result"]= "FAILURE";
		response["details"]="device::Manager::DeInitialize FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n managerDeinitialize ---->Exit\n");
	return;
}

bool Is_valid_indicator(std::string indicator_name)
{
	//get list of colors supported in the FrontPanel LEDs
	const device::List<device::FrontPanelIndicator> indicatorList = device::FrontPanelConfig::getInstance().getIndicators();
	size_t listSize = indicatorList.size();
	size_t i = 0;
	DEBUG_PRINT(DEBUG_LOG,"List of available indicators in the platform: \n");
	for (i = 0; i < listSize; i++)
	{
		DEBUG_PRINT(DEBUG_LOG,"Indicator id [%d]= name [%s] \n", i,indicatorList.at(i).getName().c_str());
		if ( indicator_name == indicatorList.at(i).getName().c_str())
		{
			return true;
		}
	}
	if (i == listSize)
	{
		return false;
	}
}
/***************************************************************************
 *Function name	: FPI_setBrightness
 *Descrption	: This function is to check the functionality of setBrightness and getBrightness APIs
 *@param  [in]	: req- 	indicator_name: indicator name for which the Brightness will be set and get.
			brightness: brightness level
 *****************************************************************************/ 
void DeviceSettingsAgent::FPI_setBrightness(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FPI_setBrightness ---->Entry\n");
	char brightnessDetails[30] = {'\0'};
	int setVal = req["brightness"].asInt();
	bool getOnly = req["get_only"].asInt();
	int getVal;

	try
	{
	    std::string indicator_name=req["indicator_name"].asCString();
            if (false == getOnly) {
                DEBUG_PRINT(DEBUG_LOG,"\nCalling setBrightness with value(%d)\n", setVal);
                device::FrontPanelIndicator::getInstance(indicator_name).setBrightness(setVal);
            }

            DEBUG_PRINT(DEBUG_LOG,"\nCalling getBrightness\n");
            device::FrontPanelIndicator::getInstance(indicator_name).setState(true);
            getVal = device::FrontPanelIndicator::getInstance(indicator_name).getBrightness();

	    DEBUG_PRINT(DEBUG_LOG,"\nBrightness: get value(%d)\n", getVal);
	    sprintf(brightnessDetails,"%d",getVal);
	    response["details"]= brightnessDetails;

            if ((false == getOnly) && (setVal != getVal))
	    {
                response["result"]= "FAILURE";
            }
	    else
            {
		response["result"]= "SUCCESS";
	    }
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_setBrightness\n");
		response["details"]= "Exception Caught in FPI_setBrightness";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n FPI_setBrightness ---->Exit\n");
	return ;	
}

void DeviceSettingsAgent::FPI_getBrightnessLevels(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPI_getBrightnessLevels ---->Entry\n");
        char brightnessDetails[50] = {'\0'};
        int levels, min, max;

        try
        {
            std::string indicator_name=req["indicator_name"].asCString();
            device::FrontPanelIndicator::getInstance(indicator_name).getBrightnessLevels(levels,min,max);

            DEBUG_PRINT(DEBUG_LOG,"BrightnessLevels: levels(%d) min(%d) max(%d)\n", levels,min,max);
            sprintf(brightnessDetails,"levels=%d min=%d max=%d",levels,min,max);
            response["details"]= brightnessDetails;
            response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_setBrightness\n");
                response["details"]= "Exception Caught in FPI_setBrightness";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"\n FPI_setBrightness ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name : FPI_setState
 *Descrption    : This function is to check the functionality of FrontPanel setState API
 *@param  [in]  : indicator_name: indicator name for which the state will be set.
                  state: 0 (OFF) / 1 (ON)
 *****************************************************************************/
void DeviceSettingsAgent::FPI_setState(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPI_setState ---->Entry\n");
        char details[30] = {'\0'};
        bool state = req["state"].asInt();
	std::string indicator_name = req["indicator_name"].asCString();

        try
        {
            device::FrontPanelIndicator::getInstance(indicator_name).setState(state);
            DEBUG_PRINT(DEBUG_LOG,"\nState set to %d\n", state);
            sprintf(details,"State set to %d",state);
            response["details"]= details;
            response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_setState\n");
                response["details"]= "Exception Caught in FPI_setState";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FPI_setState ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name	: FPI_setColor
 *Descrption	: This function is to check the functionality of setColor and getColor APIs
 *@param  [in]	: req- 	indicator_name: indicator name for which the color will be set and get.
				 color: color id.
 *****************************************************************************/ 
void DeviceSettingsAgent::FPI_setColor(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FPI_setColor ---->Entry\n");
	if(&req["indicator_name"]==NULL || &req["color"]==NULL)
	{
		return;
	}
	std::string indicator_name=req["indicator_name"].asCString();
	char colorDetails[20];
	int color=req["color"].asInt();
	int colorid;
        int colorSetId;
        int colorMatchId;
        int colorMode = 0;
        string colorName;
	bool valid_indicator=true;
	if(!Is_valid_indicator(indicator_name))
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Given indicator :%s is not supported\n", indicator_name.c_str());
		valid_indicator=false;
	}

	try
	{
		/*Creating object for Color*/
                switch(color)
                {
                    case 0: //blue
                      colorName = "Blue";
                      colorSetId = device::FrontPanelIndicator::Color::kBlue;
                      colorMatchId=255;
                      break;
                    case 1: //green
                      colorName = "Green";
                      colorSetId = device::FrontPanelIndicator::Color::kGreen;
                      colorMatchId=65280;
                      break;
                    case 2: //red
                      colorName = "Red";
                      colorSetId = device::FrontPanelIndicator::Color::kRed;
                      colorMatchId=16711680;
                      break;
                    case 3: //yellow
                      colorName = "Yellow";
                      colorSetId = device::FrontPanelIndicator::Color::kYellow;
                      colorMatchId=16777184;
                      break;
                    case 4: //orange
                      colorName = "Orange";
                      colorSetId = device::FrontPanelIndicator::Color::kOrange;
                      colorMatchId=16747520;
                      break;
                    case 5: //white
                      colorName = "White";
                      colorSetId = device::FrontPanelIndicator::Color::kWhite;
                      colorMatchId=16777215;
                      break;
                    default:
                      DEBUG_PRINT(DEBUG_LOG,"\n Not a supported color \n");
                      colorSetId = color;
                      colorMatchId = color;
                      break;
               }
                DEBUG_PRINT(DEBUG_LOG,"\nColorSetId retrieved is:%d\n",colorSetId);
                /*calling setcolor*/
                colorMode = device::FrontPanelIndicator::getInstance(indicator_name).getColorMode();
                DEBUG_PRINT(DEBUG_LOG,"\ncolor to set: %d color mode retrived: %d\n",color,colorMode);
                switch(colorMode)
                {
                    case 0: //always throws an exception
                      DEBUG_PRINT(DEBUG_LOG,"\ncolorMode is 0\n");
                      throw "Exception";
                    case 1: // passing the RGB value corresponding to the color to be set
                      device::FrontPanelIndicator::getInstance(indicator_name).setColor(colorSetId);
                      break;
                    case 2: // passing color object
                      device::FrontPanelIndicator::getInstance(indicator_name).setColor(device::FrontPanelIndicator::Color::getInstance(colorName));
                      break;
                    default:
                      DEBUG_PRINT(DEBUG_LOG,"\nUndefined colorMode\n");
                      throw "Exception";
                }
		/*calling getcolor*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getColor\n");
		colorid = device::FrontPanelIndicator::getInstance(indicator_name).getColor();
		DEBUG_PRINT(DEBUG_LOG,"\ncolor id retrieved is:%d\n",colorid);
		if (colorMatchId == colorid)
			response["result"]= "SUCCESS";
		else
			response["result"]= "FAILURE";

		sprintf(colorDetails,"Color:%d",colorid);
		DEBUG_PRINT(DEBUG_LOG,"\ncolor details:%s\n",(char*)colorDetails);
		response["details"]= colorDetails; 
	}
	catch(...)
	{
		if(valid_indicator == false)
		{
			DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_setColor due to invalid indicator provided\n");
			response["details"]= "Exception Caught in FPI_setColor due to invalid indicator provided";
		}
		else
		{
			DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_setColor\n");
			response["details"]= "Exception Caught in FPI_setColor";
		}
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n FPI_setColor ---->Exit\n");
	return;
}
/***************************************************************************
 *Function name	: FPI_setBlink
 *Descrption	: This function is to check the functionality of setBlink and 
 getBlink APIs
 *@param [in]	: req- 	indicator_name: indicator name for which the Blink rate 
					will be set and get.
			blink_interval: blink rate.
		       blink_iteration: Number of iteration for the blink.
 *****************************************************************************/ 
void DeviceSettingsAgent::FPI_setBlink(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FPI_setBlink ---->Entry\n");
	if(&req["indicator_name"]==NULL || &req["blink_interval"]==NULL || &req["blink_iteration"]==NULL)
	{
		return;
	}
	std::string indicator_name=req["indicator_name"].asCString();
	char blinkDetails[20];
	int interval=req["blink_interval"].asInt();
	int iteration=req["blink_iteration"].asInt();

	try
	{
		/*Creating object for blink*/
		device::FrontPanelIndicator::Blink p(interval,iteration);
		/*calling setBlink*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setBlink\n");
		device::FrontPanelIndicator::getInstance(indicator_name).setBlink(p);
		/*calling getBlink*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getBlink\n");
		p = device::FrontPanelIndicator::getInstance(indicator_name).getBlink();
		DEBUG_PRINT(DEBUG_LOG,"\nblink Interval:%d\n",p.getInterval());
		DEBUG_PRINT(DEBUG_LOG,"\nblink Iteration:%d\n",p.getIteration());
		sprintf(blinkDetails,"Blink Rate:%d::%d",p.getInterval(),p.getIteration());
		response["details"]= blinkDetails;

		if ((interval == p.getInterval()) && (iteration == p.getIteration()))
			response["result"]= "SUCCESS";
		else
			response["result"]= "FAILURE";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_setBlink\n");
		response["details"]= "Exception Caught in FPI_setBlink";
		response["result"]= "FAILURE";
	}

	DEBUG_PRINT(DEBUG_TRACE,"\n FPI_setBlink ---->Exit\n");
	return;
}


/***************************************************************************
 *Function name	: FPTEXT_setScroll
 *Descrption  	: This function is to check the functionality of setScroll and 
 getScroll APIs
 *@param  [in]	: req- 	text: input for scrolling the text in the 7-segment LEDs for 
                              the given iterations.
	       hold_duration: Duration for scroll hold
               hiteration   : Number of Horizontal Iterations
               viteration   : Number of Vertical Iterations
 *****************************************************************************/ 
void DeviceSettingsAgent::FPTEXT_setScroll(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FPTEXT_setScroll ---->Entry\n");
	if(&req["text"]==NULL||&req["viteration"]==NULL||&req["hiteration"]==NULL||&req["hold_duration"]==NULL)
	{
		return;
	}
	char scrollDetails[40];
	int vIteration=req["viteration"].asInt();
	int hIteration=req["hiteration"].asInt();
	int holdDuration=req["hold_duration"].asInt();

	try
	{
		/*Creating object for Scroll*/
		device::FrontPanelTextDisplay::Scroll s(vIteration,hIteration,holdDuration);
		/*calling setScroll info*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setScroll\n");
		device::FrontPanelTextDisplay::getInstance("Text").setScroll(s);
		/*calling getScroll info*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getScroll\n");
		s = device::FrontPanelTextDisplay::getInstance("Text").getScroll();
		sprintf(scrollDetails,"Scroll :: %d:%d:%d",s.getVerticalIteration(),s.getHorizontalIteration(),s.getHoldDuration());
		DEBUG_PRINT(DEBUG_LOG,"VerticalIteration:HorizontalIteration:HoldDuration: %s\n",scrollDetails);
		response["details"]= scrollDetails;
		if ((vIteration == s.getVerticalIteration()) && (hIteration == s.getHorizontalIteration()) && (holdDuration == s.getHoldDuration()))
			response["result"]= "SUCCESS";
		else
			response["result"]= "FAILURE";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_setScroll\n");
		response["details"]= "Exception Caught in FPTEXT_setScroll";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n FPTEXT_setScroll ---->Exit\n");
	return;
}

void DeviceSettingsAgent::FPTEXT_getTextColorMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPTEXT_getTextColorMode ---->Entry\n");
        try
        {
		char details[20];
                int colorMode = device::FrontPanelTextDisplay::getInstance("Text").getTextColorMode();
                sprintf(details,"%d",colorMode);
                DEBUG_PRINT(DEBUG_LOG,"Text Color Mode: %d\n",colorMode);
                if ( 0 <= colorMode )
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Invalid text color mode value";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_getTextColorMode\n");
                response["details"]= "Exception Caught in FPTEXT_getTextColorMode";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"FPTEXT_getTextColorMode ---->Exit\n");
        return;
}


void DeviceSettingsAgent::FPTEXT_getTextBrightnessLevels(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPTEXT_getTextBrightnessLevels ---->Entry\n");
        char brightnessDetails[50] = {'\0'};
        int levels=0, min=0, max=0;

        try
        {
                device::FrontPanelTextDisplay::getInstance("Text").getTextBrightnessLevels(levels,min,max);
		DEBUG_PRINT(DEBUG_LOG,"Text Brightness Levels: levels(%d) min(%d) max(%d)\n", levels,min,max);
		sprintf(brightnessDetails,"levels=%d min=%d max=%d",levels,min,max);
		response["details"]= brightnessDetails;
                response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_getTextBrightnessLevels\n");
                response["details"]= "Exception Caught in FPTEXT_getTextBrightnessLevels";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"FPTEXT_getTextBrightnessLevels ---->Exit\n");
        return;
}


void DeviceSettingsAgent::FPTEXT_setTextBrightness(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_setTextBrightness ---->Entry\n");
        char brightnessDetails[30] = {'\0'};
        int setVal = req["brightness"].asInt();

        try
        {
            DEBUG_PRINT(DEBUG_LOG,"Calling setTextBrightness with value(%d)\n", setVal);
            device::FrontPanelTextDisplay::getInstance("Text").setTextBrightness(setVal);

            DEBUG_PRINT(DEBUG_LOG,"Calling getTextBrightness\n");
            int getVal = device::FrontPanelTextDisplay::getInstance("Text").getTextBrightness();

            DEBUG_PRINT(DEBUG_LOG,"Brightness: get value(%d)\n", getVal);
            sprintf(brightnessDetails,"%d",getVal);
            response["details"]= brightnessDetails;

            if (setVal != getVal)
            {
                response["result"]= "FAILURE";
            }
            else
            {
                response["result"]= "SUCCESS";
            }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_setTextBrightness\n");
                response["details"]= "Exception Caught in setTextBrightness";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"FPTEXT_setTextBrightness ---->Exit\n");
        return;
}

void DeviceSettingsAgent::FPTEXT_getTextBrightness(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_getTextBrightness ---->Entry\n");
        char brightnessDetails[30] = {'\0'};
        int getVal;

        try
        {
            getVal = device::FrontPanelTextDisplay::getInstance("Text").getTextBrightness();
            DEBUG_PRINT(DEBUG_LOG,"\nBrightness: get value(%d)\n", getVal);
            sprintf(brightnessDetails,"%d",getVal);
            response["details"]= brightnessDetails;
            response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_getTextBrightness\n");
                response["details"]= "Exception Caught in getTextBrightness";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_getTextBrightness ---->Exit\n");
        return;
}

void DeviceSettingsAgent::FPTEXT_enableDisplay(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPTEXT_enableDisplay ---->Entry\n");
	bool enable = req["enable"].asInt();

        try
        {
	    //enable or disable the display of clock on front panel
	    DEBUG_PRINT(DEBUG_LOG,"Setting enable to %d\n", enable);
            device::FrontPanelTextDisplay::getInstance("Text").enableDisplay(enable);
	    response["result"]= "SUCCESS";
	    if (true == enable)
            	response["details"]= "Set display of clock on front panel to enable";
	    else
                response["details"]= "Set display of clock on front panel to disable";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in FPTEXT_enableDisplay\n");
                response["details"]= "Exception Caught in enableDisplay";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_enableDisplay ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name	: AOP_setLevel
 *Descrption	: This function is to check the functionality of setLevel and 
                  getLevel APIs
 *@param [in]	: req- 	port_name: video port(corresponding audio) for which audio level will be set and get.
                      audio_level: audio level for a given output audio port
 *****************************************************************************/ 
void DeviceSettingsAgent::AOP_setLevel(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setLevel ---->Entry\n");
	if(&req["port_name"]==NULL || &req["audio_level"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char levelDetails1[20] ="Audio Level:";
	float level=req["audio_level"].asFloat();
	printf("\nLevel:%f\n\n",level);
	float audio_level;
	char *levelDetails = (char*)malloc(sizeof(char)*20);
	memset(levelDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setLevel\n");
		aPort.setLevel(level);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getLevel\n");
		audio_level=aPort.getLevel();
		sprintf(levelDetails,"%.3f",audio_level);
		strcat(levelDetails1,levelDetails);
		response["details"]= levelDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setLevel\n");
		response["details"]= "Exception Caught in AOP_setLevel";
		response["result"]= "FAILURE";
	}
	free(levelDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setLevel ---->Exit\n");
	return;
}


/***************************************************************************
 *Function name	: AOP_setDB 
 *Descrption 	: This function is to check the functionality of setDB and 
                  getDB APIs.This also checks maximum and minimum DB values
 *@param  [in]	: req- 	port_name: video port( corresponding audio) for which audio DB value will be set and get.
                         db_level: audio DB level for a given output audio port
 *****************************************************************************/ 

void DeviceSettingsAgent::AOP_setDB(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setDB ---->Entry\n");
	if(&req["port_name"]==NULL||&req["db_level"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char dBDetails1[60] ="DB:";
	char maxDBDetails1[20] ="maxDB:";
	char minDBDetails1[20] ="minDB:";
	float maxDB,minDB;
	float dBValue = req["db_level"].asFloat();
	float dBval;
	char *dBDetails = (char*)malloc(sizeof(char)*20);
	memset(dBDetails,'\0', (sizeof(char)*20));
	char *maxDBDetails = (char*)malloc(sizeof(char)*20);
	memset(maxDBDetails,'\0', (sizeof(char)*20));
	char *minDBDetails = (char*)malloc(sizeof(char)*20);
	memset(minDBDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setDB\n");
		aPort.setDB(dBValue);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getDB\n");
		DEBUG_PRINT(DEBUG_LOG,"\ngetDB:%f\n",aPort.getDB());
		dBval = aPort.getDB();
		sprintf(dBDetails,"%f",dBval);
		strcat(dBDetails1,dBDetails);
		/*getting maxDB and minDB of audio*/
		maxDB=aPort.getMaxDB();
		minDB=aPort.getMinDB();
		sprintf(maxDBDetails,"%f",maxDB);
		strcat(maxDBDetails1,maxDBDetails);
		sprintf(minDBDetails,"%f",minDB);
		strcat(minDBDetails1,minDBDetails);
		strcat(dBDetails1,",");
		strcat(dBDetails1,maxDBDetails1);
		strcat(dBDetails1,",");
		strcat(dBDetails1,minDBDetails1);
		/*Copying the audio DB details to json details parameter*/
		response["details"]= dBDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setDB\n");
		response["details"]= "Exception Caught in AOP_setDB";
		response["result"]= "FAILURE";
	}
	free(dBDetails);
	free(maxDBDetails);
	free(minDBDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setDB ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: VD_setDFC 
 *Descrption 	: This function is to check the functionality of setDFC and 
                  getDFC APIs.
 *@param  [in]	: req- 	zoom_setting: new zoom setting for the video device.
 *****************************************************************************/ 

void DeviceSettingsAgent::VD_setDFC(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"VD_setDFC ---->Entry\n");
	if(&req["zoom_setting"]==NULL)
	{
		return;
	}

	try
	{
		std::string zoomSetting=req["zoom_setting"].asCString();
		/*getting video device instance*/
		device::VideoDevice decoder = device::Host::getInstance().getVideoDevices().at(0);
		DEBUG_PRINT(DEBUG_LOG,"Calling setDFC\n");
		decoder.setDFC(zoomSetting);
		DEBUG_PRINT(DEBUG_LOG,"getDFC: %s\n", decoder.getDFC().getName().c_str());
		if (decoder.getDFC().getName() == zoomSetting)
		{
			response["result"]= "SUCCESS";
			response["details"]= "setDFC successful";	
		}
		else
		{
			response["result"]= "FAILED";
			response["details"]= "setDFC failed";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VD_setDFC\n");
		response["details"]= "Exception Caught in VD_setDFC";
		response["result"]= "FAILURE";
	}

	DEBUG_PRINT(DEBUG_TRACE,"VD_setDFC ---->Exit\n");
	return;
}

void DeviceSettingsAgent::VD_setPlatformDFC(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VD_setPlatformDFC ---->Entry\n");

        try
        {
		char platformDFCDetails[50] = {'\0'};
                /*getting video device instance*/
                device::VideoDevice decoder = device::Host::getInstance().getVideoDevices().at(0);
                decoder.setPlatformDFC();
		sprintf(platformDFCDetails,"%s",decoder.getDFC().getName().c_str());
                response["details"]= platformDFCDetails;
                response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VD_setPlatformDFC\n");
                response["details"]= "Exception Caught in VD_setPlatformDFC";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VD_setPlatformDFC ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VD_getSupportedDFCs(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VD_getSupportedDFCs ---->Entry\n");

        try
        {
                char details[256] = {'\0'};
		const device::List<device::VideoDevice> vDevices = device::VideoDeviceConfig::getInstance().getDevices();
		DEBUG_PRINT(DEBUG_TRACE,"vDevices Size:%d\n", vDevices.size());
		for (size_t i = 0; i < vDevices.size(); i++)
		{
			const device::List <device::VideoDFC> dfcs = vDevices.at(i).getSupportedDFCs();
			DEBUG_PRINT(DEBUG_TRACE,"vDevice:%s dfcsSize:%d\n",vDevices.at(i).getName().c_str(), dfcs.size());
                        strcat(details, vDevices.at(i).getName().c_str());
                        strcat(details," DFCs:");
			for (size_t j = 0; j < dfcs.size(); j++)
			{
				strcat(details, dfcs.at(j).getName().c_str());
				if( j < dfcs.size()-1 )
                         	{
                                	strcat(details,",");
                        	}
			}
			if( i < vDevices.size()-1 )
			{
				strcat(details,"::");
			}
		}

                if (vDevices.at(0).getSupportedDFCs().size() != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of supported dfcs for video devices";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VD_getSupportedDFCs\n");
                response["details"]= "Exception Caught in VD_getSupportedDFCs";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VD_getSupportedDFCs ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VD_getHDRCapabilities(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VD_getHDRCapabilities ---->Entry\n");

        try
        {
                char details[256] = {'\0'};
		int Capabilities =0;
	        char *HDRCap = (char*)malloc(sizeof(char)*20);
	        memset(HDRCap,'\0', (sizeof(char)*20));
                DEBUG_PRINT(DEBUG_LOG,"Calling getHDRCapabilities\n");
                device::VideoDevice decoder = device::Host::getInstance().getVideoDevices().at(0);
                DEBUG_PRINT(DEBUG_LOG,"Calling DSgetHDRCapabilities\n");
                decoder.getHDRCapabilities(&Capabilities);
		DEBUG_PRINT(DEBUG_LOG,"HDR Capabilities = %d\n",Capabilities);
		strcat(details," Capabilities:");
		sprintf(HDRCap, "%d" , Capabilities);
		strcat(details,HDRCap);
		response["details"]=details;
		response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VD_getHDRCapabilities\n");
                response["details"]= "Exception Caught in VD_getHDRCapabilities";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VD_HDRCapabilities ---->Exit\n");
        return;
}




void DeviceSettingsAgent::VDCONFIG_getDevices(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VDCONFIG_getDevices ---->Entry\n");

        try
        {
                char details[256] = {'\0'};
                device::List<device::VideoDevice> vDevices = device::VideoDeviceConfig::getInstance().getDevices();
		DEBUG_PRINT(DEBUG_TRACE,"getDevices Size: %d\n", vDevices.size());

                for (size_t i = 0; i < vDevices.size(); i++)
                {
                        strcat(details, vDevices.at(i).getName().c_str());
                        if( i < vDevices.size()-1 )
			{
                                strcat(details,",");
			}
                }

                if (vDevices.size() != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of supported video devices";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VDCONFIG_getDevices\n");
                response["details"]= "Exception Caught in VDCONFIG_getDevices";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VDCONFIG_getDevices ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VDCONFIG_getDFCs(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VDCONFIG_getDFCs ---->Entry\n");

        try
        {
                char details[256] = {'\0'};
                const device::List <device::VideoDFC> dfcs = device::VideoDeviceConfig::getInstance().getDFCs();
                DEBUG_PRINT(DEBUG_TRACE,"getDFCs Size: %d\n", dfcs.size());
                for (size_t i = 0; i < dfcs.size(); i++)
                {
                        strcat(details, dfcs.at(i).getName().c_str());
                        if( i < dfcs.size()-1 )
                        {
                                strcat(details,",");
                        }
                }

                if (dfcs.size() != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of dfcs";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VDCONFIG_getDFCs\n");
                response["details"]= "Exception Caught in VDCONFIG_getDFCs";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VDCONFIG_getDFCs ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VDCONFIG_getDefaultDFC(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VDCONFIG_getDefaultDFC ---->Entry\n");

        try
        {
                char details[50] = {'\0'};
                device::VideoDFC dfc = device::VideoDeviceConfig::getInstance().getDefaultDFC();
                DEBUG_PRINT(DEBUG_TRACE,"DefaultDFC: %s\n", dfc.getName().c_str());
                sprintf(details,"%s",dfc.getName().c_str());
		response["details"]=details;
		response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VDCONFIG_getDefaultDFC\n");
                response["details"]= "Exception Caught in VDCONFIG_getDefaultDFC";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VDCONFIG_getDefaultDFC ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name	: AOP_setEncoding
 *Descrption	: This function is to check the functionality of setEncoding and 
                  getEncoding APIs.
 *@param [in]	: req- 	port_name: video port (corresponding audio port) Encoding format will be set and get.
                  encoding_format: encoding format to be set for audio port.
 *****************************************************************************/ 
void DeviceSettingsAgent::AOP_setEncoding(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setEncoding ---->Entry\n");
	if(&req["port_name"]==NULL||&req["encoding_format"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char encodingDetails1[30] ="Encoding Format:";
	std::string encodingFormat=req["encoding_format"].asCString();
	char *encodingDetails = (char*)malloc(sizeof(char)*20);
	memset(encodingDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setEncoding\n");
		aPort.setEncoding(encodingFormat);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getEncoding\n");
		DEBUG_PRINT(DEBUG_LOG,"\ngetEncoding::%s\n",aPort.getEncoding().getName().c_str());
		sprintf(encodingDetails,"%s",aPort.getEncoding().getName().c_str());
		strcat(encodingDetails1,encodingDetails);
		response["details"]= encodingDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setEncoding\n");
		response["details"]= "Exception Caught in AOP_setEncoding";
		response["result"]= "FAILURE";
	}
	free(encodingDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setEncoding ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: AOP_setCompression
 *Descrption	: This function is to check the functionality of setCompression and 
                  getCompression APIs.
 *@param retval : req- 	port_name: port for which compression format will be set and get.
               compression_format: compression format to be set for audio port.
 ***************************************************************************/
void DeviceSettingsAgent::AOP_setCompression(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setCompression ---->Entry\n");
	if(&req["port_name"]==NULL||&req["compression_format"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char compressionDetails1[60] ="Compression format:";
        const int compressionFormat=req["compression_format"].asInt();
	char *compressionDetails = (char*)malloc(sizeof(char)*200);
	memset(compressionDetails,'\0', (sizeof(char)*200));
	try
	{
		printf("\ncompressionDetails1:%s\n",compressionDetails1);
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setCompression\n");
		aPort.setCompression(compressionFormat);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getCompression\n");
		DEBUG_PRINT(DEBUG_LOG,"\nGetCompression:%d\n",aPort.getCompression());
		sprintf(compressionDetails,"%d",aPort.getCompression());
		printf("\ncompressionDetails1:%s\n",compressionDetails1);
		strcat(compressionDetails1,compressionDetails);
		response["details"]= compressionDetails1; 
		response["result"]="SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setCompression\n");
		response["details"]= "Exception Caught in AOP_setCompression";
		response["result"]= "FAILURE";
	}

	free(compressionDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setCompression ---->Exit\n");
	return;
}
/***************************************************************************
 *Function name	: AOP_setStereoMode
 *Descrption	: This function is to check the functionality of setStereoMode and 
                  getStereoMode APIs.
 *@param [in]	: req- 	port_name: port for which StereoModes will be set and get.
                      stereo_mode: stereo mode to be set for audio port.
 ***************************************************************************/
void DeviceSettingsAgent::AOP_setStereoMode(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setStereoMode ---->Entry\n");
	if(&req["port_name"]==NULL||&req["stereo_mode"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char stereoModeDetails1[60] ="Mode:";
	std::string stereoMode=req["stereo_mode"].asCString();
	char *stereoModeDetails = (char*)malloc(sizeof(char)*20);
	memset(stereoModeDetails,'\0', (sizeof(char)*20));
	bool getOnly = req["get_only"].asInt();
	bool persistence = req["persist"].asInt();
	try
	{
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = device::Host::getInstance().getAudioOutputPort(portName);
                if (false == getOnly)
                {
			DEBUG_PRINT(DEBUG_LOG,"\nCalling setStereoMode\n");
			aPort.setStereoMode(stereoMode);
		}
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getStereoMode\n");
		DEBUG_PRINT(DEBUG_LOG,"\ngetStereroMode:%s\n",aPort.getStereoMode(persistence).getName().c_str());
		sprintf(stereoModeDetails,"%s",aPort.getStereoMode(persistence).getName().c_str());
		strcat(stereoModeDetails1,stereoModeDetails);
		response["details"]= stereoModeDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setStreoeMode\n");
		response["details"]= "Exception Caught in AOP_setStreoeMode";
		response["result"]= "FAILURE";
	}
	free(stereoModeDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setStreoeMode ---->Exit\n");
	return;
}

void DeviceSettingsAgent::AOP_setStereoAuto(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOP_setStereoAuto ---->Entry\n");

        try
        {
		std::string portName=req["port_name"].asCString();
		bool autoMode = req["autoMode"].asInt();
		char details[30] = {'\0'};

                //Get AudioOutputPort instance for specified port name
                device::AudioOutputPort aPort = device::AudioOutputPort::getInstance(portName);
		DEBUG_PRINT(DEBUG_LOG,"Calling setStereoAuto\n");
		aPort.setStereoAuto(autoMode);
		DEBUG_PRINT(DEBUG_LOG,"getStereoAuto:%d\n",aPort.getStereoAuto());
		sprintf(details,"SET VALUE:%d GET VALUE:%d",autoMode,aPort.getStereoAuto());
		response["details"] = details;
                if ( autoMode == aPort.getStereoAuto() )
                {
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setStereoAuto\n");
                response["details"]= "Exception Caught in AOP_setStereoAuto";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOP_setStereoAuto ---->Exit\n");
        return;
}


void DeviceSettingsAgent::AOP_getStereoAuto(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOP_getStereoAuto ---->Entry\n");

        try
        {
                std::string portName=req["port_name"].asCString();
                char details[30] = {'\0'};

                DEBUG_PRINT(DEBUG_LOG,"Calling getStereoAuto\n");
		int autoMode = device::AudioOutputPort::getInstance(portName).getStereoAuto();
                DEBUG_PRINT(DEBUG_LOG,"getStereoAuto:%d\n", autoMode);
                sprintf(details,"%d",autoMode);
                response["details"] = details;
                if ( (0 <= autoMode) && (autoMode <= 1) )
                {
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getStereoAuto\n");
                response["details"]= "Exception Caught in AOP_getStereoAuto";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOP_getStereoAuto ---->Exit\n");
        return;
}


void DeviceSettingsAgent::AOP_getGain(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOP_getGain ---->Entry\n");

        try
        {
                std::string portName=req["port_name"].asCString();
                char details[30] = {'\0'};

                DEBUG_PRINT(DEBUG_LOG,"Calling getGain\n");
                float gain = device::AudioOutputPort::getInstance(portName).getGain();
                DEBUG_PRINT(DEBUG_LOG,"getGain:%f\n", gain);
                sprintf(details,"%f",gain);
                response["details"] = details;
		response["result"] = "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getGain\n");
                response["details"]= "Exception Caught in AOP_getGain";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOP_getGain ---->Exit\n");
        return;
}


void DeviceSettingsAgent::AOP_getOptimalLevel(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOP_getOptimalLevel ---->Entry\n");

        try
        {
                std::string portName=req["port_name"].asCString();
                char details[30] = {'\0'};

                DEBUG_PRINT(DEBUG_LOG,"Calling getOptimalLevel\n");
                float optimalLevel = device::AudioOutputPort::getInstance(portName).getOptimalLevel();
                DEBUG_PRINT(DEBUG_LOG,"getOptimalLevel:%f\n", optimalLevel);
                sprintf(details,"%f",optimalLevel);
                response["details"] = details;
                response["result"] = "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getOptimalLevel\n");
                response["details"]= "Exception Caught in AOP_getOptimalLevel";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOP_getOptimalLevel ---->Exit\n");
        return;
}


/***************************************************************************
 *Function name	: HOST_setPowerMode
 *Descrption	: This function is to check the functionality of setPowerMode and 
                  getPowerMode APIs.
 *@param [in]	: req- 	new_power_state: new power state to be set for decoder.
		  POWER_ON=1, POWER_STANDBY=2, POWER_OFF=3
 ***************************************************************************/
void DeviceSettingsAgent::HOST_setPowerMode(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setPowerMode ---->Entry\n");
	if(&req["new_power_state"]==NULL)
	{
		return;
	}
	int power_state=req["new_power_state"].asInt();
	try
	{
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setPowerMode\n");
		device::Host::getInstance().setPowerMode(power_state);
		int mode = device::Host::getInstance().getPowerMode();
		if (mode == power_state)
		{
			response["details"]= "Power Mode Set";
			response["result"]= "SUCCESS";
		}
		else
		{
			response["details"]= "Power Mode Not Set";
			response["result"]= "FAILURE";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_setPowerMode\n");
		response["details"]= "Exception Caught in HOST_setPowerMode";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setPowerMode ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: VOP_setResolution
 *Descrption	: This function is to check the functionality of setResolution and 
                  getResolution APIs.
 *@param [in]	: req- 	resolution: new resolution for the given video port.
                        port_name : the port for which the resolution will be 
                                    set and get.
 ***************************************************************************/
void DeviceSettingsAgent::VOP_setResolution(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n VOP_setResolution  ---->Entry\n");
	char getValue[30] = {'\0'};
	if(&req["port_name"]==NULL || &req["resolution"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	std::string setValue=req["resolution"].asCString();
	bool getOnly = req["get_only"].asInt();

	try
	{	/*getting video port instance*/
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		if (false == getOnly) {
		    /*setting VOP resolution*/
		    DEBUG_PRINT(DEBUG_LOG,"\nCalling setResolution with value (%s)\n", setValue.c_str());
		    vPort.setResolution(setValue.c_str());
		}
		/*getting VOP resolution*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getResolution\n");
		/*Need to check the return string value with test apps*/
		sprintf(getValue,"%s",(char*)vPort.getResolution().getName().c_str());
		response["details"]= getValue;
		DEBUG_PRINT(DEBUG_LOG,"\nResolution get value(%s)\n", getValue);
		if ((false == getOnly) && strncmp(setValue.c_str(), getValue, strlen(setValue.c_str())) != 0)
		{
			response["result"]= "FAILURE";
		}
		else
		{
			response["result"]= "SUCCESS";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in setResolution\n");
		response["details"]= "Exception Caught in setResolution";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n setResolution ---->Exit\n");
	return;
}


void DeviceSettingsAgent::FPCONFIG_getIndicatorFromName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getIndicatorFromName  ---->Entry\n");
	std::string indicator_name = req["indicator_name"].asCString();

        try
        {
		//Get FrontPanelndicator instance corresponding to the name parameter
		device::FrontPanelIndicator nameIndicator = device::FrontPanelConfig::getInstance().getIndicator(indicator_name);
            	string outName = nameIndicator.getName();
		DEBUG_PRINT(DEBUG_LOG,"Retrieved indicator Name: %s\n",outName.c_str());
		if ( (indicator_name == outName) )
		{
			response["result"]= "SUCCESS";
			response["details"]="Successfully retrieved FrontPanelndicator instance";
                }
		else
		{
			response["result"]= "FAILURE";
			response["details"]="Failed to retrieve FrontPanelndicator instance";
		}
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPCONFIG_getIndicatorFromName\n");
                response["details"]= "Exception Caught in FPCONFIG_getIndicatorFromName";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getIndicatorFromName ---->Exit\n");
        return;
}


void DeviceSettingsAgent::FPCONFIG_getIndicatorFromId(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getIndicatorFromId  ---->Entry\n");
        int indicator_id = req["indicator_id"].asInt();

        try
        {
		//Get FrontPanelndicator instance with the specified id
		device::FrontPanelIndicator idIndicator = device::FrontPanelConfig::getInstance().getIndicator(indicator_id);
                string name = idIndicator.getName();
                int id = idIndicator.getId();
                int indicatorSize = device::FrontPanelConfig::getInstance().getIndicators().size();
                DEBUG_PRINT(DEBUG_LOG,"Retrieved indicator Name: %s Id:%d Size:%d\n",name.c_str(),id,indicatorSize);
                if ( (indicator_id == id) && (id <= indicatorSize) )
                {
                        response["result"]= "SUCCESS";
                        response["details"]="Successfully retrieved FrontPanelndicator instance";
                }
                else
                {
                        response["result"]= "FAILURE";
                        response["details"]="Failed to retrieve FrontPanelndicator instance";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPCONFIG_getIndicatorFromId\n");
                response["details"]= "Exception Caught in FPCONFIG_getIndicatorFromId";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getIndicatorFromId ---->Exit\n");
        return;
}


/***************************************************************************
 *Functiion name	: FPCONFIG_getIndicators
 *Descrption		: This function is wrapper function to get the list of indicators 
                          supported in the FrontPanel.
 *****************************************************************************/ 
void DeviceSettingsAgent::FPCONFIG_getIndicators(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFPCONFIG_getIndicators  ---->Entry\n");
	char indicators[200] = {'\0'};

	try
	{
		/*Get list of Indicators supported in the FrontPanel*/
		device::List<device::FrontPanelIndicator> indicatorList = device::FrontPanelConfig::getInstance().getIndicators();
		size_t indSize = indicatorList.size();
		DEBUG_PRINT(DEBUG_LOG,"Indicator size:%d\n", indSize);
		for (size_t i = 0; i < indSize; i++)
		{
			strcat(indicators, indicatorList.at(i).getName().c_str());
			if( i < indSize-1 )
			{
				strcat(indicators,",");
			}
                }
		if (indSize != 0)
		{
			response["details"]=indicators;
			response["result"]= "SUCCESS";
		}
		else
		{
			response["details"]="Failed to get list of indicators";
			response["result"]= "FAILURE";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPCONFIG_getIndicators\n");
		response["details"]= "Exception Caught in getIndicators";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nFPCONFIG_getIndicators  ---->Exit\n");
	return;
}

void DeviceSettingsAgent::FPCONFIG_getTextDisplayFromName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getTextDisplayFromName  ---->Entry\n");
        std::string text_name = req["text_name"].asCString();

        try
        {
                //Get FrontPanelTextDisplay instance corresponding to the name parameter
		device::FrontPanelTextDisplay instance = device::FrontPanelConfig::getInstance().getTextDisplay(text_name);
                string outName = instance.getName();
                DEBUG_PRINT(DEBUG_LOG,"Retrieved FrontPanelTextDisplay Name: %s\n",outName.c_str());
                if ( (text_name == outName) )
                {
                        response["result"]= "SUCCESS";
                        response["details"]="Successfully retrieved FrontPanelTextDisplay instance";
                }
                else
                {
                        response["result"]= "FAILURE";
                        response["details"]="Failed to retrieve FrontPanelTextDisplay instance";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPCONFIG_getTextDisplayFromName\n");
                response["details"]= "Exception Caught in FPCONFIG_getTextDisplayFromName";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getTextDisplayFromName ---->Exit\n");
        return;
}

void DeviceSettingsAgent::FPCONFIG_getTextDisplayFromId(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getTextDisplayFromId  ---->Entry\n");
        int text_id = req["text_id"].asInt();

        try
        {
                //Get FrontPanelTextDisplay instance corresponding to the id parameter
		device::FrontPanelTextDisplay instance = device::FrontPanelConfig::getInstance().getTextDisplay(text_id);
                string name = instance.getName();
                int id = instance.getId();
                DEBUG_PRINT(DEBUG_LOG,"Retrieved FrontPanelTextDisplay Name: %s Id:%d\n",name.c_str(),id);
                if ( (text_id == id) )
                {
                        response["result"]= "SUCCESS";
                        response["details"]="Successfully retrieved FrontPanelTextDisplay instance";
                }
                else
                {
                        response["result"]= "FAILURE";
                        response["details"]="Failed to retrieve FrontPanelTextDisplay instance";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPCONFIG_getTextDisplayFromId\n");
                response["details"]= "Exception Caught in FPCONFIG_getTextDisplayFromId";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getTextDisplayFromId ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name	: FPI_getSupportedColors
 *Descrption	: This function is wrapper function to get the list of colors 
                  supported for a LED in the FrontPanel.
 *parameter[in]	: req- indicator_name: indicator name, "Text"
 *****************************************************************************/ 

void DeviceSettingsAgent::FPI_getSupportedColors(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFPI_getSupportedColors ---->Entry\n");
	bool valid_indicator=true;  

	try
	{
		char colors[512] = {'\0'};
		std::string indicator_name=req["indicator_name"].asCString();	
        	if(!Is_valid_indicator(indicator_name))
		{
			DEBUG_PRINT(DEBUG_ERROR,"\n Given indicator :%s is not supported\n", indicator_name.c_str());
			valid_indicator=false;
		}
                
		//get list of colors supported in the FrontPanel LEDs
		const device::List<device::FrontPanelIndicator::Color> colorList = device::FrontPanelIndicator::getInstance(indicator_name).getSupportedColors();
                size_t listSize = colorList.size();
		DEBUG_PRINT(DEBUG_LOG,"No. of supported colors for %s indicator: %d\n",indicator_name.c_str(), listSize);
                for (size_t i = 0; i < listSize; i++)
                {
			strcat(colors,colorList.at(i).getName().c_str());
			if( i < listSize -1 )
			{
				strcat(colors,",");
			}
                }
		DEBUG_PRINT(DEBUG_LOG,"%s Indicator SupportedColors: %s\n",indicator_name.c_str(), colors);
	
		if (colorList.size() != 0)
		{
                	response["details"]=colors;
                	response["result"]= "SUCCESS";
		}
		else
		{
                	response["details"]="Failed to get supported colors for indicator";
                	response["result"]= "FAILURE";
		}

	}
	catch(...)
	{
		if(valid_indicator == false)
		{
			DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_setColor due to invalid indicator provided\n");
			response["details"]= "Exception Caught in FPI_setColor due to invalid indicator provided";
		}
		else
		{
			DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPI_getSupportedColors\n");
			response["details"]= "Exception Caught in FPI_getSupportedColors";
		}
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nFPI_getSupportedColors ---->Exit\n");
	return;
}


void DeviceSettingsAgent::FPI_getColorMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPI_getColorMode ---->Entry\n");
        char details[20] = {'\0'};
        std::string indicator_name = req["indicator_name"].asCString();

        try
        {
		//Check whether single or multi color mode, default is set to 0 to indicate single color mode
		int colorMode = device::FrontPanelIndicator::getInstance(indicator_name).getColorMode();
                DEBUG_PRINT(DEBUG_LOG,"Color Mode: %d\n",colorMode);
		sprintf(details,"%d",colorMode);
		if ( 0 <= colorMode )
		{
                	response["details"]=details;
                	response["result"]= "SUCCESS";
		}
		else
		{
			response["details"]="Invalid color mode value";
			response["result"]= "FAILURE";
		}
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in FPI_getColorMode\n");
                response["details"]= "Exception Caught in FPI_getColorMode";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FPI_getColorMode ---->Exit\n");
        return;
}



/***************************************************************************
 *Function name	: FPCONFIG_getTextDisplays
 *Descrption	: This function is wrapper function to get a list of text display 
                  subpanels on the front panel.
 *****************************************************************************/ 
void DeviceSettingsAgent::FPCONFIG_getTextDisplays(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getTextDisplays ---->Entry\n");
	char textDisplayDetails[200] = {'\0'};

	try
	{
                /*Get list of text display supported by the front panel*/
                device::List<device::FrontPanelTextDisplay> displayList = device::FrontPanelConfig::getInstance().getTextDisplays();
                size_t listSize = displayList.size();
                DEBUG_PRINT(DEBUG_LOG,"TextDisplays size: %d\n", listSize);
                for (size_t i = 0; i < listSize; i++)
                {
                        strcat(textDisplayDetails, displayList.at(i).getName().c_str());
                        if( i < listSize-1 )
                        {
                                strcat(textDisplayDetails,",");
                        }
                }
                if (listSize != 0)
                {
                        response["details"]=textDisplayDetails;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of text displays";
                        response["result"]= "FAILURE";
                }
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPCONFIG_getTextDisplays\n");
		response["details"]= "Exception Caught in FPCONFIG_getTextDisplays";
		response["result"]= "FAILURE";
	}

	DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getTextDisplays  ---->Exit\n");
	return;
}

void DeviceSettingsAgent::FPCONFIG_getColors(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getColors ---->Entry\n");

        try
        {
		char details[200] = {'\0'};
                //Get list of colors supported by front panel indicators
                const device::List<device::FrontPanelIndicator::Color> colorList = device::FrontPanelConfig::getInstance().getColors();
                size_t listSize = colorList.size();
                DEBUG_PRINT(DEBUG_LOG,"Colors size: %d\n", listSize);
		
                for (size_t i = 0; i < listSize; i++)
                {
			strcat(details, colorList.at(i).getName().c_str());
                        if( i < listSize-1 )
                        {
                                strcat(details,",");
                        }
                }
		
                if (listSize != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of colors supported by front panel indicators";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPCONFIG_getColors\n");
                response["details"]= "Exception Caught in FPCONFIG_getColors";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FPCONFIG_getColors  ---->Exit\n");
        return;
}


/***************************************************************************
 *Function name	: FPTEXT_setText
 *Descrption	: This function will set text in the text panel.
 *@param [in]   : req-	text_display: Text to be displayed.
                               text : Name of the Text LED in the Front panel
 *****************************************************************************/ 
void DeviceSettingsAgent::FPTEXT_setText(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_setText ---->Entry\n");
	if(&req["text_display"]==NULL || &req["text"]==NULL)
	{
		return;
	}
	std::string textDisplay=req["text_display"].asCString();
	try
	{
		/*setting text in the Device front panel text display area*/
		device::FrontPanelTextDisplay::getInstance("Text").setText(textDisplay);
		response["result"]= "SUCCESS"; 
		response["details"]="setText SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_setText\n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in FPTEXT_setText";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_setText ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: FPTEXT_setTimeFormat
 *Descrption	: This function will check the functionality of setTimeFormat and
                  currentTimeFormat APIs.
 *@param [in]   : req-	time_format : time format (12Hrs or 24Hrs or string type)
                               text : Name of the Text LED in the Front panel
 *****************************************************************************/ 


void DeviceSettingsAgent::FPTEXT_setTimeFormat(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_setTimeFormat ---->Entry\n");
	if(&req["text"]==NULL || &req["time_format"]==NULL)
	{
		return;
	}
	int timeFormat=req["time_format"].asInt();
	char timeFormatDetails[30];

	try
	{
		device::FrontPanelTextDisplay::getInstance("Text").setTimeFormat(timeFormat);
		int timeFormatOut = device::FrontPanelTextDisplay::getInstance("Text").getCurrentTimeFormat();
		sprintf(timeFormatDetails,"TimeFormat:%d",timeFormatOut);
		response["details"]= timeFormatDetails;
		if (timeFormat == timeFormatOut)
			response["result"]= "SUCCESS";
		else
			response["result"]= "FAILURE";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_setTimeFormat\n");
		response["details"]= "Exception Caught in FPTEXT_setTimeFormat";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nFPTEXT_setTimeFormat ---->Exit\n");
	return;
}


/***************************************************************************
 *Function name	: FPTEXT_setTime
 *Descrption	: This function will set time in the text panel.
 *@param [in]   : req-	time_hrs: Hours.
                       time_mins: Minutes
                           text : Name of the Text LED in the Front panel
 *****************************************************************************/ 
void DeviceSettingsAgent::FPTEXT_setTime(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FPTEXT_setTime ---->Entry\n");
	if(&req["time_hrs"]==NULL || &req["time_mins"]==NULL)
	{
		return;
	}
	int time_hrs=req["time_hrs"].asInt();
	int time_mins=req["time_mins"].asInt();

	try
	{
		/*setting the time in HRS:MINS format*/
		device::FrontPanelTextDisplay::getInstance("Text").setTime(time_hrs,time_mins);
		response["result"]= "SUCCESS"; 
		response["details"]="FrontPanel Text Display setTime success";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FPTEXT_setTime \n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in FPTEXT_setTime";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n FPTEXT_setTime ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: AOP_loopThru
 *Descrption	: This function will enable and check status of LoopThru.
 *@param [in]   : req-	port_name: name of the video port.
                        loop_thru: new loopThru status(true/false)
 *****************************************************************************/ 
void DeviceSettingsAgent::AOP_loopThru(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_loopThru ---->Entry\n");
	if(&req["port_name"]==NULL||&req["loop_thru"]==NULL)
	{
		return;
	}

	std::string portName=req["port_name"].asCString();
	char loopThruDetails1[40] ="LoopThru Set Status :";
	int loop =req["loop_thru"].asInt();
	bool loopthru=false;
	if(loop==0)
	{
		loopthru=false;
	}
	else if(loop==1)
	{
		loopthru=true;
	}
	char *loopThruDetails = (char*)malloc(sizeof(char)*20);
	memset(loopThruDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		/*Enable loop thru*/
		aPort.setLoopThru(loopthru);
		/*checking loop thru status*/
		loopthru=aPort.isLoopThru();
		if(loopthru==true)
		{
			sprintf(loopThruDetails,"%d",1);
			response["result"]= "SUCCESS"; 
		}
		else if(loopthru==false)
		{
			sprintf(loopThruDetails,"%d",0);
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		strcat(loopThruDetails1,loopThruDetails);
		response["details"]=loopThruDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_loopThru\n");
		response["details"]= "Exception Caught in AOP_loopThru";
		response["result"]= "FAILURE";
	}
	free(loopThruDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_loopThru ---->Exit\n");
	return;
}
/***************************************************************************
 *Function name : AOP_mutedStatus
 *Descrption    : This function will enable and check status of mute for
                  a given audio port.
 *@param [in]   : req-  port_name: name of the video port(associated audio port mute 
                                   status will be checked).
                        loop_thru: new loopThru status(true/false)
 *****************************************************************************/

void DeviceSettingsAgent::AOP_mutedStatus(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_mutedStatus ---->Entry\n");
	if(&req["port_name"]==NULL||&req["mute_status"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char muteDetails1[30] ="Mute Set Status :";
	int mute_status =req["mute_status"].asInt();
	bool mute=false;
	if(mute_status==0)
	{
		mute=false;
	}
	else if(mute_status==1)
	{
		mute=true;
	}
	char *muteDetails = (char*)malloc(sizeof(char)*20);
	memset(muteDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		/*Enable mute */
		aPort.setMuted(mute);
		/*checking mute status*/
		mute=aPort.isMuted();
		if(mute==true)
		{
			sprintf(muteDetails,"%d",1);
			response["result"]= "SUCCESS"; 
		}
		else if(mute==false)
		{
			sprintf(muteDetails,"%d",0);
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		strcat(muteDetails1,muteDetails);
		response["details"]=muteDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_mutedStatus\n");
		response["details"]= "Exception Caught in AOP_mutedStatus";
		response["result"]= "FAILURE";
	}
	free(muteDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_mutedStatus ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name : AOPTYPE_getSupportedEncodings
 *Descrption    : This function will list the supported encoding formats for the audio port.
 *@param [in]   : req-  port_name: name of the video port.
 *****************************************************************************/
void DeviceSettingsAgent::AOPTYPE_getSupportedEncodings(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedEncodings ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char *supportedEncodingDetails = (char*)malloc(sizeof(char)*100);
	memset(supportedEncodingDetails,'\0', (sizeof(char)*100));
	char *supportedEncoding = (char*)malloc(sizeof(char)*200);
	memset(supportedEncoding,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedEncoding,"Supported Encodings:");

		//device::List<device::AudioEncoding> encodings  = device::AudioOutputPortType.getInstance().getSupportedEncodings();
		
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		for (size_t i = 0; i < aPort.getSupportedEncodings().size(); i++) 
		{
			strcpy(supportedEncodingDetails,(char*)aPort.getSupportedEncodings().at(i).getName().c_str());
			DEBUG_PRINT(DEBUG_LOG,"\nSupported Encoding:%s\n",supportedEncodingDetails);
			strcat(supportedEncoding,supportedEncodingDetails);
			if(i < aPort.getSupportedEncodings().size()-1)
			{
				strcat(supportedEncoding,",");
			}
		}
		response["result"]= "SUCCESS"; 
		response["details"]=supportedEncoding; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getSupportedEncodings\n");
		response["details"]= "Exception Caught in AOP_getSupportedEncodings";
		response["result"]= "FAILURE";
	}
	free(supportedEncodingDetails);
	free(supportedEncoding);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedEncodings ---->Exit\n");
	return;	
}


/***************************************************************************
 *Function name : AOPTYPE_getSupportedCompressions
 *Descrption    : This function will list the supported compression formats for the audio port.
 *@param [in]   : req-  port_name: name of the video port.
 *****************************************************************************/ 
void DeviceSettingsAgent::AOPTYPE_getSupportedCompressions(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedCompression ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char *supportedCompressionDetails = (char*)malloc(sizeof(char)*100);
	memset(supportedCompressionDetails,'\0', (sizeof(char)*100));
	char *supportedCompression = (char*)malloc(sizeof(char)*200);
	memset(supportedCompression,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedCompression,"Supported Compressions:");
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		for (size_t i = 0; i < aPort.getSupportedCompressions().size(); i++)
		{
			strcpy(supportedCompressionDetails,(char*)aPort.getSupportedCompressions().at(i).getName().c_str());
			strcat(supportedCompression,supportedCompressionDetails);
			if(i < aPort.getSupportedCompressions().size()-1)
			{
				strcat(supportedCompression,",");
			}
		}
		response["details"]=supportedCompression; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getSupportedCompression\n");
		response["details"]= "Exception Caught in AOP_getSupportedCompression";
		response["result"]= "FAILURE";
	}
	free(supportedCompressionDetails);
	free(supportedCompression);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedCompression ---->Exit\n");
	return;
}
/***************************************************************************
 *Function name : AOPTYPE_getSupportedStereoModes
 *Descrption    : This function will list the supported stereo modes for the audio port.
 *@param [in]   : req-  port_name: name of the video port.
 *****************************************************************************/ 
void DeviceSettingsAgent::AOPTYPE_getSupportedStereoModes(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedStereoModes ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char *supportedStereoModesDetails = (char*)malloc(sizeof(char)*100);
	memset(supportedStereoModesDetails,'\0', (sizeof(char)*100));
	char *supportedStereoModes = (char*)malloc(sizeof(char)*200);
	memset(supportedStereoModes,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedStereoModes,"Supported StereoModes:");
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = device::Host::getInstance().getAudioOutputPort(portName);
		for (size_t i = 0; i < aPort.getSupportedStereoModes().size(); i++)
		{
			strcpy(supportedStereoModesDetails,(char*)aPort.getSupportedStereoModes().at(i).getName().c_str());
			strcat(supportedStereoModes,supportedStereoModesDetails);
			if(i < aPort.getSupportedStereoModes().size()-1)
			{
				strcat(supportedStereoModes,",");
			}
		}
		response["details"]=supportedStereoModes; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getSupportedStereoModes\n");
		response["details"]= "Exception Caught in AOP_getSupportedStereoModes";
		response["result"]= "FAILURE";
		return;
	}
	free(supportedStereoModesDetails);
	free(supportedStereoModes);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedStereoModes ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: HOST_addPowerModeListener
 *Descrption	: This function will add the listener for the power mode change event.
 *****************************************************************************/ 
void DeviceSettingsAgent::HOST_addPowerModeListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addPowerModeListener ---->Entry\n");
	try
	{
		device::Host::getInstance().addPowerModeListener(&power_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_addPowerModeListener\n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in HOST_addPowerModeListener";
		return;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addPowerModeListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]="HOST_addPowerModeListener - SUCCESS";
	return;
}
/***************************************************************************
 *Function name	: HOST_removePowerModeListener
 *Descrption	: This function will remove the listener for the power mode change event.
 *****************************************************************************/ 
void DeviceSettingsAgent::HOST_removePowerModeListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removePowerModeListener ---->Entry\n");
	try
	{
		device::Host::getInstance().removePowerModeChangeListener(&power_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_removePowerModeListener\n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in HOST_removePowerModeListener";
		return;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removePowerModeListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]="HOST_removePowerModeListener - SUCCESS";
	return;
}

/***************************************************************************
 *Function name	: VOP_isDisplayConnected
 *Descrption	: This function will check for display connection status for the given 
                  video port.
 *parameter [in]: req-	display_status - new status of display connection.(true/false)
 *****************************************************************************/ 

void DeviceSettingsAgent::VOP_isDisplayConnected(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isDisplayConnected ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	/*getting instance for video ports*/
	char displayDetails1[40] ="DisplayConnection Status :";
	bool display_connect=false;
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*checking DisplayConnection status*/
		display_connect=vPort.isDisplayConnected();
		if(display_connect==true)
		{
			strcat(displayDetails1,"TRUE");
			response["result"]= "SUCCESS"; 
		}
		else if(display_connect==false)
		{
			strcat(displayDetails1,"FALSE");
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		response["details"]=displayDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_isDisplayConnected\n");
		response["details"]= "Exception Caught in VOP_isDisplayConnected";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isDisplayConnected ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: HOST_addDisplayConnectionListener
 *Descrption	: This function will add the listener for the display connection
 *****************************************************************************/ 
void DeviceSettingsAgent::HOST_addDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addDisplayConnectionListener ---->Entry\n");
	try
	{
		device::Host::getInstance().addDisplayConnectionListener(&display_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_addDisplayConnectionListener \n");
		response["result"]= "FAILURE";
		response["details"]= "Exception Caught in HOST_addDisplayConnectionListener";
		return;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addDisplayConnectionListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]= "HOST_addDisplayConnectionListener - SUCCESS";
	return;
}
/***************************************************************************
 *Function name	: HOST_removeDisplayConnectionListener
 *Descrption	: This function will remove the listener for the display connection
 *****************************************************************************/ 
void DeviceSettingsAgent::HOST_removeDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removeDisplayConnectionListener ---->Entry\n");
	try
	{
		device::Host::getInstance().removeDisplayConnectionListener(&display_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_removeDisplayConnectionListener \n");
		response["result"]= "FAILURE";
		response["details"]= "Exception Caught in HOST_removeDisplayConnectionListener";
		return;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removeDisplayConnectionListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]= "HOST_removeDisplayConnectionListener - SUCCESS";
	return;
}


/***************************************************************************
 *Function name	: VOPTYPE_getSupportedResolutions
 *Descrption	: This function will give the supported and current resolution 
                  suppported by the given video port.
 *parameter [in]: req-	port_name - name of the video port.
 *****************************************************************************/ 
void DeviceSettingsAgent::VOPTYPE_getSupportedResolutions(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"VOPTYPE_getSupportedResolutions ---->Entry\n");
	std::string portName=req["port_name"].asCString();
	char *supportedResolutions = (char*)malloc(sizeof(char)*200);
	memset(supportedResolutions,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedResolutions,"Supported Resolutions:");
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		DEBUG_PRINT(DEBUG_LOG,"\nsupportedResolutions::size:%d\n",vPort.getType().getSupportedResolutions().size());
		for (size_t i = 0; i < vPort.getType().getSupportedResolutions().size(); i++)
		{
			DEBUG_PRINT(DEBUG_LOG,"supportedResolutions::%s\n",vPort.getType().getSupportedResolutions().at(i).getName().c_str());
			strcat(supportedResolutions,vPort.getType().getSupportedResolutions().at(i).getName().c_str());
			if(i < vPort.getType().getSupportedResolutions().size()-1)
			{
				strcat(supportedResolutions,",");
			}
		}

                if ( vPort.getType().getSupportedResolutions().size() != 0 )
                {
                        response["details"]=supportedResolutions;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of supported resolutions";
                        response["result"]= "FAILURE";
                }
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_getSupportedResolutions\n");
		response["details"]= "Exception Caught in VOPTYPE_getSupportedResolutions";
		response["result"]= "FAILURE";
	}
	free(supportedResolutions);
	DEBUG_PRINT(DEBUG_TRACE,"VOPTYPE_getSupportedResolutions ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: VOPTYPE_isHDCPSupported
 *Descrption	: This function will check if HDCP is supported for the given port.
 *parameter [in]: req-	port_name: id of the video port.
 *****************************************************************************/ 
void DeviceSettingsAgent::VOPTYPE_isHDCPSupported(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_isHDCPSupported ---->Entry\n");
	std::string portName=req["port_name"].asCString();

	try
	{
		/*getting instance for video ports*/
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*checking HDCP support*/
		bool HDCPEnable = vPort.getType().isHDCPSupported();
		DEBUG_PRINT(DEBUG_LOG,"\nIs HDCP Supported: %d\n", vPort.getType().isHDCPSupported());
		if(true == HDCPEnable)
		{
			response["result"]= "SUCCESS";
			response["details"]= "HDCP Support: TRUE";
		}
		else
		{
			response["result"]= "SUCCESS";
			response["details"]= "HDCP Support: FALSE";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_isHDCPSupported\n");
		response["details"]= "Exception Caught in VOPTYPE_isHDCPSupported";
		response["result"]= "FAILURE";
	}

	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_isHDCPSupported ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name : VOPTYPE_enableHDCP
 *Descrption    : This function enables HDCP for HDMI.
 *parameter [in]: protectContent
 *                hdcpKey
 *                keySize
 *                portName (hardcoded to type HDMI in RDK)
 *****************************************************************************/
void DeviceSettingsAgent::VOPTYPE_enableHDCP(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_enableHDCP ---->Entry\n");

        //std::string portName=req["port_name"].asCString();
        bool protectContent = req["protectContent"].asInt();
        string key = req["hdcpKey"].asCString();
        int keySize = req["keySize"].asInt();
        bool useMfrKey = req["useMfrKey"].asInt();
        char *hdcpKey = 0;

        try
        {
                if (useMfrKey)
                {
                        //Check if mfrMgrMain process in running
                        bool running = checkRunningProcess(MFRMGR);
                        if ( !running )
                        {
                                DEBUG_PRINT(DEBUG_TRACE, "%s process is not running\n",MFRMGR);
                                response["result"] = "FAILURE";
                                response["details"] = "mfrMgrMain process not running to get Mfr HDCP Key";
                                return;
                        }

                        int IsMfrDataNull = false;
                        int retry_count = 0;
                        protectContent = true;
                        IARM_Bus_MFRLib_GetSerializedData_Param_t param_, *param = &param_;

                        do
                        {
                                IsMfrDataNull = false;
                                /* Initialize the struct */
                                memset(param, 0, sizeof(*param));
                                /* Get Key */
                                param->type = mfrSERIALIZED_TYPE_HDMIHDCP;
                                param->bufLen = MAX_SERIALIZED_BUF;

                                int ret = IARM_Bus_Call(IARM_BUS_MFRLIB_NAME,IARM_BUS_MFRLIB_API_GetSerializedData,
                                          (void *)param, sizeof(IARM_Bus_MFRLib_GetSerializedData_Param_t));

                                if(ret != IARM_RESULT_SUCCESS)
                                {
                                        DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_Call failed for %s: error code:%d\n","IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP",ret);
                                }
                                else
                                {
                                        DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_Call success for %s\n", "IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP");
                                        keySize = param->bufLen;
                                        hdcpKey = param->buffer;

                                        if ((hdcpKey[0] == 0) && (hdcpKey[1] == 0) && (hdcpKey[2] == 0) &&
                                            (hdcpKey[3] == 0) && (hdcpKey[4] == 0) && (hdcpKey[5] == 0))
                                        {
                                                DEBUG_PRINT(DEBUG_TRACE,"Received [%d] bytes from %s\n", param->bufLen,"IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP");
                                                IsMfrDataNull = true;;
                                        }
                                        else
                                        {
                                                DEBUG_PRINT(DEBUG_TRACE,"Invalid MFR Data !! Wait for MFR data to be ready..Retry after 10 sec\n");
                                                sleep(10);                                          
                                        }
                                }

                                retry_count ++;

                        } while((false == IsMfrDataNull) && (retry_count < 6));

                        if (false == IsMfrDataNull)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to get MfrData for enabling HDCP\n");
                                response["result"] = "FAILED";
                                response["details"] = "IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP returned NON-NULL value";
                        }
                        else
                        {
                                /*keysize willbe always NULL for mfrSERIALIZED_TYPE_HDMIHDCP - Refer:PACXG1V3-5823, DELIA-22245 */
                                response["result"] = "SUCCESS";
                                response["details"] = "IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP returned NULL as expected";
                        }
                }
                else
                {
                        hdcpKey = &key[0];
                        DEBUG_PRINT(DEBUG_TRACE,"protectContent:%d hdcpKeyAddr:%p hdcpKey:%s keySize:%d\n", protectContent,hdcpKey,hdcpKey,keySize);
                        /* Enable HDCP */
                        device::VideoOutputPortType::getInstance(device::VideoOutputPortType::kHDMI).enabledHDCP(protectContent,hdcpKey,keySize);
                        response["result"] = "SUCCESS";
                        response["details"] = "Enable HDCP done";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_enableHDCP\n");
                response["details"]= "Exception Caught in VOPTYPE_enableHDCP";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_enableHDCP ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VOPTYPE_getPorts(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_getPorts ---->Entry\n");

        try
        {
                char details[256] = {'\0'};

		//GetPorts for all supported PortTypes
		device::VideoOutputPortConfig & vConfig = device::VideoOutputPortConfig::getInstance();
                device::List<device::VideoOutputPortType> vPortTypes = vConfig.getSupportedTypes();
                for (size_t i = 0; i < vPortTypes.size(); i++)
		{
			strcat(details,"Type:");
			strcat(details,vPortTypes.at(i).getName().c_str());
			strcat(details," Ports:");
			DEBUG_PRINT(DEBUG_LOG,"PortType:%s Ports Size:%d", vPortTypes.at(i).getName().c_str(), vPortTypes.at(i).getPorts().size());
                	for (size_t j = 0; j < vPortTypes.at(i).getPorts().size(); j++)
			{
				DEBUG_PRINT(DEBUG_LOG,"PortName:%s ", vPortTypes.at(i).getPorts().at(j).getName().c_str());
				strcat(details,vPortTypes.at(i).getPorts().at(j).getName().c_str());
                        	if( j < vPortTypes.at(i).getPorts().size()-1 )
                        	{
                                	strcat(details,",");
                        	}
                        }

                        if( i < vPortTypes.size()-1 )
                        {
                                strcat(details,",");
                        }
                }

                if (vPortTypes.size() != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of supported video output ports";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_getPorts\n");
                response["details"]= "Exception Caught in VOPTYPE_getPorts";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_getPorts ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VOPTYPE_setRestrictedResolution(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPTYPE_setRestrictedResolution ---->Entry\n");

        try
        {
                char details[50] = {'\0'};
		std::string portType=req["port_name"].asCString();
		int iResolution=req["resolution"].asInt();

                device::VideoOutputPortType::getInstance(portType).setRestrictedResolution(iResolution);
		int oResolution = device::VideoOutputPortType::getInstance(portType).getRestrictedResolution();
		sprintf(details,"SETVALUE:%d GETVALUE:%d",iResolution,oResolution);
                DEBUG_PRINT(DEBUG_LOG,"RestrictedResolution %s\n", details);
		response["details"]=details;
                if (iResolution == oResolution)
                {
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_setRestrictedResolution\n");
                response["details"]= "Exception Caught in VOPTYPE_setRestrictedResolution";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPTYPE_setRestrictedResolution ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOPTYPE_getRestrictedResolution(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPTYPE_getRestrictedResolution ---->Entry\n");

        try
        {
                char details[50] = {'\0'};
                std::string portType=req["port_name"].asCString();

                int resolution = device::VideoOutputPortType::getInstance(portType).getRestrictedResolution();
                sprintf(details,"%d",resolution);
                DEBUG_PRINT(DEBUG_LOG,"PortType: %s RestrictedResolution: %s\n", portType.c_str(), details);
                response["details"]=details;
		response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in VOPTYPE_getRestrictedResolution\n");
                response["details"]= "Exception Caught in VOPTYPE_getRestrictedResolution";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPTYPE_getRestrictedResolution ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOPCONFIG_getPixelResolution(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPixelResolution ---->Entry\n");

        try
        {
		char details[50] = {'\0'};
		//Get PixelResolution for current resolution on given video output port
       		std::string portName=req["port_name"].asCString();
		std::string pixel = device::Host::getInstance().getVideoOutputPort(portName).getResolution().getPixelResolution().toString();
		sprintf(details,"%s",pixel.c_str());
		DEBUG_PRINT(DEBUG_LOG,"PortName:%s PixelResolution:%s\n", portName.c_str(), details);

                response["details"]= details;
                response["result"]= "SUCCESS";
		
		/*
                //Get PixelResolution for given resolution value
                if(&req["resolution"]!=NULL)
                {
                        std::string resolutionName=req["resolution"].asCString();
                        std::string pixel = device::VideoResolution::getInstance(resolutionName).getPixelResolution().toString();
                        DEBUG_PRINT(DEBUG_LOG,"Resolution: %s PixelResolution: %s\n", resolutionName.c_str(),pixel.c_str());
                }
		*/
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPCONFIG_getPixelResolution\n");
                response["details"]= "Exception Caught in VOPCONFIG_getPixelResolution";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPixelResolution  ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOPCONFIG_getSSMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getSSMode ---->Entry\n");

        try
        {
                char details[20] = {'\0'};
                int id = req["ss_id"].asInt();
                device::StereoScopicMode mode = device::VideoOutputPortConfig::getInstance().getSSMode(id);
		sprintf(details,"%s",mode.getName().c_str());
                DEBUG_PRINT(DEBUG_LOG,"ss_id: %d SSMode Id:%d\n", id, mode.getId());
		response["details"]=details;
                if (mode.getId() == id)
                {
                        response["result"]="SUCCESS";
                }
                else
                {
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VOPCONFIG_getSSMode\n");
                response["details"]= "Exception Caught in VOPCONFIG_getSSMode";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getSSMode ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VOPCONFIG_getVideoResolution(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getVideoResolution ---->Entry\n");

        try
        {
                char details[50] = {'\0'};
                //Get VideoResolution on given video output port
                int portId=req["port_id"].asInt();
		std::string resolution = device::VideoOutputPortConfig::getInstance().getVideoResolution(portId).toString();
                sprintf(details,"%s",resolution.c_str());
                DEBUG_PRINT(DEBUG_LOG,"Port Id:%d VideoResolution:%s\n", portId,resolution.c_str());

		device::VideoResolution vResolution = device::VideoResolution::getInstance(portId);
                DEBUG_PRINT(DEBUG_LOG,"VideoResolution: %s\n", vResolution.toString().c_str());
		if (vResolution.toString() == resolution)
		{
                	response["details"]=details;
                	response["result"]= "SUCCESS";
		}
		else
		{
			response["details"]="Failed to get VideoResolution";
			response["result"]= "FAILURE";
		}
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VOPCONFIG_getVideoResolution\n");
                response["details"]= "Exception Caught in VOPCONFIG_getVideoResolution";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getVideoResolution ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VOPCONFIG_getFrameRate(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getFrameRate ---->Entry\n");

        try
        {
                char details[50] = {'\0'};
                //Get FrameRate for current resolution on given video output port
                std::string portName=req["port_name"].asCString();
                std::string framerate = device::Host::getInstance().getVideoOutputPort(portName).getResolution().getFrameRate().toString();
                sprintf(details,"%s",framerate.c_str());
                DEBUG_PRINT(DEBUG_LOG,"PortName:%s Framerate: %s\n", portName.c_str(), details);

                response["details"]=details;
                response["result"]= "SUCCESS";

		/*
                //Get PixelResolution for given resolution value
                if(&req["resolution"]!=NULL)
                {
                        std::string resolutionName=req["resolution"].asCString();
                        std::string framerate = device::VideoResolution::getInstance(resolutionName).getFrameRate().toString();
                        DEBUG_PRINT(DEBUG_LOG,"Resolution: %s FrameRate: %s\n", resolutionName.c_str(),framerate.c_str());
                }
		*/
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VOPCONFIG_getFrameRate\n");
                response["details"]= "Exception Caught in VOPCONFIG_getFrameRate";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getFrameRate ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOPCONFIG_getPortType(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPortType ---->Entry\n");

        try
        {
                char details[50] = {'\0'};
                int portId = req["port_id"].asInt();

                //Get VideoOutputPortType for specified port id
                device::VideoOutputPortType type = device::VideoOutputPortConfig::getInstance().getPortType(portId);
		sprintf(details,"%s",type.getName().c_str());
                DEBUG_PRINT(DEBUG_TRACE,"Port Id: %d Port Name: %s\r\n", type.getId(), type.getName().c_str());
                if (portId == type.getId())
                {
                        response["details"] = details;
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port video type from video port Id";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VOPCONFIG_getPortType\n");
                response["details"]= "Exception Caught in VOPCONFIG_getPortType";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPortType ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOPCONFIG_getPortFromName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPortFromName ---->Entry\n");

        try
        {
                std::string portName=req["port_name"].asCString();
                //Get VideoOutputPort instance for specified port name
                device::VideoOutputPort vPort = device::VideoOutputPortConfig::getInstance().getPort(portName);
                if ( portName == vPort.getName() )
                {
                        response["details"] = "Successfully fetched Video port instance from Video port name";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port Video instance from Video port name";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VOPCONFIG_getPortFromName\n");
                response["details"]= "Exception Caught in VOPCONFIG_getPortFromName";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPortFromName ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VOPCONFIG_getPortFromId(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPortFromId ---->Entry\n");

        try
        {
                int portId = req["port_id"].asInt();
                //Convert the Video port id to the corresponding port object
                device::VideoOutputPort vPort = device::VideoOutputPortConfig::getInstance().getPort(portId);
                DEBUG_PRINT(DEBUG_TRACE,"Port Id: %d Port Name: %s\r\n", portId, vPort.getName().c_str());
                if (portId == vPort.getId())
                {
                        response["details"] = "Successfully fetched video port instance from video port Id";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port video instance from video port Id";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VOPCONFIG_getPortFromId\n");
                response["details"]= "Exception Caught in VOPCONFIG_getPortFromId";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getPortFromId ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOPCONFIG_getSupportedTypes(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getSupportedTypes ---->Entry\n");

        try
        {
                char details[256] = {'\0'};
                device::List<device::VideoOutputPortType> vPortTypes = device::VideoOutputPortConfig::getInstance().getSupportedTypes();
		DEBUG_PRINT(DEBUG_LOG,"VideoOutputPort SupportedTypes Size: %d\n", vPortTypes.size());
                for (size_t i = 0; i < vPortTypes.size(); i++)
                {
                        strcat(details, vPortTypes.at(i).getName().c_str());
                        if( i < vPortTypes.size()-1 )
                        {
                        	strcat(details,",");
                        }
                }

                if (vPortTypes.size() != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of supported types for video output port";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VOPCONFIG_getSupportedTypes\n");
                response["details"]= "Exception Caught in VOPCONFIG_getSupportedTypes";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOPCONFIG_getSupportedTypes ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name : VOP_getHDCPStatus
 *Descrption    : This function gets the status of HDCP authentication.
 *parameter [in]: portName
 *****************************************************************************/
void DeviceSettingsAgent::VOP_getHDCPStatus(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getHDCPStatus ---->Entry\n");
        std::string portName=req["port_name"].asCString();

        try
        {
                char details[30] = {'\0'};
                // getting instance for video port
                device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
                // checking HDCP status
                int hdcpStatus = vPort.getHDCPStatus();
                DEBUG_PRINT(DEBUG_ERROR,"PortName: %s hdcpStatus: %d\n", portName.c_str(), hdcpStatus);
                // Verify the status value
                if ((hdcpStatus < dsHDCP_STATUS_UNPOWERED) || (hdcpStatus >= dsHDCP_STATUS_MAX))
                {
                    response["result"] = "FAILURE";
                    sprintf(details,"InvalidStatus(%d)",hdcpStatus);
                }
                else
                {
                    response["result"] = "SUCCESS";
                    switch(hdcpStatus)
                    {
                        case dsHDCP_STATUS_UNPOWERED:
                            sprintf(details,"Unpowered(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_UNAUTHENTICATED:
                            sprintf(details,"Unauthenticated(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_AUTHENTICATED:
                            sprintf(details,"Authenticated(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_AUTHENTICATIONFAILURE:
                            sprintf(details,"AuthenticationFailure(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_INPROGRESS:
                            sprintf(details,"InProgress(%d)",hdcpStatus);
                    }
                }
                response["details"] = details;
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getHDCPStatus\n");
                response["details"]= "Exception Caught in VOP_getHDCPStatus";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getHDCPStatus ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name	: VOPTYPE_isDynamicResolutionSupported
 *Descrption	: This function will check for the DynamicResolution support for
                  the given port.
 *parameter [in]: req-	port_name: name of the video port.
 *****************************************************************************/ 
void DeviceSettingsAgent::VOPTYPE_isDynamicResolutionSupported(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n VOPTYPE_isDynamicResolutionSupported ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return;
	}
	std::string portName=req["port_name"].asCString();
	char dynamicResolutionDetails1[40] ="isDynamicResolutionSupported :";
	bool dynamicResolutionSupport=false;
	char *dynamicResolutionSupportDetails = (char*)malloc(sizeof(char)*20);
	memset(dynamicResolutionSupportDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*checking for DynamicResolution supported*/
		dynamicResolutionSupport=vPort.isDynamicResolutionSupported();
		if(dynamicResolutionSupport==true)
		{
			sprintf(dynamicResolutionSupportDetails,"%s","TRUE");
			response["result"]= "SUCCESS"; 
		}
		else if(dynamicResolutionSupport==false)
		{
			sprintf(dynamicResolutionSupportDetails,"%s","FALSE");
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		strcat(dynamicResolutionDetails1,dynamicResolutionSupportDetails);
		response["details"]=dynamicResolutionDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_isDynamicResolutionSupported\n");
		response["details"]= "Exception Caught in VOPTYPE_isDynamicResolutionSupported";
		response["result"]= "FAILURE";
	}
	free(dynamicResolutionSupportDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_isDynamicResolutionSupported ---->Exit\n");
	return;
}


/***************************************************************************
 *Function name : VOP_isContentProtected
 *Descrption    : This function is to check content protect status.
 *parameter [in]: req-  port_name: video port name.
 *****************************************************************************/
void DeviceSettingsAgent::VOP_isContentProtected(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isContentProtected ---->Entry\n");
	std::string portName=req["port_name"].asCString();

	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		bool cpSupport = vPort.isContentProtected();
		DEBUG_PRINT(DEBUG_LOG,"\nIs Content Protected: %d\n",vPort.isContentProtected());
		if(true == cpSupport)
		{
			response["details"]= "Content Protected: TRUE";
			response["result"]= "SUCCESS";
		}
		else
		{
			response["details"]= "Content Protected: FALSE";
			response["result"]= "SUCCESS";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_isContentProtected\n");
		response["details"]= "Exception Caught in VOP_isContentProtected";
		response["result"]= "FAILURE";
	}

	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isContentProtected ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name	: VOP_getAspectRatio
 *Descrption	: This function is to get the AspectRatio of the video port.
 *parameter [in]: req-	port_name: video port name.
 *****************************************************************************/ 
void DeviceSettingsAgent::VOP_getAspectRatio(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getAspectRatio ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return;
	}
	char aspectRatioDetails1[30] ="AspectRatio:";
	char *aspectRatioDetails = (char*)malloc(sizeof(char)*20);
	memset(aspectRatioDetails,'\0', (sizeof(char)*20));
	std::string portName=req["port_name"].asCString();
	char *aspectRatio=(char*)malloc(sizeof(char)*20);
	memset(aspectRatio,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting AspectRatio for a given video ports*/
		strcpy(aspectRatio,(char*)vPort.getDisplay().getAspectRatio().getName().c_str());
		strcpy(aspectRatioDetails,aspectRatio);
		strcat(aspectRatioDetails1,aspectRatioDetails);
		response["details"]=aspectRatioDetails1;
		response["result"]="SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getAspectRatio\n");
		response["details"]= "Exception Caught in VOP_getAspectRatio";
		response["result"]= "FAILURE";
	}
	free(aspectRatioDetails);
	free(aspectRatio);
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getAspectRatio ---->Exit\n");
	return;
}



/***************************************************************************
 *Function name	: VOP_getDisplayDetails
 *Descrption	: This function is to get the list of details about video port.
 *parameter [in]: req-	port_name: video port name.
 *****************************************************************************/ 
void DeviceSettingsAgent::VOP_getDisplayDetails(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getDisplayDetails ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return;
	}
	char *displayDetails1 = (char*)malloc(sizeof(char)*200);
	memset(displayDetails1,'\0', (sizeof(char)*200));
	char *displayDetails = (char*)malloc(sizeof(char)*20);
	memset(displayDetails,'\0', (sizeof(char)*20));
	char *weekDetails =(char*)malloc(sizeof(char)*20);
	memset(weekDetails,'\0', (sizeof(char)*20));
	char *yearDetails =(char*)malloc(sizeof(char)*20);
	memset(yearDetails,'\0', (sizeof(char)*20));
	char *pcodeDetails =(char*)malloc(sizeof(char)*20);
	memset(pcodeDetails,'\0', (sizeof(char)*20));
	char *pnumberDetails =(char*)malloc(sizeof(char)*20);
	memset(pnumberDetails,'\0', (sizeof(char)*20));
	std::string portName=req["port_name"].asCString();
	try
	{
		strcpy(displayDetails1,"Display Details:");
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting list of details for a given video ports*/	
		sprintf(weekDetails,"%d",vPort.getDisplay().getManufacturerWeek());
		strcat(displayDetails1,"ManufacturerWeek:");
		strcat(displayDetails1,weekDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nManufacturer Week:%s\n",weekDetails);
		sprintf(yearDetails,"%d",vPort.getDisplay().getManufacturerYear());
		strcat(displayDetails1,",ManufacturerYear:");
		strcat(displayDetails1,yearDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nManufacturer Year:%s\n",yearDetails);
		sprintf(pcodeDetails,"%x",vPort.getDisplay().getProductCode());
		strcat(displayDetails1,",ProductCode:");
		strcat(displayDetails1,pcodeDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nProductCode:%s\n",pcodeDetails);
		sprintf(pnumberDetails,"%x",vPort.getDisplay().getSerialNumber());
		strcat(displayDetails1,",ProductSerialNumber:");
		strcat(displayDetails1,pnumberDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nProductCode:%s\n",pnumberDetails);
		response["details"]=displayDetails1;
		response["result"]="SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getDisplayDetails\n");
		response["details"]= "Exception Caught in VOP_getDisplayDetails";
		response["result"]= "FAILURE";
	}
	free(displayDetails);
	free(displayDetails1);
	free(weekDetails);
	free(yearDetails);
	free(pcodeDetails);
	free(pnumberDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getDisplayDetails ---->Exit\n");
	return;
}

/***************************************************************************
 *Function name : VOP_setEnable
 *Descrption    : This function enables or disables the specified video port.
 *parameter [in]: port_name: video port name
		  enable: true to enable, false to disable
 *****************************************************************************/
void DeviceSettingsAgent::VOP_setEnable(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOP_setEnable  ---->Entry\n");
        char details[30] = {'\0'};
        std::string portName=req["port_name"].asCString();
        bool enable = req["enable"].asInt();

        try
        {       /*getting video port instance*/
                device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
                if (true == enable)
		{
                    /*setting VOP to enable*/
                    DEBUG_PRINT(DEBUG_LOG,"\nCalling VideoOutputPort enable\n");
		    vPort.enable();
                }
		else
		{
		    /*setting VOP to disable*/
		    DEBUG_PRINT(DEBUG_LOG,"\nCalling VideoOutputPort disable\n");
		    vPort.disable();
		}

		if (vPort.isEnabled() == enable)
		{
		    response["result"]="SUCCESS";
		}
		else
		{
		    response["result"]="FAILURE";
		}
		sprintf(details,"Port enable status:%d", vPort.isEnabled());
		response["details"]=details;
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in setEnable\n");
                response["details"]= "Exception Caught in setEnable";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"VOP_setEnable ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VOP_isActive(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOP_isActive  ---->Entry\n");

        try
        {
		char details[30] = {'\0'};
		std::string portName=req["port_name"].asCString();

		bool active = device::VideoOutputPort::getInstance(portName).isActive();
		sprintf(details,"%d",active);
		DEBUG_PRINT(DEBUG_LOG,"Active - [%s]\r\n", active? "Yes" : "No");
		response["details"]=details;
		response["result"]="SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_isActive\n");
                response["details"]= "Exception Caught in VOP_isActive";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"VOP_isActive ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOP_setDisplayConnected(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOP_setDisplayConnected  ---->Entry\n");

        try
        {
                char details[30] = {'\0'};
                std::string portName=req["port_name"].asCString();
		bool connected = req["connected"].asInt();

                device::VideoOutputPort::getInstance(portName).setDisplayConnected(connected);
		sprintf(details,"SetDisplayConnected to %d",connected);
                response["details"]=details;
                response["result"]="SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_setDisplayConnected\n");
                response["details"]= "Exception Caught in VOP_setDisplayConnected";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"VOP_setDisplayConnected ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VOP_hasSurround(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOP_hasSurround ---->Entry\n");

        try
        {
                char details[30] = {'\0'};
                std::string portName=req["port_name"].asCString();

                bool surround = device::VideoOutputPort::getInstance(portName).getDisplay().hasSurround();
                sprintf(details,"%d",surround);
                DEBUG_PRINT(DEBUG_LOG,"hasSurround - [%s]\r\n", surround? "Yes" : "No");
                response["details"]=details;
                response["result"]="SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_hasSurround\n");
                response["details"]= "Exception Caught in VOP_hasSurround";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"VOP_hasSurround ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOP_getEDIDBytes(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOP_getEDIDBytes ---->Entry\n");

        try
        {
                std::string portName=req["port_name"].asCString();

                std::vector<unsigned char> bytes;
		device::VideoOutputPort::getInstance(portName).getDisplay().getEDIDBytes(bytes);
                DEBUG_PRINT(DEBUG_TRACE,"Display [%s] has %d bytes EDID\r\n", portName.c_str(), bytes.size());

                /* Dump the bytes */
                for (size_t i = 0; i < bytes.size(); i++)
                {
                        if (i % 16 == 0) {
                                DEBUG_PRINT(DEBUG_TRACE,"\r\n");
                        }
                        if (i % 128 == 0) {
                                DEBUG_PRINT(DEBUG_TRACE,"\r\n");
                        }
                        DEBUG_PRINT(DEBUG_TRACE,"%02X ", bytes[i]);
                }

                DEBUG_PRINT(DEBUG_TRACE,"\r\n");
                if (bytes.size() >= 128)
                {
                        unsigned char sum = 0;
                        for (int i = 0; i < 128; i++)
                        {
                                sum += bytes[i];
                        }

                        if (sum != 0) {
                                response["details"] = "[EDID Sanity Warning] : Checksum is invalid";
                                response["result"] = "FAILURE";
                        }
                        else {
                                response["details"] = "EDID Checksum is valid";
                                response["result"] = "SUCCESS";
                        }
                }
                else
                {
                        response["details"] = "EDID value less than 128 bytes";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getEDIDBytes\n");
                response["details"]= "Exception Caught in VOP_getEDIDBytes";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"VOP_getEDIDBytes ---->Exit\n");
        return;
}

void DeviceSettingsAgent::VOP_getDefaultResolution(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOP_getDefaultResolution ---->Entry\n");

        try
        {
		char details[50]={'\0'};
		std::string portName=req["port_name"].asCString();
		device::VideoResolution resolution = device::VideoOutputPort::getInstance(portName).getDefaultResolution();
                sprintf(details,"%s",resolution.getName().c_str());
		DEBUG_PRINT(DEBUG_LOG,"Display [%s] Default Resolution: %s\n", portName.c_str(), resolution.getName().c_str());
                response["details"]= details;
                response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getDefaultResolution\n");
                response["details"]= "Exception Caught in VOP_getDefaultResolution";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VOP_getDefaultResolution ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getCPUTemperature(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getCPUTemperature ---->Entry\n");
        try
        {
                char details[30] = {'\0'};
                float cpuTemp = device::Host::getInstance().getCPUTemperature();
                DEBUG_PRINT(DEBUG_LOG,"Current CPU temperature: %+7.2fC\n", cpuTemp);
                sprintf(details,"%5.2f",cpuTemp);
                response["details"] = details;
                response["result"] = "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getCPUTemperature\n");
                response["details"] = "Exception Caught in HOST_getCPUTemperature";
                response["result"] = "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getCPUTemperature ---->Exit\n");
        return;
}

void DeviceSettingsAgent::HOST_setVersion(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setVersion ---->Entry\n");

        try
        {
		unsigned int versionNo = req["versionNo"].asUInt();
		DEBUG_PRINT(DEBUG_LOG,"Version number to be set: %d\n", versionNo);
		unsigned int version = device::Host::getInstance().getVersion();
                DEBUG_PRINT(DEBUG_LOG,"Current version number: %d\n", version);
                device::Host::getInstance().setVersion(versionNo);
		version = device::Host::getInstance().getVersion();
		DEBUG_PRINT(DEBUG_LOG,"Changed version number: %d\n", version);
                if (version == versionNo)
                {
             		response["details"] = "Version number retrieved is same as value set";
	             	response["result"] = "SUCCESS";
                }
                else
                {
	             	response["details"] = "Version number retrieved is not same as value set";
			response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_setVersion\n");
                response["details"] = "Exception Caught in HOST_setVersion";
                response["result"] = "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setVersion ---->Exit\n");
        return;
}

void DeviceSettingsAgent::HOST_setPreferredSleepMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setPreferredSleepMode ---->Entry\n");

        try
        {
		std::string sleepModeStr = req["sleepMode"].asCString();
		const device::SleepMode &mode= device::SleepMode::getInstance(sleepModeStr);
                int ret = device::Host::getInstance().setPreferredSleepMode(mode);
		DEBUG_PRINT(DEBUG_LOG,"Set PreferredSleepMode returned value: %d\n", ret);
		const device::SleepMode &currMode = device::Host::getInstance().getPreferredSleepMode();
                DEBUG_PRINT(DEBUG_LOG,"Changed PreferredSleepMode: %s\n", currMode.toString().c_str());
                if ( currMode.getId() == mode.getId() )
                {
                        response["details"] = "PreferredSleepMode changed successfully";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "PreferredSleepMode retrieved is not same as value set";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_setPreferredSleepMode\n");
                response["details"] = "Exception Caught in HOST_setPreferredSleepMode";
                response["result"] = "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setPreferredSleepMode ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getPreferredSleepMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getPreferredSleepMode ---->Entry\n");
	char details[30] = {'\0'};

        try
        {
		const device::SleepMode &currMode = device::Host::getInstance().getPreferredSleepMode();
                DEBUG_PRINT(DEBUG_LOG,"Current PreferredSleepMode: %s\n", currMode.toString().c_str());
		if ( (0 <= currMode.getId()) and (currMode.getId() < 3) )
		{
			sprintf(details,"%s",currMode.toString().c_str());
			response["details"] = details;
			response["result"] = "SUCCESS";
		}
		else
		{
                	response["details"] = "PreferredSleepMode value not valid";
                	response["result"] = "FAILURE";
		}
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getPreferredSleepMode\n");
                response["details"] = "Exception Caught in HOST_getPreferredSleepMode";
                response["result"] = "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getPreferredSleepMode ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getAvailableSleepModes(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getAvailableSleepModes ---->Entry\n");
        char details[100] = {'\0'};

        try
        {
                const device::List<device::SleepMode> sleepModes = device::Host::getInstance().getAvailableSleepModes();
                for(size_t i = 0; i < sleepModes.size(); i++)
                {
			strcat(details, sleepModes.at(i).toString().c_str());
                        if( i < sleepModes.size() - 1 )
                        {
                                strcat(details, ",");
                        }
                }

                if (sleepModes.size() != 0)
                {
                        response["details"] = details;
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "No SleepModes available";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getAvailableSleepModes\n");
                response["details"] = "Exception Caught in HOST_getAvailableSleepModes";
                response["result"] = "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getAvailableSleepModes ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getVideoOutputPorts(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getVideoOutputPorts ---->Entry\n");

        try
        {
		char details[128] = {'\0'};
		device::List<device::VideoOutputPort> vPorts = device::Host::getInstance().getVideoOutputPorts();
		DEBUG_PRINT(DEBUG_TRACE, "VideoOutputPort size: %d\r\n", vPorts.size());

    		for (size_t i = 0; i < vPorts.size(); i++)
		{
        		device::VideoOutputPort &vPort = vPorts.at(i);
			/*
        		DEBUG_PRINT(DEBUG_TRACE, "Port Name [%s] Enabled [%s] Active [%s] Connected [%s] Type [%s] Resolution [%s]\r\n",
						vPort.getName().c_str(),
						vPort.isEnabled() ? "Yes" : "No",
						vPort.isActive() ? "Yes" : "No",
						vPort.isDisplayConnected() ? "Yes" : "No",
						vPort.getType().getName().c_str(),
						vPort.getResolution().getName().c_str());
			*/
			strcat(details, vPort.getName().c_str());
                        if( i < vPorts.size() - 1 )
                        {
                                strcat(details, ",");
                        }

        	}

		if (vPorts.size() != 0)
		{
                	response["details"] = details;
                	response["result"] = "SUCCESS";
		}
		else
		{
			response["details"] = "No VideoOutputPorts";
			response["result"] = "FAILURE";
		}
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getVideoOutputPorts\n");
                response["details"] = "Exception Caught in HOST_getVideoOutputPorts";
                response["result"] = "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getVideoOutputPorts ---->Exit\n");
        return;
}

void DeviceSettingsAgent::HOST_getAudioOutputPorts(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getAudioOutputPorts ---->Entry\n");
        char details[128] = {'\0'};

        try
        {
		device::List<device::AudioOutputPort> aPorts = device::Host::getInstance().getAudioOutputPorts();
                for (size_t i = 0; i < aPorts.size(); i++)
                {
			device::AudioOutputPort &aPort = aPorts.at(i);

                        DEBUG_PRINT(DEBUG_TRACE, "Port Name [%s] Encoding [%s] StereoMode [%s] Gain [%f] DB [%f]\r\n",
                                                aPort.getName().c_str(),
						aPort.getEncoding().getName().c_str(),
						aPort.getStereoMode().getName().c_str(),
						aPort.getGain(),
						aPort.getDB());

                        strcat(details, aPort.getName().c_str());
                        if( i < aPorts.size() - 1 )
                        {
                                strcat(details, ",");
                        }
                }

                if (aPorts.size() != 0)
                {
                        response["details"] = details;
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "No AudioOutputPorts available";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getAudioOutputPorts\n");
                response["details"] = "Exception Caught in HOST_getAudioOutputPorts";
                response["result"] = "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getAudioOutputPorts ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getVideoDevices(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getVideoDevices ---->Entry\n");
        char details[100] = {'\0'};

        try
        {
		device::List<device::VideoDevice> vDevices = device::Host::getInstance().getVideoDevices();
		DEBUG_PRINT(DEBUG_LOG,"No of Video Devices: %d\n",vDevices.size());
                for (size_t i = 0; i < vDevices.size(); i++)
                {
                        device::VideoDevice device = vDevices.at(i);
                        DEBUG_PRINT(DEBUG_TRACE, "Device Name [%s] ZoomSettings [%s]\r\n", device.getName().c_str(), device.getDFC().getName().c_str());
                        strcat(details, device.getName().c_str());
                        if( i < vDevices.size() - 1 )
                        {
                                strcat(details, ",");
                        }
                }

                if (vDevices.size() != 0)
                {
                        response["details"] = details;
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "No Video Devices available";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getVideoDevices\n");
                response["details"] = "Exception Caught in HOST_getVideoDevices";
                response["result"] = "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getVideoDevices ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getHostEDID(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getHostEDID ---->Entry\n");

        try
        {
		std::vector<unsigned char> bytes;
		device::Host::getInstance().getHostEDID(bytes);
		DEBUG_PRINT(DEBUG_TRACE,"Host has %d bytes EDID\r\n", bytes.size());
		
            	/* Dump the bytes */
            	for (size_t i = 0; i < bytes.size(); i++)
		{
                	if (i % 16 == 0) {
				DEBUG_PRINT(DEBUG_TRACE,"\r");
                	}
                	if (i % 128 == 0) {
                    		DEBUG_PRINT(DEBUG_TRACE,"\r");
                	}
                	DEBUG_PRINT(DEBUG_TRACE,"%02X ", bytes[i]);
            	}

		DEBUG_PRINT(DEBUG_TRACE,"\r\n");
            	if (bytes.size() >= 128)
		{
                	unsigned char sum = 0;
                	for (int i = 0; i < 128; i++)
			{
                    		sum += bytes[i];
                	}

                	if (sum != 0) {
				response["details"] = "[EDID Sanity Warning] : Checksum is invalid";
				response["result"] = "FAILURE";
                	}
                	else {
				response["details"] = "EDID Checksum is valid";
				response["result"] = "SUCCESS";
                	}
            	}
                else
                {
                        response["details"] = "EDID value less than 128 bytes";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getHostEDID \n");
                response["details"] = "Exception Caught in HOST_getHostEDID";
                response["result"] = "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"HOST_getHostEDID ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getVideoOutputPortFromName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"HOST_getVideoOutputPortFromName ---->Entry\n");

        try
        {

		std::string portName=req["port_name"].asCString();
		//Convert the video port Name to the corresponding port object
                device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		std::string outPortName = vPort.getName();
		if (portName == outPortName)
		{
                	response["details"] = "Successfully fetched video port instance from video port Name";
                	response["result"] = "SUCCESS";
		}
		else
		{
			response["details"] = "Failed to fetch port video instance from video port Name";
			response["result"] = "FAILURE";
		}
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in HOST_getVideoOutputPortFromName\n");
                response["details"]= "Exception Caught in HOST_getVideoOutputPortFromName";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"HOST_getVideoOutputPortFromName ---->Exit\n");
        return;
}

void DeviceSettingsAgent::HOST_getVideoOutputPortFromId(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"HOST_getVideoOutputPortFromId ---->Entry\n");

        try
        {
		int portId = req["port_id"].asInt();
                //Convert the video port id to the corresponding port object
                device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portId);
		DEBUG_PRINT(DEBUG_TRACE,"Port Id: %d Port Name: %s\r\n", portId, vPort.getName().c_str());
                if (portId == vPort.getId())
                {
                        response["details"] = "Successfully fetched video port instance from video port Id";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port video instance from video port Id";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in HOST_getVideoOutputPortFromId\n");
                response["details"]= "Exception Caught in HOST_getVideoOutputPortFromId";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"HOST_getVideoOutputPortFromId ---->Exit\n");
        return;
}

void DeviceSettingsAgent::HOST_getAudioOutputPortFromName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"HOST_getAudioOutputPortFromName ---->Entry\n");

        try
        {
		std::string portName=req["port_name"].asCString();
                //Convert the audio port Name to the corresponding port object
                device::AudioOutputPort aPort = device::Host::getInstance().getAudioOutputPort(portName);
                std::string outPortName = aPort.getName();
                if (portName == outPortName)
                {
                        response["details"] = "Successfully fetched audio port instance from audio port Name";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port audio instance from audio port Name";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in HOST_getAudioOutputPortFromName\n");
                response["details"]= "Exception Caught in HOST_getAudioOutputPortFromName";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"HOST_getAudioOutputPortFromName ---->Exit\n");
        return;
}


void DeviceSettingsAgent::HOST_getAudioOutputPortFromId(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"HOST_getAudioOutputPortFromId ---->Entry\n");

        try
        {
		int portId = req["port_id"].asInt();
                //Convert the audio port id to the corresponding port object
                device::AudioOutputPort aPort = device::Host::getInstance().getAudioOutputPort(portId);
                DEBUG_PRINT(DEBUG_TRACE,"Port Id: %d Port Name: %s\r\n", portId, aPort.getName().c_str());
                if (portId == aPort.getId())
                {
                        response["details"] = "Successfully fetched audio port instance from audio port Id";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port audio instance from audio port Id";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in HOST_getAudioOutputPortFromId\n");
                response["details"]= "Exception Caught in HOST_getAudioOutputPortFromId";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"HOST_getAudioOutputPortFromId ---->Exit\n");
        return;
}


void DeviceSettingsAgent::AOPCONFIG_getPortType(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPortType ---->Entry\n");

        try
        {
		int portId = req["port_id"].asInt();
		char details[50] = {'\0'};
                //Get AudioOutputPortType for specified port id
		device::AudioOutputPortType type = device::AudioOutputPortConfig::getInstance().getPortType(portId);
                sprintf(details,"%s",type.getName().c_str());
                DEBUG_PRINT(DEBUG_TRACE,"Port Id: %d Port Name: %s\r\n", type.getId(), type.getName().c_str());
		if (portId == type.getId())
                {
                        response["details"] = details;
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port audio type from audio port Id";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in AOPCONFIG_getPortType\n");
                response["details"]= "Exception Caught in AOPCONFIG_getPortType";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPortType ---->Exit\n");
        return;
}


void DeviceSettingsAgent::AOPCONFIG_getPortFromName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPortFromName ---->Entry\n");

        try
        {
		std::string portName=req["port_name"].asCString();
                //Get AudioOutputPort instance for specified port name
                device::AudioOutputPort aPort = device::AudioOutputPortConfig::getInstance().getPort(portName);
                if ( portName == aPort.getName() )
                {
                        response["details"] = "Successfully fetched audio port instance from audio port name";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port audio instance from audio port name";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in AOPCONFIG_getPortFromName\n");
                response["details"]= "Exception Caught in AOPCONFIG_getPortFromName";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPortFromName ---->Exit\n");
        return;
}



void DeviceSettingsAgent::AOPCONFIG_getPortFromId(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPortFromId ---->Entry\n");

        try
        {
                int portId = req["port_id"].asInt();
                //Convert the audio port id to the corresponding port object
                device::AudioOutputPort aPort = device::AudioOutputPortConfig::getInstance().getPort(portId);
                DEBUG_PRINT(DEBUG_TRACE,"Port Id: %d Port Name: %s\r\n", portId, aPort.getName().c_str());
                if (portId == aPort.getId())
                {
                        response["details"] = "Successfully fetched audio port instance from audio port Id";
                        response["result"] = "SUCCESS";
                }
                else
                {
                        response["details"] = "Failed to fetch port audio instance from audio port Id";
                        response["result"] = "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in AOPCONFIG_getPortFromId\n");
                response["details"]= "Exception Caught in AOPCONFIG_getPortFromId";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPortFromId ---->Exit\n");
        return;
}

void DeviceSettingsAgent::AOPCONFIG_getPorts(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPorts ---->Entry\n");

        try
        {
                char details[200] = {'\0'};
                device::List<device::AudioOutputPort> aPorts = device::AudioOutputPortConfig::getInstance().getPorts();
                size_t listSize = aPorts.size();
                DEBUG_PRINT(DEBUG_LOG,"AudioOutputPort Supported Ports size: %d\n", listSize);
                for (size_t i = 0; i < listSize; i++)
                {
                        strcat(details, aPorts.at(i).getName().c_str());
                        if( i < listSize-1 )
                        {
                                strcat(details,",");
                        }
                }
                if (listSize != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of supported audio output ports";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in AOPCONFIG_getPorts\n");
                response["details"]= "Exception Caught in AOPCONFIG_getPorts";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getPorts ---->Exit\n");
        return;
}

void DeviceSettingsAgent::AOPCONFIG_getSupportedTypes(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getSupportedTypes ---->Entry\n");

        try
        {
		char details[200] = {'\0'};
		device::List<device::AudioOutputPortType> aTypes = device::AudioOutputPortConfig::getInstance().getSupportedTypes();
                size_t listSize = aTypes.size();
                DEBUG_PRINT(DEBUG_LOG,"AudioOutputPort Supported Types size: %d\n", listSize);
                for (size_t i = 0; i < listSize; i++)
                {
                        strcat(details, aTypes.at(i).getName().c_str());
                        if( i < listSize-1 )
                        {
                                strcat(details,",");
                        }
                }
                if (listSize != 0)
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Failed to get list of supported types for audio output port";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in AOPCONFIG_getSupportedTypes\n");
                response["details"]= "Exception Caught in AOPCONFIG_getSupportedTypes";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_getSupportedTypes ---->Exit\n");
        return;
}


void DeviceSettingsAgent::AOPCONFIG_release(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_release ---->Entry\n");

        try
        {
                char details[200] = {'\0'};
                device::AudioOutputPortConfig::getInstance().release();

		//Verify if API clears the instance of audio encoding, compression, stereo modes and audio port types
		device::List<device::AudioOutputPort> audioPorts = device::AudioOutputPortConfig::getInstance().getPorts();
                device::List<device::AudioOutputPortType> aTypes = device::AudioOutputPortConfig::getInstance().getSupportedTypes();
                device::List<device::AudioOutputPort> aPorts = device::Host::getInstance().getAudioOutputPorts();
                for (size_t i = 0; i < aPorts.size(); i++)
                {
                        device::AudioOutputPort &aPort = aPorts.at(i);
                        DEBUG_PRINT(DEBUG_TRACE, "Port Name [%s] Encoding [%s] StereoMode [%s]\r\n",
                                                aPort.getName().c_str(),
                                                aPort.getEncoding().getName().c_str(),
                                                aPort.getStereoMode().getName().c_str());

                        strcat(details, aPort.getName().c_str());
                        if( i < aPorts.size() - 1 )
                        {
                                strcat(details, ",");
                        }
                }

                if ( (audioPorts.size() != 0) || (aPorts.size() != 0) )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Audio output ports not reset\n");
                }
                if (aTypes.size() != 0)
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Audio output port types not reset\n");
                }

                if ( (aPorts.size() == 0) && (audioPorts.size() == 0) && (aTypes.size() == 0) )
                {
			response["details"]="Audio output ports released successfully";
			response["result"]= "SUCCESS";
                }
		else
		{
			response["details"]=details;
			response["result"]= "FAILURE";
		}
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in AOPCONFIG_release\n");
                response["details"]= "Exception Caught in AOPCONFIG_release";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_release ---->Exit\n");
        return;
}


void DeviceSettingsAgent::AOPCONFIG_load(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_load ---->Entry\n");

        try
        {
                char details[200] = {'\0'};
                device::AudioOutputPortConfig::getInstance().load();

                //Verify if API loads constants first and initialize Audio portTypes, encodings, compressions and stereo modes
                device::List<device::AudioOutputPort> audioPorts = device::AudioOutputPortConfig::getInstance().getPorts();
                if (audioPorts.size() == 0)
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Audio output ports not loaded\n");
                }

                device::List<device::AudioOutputPortType> aTypes = device::AudioOutputPortConfig::getInstance().getSupportedTypes();
                if (aTypes.size() == 0)
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Audio output port types not loaded\n");
                }

                device::List<device::AudioOutputPort> aPorts = device::Host::getInstance().getAudioOutputPorts();
                for (size_t i = 0; i < aPorts.size(); i++)
                {
                        device::AudioOutputPort &aPort = aPorts.at(i);
                        DEBUG_PRINT(DEBUG_TRACE, "Port Name [%s] Encoding [%s] StereoMode [%s]\r\n",
                                                aPort.getName().c_str(),
                                                aPort.getEncoding().getName().c_str(),
                                                aPort.getStereoMode().getName().c_str());

                        strcat(details, aPort.getName().c_str());
                        if( i < aPorts.size() - 1 )
                        {
                                strcat(details, ",");
                        }
                }


                if ( (aPorts.size() != 0) && (audioPorts.size() != 0) && (aTypes.size() != 0) )
                {
                        response["details"]=details;
                        response["result"]= "SUCCESS";
                }
                else
                {
                        response["details"]="Audio output ports not loaded successfully";
                        response["result"]= "FAILURE";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in AOPCONFIG_load\n");
                response["details"]= "Exception Caught in AOPCONFIG_load";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"AOPCONFIG_load ---->Exit\n");
        return;
}


void DeviceSettingsAgent::VR_isInterlaced(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VR_isInterlaced ---->Entry\n");

        try
        {
                char details[2048]={'\0'};
                std::string portName=req["port_name"].asCString();
		//Get video port instance
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
                //Check video resolution of VideoOutputPort is interlaced
                bool isInterlaced = vPort.getResolution().isInterlaced();
		DEBUG_PRINT(DEBUG_LOG,"Port [%s] Current Resolution [%s] isInterlaced [%d]\r\n",portName.c_str(),vPort.getResolution().getName().c_str(),isInterlaced);

		sprintf(details,"Port %s: ", portName.c_str());
		//Check isInterlaced for all the supported resolutions on given video port
		size_t listSize = vPort.getType().getSupportedResolutions().size();
                DEBUG_PRINT(DEBUG_LOG,"PortName:%s SupportedResolutions size:%d\n",portName.c_str(), listSize);
                for (size_t i = 0; i < listSize; i++)
                {
			char interlacedDetails[50]={'\0'};
			sprintf(interlacedDetails,"Resolution:%s isInterlaced:%d",vPort.getType().getSupportedResolutions().at(i).getName().c_str(),
									          vPort.getType().getSupportedResolutions().at(i).isInterlaced());
			DEBUG_PRINT(DEBUG_LOG,"%s\n",interlacedDetails);
                        strcat(details,interlacedDetails);
                        if( i < listSize - 1 )
                        {
                                strcat(details, ",");
                        }
                }
		
                response["details"]= details;
                response["result"]= "SUCCESS";

		/*
		//Check isInterlaced for given resolution value
	        if(&req["resolution"]!=NULL)
        	{
			std::string resolutionName=req["resolution"].asCString();
			bool isResolutionInterlaced = device::VideoResolution::getInstance(resolutionName).isInterlaced();
			DEBUG_PRINT(DEBUG_LOG,"Resolution [%s] isInterlaced [%d]\n",resolutionName.c_str(),isResolutionInterlaced);
		}
		*/
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception Caught in VR_isInterlaced\n");
                response["details"]= "Exception Caught in VR_isInterlaced";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"VR_isInterlaced ---->Exit\n");
        return;
}


/**************************************************************************
 * Function Name: CreateObject
 * Description	: This function will be used to create a new object for the
 *		  class "DeviceSettingsAgent".
 *
 **************************************************************************/

extern "C" DeviceSettingsAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Entry\n");
	return new DeviceSettingsAgent(ptrtcpServer);
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Exit\n");
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will be used to clean the log details. 
 *
 **************************************************************************/

bool DeviceSettingsAgent::cleanup(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Entry\n");
	DEBUG_PRINT(DEBUG_LOG,"\n DeviceSettingsAgent shutting down \n");
	IARM_Result_t retval;
	retval=IARM_Bus_Disconnect();
	if(retval==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Application Disconnected from IARMBUS \n");
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Application failed to Disconnect from IARMBUS \n");
		return TEST_FAILURE;
	}
	IARM_Bus_Term();

	DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Exit\n");
	return TEST_SUCCESS;
}


/**************************************************************************
 * Function Name : DestroyObject
 * Description   : This function will be used to destory the object. 
 *
 **************************************************************************/
extern "C" void DestroyObject(DeviceSettingsAgent *agentobj)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n DestroyObject ---->Entry\n");
	DEBUG_PRINT(DEBUG_LOG,"Destroying DeviceSettings Agent object");
	delete agentobj;
	DEBUG_PRINT(DEBUG_TRACE,"\n DestroyObject ---->Exit\n");
}

