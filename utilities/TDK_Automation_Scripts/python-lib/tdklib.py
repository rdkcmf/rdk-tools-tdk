#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import os
import sys
import json
import time
import tftpy
import socket
import signal
import urllib
import dvrlib
import datetime
import threading
import streamlib
import recordinglib
from sys import exit
from resetAgent import resetAgent
from time import gmtime, strftime
from devicestatus import getStatus
from recorderlib import startRecorderApp
import MySQLdb
import shutil
import logging
import random
import select
import StringIO
from xml.dom.minidom import Document,parseString
import string
from TdkPrimitiveFunction import Primitive_TestCase
from mySQLConfig import *

isDatabase=False 
#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------
class RecordList:
	"""
	Class to fetch the recording details from gateway box

    	Syntax       : OBJ = RecordList (ipaddress, portnumber, path, url, execId, execDevId, execResId, testCaseId, deviceId)
        
        Parameters   : ipaddress - IP address of device
		       portnumber - port number 
		       path - Path to save log files
                       url  - url from test manager
		       execId - Execution Id
		       execDevId - Device Id for that execution
		       execResId - Result Id
		       testCaseId - Test case Id
		       deviceId - Device Id

	"""	

	#------------------------------------------------------------------------------
	# __init__ and __del__ block
	#------------------------------------------------------------------------------
	def __init__(self, ipaddress, portnumber, path, url, execId, execDevId, execResId, testCaseId, deviceId):
		try:
			self.ipaddress = ipaddress
			self.portnumber = portnumber
			self.path = path
			self.url = url
			self.execId = execId
			self.execDevId = execDevId
			self.execResId = execResId
			self.testCaseId = testCaseId
			self.deviceId = deviceId
			self.logpath = ""
			self.numOfRecordings = 0
		except:
			print "#TDK_@error-An Error occured in fetching Recording details"
			sys.stdout.flush()
		else:
			return 

	def __del__(self):
		return

    	#------------------------------------------------------------------------------
    	# Public methods
    	#------------------------------------------------------------------------------

	def rmfAppMod(self):

	# To initiate a recording in the Gateway box using rmfapp

        # Syntax       : OBJ.rmfAppMod()
        #                
        # Parameters   : None
        #                
        # Return Value : 0 on success and 1 on failure

    		obj = TDKScriptingLibrary("rmfapp","2.0");
    		obj.configureTestCase(self.url,self.path,self.execId,self.execDevId,self.execResId,self.ipaddress,self.portnumber,69,8088,self.testCaseId,self.deviceId,"false","false","false",'TdkRmfApp_CreateRecord');

    		#Get the result of connection with test component and STB
    		result =obj.getLoadModuleResult();

    		if "SUCCESS" not in result.upper():
         		obj.setLoadModuleStatus("FAILURE");
         		return 1;

    		obj.setLoadModuleStatus(result);
		print "rmfApp module loading status :%s" %result;	
	
		obj.initiateReboot();

    		#Prmitive test case which initiates recording if no recordings found
    		tdkTestObj = obj.createTestStep('TdkRmfApp_CreateRecording');

    		streamDetails = tdkTestObj.getStreamDetails('01');

    		recordtitle = "test_dvr"
    		recordid = "117712111"
		recordduration = "4"
		ocapid = streamDetails.getOCAPID();

		print recordid
		print recordduration
		print recordtitle
		print ocapid

		tdkTestObj.addParameter("recordId",recordid);
		tdkTestObj.addParameter("recordDuration",recordduration);
		tdkTestObj.addParameter("recordTitle",recordtitle);
		tdkTestObj.addParameter("ocapId",ocapid);

    		expectedresult="SUCCESS"

    		#Execute the test case in STB
    		tdkTestObj.executeTestCase(expectedresult);
		
		print "After execution test tdkRmfApp."
		
		time.sleep(3);	
		
		print "After Sleeping."		
	
    		#Get the result of execution
    		result = tdkTestObj.getResult();

		print "After Checking for result."	
	
    		if expectedresult in result:
         		tdkTestObj.setResultStatus("SUCCESS");
    		else:
         		tdkTestObj.setResultStatus("FAILURE");
         		details=tdkTestObj.getResultDetails();
         		obj.unloadModule("rmfapp");
         		return 1;

    		duration = int(recordduration)
		
		obj.initiateReboot();
    		obj.unloadModule("rmfapp");
    		return 0;

	########## End of Function ##########

	def getRecordList(self):

	# To fetch the list of recordings from a gateway box.

        # Syntax       : OBJ.getRecordList()
        #                
        # Parameters   : None
        #                
        # Return Value : 0 on success and 1 on failure

     		obj = TDKScriptingLibrary("mediaframework","2.0");
    		obj.configureTestCase(self.url,self.path,self.execId,self.execDevId,self.execResId,self.ipaddress,self.portnumber,69,8088,self.testCaseId,self.deviceId,"false","false","false",'RMF_DVR_Get_Recording_List');

     		#Get the result of connection with test component and STB
     		result =obj.getLoadModuleResult();

     		if "SUCCESS" in result.upper():
          		obj.setLoadModuleStatus("SUCCESS");
          		tdkTestObj = obj.createTestStep('RMF_GetDvr_Recording_List');

          		expectedRes = "SUCCESS"

          		#Execute the test case in STB
          		tdkTestObj.executeTestCase(expectedRes );

          		#Get the result of execution
          		result = tdkTestObj.getResult();

          		#Get the log path of the Dvr Record List
          		self.logpath  = tdkTestObj.getLogPath();

          		if "NULL" in self.logpath.upper():
               			tdkTestObj.setResultStatus("FAILURE");
               			details=tdkTestObj.getResultDetails();
		               	obj.unloadModule("mediaframework");
               			return 1;

          		recordingObj = tdkTestObj.getRecordingDetails(self.logpath);

          		self.numOfRecordings = recordingObj.getTotalRecordings();

          		#Set the result status of execution
          		tdkTestObj.setResultStatus("SUCCESS");

          		obj.unloadModule("mediaframework");
     		else:
          		obj.setLoadModuleStatus("FAILURE");
          		return 1

     		return 0

	########## End of Function ##########

	def getList(self):

	# An api to fetch list of recording, if recording doesnot exist, initiate a recording and 
	# fetch that details

        # Syntax       : OBJ.rmfAppMod()
        #                
        # Parameters   : None
        #                
        # Return Value : 0 on success and 1 on failure

        	print "Trying to fetch recording details from gateway box [" + str(self.ipaddress) + "]"

        	retrmfAppMod = 0
        	retgetRecordList = 0
        	#Fetch the recording list.
        	retgetRecordList = self.getRecordList();

        	#If recordDetails file Creation fails, exit without running other scripts
        	if "NULL" not in self.logpath.upper():
                	#check if numOfRecordings is 0, then initiate the recording.
                	if 0 == self.numOfRecordings:
	                        retrmfAppMod = self.rmfAppMod();
				time.sleep(8);
        	                retgetRecordList = self.getRecordList();

        	if ((retrmfAppMod == 0) & (retgetRecordList == 0)):
                	return 0
        	else:
                	return 1

	########## End of Function ##########


########## End of Class  ##########



#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------

