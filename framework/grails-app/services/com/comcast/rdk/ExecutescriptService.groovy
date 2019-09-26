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
package com.comcast.rdk

import static com.comcast.rdk.Constants.*
import groovy.sql.Sql

import java.text.DecimalFormat
import java.util.List
import java.util.concurrent.Callable
import java.util.concurrent.ExecutorService
import java.util.concurrent.Future
import java.util.concurrent.Executors
import java.util.concurrent.FutureTask;


/**
 * 
 * Service class of ExecutionController
 *
 */

class ExecutescriptService {
	/**
	 * Injecting executor service.
	 */
	static ExecutorService executorService = Executors.newCachedThreadPool()

	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication

	/**
	 * Injects the executionService.
	 */
	def executionService
	
	def scriptService

	/**
	 * Injects the deviceStatusService.
	 */
	def deviceStatusService

	/**
	 * Injects the scriptexecutionService.
	 */
	def scriptexecutionService

	/**
	 * Injects the tclExecutionService
	 */
	def tclExecutionService
	/**
	 * Injects dataSource.
	 */
	def dataSource
	public static volatile Object  lock = new Object()
	
	/**
	 * Sets the transactional to false as it is causing many issues
	 * in database operations that invokes from different threads.
	 */
	static transactional = false

	/**
	 * Method to execute the script
	 * @param scriptGroupInstance
	 * @param scriptInstance
	 * @param deviceInstance
	 * @param url
	 * @return
	 */
	
	def String executeScript(final String executionName, final ExecutionDevice executionDevice, final def scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark, final String isSystemDiagnostics,final String uniqueExecutionName,final String isMultiple, def executionResult,def isLogReqd, final def category) {
				Date startTime = new Date()
		String htmlData = ""
		String scriptData = executionService.convertScriptFromHTMLToPython(scriptInstance?.scriptContent)
		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES
		def executionInstance = Execution.findByName(executionName)
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution
		def resultArray = Execution.executeQuery("select a.executionTime from Execution a where a.name = :exName",[exName: executionName])
		def totalTimeArray = Execution.executeQuery("select a.realExecutionTime from Execution a where a.name = :exName",[exName: executionName])
		def executionResultId
		if(executionResult == null){			
		    try {
			   def sql = new Sql(dataSource)
			   sql.execute("insert into execution_result(version,execution_id,execution_device_id,script,device,date_of_execution,status,category) values(?,?,?,?,?,?,?,?)", [1,executionInstance?.id, executionDevice?.id, scriptInstance.name, deviceInstance.stbName, startTime, UNDEFINED_STATUS, category])
			    def result = ExecutionResult.findByExecution(executionInstance)
			} catch (Exception e) {
				e.printStackTrace()
			}

			def resultArray1 = ExecutionResult.executeQuery("select a.id from ExecutionResult a where a.execution = :exId and a.script = :scriptname and device = :devName ",[exId: executionInstance, scriptname: scriptInstance.name, devName: deviceInstance?.stbName.toString()])
			if(resultArray1[0]){
				executionResultId = resultArray1[0]
			}
		}else{
			executionResultId = executionResult?.id
		}
		def mocaDeviceList = Device.findAllByStbIpAndMacIdIsNotNull(deviceInstance?.stbIp)
		
		int counter = 1
		def mocaString = CURLY_BRACKET_OPEN
		
		int mocaListSize = mocaDeviceList?.size()
		mocaDeviceList.each{ mocaDevice ->
			
			mocaString = mocaString + counter.toString() + COLON + SQUARE_BRACKET_OPEN + STRING_QUOTES + mocaDevice?.macId + STRING_QUOTES +
			COMMA_SEPERATOR + mocaDevice?.stbPort + SQUARE_BRACKET_CLOSE
			
			if(mocaListSize != counter){
				mocaString = mocaString + COMMA_SEPERATOR
			}
			counter++
		}
		mocaString = mocaString + CURLY_BRACKET_CLOSE
		
		scriptData = scriptData.replace( IP_ADDRESS , stbIp )
		scriptData = scriptData.replace( PORT , deviceInstance?.stbPort )		
		scriptData = scriptData.replace( CLIENTLIST , mocaString )
		
		String gatewayIp = deviceInstance?.gatewayIp		
		String logFilePath = realPath?.toString()+"/logs/logs/"
		
		def sFile = ScriptFile.findByScriptNameAndModuleName(scriptInstance?.name,scriptInstance?.primitiveTest?.module?.name)

		/*scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
				executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
				sFile?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
				SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR)*/
		
		scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES +logFilePath+SINGLE_QUOTES + COMMA_SEPERATOR +
			executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.agentMonitorPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
			sFile?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
			SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR)


		scriptData	 = scriptData + "\nprint \"SCRIPTEND#!@~\";"
		Date date = new Date()
		String newFile = FILE_STARTS_WITH+date.getTime().toString()+PYTHON_EXTENSION
		File file = new File(filePath, newFile)
		boolean isFileCreated = file.createNewFile()
		if(isFileCreated) {
			file.setExecutable(true, false )
		}
		PrintWriter fileNewPrintWriter = file.newPrintWriter();
		fileNewPrintWriter.print( scriptData )
		fileNewPrintWriter.flush()
		fileNewPrintWriter.close()
		
		Date executionStartDt = new Date()
		def executionStartTime =  executionStartDt.getTime()
		
