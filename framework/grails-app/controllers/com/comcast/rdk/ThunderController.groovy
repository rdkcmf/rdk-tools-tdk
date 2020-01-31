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

import org.apache.shiro.SecurityUtils
import static com.comcast.rdk.Constants.*
import static org.quartz.CronScheduleBuilder.*
import static org.quartz.DateBuilder.*
import static org.quartz.JobKey.*
import static org.quartz.TriggerBuilder.*
import static org.quartz.TriggerKey.*
import grails.converters.JSON

import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Map;
import java.util.date.*
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

import java.util.Properties;
import org.codehaus.groovy.grails.web.json.JSONObject
import org.custommonkey.xmlunit.*
import org.quartz.JobBuilder
import org.quartz.JobDetail
import org.quartz.Trigger
import org.quartz.impl.triggers.SimpleTriggerImpl

import rdk.test.tool.*

import com.google.gson.Gson;
import com.google.gson.JsonArray
import com.google.gson.JsonObject

class ThunderController {
	/**
	 * Injects the thunderService.
	 */
	def thunderService
	/**
	 * Injects the executionService
	 */
	def executionService
	
	/**
	 * Injects the deviceStatusService
	 */
	def deviceStatusService
	
	/**
	 * Injects the executeScriptService.
	 */
	def executeScriptService
	
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication
	
	/**
	 * Injects the scriptService.
	 */
	def scriptService

	/**
	 * Method to call thunder script execution function in thunderservice.
	 * @return
	 */
	def executeThunderScript(){
		String htmlData = ""
		htmlData = thunderService.executeThunderScripts(params, getRealPath())
		render htmlData
	}
	
	/**
	 * Method to get the real path to rdk-test-tool directory in VM.
	 * @return
	 */
	def getRealPath(){
		return request.getSession().getServletContext().getRealPath("/")
	}
	
	/**
	 *  Method to execute single thunder script using REST-API
	 * @param stbName
	 * @param scriptName
	 * @return
	 */
	def thirdPartySingleTestExecutionThunder(final String stbName, final String scriptName){
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_TIME_OUT = thunderService.getConfigProperty(configFile, Constants.STORM_TIME_OUT)
		def STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
		def STORM_COUNTER_MAXIMUM = (STORM_TIME_OUT_INTEGER * 60 * 1000)/(10000)
		def htmlData = "No data"
		def deviceName
		def executionName
		JsonObject jsonOutData = new JsonObject()
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
		Calendar cal = Calendar.getInstance()
		def deviceInstance = Device.findByStbName(stbName)
		deviceName = deviceInstance?.stbName
		executionName = CI_EXECUTION+deviceName+"-"+dateFormat.format(cal.getTime()).toString()
		boolean scriptNotPresent = false
		def scriptObject = ScriptFile.findByScriptNameAndCategory(scriptName,Category.RDKV_THUNDER)
		if(!(scriptService?.totalThunderScriptList?.contains(scriptObject))){
			scriptNotPresent = true
		}
		if ((scriptName != null)  && !scriptNotPresent){
			def startExecutionTime = new Date()
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
			if((status.equals( Status.FREE.toString() ))){
				boolean executionResult = false
				boolean executionFinished = false
				def waitCounter = 0
				StormExecuter.executeThunderScript(grailsApplication,scriptName,deviceInstance?.stbIp,executionName)
				sleep(10000)
				waitCounter++
				executionFinished = StormExecuter.checkThunderExecution(grailsApplication, scriptName, executionName)
				while(!executionFinished && waitCounter<STORM_COUNTER_MAXIMUM){
					sleep(10000)
					executionFinished = StormExecuter.checkThunderExecution(grailsApplication, scriptName, executionName)
					if(executionFinished){
						break;
					}
					waitCounter++
				}
				if(waitCounter==STORM_COUNTER_MAXIMUM && !executionFinished){
					executionResult = false
				}else if(executionFinished){
					executionResult = StormExecuter.parseThunderResult(grailsApplication,scriptName,executionName)
				}
				def endExecutionTime = new Date()
				long timeDifference = endExecutionTime.getTime() - startExecutionTime.getTime()
				long timeDifferenceInSeconds = (long)(timeDifference/(1000))
				float timeDifferenceInMinutes = (float)(timeDifferenceInSeconds/(60.0))
				String timeDifferenceInMinutesString = timeDifferenceInMinutes.toString()
				htmlData = StormExecuter.returnThunderLogFile(grailsApplication, scriptName, executionName)
				boolean executionSaveStatus = saveExecutionDetailsThunder(stbName, executionName, scriptName, executionResult, startExecutionTime, timeDifferenceInMinutesString, htmlData)
				String url = getApplicationUrl()
				url = url + "/thunder/thirdPartyJsonResultThunder?execName=${executionName}"
				jsonOutData.addProperty("status", "RUNNING")
				jsonOutData.addProperty("result",url )
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
			}
			else{
				log.error "Device status noT FREE"
				jsonOutData.addProperty("status", "Device is not free to execute scripts")
				jsonOutData.addProperty("result", "None")
			}
		} else {
			log.error "Couldn't find the test.."
			jsonOutData.addProperty("status", "TEST NOT FOUND")
			jsonOutData.addProperty("result", "None")
		}
		render jsonOutData
	}
	