class PrimitiveTestCase:
	"""
	Class to hold a TestCase in TDK

    	Syntax       : OBJ = PrimitiveTestCase (name, url, execId, execDeviceId, execResId, ipAddr, realpath, tcpClient, logTransferPort, testcaseId, deviceId)
        
        Parameters   : name - Name of testcase
                       url  - url from test manager
                       execId       - execution id
                       execDeviceId - device id
                       execResId    - result id
                       ipAddr       - IP address of device
                       realpath     - Path to save log files
                       tcpClient    - instance of tcp socket client
                       logTransferPort - Port for transfering log files 
		       testcaseId   - test case Id
		       deviceId     - device Id

    	Description  : This class stores the information about a testcase.
	"""	
    	#------------------------------------------------------------------------------
    	# __init__ and __del__ block
    	#------------------------------------------------------------------------------
	def __init__(self,compName, name, url, execId, execDeviceId, execResId, ipAddr, realPath, tcpClient, logTransferPort, testcaseId, deviceId):
		#print "URL in primitive testcase method: ",url
		try:
			self.url = url
			self.execID = execId
			self.ip = ipAddr
			self.resultId = execResId
			self.execDevId = execDeviceId
			self.testcaseId = testcaseId
			self.deviceId = deviceId
			self.realpath = realPath
			self.tcpClient = tcpClient
			self.testCaseName = name
			self.logTransferPort = logTransferPort
			self.result = ""
			self.streamID = None
			self.resultStr=None
			self.resultDetails=None
			self.resultStatus = None
			self.expectedResult = None
			self.componentName = compName
			temp = self.url + "/primitiveTest/getJson?testName=&idVal=2"
			data = temp.split("&")
			url = data[0] + name + "&" + data[1]
                        print "Given URL: ",url
                        self.jsonMsgValue = urllib.urlopen(url).read()
                        if ("Error" in  self.jsonMsgValue or self.jsonMsgValue == "{}"):
                                print "\n********************\nGiven URL is invalid. Proceeding without UI Configuration...\n********************\n"
                                self.jsonMsgValue = Primitive_TestCase(self.componentName, self.testCaseName)
                                #print "Return from function : " + str(self.jsonMsgValue)
                        self.parentTestCase=None
                        self.TestFnLogDom=None
                        self.executionTime=0
                        self.xmlLogEnabled=True;
                        self.testFnDescription="None"

                except Exception, e:
                        print "#TDK_@error-An Error occured in fetching Primitive Test details", e.message;
                        sys.stdout.flush()
                        print "\n********************\nGiven URL is invalid. Proceeding without UI Configuration...\n********************\n"
                        self.jsonMsgValue = Primitive_TestCase(self.componentName, self.testCaseName)
                        #print "Return from function : " + str(self.jsonMsgValue)


		else:
			return 

	def __del__(self):
		return

    	#------------------------------------------------------------------------------
    	# Public methods
    	#------------------------------------------------------------------------------
	def setParentTestCase(self,parentTestCase):
		self.parentTestCase=parentTestCase
	def setXmlLog(self,functionLogDom,testFnDescription):
		self.TestFnLogDom=functionLogDom
		self.testFnDescription=testFnDescription
		
	def enableXmlLog(self,bEnabled):
		self.xmlLogEnabled=bEnabled 

	def addParameter(self, paramName, paramValue):

	# Updates the JSON Message with new parameter values.

	# Syntax       : OBJ.addParameter(paramName, paramValue)
	# Description  : Checks for the paramName in JSON string 
	#                Replaces the value of paramName with paramValue
	# Parameters   : paramName  - The parameter whose value is to be replaced.
	#                paramValue - New value for the parameter
	# Return Value : None 

		try:
			data = json.loads(self.jsonMsgValue)
			#print data
			if self.xmlLogEnabled==True:	
				paramEl=self.parentTestCase.xmlLogDom.createElement("Parameter")
				addTxtEle(self.parentTestCase.xmlLogDom,paramEl,"name",str(paramName))
				addTxtEle(self.parentTestCase.xmlLogDom,paramEl,"value",str(paramValue))
				self.TestFnLogDom.appendChild(paramEl)

		except:
			print "#TDK_@error-ERROR : Json Message is in Incorrect Format !!!"
			sys.stdout.flush()
			exit()
	
		self.replaceValueInJson(data, paramName, paramValue)
		jsonAscii = json.dumps(data, ensure_ascii = False) 
		self.jsonMsgValue = jsonAscii
		return

	########## End of Function ##########
	
	def replaceValueInJson(self, orgJson, searchKey, replaceValue):

	# Replaces the JSON Message with new values.

	# Description  : Search for the key in JSON string
	#                Replaces the value of corresponding key with new Value
	# Parameters   : orgJson      - Json message
	#                searchKey    - The key whose value to be replaced
	#                replaceValue - value to be replaced
	# Return Value : None

		flag = 0
		for key in orgJson.keys():
		  	if key.strip() == searchKey.strip():
		  		orgJson[key] = replaceValue
				flag = 1
		
		if (flag == 0):
			print "#TDK_@error-ERROR : Parameter (" + searchKey + ") not found in primitive test !!!"
			sys.stdout.flush()
			exit()
	
	    	return

	########## End of Function ##########

	def getUTCTime(self):

	# To get UTC time

	# Syntax       : OBJ.getUTCTime()
	# Description  : Method to return current UTC time
	# Parameters   : Nil
	# Return Value : Current UTC time 
		
		timeStamp = strftime("%m%d%H%M%Y", datetime.datetime.utcnow().timetuple())
		return timeStamp

	########## End of Function ##########

	def executeTestCase(self, expectedResult):

	# Send the JSON Message to Server over TCP

	# Syntax       : OBJ.executeTestCase()
	# Description  : Send the JSON Message to Server over TCP
	#                Receives the result of the execution send by the Server 
	# Parameters   : expectedResult - Expected result for that particular test
	# Return Value : None 

		print "Executing %s...." %self.testCaseName
		sys.stdout.flush()
		self.tcpClient.send(str(self.jsonMsgValue))
		t1 = time.time();
		self.result = self.tcpClient.recv(1024)
		t2 = time.time();
		self.executionTime = t2-t1;
		# TODO check if required		self.executionName=executionName
		self.expectedResult = expectedResult

		self.result = self.result.replace("result","TDK__#@$00_result")
		self.result = self.result.replace("details","TDK__#@$00_details")
		self.result = self.result.replace("log-path","TDK__#@$00_log-path")

		self.result = self.result.replace("performanceDataReading","TDK__#@$00_performanceDataReading")
		self.result = self.result.replace("performanceDataName","TDK__#@$00_performanceDataName")
		self.result = self.result.replace("performanceDataUnit","TDK__#@$00_performanceDataUnit")
		self.result = self.result.replace("performanceDataInfo","TDK__#@$00_performanceDataInfo")

		
		if self.xmlLogEnabled==True:
			addTxtEle(self.parentTestCase.xmlLogDom,self.TestFnLogDom,"ResultStr",''.join([i if ord(i) < 128 else ' ' for i in str(self.result)]))
			addTxtEle(self.parentTestCase.xmlLogDom,self.TestFnLogDom,"ExecutionTime",str(self.executionTime))
		return self.executionTime;

	########## End of Function ##########

	def getResult(self):

	# To get the result

	# Syntax       : OBJ.getResult()
	# Description  : Shows the result SUCCESS/FAILURE
	# Parameters   : None
	# Return Value : Result of the test execution 
    		
		if "Method not found." in self.result:
			print "#TDK_@error-ERROR : Method not registered with Test Agent"
			if self.xmlLogEnabled==True:
				addTxtEle(self.parentTestCase.xmlLogDom,self.TestFnLogDom,"message","#TDK_@error-ERROR : Method not registered with Test Agent")
                        sys.stdout.flush()
                        #exit()
		else:
			message = self.getValueFromJSON("TDK__#@$00_result")
			self.resultStr=message			
			if self.xmlLogEnabled==True:
				addTxtEle(self.parentTestCase.xmlLogDom,self.TestFnLogDom,"Message",str(message))

			return message
		
	########## End of Function ##########

	def setResultStatus(self, status):

	# Set the result status after doing logic in script

	# Syntax       : OBJ.setResultStatus()
	# Description  : Shows the result status(SUCCESS/FAILURE)
	# Parameters   : status of the test 
	# Return Value : None

		try:
			self.resultStatus = status
			if "FAILURE" in status :
				self.parentTestCase.resultStatus=status
			result = self.getResult()
			temp = self.url + "/execution/saveResultDetails?execId=&resultData=&execResult=&expectedResult=&resultStatus=&testCaseName=&execDevice=&"  
			data = temp.split("&")
			url = data[0] + str(self.execID) + "&" + data[1] + result + "&" + data[2] + str(self.resultId) + "&" \
				+ data[3] + str(self.expectedResult) + "&" + data[4] + str(self.resultStatus) + "&" \
				+ data[5] + str(self.testCaseName) + "&" + data[6] + str(self.execDevId)

			#loadstring = urllib.urlopen(url).read()
			if self.xmlLogEnabled==True:
				incidentEle=self.parentTestCase.xmlLogDom.createElement("Incident")			
				incidentEle.setAttribute("type",str(status))
				self.TestFnLogDom.appendChild(incidentEle)
				addTxtEle(self.parentTestCase.xmlLogDom,self.TestFnLogDom,"Result",str(result))

			sys.stdout.flush()
			
		except :
			print "#TDK_@error-ERROR : error:Unable to access url to save result details !!!"
			print "Unexpected error:", sys.exc_info()[0] 
			sys.stdout.flush()
			#exit()
		
		return
		
	########## End of Function ##########
	def logPerformanceData(self,performanceDataName="no_name_given",performanceDataUnit="unit_not_set",performanceDataReading="no_data",performanceDataInfo="no_info"):
		if self.xmlLogEnabled==True:
			if performanceDataName == "no_name_given":
				performanceDataReading = self.getValueFromJSON("TDK__#@$00_performanceDataReading")
				performanceDataName=self.getValueFromJSON("TDK__#@$00_performanceDataName")
				performanceDataUnit=self.getValueFromJSON("TDK__#@$00_performanceDataUnit")
				performanceDataInfo=self.getValueFromJSON("TDK__#@$00_performanceDataInfo")

			performanceDataEle=self.parentTestCase.xmlLogDom.createElement("PerformanceData")
			performanceDataEle.setAttribute("name",str(performanceDataName))
			performanceDataEle.setAttribute("unit",str(performanceDataUnit))
			addTxtEle(self.parentTestCase.xmlLogDom,performanceDataEle,"PerfDataReading",str(performanceDataReading))
			addTxtEle(self.parentTestCase.xmlLogDom,performanceDataEle,"PerfDataInfo",str(performanceDataInfo))
			self.TestFnLogDom.appendChild(performanceDataEle)

	                sys.stdout.flush()
		else:
			print "xmlLogEnabled==False for this function."+self.testCaseName 
			return None
