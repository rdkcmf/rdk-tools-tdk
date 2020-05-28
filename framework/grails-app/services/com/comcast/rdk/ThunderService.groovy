/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
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

import org.apache.shiro.SecurityUtils
import org.codehaus.groovy.grails.web.json.JSONObject
import org.junit.After;

import grails.converters.JSON

import java.text.DateFormat
import java.text.SimpleDateFormat
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.FutureTask
import java.util.regex.Matcher
import java.util.regex.Pattern

import com.google.gson.JsonObject

class ThunderService {
	
	static transactional = false
	/**
	 * Injects the executionSerice.
	 */
	def executionService
	
	/**
	 * Injects the deviceStatusService
	 */
	
	def deviceStatusService
	
	/**
	 * Injects the scriptService
	 */
	def scriptService
	
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication
	
	/**
	 * Method to execute the thunder scripts
	 */
	public String executeThunderScripts(def params,def realPath){
		def htmlData = ""
		def executionName
		String scriptGroupName = ""
		executionName = params?.name
		def currentExecutionName = executionName
		int repeatNo = Integer.parseInt(params?.repeatNo)
		if(params?.scriptGrpThunder != null) {
			ScriptGroup scriptGroup = ScriptGroup.findById(params?.scriptGrpThunder)
			scriptGroupName = scriptGroup?.name
		}
		for(int repeatCount = 0; repeatCount < repeatNo; repeatCount++) {
			htmlData = ""
			if(repeatCount > 0) {
				executionName = currentExecutionName + "_" + repeatCount
			}
			if( params?.myGroupThunder == "TestSuiteThunder") {
				htmlData = executeThunderScriptGroup(scriptGroupName, executionName, params, realPath)
			}
			else if (params?.scriptsThunder != null){
				if(params?.scriptsThunder instanceof String) {
					htmlData = executeSingleThunderScript(executionName,params, realPath)
				} else {
					def scriptList = params?.scriptsThunder
					def groupName = MULTIPLESCRIPT
					htmlData = executeMultipleThunderScriptList(scriptList,executionName,groupName, params, realPath)
				}
			} else {
				log.error "Couldn't find the test.."
			}
			rerunOnFailureEnable(executionName, realPath, params)
		}
		return htmlData
	}
	
	/**
	 * Method to execute multiple thunder scripts
	 */
	def executeMultipleThunderScriptList(def scriptList, def executionName,def scriptGroupName,def params, def realPath){
		Device device = Device.findById(params?.devices)
		def scriptInstanceList = []
		def htmlData = ""
		ScriptFile.withTransaction {
			scriptList.each { scriptName->
				def scriptFile = ScriptFile.findByScriptName(scriptName)
				if(scriptFile != null) {
					scriptInstanceList.add(scriptFile)
				}
			}
		}
		if(scriptInstanceList.size() > 0) {
			htmlData = executeThunderScriptList(scriptInstanceList, device, params?.grailsUrl, realPath,scriptGroupName, executionName, grailsApplication, params)
		}
		return htmlData
	}
	