		int execTime = 0
		try {
			if(scriptInstance?.executionTime instanceof String){
				execTime = Integer.parseInt(scriptInstance?.executionTime)
			}else if(scriptInstance?.executionTime instanceof Integer){
				execTime = scriptInstance?.executionTime?.intValue()
			}else {
				execTime = scriptInstance?.executionTime
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		
		
		String outData = executionService.executeScript( file.getPath() , execTime, uniqueExecutionName , scriptInstance.name)
		file.delete()
		
		def logPath = "${realPath}/logs//${executionId}//${executionDevice?.id}//${executionResultId}//"
		copyLogsIntoDir(realPath,logPath, executionId,executionDevice?.id, executionResultId)	
		
		
		
		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}
		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()
		// time difference for single script in seconds
		def timeDifference = ( execEndTime - executionStartTime  ) / 1000;
		String timeDiff =  String.valueOf(timeDifference)	
		String singleScriptExecTime = timeDifference
		try
		{
			def cumulativeTime
			if(resultArray){
				cumulativeTime = calculateTotalExecutiontime(resultArray[0], timeDiff)
			}else{
				cumulativeTime = calculateTotalExecutiontime(resultArray, timeDiff)
			}
			timeDiff = convertExecutionTimeFormat(cumulativeTime )
			singleScriptExecTime = convertExecutionTimeFormat((new BigDecimal (singleScriptExecTime)))
			if(singleScriptExecTime.contains(".") ){
				int index = singleScriptExecTime.indexOf(".")
				if((index + 3) < singleScriptExecTime.length() ){
					singleScriptExecTime = singleScriptExecTime.substring(0, index+3);
				}
			}
		}
		catch (Exception e) {
			e.printStackTrace()
		}
		
		
		if(executionService.abortList.contains(executionInstance?.id?.toString())){
			
			resetAgent(deviceInstance,TRUE)
		}else if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
			}
			//def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
			def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
			def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"
			//new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			//logTransfer(deviceInstance,logTransferFilePath,logTransferFileName)
			logTransfer(deviceInstance,logTransferFilePath,logTransferFileName,realPath, executionId,executionDevice?.id, executionResultId,url)
			if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
				//transferSTBLog(scriptInstance?.primitiveTest?.module?.name, deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId)
				transferSTBLog(scriptInstance?.primitiveTest?.module?.name, deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId , realPath,url)
			}
			executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
			Thread.sleep(4000)
			hardResetAgent(deviceInstance)
			if(deviceInstance?.isChild)
			{
				def parentDevice = Device.findByStbIp(deviceInstance?.gatewayIp)
				if(parentDevice != null && parentDevice?.childDevices?.contains(deviceInstance))
				{
					String stat = DeviceStatusUpdater?.fetchDeviceStatus(grailsApplication, parentDevice)
					if(  stat?.equals(Status.BUSY.toString()) || stat?.equals(Status.HANG.toString()) ){
							hardResetAgent(parentDevice)
							Thread.sleep(4000)
					}
				}
			}
		}else if(htmlData.contains("Pre-Condition not met")){
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
			}
			executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
		}
		else{
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
//				if(!checkExecutionCompletionStatus(executionResultId)){
//					executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
//				}else{
					String outputData = htmlData
					executionService.updateExecutionResults(outputData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
//				}
			}
			else{
				
				
				if((timeDifference >= execTime) && (execTime != 0))	{					
					File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
					def absolutePath = layoutFolder.absolutePath
					String[] cmd = [
						PYTHON_COMMAND,
						absolutePath,
						deviceInstance?.stbIp,
						deviceInstance?.agentMonitorPort,
						TRUE
					]
					ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
					def resetExecutionData = ""
					
					try {
						resetExecutionData = scriptExecutor.executeScript(cmd,1)
					} catch (Exception e) {
						e.printStackTrace()
					}
					executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
					htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
					executionService.updateExecutionResultsTimeOut(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
					Thread.sleep(10000)
				}else{
					executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
					Thread.sleep(4000)
					resetAgent(deviceInstance)
				}
			}
		}
		if(!executionService.abortList.contains(executionInstance?.id?.toString())){
		String performanceFilePath
		String performanceFileName
		String diagnosticsFilePath
		if(isBenchMark.equals(TRUE) || isSystemDiagnostics.equals(TRUE)){
			//new File("${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			performanceFileName = "${executionId}_${executionDevice?.id}_${executionResultId}"
			performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}//"
			diagnosticsFilePath = "${realPath}//logs//stblogs//${executionId}//${executionDevice?.id}//${executionResultId}//"
		}
		def tmUrl = executionService.updateTMUrl(url,deviceInstance)
		if(isBenchMark.equals(TRUE)){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath

			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.agentMonitorPort,
				//deviceInstance?.logTransferPort,
				KEY_PERFORMANCE_BM,
				performanceFileName,
				//performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,1)
			copyPerformanceLogIntoDir(realPath, performanceFilePath, executionId,executionDevice?.id, executionResultId)
		}
		if(isSystemDiagnostics.equals(TRUE)){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.agentMonitorPort,
				//deviceInstance?.logTransferPort,
				KEY_PERFORMANCE_SD,
				performanceFileName,
				//performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,10)
			copyPerformanceLogIntoDir(realPath, performanceFilePath, executionId,executionDevice?.id, executionResultId)
			
			initiateDiagnosticsTest(deviceInstance, performanceFileName, tmUrl,uniqueExecutionName)
			copyLogFileIntoDir(realPath, diagnosticsFilePath, executionId,executionDevice?.id, executionResultId,DEVICE_DIAGNOSTICS_LOG)
		}
		//def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"
		def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
		//new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			logTransfer(deviceInstance,logTransferFilePath,logTransferFileName ,realPath, executionId,executionDevice?.id, executionResultId,url)
		if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
			transferSTBLog(scriptInstance?.primitiveTest?.module?.name, deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId, ,realPath,url)
		}
		}
		Date endTime = new Date()
		try {
			def totalTimeTaken = (endTime?.getTime() - startTime?.getTime()) / 1000
	//		totalTimeTaken = totalTimeTaken?.round(2)
			executionService.updateExecutionTime(totalTimeTaken?.toString(), executionResultId)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return htmlData
	}
	
	/**
	* The function for getting the cummulative time for execution  in seconds
	* @param totalExecutionTime
	* @param scriptExecutionTime
	* @return totalExecTime
	*/
			
	def calculateTotalExecutiontime(def totalExecutionTime , def scriptExecutionTime)
	{

		BigDecimal totalExecTime
		if(totalExecutionTime){
			def totalTime =  Double.parseDouble(totalExecutionTime);
			def minPart = (long) totalTime
			def decimalPart = totalTime - minPart;
			totalExecTime = ((new BigDecimal (minPart))*60) + new BigDecimal (scriptExecutionTime) + ((new BigDecimal (decimalPart))*100)
		}
		else{
			totalExecTime =  new BigDecimal (scriptExecutionTime)

		}
		return totalExecTime
	}

	/**
	 * The function for getting the execution time mm.ss format
	 * @param executionTime
	 * @return timeDiff
	 */
	def convertExecutionTimeFormat(def executionTime)
	{
		BigDecimal timeCount = 60.00;
		BigDecimal mintVal = 0
		BigDecimal secVal = 0
		if(executionTime>timeCount){
			mintVal =(int)  executionTime/timeCount
			secVal =  executionTime.remainder(timeCount)
			
		}
		else{
			secVal = executionTime
		}
		executionTime =mintVal+(secVal/100)
		def timeDiff =  String.valueOf(executionTime)
		return timeDiff
	}
			
			/**
			 * The function for performance related log transfer using TFTP server
			 * @param realPath
			 * @param logTransferFilePath
			 * @return
			 */
			def copyAgentconsoleLogIntoDir(def realPath, def logTransferFilePath, def executionId, def executionDeviceId , def executionResultId){
				try {
					String logsPath = realPath.toString()+"/logs/logs/"
					File logDir  = new File(logsPath)
					if(logDir.isDirectory()){
						logDir.eachFile{ file->
							if(file?.name?.contains("AgentConsoleLog.txt")){
								def logFileName =  file.getName().split("_")
									if(logFileName?.length >= 3){
										if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
										new File(logTransferFilePath?.toString()).mkdirs()
										File logTransferPath  = new File(logTransferFilePath)
										if(file.exists()){
											boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
										}
									}
								}
							}
						}
					}
				} catch (Exception e) {
					println  " Error"+e.getMessage()
					e.printStackTrace()
				}
			}
			/**
			 * Function For Tranfer the performance related file using tftp
			 * @param realPath
			 * @param logTransferFilePath
			 * @return
			 */
		
			def copyPerformanceLogIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId){
				try {
					String logsPath = realPath.toString()+"/logs/logs/"
		
					File logDir  = new File(logsPath)
					if(logDir.isDirectory()){
						logDir.eachFile{ file->
							if(file.toString()?.contains("benchmark.log") || file.toString()?.contains("memused.log") || file.toString()?.contains("cpu.log")){
								def logFileName =  file.getName().split("_")
								if(logFileName?.length >= 3){
									if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
										new File(logTransferFilePath?.toString()).mkdirs()
										File logTransferPath  = new File(logTransferFilePath)
										if(file.exists()){
											boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
										}
									}
								}
							}
						}
					}
				} catch (Exception e) {
					println  " Error"+e.getMessage()
					e.printStackTrace()
				}
			}
			
			/**
			 * Function for copy the logs to specified directory
			 */
			def copyLogFileIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId , def fileName){
				try {
					String logsPath = realPath.toString()+"/logs/logs/"
		
					File logDir  = new File(logsPath)
					if(logDir.isDirectory()){
						logDir.eachFile{ file->
							if(file.toString()?.contains(fileName)){
								def logFileName =  file.getName().split("_")
								if(logFileName?.length >= 3){
									if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
										new File(logTransferFilePath?.toString()).mkdirs()
										File logTransferPath  = new File(logTransferFilePath)
										if(file.exists()){
											boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
										}
									}
								}
							}
						}
					}
				} catch (Exception e) {
					println  " Error"+e.getMessage()
					e.printStackTrace()
				}
			}
		
			/**
			 * Function for copy the stblogs from tftp server
			 * @param realPath
			 * @param logTransferFilePath
			 * @param name
			 * @return
			 */
		
			def copyStbLogsIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId){
				try {
					String logsPath = realPath.toString()+"/logs/logs/"
					File logDir  = new File(logsPath)
					if(logDir.isDirectory()){
						logDir.eachFile{ file->
							if(!(file?.toString()?.contains("version.txt") || file.toString()?.contains("benchmark.log") || file.toString()?.contains("memused.log") || file.toString()?.contains("cpu.log") || file?.toString()?.contains("AgentConsoleLog.log"))){
								def logFileName =  file.getName().split("_")
								if(logFileName?.length >= 3){
								if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
										def fName = file.getName()
										fName = fName?.replaceFirst(logFileName[0]+UNDERSCORE+logFileName[1]+UNDERSCORE+logFileName[2]+UNDERSCORE, "" )
										new File(logTransferFilePath?.toString()).mkdirs()
										File logTransferPath  = new File(logTransferFilePath)
										if(file.exists()){
											boolean fileMoved = file.renameTo(new File(logTransferPath,fName.trim()));
										}
									}
								}
							}
						}
					}
				} catch (Exception e) {
					println  " Error"+e.getMessage()
					e.printStackTrace()
				}
			}
		
		
			/**
			 * Function for transfer the open sourse logs from "tftp server
			 * @param realPath
			 * @param logTransferFilePath
			 * @return
			 */
			def copyLogsIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId){
				try {
					String logsPath = realPath.toString()+"/logs/logs/"
					File logDir  = new File(logsPath)
					if(logDir.isDirectory()){
						logDir.eachFile{ file->
							if(!(file?.toString()?.contains("version.txt") || file.toString()?.contains("benchmark.log") || file.toString()?.contains("memused.log") || file.toString()?.contains("cpu.log") || file?.toString()?.contains("AgentConsoleLog.log"))){
								def logFileName =  file.getName().split("_")
								if(logFileName?.length >= 3){
								if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
										if (file.isFile()) {
											String fileName = file.getName()
											fileName = fileName.replaceAll("\\s","")
											if(fileName.toString().contains("\$:")){
												fileName = fileName.replaceAll('\\$:',"Undefined")
											}
											if(fileName.startsWith( logFileName[0] )){
												fileName = fileName.replaceFirst( logFileName[0]+UNDERSCORE+logFileName[1]+UNDERSCORE+logFileName[2]+UNDERSCORE, "" )
												fileName= logFileName[0]+UNDERSCORE+fileName
												new File(logTransferFilePath?.toString()).mkdirs()
												File logTransferPath  = new File(logTransferFilePath)
												if(file.exists()){
													boolean fileMoved = file.renameTo(new File(logTransferPath, fileName.trim()));
												}
											}
										}
									}
								}
							}
						}
					}
				} catch (Exception e) {
					println  " Error"+e.getMessage()
					e.printStackTrace()
				}
			}
			

		
	/** 
	 *  Method to check whether the execution result is having any result update or not.
	 *  Check If execution result  got any update or it is initial status.
	 * @param executionResultId
	 * @return
	 */
	def checkExecutionCompletionStatus(def executionResultId){
		boolean status = true
		ExecutionResult.withTransaction {
			def resultArray = ExecutionResult.executeQuery("select a.status from ExecutionResult a where a.id = :exId",[exId: executionResultId])
			if(resultArray?.size() > 0){
//				if(resultArray[0] == Constants.UNDEFINED_STATUS || resultArray[0] == Constants.PENDING){
//					status = false
//				}
			}
		}
		return status
	}

	/**
	 * Create file to append execution log
	 * @param executionName
	 * @param scriptName
	 * @return
	 */
	private String prepareOutputfile(final String executionName, final String scriptName){
		try {
			def folderName = Constants.SCRIPT_OUTPUT_FILE_PATH
			File folder = grailsApplication.parentContext.getResource(folderName).file
			folder.mkdirs();
			def fileName = folderName+executionName+Constants.SCRIPT_OUTPUT_FILE_EXTN
			File opFile = grailsApplication.parentContext.getResource(fileName).file
			boolean append = true
			FileWriter fileWriter = new FileWriter(opFile, append)
			BufferedWriter buffWriter = new BufferedWriter(fileWriter)
			buffWriter.write("<br/>Executing script : "+scriptName+"<br/>"+NEW_LINE);
			buffWriter.write("======================================<br/>"+NEW_LINE);
			buffWriter.flush()
			buffWriter.close()
			return opFile.getAbsolutePath();
		} catch(Exception ex) {
		}

		return null
	}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def logTransfer(def deviceInstance, def logTransferFilePath, def logTransferFileName, def realPath,  def executionId, def executionDeviceId , def executionResultId , def url){
		Thread.sleep(4000)
		try{			
			
			String scriptName = getConsoleFileTransferScriptName(deviceInstance)
			
			File layoutFolder = grailsApplication.parentContext.getResource(scriptName).file
			def absolutePath = layoutFolder.absolutePath
			def cmdList = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				//deviceInstance?.logTransferPort,
				"AgentConsole.log",
				//logTransferFilePath
				logTransferFileName			
			]
			
			if(scriptName?.equals(CONSOLE_FILE_UPLOAD_SCRIPT)){
				url = executionService.updateTMUrl(url,deviceInstance)
				cmdList.push(url)
			}
			
			String [] cmd = cmdList.toArray()
			
			
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,2)
			copyAgentconsoleLogIntoDir(realPath,logTransferFilePath,executionId,executionDeviceId,executionResultId)
			Thread.sleep(4000)
		}
		catch(Exception e){		
			println " Error "+e.getMessage()	
		}		
	}
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance,String hardReset){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				hardReset
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(4000)
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				FALSE
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(4000)
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def hardResetAgent(def deviceInstance){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				TRUE
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(4000)
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

/**
	 * Re run the tests if the status of script execution is not failure
	 * @param realPath
	 * @param filePath
	 * @param execName
	 * @return
	 */
	def reRunOnFailure(final String realPath, final String filePath, final String execName, final String uniqueExecutionName, final String appUrl, final String category){
		try {
			def newExecName
			def aborted=false
			boolean pause = false
			List pendingScripts = []
			Execution executionInstance = Execution.findByName(execName)
			int executionCount=0
			int execCnt = 0
			int execCount =0
			def executionList = Execution?.findAll()
			if(execName?.toString()?.contains("_RERUN_")){
				def execNameSplitList = execName.toString().split("_RERUN_")
				if(execNameSplitList?.length == 2){
					executionCount =Integer.parseInt(execNameSplitList[1])
					executionCount++
					newExecName =  execNameSplitList[0]+"_RERUN_"+executionCount
					if(executionList?.toString().contains(newExecName?.toString())){
						executionList?.each { exName ->
							if(exName?.toString().contains(execNameSplitList[0]?.toString())){
								execCount++
							}
						}
						newExecName = execNameSplitList[0]+"_RERUN_"+(execCount)
					}else{
						newExecName =newExecName
					}
				}else{
					newExecName  = execName
					//	if(Execution?.findByName(execName?.toString())){
					if(executionList?.toString().contains(execName?.toString())){
						def lastExecname  = executionList.find{ it  ->
							it?.toString().contains(execName?.toString())
						}
						def newExecNameList = lastExecname.toString().tokenize("_")
						execCnt = Integer.parseInt(newExecNameList[2])
						execCnt++
						newExecName = execName+"_"+execCnt
					}
				}
			}else{
				newExecName = execName +"_RERUN_"+1
				if( Execution.findByName(newExecName?.toString() )){
					def lastExecname  = executionList.find{ it  ->
						it?.toString().contains(execName?.toString())
					}
					
					if(lastExecname?.toString()?.contains("_RERUN_")){
						def newExecNameList = lastExecname.toString().split("_RERUN_")
						if(newExecNameList?.length == 2){
							execCnt = Integer.parseInt(newExecNameList[1])
							execCnt++
							newExecName = execName+"_RERUN_"+(execCnt)
						}
					}
				}else{
					newExecName= newExecName
				}
			}


			def exeId = executionInstance?.id
			def resultArray = Execution.executeQuery("select a.result from Execution a where a.name = :exName",[exName: execName])
			def result = resultArray[0]

			Execution rerunExecutionInstance
			def executionSaveStatus = true
			if(result != SUCCESS_STATUS){
				def scriptName
				def scriptGroupInstance = ScriptGroup.findByName(executionInstance?.scriptGroup)
				/**
				 * Get all devices for execution
				 */
				def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
				int cnt = 0
				executionDeviceList.each{ execDeviceInstance ->
					if(execDeviceInstance.status != SUCCESS_STATUS){
						Device deviceInstance = Device.findByStbName(execDeviceInstance?.device)

						String status1 = ""
						boolean allocated = false
						try {
							status1 = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
							synchronized (lock) {
								if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
									status1 = "BUSY"
								}else{
									if((status1.equals( Status.FREE.toString() ))){
										if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
											allocated = true
											executionService.deviceAllocatedList.add(deviceInstance?.id)
											Thread.start{
												deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
											}
										}
									}
								}
							}

						}
						catch(Exception eX){
							println  " ERROR "+ eX.printStackTrace()
						}
						def executionResultList
						ExecutionResult.withTransaction {
							executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
						}


						def resultSize = executionResultList.size()
						if(cnt == 0){
							scriptName = executionInstance?.script
							def deviceName = deviceInstance?.stbName
							if(executionDeviceList.size() > 1){
								deviceName = MULTIPLE
							}
							//executionSaveStatus = executionService.saveExecutionDetails(newExecName, scriptName, deviceName, scriptGroupInstance,appUrl,"false","false","false","false",category])
							executionSaveStatus = executionService.saveExecutionDetails(newExecName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance,appUrl:appUrl, isBenchMark:"false", isSystemDiagnostics:"false", rerun:"false", isLogReqd:"false",category:category, rerunOnFailure:FALSE])
							cnt++
							Execution.withTransaction{
								rerunExecutionInstance = Execution.findByName(newExecName)
							}
						}
						if(executionSaveStatus){
							ExecutionDevice executionDevice
							ExecutionDevice.withTransaction {
								executionDevice = new ExecutionDevice()
								executionDevice.execution = rerunExecutionInstance
								executionDevice.device = deviceInstance?.stbName
								executionDevice.deviceIp = deviceInstance?.stbIp
								executionDevice.dateOfExecution = new Date()
								executionDevice.status = UNDEFINED_STATUS
								executionDevice.category = Utility.getCategory(category)
								executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
								executionDevice.save(flush:true)
							}
							executionService.executeVersionTransferScript(realPath, filePath, newExecName, executionDevice?.id, deviceInstance.stbName, deviceInstance?.logTransferPort,appUrl)
							def scriptInstance
							def htmlData

							int counter = 0
							def isMultiple = TRUE
							// adding log transfer to server for reruns
							Properties props = new Properties()
							try {
								// initiating log transfer
								if(executionResultList.size() > 0){
									LogTransferService.transferLog(newExecName, deviceInstance)
								}
							} catch (Exception e) {
								e.printStackTrace()
							}
							def executionName = Execution?.findByName(newExecName)
							executionResultList.each{ executionResult ->
								if(!executionResult.status.equals(SKIPPED)){
									//	scriptInstance = Script.findByName(executionResult?.script)
									def scriptFile = ScriptFile.findByScriptName(executionResult?.script)
									scriptInstance = scriptService.getScript(realPath,scriptFile?.moduleName,scriptFile?.scriptName, category)
									counter ++
									if(counter == resultSize){
										isMultiple = FALSE
									}
									def deviceStatus = " "
									try{
										deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
									}catch (Exception e){
										e.getMessage()
									}
									
									if(scriptInstance){
										String rdkVersion = executionService.getRDKBuildVersion(deviceInstance) 
										if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance) && executionService.validateScriptRDKVersions(scriptInstance,rdkVersion) ){
											def startExecutionTime = new Date()
											//aborted = executionService.abortList.contains(exeId?.toString())
											aborted = executionService.abortList?.toString().contains(executionName?.id?.toString())
											if(!aborted && !(deviceStatus?.toString().equals(Status.NOT_FOUND.toString()) || deviceStatus?.toString().equals(Status.HANG.toString())) && !pause){
												htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, appUrl, filePath, realPath,"false","false",uniqueExecutionName,isMultiple,null,"false", category)
											}else{
												if(!aborted && (deviceStatus.equals(Status.NOT_FOUND.toString()) ||  deviceStatus.equals(Status.HANG.toString()))){
													pause = true
												}
												if(!aborted && pause) {
													try {
														pendingScripts.add(scriptInstance)
														def execInstance
														Execution.withTransaction {
															def execInstance1 = Execution.findByName(newExecName)
															execInstance = execInstance1
														}
														def scriptInstanceObj
														//							Script.withTransaction {
														//							Script scriptInstance1 = Script.findById(scriptObj.id)
														scriptInstanceObj = scriptInstance
														//							}
														Device deviceInstanceObj
														def devId = deviceInstance?.id
														Device.withTransaction {
															Device deviceInstance1 = Device.findById(devId)
															deviceInstanceObj = deviceInstance1
														}
														ExecutionDevice executionDevice1
														ExecutionDevice.withTransaction {
															def exDev = ExecutionDevice.findById(executionDevice?.id)
															executionDevice1 = exDev
														}
														ExecutionResult.withTransaction { resultstatus ->
															try {
																def executionResult1 = new ExecutionResult()
																executionResult1.execution = execInstance
																executionResult1.executionDevice = executionDevice1
																executionResult1.script = scriptInstanceObj?.name
																executionResult1.device = deviceInstanceObj?.stbName
																executionResult1.execDevice = null
																executionResult1.deviceIdString = deviceInstanceObj?.id?.toString()
																executionResult1.status = PENDING
																executionResult1.dateOfExecution = new Date()
																executionResult1.category=Utility.getCategory(executionDevice1?.category?.toString())
																if(! executionResult1.save(flush:true)) {
																}
																resultstatus.flush()
															}
															catch(Throwable th) {
																resultstatus.setRollbackOnly()
															}
														}
													} catch (Exception e) {
													}
												}

											}
											def endExecutionTime = new Date()
											executionTimeCalculation(newExecName,startExecutionTime,endExecutionTime)
										}
									}
									
								}
							}
							try {
								// stopping log transfer
								if(executionResultList.size() > 0){
									LogTransferService.closeLogTransfer(newExecName)
								}
							} catch (Exception e) {
								e.printStackTrace()
							}
							if(aborted && executionService.abortList.contains(executionName?.id?.toString())){
								executionService.abortList.remove(executionName?.id?.toString())
							}
							Execution executionInstance1 = Execution.findByName(newExecName)
							if(!aborted && pause && pendingScripts.size() > 0 ){			
								executionService.savePausedExecutionStatus(executionInstance1?.id)
								executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
							}
							if(!aborted && !pause){
								executionService.saveExecutionStatus(aborted,executionInstance1?.id)								
							}							
						}
						if(allocated && executionService.deviceAllocatedList.contains(deviceInstance?.id)){
							executionService.deviceAllocatedList.remove(deviceInstance?.id)
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Called from REST API : To save the result details
	 * @param executionId
	 * @param resultData
	 * @return
	 */

	def saveExecutionResultStatus(final String execId, final String resultData, final String execResult,
			final String expectedResult, final String resultStatus, final String testCaseName, final String execDevice)
	{
		try{
			if(resultData){
				String actualResult = resultData
				if(actualResult){
					ExecutionResult.withTransaction {
						ExecutionResult executionResult = ExecutionResult.findById(execResult)

						ExecuteMethodResult executionMethodResult = new ExecuteMethodResult()
						if(resultStatus.equals( STATUS_NONE ) || resultStatus == null ){
							executionMethodResult.status = actualResult
						}
						else{
							executionMethodResult.executionResult = executionResult
							executionMethodResult.expectedResult = expectedResult
							executionMethodResult.actualResult = actualResult
							executionMethodResult.status = resultStatus
						}
						executionMethodResult.functionName = testCaseName
						executionMethodResult.save(flush:true)

						executionResult.addToExecutemethodresults(executionMethodResult)
						executionResult.save(flush:true)

						Execution execution = Execution.findById(execId)
						ExecutionDevice execDeviceInstance = ExecutionDevice.findById(execDevice)
						if(!executionResult.status.equals( FAILURE_STATUS )){
							executionResult.status = resultStatus
							executionResult.save(flush:true)
							if(!execution.result.equals( FAILURE_STATUS )){
								execution.result = resultStatus
								execution.save(flush:true)
							}
							if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
								execDeviceInstance.addToExecutionresults(executionResult)
								execDeviceInstance.status = resultStatus
								execDeviceInstance.save(flush:true)
							}
						}
					}
				}
			}
			else{
				Execution.withTransaction {
					Execution execution = Execution.findById(execId)
					execution.result = FAILURE_STATUS
					execution.save(flush:true)
				}
			}
		}catch(Exception ex){
			ex.printStackTrace()
		}

	}

	/**
	 *  Called from REST API : To save the load module status
	 * @param executionId
	 * @param resultData
	 * @return
	 */
	def saveLoadModuleStatus(final String execId, final String statusData, final String execDevice, final String execResult){

		Execution.withTransaction{
			Execution execution = Execution.findById(execId)
			if(execution && !(execution?.result?.equals( FAILURE_STATUS ))){
				execution?.result = statusData?.toUpperCase().trim()
				execution?.save(flush:true)
			}

			ExecutionDevice execDeviceInstance = ExecutionDevice.findByExecutionAndId(execution,execDevice)
			if(execDeviceInstance && !(execDeviceInstance?.status.equals( FAILURE_STATUS ))){
				execDeviceInstance?.status = statusData?.toUpperCase().trim()
				execDeviceInstance?.save(flush:true)
			}

			ExecutionResult executionResult = ExecutionResult.findById(execResult)
			if(executionResult && !(executionResult?.status.equals( FAILURE_STATUS ))){
				executionResult?.status = statusData?.toUpperCase().trim()
				executionResult?.save(flush:true)
			}
		}
	}

	
	/**
	 * To calculate the total execution time and updating the data base 
	 * @param execName
	 * @param startExecutionTime
	 * @param endExecutionTime
	*/
	def executionTimeCalculation(String execName, Date startExecutionTime, Date endExecutionTime)
	{
		try
		{	
			def totalSecTime 
			Execution executionInstance1 = Execution.findByName(execName)
			def totalTimeArray = Execution.executeQuery("select a.realExecutionTime from Execution a where a.name = :exName",[exName: execName])	
			def execTimeDiff = (endExecutionTime.getTime() - startExecutionTime.getTime())/1000;
			/* Calculating and formatting the total execution time */
			if(totalTimeArray){
				totalSecTime = calculateTotalExecutiontime(totalTimeArray[0], execTimeDiff )
			}else{
				totalSecTime = calculateTotalExecutiontime(totalTimeArray, execTimeDiff )
			}
			def execTimeDifference = convertExecutionTimeFormat(totalSecTime )
			executionService.updateTotalExecutionTime(execTimeDifference ?.toString(), executionInstance1?.id)
		}catch (Exception e) {
			println  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}

	/**
	 * Execute scripts on Device
	 * @param execName
	 * @param device
	 * @param executionDevice
	 * @param scripts
	 * @param scriptGrp
	 * @param executionName
	 * @param filePath
	 * @param realPath
	 * @param groupType
	 * @param url
	 * @param isBenchMark
	 * @param isSystemDiagnostics
	 * @param rerun
	 * @return
	 */
	def executescriptsOnDevice(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun,def isLogReqd, def category)
	{
		boolean aborted = false
		boolean pause = false
		def htmlData = ""
		Device deviceInstance
		Execution executionInstance1 = Execution.findByName(execName)
		def executionResultId = executionInstance1?.id
		def deviceId
		
		try{
			
		def scriptInstance
		Device.withTransaction {
			deviceInstance= Device.findById(device)
		}
		deviceId = deviceInstance?.id
		ScriptGroup scriptGroupInstance
		StringBuilder output = new StringBuilder();
		int scriptGrpSize = 0
		int scriptCounter = 0
		def isMultiple = TRUE
		List pendingScripts = []

		if(groupType == TEST_SUITE){
			scriptCounter = 0
			boolean skipStatus = false
			boolean notApplicable = false
			List validScriptList = new ArrayList()
			String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);

			ScriptGroup.withTransaction { trans ->
				scriptGroupInstance = ScriptGroup.findById(scriptGrp)
				scriptGroupInstance?.scriptList?.each { script ->
				def scriptInstance1 = scriptService.getScript(realPath,script?.moduleName, script?.scriptName, category)
				if(scriptInstance1){
					if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
						if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
						if(scriptInstance1?.skip?.toString().equals("true")){
							skipStatus = true
							executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance1, deviceInstance, category)
							}else{
								validScriptList << scriptInstance1
							}
						}else{
							notApplicable = true
							String rdkVersionData = ""

//							Script.withTransaction {
//								def scriptInstance2 = Script.findById(script?.id)
								rdkVersionData = scriptInstance1?.rdkVersions
//							}

							String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
							executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance1, deviceInstance,reason, category)
						}
					}else{
					
						notApplicable = true
						String boxTypeData = ""

						String deviceBoxType = ""

						Device.withTransaction {
							Device dev = Device.findById(deviceInstance?.id)
							deviceBoxType = dev?.boxType
						}

//						Script.withTransaction {
//							def scriptInstance1 = Script.findById(script?.id)
							boxTypeData = scriptInstance1?.boxTypes
//						}

						String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
						executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance1, deviceInstance,reason, category)
					}
				}else{
				
				String reason = "No script is available with name :"+script?.scriptName+" in module :"+script?.moduleName
				executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script?.scriptName, deviceInstance,reason, category)
				
				}
				}
			}

			scriptGrpSize = validScriptList?.size()
			Execution ex = Execution.findByName(execName)
			def exeId = ex?.id
			
			if((skipStatus || notApplicable)&& scriptGrpSize == 0){
				executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, exeId)
				executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, executionDevice?.id)
			}
			
			
			boolean executionStarted = false
			
			//Properties props = new Properties()
			
			try {
				// rest call for log transfer starts
				
				if(validScriptList.size() > 0){
					LogTransferService.transferLog(execName, deviceInstance)
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
			validScriptList.each{ scriptObj ->
				
				executionStarted = true
				scriptCounter++
				if(scriptCounter == scriptGrpSize){
					isMultiple = FALSE
				}
				aborted = executionService.abortList.contains(exeId?.toString())
				
				String devStatus = ""
				if(!pause && !aborted){
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						/*Thread.start{
							deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
						}*/
						if(devStatus.equals(Status.HANG.toString())){
							resetAgent(deviceInstance, TRUE)
							Thread.sleep(6000)
							devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						}
					}
					catch(Exception eX){
					}
				}
				if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString())) && !pause){
					executionStarted = true
					def startExecutionTime = new Date()
					try {
						htmlData = executeScript(execName, executionDevice, scriptObj, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics, executionName, isMultiple,null,isLogReqd, category)

					} catch (Exception e) {
					
						e.printStackTrace()
					}
					output.append(htmlData)
					Thread.sleep(6000)
					def endExecutionTime = new Date()
					executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
				}else{
				
					if(!aborted && (devStatus.equals(Status.NOT_FOUND.toString()) ||  devStatus.equals(Status.HANG.toString()))){
						pause = true
					}

					if(!aborted && pause) {
						try {
							pendingScripts.add(scriptObj)
							def execInstance
							Execution.withTransaction {
								def execInstance1 = Execution.findByName(execName)
								execInstance = execInstance1
							}
							def scriptInstanceObj
//							Script.withTransaction {
//							Script scriptInstance1 = Script.findById(scriptObj.id)
							scriptInstanceObj = scriptObj
//							}
							Device deviceInstanceObj
							def devId = deviceInstance?.id
							Device.withTransaction {
								Device deviceInstance1 = Device.findById(devId)
								deviceInstanceObj = deviceInstance1
							}
							ExecutionDevice executionDevice1
							ExecutionDevice.withTransaction {
								def exDev = ExecutionDevice.findById(executionDevice?.id)
								executionDevice1 = exDev
							}
							
							ExecutionResult.withTransaction { resultstatus ->
							try {
								def executionResult = new ExecutionResult()
								executionResult.execution = execInstance
								executionResult.executionDevice = executionDevice1								
								executionResult.script = scriptInstanceObj?.name
								//executionResult.script = script?.name 								
								executionResult.device = deviceInstanceObj?.stbName
								executionResult.execDevice = null
								executionResult.deviceIdString = deviceInstanceObj?.id?.toString()
								executionResult.status = PENDING
								executionResult.dateOfExecution = new Date()
								executionResult.category = Utility.getCategory(category)
								if(! executionResult.save(flush:true)) {
								}
								resultstatus.flush()
							}
							catch(Throwable th) {
								resultstatus.setRollbackOnly()
							}
							}
						} catch (Exception e) {
						}

					}
				}
			}
			
				if(validScriptList.size() > 0){
					LogTransferService.closeLogTransfer(execName)
				}
			
			if(aborted && executionService.abortList.contains(exeId?.toString())){
				executionService.abortList.remove(exeId?.toString())
			}

			if(!aborted && pause && pendingScripts.size() > 0 ){
				def exeInstance = Execution.findByName(execName)
				executionService.savePausedExecutionStatus(exeInstance?.id)
				executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
//				ExecutionDevice.withTransaction {
//					ExecutionDevice exDevice = ExecutionDevice.findById(idd)
//					exDevice.status = PAUSED
//					exDevice.save();
//				}
			}
		}
		else if(groupType == SINGLE_SCRIPT){

			println " [ScriptName="+scripts + "] [Device="+deviceInstance?.stbName+"] [execName="+execName+"]"
			
			if(scripts instanceof String){
				def moduleName= scriptService.scriptMapping.get(scripts)
				def script1 = scriptService.getScript(realPath,moduleName, scripts, category)
				isMultiple = FALSE
				def startExecutionTime = new Date()
				try {
					htmlData = executeScript(execName, executionDevice, script1, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics,executionName,isMultiple,null,isLogReqd, category)
					
				def exeInstance = Execution.findByName(execName)
				if(executionService.abortList.contains(exeInstance?.id?.toString())){
					aborted = true
					executionService.abortList.remove(exeInstance?.id?.toString())
				}
				} catch (Exception e) {
					e.printStackTrace()
				}
				def endExecutionTime = new Date()
				executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
				output.append(htmlData)
			}
			else{
				scriptCounter = 0
				List validScripts = new ArrayList()
				String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
				boolean notApplicable = false
				boolean skipStatus = false
					scripts.each { script ->
//						scriptInstance = Script.findById(script,[lock: true])
						def moduleName= scriptService.scriptMapping.get(script)
						if(moduleName){
						scriptInstance = scriptService.getScript(realPath,moduleName,script, category)
						if(scriptInstance){
						if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance)){
							if(executionService.validateScriptRDKVersions(scriptInstance,rdkVersion)){
								if(scriptInstance?.skip?.toString().equals("true")){
									skipStatus = true
									executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,category)
								}else{
									validScripts << scriptInstance
								}
							}else{
								notApplicable = true
								String rdkVersionData = ""
								rdkVersionData = scriptInstance?.rdkVersions

								String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
								executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason,category)
							}
						}else{
							notApplicable = true
							String boxTypeData = ""

							String deviceBoxType = ""

							Device.withTransaction {
								Device dev = Device.findById(deviceInstance?.id)
								deviceBoxType = dev?.boxType
							}
								boxTypeData = scriptInstance?.boxTypes

							String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
							executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason, category)
						}
						}else{
				
							String reason = "No script is available with name :"+script+" in module :"+moduleName
								executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason, category)
				
						}
					}else{
				
					String reason = "No module information is present for script :"+script
					executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason, category)
				
				}
					}
				scriptGrpSize = validScripts?.size()
				Execution ex = Execution.findByName(execName)
				def exeId = ex?.id
				if((skipStatus || notApplicable)&& scriptGrpSize == 0){
					executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, exeId)
					executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, executionDevice?.id)
				}
				String devStatus = ""
					validScripts.each{ script ->
						scriptCounter++
						if(scriptCounter == scriptGrpSize){
							isMultiple = FALSE
						}
						def startExecutionTime = new Date()
						try {
							// This code for issue fix . while  selecting multiple script the  box is not up then the pending script not executed
							aborted = executionService.abortList.contains(exeId?.toString())							
							devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)	
							
							if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString()))){								
							
								try{
									htmlData = executeScript(execName, executionDevice, script, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics,executionName,isMultiple,null,isLogReqd,category )
								}catch(Exception e){
									e.printStackTrace()
								}
								

							}else 	{
								if(!aborted && devStatus.equals(Status.NOT_FOUND.toString())){
									pause = true
								}

								if(!aborted && pause) {
									try {
										pendingScripts.add(script)
										def execInstance
										Execution.withTransaction {
											def execInstance1 = Execution.findByName(execName)
											execInstance = execInstance1
										}
										Script scriptInstanceObj
										scriptInstanceObj = scriptInstance
										Device deviceInstanceObj
										def devId = deviceInstance?.id
										Device.withTransaction {
											Device deviceInstance1 = Device.findById(devId)
											deviceInstanceObj = deviceInstance1
										}
										ExecutionDevice executionDevice1
										ExecutionDevice.withTransaction {
											def exDev = ExecutionDevice.findById(executionDevice?.id)
											executionDevice1 = exDev
										}

										ExecutionResult.withTransaction { resultstatus ->
											try {
												def executionResult = new ExecutionResult()
												executionResult.execution = execInstance
												executionResult.executionDevice = executionDevice1
												//executionResult.script = scriptInstanceObj?.name
												executionResult.script = script.name
												executionResult.device = deviceInstanceObj?.stbName
												executionResult.execDevice = null
												executionResult.deviceIdString = deviceInstanceObj?.id?.toString()
												executionResult.status = PENDING
												executionResult.dateOfExecution = new Date()
												executionResult.category = Utility.getCategory(category)
												if(! executionResult.save(flush:true)) {
												}
												resultstatus.flush()
											}
											catch(Throwable th) {
												resultstatus.setRollbackOnly()
											}
										}
									} catch (Exception e) {
										e.printStackTrace()

									}
								}
							}
							if(!aborted && pause && pendingScripts.size() > 0 ){
								def exeInstance = Execution.findByName(execName)
								executionService.savePausedExecutionStatus(exeInstance?.id)
								executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
							}
						} catch (Exception e) {
							e.printStackTrace()
						}
			
						
						output.append(htmlData)
						Thread.sleep(6000)
						def endExecutionTime = new Date()
						executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
					}
					if(aborted && executionService.abortList.contains(exeId?.toString())){
						executionService.abortList.remove(exeId?.toString())
					}
			}
		}

		
		
		if(!pause){
			executionService.saveExecutionStatus(aborted, executionInstance1?.id)
		}
		htmlData = ""

		if(!aborted && !pause){

			def executionDeviceObj1
			ExecutionDevice.withTransaction{ wthTrans ->
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)
				executionDeviceObj1 = executionDeviceObj
			}

				if((executionDeviceObj1) && ((rerun?.toString().equals("true")) || (rerun?.toString().equals("on")))){
				htmlData = reRunOnFailure(realPath,filePath,execName,executionName,url, category)
				output.append(htmlData)
			}

		}else{
			resetAgent(deviceInstance)
		}
		deleteOutputFile(executionName)
		htmlData = output.toString()
		
		}
		catch(Exception ex){
			println "Error "+ex.getMessage()
		}
		finally{

			try {
				
				removeBusyLock(deviceId)

				String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				Thread.start{
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
				}

				Thread.sleep(2000);

				Device devv = Device.get(deviceId)
				println "["+ deviceInstance?.stbName+"] ["+  devStatus + "] ["+devv?.deviceStatus+"]"+" [execName="+execName+"]"

				if(executionService.deviceAllocatedList?.contains(deviceId)){
					println " Device instance is still there in the allocated list :  "+deviceInstance?.stbName + " id "+ deviceInstance?.id +" [execName="+execName+"]"+ " deviceAllocatedList "+executionService.deviceAllocatedList
					removeBusyLock(deviceId)
					devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					Thread.start{
						deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
					}
					println " Again checking the device lock  for "+deviceInstance?.stbName + " status =  "+executionService.deviceAllocatedList.contains(deviceInstance?.id)
				}
			} catch (Exception e) {
				println " Error "+e.getMessage()
				e.printStackTrace()
			}

		}
		
		return htmlData
	}

	private void removeBusyLock(def deviceId ){
		try {
			if(executionService.deviceAllocatedList?.contains(deviceId)){
				println " removeBusyLock "+deviceId+" status "+executionService.deviceAllocatedList?.removeAll(deviceId)
			}
		} catch (Exception e) {
			println " removeBusyLock Error "+e.getMessage()
			e.printStackTrace()
		}
	}
	
	/**
	 * Deletes the file created to store execution log
	 * @param opFileName
	 */
	private void deleteOutputFile(String opFileName){
		try{
			def fileName = Constants.SCRIPT_OUTPUT_FILE_PATH+opFileName+Constants.SCRIPT_OUTPUT_FILE_EXTN
			File opFile = grailsApplication.parentContext.getResource(fileName).file
			if(opFile.exists()){
				opFile.delete();
			}
		}catch(Exception e){
			e.printStackTrace();
		}
	}

	/**
	 * Calls when the execution of scripts is targeted on multiple devices.
	 * Scripts will be executed on multiple devices concurrently.
	 * @param execName
	 * @param device
	 * @param executionDevice
	 * @param scripts
	 * @param scriptGrp
	 * @param executionName
	 * @param filePath
	 * @param realPath
	 * @param groupType
	 * @param url
	 * @param isBenchMark
	 * @param isSystemDiagnostics
	 * @param rerun
	 * @return
	 */
	def executeScriptInThread(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun,def isLogReqd, def category){

		Future<String> future =  executorService.submit( {
			executescriptsOnDevice(execName, device, executionDevice, scripts, scriptGrp,
					executionName, filePath, realPath, groupType, url, isBenchMark, isSystemDiagnostics, rerun,isLogReqd, category)} as Callable< String > )
		
	}
			
	def executeRepeatScriptInThread(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun,def isLogReqd,int repeat){

		Future<String> future =  executorService.submit( {

			for (int i=0;i<repeat;i++){
				executescriptsOnDevice(execName, device, executionDevice, scripts, scriptGrp,
						executionName, filePath, realPath, groupType, url, isBenchMark, isSystemDiagnostics, rerun,isLogReqd)
			}} as Callable< String > )

	}


	/**
	 * Restart the script execution in case of device unavailablity
	 * @param execDevice
	 * @param grailsApplication
	 */
	public boolean restartExecution(ExecutionDevice execDevice, def grailsApplication){
		String htmlData = ""
		StringBuilder output = new StringBuilder()
		int scriptCounter = 0
		boolean pause = false
		String url = ""
		boolean aborted = false
		try {
			def rootFolder = grailsApplication.parentContext.getResource("/").file
			String rootPath = rootFolder.absolutePath
			String filePath = rootPath + "//fileStore"
			String realPath = rootPath
			def exId
			def exResults
			def eId = execDevice?.id
			ExecutionDevice.withTransaction {
				ExecutionDevice exDevice =  ExecutionDevice.findById(eId)
				exResults = exDevice?.executionresults
				exId = exDevice?.execution?.id
			}
			Execution execution
			boolean thirdParyExecution = false
			def thirdPartyExecutionDetails
			Execution.withTransaction {
				execution = Execution.findById(exId)
				thirdPartyExecutionDetails = execution?.thirdPartyExecutionDetails
				thirdParyExecution = (thirdPartyExecutionDetails != null)
			}
			ExecutionResult.withTransaction {
				exResults =  ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatus(execution,execDevice,PENDING)
			}
			Device deviceInstance
			url = execution?.applicationUrl
			String exName = execution?.name
			executionService.updateExecutionStatusData(INPROGRESS_STATUS, execution?.id)
			String isMultiple = TRUE
			int totalSize = exResults.size()

			Properties props = new Properties()
			try {
				def device = null
				def exeDev = null
				ExecutionDevice.withTransaction {
					exeDev = ExecutionDevice.findByExecution(execution)
					device = Device.findByStbIp(exeDev?.deviceIp)
				}
				LogTransferService.transferLog(exName, Device.findByStbIp(exeDev?.deviceIp))

			} catch (Exception e) {
				e.printStackTrace()
			}
			boolean tclScript = false // for validate TCL script or not
			boolean validScript = false
			exResults.each {
				try {
					scriptCounter++
					if(scriptCounter == totalSize){
						isMultiple = FALSE
					}
					def idVal = it?.id
					ExecutionResult.withTransaction {
						def exResult = ExecutionResult.findById(idVal)
						if(exResult?.status.equals(PENDING)){							
							Device executionDevice = Device.findById(exResult?.deviceIdString)
							aborted = executionService.abortList.contains(exId?.toString())
							deviceInstance = executionDevice
							def combinedScript = [:]
							if(exResult?.category?.toString()?.equals(Category?.RDKV?.toString()) || exResult?.category?.toString()?.equals(Category?.RDKB?.toString())){
								tclScript  = false
							}else if(exResult?.category?.toString()?.equals(Category?.RDKB_TCL?.toString())){
								tclScript  = true
							}
							def scriptFile =ScriptFile.findByScriptName(exResult?.script)
							def script1
							if(tclScript){
								boolean tclCombined = false
								def combainedTclScript =  ScriptService?.combinedTclScriptMap
								def newScriptName  = ""
								combainedTclScript?.each{
									if(it?.value?.toString()?.contains(exResult?.script.toString())){
										newScriptName = it.key?.toString()
										tclCombined = true
									}
								}
								if(tclCombined){
									newScriptName= newScriptName
								}else{
									newScriptName = exResult?.script?.toString()							
								}
								if(Utility.isTclScriptExists(rootPath?.toString(), newScriptName?.toString())){								
									if(Utility?.isConfigFileExists(rootPath, deviceInstance?.stbName)){
										if(tclCombined){
											combinedScript.put("scriptName", exResult?.script?.toString())
										}else{
											combinedScript.put("scriptName","")
										}									
										validScript = true
									}
								}
								scriptFile = ScriptFile?.findByScriptName(newScriptName) 								
							}else{
								script1=scriptService.getScript(realPath,scriptFile?.moduleName,scriptFile?.scriptName, scriptFile?.category.toString())
								if(executionService.validateScriptBoxTypes(script1,executionDevice)){
									validScript = true
								}
							}
							if(validScript){
								aborted = executionService.abortList.contains(exId?.toString())
								String devStatus = ""
								if(!pause && !aborted){
									try {										
										devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, executionDevice)
										Thread.start{
											deviceStatusService.updateDeviceStatus(executionDevice, devStatus)
										}
										if(devStatus.equals(Status.HANG.toString())){
											resetAgent(deviceInstance, TRUE)
											Thread.sleep(6000)
											devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
										}
									}
									catch(Exception eX){
									}
								}
								if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString()))&& !pause){
									
									def startExecutionTime = new Date()
									// ISSUE FIX related to restart execution not happening append category at the end.
									if(!tclScript){
										htmlData = executeScript(exResult?.execution?.name, execDevice, script1 , executionDevice , url, filePath, realPath ,execution?.isBenchMarkEnabled.toString(), execution?.isSystemDiagnosticsEnabled?.toString(),exResult?.execution?.name,isMultiple,exResult,execution?.isStbLogRequired, scriptFile?.category?.toString())
									}else{	// For TCL script execution																		
										htmlData = tclExecutionService?.executeScript(exResult?.execution?.name, execDevice, scriptFile , executionDevice , url, filePath, realPath ,execution?.isBenchMarkEnabled.toString(), execution?.isSystemDiagnosticsEnabled?.toString(),exResult?.execution?.name,isMultiple?.toString(),exResult,execution?.isStbLogRequired, execution?.category,combinedScript)
										
									}
									output.append(htmlData)
									if(!thirdParyExecution){
										Thread.sleep(6000)										
										def endExecutionTime = new Date()
										executionTimeCalculation(exResult?.execution?.name,startExecutionTime,endExecutionTime)
										
									}
									
								}else{
									if(!aborted){
										pause = true
										def exeInstance = Execution.findByName(exResult.execution.name)
										ExecutionDevice.withTransaction {
											def exDev = ExecutionDevice.findById(execDevice?.id)
											exDev.status = PAUSED
											exDev.save(flush:true)
										}
										if(exeInstance){
											executionService.updateExecutionStatusData(PAUSED, exeInstance.id);
										}
									}
								}
								//}
							}else{
								String reason = "No script is available with name :"+scriptFile?.scriptName+" in module :"+scriptFile?.moduleName
								executionService.saveNoScriptAvailableStatus(Execution.findByName(exResult?.execution?.name), executionDevice, scriptFile?.scriptName, deviceInstance,reason, exResult?.category) // Issue fix 
							}
						}
					}
				} catch (Exception e) {
					e.printStackTrace()
				}
			}

			try {
				LogTransferService.closeLogTransfer(exName)
			} catch (Exception e) {
				e.printStackTrace()
			}

			if(aborted && executionService.abortList.contains(execution?.id?.toString())){
				String dat = execution?.id?.toString()+","
				executionService.abortList.remove(execution?.id?.toString())
			}

			if(!pause){
				Execution executionInstance1 = Execution.findByName(exName)
				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
			}

			//		if(!aborted && !pause){
			//
			//			def executionDeviceObj1
			//			boolean rerun = false
			//			  ExecutionDevice.withTransaction{ wthTrans ->
			//
			//				  def executionObj = Execution.findByName(exName)
			//				  println " execcc "+executionObj
			//				  println "executionObj?.isRerunRequired "+executionObj?.isRerunRequired
			//				  def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)
			//				  executionDeviceObj1 =  executionDeviceObj
			//				  rerun  	= executionObj?.isRerunRequired
			//				    }
			////			  if((executionDeviceObj1) && rerun ){
			////				  htmlData = reRunOnFailure(realPath,filePath,exName,exName,url)
			//////					  output.append(htmlData)
			////			  }
			//		  }

			if(aborted && deviceInstance ){
				resetAgent(deviceInstance)
			}

			if(!aborted && thirdPartyExecutionDetails && !pause){
				ThirdPartyExecutionDetails.withTransaction {
					scriptexecutionService.executeCallBackUrl(thirdPartyExecutionDetails.execName,thirdPartyExecutionDetails.url,thirdPartyExecutionDetails.callbackUrl,thirdPartyExecutionDetails.filePath,thirdPartyExecutionDetails.executionStartTime,thirdPartyExecutionDetails.imageName,thirdPartyExecutionDetails.boxType,realPath)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}finally{
			//			if(!pause){
			//				Execution executionInstance1 = Execution.findByName(exName)
			//				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
			//			}
		}
		return pause;	
	}
	
	/**
	 * Method to trigger the complete repeat execution
	 * @param execution
	 * @param execName
	 * @param grailsApplication
	 * @param deviceName
	 * @return
	 */
	public boolean triggerRepeatExecution(Execution execution , String execName , def grailsApplication,String deviceName){
		def scriptName = execution.script
//		def deviceName = execution.device
		def scriptGroup = execution.scriptGroup
		def url = execution.applicationUrl
		def groups = execution?.groups
		def isBenchMark = execution.isBenchMarkEnabled ? "true" : "false"
		def isSystemDiagnostics = execution.isSystemDiagnosticsEnabled ? "true" : "false"
		def isLogReqd = execution.isStbLogRequired ? "true" : "false"
		def rerun = execution.isRerunRequired ? "true" : "false"
		def htmlData
		int scriptCnt
		def scriptGroupInstance 
		ScriptGroup.withTransaction {
			scriptGroupInstance= ScriptGroup.findByName(scriptGroup)
			scriptCnt= scriptGroupInstance?.scriptList?.size()
		}
		def rootFolder = grailsApplication.parentContext.getResource("/").file
		String rootPath = rootFolder.absolutePath
		String filePath = rootPath + "//fileStore"
		String realPath = rootPath
		def deviceInstance 
		Device.withTransaction {
			deviceInstance = Device.findByStbName(deviceName)
		}
		
		boolean paused = false

		boolean executionSaveStatus 
		
			executionSaveStatus = saveRepeatExecutionDetails(execName, "", deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun,groups,scriptCnt,isLogReqd)
		
		def executionDevice
		if(executionSaveStatus){
			try{
				ExecutionDevice.withTransaction {
					executionDevice = new ExecutionDevice()
					executionDevice.execution = Execution.findByName(execName)
					executionDevice.dateOfExecution = new Date()
					executionDevice.device = deviceInstance?.stbName
					executionDevice.deviceIp = deviceInstance?.stbIp
					executionDevice.status = UNDEFINED_STATUS
					executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
					executionDevice.save(flush:true)
				}
			}
			catch(Exception e){
				e.printStackTrace()
			}
			
			def scriptId
			String deviceID = deviceInstance?.id
			executionService.executeVersionTransferScript(realPath,filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
			try {
				htmlData = repeatExecutionOnDevice(execName,deviceID , executionDevice, "", scriptGroupInstance?.id, execName,
					filePath, realPath, TEST_SUITE, url, isBenchMark, isSystemDiagnostics, rerun,isLogReqd)

			} catch (Exception e) {
				e.printStackTrace()
			}

			Execution exe = Execution.findByName(execName)
			if(exe){
				paused = exe?.executionStatus.equals(Constants.PAUSED)
			}
		}
		return paused
	}
	
	/**
	 * Method to save the repeat execution details
	 */
	public boolean saveRepeatExecutionDetails(final String execName, String scriptName, String deviceName,
		ScriptGroup scriptGroupInstance , String appUrl,String isBenchMark , String isSystemDiagnostics,String rerun,Groups groups, int scriptCnt, String isLogReqd){
		   def executionSaveStatus = true
		   try {
			   Execution.withTransaction {
			   Execution execution = new Execution()
			   execution.name = execName
			   execution.script = scriptName
			   execution.device = deviceName
			   execution.scriptCount = scriptCnt
			   execution.scriptGroup = scriptGroupInstance?.name
			   execution.result = UNDEFINED_STATUS
			   execution.executionStatus = INPROGRESS_STATUS
			   execution.dateOfExecution = new Date()
			   execution.groups = groups
			   execution.applicationUrl = appUrl
			   execution.isRerunRequired = rerun?.equals("true")
			   execution.isBenchMarkEnabled = isBenchMark?.equals("true")
			   execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals("true")
			   execution.isStbLogRequired = isLogReqd?.equals("true")
			   if(! execution.save(flush:true)) {
				   executionSaveStatus = false
			   }
			   
			   }
		   }
		   catch(Exception th) {
			   th.printStackTrace()
			   executionSaveStatus = false
		   }
		   return executionSaveStatus
	   }
		
	/**
	 *	Method to execute a execute a script on device as part of repeat after pause
	 * @return
	 */
	def repeatExecutionOnDevice(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun, def isLogReqd)
	{
		boolean aborted = false
		boolean pause = false
		def scriptInstance
		Device deviceInstance
		Device.withTransaction {
			deviceInstance = Device.findById(device)
		}
		ScriptGroup scriptGroupInstance
		StringBuilder output = new StringBuilder();
		def htmlData = ""
		int scriptGrpSize = 0
		int scriptCounter = 0
		def isMultiple = TRUE
		if(groupType == TEST_SUITE){
			scriptCounter = 0
			boolean skipStatus = false
			boolean notApplicable = false
			List validScriptList = new ArrayList()
			String rdkVersion = ""
			Device.withTransaction {
				Device dev = Device.findById(deviceInstance?.id)
				rdkVersion = executionService.getRDKBuildVersion(dev);
			}
			ScriptGroup.withTransaction { trans ->
				scriptGroupInstance = ScriptGroup.findById(scriptGrp)
				scriptGroupInstance.scriptList.each { script ->
					
					scriptInstance = scriptService.getScript(realPath, script?.moduleName, script?.scriptName)
					if(scriptInstance){
					if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance)){
						if(executionService.validateScriptRDKVersions(scriptInstance,rdkVersion)){
							if(scriptInstance.skip.toString().equals("true")){
								skipStatus = true
								executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance)
							}else{
								validScriptList << scriptInstance
							}

						}else{
							notApplicable = true
							String rdkVersionData = ""

//							Script.withTransaction {
//								def scriptInstance1 = Script.findById(script?.id)
							
								rdkVersionData = scriptInstance?.rdkVersions
//							}

							String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
							executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)
						}
					}else{
						notApplicable = true
						String boxTypeData = ""

						String deviceBoxType = ""

						Device.withTransaction {
							Device dev = Device.findById(deviceInstance?.id)
							deviceBoxType = dev?.boxType

						}

//						Script.withTransaction {
//							def scriptInstance1 = Script.findById(script?.id)
							boxTypeData = scriptInstance?.boxTypes
//						}

						String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
						executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason)
					}
					}else{
					String reason = "No script is available with name :"+script?.scriptName+" in module :"+script?.moduleName
					executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script?.scriptName, deviceInstance,reason)
					}
				}
			}
			
			scriptGrpSize = validScriptList?.size()
			Execution ex = Execution.findByName(execName)
			def exeId = ex?.id

			if((skipStatus || notApplicable) && scriptGrpSize == 0){
//				executionService.updateExecutionSkipStatusWithTransaction(SKIPPED, exeId)
				executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, exeId)
				executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, executionDevice?.id)
			}
			boolean executionStarted = false
			List pendingScripts = []
			// rest call for log transfer starts
			try {
				if(validScriptList.size() > 0){
					LogTransferService.transferLog(execName, deviceInstance)
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
			validScriptList.each{ scriptObj ->

				scriptCounter++
				if(scriptCounter == scriptGrpSize){
					isMultiple = FALSE
				}
				aborted = executionService.abortList.contains(exeId?.toString())

				String devStatus = ""
				if(!pause && !aborted){
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						/*Thread.start{
							deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
						}*/
					}
					catch(Exception eX){
					}
				}
				
				if(!aborted && !devStatus.equals(Status.NOT_FOUND.toString()) && !pause){
					def startExecutionTime = new Date()
					executionStarted = true
					htmlData = executeScript(execName, executionDevice, scriptObj, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics, executionName, isMultiple,null,isLogReqd)
					output.append(htmlData)
					Thread.sleep(6000)
					def endExecutionTime = new Date()
					executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
				}else{
					if(!aborted && devStatus.equals(Status.NOT_FOUND.toString())){
						pause = true
					}

					if(!aborted && pause) {
						
						try {
							pendingScripts.add(scriptObj)
							def execInstance
							Execution.withTransaction {
								def execInstance1 = Execution.findByName(execName)
								execInstance = execInstance1
							}
							Script scriptInstanceObj
//							Script.withTransaction {
//								Script scriptInstance1 = Script.findById(scriptObj.id)
								scriptInstanceObj = scriptInstance
//							}
							Device deviceInstanceObj
							def devId = deviceInstance?.id
							Device.withTransaction {
								Device deviceInstance1 = Device.findById(devId)
								deviceInstanceObj = deviceInstance1
							}
							ExecutionDevice executionDevice1
							ExecutionDevice.withTransaction {
								def exDev = ExecutionDevice.findById(executionDevice?.id)
								executionDevice1 = exDev
							}

							ExecutionResult.withTransaction { resultstatus ->
								try {
									def executionResult = new ExecutionResult()
									executionResult.execution = execInstance
									executionResult.executionDevice = executionDevice1
									executionResult.script = scriptInstanceObj?.name
									executionResult.device = deviceInstanceObj?.stbName
									executionResult.execDevice = null
									executionResult.deviceIdString = deviceInstanceObj?.id?.toString()
									executionResult.status = PENDING
									executionResult.dateOfExecution = new Date()
									if(! executionResult.save(flush:true)) {
									}
									resultstatus.flush()
								}
								catch(Throwable th) {
									resultstatus.setRollbackOnly()
								}
							}
						} catch (Exception e) {
						
						}

					}
				}
			}
			
			try {
				if(validScriptList.size() > 0){
					LogTransferService.closeLogTransfer(execName)
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
			
			if(aborted && executionService.abortList.contains(exeId?.toString())){
				executionService.abortList.remove(exeId?.toString())
			}

			if(!aborted && pause && pendingScripts.size() > 0 ){
				def exeInstance = Execution.findByName(execName)
				executionService.savePausedExecutionStatus(exeInstance?.id)
				executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
				//				ExecutionDevice.withTransaction {
				//					ExecutionDevice exDevice = ExecutionDevice.findById(idd)
				//					exDevice.status = PAUSED
				//					exDevice.save();
				//				}
			}
		}
		Execution executionInstance1 = Execution.findByName(execName)
		if(!pause){
			executionService.saveExecutionStatus(aborted, executionInstance1?.id)
		}
		htmlData = ""

		if(!aborted && !pause){

			def executionDeviceObj1
			ExecutionDevice.withTransaction{ wthTrans ->
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)
				executionDeviceObj1 = executionDeviceObj
			}
			if((executionDeviceObj1) && (rerun.equals(TRUE))){
				htmlData = reRunOnFailure(realPath,filePath,execName,executionName,url)
				output.append(htmlData)
			}

		}else{
			resetAgent(deviceInstance)
		}
		deleteOutputFile(executionName)
		htmlData = output.toString()
		return htmlData
	}
	
	/**
	 * method to fetch the name of the file transfer script
	 */
	def getFileTransferScriptName(Device device){
		String scriptName = FILE_TRANSFER_SCRIPT
		if(InetUtility.isIPv6Address(device?.stbIp)){
			scriptName = FILE_UPLOAD_SCRIPT
		}else{
			String mechanism = executionService.getIPV4LogUploadMechanism()
			if(mechanism?.equals(Constants.REST_MECHANISM)){
				scriptName = FILE_UPLOAD_SCRIPT
			}
			
		}
		return scriptName
	}
	
	/**
	 * method to fetch the name of the console file transfer script
	 */
	def getConsoleFileTransferScriptName(Device device){
		String scriptName = CONSOLE_FILE_TRANSFER_SCRIPT
		if(InetUtility.isIPv6Address(device?.stbIp)){
			scriptName = CONSOLE_FILE_UPLOAD_SCRIPT
		}else{
			String mechanism = executionService.getIPV4LogUploadMechanism()
			if(mechanism?.equals(Constants.REST_MECHANISM)){
				scriptName = CONSOLE_FILE_UPLOAD_SCRIPT
			}
			
		}
		return scriptName
	}
	
	
	def transferSTBLog(def moduleName , def dev,def execId, def execDeviceId,def execResultId,def realPath,def url){
		try {
			def module
			def stbLogFiles
			Module.withTransaction {
				module = Module.findByName(moduleName)
				if(module?.stbLogFiles?.size() > 0){
					stbLogFiles = module?.stbLogFiles
				}
			}

			def destFolder = grailsApplication.parentContext.getResource("//logs//stblogs//execId_logdata.txt").file
			def destPath = destFolder.absolutePath
			
			
			def filePath = destPath.replace("execId_logdata.txt", "${execId}//${execDeviceId}//${execResultId}")
			def directoryPath =  "${execId}_${execDeviceId}_${execResultId}"
			def stbFilePath = "${realPath}/logs//stblogs//${execId}//${execDeviceId}//${execResultId}//"
			//def directoryPath = destPath.replace("execId_logdata.txt", "${execId}//${execDeviceId}//${execResultId}")
			//new File(directoryPath).mkdirs()
			
			stbLogFiles?.each{ name -> 
				
			String scriptName = getFileTransferScriptName(dev)
			File layoutFolder = grailsApplication.parentContext.getResource(scriptName).file

			File fileStore = grailsApplication.parentContext.getResource("//fileStore//").file
			def fileStorePath = fileStore.absolutePath

			def absolutePath = layoutFolder.absolutePath
			String fName = name?.replaceAll("//", "_")
			fName = fName?.replaceAll("/", "_")
			
			if((absolutePath) && !(absolutePath.isEmpty())){

				def cmdList = [
					"python",
					absolutePath,
					dev?.stbIp,
					//dev?.logTransferPort,
					dev?.agentMonitorPort,
					name,
					directoryPath+"_"+fName 
				]
				
				if(scriptName?.equals(FILE_UPLOAD_SCRIPT)){
					url = executionService.updateTMUrl(url,dev)
					cmdList.push(url)
				}
				
				String [] cmd = cmdList.toArray()
				try {
					ScriptExecutor scriptExecutor = new ScriptExecutor()
					def outputData = scriptExecutor.executeScript(cmd,1)
					copyStbLogsIntoDir(realPath,stbFilePath, execId,execDeviceId,execResultId)
				}catch (Exception e) {
					println " error >> "+e.getMessage()
					e.printStackTrace()
				}
			}
			
			}
		} catch (Exception e) {
			println " ERROR "+e.getMessage()
		}
	}
	
	/**
	 * To initiate the diagnostics test 
	 */
	def initiateDiagnosticsTest(def deviceInstance , def diagFileName , def tmUrl , def uniqueExecutionName ){
		def output = ""
		try{
				File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callDiagnosticsTest.py").file
				def absolutePath = layoutFolder.absolutePath
		
				String[] cmd = [
					PYTHON_COMMAND,
					absolutePath,
					deviceInstance?.stbIp,
					deviceInstance?.stbPort,
					deviceInstance?.agentMonitorPort,
					//deviceInstance?.logTransferPort,
					KEY_DIAGNOSTICS,
					diagFileName,
					tmUrl
				]
				
				ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
				output = scriptExecutor.executeScript(cmd,10)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return output
	}
	
	
	/*def initiateLogTransfer(String executionName, String server, String logAppName, Device device){
				int count = 3
				boolean logTransferInitiated = false
				try{
					println "start url : http://$server/$logAppName/startScheduler/$executionName/$device.stbName/$device.stbIp/$device.statusPort/$device.logTransferPort"
				}
				catch(Exception e){
					println e.getMessage()
				}
				
				while(count > 0 && !logTransferInitiated){
					HttpURLConnection connection = null
					try{
							println "initiating transaction"
							connection = new URL("http://$server/$logAppName/startScheduler/$executionName/$device.stbName/$device.stbIp/$device.statusPort/$device.logTransferPort").openConnection()
							connectToLogServerAndExecute(connection)
							println "Initiated log transfer for $executionName"
							logTransferInitiated = true
						}
						catch(Exception e) {
							e.printStackTrace()
							--count
						}
						finally{
							if(connection != null){
								connection.disconnect()
							}
						}
					}
				println "logTransferInitiated : $logTransferInitiated"
				logTransferInitiated

	}

	def stopLogTransfer(String executionName, String server, String logAppName){

				int count = 3
				boolean logTransferStopInitiated = false
				while(count > 0 && !logTransferStopInitiated){
					HttpURLConnection connection = null
					try{
						String url = "http://$server/$logAppName/stopScheduler/$executionName"
						print "url : $url"
						connection = new URL(url).openConnection()
						connectToLogServerAndExecute(connection)
						logTransferStopInitiated = true
					}
					catch(Exception e){
						e.printStackTrace()
						--count
					}
					finally{
						if(connection != null){
							connection.disconnect()
						}
					}
				}
				logTransferStopInitiated
	}
	
	def void connectToLogServerAndExecute(URLConnection connection) {
		connection.setConnectTimeout(120000)
		int responseCode = connection.getResponseCode()
		if(responseCode == 200){
			String finalresp = getResponse(connection.getInputStream())
			println finalresp
		}
		else{
			String finalresp = getResponse(connection.getErrorStream())
			try{
				String resp = finalresp.substring(finalresp.indexOf("<body><h1>")+"<body><h1>".length(), finalresp.indexOf("</h1>"))
				println resp.split("-")[1].trim()
			}
			catch(Exception e){
				println finalresp
			}
		}
	}
	
	def String getResponse(InputStream inputStream){
		BufferedReader buf = new BufferedReader(new InputStreamReader(inputStream))
		StringBuilder build = new StringBuilder()
		String x = null
		while( (x = buf.readLine())!= null){
			build.append(x).append("\n")
		}
		buf.close()
		String finalresp = build.toString()
		finalresp
	}*/
}