#                self.resultDetails=message
                return performanceDataEle.toxml() 
	
	def getResultDetails(self):
    	
	# Get the Details of result

	# Syntax       : OBJ.getResultDetails()
	# Description  : Shows the details of the result
	# Parameters   : None
	# Return Value : Details of the test execution 
    
		message = self.getValueFromJSON("TDK__#@$00_details")
		sys.stdout.flush()
		self.resultDetails=message
		return message

	########## End of Function ##########

	def getLogPath(self):

	# To get the path to log file

	# Syntax       : OBJ.getLogPath()
	# Description  : Shows the path of log
	# Parameters   : None
	# Return Value : Result path  of the result
 
		message = self.getValueFromJSON("TDK__#@$00_log-path")
		sys.stdout.flush()
		return message

	########## End of Function ##########
   
	def getValueFromJSON(self, key):

	# To get the value corresponding to a key from json response

	# Syntax       : OBJ.getValueFromJSON(key)
	# Description  : Parse the string of corresponding key and fetch the value
	# Parameters   : key to find value
	# Return Value : value of the key

		#print self.result
		if key in self.result:
			resultIndex = self.result.find(key) + len(key+"\":\"")
			message = self.result[resultIndex:]
			message = message[:(message.find("TDK__#@$00_"))]
			message = message.strip("\"}")
			message = message.strip("\",\"")

		else:
			index = key.find("#@$00_") + len("#@$00_")
			key = key[index:]
			print "#TDK_@error-ERROR : Unable to find " + "\"" + key + "\"" + " in response message"
			sys.stdout.flush()
			#exit()

		return message
	
	########## End of Function ##########

        def getClientIPAddress(self, mac):

        # To get the moca ip address for a mac address

        # Syntax       : OBJ.getClientIPAddress(mac)
        # Description  : Send query to TDKagent to get client ipaddress for corresponding mac address
        # Parameters   : mac address
        # Return Value : client moca ip address

                try:
                        message = {'jsonrpc':'2.0','id':'2','method':'getClientMocaIpAddress','MACaddr':str(mac)}
                        query = json.dumps(message)
                        self.tcpClient.send(query)

                except socket.error:
                        print "******************************************************************************************"
                        print " #TDK_@error-Error while Connecting to Server ... "
                        print " Please ensure the Box " + self.IP + " is up and Test Agent is running..."
                        print "******************************************************************************************"
                        sys.stdout.flush()
                        exit()
                except:
                        print "#TDK_@error-ERROR : Unable to connect.. Please check box is up and agent is running.....\n"
			print "Details : "
			logging.exception('')
                        sys.stdout.flush()
                        exit()

                result = self.tcpClient.recv(1048)
                resultIndex = result.find("result") + len("result"+"\":\"")
                message = result[resultIndex:]
                result = message[:(message.find("\""))]

                if((result == "") | ("incomplete" in result)):
                        print "#TDK_@error-ERROR : Given mac address does not have available Moca IP address\n"
                        sys.stdout.flush()
                        exit()

                return result

	########## End of Function ##########
  
	def initiateRecorderApp(self, arg):

	# To start recorder application

	# Syntax       : OBJ.initiateRecorderApp(argument)
	# Description  : start recorder application and redirect the console output back to script
	# Parameters   : argument
	# Return Value : console output of the app

		outdata = startRecorderApp(self.realpath, arg)
		sys.stdout.flush()
		return outdata
	
	########## End of Function ##########
 
	def downloadFile(self, IP, PORT, RemoteFile, LocalFile):
	
	# Download a file

	# Syntax       : OBJ.downloadFile()
	# Description  : To download a file 
	# Parameters   : IP         - IP address of the remote machine where the file resides
	#                PORT       - Port using for download
	#                RemoteFile - Remote file location
	#                LocalFile  - Local file location where the file to be downloaded.
	# Return Value : returns status
            
        	status = 0
        	try:
                	client = tftpy.TftpClient(IP, PORT)
                	client.download(RemoteFile, LocalFile)
                	status = 1
			print "Remote Path from box:",RemoteFile
			print "Local Path:",LocalFile
			sys.stdout.flush()

       		except TypeError:
                	print "Connection Error : Transfer of " + RemoteFile + " Failed.."
			sys.stdout.flush()
       		except IOError:
			print "Remote Path from box:",RemoteFile
                        print "Local Path:",LocalFile
                	print "IO Error : Transfer of " + RemoteFile + " Failed.."
			print "Failed to find destination file path or permission denied"
			sys.stdout.flush()
        	except:
                	print "ERROR : Transfer of " + RemoteFile + " Failed.." 
			sys.stdout.flush()
	       	return status

	########## End of Function ##########

    	def transferLogs(self, sourceLogPath, multiLog):
	
	# For transfering logs using tftp

	# Syntax       : OBJ.transferLogs()
	# Description  : To transfer log files 
	# Parameters   : logpath  - Path of logfile in remote machine
	#                multilog - 'true' for multiple logs,'false' for single log
	# Return Value : none
            
        	ipAddress = self.ip
        	port = self.logTransferPort
		#dir = self.realpath + str(self.execID) previously it was like this
		'''#TODO: Commented below block. Verify if it is OK.  This block was  unnecessarily creating a logpth/executionid folder
		dir = self.realpath + str(self.execID)
		print "Directory path:",dir
		#checking if directory is exists or not if exists then rename the existing one as <execID>old and create new with name <execID>.
		try:
                        os.makedirs(dir)
                except OSError:
                        if os.path.exists(dir):
								try:
									shutil.move(dir, dir+"old")
								except:
									print "\n Error in log Directory path \n"
                        else:
                                print "\n Error in log Directory path \n"
		'''
		#TODO
		destinationLogPath = self.realpath + "logs/" + str(self.execID) + "/" + str(self.execDevId) + "/" + str(self.resultId) + "/" 
		#destinationLogPath = self.realpath +  str(self.execID) + "/" + str(self.execDevId) + "/" 
		timeStamp = strftime("%d%m%y%H%M%S", gmtime())
                if not os.path.exists(destinationLogPath):
                        os.makedirs(destinationLogPath)

	#
	#  If there are multiple logs, logdetails file will be downloaded first. All the application logs
	#  will be downloaded after getting the log path from logdetails file. All the application logs
	#  are saved with application name and timestamp(GMT).
	#

		if (multiLog == "true"):
			summaryFile = destinationLogPath + str(self.execID) + "_" + "TestSummary" + "_" + timeStamp
			self.downloadFile (ipAddress, port, sourceLogPath, summaryFile)
			logDetails = open (summaryFile, "r")
			logDetails.readline()
			line = logDetails.readline()
			while(line != ''):
				time.sleep(1)
				path = line.split(";")[-1]
				path = path.replace('"', '').strip()
				path = path.strip("\n")
				localFileName = path.split("/")[-1]
				localFileName = destinationLogPath + str(self.execID) + "_" + localFileName + "_" + timeStamp
				self.downloadFile(ipAddress, port, path, localFileName)
				line = logDetails.readline()
			logDetails.close()

	#
	#  If there is only single log, that file will be downloaded from the logpath and timestamp(GMT)
	#  will be appended in the filename.
	#

		elif( multiLog == "false"):
			localFileName = sourceLogPath.split("/")[-1]
			localFileName = destinationLogPath + str(self.execID) + "_" + localFileName + "_" + timeStamp
			self.downloadFile(ipAddress, port, sourceLogPath, localFileName)
		return

	########## End of Function ##########

	def getDVRDetails(self, infoFileName):

	# Create an object for DVR details 

	# Syntax      : OBJ.getDVRDetails()
	# Description : Create an object of DVR Details 
	# Parameters  : logFileName - path to file name having the DVR details
	# Return Value: An instance of class DVRDetails
		
		ipAddress = self.ip
		port = self.logTransferPort
		recordedUrlLogPath = infoFileName

		destinationLogPath = self.realpath + "fileStore/" 
		destinationLogPath = destinationLogPath + str(self.execID) + "_RecordedUrlsLog.txt"
		if self.downloadFile(ipAddress, port, recordedUrlLogPath, destinationLogPath) == 0:
                        print "#TDK_@error-ERROR : Unable to fetch recording details !!! "
                	sys.stdout.flush()
			exit()
		else:
    			dvrObj = dvrlib.DVRDetails (destinationLogPath)

		sys.stdout.flush()
		return dvrObj

        ########## End of Function ##########

        def getRecordingDetails(self, infoFileName = "client"):

        # Create an object for Recording details

        # Syntax      : OBJ.getRecordingDetails()
        # Description : Create an object of Recording Details
        # Parameters  : logFileName - path to file name having Recording details
        # Return Value: An instance of class RecordingDetails

                ipAddress = self.ip
                port = self.logTransferPort

		if (infoFileName == "client"):
			returnvalue = 1
			obj = self.getStreamDetails('01')
			gatewayip = obj.getGatewayIp()
			recobj = RecordList(str(gatewayip),8087,self.realpath,self.url,self.execID,self.execDevId, self.resultId, self.testcaseId, self.deviceId)
			returnvalue = recobj.getList()
			if(returnvalue == 0):
				destinationLogPath = self.realpath + "/fileStore/recordDetails.txt"
                        	recordingObj = recordinglib.RecordingDetails (destinationLogPath)
			else:
				print "#TDK_@error-ERROR : Failed to fetch recording details from gateway box ( " + str(gatewayip) + " ) !!! "
				sys.stdout.flush()
                                exit()
	
		else:

                	recordedUrlLogPath = infoFileName

                	destinationLogPath = self.realpath + "/fileStore/"
                	destinationLogPath = destinationLogPath + "recordDetails.txt"
                	if self.downloadFile(ipAddress, port, recordedUrlLogPath, destinationLogPath) == 0:
                	        print "#TDK_@error-ERROR : Unable to fetch recording details !!! "
                		sys.stdout.flush()
				exit()
                	else:
                        	recordingObj = recordinglib.RecordingDetails (destinationLogPath)

                sys.stdout.flush()
                return recordingObj


	########## End of Function ##########

	def getStreamDetails(self, streamId):

	# Create an object for Streaming details 

	# Syntax      : OBJ.getStreamDetails(streamId)
	# Description : Create an object of StreamingDetails 
	# Parameters  : streamId - Id of the stream you want to use
	# Return Value: An instance of StreamingDetails
	
		self.streamID = streamId
		print "self url:",self.url
		url = self.url + "/primitiveTest/getStreamDetails?idVal=" + str(streamId) + "&stbIp=" + self.ip
		try:
			loadstring = urllib.urlopen(url).read()
			testObj = streamlib.StreamingDetails(loadstring)
		except:
			print "#TDK_@error-ERROR : Unable to access url for getting stream details !!!"
			#exit()

		sys.stdout.flush()
		return testObj 

			
	########## End of Function ##########

	