	/**
	 * Method to execute single thunder script
	 */
	def executeSingleThunderScript(def executionName,def params, def realPath){
		boolean scriptNotPresent = false
		def scriptObject = ScriptFile.findByScriptNameAndCategory(params?.scriptsThunder,Category.RDKV_THUNDER)
		if(!(scriptService?.totalThunderScriptList?.contains(scriptObject))){
			scriptNotPresent = true
		}
		File configFile
		def STORM_TIME_OUT = null
		def STORM_TIME_OUT_INTEGER
		try{
		    configFile = grailsApplication.parentContext.getResource(Constants.STORM_TESTS_TIME_OUT_CONFIG_FILE).file
		    STORM_TIME_OUT = getConfigProperty(configFile, params?.scriptsThunder)
		    if(STORM_TIME_OUT == null || STORM_TIME_OUT == ""){
		        configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		        STORM_TIME_OUT = getConfigProperty(configFile, Constants.STORM_TIME_OUT)
		    }else if(STORM_TIME_OUT == null || STORM_TIME_OUT == ""){
			    STORM_TIME_OUT = Constants.STORM_DEFAULT_TIME_OUT
		    }
            STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
		}catch(Exception e){
		    e.printStackTrace()
			STORM_TIME_OUT = Constants.STORM_DEFAULT_TIME_OUT
			STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
		}
		def STORM_COUNTER_MAXIMUM = (STORM_TIME_OUT_INTEGER * 60 * 1000)/(10000)
		boolean executionResult = false
		String htmlData = ""
		Device deviceInstance
		def startExecutionTime = new Date()
		deviceInstance = Device.findById(params?.devices)
		long timeDifference
		String status
		boolean allocated = false
		try {
			status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
		
				if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
					status = "BUSY"
				}else{
					if((status.equals( Status.FREE.toString() ))){
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
		catch(Exception eX){
			eX.printStackTrace()
		}
		def executionId
		def executionDeviceId
		def executionResultId
		def rerun = "off"
		if((params.rerun?.toString().equals("on"))){
			rerun =  params.rerun
		}
		if((status.equals( Status.FREE.toString() )) && !scriptNotPresent){
			(executionId, executionDeviceId) = saveMultipleScriptExecutionDetailsThunder(deviceInstance?.stbName, executionName, params?.scriptsThunder, UNDEFINED_STATUS, startExecutionTime, timeDifference, htmlData, 0, params?.grailsUrl,rerun)
			Execution execution = Execution.findById(executionId)
			ExecutionDevice executionDevice = ExecutionDevice.findById(executionDeviceId)
			boolean executionFinished = false
			def waitCounter = 0
			startExecutionTime = new Date()
			StormExecuter.executeThunderScript(grailsApplication,params?.scriptsThunder,deviceInstance?.stbIp,executionName)
			sleep(10000)
			waitCounter++
			executionFinished = StormExecuter.checkThunderExecution(grailsApplication,params?.scriptsThunder,executionName)
			while(!executionFinished && waitCounter<STORM_COUNTER_MAXIMUM){
				sleep(10000)
				executionFinished = StormExecuter.checkThunderExecution(grailsApplication,params?.scriptsThunder,executionName)
				if(executionFinished){
					break;
				}
				waitCounter++
			}
			def endExecutionTime = new Date()
			if(waitCounter==STORM_COUNTER_MAXIMUM && !executionFinished){
				executionResult = false
			}else if(executionFinished){
				executionResult = StormExecuter.parseThunderResult(grailsApplication,params?.scriptsThunder,executionName)
			}
			timeDifference = endExecutionTime.getTime() - startExecutionTime.getTime()
			long timeDifferenceInSeconds = (long)(timeDifference/(1000))
			float timeDifferenceInMinutes = (float)(timeDifferenceInSeconds/(60.0))
			String timeDifferenceInMinutesString = timeDifferenceInMinutes.toString()
			timeDifferenceInMinutesString = truncateTimeTaken(timeDifferenceInMinutesString)
			def statusExecution
			if(executionResult){
				statusExecution = SUCCESS_STATUS
			}else{
				statusExecution = FAILURE_STATUS
			}
			try{
				if(allocated && executionService.deviceAllocatedList.contains(deviceInstance?.id)){
					executionService.deviceAllocatedList.remove(deviceInstance?.id)
					allocated = false
				}
				status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				Thread.start{
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, status)
				}
			}catch(Exception e){
				e.printStackTrace()
			}
			htmlData = StormExecuter.returnThunderLogFile(grailsApplication,params?.scriptsThunder,executionName)
			ExecutionResult.withTransaction{
				def executionResultObject = new ExecutionResult()
				executionResultObject.execution = execution
				executionResultObject.executionDevice = executionDevice
				executionResultObject.script = params?.scriptsThunder
				executionResultObject.device = executionDevice.device
				executionResultObject.execDevice = null
				executionResultObject.deviceIdString = null
				executionResultObject.status = statusExecution
				executionResultObject.executionTime = timeDifferenceInMinutesString
				executionResultObject.totalExecutionTime = timeDifferenceInMinutesString
				executionResultObject.dateOfExecution = execution.dateOfExecution
				executionResultObject.category = execution.category
				executionResultObject.executionOutput = htmlData
				if(!executionResultObject.save(flush:true)) {
					println "error : "+executionResultObject?.errors
				}else {
					executionResultId = executionResultObject.id
				}
			}
			boolean serverConsoleLogFilecreated =StormExecuter.writeServerConsoleLogFileData(grailsApplication, realPath,  executionId, executionDeviceId, executionResultId, params?.scriptsThunder, executionName)
			boolean versionFilecreated = StormExecuter.createThunderVersionFile(realPath, executionId, executionDeviceId, executionDevice?.deviceIp)
			Execution.executeUpdate("update Execution e set e.executionStatus = :completedStatus , e.result = :newStatus, e.realExecutionTime = :timeDifference, e.executionTime = :timeDifference, e.outputData = :outputData where e.id = :execId",
				[newStatus: statusExecution, execId: executionId, completedStatus: COMPLETED_STATUS, timeDifference: timeDifferenceInMinutesString, outputData: htmlData])
			ExecutionDevice.executeUpdate("update ExecutionDevice e set e.executionTime = :timeDifference where e.id = :execDeviceId",
				[execDeviceId: executionDeviceId, timeDifference: timeDifferenceInMinutesString])
		}else if(scriptNotPresent){
			htmlData = "Script not found"
		}
		return htmlData
	}
	
	/**
	 * Method to execute thunder test suite
	 */
	def executeThunderScriptGroup(def scriptGroupName, def executionName ,def params, def realPath){
		Device device = Device.findById(params?.devices)
		String htmlData =""
		def scriptList
		ScriptGroup scriptGroup = ScriptGroup.findByName(scriptGroupName)
		scriptList = scriptGroup.scriptList
		if(scriptGroup != null) {
			if(scriptList.size() > 0) {
				htmlData = executeThunderScriptList(scriptList, device, params?.grailsUrl, realPath,scriptGroupName, executionName, grailsApplication, params)
			}else {
				htmlData = "Test Suite is empty."
			}
		}
		return htmlData
	}
	
	/**
	 * Method to execute a list of thunder scripts.
	 * @return
	 */
	def executeThunderScriptList(def scriptList, def device, def applicationUrl, def realPath, def scriptGroupName, def executionName, def grailsApplication, params){
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_FRAMEWORK_LOCATION = getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
		def folderName = Constants.SCRIPT_OUTPUT_FILE_PATH_STORM
		File folder = grailsApplication.parentContext.getResource(folderName).file
		folder.mkdirs()
		String fullLogFilePath = folderName+executionName+Constants.UNDERSCORE+Constants.FULLLOG_LOG
		File fullLogFile = grailsApplication.parentContext.getResource(fullLogFilePath).file
		String fullLogFileAbsolutePath = fullLogFile.getAbsolutePath()
		String STORM_TIME_OUT = ""
		try{
		    STORM_TIME_OUT = getConfigProperty(configFile, Constants.STORM_TIME_OUT)
		}catch(Exception e){
		    e.printStackTrace()
		}
		def STORM_TIME_OUT_INTEGER
		def STORM_COUNTER_MAXIMUM
		File fullLog = new File(fullLogFileAbsolutePath)
		boolean fullLogFileCreated = false
		try{
		if(fullLog.createNewFile()){
			fullLogFileCreated = true
		}}catch(Exception e){
			e.printStackTrace()
		}		
		def executionId
		def executionResultId
		def executionDeviceId
		def suiteStartTime = new Date()
		def suiteEndTime = null
		long timeDifference
		long timeDifferenceInSeconds
		float timeDifferenceInMinutes
		String timeDifferenceInMinutesString
		String status
		boolean allocated = false
		boolean aborted = false
		String rerun = ""
		String htmlData = ""
		String executionLogData = ""
		executionLogData = executionLogData + HTML_BR + HTML_BR
		Device deviceInstance = Device.findById(params?.devices)
		def stbName = deviceInstance?.stbName
		def executionResultStatus = UNDEFINED_STATUS
		def scriptCount = scriptList.size()
		try{
			status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
			if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				status = "BUSY"
			}else{
			    if((status.equals( Status.FREE.toString() ))){
				    if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
					    allocated = true
					    executionService.deviceAllocatedList.add(deviceInstance?.id)
					    Thread.start{
						    deviceStatusService.updateOnlyDeviceStatus(deviceInstance, "BUSY")
					    }
				    }
			    }
			}
		}catch(Exception e){
		    e.printStackTrace()
		}
		if((params.rerun?.toString().equals("on"))){
			rerun =  params.rerun
		}
		if(status.equals( Status.FREE.toString() )){
			(executionId, executionDeviceId) = saveMultipleScriptExecutionDetailsThunder(stbName, executionName, scriptGroupName, executionResultStatus, suiteStartTime, timeDifferenceInSeconds, htmlData, scriptCount, applicationUrl,rerun)
			Execution execution = Execution.findById(executionId)
			ExecutionDevice executionDevice = ExecutionDevice.findById(executionDeviceId)
			int scriptCounter = 0
			boolean executionCompleted = "false"
			for(int i=0; i<scriptList.size(); i++) {
				boolean scriptPresent = false
				scriptCounter++
				aborted = executionService.abortList.contains(executionId?.toString())
				def executionResultStatusScript = FAILURE_STATUS
				if(!aborted && !(status.equals(Status.NOT_FOUND.toString()) || status.equals(Status.HANG.toString()))){
					try {
								def scriptObject = ScriptFile.findByScriptNameAndCategory(scriptList[i]?.scriptName,Category.RDKV_THUNDER)
								def fileStorePath = STORM_FRAMEWORK_LOCATION+Constants.TESTCASES+File.separator+Constants.STORM_TESTCASES+File.separator+Constants.SRC+File.separator+Constants.TESTS+File.separator
								List directories = new File(fileStorePath).listFiles()
								List dirList = []
								directories.each{directory ->
									String directoryName = directory.toString()
									int index = directoryName.lastIndexOf("/");
									String directoryNameString = directoryName.substring(index+1, directoryName.length());
									dirList.add(directoryNameString)
								}
								String fileName
								boolean fileFound = false
								def path
								for(String directory : dirList){
									File scriptsDir = new File("$fileStorePath"+directory+File.separator)
									if(scriptsDir.exists()){
										def testscriptfiles = scriptsDir.list()
										for(String testscriptfile : testscriptfiles){
											if(testscriptfile.contains(".js") ){
												fileName = testscriptfile.split(".js")[0]
												if(fileName.equals(scriptList[i]?.scriptName)){
													path = fileStorePath + directory + File.separator + scriptList[i]?.scriptName + JAVASCRIPT_EXTENSION
													fileFound = true
													break
												}
											}
										}
										if(fileFound){
											break
										}
									}
								}
								if(fileFound){
									scriptPresent = true
								}
						if(scriptPresent){
							boolean executionResult = false
							boolean executionFinished = false
							def waitCounter = 0
							DateFormat dateFormat1 = new SimpleDateFormat(DATE_FORMAT)
							Calendar cal1 = Calendar.getInstance()
							def timeStamp = dateFormat1.format(cal1.getTime()).toString()
							def scriptStartTime = new Date()
							File timeoutConfigFile = grailsApplication.parentContext.getResource(Constants.STORM_TESTS_TIME_OUT_CONFIG_FILE).file
							def STORM_SPECIFIC_TIME_OUT = null
							try{
							    STORM_SPECIFIC_TIME_OUT = getConfigProperty(timeoutConfigFile, scriptList[i]?.scriptName)
							    if(STORM_SPECIFIC_TIME_OUT != null && STORM_SPECIFIC_TIME_OUT != ""){
								    STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_SPECIFIC_TIME_OUT)
							    }else if(STORM_TIME_OUT != null && STORM_TIME_OUT != ""){
							        STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
							    }else{
								    STORM_TIME_OUT = Constants.STORM_DEFAULT_TIME_OUT
									STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
							    }
								STORM_COUNTER_MAXIMUM = (STORM_TIME_OUT_INTEGER * 60 * 1000)/(10000)
							}catch(Exception e){
							    e.printStackTrace()
								STORM_TIME_OUT = Constants.STORM_DEFAULT_TIME_OUT
								STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
								STORM_COUNTER_MAXIMUM = (STORM_TIME_OUT_INTEGER * 60 * 1000)/(10000)
							}
							StormExecuter.executeThunderScript(grailsApplication,scriptList[i]?.scriptName,device?.stbIp,executionName)
							sleep(10000)
							waitCounter++
							executionFinished = StormExecuter.checkThunderExecution(grailsApplication,scriptList[i]?.scriptName,executionName)
							while(!executionFinished && waitCounter<STORM_COUNTER_MAXIMUM){
								sleep(10000)
								executionFinished = StormExecuter.checkThunderExecution(grailsApplication,scriptList[i]?.scriptName,executionName)
								if(executionFinished){
									break;
								}
								waitCounter++
							}
							def scriptEndTime = new Date()
							def scripttimeDifference = scriptEndTime.getTime() - scriptStartTime.getTime()
							def scripttimeDifferenceInSeconds = (long)(scripttimeDifference/(1000))
							def scripttimeDifferenceInMinutes = (float)(scripttimeDifferenceInSeconds/(60.0))
							def scripttimeDifferenceInMinutesString = scripttimeDifferenceInMinutes?.toString()
							scripttimeDifferenceInMinutesString = truncateTimeTaken(scripttimeDifferenceInMinutesString)
							if(waitCounter==STORM_COUNTER_MAXIMUM && !executionFinished){
								executionResult = false
							}else if(executionFinished){
							    executionResult = StormExecuter.parseThunderResult(grailsApplication,scriptList[i]?.scriptName,executionName)
							}						
							htmlData = StormExecuter.returnThunderLogFile(grailsApplication,scriptList[i]?.scriptName,executionName)
							def htmlDataForAppend  = timeStamp + HTML_BR + EXECUTING_SCRIPT + scriptList[i]?.scriptName + HTML_BR + LOG_SEPARATION_LINE_STRING + HTML_BR + htmlData
							executionLogData = executionLogData + timeStamp + HTML_BR + EXECUTING_SCRIPT + scriptList[i]?.scriptName + HTML_BR + LOG_SEPARATION_LINE_STRING + HTML_BR + htmlData + HTML_BR + HTML_BR
							try{
								if(fullLogFileCreated){
								    FileWriter fr = new FileWriter(fullLog, true)
								    fr.write(htmlDataForAppend)
								    fr.write("\n\n")
								    fr.close()
								}
							}catch(Exception e){
							    e.printStackTrace()
							}
							if(executionResult){
								executionResultStatusScript = SUCCESS_STATUS
							}
							ExecutionResult.withTransaction{
								def executionResultObject = new ExecutionResult()
								executionResultObject.execution = execution
								executionResultObject.executionDevice = executionDevice
								executionResultObject.script = scriptList[i]?.scriptName
								executionResultObject.device = executionDevice.device
								executionResultObject.execDevice = null
								executionResultObject.deviceIdString = null
								executionResultObject.status = executionResultStatusScript
								executionResultObject.executionTime = scripttimeDifferenceInMinutesString
								executionResultObject.totalExecutionTime = scripttimeDifferenceInMinutesString
								executionResultObject.dateOfExecution = execution.dateOfExecution
								executionResultObject.category = execution.category
								executionResultObject.executionOutput = htmlData
								if(!executionResultObject.save(flush:true)) {
									println "error : "+executionResultObject?.errors
								}else {
										executionResultId = executionResultObject.id
								}
							}
							if(scriptCounter == (scriptCount-1)){
								executionCompleted = "true"
							}
						}
						else{
							String reason = "No script is available with name :"+scriptList[i]?.scriptName
								ExecutionResult.withTransaction{
									ExecutionResult executionResult = new ExecutionResult()
									executionResult.execution = execution
									executionResult.executionDevice = executionDevice
									executionResult.script = scriptList[i]?.scriptName
									executionResult.device = deviceInstance?.stbName
									executionResult.status = Constants.SKIPPED_STATUS
									executionResult.dateOfExecution = new Date()
									executionResult.executionOutput = "Test not executed. Reason : "+reason
									executionResult.category = Category.RDKV_THUNDER
									if(! executionResult.save(flush:true)) {
										log.error "Error saving executionResult instance : ${executionResult.errors}"
									}
							   }
						}
				} catch (Exception e) {
						log.error"Exception occurred!!. e : "+e
						e.printStackTrace()
					}
					boolean serverConsoleLogFilecreated =StormExecuter.writeServerConsoleLogFileData(grailsApplication, realPath,  executionId, executionDeviceId, executionResultId, scriptList[i]?.scriptName, executionName)
					
			}
				else{
					if(aborted && executionService.abortList.contains(executionId?.toString())){
						break
					}
				}
			}
			suiteEndTime = new Date()
			timeDifference = suiteEndTime.getTime() - suiteStartTime.getTime()
			timeDifferenceInSeconds = (long)(timeDifference/(1000))
			timeDifferenceInMinutes = (float)(timeDifferenceInSeconds/(60.0))
			timeDifferenceInMinutesString = timeDifferenceInMinutes?.toString()
			try{
				if(allocated && executionService.deviceAllocatedList.contains(deviceInstance?.id)){
					executionService.deviceAllocatedList.remove(deviceInstance?.id)
					allocated = false
				}
				status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				Thread.start{
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, status)
				}
			}catch(Exception e){
				e.printStackTrace()
			}
			def failureListCount = ExecutionResult.executeQuery("SELECT count(*) from ExecutionResult where execution_id = :execId and status like :status",
			[execId:executionId, status:"FAILURE"])
			def timeoutListCount = ExecutionResult.executeQuery("SELECT count(*) from ExecutionResult where execution_id = :execId and status like :status",
			[execId:executionId, status:"SCRIPT TIME OUT"])
			def statusExecution = "SUCCESS"
			if(failureListCount[0] > 0 || timeoutListCount[0] > 0) {
				statusExecution = "FAILURE"
			}
			
			if(aborted && executionService.abortList.contains(executionId?.toString())){
				Execution.executeUpdate("update Execution e set e.executionStatus = :completedStatus , e.result = :newStatus, e.realExecutionTime = :timeDifference, e.executionTime = :timeDifference, e.outputData = :outputData where e.id = :execId",
				[newStatus: statusExecution, execId: executionId, completedStatus: "ABORTED", timeDifference: timeDifferenceInMinutesString, outputData: executionLogData])
				executionService.abortList.remove(executionId?.toString())
			}else{
				Execution.executeUpdate("update Execution e set e.executionStatus = :completedStatus , e.result = :newStatus, e.realExecutionTime = :timeDifference, e.executionTime = :timeDifference, e.outputData = :outputData where e.id = :execId",
				[newStatus: statusExecution, execId: executionId, completedStatus: "COMPLETED", timeDifference: timeDifferenceInMinutesString, outputData: executionLogData])
			}
			ExecutionDevice.executeUpdate("update ExecutionDevice e set e.executionTime = :timeDifference where e.id = :execDeviceId",
				[execDeviceId: executionDeviceId, timeDifference: timeDifferenceInMinutesString])
			
			boolean versionFilecreated = StormExecuter.createThunderVersionFile(realPath, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
		}else {
		    executionLogData = "Device is not FREE to execute scripts"
		}
		return executionLogData
	}
	
	/**
	 * Method to check whether rerun is enabled or not. If enabled, call the runFailedScripts method
	 * @param execName
	 * @param applicationUrl
	 * @param realPath
	 * @param params
	 * @return
	 */
	def rerunOnFailureEnable(def execName, def realPath, params){
		Execution.withSession { session ->
			session.clear()
		}
		def execution = Execution.findByName(execName)
		if(execution){
			try{
				def isRerunRequired = execution.isRerunRequired
				if(execution.result == FAILURE && isRerunRequired){
					runFailedScripts(params, execName, realPath)
				}
			}catch(Exception e){
		    	e.printStackTrace()
			}
		}
	}

	/**
	 * Method to rerun a failed execution if 'Re-Run on Failure' option is enabled while triggering execution
	 * @param params
	 * @param executionName
	 * @param realPath
	 * @return
	 */
	def runFailedScripts(params,final String executionName,  final String realPath){
		def execution = Execution.findByName(executionName)
		Device device = Device.findById(params?.devices)
		def failedExecutionResultList = ExecutionResult.findAllByExecutionAndStatus(execution, "FAILURE")
		def failedScriptList = []
		def scriptInstanceList = []
		String scriptGroupName = ""
		String htmlData = ""
		failedExecutionResultList.each { result ->
			failedScriptList.add(result?.script)
			def scriptFile = ScriptFile.findByScriptName(result?.script)
			if(scriptFile != null) {
				scriptInstanceList.add(scriptFile)
			}
		}
		def newExecName = getRerunExecutionName(executionName)
		def rerunExec = Execution.findByName(newExecName)
		if(rerunExec == null){
			if(params?.scriptGrpThunder != null) {
				ScriptGroup scriptGroup = ScriptGroup.findById(params?.scriptGrpThunder)
				scriptGroupName = scriptGroup?.name
			}
			htmlData = ""
			if( params?.myGroupThunder == "TestSuiteThunder") {
				htmlData = executeThunderScriptList(scriptInstanceList, device, params?.grailsUrl, realPath,scriptGroupName, newExecName, grailsApplication, params)
			}
			else if (params?.scriptsThunder != null){
				if(params?.scriptsThunder instanceof String) {
					htmlData = executeSingleThunderScript(newExecName, params, realPath)
				} else {
					def groupName = MULTIPLESCRIPT
					htmlData = executeThunderScriptList(scriptInstanceList, device, params?.grailsUrl, realPath,groupName, newExecName, grailsApplication, params)
				}
			} else {
				log.error "Couldn't find the test.."
			}
		}
	}
	
	/**
	 * Method to rerun a failed execution from execution popup
	 * @param params
	 * @param executionName
	 * @param realPath
	 * @param applicationUrl
	 * @return
	 */
	def runFailedScriptsManually(params,final String executionName,  final String realPath, final String applicationUrl){
		def execution = Execution.findByName(executionName)
		Device device = Device.findByStbName(params?.device)
		params?.devices = device.id.toString()
		def failedExecutionResultList = ExecutionResult.findAllByExecutionAndStatus(execution, "FAILURE")
		def scriptInstanceList = []
		String scriptGroupName = ""
		String htmlData = ""
		failedExecutionResultList.each { result ->
			def scriptFile = ScriptFile.findByScriptName(result?.script)
			if(scriptFile != null) {
				scriptInstanceList.add(scriptFile)
			}
		}
		def newExecName = getRerunExecutionNameForManual(executionName)
		def rerunExec = Execution.findByName(newExecName)
		if(rerunExec == null){
			if (params?.script){
				if (params?.script?.equals("Multiple Scripts")){
					def groupName = MULTIPLESCRIPT
					htmlData = executeThunderScriptList(scriptInstanceList, device, applicationUrl, realPath,groupName, newExecName, grailsApplication, params)
				}
				else{
					params?.scriptsThunder = params?.script
					params?.grailsUrl = applicationUrl
					params?.category = Category.RDKV_THUNDER.toString()
					htmlData = executeSingleThunderScript(newExecName, params, realPath)
				}
			}else if(params?.scriptGroup) {
				scriptGroupName = params?.scriptGroup
				htmlData = executeThunderScriptList(scriptInstanceList, device, applicationUrl, realPath,scriptGroupName, newExecName, grailsApplication, params)
			}else{
				log.error "Couldn't find the test.."
			}
		}
	}
	
	/**
	 * Method to repeat a particular execution from execution popup
	 * @param params
	 * @param execName
	 * @param realPath
	 * @param url
	 * @return
	 */
	def executeScriptsRepeat(def params, def execName, def realPath, def url)
	{
		def scriptGroupName = params?.scriptGroup
		Device device = Device.findByStbName(params?.device)
		params?.devices = device.id.toString()
		String htmlData = ""
		def scriptInstanceList = []
		if (params?.script?.equals("Multiple Scripts")){
			def groupName = MULTIPLESCRIPT
			def oldExecName = params?.executionName
			def execution = Execution.findByName(oldExecName)
			def execResult = ExecutionResult?.findAllByExecution(execution)
			execResult.each { result ->
				def scriptFile = ScriptFile.findByScriptName(result?.script)
				if(scriptFile != null) {
					scriptInstanceList.add(scriptFile)
				}
			}
			htmlData = executeThunderScriptList(scriptInstanceList, device, url, realPath,groupName, execName, grailsApplication, params)
		} else if( params?.scriptGroup ) {
			scriptGroupName = params?.scriptGroup
			ScriptGroup scriptGroup = ScriptGroup.findByName(scriptGroupName)
			scriptInstanceList = scriptGroup.scriptList
			htmlData = executeThunderScriptList(scriptInstanceList, device, url, realPath,scriptGroupName, execName, grailsApplication, params)
			
		}else {
			log.error "Couldn't find the test.."
		}
	}
	
	/**
	 * Method to generate and return rerun execution name of an execution while triggering rerun manually
	 * @param execName
	 * @return
	 */
	def getRerunExecutionNameForManual(String execName){
		def newExecName
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
		return newExecName
	}
	
	/**
	 * Method to generate and return rerun execution name of an execution
	 * @param execName
	 * @return
	 */
	def getRerunExecutionName(String execName) {
		def newExecName
		String rerunKey = "_RERUN_"
		if(execName.contains(rerunKey)){
			def tokens = execName.split(rerunKey)
			newExecName = tokens[0] + rerunKey +  (Integer.parseInt(tokens[1]) + 1).toString()
		} else {
			newExecName = execName + rerunKey + "1"
		}
		return newExecName
	}
	
	/**
	 * Method to save execution , execution device details for multiple script and test suite executions
	 * @param stbName
	 * @param executionName
	 * @param scriptName
	 * @param executionResult
	 * @param startExecutionTime
	 * @param timedifference
	 * @param htmlData
	 * @param scriptCount
	 * @param applicationUrl
	 * @param rerun
	 * @return
	 */
	def saveMultipleScriptExecutionDetailsThunder(def stbName, def executionName, def scriptName, def executionResult, def startExecutionTime, def timedifference, def htmlData, def scriptCount, def applicationUrl, def rerun){
		def executionId
		def executionDeviceId
		try{
			Device deviceInstance = Device.findByStbName(stbName)
			def deviceName = deviceInstance?.stbName
			def category = deviceInstance?.category
			Execution.withTransaction{
			Execution execution = new Execution()
			execution.name = executionName
			if(scriptName == "Multiple Scripts" || scriptCount == 0)
			{
			    execution.script = scriptName
				execution.scriptGroup = ""
			}else{
				execution.script = ""
				execution.scriptGroup = scriptName
			}
			execution.device = deviceName
			execution.executionStatus = INPROGRESS_STATUS
			execution.result = executionResult
			execution.dateOfExecution = startExecutionTime
			execution.groups = getGroup()
			execution.applicationUrl = applicationUrl
			if((rerun?.toString().equals("on"))){
				execution.isRerunRequired = true
			}else{
				execution.isRerunRequired = false
			}
			execution.isBenchMarkEnabled = false
			execution.isStbLogRequired = false
			execution.isSystemDiagnosticsEnabled = false
			execution.rerunOnFailure= false
			execution.scriptCount = scriptCount
			execution.category = Category.RDKV_THUNDER.toString()
			if(!execution.save(flush:true)) {
				log.error "Error saving Execution instance : ${execution.errors}"
			}
			executionId = execution?.id
			}
			ExecutionDevice.withTransaction{
			Execution execution = Execution.findById(executionId)
			ExecutionDevice executionDevice = new ExecutionDevice()
			executionDevice.execution = Execution.findByName(executionName)
			executionDevice.dateOfExecution = execution.dateOfExecution
			executionDevice.executionTime = timedifference
			executionDevice.device = deviceName
			executionDevice.boxType = deviceInstance?.boxType?.name
			executionDevice.deviceIp = deviceInstance?.stbIp
			executionDevice.status = UNDEFINED_STATUS
			executionDevice.category = execution.category
			executionDevice.buildName = "Image name not available"
			if(!executionDevice.save(flush:true)) {
				println "error : "+executionDevice?.errors
			}
			executionDeviceId = executionDevice?.id
			}
		}catch(Exception e){
			e.printStackTrace()
		}
		return [
			executionId,
			executionDeviceId
		]
	}
	
	/**
	 * Method to save the execution and execution device details for script group /multiple script execution
	 * @return
	 */
	def saveGroupExecutionData(String execName, String scriptName, String deviceName, String scriptGroupName, String result, String executionStatus,String outputData, String category, def url, def rerun,
		def isBenchMark, def isSystemDiagnostics,def  isLogReqd) {
		def deviceInstance = Device.findByStbName(deviceName)
		boolean update = false
		Execution execution
		ExecutionDevice executionDevice
		ExecutionResult executionResult
		def executionId
		def executionResultId
		def executionDeviceId
		try {
			Execution.withTransaction {
				execution = Execution.findByName(execName)
				if( execution == null ) {
					execution = new Execution()
					execution.dateOfExecution = new Date()
					execution.name = execName
					execution.script = scriptName
					execution.device = deviceName
					execution.scriptGroup = scriptGroupName
					execution.version = -1
					execution.applicationUrl = url
					execution.isRerunRequired = false
					execution.isBenchMarkEnabled = isBenchMark?.equals(TRUE)? true: false
					execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals(TRUE)? true: false
					execution.isStbLogRequired = isLogReqd?.equals(TRUE)? true: false
					execution.rerunOnFailure = rerun?.equals(TRUE)? true: false
					execution.category = Utility.getCategory(category)
				} else {
					update = true
				}
				execution.result = result
				execution.executionStatus = executionStatus
				execution.outputData = outputData
				def executionSaveStatus = execution.save(flush:true)
				if(executionSaveStatus != null ) {
					executionId = executionSaveStatus.id
				}else{
				    println "error : "+execution?.errors
				}
				def executionObjectData = Execution.executeQuery("select name from Execution where id=:executionId",[executionId:executionId])
			}
			if(!update) {
				if(execution != null){
					ExecutionDevice.withTransaction {
						executionDevice = new ExecutionDevice()
						executionDevice.execution = Execution.findByName(execName)
						executionDevice.dateOfExecution = new Date()
						executionDevice.device = deviceInstance?.stbName
						executionDevice.deviceIp = deviceInstance?.stbIp
						executionDevice.status = UNDEFINED_STATUS
						executionDevice.category = Category.RDKV_THUNDER.toString()
						executionDevice.boxType =  deviceInstance?.boxType?.name
						executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
						def savedexecutionDevice = executionDevice.save(flush:true)
						if(savedexecutionDevice){
							executionDeviceId = savedexecutionDevice.id
						}else{
						    println "error : "+executionDevice?.errors
						}
						def executionDeviceObjectData = ExecutionDevice.executeQuery("select device from ExecutionDevice where id=:executionDeviceId",[executionDeviceId:executionDeviceId])
					}
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
		return [
			executionId,
			executionDeviceId
		]
	}

	/**
	 * Method to save execution , execution device and execution result details for single script executions
	 * @param executionName
	 * @param executionResult
	 * @param params
	 * @param htmlData
	 * @param timedifference
	 * @param realPath
	 * @return
	 */
	public boolean saveExecutionDetailsThunder(def executionName,boolean executionResult, def params, def htmlData, def timedifference, def realPath){
		def executionSaveStatus = true
		try {
			Device deviceInstance = Device.findById(params?.devices)
			def deviceName = deviceInstance?.stbName
			Execution execution = new Execution()
			execution.name = executionName
			execution.script = params?.scriptsThunder
			execution.executionTime = timedifference
			execution.realExecutionTime = timedifference
			execution.device = deviceName
			execution.scriptGroup = ""
			execution.executionStatus = COMPLETED_STATUS
			if(executionResult){
				execution.result = SUCCESS_STATUS
			}else{
				execution.result = FAILURE_STATUS
			}
			execution.dateOfExecution = new Date()
			execution.groups = getGroup()
			execution.applicationUrl = params?.grailsUrl
			if((params.rerun?.toString().equals("on"))){
				execution.isRerunRequired = true
			}else{
				execution.isRerunRequired = false
			}
			execution.isBenchMarkEnabled = false
			execution.isStbLogRequired = false
			execution.isSystemDiagnosticsEnabled = false
			execution.rerunOnFailure= false
			execution.scriptCount = 0
			execution.realExecutionTime = timedifference
			execution.category = Utility.getCategory(params?.category)
			execution.deviceGroup = "STORM"
			if(! execution.save(flush:true)) {
				executionSaveStatus = false
				execution.errors.allErrors.each {
					println "error : "+it
				}
			}
			ExecutionDevice executionDevice = new ExecutionDevice()
			executionDevice.execution = Execution.findByName(executionName)
			executionDevice.dateOfExecution = execution.dateOfExecution
			executionDevice.executionTime = timedifference
			executionDevice.device = deviceInstance?.stbName
			executionDevice.boxType = deviceInstance?.boxType?.name
			executionDevice.deviceIp = deviceInstance?.stbIp
			executionDevice.status = UNDEFINED_STATUS
			executionDevice.category = Utility.getCategory(params?.category)
			executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
			executionDevice.save(flush:true)
			def executionResultObject = new ExecutionResult()
			executionResultObject.execution = execution
			executionResultObject.executionDevice = executionDevice
			executionResultObject.script = execution.script
			executionResultObject.device = executionDevice.device
			executionResultObject.execDevice = null
			executionResultObject.deviceIdString = null
			executionResultObject.status = execution.result
			executionResultObject.dateOfExecution = execution.dateOfExecution
			executionResultObject.category =execution.category
			executionResultObject.executionOutput = htmlData
			if(!executionResultObject.save(flush:true)) {
				println "error : "+executionResultObject?.errors
			}
			boolean versionFilecreated = StormExecuter.createThunderVersionFile(realPath, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
			boolean serverConsoleLogFilecreated =StormExecuter.writeServerConsoleLogFileData(grailsApplication, realPath,  execution?.id, executionDevice?.id, executionResultObject?.id, execution?.script, executionName)//To copy contents of serverconsolelog file to logs.. folder
		}
		catch(Exception th) {
			th.printStackTrace()
			executionSaveStatus = false
		}
		return executionSaveStatus
	}
	
	/**
	 * Method to get the group of the logged in user
	 * @return
	 */
	def Groups getGroup(){
		def user = User.findByUsername(SecurityUtils.subject.principal)
		def group = Groups.findById(user?.groupName?.id)
		return group
	}
	
	/**
	 * Function to format execution time for thunder scripts
	 */
	def truncateTimeTaken ( String executionTime )
	{
		try {
			if(executionTime.contains(".") ){
					int index = executionTime.indexOf(".")
					if((index + 3) < executionTime.length() ){
						executionTime = executionTime?.substring(0, index+3);
					}
				}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return 	executionTime
	}
	
	/**
	 * Method to return the json result of a third party execution
	 * @param execName
	 * @param appurl
	 * @param realPath
	 * @return
	 */
	def thirdPartyJsonResultFromThunderController(final String execName, final String appurl,def realPath ){
		def appUrl = appurl + "/thunder/getDetailedTestResultThunder?execResId="
		String url
		Execution executionInstance = Execution.findByName(execName)
		def executionDevice = ExecutionDevice.findByExecution(executionInstance)
		def multiple = false
		def executionResult
		if(executionInstance?.script == MULTIPLESCRIPT || executionInstance?.scriptGroup){
			executionResult = ExecutionResult.findAllByExecution(executionInstance)
			multiple = true
		}else{
		    executionResult = ExecutionResult.findByExecution(executionInstance)
		}
		JsonObject executionNode
		executionNode = new JsonObject()
		executionNode.addProperty("ExecutionName",execName)
		String execStatus
		if(executionInstance?.executionStatus){
			execStatus = executionInstance?.executionStatus
		}
		else{
			execStatus = "IN-PROGRESS"
		}
		executionNode.addProperty("ExecutionStatus",execStatus.toString())
		executionNode.addProperty("Device Name", executionDevice?.device.toString())
		if(multiple){
			def scriptCounter = 0
			executionResult.each{execResult ->
				scriptCounter = scriptCounter + 1
				try
				{
					url = appUrl + execResult?.id.toString()
				}
				catch(Exception e){
					e.printStackTrace()
				}
				executionNode.addProperty("ScriptName_"+scriptCounter,execResult?.script)
				executionNode.addProperty("LogUrl_"+scriptCounter,url.toString())
			}
		}else{
		try
		{
			url = appUrl + executionResult?.id.toString()
		}
		catch(Exception e){
			e.printStackTrace()
		}
		executionNode.addProperty("ScriptName",executionInstance?.script)
		executionNode.addProperty("LogUrl",url.toString())
		}
		return executionNode
	}
	
	/**
	 * Method to return the value of a property after reading from a config file
	 * @param configFile
	 * @param key
	 * @return
	 */
	public static String getConfigProperty(File configFile, String key) {
		try {
			Properties prop = new Properties()
			if (configFile.exists()) {
				InputStream is = new FileInputStream(configFile);
				prop.load(is)
				String value = prop.getProperty(key)
				if (value != null && !value.isEmpty()) {
					return value
				}
			}else{
				println "No Config File !!! "
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return null
	}
	
}