	/**
	 * Method to execute multiple thunder scripts using REST-API
	 * @param stbName
	 * @param scripts
	 * @return
	 */
	def thirdPartyMultipleTestExecutionThunder(final String stbName, final String scripts){
		def scriptList  = scripts?.tokenize(",")
		boolean scriptNotPresent = false
		for(String script : scriptList){
			def scriptObject = ScriptFile.findByScriptNameAndCategory(script,Category.RDKV_THUNDER)
			if(!(scriptService?.totalThunderScriptList?.contains(scriptObject))){
				scriptNotPresent = true
				break
			}
		}
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_TIME_OUT = thunderService.getConfigProperty(configFile, Constants.STORM_TIME_OUT)
		def STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
		def STORM_COUNTER_MAXIMUM = (STORM_TIME_OUT_INTEGER * 60 * 1000)/(10000)
		def htmlData = ""
		def deviceName
		def executionName
		def scriptCount
    	boolean executionSaveStatus
		boolean aborted = false
		String executionLogData = ""
		executionLogData = executionLogData + HTML_BR + HTML_BR
		JsonObject jsonOutData = new JsonObject()
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
		Calendar cal = Calendar.getInstance()
		def deviceInstance = Device.findByStbName(stbName)
		deviceName = deviceInstance?.stbName
		executionName = CI_EXECUTION+deviceName+"-"+dateFormat.format(cal.getTime()).toString()
		String STORM_FRAMEWORK_LOCATION = thunderService.getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION)
		String STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX = STORM_FRAMEWORK_LOCATION+"src/logs/"
		String fullLogFileAbsolutePath = STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX+executionName+"_fullLog.log"
		File fullLog = new File(fullLogFileAbsolutePath)
		boolean fullLogFileCreated = false
		if(fullLog.createNewFile()){
			fullLogFileCreated = true
		}
		String scriptName = MULTIPLESCRIPT
		def executionResult = UNDEFINED_STATUS
		long timeDifferenceInSeconds
		float timeDifferenceInMinutes
		if ((scriptList?.size() > 0)  && !scriptNotPresent){
			scriptCount = scriptList?.size()
			String status = ""
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
			def startExecutionTime = new Date()
			def executionId
			def executionDeviceId
			def executionResultId
			if((status.equals( Status.FREE.toString() ))){
				(executionId, executionDeviceId) = saveMultipleScriptExecutionDetailsThunder(stbName, executionName, scriptName, executionResult, startExecutionTime, timeDifferenceInSeconds, htmlData, scriptCount)
				Execution execution = Execution.findById(executionId)
				ExecutionDevice executionDevice = ExecutionDevice.findById(executionDeviceId)
				for(int i=0; i<scriptList.size(); i++) {
					aborted = executionService.abortList.contains(executionId?.toString())
					if(!aborted && !(status.equals(Status.NOT_FOUND.toString()) || status.equals(Status.HANG.toString()))){
						boolean executionResultBool = false
						boolean executionFinished = false
						def waitCounter = 0
						DateFormat dateFormat1 = new SimpleDateFormat(DATE_FORMAT)
						Calendar cal1 = Calendar.getInstance()
						String timeStamp = dateFormat1.format(cal1.getTime()).toString()
						StormExecuter.executeThunderScript(grailsApplication,scriptList[i],deviceInstance?.stbIp,executionName)
						sleep(10000)
						waitCounter++
						executionFinished = StormExecuter.checkThunderExecution(grailsApplication, scriptList[i], executionName)
						while(!executionFinished && waitCounter<STORM_COUNTER_MAXIMUM){
							sleep(10000)
							executionFinished = StormExecuter.checkThunderExecution(grailsApplication, scriptList[i], executionName)
							if(executionFinished){
								break
							}
							waitCounter++
						}
						if(waitCounter==STORM_COUNTER_MAXIMUM && !executionFinished){
							executionResultBool = false
						}else if(executionFinished){
						    executionResultBool = StormExecuter.parseThunderResult(grailsApplication, scriptList[i], executionName)
						}
						htmlData = StormExecuter.returnThunderLogFile(grailsApplication, scriptList[i], executionName)
						def htmlDataForAppend  = timeStamp + HTML_BR + EXECUTING_SCRIPT + scriptList[i] + HTML_BR + LOG_SEPARATION_LINE_STRING + HTML_BR + htmlData
						executionLogData = executionLogData + timeStamp + HTML_BR + EXECUTING_SCRIPT + scriptList[i] + HTML_BR + LOG_SEPARATION_LINE_STRING + HTML_BR + htmlData + HTML_BR + HTML_BR
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
						ExecutionResult.withTransaction{
						def executionResultObject = new ExecutionResult()
						executionResultObject.execution = execution
						executionResultObject.executionDevice = executionDevice
						executionResultObject.script = scriptList[i]
						executionResultObject.device = executionDevice.device
						executionResultObject.execDevice = null
						executionResultObject.deviceIdString = null
						if(executionResultBool){
							executionResultObject.status = SUCCESS_STATUS
						}else{
							executionResultObject.status = FAILURE_STATUS
						}
						executionResultObject.dateOfExecution = execution.dateOfExecution
						executionResultObject.category = execution.category
						executionResultObject.executionOutput = htmlData
						if(!executionResultObject.save(flush:true)) {
							executionSaveStatus = false
						}else {
								executionResultId = executionResultObject.id
						}
						}
						boolean serverConsoleLogFilecreated =StormExecuter.writeServerConsoleLogFileData(grailsApplication, realPath,  executionId, executionDeviceId, executionResultId, scriptList[i], executionName)
					}else{
						if(aborted && executionService.abortList.contains(executionId?.toString())){
							break
						}
					}
				}
				def endExecutionTime = new Date()
				long timeDifference = endExecutionTime.getTime() - startExecutionTime.getTime()
				timeDifferenceInSeconds = (long)(timeDifference/(1000))
				timeDifferenceInMinutes = (float)(timeDifferenceInSeconds/(60.0))
				String timeDifferenceInMinutesString = timeDifferenceInMinutes.toString()
				def failureListCount = ExecutionResult.executeQuery("SELECT count(*) from ExecutionResult where execution_id = :execId and status like :status",
				[execId:executionId, status:"FAILURE"])
				def statusExecution = SUCCESS_STATUS
				if(failureListCount[0] > 0) {
					statusExecution = FAILURE_STATUS
				}
				if(aborted && executionService.abortList.contains(executionId?.toString())){
					Execution.executeUpdate("update Execution e set e.executionStatus = :completedStatus , e.result = :newStatus, e.realExecutionTime = :timeDifference, e.executionTime = :timeDifference, e.outputData = :outputData where e.id = :execId",
					[newStatus: statusExecution, execId: executionId, completedStatus: ABORTED_STATUS, timeDifference: timeDifferenceInMinutesString, outputData: executionLogData])
					executionService.abortList.remove(executionId?.toString())
				}else{
					Execution.executeUpdate("update Execution e set e.executionStatus = :completedStatus , e.result = :newStatus, e.realExecutionTime = :timeDifference, e.executionTime = :timeDifference, e.outputData = :outputData where e.id = :execId",
						[newStatus: statusExecution, execId: executionId, completedStatus: COMPLETED_STATUS, timeDifference: timeDifferenceInMinutesString, outputData: executionLogData])
				}	
				ExecutionDevice.executeUpdate("update ExecutionDevice e set e.executionTime = :timeDifference where e.id = :execDeviceId",
					[execDeviceId: executionDeviceId, timeDifference: timeDifferenceInMinutesString])
				boolean versionFilecreated = StormExecuter.createThunderVersionFile(realPath, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
				println " multipleTestRestExecutionThunder [stbName="+stbName+"] [scripts="+scripts+"] [executionName="+executionName+"] [Triggered Execution]"
				String url = getApplicationUrl()
				url = url + "/thunder/thirdPartyJsonResultThunder?execName=${executionName}"
				jsonOutData.addProperty("status", "RUNNING")
				jsonOutData.addProperty("result",url )
			}
			else {
				log.error "device not free ."
				jsonOutData.addProperty("status", "Device is not free to execute scripts")
				jsonOutData.addProperty("result", "None")
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
		} else {
			log.error "script list empty or script not found..."
			jsonOutData.addProperty("status", "TESTS NOT FOUND")
			jsonOutData.addProperty("result", "None")
		}
		render jsonOutData
	}
	
	/**
	 * Method to execute test suites using REST-API
	 * @param stbName
	 * @param suiteName
	 * @return
	 */
	def thirdPartySuiteExecutionThunder(final String stbName, final String suiteName){
		boolean suiteNotPresent = false
		if((ScriptGroup.findByName(suiteName) == null) || (ScriptGroup.findByName(suiteName) == "")){
			suiteNotPresent = true
		}
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_TIME_OUT = thunderService.getConfigProperty(configFile, Constants.STORM_TIME_OUT)
		def STORM_TIME_OUT_INTEGER = Integer.parseInt(STORM_TIME_OUT)
		def STORM_COUNTER_MAXIMUM = (STORM_TIME_OUT_INTEGER * 60 * 1000)/(10000)
		ScriptGroup scriptGroup = ScriptGroup.findByName(suiteName)
		def scriptsList
		if(scriptGroup){
			scriptsList  = scriptGroup?.scriptList
		}
		boolean scriptNotPresent = false
		for(String script : scriptsList){
			def scriptObject = ScriptFile.findByScriptNameAndCategory(script,Category.RDKV_THUNDER)
			if(!(scriptService?.totalThunderScriptList?.contains(scriptObject))){
				scriptNotPresent = true
				break
			}
		}
		def htmlData = ""
		def deviceName
		def executionName
		def scriptCount
		Long executionResultId
		boolean executionSaveStatus
		boolean aborted = false
		String executionLogData = ""
		executionLogData = executionLogData + HTML_BR + HTML_BR
		JsonObject jsonOutData = new JsonObject()
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
		Calendar cal = Calendar.getInstance()
		def deviceInstance = Device.findByStbName(stbName)
		deviceName = deviceInstance?.stbName
		executionName = CI_EXECUTION+deviceName+"-"+dateFormat.format(cal.getTime()).toString()
		String STORM_FRAMEWORK_LOCATION = thunderService.getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION)
		String STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX = STORM_FRAMEWORK_LOCATION+"src/logs/"
		String fullLogFileAbsolutePath = STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX+executionName+"_fullLog.log"
		File fullLog = new File(fullLogFileAbsolutePath)
		boolean fullLogFileCreated = false
		if(fullLog.createNewFile()){
			fullLogFileCreated = true
		}
		String scriptName = scriptGroup?.name
		def executionResult = UNDEFINED_STATUS
		long timeDifferenceInSeconds
		float timeDifferenceInMinutes
		if ( (scriptsList?.size() > 0) && !suiteNotPresent && !scriptNotPresent){
			scriptCount = scriptsList?.size()
			String status = ""
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
			def startExecutionTime = new Date()
			def executionId
			def executionDeviceId
			if((status.equals( Status.FREE.toString() ))){
				(executionId, executionDeviceId) = saveMultipleScriptExecutionDetailsThunder(stbName, executionName, scriptName, executionResult, startExecutionTime, timeDifferenceInSeconds, htmlData, scriptCount)
				Execution execution = Execution.findById(executionId)
				ExecutionDevice executionDevice = ExecutionDevice.findById(executionDeviceId)
				for(int i=0; i<scriptsList.size(); i++) {
					aborted = executionService.abortList.contains(executionId?.toString())
					if(!aborted && !(status.equals(Status.NOT_FOUND.toString()) || status.equals(Status.HANG.toString()))){
						boolean executionResultBool = false
						boolean executionFinished = false
						def waitCounter = 0
						DateFormat dateFormat1 = new SimpleDateFormat(DATE_FORMAT)
						Calendar cal1 = Calendar.getInstance()
						def timeStamp = dateFormat1.format(cal1.getTime()).toString()
						try{
						    StormExecuter.executeThunderScript(grailsApplication,scriptsList[i]?.scriptName,deviceInstance?.stbIp,executionName)
						}catch(Exception e){
						    e.printStackTrace()
						}
						sleep(10000)
						waitCounter++
						executionFinished = StormExecuter.checkThunderExecution(grailsApplication, scriptsList[i]?.scriptName, executionName)
						while(!executionFinished && waitCounter<STORM_COUNTER_MAXIMUM){
							sleep(10000)
							executionFinished = StormExecuter.checkThunderExecution(grailsApplication, scriptsList[i]?.scriptName, executionName)
							if(executionFinished){
								break
							}
							waitCounter++
						}
						if(waitCounter==STORM_COUNTER_MAXIMUM && !executionFinished){
							executionResultBool = false
						}else if(executionFinished){
						    executionResultBool = StormExecuter.parseThunderResult(grailsApplication, scriptsList[i]?.scriptName, executionName)
						}
						htmlData = StormExecuter.returnThunderLogFile(grailsApplication, scriptsList[i]?.scriptName, executionName)
						def htmlDataForAppend  = timeStamp + HTML_BR + EXECUTING_SCRIPT + scriptsList[i]?.scriptName + HTML_BR + LOG_SEPARATION_LINE_STRING + HTML_BR + htmlData
						executionLogData = executionLogData + timeStamp + HTML_BR + EXECUTING_SCRIPT + scriptsList[i]?.scriptName + HTML_BR + LOG_SEPARATION_LINE_STRING + HTML_BR + htmlData + HTML_BR + HTML_BR
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
						def executionResultObject = new ExecutionResult()
						executionResultObject.execution = execution
						executionResultObject.executionDevice = executionDevice
						executionResultObject.script = scriptsList[i]?.scriptName
						executionResultObject.device = executionDevice?.device
						executionResultObject.execDevice = null
						executionResultObject.deviceIdString = null
						if(executionResultBool){
							executionResultObject.status = SUCCESS_STATUS
						}else{
							executionResultObject.status = FAILURE_STATUS
						}
						executionResultObject.dateOfExecution = execution.dateOfExecution
						executionResultObject.category = execution.category
						executionResultObject.executionOutput = htmlData
						if(!executionResultObject.save(flush:true)) {
							executionSaveStatus = false
						}else {
								executionResultId = executionResultObject.id
						}
						boolean serverConsoleLogFilecreated =StormExecuter.writeServerConsoleLogFileData(grailsApplication, realPath,  execution?.id, executionDevice?.id, executionResultId, executionResultObject?.script, executionName)
					}else{
						if(aborted && executionService.abortList.contains(executionId?.toString())){
							break
						}
					}
				}
				def endExecutionTime = new Date()
				long timeDifference = endExecutionTime.getTime() - startExecutionTime.getTime()
				timeDifferenceInSeconds = (long)(timeDifference/(1000))
				timeDifferenceInMinutes = (float)(timeDifferenceInSeconds/(60.0))
				String timeDifferenceInMinutesString = timeDifferenceInMinutes.toString()
				def failureListCount = ExecutionResult.executeQuery("SELECT count(*) from ExecutionResult where execution_id = :execId and status like :status",
				[execId:executionId, status:"FAILURE"])
				def statusExecution = SUCCESS_STATUS
				if(failureListCount[0] > 0) {
					statusExecution = FAILURE_STATUS
				}
				if(aborted && executionService.abortList.contains(executionId?.toString())){
					Execution.executeUpdate("update Execution e set e.executionStatus = :completedStatus , e.result = :newStatus, e.realExecutionTime = :timeDifference, e.executionTime = :timeDifference, e.outputData = :outputData where e.id = :execId",
					[newStatus: statusExecution, execId: executionId, completedStatus: ABORTED_STATUS, timeDifference: timeDifferenceInMinutesString, outputData: executionLogData])
					executionService.abortList.remove(executionId?.toString())
				}else{
					Execution.executeUpdate("update Execution e set e.executionStatus = :completedStatus , e.result = :newStatus, e.realExecutionTime = :timeDifference, e.executionTime = :timeDifference, e.outputData = :outputData where e.id = :execId",
					[newStatus: statusExecution, execId: executionId, completedStatus: COMPLETED_STATUS, timeDifference: timeDifferenceInMinutesString, outputData: executionLogData])			
				}
				ExecutionDevice.executeUpdate("update ExecutionDevice e set e.executionTime = :timeDifference where e.id = :execDeviceId",
					[execDeviceId: executionDeviceId, timeDifference: timeDifferenceInMinutesString])
				boolean versionFilecreated = StormExecuter.createThunderVersionFile(realPath, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
				println " suiteRestExecutionThunder [stbName="+stbName+"] [suitename="+suiteName+"] [executionName="+executionName+"] [Triggered Execution]"
				String url = getApplicationUrl()
				url = url + "/thunder/thirdPartyJsonResultThunder?execName=${executionName}"
				jsonOutData.addProperty("status", "RUNNING")
				jsonOutData.addProperty("result",url )
			}
			else {
				log.error "device not free ."
				jsonOutData.addProperty("status", "Device is not free to execute scripts")
				jsonOutData.addProperty("result", "None")
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
		} else {
			log.error "script list empty or script not found..."
			jsonOutData.addProperty("status", "TESTS NOT FOUND")
			jsonOutData.addProperty("result", "None")
		}
		render jsonOutData
	}
	
	/**
	 * Method to get the thirdparty result as a json object
	 * @param execName
	 * @param appurl
	 * @return
	 */
	def thirdPartyJsonResultThunder(final String execName, final String appurl ){
		JsonObject thunderNode = thunderService.thirdPartyJsonResultFromThunderController(execName, getApplicationUrl() ,getRealPath())
		render thunderNode
	}
	
	/**
	 * Method to get the detailed result as a json object
	 * @param execResId
	 * @return
	 */
	def getDetailedTestResultThunder(final String execResId){
		JsonObject resultNode = new JsonObject()
		if(execResId){
			ExecutionResult executionResult = ExecutionResult.findById(execResId)
			resultNode.addProperty("ExecutionName",executionResult?.execution?.name.toString())
			resultNode.addProperty("Device",executionResult?.device.toString())
			resultNode.addProperty("Script",executionResult?.script.toString())
			resultNode.addProperty("Status",executionResult?.status.toString())
			resultNode.addProperty("LogData",executionResult?.executionOutput.toString())
			def executionInstance = Execution.findById(executionResult?.execution?.id)
			resultNode.addProperty("ServerConsoleLogURL",executionInstance?.applicationUrl+"/thunder/getServerConsoleLog?execResId="+executionResult?.id)
		}else{
			render"Execution result not found"
		}
		render resultNode
	}
	
	/**
	 * Method to get the server console log 
	 * @param execResId
	 * @return
	 */
	def getServerConsoleLog(final String execResId){
		ExecutionResult executionResult = ExecutionResult.findById(execResId)
		def serverConsoleFileData = "Server Console Log empty"
		if(executionResult){
			try {
				serverConsoleFileData = executionService.getAgentConsoleLogData(request.getRealPath('/'), executionResult?.execution?.id?.toString(), executionResult?.executionDevice?.id?.toString(),executionResult?.id?.toString())
				if(serverConsoleFileData){
					serverConsoleFileData =serverConsoleFileData.trim()
					if(serverConsoleFileData.length() == 0){
						serverConsoleFileData = "No server console log available"
					}
				}else{
					serverConsoleFileData = "No server console log available"
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}else{
			serverConsoleFileData = "No execution result available with the given execResId"
		}
		render serverConsoleFileData
	}
	
	/**
	 * Method to save the execution and execution device details for script group /multiple script REST API execution 
	 * @param stbName
	 * @param executionName
	 * @param scriptName
	 * @param executionResult
	 * @param startExecutionTime
	 * @param timedifference
	 * @param htmlData
	 * @param scriptCount
	 * @return
	 */
	def saveMultipleScriptExecutionDetailsThunder(def stbName, def executionName, def scriptName, def executionResult, def startExecutionTime, def timedifference, def htmlData, def scriptCount){
		def executionId
		def executionDeviceId
		try{
			Device deviceInstance = Device.findByStbName(stbName)
			def deviceName = deviceInstance?.stbName
			def category = deviceInstance?.category
			Execution.withTransaction{
			Execution execution = new Execution()
			execution.name = executionName
			execution.device = deviceName
			if(scriptName == "Multiple Scripts")
			{
				execution.script = scriptName
				execution.scriptGroup = ""
			}else{
				execution.script = ""
				execution.scriptGroup = scriptName
			}
			execution.executionStatus = INPROGRESS_STATUS
			execution.result = executionResult
			execution.dateOfExecution = startExecutionTime
			execution.groups = getGroup()
			execution.applicationUrl = getApplicationUrl()
			execution.isRerunRequired = false
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
	 * Method to save execution , execution device and execution result details for single script REST API executions
	 * @param stbName
	 * @param executionName
	 * @param scriptName
	 * @param executionResult
	 * @param startExecutionTime
	 * @param timedifference
	 * @param htmlData
	 * @return
	 */
	def saveExecutionDetailsThunder(def stbName, def executionName, def scriptName, def executionResult, def startExecutionTime, def timedifference, def htmlData){
		boolean executionSaveStatus = false
		try{
		Device deviceInstance = Device.findByStbName(stbName)
		def deviceName = deviceInstance?.stbName
		def category = deviceInstance?.category
		Execution execution = new Execution()
		execution.name = executionName
		execution.script = scriptName
		execution.device = deviceName
		execution.realExecutionTime = timedifference
		execution.executionTime = timedifference
		execution.scriptGroup = ""
		execution.executionStatus = COMPLETED_STATUS
		if(executionResult){
			execution.result = SUCCESS_STATUS
		}else{
			execution.result = FAILURE_STATUS
		}
		execution.dateOfExecution = startExecutionTime
		execution.groups = getGroup()
		execution.applicationUrl = getApplicationUrl()
		execution.isRerunRequired = false
		execution.isBenchMarkEnabled = false
		execution.isStbLogRequired = false
		execution.isSystemDiagnosticsEnabled = false
		execution.rerunOnFailure= false
		execution.scriptCount = 1
		execution.category = Category.RDKV_THUNDER.toString()
		execution.outputData = htmlData
		if(!execution.save(flush:true)) {
			log.error "Error saving Execution instance : ${execution.errors}"
			executionSaveStatus = false
		}
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
			executionSaveStatus = false
		}
		def executionResultObject = new ExecutionResult()
		executionResultObject.execution = execution
		executionResultObject.executionDevice = executionDevice
		executionResultObject.script = execution.script
		executionResultObject.device = executionDevice.device
		executionResultObject.execDevice = null
		executionResultObject.deviceIdString = null
		executionResultObject.status = execution.result
		executionResultObject.dateOfExecution = execution.dateOfExecution
		executionResultObject.category = execution.category
		executionResultObject.executionOutput = htmlData
		if(!executionResultObject.save(flush:true)) {
			executionSaveStatus = false
		}
		def realPath = getRealPath()
		boolean versionFilecreated = StormExecuter.createThunderVersionFile(realPath, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
		boolean serverConsoleLogFilecreated = StormExecuter.writeServerConsoleLogFileData(grailsApplication, realPath, execution?.id, executionDevice?.id, executionResultObject?.id, execution?.script, executionName)
		}catch(Exception e){
			e.printStackTrace()
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
	 * Method to get the current url and to create
	 * new url upto the application name
	 * @return
	 */
	def String getApplicationUrl(){
		String currenturl = request.getRequestURL().toString();
		String[] urlArray = currenturl.split( URL_SEPERATOR );
		String serverAddr = urlArray[INDEX_TWO]
		if(serverAddr.contains("localhost:")){
			String localAddr = request.getProperties().get("localAddr")
			String localPort = request.getProperties().get("localPort")
			if((!localAddr.startsWith("0:0:0:0:0:0:0:1")) && (!localAddr.startsWith("0.0.0.0"))){
				serverAddr = ""+localAddr+":"+localPort
			}
		}
		String url = urlArray[INDEX_ZERO] + DOUBLE_FWD_SLASH + serverAddr + URL_SEPERATOR + urlArray[INDEX_THREE]
		return url
	}
}