########## End of Class  ##########
		
def addTxtEle(xmlLogDom,parentElement,tagName,contentText):
	child=xmlLogDom.createElement(tagName)
	contentTextNode=xmlLogDom.createTextNode(str(contentText))
	child.appendChild(contentTextNode)
	parentElement.appendChild(child)

#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------

class TDKScriptingLibrary:

	"""
	Class to act as a wrapper for the testcase script in TDK

	Description  : This class configures and gives an instance of a testcase 
	Syntax       : OBJ = TDKScriptingLibrary( componentName, version) 
	Parameters   :  componentName   - Component Name
			version         - RDK version
	"""	

    	#------------------------------------------------------------------------------
    	# __init__ and __del__ block
    	#------------------------------------------------------------------------------	

	def __init__(self, cName, version):
		self.serviceIp = None
		self.servicePort = None
		self.componentName = cName
		self.rdkversion = version
		self.url = None
		self.execID = None
		self.resultId = None
		self.result = None
		self.IP = None
		self.realpath = None
		self.tcpClient = None
		self.resultStatus='SUCCESS'
		self.uiLogData=None
		self.execName=None
		self.xmlLogDom=None
		self.scriptName=None
		self.enabledXmlLogging=False
		self.logpath=None
		self.primitiveTests=[]	
		self.startTime=0;
		self.timeTaken=0
		self.infoDict=None
		return 

	def __del__(self):
		return

    	#------------------------------------------------------------------------------
    	# Public methods
    	#------------------------------------------------------------------------------
	def enableLogging(self,scriptName,logpath,infoDict=None):
		self.scriptName=scriptName				
		self.enabledXmlLogging=True
		self.logpath=logpath
		self.infoDict=infoDict

	def configureTestCase(self, url, path, execId, execDeviceId, execResId, deviceIp, devicePort, logTransferPort,\
				statusPort, testcaseID, deviceId, performanceBenchMarkingEnabled, performanceSystemDiagnosisEnabled, \
				scriptSuiteEnabled, executionName):
	# Configures the testcase for Execution

	# Syntax       : OBJ.configureTestCase(url, path, execId, execDeviceId, execResId, 
	#                                    deviceIp, devicePort, logTransferPort, statusPort, testcaseID, deviceId,
	#				     performanceBenchMarkingEnabled, performanceSystemDiagnosisEnabled, scriptSuiteEnabled,
	#				     executionName)
	# eg           : obj.configureTestCase ('http://192.168.160.248:8080/rdk-test-tool', 
	#                                       '/opt/comcast/software/tomcat/current/webapps/rdk-test-tool/',
	#                                       25, 3333, 29, ip, port, 69, 8088, 55, 66, 'true', 'true', 'true', 'CT_IARMBUS_3');
	# Description  : Obtain the device ip and port number,
	#                Create a TCP connection to the device under Test
	# Parameters   : url           - url to fetch webservice calls
	#                path	       - Path to save the files tranferred from the box
	#                execId        - Execution id
	#                execDeviceId  - Device id for that execution
	#                execResId     - Result id
	#                deviceIp      - Device Ip
	#                devicePort    - Device Port connecting to "agent"
	#                logTransferPort - Port for log transfering using TFTP
	#                statusPort    - Port for status checking
	#		 testcaseID    - TestCaseID
	#                deviceId      - Device Id
	#		 performanceBenchMarkingEnabled - true / false
	#		 performanceSystemDiagnosisEnabled - true / false
	#		 scriptSuiteEnabled - true / false
	# 	         executionName - Test Execution Name
	# Return Value : None 
	# Exceptions   : IOError      - File doesnot exist
	#                socket.error - Error while opening socket
    	
		try:
			
			self.url = url
			self.execID = execId
			self.resultId = execResId
			self.execDevId = execDeviceId
			self.testcaseId = testcaseID
			self.deviceId = deviceId
			self.tcpClient = socket.socket()
			self.IP = deviceIp
			self.portValue = devicePort
			self.realpath = path
			self.performanceBenchMarkingEnabled = performanceBenchMarkingEnabled  
			self.performanceSystemDiagnosisEnabled = performanceSystemDiagnosisEnabled 
			self.scriptSuiteEnabled = scriptSuiteEnabled
			self.startTime=time.time()
			self.realpath = self.realpath + "/"
			
			#print self.portValue
			# Querry Test Manager to get status port and log transfer port
                        url = self.url + "/execution/getClientPort?deviceIP=" + str(self.IP) + "&agentPort=" + str(self.portValue)
			self.xmlLogDom=Document()
			#print url
			testCase=self.xmlLogDom.createElement("TestCase")
			testCase.setAttribute("name",str(self.scriptName))
			if self.infoDict is not None:
				for key in self.infoDict:
					testCase.setAttribute(str(key),str(self.infoDict[key]))

			self.xmlLogDom.appendChild(testCase)
			envEl=self.xmlLogDom.createElement("Environment")
			#self.addTxtEle(envEl,"url",url)
			addTxtEle(self.xmlLogDom,envEl,"execId",execId)
			addTxtEle(self.xmlLogDom,envEl,"execResId",execResId)
			addTxtEle(self.xmlLogDom,envEl,"execDeviceId",execDeviceId)
			addTxtEle(self.xmlLogDom,envEl,"testcaseID",testcaseID)
			addTxtEle(self.xmlLogDom,envEl,"deviceId",deviceId)
			addTxtEle(self.xmlLogDom,envEl,"deviceIp",deviceIp)
			addTxtEle(self.xmlLogDom,envEl,"path",path)
			addTxtEle(self.xmlLogDom,envEl,"executionName",executionName)
			addTxtEle(self.xmlLogDom,envEl,"componentName",self.componentName)
			addTxtEle(self.xmlLogDom,envEl,"rdkversion",self.rdkversion)
			testCase.appendChild(envEl)
			#print self.xmlLogDom.toprettyxml(indent='\t')
			
                        try:
                                loadstring = urllib.urlopen(url).read()
                                if "null" in loadstring:
                                        self.logTransferPort = logTransferPort
                                        self.statusPort = statusPort
                                else:
                                        data = json.loads(loadstring)
                                        self.logTransferPort = int(data["logTransferPort"])
                                        self.statusPort = int(data["statusPort"])
                                        
                                        #print self.logTransferPort

                        except ValueError, details:
                                #print "#TDK_@error-ERROR : Unable to access url for getting device port numbers !!!"
                                print "Initializing Port Values.."
                                #print "Details : ", details
                                self.logTransferPort = logTransferPort
                                self.statusPort = statusPort
                                #sys.stdout.flush()
                                #exit()
                        except:
                                print "#TDK_@error-ERROR : Unable to access url for getting device port numbers !!!\n Setting Device port numbers manually.\n"
				print "Details : "
				#logging.exception('')
                                self.logTransferPort = logTransferPort
                                self.statusPort = statusPort
                                #sys.stdout.flush()
                                #exit()

			# Connecting to device
			self.tcpClient.connect((self.IP, self.portValue))
			self.uiLogData =str(self.uiLogData)+ "<br/> Connected to "+ str(self.IP) +" Box for testing "+ str(self.componentName);
			print "Connected to "+ self.IP +" Box for testing "+ self.componentName
			self.execName = executionName
			print "Test Execution Name is: %s" %self.execName
	
			#For DynamicLoading ....
			#Load the particular shared object  before executing
			#print "Connected to "+ self.IP +" Box for testing "+ self.componentName
       			sys.stdout.flush()         	
	
			final = {'jsonrpc':'2.0','id':'2','method':'LoadModule','param1':self.componentName,'version':self.rdkversion,\
				 'execID':str(self.execID),'deviceID':str(self.deviceId),'testcaseID':str(self.testcaseId),\
				 'execDevID':str(self.execDevId),'resultID':str(self.resultId),\
				 'performanceBenchMarkingEnabled':str(self.performanceBenchMarkingEnabled), \
				 'performanceSystemDiagnosisEnabled': str(self.performanceSystemDiagnosisEnabled) }
			#print "Final: ",final
			query = json.dumps(final)
			#print "*****Query: ",query,"*****"
			self.tcpClient.send(query)
			#print self.tcpClient.send(query)
			
		except socket.error:
			print "******************************************************************************************" 
			print " #TDK_@error-Error while Connecting to Server ... "
			print " Please ensure the Box " + self.IP + " is up and Test Agent is running..."
			print "******************************************************************************************" 
			sys.stdout.flush()
			#exit()
		except IOError:
			print "#TDK_@error-ERROR : Configuration File Not Found!\n"
			sys.stdout.flush()
			#exit()
		except:
			print "#TDK_@error-ERROR : Unable to connect.. Please check box is up and agent is running.....\n"
			print "Details : "
			logging.exception('')
			sys.stdout.flush()
			#exit()
		else:
			print "Connected to Server!\n"
			self.uiLogData = self.uiLogData+"<br/> Connected to Server!";#print "Connected to Server!\n";
			sys.stdout.flush()
			self.result = self.tcpClient.recv(1048)

		return

	########## End of Function ##########

	def getLoadModuleResult(self):

	# Displays the result of Load module

	# Syntax       : OBJ.getLoadModuleResult()
	# Description  : Shows the result of LoadModule
	# Parameters   : None
	# Return Value : Result of the load module
    	
		if self.result:
			resultIndex = self.result.find("result") + len("result\":\"")
			message = self.result[resultIndex:]
			message = message[:(message.find("\""))]
			if "Success" in message:
				self.uiLogData=self.uiLogData+ "<br/> Opensource test module successfully loaded\n"
			else:
				self.uiLogData=self.uiLogData+ "<br/> Failed to load Opensource test module \n"

			return message
		else:
			return "#TDK_@error-Error in socket.. Please check STB is up and agent is running inside it"
			
	########## End of Function ##########

	def setLoadModuleStatus(self, status):

	# Set the status of load module as sccess or failure

	# Syntax       : OBJ.setLoadModuleStatus()
	# Description  : Sets the LoadModule status(SUCCESS/FAILURE)
	# Parameters   : status of the LoadModule
	# Return Value : None

		try:
			sys.stdout.flush()
			if self.result:
				if "details" in self.result:
					resultIndex = self.result.find("details") + len("details\":\"")
					message = self.result[resultIndex:]
					message = message[:(message.find("\""))]
					print "Load Module Details : " + message
					sys.stdout.flush()

			temp = self.url + "/execution/saveLoadModuleStatus?execId=&statusData=&execDevice=&execResult=&"
			data = temp.split("&")
			url = data[0] + str(self.execID) + "&" + data[1] + str(status) + "&" + data[2] + str(self.execDevId) \
			      + "&" + data[3] + str(self.resultId)
			#loadstring = urllib.urlopen(url).read()
			#print "%%%%%Load String:In setLoadModuleStatus%%%%",loadstring
		
		except:
			print "#TDK_@error-ERROR : Unable to access url to save result details !!!"
			print "Unexpected error:", sys.exc_info()[0]
			sys.stdout.flush()
		
		sys.stdout.flush()
		return

        ########## End of Function ##########

	def createTestStep(self, testCaseName,testFnRelevanceNumber="0",testFnDescription="none",bXmlLogEnabledForTestFn=True):

	# Create an object for testcase 

	# Syntax      : OBJ.createTestStep(testCaseName)
	# Description : Create an object of testcase 
	# Parameters  : testCaseName - Name of test case
	# Return Value: An instance of PrimitiveTestCase 
    	
		sys.stdout.flush()
		testObj = PrimitiveTestCase(self.componentName,testCaseName, self.url, self.execID, self.execDevId, self.resultId, self.IP, self.realpath, self.tcpClient, self.logTransferPort, self.testcaseId, self.deviceId)
		testObj.setParentTestCase(self)
		if bXmlLogEnabledForTestFn == True:
			testFnEl=self.xmlLogDom.createElement("TestFunction")
			testFnEl.setAttribute("name",str(testCaseName))
			testFnEl.setAttribute("description",str(testFnDescription))
			testFnEl.setAttribute("relevance",str(testFnRelevanceNumber))
			self.xmlLogDom.getElementsByTagName("TestCase")[0].appendChild(testFnEl)
			testObj.setXmlLog(testFnEl,testFnDescription)
			testObj.enableXmlLog(True)
		else:
			testObj.enableXmlLog(False)

		self.primitiveTests.append(testObj)

		return testObj
 
	########## End of Function ##########
	
	def readConfigFile(self,configFile):

	# Reads config file and returns list of steps to be performed in script.

	# Syntax      : OBJ.readConfigFile()
	# Description : Reads config file and returns list of steps to be performed in script.
	# Parameters  : configFile - Name of config file.
	# Return Value: List of steps to be performed in script.

		itemList = []
		# TODO : configFile = str(sys.argv[0]).replace(".py",".config")
		configFile = self.realpath + "fileStore/" + configFile
		print "Configuration File Found : ", configFile
		sys.stdout.flush()

		# Checking if file exists
		fileCheck = os.path.isfile(configFile)
		if (fileCheck):
			configFileObj = open(configFile,'r')
			
			# Parsing through config file and appending list
			line = configFileObj.readline()
			while(line != ''):
				line = line.rstrip('\n')
				itemList.append(line)
				line = configFileObj.readline()

			configFileObj.close()
		else:
			print "#TDK_@error-ERROR : Configuration File does not exist."
			sys.stdout.flush()
			#exit()

		return itemList

	########## End of Function ##########


	def unloadModule(self, cName):

	# Unload the component test module

	# Syntax       : OBJ.unloadModule(cName)
	# Description  : Unload module
	# Parameters   : cName - Component name
	# Return Value : null
    		try:
			if(self.enabledXmlLogging == True):
				logdir=self.logpath+"/logs/"+str(self.execID)+"/"+str(self.execDevId)+"/"+str(self.resultId)
				print "print the xml log to  "+logdir
				if not os.path.exists(logdir):
					os.makedirs(logdir)

				logxmlfile = open(logdir+"/"+str(self.scriptName)+"_xmllog.xml", "wb")	
				logstr=self.xmlLogDom.toprettyxml(indent='\t')
				logxmlfile.write(logstr)
				logxmlfile.close()
			
			final = {'jsonrpc':'2.0','id':'2','method':'UnloadModule','param1':cName,'version':self.rdkversion, \
                                 'ScriptSuiteEnabled':self.scriptSuiteEnabled}
			query = json.dumps(final)
			self.tcpClient.send(query)
			unloadmoduleresult = self.tcpClient.recv(1048)
		
		except socket.error:
			print "******************************************************************************************" 
			print " #TDK_@error-Error while Connecting to Server ... "
			print " Please ensure the Box " + self.IP + " is up and Test Agent is running..."
			print "******************************************************************************************" 
			sys.stdout.flush()
			self.tcpClient.close()
			#exit()
		except:
			print "#TDK_@error-ERROR : Unable to connect.. Please check box is up and agent is running.....\nOr there can be a problem with writing the xml log file. "
			print "Details : "
			logging.exception('')
			sys.stdout.flush()
			self.tcpClient.close()
			#exit()
		else:
			if unloadmoduleresult:
				if "SUCCESS" in unloadmoduleresult.upper():
					print "Unload Module Status  : Success"
					endTime=time.time()
					self.timeTaken=endTime-self.startTime
				else:
					print "Unload Module Status  : Failure"

				if "details" in unloadmoduleresult:
					resultIndex = unloadmoduleresult.find("details") + len("details\":\"")
					message = unloadmoduleresult[resultIndex:]
					message = message[:(message.find("\""))]
					print "Unload Module Details : " + message
			else:
				print "#TDK_@error-ERROR : Unload Module failed\n"	
				sys.stdout.flush()
				self.tcpClient.close()
				#exit()

		sys.stdout.flush()
		self.tcpClient.close()
		return 

	########## End of Function ##########

	def initiateReboot(self):

	# To initiate a reboot on device under test

	# Syntax       : OBJ.initiateReboot()
	# Description  : Initiate a reboot
	# Parameters   : none
	# Return Value : null


		# Invoking RPC 'EnableReboot' to reboot the device 
		try:
			message = {'jsonrpc':'2.0','id':'2','method':'EnableReboot','version':self.rdkversion}
			query = json.dumps(message)
			self.tcpClient.send(query)
	
		except socket.error:
			print "******************************************************************************************" 
			print " #TDK_@error-Error while Connecting to Server ... "
			print " Please ensure the Box " + self.IP + " is up and Test Agent is running..."
			print "******************************************************************************************" 
			sys.stdout.flush()
			#exit()
		except:
			print "#TDK_@error-ERROR : Unable to connect.. Please check box is up and agent is running.....\n"
			print "Details : "
			logging.exception('')
			sys.stdout.flush()
			#exit()
		else:
			self.tcpClient.setblocking(0)
			recvStatus = select.select([self.tcpClient], [], [], 5) #Setting timeout for response(3 Sec)
			if recvStatus[0]:
				result = self.tcpClient.recv(1048)
				if "SUCCESS" in result.upper():
					print "\"" + self.IP + "\"" + " Going For a Reboot.."
					sys.stdout.flush()
				else:
					print "#TDK_@error-ERROR : Unable to set preconditons for reboot"
					resultIndex = result.find("details") + len("details"+"\":\"")
					message = result[resultIndex:]
					details = message[:(message.find("\""))]
					print "Deatils : " + details
					sys.stdout.flush()
					#exit()
		
		# Waiting to get a "FREE" status from device
		time.sleep(60);

		while(1):

			time.sleep(5)
			status = getStatus(self.IP, "NULL", "NULL", self.statusPort)
			if "FREE" in status.upper():
				break;

		time.sleep(10);

		# Invoking RPC 'RestorePreviousState' to restore the state before reboot
		try:
			message = {'jsonrpc':'2.0','id':'2','method':'RestorePreviousState','version':self.rdkversion,\
				   'execID':str(self.execID),'deviceID':str(self.deviceId),'testcaseID':str(self.testcaseId),\
				   'execDevID':str(self.execDevId),'resultID':str(self.resultId)}
			query = json.dumps(message)

			self.tcpClient = socket.socket()
			self.tcpClient.connect((self.IP, self.portValue))
			self.tcpClient.send(query)

		except socket.error:
			print "******************************************************************************************" 
			print " #TDK_@error-Error while Connecting to Server ... "
			print " Please ensure the Box " + self.IP + " is up and Test Agent is running..."
			print "******************************************************************************************" 
			sys.stdout.flush()
			exit()
		except:
			print "#TDK_@error-ERROR : Unable to connect.. Please check box is up and agent is running.....\n"
			print "Details : "
			logging.exception('')
			sys.stdout.flush()
			exit()
		else:
			result = self.tcpClient.recv(1048)
			if "SUCCESS" in result.upper():
				print "\"" + self.IP + "\"" + " Rebooted Successfully.Previous state restored.."	
				sys.stdout.flush()
			else:
				print "#TDK_@error-ERROR : Unable to restore previous state after reboot" 
				resultIndex = result.find("details") + len("details"+"\":\"")
				message = result[resultIndex:]
				details = message[:(message.find("\""))]
				print "Details : " + details
				sys.stdout.flush()
				exit()

		return

	########## End of Function ##########
 
	def resetConnectionAfterReboot(self):

	# To reset tcp connection with other instances after STB reboot in multi component tests

	# Syntax       : OBJ.resetConnectionAfterReboot()
	# Description  : To reset tcp connection with other instances after STB reboot in multi component tests
	# Parameters   : none
	# Return Value : null

		print "Resetting connection after Reboot"
		self.tcpClient.close()
		time.sleep(5)
		self.tcpClient = socket.socket()
		self.tcpClient.connect((self.IP, self.portValue))
		return

	########## End of Function ##########

	def fetchLastExecutionId(self):
    	# fetch last inserted executionId from the database
    	# Syntax       : obj.fetchLastExecutionId();
    	# Description  : fetch last inserted executionId from  execution table of database
   	# Parameters   : 
    	# Return Value : executionId
		global isDatabase	
		lastExecutionId = 0
    		try:
                        conn = MySQLdb.connect (host = "localhost", user = username, passwd = password, db = "rdktesttoolproddb")
	                cur = conn.cursor()
        	        query = "SELECT id FROM execution ORDER BY id DESC limit 1";
	                #print query;
			cur.execute(query);
			lastExecId = list(cur.fetchall());
	                #print "list value: ", lastExecId;
			#print "Row(s) were updated :" +  str(cur.rowcount);
		        #print "Last ExecutionId fetched from the database is:", lastExecId[0];
			for execId in lastExecId:
				print (execId[0] + 1)
			conn.commit();
        	        conn.close();
			lastExecutionId	 = execId[0]+1
			isDatabase = True
                	return lastExecutionId;

		except MySQLdb.Error, sqlErr:
                        lastExecutionId = random.randint(0, 32767) 
			print "Random ExecutionId generated %d" %lastExecutionId
			print "ERROR: Exception in SQL Database while fetching LastExecutionId. \nException type is: %s" %sqlErr
			return lastExecutionId
		except Exception, e:
			print "ERROR : exception in fetching last executionId!\n";
                        print "Exception type is: %s" %e;
                	
		else:
                        print "Unload module Success\n"
    ########## End of Function ##########	

	def fetchLastExecutionResultId(self):
        # fetch last inserted executionresultId from the database
        # Syntax       : obj.fetchLastExecutionResultId();
        # Description  : fetch last inserted executionresultId from  execution_result table of database
        # Parameters   :
        # Return Value : executionresultId
		global isDatabase	
		lastExecutionResultId=0
                try:
                        conn = MySQLdb.connect (host = "localhost", user = username, passwd = password, db = "rdktesttoolproddb")
                        cur = conn.cursor()
                        query = "SELECT id FROM execution_result ORDER BY id DESC limit 1";
                        #print query;
                        cur.execute(query);
                        lastExecResId = list(cur.fetchall());
                        print "list value: ", lastExecResId;
                        print "Row(s) fetched :" +  str(cur.rowcount);
                        print "Last ExecutionId fetched from the database is:", lastExecResId[0];
                        for execResId in lastExecResId:
                                print execResId[0]
                        conn.commit();
                        conn.close();
			lastExecutionResultId=execResId[0]
			isDatabase = True
                        return lastExecutionResultId;

                except MySQLdb.Error, sqlErr:
			lastExecutionResultId = random.randint(0, 32767)
                        print "Random ExecutionResultId generated %d" %lastExecutionResultId
			print "ERROR: Exception in SQL Database while fetching LastExecutionResultId. \nException type is: %s" %sqlErr
			return lastExecutionResultId
		except Exception, e:
                        print "ERROR : exception in fetching last executionResultId!\n";
                        print "Exception type is: %s" %e;
                else:
                        print "Unload module Success\n"
    ########## End of Function ##########

        def fetchLastExecuteMethodResultId(self):
        # fetch last inserted executemethodresultId from the database
        # Syntax       : obj.fetchLastExecuteMethodResultId();
        # Description  : fetch last inserted executemethodresultId from  execute_method_result table of database
        # Parameters   :
        # Return Value : executemethodresultId
		global isDatabase	
		lastExecuteMethodResultId = 0
                try:
                        conn = MySQLdb.connect (host = "localhost", user = username, passwd = password, db = "rdktesttoolproddb")
                        cur = conn.cursor()
                        query = "SELECT id FROM execute_method_result ORDER BY id DESC limit 1";
                        print query;
                        cur.execute(query);
                        lastExecMethResId = list(cur.fetchall());
			print "list value: ", lastExecMethResId;
                        print "Row(s) fetched :" +  str(cur.rowcount);
                        print "Last ExecuteMethodResultId fetched from the database is:", lastExecMethResId[0];
                        for execMethResId in lastExecMethResId:
                                print execMethResId[0]
                        conn.commit();
                        conn.close();
                        lastExecuteMethodResultId = execMethResId[0];
			isDatabase = True
			return lastExecuteMethodResultId

                except MySQLdb.Error, sqlErr:
                        lastExecuteMethodResultId = random.randint(0, 32767)
                        print "Random ExecuteMethodResultId generated %d" %lastExecuteMethodResultId
			print "ERROR: Exception in SQL Database while fetching LastExecuteMethodResultId. \nException type is: %s" %sqlErr
                        return lastExecuteMethodResultId
		except Exception, e:
                        print "ERROR : exception in fetching last executeMethodResultId!\n";
                        print "Exception type is: %s" %e;
                else:
                        print "Unload module Success\n"
    ########## End of Function ##########

	def fetchLastExecutionDeviceId(self):
        # fetch last inserted executionDeviceId from the database
        # Syntax       : obj.fetchLastExecutionDeviceId();
        # Description  : fetch last inserted executiondeviceId from  execute_method_result table of database
        # Parameters   :
        # Return Value : executemethodresultId
		global isDatabase	
		lastExecutionDeviceId=0
                try:
                        conn = MySQLdb.connect (host = "localhost", user = username, passwd = password, db = "rdktesttoolproddb")
                        cur = conn.cursor()
                        query = "SELECT id FROM execution_device ORDER BY id DESC limit 1";
                        print query;
                        cur.execute(query);
                        lastExecDevId = list(cur.fetchall());
                        print "list value: ", lastExecDevId;
                        print "Row(s) fetched  :" +  str(cur.rowcount);
                        print "Last ExecutionDeviceId fetched from the database is:", lastExecDevId[0];
                        for execDevId in lastExecDevId:
                                print execDevId[0]
                        conn.commit();
                        conn.close();
                        lastExecutionDeviceId = execDevId[0]
			isDatabase = True
			return lastExecutionDeviceId;
                
		except MySQLdb.Error, sqlErr:
			lastExecutionDeviceId = random.randint(0, 32767)
			print "Random ExecutionDeviceId generated %d" %lastExecutionDeviceId
			print "ERROR: Exception in SQL Database while fetching LastExecutionDeviceId. \nException type is: %s" %sqlErr
                        return lastExecutionDeviceId
		except Exception, e:
                        print "ERROR : exception in fetching last executionDeviceId!\n";
                        print "Exception type is: %s" %e;
                else:
                        print "Unload module Success\n"
    ########## End of Function ##########	

	def insertScriptAndFnExeDetailsInDb(self):
		global isDatabase		
		print "Database flag is set to ",isDatabase
		if (isDatabase):
			script=self.scriptName 
			executionDate = strftime("%Y-%m-%d %H:%M:%S", gmtime());
			print "Date of Execution: "+ str(executionDate);
			devName=self.execName.split("-")[0]
			print "Device Name: "+str(devName);
                        conn = MySQLdb.connect (host = "localhost", user = username, passwd = password, db = "rdktesttoolproddb")
			cur = conn.cursor()
			logfile=open(self.logpath+"/logs/"+self.scriptName+".log")
			outputData=logfile.read() 
			logfile.close()
			outputData=conn.escape_string(outputData)
			timeNow=time.time()
			executionTime=timeNow-self.startTime
			query1 = """INSERT INTO execution (
				id, 

				version, 
				date_of_execution, 
				device, 
				device_group, 

				execution_time, 
				is_marked, 
				name, 
				output_data, 

				result, 
				script, 
				script_group, 
				groups_id,
				execution_status, 

				is_performance_done,
				is_aborted,
				is_bench_mark_enabled,
				is_rerun_required,

				is_system_diagnostics_enabled,
				script_count) VALUES ('%s','%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s', NULL,'COMPLETED', 0,0,0,0,0,0)""" %(self.execID, 
				self.rdkversion, 
				executionDate, 
				devName, 
				"NULL", 
				executionTime, 
				0, 
				self.execName, 
				outputData, 
				self.resultStatus, 
				script, 
				"NULL");
			try:
				cur.execute(query1);
				print "Row(s) updated :" +  str(cur.rowcount)+" in table: execution";
				conn.commit();
			except Exception ,e:
				#print sys.exc_info()[0]
				print str(e)
				print "------"+e.message
			
			query4 = "INSERT INTO execution_device (id, version, date_of_execution, device, device_ip, execution_id, execution_time, status) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (self.execDevId, self.rdkversion, executionDate, devName, self.IP, self.execID, executionTime, self.resultStatus);
			#print query4;
			try :
				cur.execute(query4);
				print "Row(s) updated :" +  str(cur.rowcount)+" in table: execution_device";
				conn.commit();
			except Exception, e:
				print str(e)
	                        print "------"+e.message
			query2 = """INSERT INTO execution_result (id, version, device, execution_id, execution_device_id, execution_output, script, status) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')""" % (self.resultId, self.rdkversion, devName, self.execID, self.execDevId, outputData, script,  self.resultStatus);
	                try :
				cur.execute(query2);
				print "Row(s) updated :" +  str(cur.rowcount)+" in table: execution_result";
				conn.commit();
			except Exception, e:
				print str(e)
                	        print "------"+e.message
		
			for testFn in self.primitiveTests :
				expectedResult = "Test Suite Executed"
				executeMethodId=self.fetchLastExecuteMethodResultId()+1		
				query3 = """INSERT INTO execute_method_result (id, version, actual_result, execution_result_id, expected_result, function_name, status) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (executeMethodId, self.rdkversion, testFn.resultStatus, self.resultId, expectedResult, testFn.testCaseName, testFn.resultStatus);
				try :
					cur.execute(query3);
					print "Row(s) updated :" +  str(cur.rowcount)+" in table: execute_method_result";
					conn.commit();
				except Exception, e:
					print str(e)
					print "------"+e.message

			conn.close();
		else:
			print "Database is not available inside insertScriptAndFnExeDetailsInDb.\n"
    ########## End of Function ##########
	
	def checkAndVerifyDvrRecording(self,duration=4):
        # Checks to see sepcified duration or greater duration recording is present or not.
        # If not, records with specidifed duration.

        # Syntax       : OBJ.checkAndVerifyDvrRecording(duration)
        # eg           : OBJ.checkAndVerifyDvrRecording(3)
        # Description  : Checks to see sepcified duration or greater duration recording is present or not.
        # If not, records with specidifed duration.
        # Parameters   : duration - duration of the recording to check for in mins.
        # Return Value : result will be list with recording details found, else empty list if not found.
        # eg           : list = [0,'1111111','test_dvr',299,2121443214321423]
        #                       [index,recordingId,recordingName,durationInSecs,sgementName] - if found.
        #               else, Empty list.
                print "In checkAndVerifyDvrRecording"
                numOfRecordings,recordingObj = fetchTotalRecording(self)
                list1 = []

                if recordingObj == "NULL":
                        print "Failed to fetch Recording list."
                        return list1

                print "Done Fetching list1"

                list1 = findRecordMatchingDuration(numOfRecordings,recordingObj,duration)
                if (len(list1) == 0):
                        print "Matching Recording not found. So, Recording initiated with the duration required"
                        #Increasing the duration by 1 minute. To make sure sufficient recording will be done.
                        result = initiateDvrRecording(self,duration + 1)
                        if result == 1:
                                print "Initiated recording for ",duration," failed!!!."
                                list2 = []
                                return list2
                        print "Recording Successful!!!."
                        numOfRecordings,recordingObj = fetchTotalRecording(self)
                        if recordingObj == "NULL":
                                print "Failed to fetch Recording list. After initiating recording."
                                return list1

                        print "Done Fetching"
                        list1 = findRecordMatchingDuration(numOfRecordings,recordingObj,duration)
                        print "List:",list1
                        return list1

                print "Match found!!!. Recording details: ",list1

                return list1;
    ########## End of Function ##########	
########## End of Class  ##########

#Helper function to return a list (containing matching Record details else empty)
def findRecordMatchingDuration(numOfRecordings,recordingObj,duration):
        print "In findRecordMatchingDuration"
        list1 = []
        if numOfRecordings > 0:
                i = 0
                while i< numOfRecordings:
                        du = recordingObj.getDuration(i);
                        print "Duration: ",du
                        #converting the duration into seconds and comparing it with avaliable recordings duration.
                        if int(du) >= (duration * 60):
                                list1 = [i];
                                list1.append(recordingObj.getRecordingId(i))
                                list1.append(recordingObj.getRecordingTitle(i))
                                list1.append(recordingObj.getDuration(i))
                                list1.append(recordingObj.getSegmentName(i))
                                print "Matching recording found with duration found."
                                print list1
                                return list1
                        i = i + 1

        print "Matching recording not found."
        return list1
		
#Helper function to return Number of Recordings.
def fetchTotalRecording(testObj):
        print "In FetchTotalRecording"
        primitiveObj = testObj.createTestStep("RMF_GetDvr_Recording_List");

        recordingObj = primitiveObj.getRecordingDetails();
        print "Call done for reading the file"
        numOfRecordings = recordingObj.getTotalRecordings();
        print "Total Rec: ",numOfRecordings

        return numOfRecordings,recordingObj

		
#Helper funtion to InitiateRecording
def initiateDvrRecording(testObj,duration):
        primitiveObj = testObj.createTestStep("RMF_Dvr_CreateNew_Recording");
        RECORD_ERROR = 1
        SUCCESS = 0
		
        streamDetails = primitiveObj.getStreamDetails('01');

        recordtitle = "test_dvr"
        #Generating the random recordid of 10 digits.
        recordidInt = random.randrange(10**9, 10**10)
        recordid = str(recordidInt)
        recordduration = str(duration)
        ocapid = streamDetails.getOCAPID();

        print recordid
        print recordduration
        print recordtitle
        print ocapid

        primitiveObj.addParameter("recordId",recordid);
        primitiveObj.addParameter("recordDuration",recordduration);
        primitiveObj.addParameter("recordTitle",recordtitle);
        primitiveObj.addParameter("ocapId",ocapid);

        expectedresult="SUCCESS"

        print "Before executing the Test case"
        #Execute the test case in STB
        primitiveObj.executeTestCase(expectedresult);

        print "After execu done"
        #Get the result of execution
        result = primitiveObj.getResult();
        print "Result of recording: ",result

        #Check any failure, During the recording.
        if expectedresult not in result.upper():
                print "Failed to record"
                primitiveObj.setResultStatus(result);
                return RECORD_ERROR

        print "Initiating Reboot";
        testObj.initiateReboot();

        primitiveObj.setResultStatus(result);

        time.sleep(5)
        print "Reboot Done"

        return SUCCESS
		
#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------

class CreateTestThread (threading.Thread):
        """
        Class to run tests in multiple box in parallel

        Syntax       : obj = CreateTestThread (ipAddress, port, FunctionName) 

        Description  : Class helps the users to run different test on different box from the same script.

	parameter    : IP - ip address of the device under test
		       port - port number
		       function - name of the function to be invoked in that thread 
 
        """
	#------------------------------------------------------------------------------
	# __init__ , __del__ and run block
	#------------------------------------------------------------------------------

	def __init__ (self, IP, port, function, args=(), kwargs={}):
		threading.Thread.__init__(self)
		self.function = function
		self.IP = IP
		self.port = port
		self.args = args
		self.kwargs = kwargs

	def run(self):
		print "Starting Thread for " + self.IP + "\n"
		sys.stdout.flush()
               	
		self.returnValue = self.function(self.IP,self.port,self.args,self.kwargs)

		print "Exiting Thread for " + self.IP + "\n"
		sys.stdout.flush()

	def __del__(self):
		return


########## End of Class  ##########


#------------------------------------------------------------------------------
# module class
#------------------------------------------------------------------------------

class ClientList:

        """
        Class to fetch details of a client box

        Description  : This class is used to get details of client boxes connected to a gateway
        Syntax       : OBJ = ClientList (clientList)
        Parameters   : clientList - List of client devices with their mac address and agent port number
        """

        #------------------------------------------------------------------------------
        # __init__ and __del__ block
        #------------------------------------------------------------------------------

        def __init__(self, clientList):
                self.clientList = clientList
                self.clientLength = len(self.clientList)
                return

        def __del__(self):
                return

        #------------------------------------------------------------------------------
        # Public methods
        #------------------------------------------------------------------------------

        def getNumberOfClientDevices(self):

        # To get number of client devices

        # Syntax       : OBJ.getNumberOfClientDevices()
        # Description  : To get number of client devices
        # Parameters   : none
        # Return Value : number of client devices

                return len(self.clientList)

        ########## End of Function ##########

        def getAgentPort(self,index):

        # To get agent port number of device with given index

        # Syntax       : OBJ.getAgentPort(index)
        # Description  : To get agent port number
        # Parameters   : index of client device in client list
        # Return Value : port number

                if (index <= self.clientLength):
                        return self.clientList[index][1]
                else:
                        print "Only \"" + str(self.clientLength) + "\" client devices are available for test execution"
                        sys.stdout.flush()
                        exit()

        ########## End of Function ##########


        def getClientMACAddress(self, index):

        # To get mac address of device with given index

        # Syntax       : OBJ.getClientMACAddress()
        # Description  : To get mac address
        # Parameters   : index of client device in client list
        # Return Value : mac address

                if (index <= self.clientLength):
                        mac = self.clientList[index][0]
                        return mac
                else:
                        print "Only \"" + str(self.clientLength) + "\" client devices are available for test execution"
                        sys.stdout.flush()
                        exit()

        ########## End of Function ##########


########## End of Class  ##########



# To initiate a Create and Execute test cases in all the modules
#
# Syntax       : Create_ExecuteTestcase(obj,primitivetest,expectedresult,verifyList, **kwargs)
#
# Parameters   : obj,primitivetest,expectedresult,verifyList, **kwargs
#
# Return Value : 0 on success and 1 on failure

def Create_ExecuteTestcase(obj,primitivetest,expectedresult,verifyList, **kwargs):
    print kwargs
    details = "NULL";
 
    #calling primitive test case    
    tdkTestObj = obj.createTestStep(primitivetest);
    for name, value in kwargs.iteritems():
      
        print "Name: %s"%str(name);
        tdkTestObj.addParameter(str(name),value);                                   
       
    Expectedresult=expectedresult;
    tdkTestObj.executeTestCase(Expectedresult); 
    actualresult = tdkTestObj.getResult();
    print "Actual Result: %s"%actualresult;
    
    try: 
        details = tdkTestObj.getResultDetails();
        print "Details:%s"%details;
    except:                
        pass;
    
    #Check for SUCCESS/FAILURE return value 
    if Expectedresult in actualresult:
        count = 0;
        if verifyList:
            print "Verify List not empty"
            for name,value in verifyList.items():	
                print "Name:%s,Value:%s to be verified in the details"%(name,value);
                if value in details:
            	    print details;	    
                    print "SUCCESS : %s sucess"%primitivetest;
                    #count+=1;
                    #if count > 0:
                    tdkTestObj.setResultStatus("SUCCESS");
                    #    print "SUCCESS:%s"%(primitivetest);
                else:                    
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE:Value not in details %s" %details;
        else:            
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");            
    
    return (actualresult,tdkTestObj,details);



########## End of tdklib ##########


