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
package rdk.test.tool

import java.io.File;
import java.io.InputStream;
import java.net.URLConnection;
import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Date;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher
import com.google.gson.JsonObject

import groovy.sql.Sql

import org.quartz.Job
import org.quartz.JobExecutionContext

import com.comcast.rdk.*

import javax.servlet.http.HttpServletRequest

import static com.comcast.rdk.Constants.*

import java.util.regex.Pattern

import org.codehaus.groovy.grails.commons.ConfigurationHolder

import rdk.test.tool.DeviceStatusJob

import org.codehaus.groovy.grails.web.json.JSONObject

import grails.converters.JSON

/**
 * Schedular class to schedule script execution for a future date
 * Quartz Schedular
 * @author sreejasuma
 *
 */
class JobSchedulerService implements Job{

	def grailsApplication
	def dataSource
	boolean transactional = false

	static ExecutorService executorService = Executors.newCachedThreadPool()

	static triggers ={}

	/**
	 * Method which is invoked based on the schedule time
	 * @param context
	 */
	public void execute (JobExecutionContext context) {
		def jobName = context.jobDetail.key.name
		def triggerName = context.trigger.key.name

		try {
			JobDetails jobDetails

			JobDetails.withTransaction {
				jobDetails = JobDetails.findByJobNameAndTriggerName(jobName,triggerName)
			}

			if(jobDetails){
				DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
				Calendar cal = Calendar.getInstance()
				String date = dateFormat.format(cal.getTime()).toString()
				String executionName = KEY_JOB+UNDERSCORE+jobDetails.device+UNDERSCORE+date
				startExecutions(executionName,jobDetails.id)
			}
		} catch (Exception e) {
			e.printStackTrace()
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
			updateTotalExecutionTime(execTimeDifference ?.toString(), executionInstance1?.id)
		}catch (Exception e) {
			println  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to execute the script
	 * @param executionName
	 * @param jobId
	 * @return
	 */
	def startExecutions(final String executionName, final def jobId){
		def filePath
		def scripts = null
		def scriptGrpId = null
		def devices = null
		def realpath
		def url
		def deviceList = []
		List pendingScripts = []
		boolean allocated = false
		def category = null
		boolean combinedTCL = false
		boolean tclCombined =  false
		def deviceInstance //= Device.findById(jobDetails?.device, [lock: true])
		try {
			JobDetails jobDetails
			ExecutionDevice executionDevice
			StringBuilder output = new StringBuilder();
			JobDetails.withTransaction{
				jobDetails = JobDetails.findById(jobId, [lock: true])
				// log.info jobDetails.script
				filePath = jobDetails?.filePath
				scripts = jobDetails?.script
				scriptGrpId = jobDetails?.scriptGroup

				realpath = jobDetails?.realPath
				url = jobDetails?.appUrl
				devices = jobDetails?.device
				category = jobDetails?.category
			}
			//			ScriptService.getScriptNameFileList(realpath)
			def scriptInstance
			def scriptGroupInstance
			def deviceName
			String htmlData = ""
			boolean abortedExecution = false
			boolean pause = false
			def scriptObject
			def scriptName

			DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT);
			Calendar cal = Calendar.getInstance();

			if(devices instanceof String){
				deviceList << devices
				deviceInstance = Device.findById(devices, [lock: true])
				deviceName = deviceInstance?.stbName
			}
			else{
				(devices).each{ deviceid -> deviceList << deviceid }
				deviceName = MULTIPLE
			}

			// to get the category of script or scriptGroup
			//	def category = null

			def repeatCount = jobDetails?.repeatCount
			def deviceId
			def execName
			def executionNameForCheck
			for(int i = 0; i < repeatCount; i++ ){
				executionNameForCheck = null
				deviceList.each{ device ->
					deviceInstance = Device.findById(device)


					def executionSaveStatus = true
					def execution = null
					boolean aborted = false
					deviceId = deviceInstance?.id
					def scriptStatus = true
					def scriptVersionStatus =true
					def scriptId
					String devStatus = ""
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						synchronized (ExecutionController.lock) {
							if(ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
								devStatus = "BUSY"
							}else{
								if((devStatus.equals( Status.FREE.toString() ))){
									if(!ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
										allocated = true
										ExecutionService.deviceAllocatedList.add(deviceInstance?.id)
									}
								}
							}
						}

					}
					catch(Exception eX){
						eX.printStackTrace()
					}
					if(scripts){
						if(scripts.size() > 1){
							scriptName = MULTIPLESCRIPT
							def script = ScriptFile.findByScriptName(scripts.get(0))
							category = script?.category
							if(category == jobDetails?.category){
								category = script?.category
							}else{
								category =   jobDetails?.category
							}
						}
						else{

							def script = scripts[0]
							def scriptFile = ScriptFile.findByScriptName(script)
							if(scriptFile){
								category = scriptFile?.category
								if(category == jobDetails?.category){
									category = scriptFile?.category
								}else{
									category =   jobDetails?.category
								}
							}
							if(category == Category.RDKB_TCL){
								def combainedTclScript =  ScriptService?.combinedTclScriptMap
								combainedTclScript?.each{
									if(it?.value?.toString().contains(script?.toString())){
										combinedTCL = true
									}
								}
								if((ScriptService?.totalTclScriptList?.toString()?.contains(scriptFile?.scriptName?.toString())) && combinedTCL ){
									combainedTclScript?.each{
										if(it?.value?.toString()?.contains(scriptFile?.scriptName?.toString())){
											script = it.key?.toString()
										}
									}
								}
								scriptVersionStatus = true
								//	scriptStatus = Utility.isTclScriptExists(realpath, scriptFile?.scriptName) && Utility.isConfigFileExists(realpath, deviceInstance?.stbName)
								scriptStatus = Utility.isTclScriptExists(realpath, script) && Utility.isConfigFileExists(realpath, deviceInstance?.stbName)
								if(scriptStatus){
									scriptName = scriptFile?.scriptName
								}else{
									//scriptName = script?.toString()
									scriptName = scriptFile?.scriptName //Issue fix : for compound TCL script single script execution
								}
							}
							else{
								def moduleName= ScriptService.scriptMapping.get(scripts[0])
								scriptInstance = getScript(realpath,moduleName, scripts[0], category)

								scriptStatus = validateScriptBoxTypes(scriptInstance,deviceInstance)
								String rdkVersion = getRDKBuildVersion(deviceInstance);
								scriptVersionStatus = validateScriptRDKVersions(scriptInstance,rdkVersion)
								scriptName = scriptInstance?.name
							}
						}
					}else if(scriptGrpId){
						scriptGroupInstance = ScriptGroup.findById(scriptGrpId,[lock: true])
						if(category == null){
							category = scriptGroupInstance.category
						}
					}
					boolean value = false
					if(scriptStatus && scriptVersionStatus){
						value = true
					}else{
						value = false
					}
					if( devStatus.equals( Status.FREE.toString() ) && value){
						if(!ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
							allocated = true
							ExecutionService.deviceAllocatedList.add(deviceInstance?.id)
						}
						if(scriptStatus && scriptVersionStatus){
							if(!executionNameForCheck){
								if(i > 0){
									execName = executionName + UNDERSCORE +i
								}
								else{
									execName = executionName
								}
								int scriptCnt = 0
								if(scriptGroupInstance?.scriptList?.size() > 0){
									scriptCnt = scriptGroupInstance?.scriptList?.size()
								}// Test case  count includes execution result page while executing multiple scripts.
								else if(scriptName.equals("Multiple Scripts")){
									scriptCnt  = scripts?.size()
								}
								Execution.withTransaction { status ->
									try {
										execution = new Execution()
										execution.name = execName
										execution.script = scriptName
										execution.device = deviceName
										execution.applicationUrl = url
										execution.scriptGroup = scriptGroupInstance?.name
										execution.result = UNDEFINED_STATUS
										execution.executionStatus = INPROGRESS_STATUS
										execution.dateOfExecution = new Date()//dateFormat.format(cal.getTime())
										execution.groups = jobDetails?.groups
										execution.isBenchMarkEnabled = jobDetails?.isBenchMark?.equals("true")
										execution.isSystemDiagnosticsEnabled = jobDetails?.isSystemDiagnostics?.equals("true")
										execution.isStbLogRequired= jobDetails.isStbLogRequired?.equals("true")
										execution.rerunOnFailure = jobDetails.rerunOnFailure?.equals("true")
										execution.category = category
										execution.scriptCount = scriptCnt
										if(! execution.save(flush:true)) {
											log.error "Error saving Execution instance : ${execution.errors}"
											executionSaveStatus = false
										}
										status.flush()
									}
									catch(Throwable th) {
										status.setRollbackOnly()
									}
								}

								if(deviceList.size() > 0 ){
									executionNameForCheck = execName
								}
							}
							else{
								execution = Execution.findByName(executionNameForCheck)
								execName = executionNameForCheck
							}

							if(executionSaveStatus){
								ExecutionDevice.withTransaction { status ->
									try{
										executionDevice = new ExecutionDevice()
										executionDevice.execution = Execution.findByName(execName)
										executionDevice.dateOfExecution = new Date()
										executionDevice.device = deviceInstance?.stbName
										executionDevice.boxType = deviceInstance?.boxType?.name
										executionDevice.deviceIp = deviceInstance?.stbIp
										executionDevice.status = UNDEFINED_STATUS
										executionDevice.category = category
										executionDevice.buildName = getBuildName( deviceInstance?.stbName )
										executionDevice.save(flush:true)
										if(! executionDevice.save(flush:true)) {
											log.error "Error saving Execution instance : ${execution.errors}"
										}
										status.flush()
									}
									catch(Throwable th) {
										status.setRollbackOnly()
									}

								}
								executeVersionTransferScript(realpath, filePath, executionName, executionDevice?.id, deviceInstance.stbName, deviceInstance?.logTransferPort,url)
								int scriptGrpSize = 0
								int scriptCounter = 0
								def isMultiple = TRUE
								if(jobDetails?.scriptGroup){
									scriptGroupInstance = ScriptGroup.findById(jobDetails?.scriptGroup,[lock: true])
									scriptCounter = 0
									List validScriptList = new ArrayList()

									boolean skipStatus = false
									boolean notApplicable = false

									String rdkVersion = getRDKBuildVersion(deviceInstance);
									scriptGroupInstance.scriptList.each { scrpt ->
										if(category == jobDetails?.category){
											category = scrpt.category
										}else{
											category =   jobDetails?.category
										}
										if(category != Category.RDKB_TCL){
											def script = getScript(realpath,scrpt?.moduleName, scrpt?.scriptName, category)

											if(script){
												if(validateScriptBoxTypes(script,deviceInstance)){
													if(validateScriptRDKVersions(script,rdkVersion)){
														if(script.skip.toString().equals(TRUE)){
															skipStatus = true
															saveSkipStatus(Execution.findByName(execName), executionDevice, script, deviceInstance)
														}else{
															validScriptList << script
														}
													}else{
														notApplicable =true
														String rdkVersionData = ""
														rdkVersionData = script?.rdkVersions

														String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData

														saveNotApplicableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason,scrpt.category)

													}

												}else{
													notApplicable =true
													String boxTypeData = ""

													String deviceBoxType = ""

													Device.withTransaction { deviceBoxType = deviceInstance?.boxType }

													//										Script.withTransaction {
													//											def scriptInstance1 = Script.findById(script?.id)
													boxTypeData = script?.boxTypes
													//										}

													String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
													saveNotApplicableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance, reason, scrpt.category)
												}
											}else{
												String reason = "No script is available with name :"+scrpt?.scriptName+" in module :"+scrpt?.moduleName
												saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, scrpt?.scriptName, deviceInstance,reason, scrpt.category)
												notApplicable =true
											}
										}
										else{
											def combainedTclScript =  ScriptService?.combinedTclScriptMap
											def newScriptName  = ""
											combainedTclScript?.each{
												if(it?.value?.toString()?.contains(scrpt?.scriptName.toString())){
													//tclCombinedScriptMap.put(script?.scriptName,it.key?.toString())
													newScriptName = it.key?.toString()
													tclCombined = true
												}
											}
											if(tclCombined ){
												newScriptName= newScriptName
											}else{
												newScriptName = scrpt?.scriptName?.toString()
											}
											if(isTclScriptExists(realpath, newScriptName)){
												if( isConfigFileExists(realpath, deviceInstance?.stbName)){
													def script = [:]
													if(tclCombined){
														script.put('scriptName',newScriptName)
													}else{
														script.put('scriptName', scrpt?.scriptName)
													}

													validScriptList << script
												}
												else{
													notApplicable =true
													String reason = "No config file is available with name : Config_"+deviceInstance?.stbName+".txt"
													saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, scrpt?.scriptName, deviceInstance,reason, scrpt.category)

												}
											}
											else{
												notApplicable =true
												String reason = "No script is available with name : "+scrpt?.scriptName+".tcl"
												saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, scrpt?.scriptName, deviceInstance,reason, scrpt.category)
											}
										}
									}
									scriptGrpSize = validScriptList?.size()

									if((skipStatus || notApplicable )&& scriptGrpSize == 0){
										Execution ex = Execution.findByName(execName)
										if(ex){
											updateExecutionStatus(FAILURE_STATUS, ex?.id)
											updateExecutionDeviceSkipStatus(FAILURE_STATUS, executionDevice?.id)
										}
									}

									Execution ex = Execution.findByName(execName)
									Properties props = new Properties()
									try {
										// rest call for log transfer starts
										if(validScriptList.size() > 0){
											LogTransferService.transferLog(execName, deviceInstance)
										}
									} catch (Exception e) {
										e.printStackTrace()
									}
									int index = 0
									validScriptList.each{ scriptObj ->
										scriptCounter++
										if(scriptCounter == scriptGrpSize){
											isMultiple = FALSE
										}
										aborted = ExecutionService.abortList.contains(ex?.id?.toString())

										String deviceStatus = ""
										if(!pause && !aborted){
											try {
												deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
												/*Thread.start{
												 deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
												 }*/
												if(deviceStatus.equals(Status.HANG.toString())){
													resetAgent(deviceInstance, TRUE)
													Thread.sleep(6000)
													deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
												}
											}
											catch(Exception eX){
											}
										}

										if(!aborted && !(deviceStatus.equals(Status.NOT_FOUND.toString()) || deviceStatus.equals(Status.HANG.toString())) && !pause){
											
											def startExecutionTime = new Date()
											if(category != Category.RDKB_TCL) {
												htmlData = executeScript(execName, executionDevice, scriptObj , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark,jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired,executionName,isMultiple, category)
											}
											else{
												def combainedTcl = [:]
												if(scriptGroupInstance?.scriptList?.size() ==  validScriptList?.size()){
													if( !(ScriptService?.totalTclScriptList?.toString()?.contains(scriptObj?.scriptName?.toString())) && ScriptService?.tclScriptsList?.toString()?.contains(scriptObj?.scriptName?.toString())){
														combainedTcl?.put("scriptName", scriptGroupInstance?.scriptList[index]?.toString())
													}else{
														combainedTcl?.put("scriptName","")
													}
												}
												index = index + 1
												htmlData = executeTclScript(execName, executionDevice, scriptObj , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark,jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired,executionName,isMultiple, category, combainedTcl)
											}
											output.append(htmlData)
											Thread.sleep(6000)
											def endExecutionTime = new Date()
											executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
										}else{

											if(!aborted && (deviceStatus.equals(Status.NOT_FOUND.toString()) ||  deviceStatus.equals(Status.HANG.toString()))){
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
															executionResult.device = deviceInstanceObj?.stbName
															executionResult.execDevice = null
															executionResult.deviceIdString = deviceInstanceObj?.id?.toString()
															executionResult.status = PENDING
															executionResult.dateOfExecution = new Date()
															executionResult.category = category
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

									if(aborted && ExecutionService.abortList.contains(ex?.id?.toString())){
										ExecutionService.abortList.remove(ex?.id?.toString())
									}
									if(!aborted && pause && pendingScripts.size() > 0 ){
										def exeInstance = Execution.findByName(execName)
										savePausedExecutionStatus(exeInstance?.id)
										saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
									}
								}
								else if(scripts){

									if(scripts instanceof String){
										//									scriptInstance = Script.findById(scripts,[lock: true])
										//									scriptId = scriptInstance?.id
										def scpt = ScriptFile.findByScriptName(scripts)
										boolean notApplicable =false
										def catgory = scpt?.category
										if( catgory  == jobDetails?.category){
											catgory = scpt?.category
										}else{
											catgory = jobDetails?.category
										}
										isMultiple = FALSE
										def startExecutionTime = new Date()
										if(category != Category.RDKB_TCL){
											def moduleName= ScriptService.scriptMapping.get(scripts)
											scriptInstance = getScript(realpath,moduleName, scripts, category)
											htmlData = executeScript(execName, executionDevice, scriptInstance , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired,executionName,isMultiple, catgory)

										}
										else{
											def scriptNameTcl
											scriptInstance = [:]
											def combinedScript = [:]
											def combainedTclScript =  ScriptService?.combinedTclScriptMap
											combainedTclScript?.each{
												if(it?.value?.toString().contains(scripts?.toString())){
													combinedTCL = true
												}
											}
											if((ScriptService?.totalTclScriptList?.toString()?.contains(scripts?.toString())) && combinedTCL ){
												scriptNameTcl = scripts
												combainedTclScript?.each{
													if(it?.value?.toString()?.contains(scripts?.toString())){
														scripts = it.key?.toString()
														tclCombined =true
													}
												}
											}
											if(Utility.isTclScriptExists(realpath, scripts)){
												if(Utility.isConfigFileExists(realpath, deviceInstance?.stbName)){
													scriptInstance.put('scriptName', scripts)
													if(tclCombined){
														combinedScript.put("scriptName",scriptNameTcl)
													}else{
														combinedScript?.put("scriptName","")
													}
												}else{
													notApplicable =true
													String reason = "No config file is available with name : Config_"+deviceInstance?.stbName+".txt"
													saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, scripts, deviceInstance,reason, category)
												}
											}else{
												notApplicable =true
												String reason = "No script is available with name : "+scripts+".tcl"
												saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, scripts, deviceInstance,reason, category)
											}
											isMultiple = FALSE
											//	scriptInstance.put('scriptName',scripts)
											htmlData = executeTclScript(execName, executionDevice, scriptInstance , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired,executionName,isMultiple, catgory,combinedScript)
										}
										def endExecutionTime = new Date()
										executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
										output.append(htmlData)
									}
									else{
										def combinedScript = [:]
										def scriptNameTcl
										scriptCounter = 0
										List<Script> validScripts = new ArrayList<Script>()
										String rdkVersion = getRDKBuildVersion(deviceInstance);
										boolean skipStatus =false
										boolean notApplicable =false
										scripts.each { script ->

											def scrpInst = ScriptFile.findByScriptName(script)
											def catgry = scrpInst?.category
											if( catgry  == jobDetails?.category){
												catgry = scrpInst?.category
											}else{
												catgry = jobDetails?.category
											}
											if(catgry != Category.RDKB_TCL) {
												def moduleName= ScriptService.scriptMapping.get(script)
												scriptInstance = getScript(realpath,moduleName, script, category)

												//										scriptInstance = Script.findById(script,[lock: true])
												if(validateScriptBoxTypes(scriptInstance,deviceInstance)){
													if(validateScriptRDKVersions(scriptInstance,rdkVersion)){
														if(scriptInstance.skip.toString().equals(TRUE)){
															skipStatus = true
															saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance)
														}else{
															validScripts << scriptInstance
														}
													}else{
														notApplicable =true
														String rdkVersionData = ""
														//												Script.withTransaction {
														//													def scriptInstance1 = Script.findById(scriptInstance?.id)
														rdkVersionData = scriptInstance?.rdkVersions
														//												}

														String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData

														saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason, catgry)

													}

												}else{
													notApplicable =true
													String boxTypeData = ""

													String deviceBoxType = ""

													Device.withTransaction { deviceBoxType = deviceInstance?.boxType }

													//											Script.withTransaction {
													//												def scriptInstance1 = Script.findById(scriptInstance?.id)
													boxTypeData = scriptInstance?.boxTypes
													//											}

													String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
													saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance, reason, catgry)
												}
											}
											else{
												def combainedTclScript =  ScriptService?.combinedTclScriptMap
												def newScriptName  = ""
												combainedTclScript?.each{
													if(it?.value?.toString().contains(script?.toString())){
														newScriptName = it.key?.toString()
														tclCombined = true
													}
												}
												if(tclCombined ){
													newScriptName= newScriptName
												}else{
													newScriptName = script?.toString()
												}
												if(isTclScriptExists(realpath, newScriptName)){
													if( isConfigFileExists(realpath, deviceInstance?.stbName)){
														def scpt = [:]
														if(tclCombined){
															scpt.put('scriptName',newScriptName)
														}else{
															scpt.put('scriptName', script?.toString() )
														}
														validScripts << scpt
													}
													else{
														notApplicable =true
														String reason = "No config file is available with name : Config_"+deviceInstance?.stbName+".txt"
														saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason, catgry)
													}
												}
												else{
													notApplicable =true
													String reason = "No script is available with name : "+script+".tcl"
													saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason, catgry)
												}
											}

										}

										scriptGrpSize = validScripts?.size()

										if((skipStatus || notApplicable )&& scriptGrpSize == 0){
											Execution ex = Execution.findByName(execName)
											if(ex){
												updateExecutionStatus(FAILURE_STATUS, ex?.id)
												updateExecutionDeviceSkipStatus(FAILURE_STATUS, executionDevice?.id)
											}
										}
										Execution ex = Execution.findByName(execName)
										String deviceStatus
										def exeId = ex?.id
										def combainedTclScript =  ScriptService?.combinedTclScriptMap
										int index = 0
										validScripts.each{ script ->
											combinedScript = [:]
											scriptCounter++
											if(scriptCounter == scriptGrpSize){
												isMultiple = FALSE
											}
											def startExecutionTime = new Date()
											aborted = ExecutionService.abortList.contains(exeId?.toString())
											if(!aborted && !pause)
											{
												try{
													deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
												}catch(Exception e){
													e.printStackTrace()
												}
											}
											if(!aborted && !(deviceStatus.equals(Status.NOT_FOUND.toString()) || deviceStatus.equals(Status.HANG.toString()))){
												def scpt = ScriptFile.findByScriptName(script.name?script.name:script.scriptName)
												if(scpt?.category != Category.RDKB_TCL && jobDetails?.category != Category.RDKB_TCL ){
													htmlData = executeScript(execName, executionDevice, script , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired, executionName,isMultiple, scpt?.category)
												}
												else{
													def combinedTcl  = [:]
													if(scripts?.size() ==  validScripts?.size()){
														if( scripts?.toString()?.contains(script?.scriptName?.toString())){
															combinedTcl?.put("scriptName","")
														}else{
															combinedTcl?.put("scriptName", scripts[index]?.toString())
														}
													}
													index = index + 1
													htmlData = executeTclScript(execName, executionDevice, script , deviceInstance , url, filePath, realpath, jobDetails?.isBenchMark, jobDetails?.isSystemDiagnostics,jobDetails?.isStbLogRequired, executionName,isMultiple, jobDetails?.category, combinedTcl)
												}

											}else {
												if(!aborted && deviceStatus.equals(Status.NOT_FOUND.toString())){
													pause = true
												}
												if(!aborted && pause){
													try{
														pendingScripts.add(script)
														def execInstance
														Execution.withTransaction {
															def execInstance1 = Execution.findByName(execName)
															execInstance = execInstance1
														}
														def scriptInstanceObj
														scriptInstanceObj = script
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
																executionResult.category = category

																if(! executionResult.save(flush:true)) {
																}
																resultstatus.flush()
															}
															catch(Throwable th) {
																resultstatus.setRollbackOnly()
															}

														}

													}catch(Exception e){
														e.printStackTrace()
													}
												}

											}
											if(aborted && ExecutionService.abortList.contains(exeId?.toString())){
												ExecutionService.abortList.remove(ex?.toString())
											}
											if(!aborted && pause && pendingScripts.size() > 0 ){
												def exeInstance = Execution.findByName(execName)
												savePausedExecutionStatus(exeInstance?.id)
												saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
											}
											output.append(htmlData)
											Thread.sleep(6000)
											def endExecutionTime = new Date()
											executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
										}
									}
								}

								Execution executionInstance1 = Execution.findByName(execName)
								if(!pause && executionInstance1){
									saveExecutionStatus(aborted, executionInstance1?.id)
								}

								Device devInstance1 = Device.findById(device)
								if(ExecutionService.deviceAllocatedList.contains(devInstance1?.id)){
									ExecutionService.deviceAllocatedList.remove(devInstance1?.id)
								}

								if(aborted){
									abortedExecution = true
									resetAgent(deviceInstance)
								}

							}
						}
						else{

							output.append(htmlData)
						}
					}else{
						// issue fix for tcl sctipt execution
						String outData = " "
						if(!value){
							outData = "No valid tcl script or No Config file is available with name Config_${deviceInstance?.stbName}.txt  "
						}else{
							outData ="Execution failed due to the unavailability of box"
						}
						try {
							Execution.withTransaction{
								def execution1 = new Execution()
								execution1.name = executionName
								execution1.script = scriptName
								execution1.device = deviceName
								execution1.scriptGroup = scriptGroupInstance?.name
								execution1.result = FAILURE_STATUS
								execution1.executionStatus = FAILURE_STATUS
								execution1.dateOfExecution = new Date()
								execution1.applicationUrl = url
								execution1.isRerunRequired = jobDetails?.rerun?.equals(TRUE)
								execution1.isBenchMarkEnabled = jobDetails?.isBenchMark?.equals(TRUE)
								execution1.isSystemDiagnosticsEnabled = jobDetails?.isSystemDiagnostics?.equals(TRUE)
								execution1.isStbLogRequired= jobDetails.isStbLogRequired?.equals(TRUE)
								execution1.rerunOnFailure = jobDetails.rerunOnFailure?.equals(TRUE)
								//	execution1.outputData = "Execution failed due to the unavailability of box"
								execution1.outputData = outData
								execution1.category = category
								if(! execution1.save(flush:true)) {
									log.error "Error saving Execution instance : ${execution1.errors}"
								}
							}
						}
						catch(Exception th) {
							th.printStackTrace()
							println th.getMessage()
						}

					}

					htmlData = ""
				}

				/**
				 * Re run on failure
				 */
				def executionObj = Execution.findByName(execName)
				def executionDeviceObj = ExecutionDevice.findAllByExecutionAndStatusNotEqual(executionObj, SUCCESS_STATUS)
				if(!abortedExecution && !pause && (executionDeviceObj.size() > 0 ) && (jobDetails?.rerun?.toString()?.equals("true"))){
					try{
						htmlData = reRunOnFailure(realpath?.toString(),filePath?.toString(),url?.toString(),execName?.toString(),executionName?.toString(),jobDetails?.isBenchMark?.toString(), jobDetails?.isSystemDiagnostics?.toString(),jobDetails?.isStbLogRequired?.toString(), jobDetails?.rerunOnFailure?.toString(),jobDetails.rerun?.toString(), jobDetails?.groups)
					}catch(Exception e){
						println e.getMessage()
						e.printStackTrace()
					}
					output.append(htmlData)
				}

			}

		} catch (Exception e) {
			e.printStackTrace()
		}
		finally{
			deviceList.each{ device ->
				Device devInstance1 = Device.findById(device)
				if(allocated && ExecutionService.deviceAllocatedList.contains(devInstance1?.id)){
					ExecutionService.deviceAllocatedList.remove(devInstance1?.id)
				}
			}
		}
	}


	public void saveNotApplicableStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance, String reason, def category){
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance.stbName
				executionResult.status = Constants.NOT_APPLICABLE_STATUS
				executionResult.executionOutput = "Test not executed . Reason : "+reason
				executionResult.dateOfExecution = new Date()
				executionResult.category = category
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}
	}

	/**
	 * Function for rerun single script or multiple scripts or suite  
	 * @param realPath
	 * @param filePath
	 * @param url
	 * @param execName
	 * @param uniqueExecutionName
	 * @param isBenchMark
	 * @param isSystemDiagnostics
	 * @param islogReqd
	 * @param rerunOnFailure
	 * @param rerun
	 * @param groups
	 * @return
	 */
	def reRunOnFailure(final String realPath, final String filePath, String url, final String execName,final String uniqueExecutionName,
			final String isBenchMark, final String isSystemDiagnostics,final String islogReqd, final String rerunOnFailure, final String rerun, final def groups){
		try{
			boolean pause= false
			List pendingScripts =[]

			Execution executionInstance = Execution.findByName(execName)
			def resultArray = Execution.executeQuery("select a.result from Execution a where a.name = :exName",[exName: execName])
			def result = resultArray[0]
			def newExecName
			def execution
			Execution rerunExecutionInstance
			def executionSaveStatus = true
			boolean tclScript = false
			boolean validScript = false
			if(result != SUCCESS_STATUS){
				def scriptName
				def scriptGroupInstance = ScriptGroup.findByName(executionInstance?.scriptGroup)
				/**
				 * Get all devices for execution
				 */
				def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
				int cnt = 0
				boolean aborted = false
				executionDeviceList.each{ execDeviceInstance ->
					Device deviceInstance = Device.findByStbName(execDeviceInstance?.device)
					boolean allocated = false
					if(execDeviceInstance.status != SUCCESS_STATUS){
						String status1 = ""
						String deviceStatus = " "
						try {
							deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
							synchronized (ExecutionController.lock) {
								if(ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
									status1 = "BUSY"
								}else{
									if((deviceStatus.equals( Status.FREE.toString() ))){
										if(!ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
											allocated = true
											ExecutionService.deviceAllocatedList.add(deviceInstance?.id)
											Thread.start{
												DeviceStatusService?.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
											}
										}
									}
								}
							}
						}
						catch(Exception eX){
							println  " ERROR "+ eX.printStackTrace()
						}
						if(cnt == 0){
							newExecName = execName + RERUN
							scriptName = executionInstance?.script
							def deviceName = deviceInstance?.stbName
							if(executionDeviceList.size() > 1){
								deviceName = MULTIPLE
							}
							int scriptCnt = 0
							ScriptGroup.withTransaction {
								def scriptGroupInstance1 = ScriptGroup.get(scriptGroupInstance?.id)
								if(scriptGroupInstance1?.scriptList?.size() > 0){
									scriptCnt = scriptGroupInstance1?.scriptList?.size()
								}
							}
							Execution.withTransaction { status ->
								try {
									execution = new Execution()
									execution.name = newExecName
									execution.script = scriptName
									execution.device = deviceName
									execution.scriptGroup = scriptGroupInstance?.name
									execution.result = UNDEFINED_STATUS
									execution.executionStatus = INPROGRESS_STATUS
									execution.dateOfExecution = new Date()//dateFormat.format(cal.getTime())
									execution.groups = groups
									execution.applicationUrl = url
									execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals(TRUE)
									execution.isBenchMarkEnabled = isBenchMark?.equals(TRUE)
									execution.isStbLogRequired = islogReqd?.equals(TRUE)
									execution?.rerunOnFailure = rerunOnFailure?.equals(TRUE)
									execution.isRerunRequired = "false"
									execution.scriptCount = scriptCnt
									execution.category = execDeviceInstance.category?.toString()
									if(! execution.save(flush:true)) {
										log.error "Error saving Execution instance : ${execution.errors}"
										executionSaveStatus = false
									}
									status.flush()
								}catch(Exception e){
									println  e.getMessage()
									e.printStackTrace()
								}

							}

							cnt++
							rerunExecutionInstance = Execution.findByName(newExecName)
						}
						if(executionSaveStatus){
							ExecutionDevice executionDevice
							Execution.withTransaction {
								executionDevice = new ExecutionDevice()
								executionDevice.execution = rerunExecutionInstance
								executionDevice.device = deviceInstance?.stbName
								executionDevice.boxType = deviceInstance?.boxType?.name
								executionDevice.deviceIp = deviceInstance?.stbIp
								executionDevice.dateOfExecution = new Date()
								executionDevice.status = UNDEFINED_STATUS
								executionDevice.category = execution.category
								executionDevice.buildName = getBuildName( deviceInstance?.stbName )
								executionDevice.save(flush:true)
							}
							executeVersionTransferScript(realPath, filePath, newExecName, executionDevice?.id, deviceInstance.stbName, deviceInstance?.logTransferPort,url)
							def executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
							def scriptInstance
							def htmlData
							def resultSize = executionResultList.size()
							int counter = 0
							def isMultiple = "true"

							// adding log transfer to server for reruns

							Properties props = new Properties()
							try {
								props.load(grailsApplication.parentContext.getResource("/appConfig/logServer.properties").inputStream)
								// initiating log transfer
								if(executionResultList.size() > 0){
									LogTransferService.transferLog(newExecName, deviceInstance)
								}
							} catch (Exception e) {
								e.printStackTrace()
							}
							executionResultList.each{ executionResult ->
								def scriptFile = ScriptFile.findByScriptName(executionResult?.script)
								def combinedScript = [:]
								if(executionResult?.category?.toString()?.equals(Category?.RDKV?.toString()) || executionResult?.category?.toString()?.equals(Category?.RDKB?.toString())){
									tclScript  = false
								}else if(executionResult?.category?.toString()?.equals(Category?.RDKB_TCL?.toString())){
									tclScript  = true
								}
								if(tclScript){
									boolean tclCombined = false
									def combainedTclScript =  ScriptService?.combinedTclScriptMap
									def newScriptName  = ""
									combainedTclScript?.each{
										if(it?.value?.toString()?.contains(executionResult?.script.toString())){
											newScriptName = it.key?.toString()
											tclCombined = true
										}
									}
									if(tclCombined){
										newScriptName= newScriptName
									}else{
										newScriptName = executionResult?.script?.toString()
									}
									if(Utility.isTclScriptExists(realPath?.toString(), newScriptName?.toString())){
										if(Utility?.isConfigFileExists(realPath, deviceInstance?.stbName)){
											if(tclCombined){
												combinedScript.put("scriptName", executionResult?.script?.toString())
											}else{
												combinedScript.put("scriptName","")
											}
											validScript = true
										}
									}
									scriptFile = ScriptFile?.findByScriptName(newScriptName)
								}else{
									scriptInstance = getScript(realPath?.toString(),scriptFile?.moduleName,scriptFile?.scriptName, executionResult?.category)
									if(validateScriptBoxTypes(scriptInstance,deviceInstance)){
										validScript = true
									}
								}
								counter++
								if(counter == resultSize){
									isMultiple = "false"
								}
								//	if(executionResult.category != Category.RDKB_TCL){
								//	if(validateScriptBoxTypes(scriptInstance,deviceInstance)){
								def startExecutionTime = new Date()
								if(validScript){
									Execution exec = Execution.findByName(newExecName)
									aborted = ExecutionService.abortList?.toString().contains(exec?.id?.toString())
									try{
										deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
									}catch (Exception e){
										e.getMessage()
									}
									print deviceStatus
									if(!aborted && !(deviceStatus?.toString().equals(Status.NOT_FOUND.toString()) || deviceStatus?.toString().equals(Status.HANG.toString())) && !pause){
										if(!tclScript){

											htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, url, filePath, realPath,isBenchMark,isSystemDiagnostics,islogReqd,uniqueExecutionName,isMultiple,executionResult.category?.toString() )
										}else {
											htmlData = executeTclScript(newExecName, executionDevice, scriptFile, deviceInstance, url, filePath, realPath,isBenchMark,isSystemDiagnostics,islogReqd,uniqueExecutionName,isMultiple,executionResult.category, combinedScript )

										}
									}else{
										if(!aborted && (deviceStatus?.equals(Status.NOT_FOUND.toString()) ||  deviceStatus?.equals(Status.HANG.toString()))){
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
														def executionResult1 = new ExecutionResult()
														executionResult1.execution = execInstance
														executionResult1.executionDevice = executionDevice1
														executionResult1.script = scriptInstanceObj?.name
														executionResult1.device = deviceInstanceObj?.stbName
														executionResult1.execDevice = null
														executionResult1.deviceIdString = deviceInstanceObj?.id?.toString()
														executionResult1.status = PENDING
														executionResult1.dateOfExecution = new Date()
														//executionResult.category = executionDevice1?.category?.toString()
														executionResult1.category = Utility.getCategory(executionDevice1?.category?.toString())
														if(!executionResult1.save(flush:true)) {
														}
														resultstatus.flush()
													}
													catch(Exception e){
														e.printStackTrace()
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
								//	}
								else{
									if(!aborted && !(deviceStatus?.toString().equals(Status.NOT_FOUND.toString()) || deviceStatus?.toString().equals(Status.HANG.toString())) && !pause){
										def scrip = [:]
										scrip.put('scriptName',scriptInstance?.scriptName)
										htmlData = executeTclScript(newExecName, executionDevice, scrip, deviceInstance, url, filePath, realPath,isBenchMark,isSystemDiagnostics,islogReqd,uniqueExecutionName,isMultiple,executionResult.category )
									}
								}
								def endExecutionTime = new Date()
								executionTimeCalculation(newExecName,startExecutionTime,endExecutionTime)
							}
							//}
							// stopping log transfer
							try {
								if(executionResultList.size() > 0){
									LogTransferService.closeLogTransfer(newExecName)
								}
							} catch (Exception e) {
								e.printStackTrace()
							}

							Execution exec = Execution.findByName(newExecName)
							if(aborted && ExecutionService.abortList.contains(exec?.id?.toString())){
								saveExecutionStatus(aborted, exec?.id)
								ExecutionService.abortList.remove(exec?.id?.toString())
							}
							if(!aborted && pause && pendingScripts.size() > 0 ){
								savePausedExecutionStatus(exec?.id)
								saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
							}
							if(!aborted && !pause ){
								saveExecutionStatus(aborted, exec?.id)
							}
						}
					}

					if(allocated && ExecutionService.deviceAllocatedList.contains(deviceInstance?.id)){
						ExecutionService.deviceAllocatedList.remove(deviceInstance?.id)
					}
				}
			}
		}catch(Exception e){
			println " ERROR "+e.getMessage()
		}
	}

	/**
	 * method to fetch the name of the file transfer script
	 */
	def getFileTransferScriptName(Device device){
		String scriptName = FILE_TRANSFER_SCRIPT
		if(InetUtility.isIPv6Address(device?.stbIp)){
			scriptName = FILE_UPLOAD_SCRIPT
		}else{
			String mechanism = getIPV4LogUploadMechanism()
			if(mechanism?.equals(Constants.REST_MECHANISM)){
				scriptName = FILE_UPLOAD_SCRIPT
			}

		}
		return scriptName
	}

	/**
	 * Method to execute the script to get the device's version details
	 * @param realPath
	 * @param filePath
	 * @param executionName
	 * @param exectionDeviceId
	 * @param stbIp
	 * @param logTransferPort
	 * @return
	 */
	def executeVersionTransferScript(final String realPath, final String filePath, final String executionName, def exectionDeviceId, final String stbName, final String logTransferPort, def url){
		try{
			def executionInstance = Execution.findByName(executionName)

			Device device
			Device.withTransaction{
				device = Device.findByStbName(stbName)
			}
			String versionFileName = "${executionInstance?.id}_${exectionDeviceId?.toString()}_version.txt"
			def versionFilePath = "${realPath}//logs//version//${executionInstance?.id}//${exectionDeviceId?.toString()}"
			String scriptName = getFileTransferScriptName(device)
			File layoutFolder = grailsApplication.parentContext.getResource(scriptName).file
			def absolutePath = layoutFolder.absolutePath

			def cmdList = [
				PYTHON_COMMAND,
				absolutePath,
				device.stbIp,
				device.agentMonitorPort,
				"/version.txt",
				versionFileName
			]

			if(scriptName?.equals(FILE_UPLOAD_SCRIPT)){
				url = updateTMUrl(url,device)
				cmdList.push(url)
			}

			String [] cmd = cmdList.toArray()


			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def outputData = scriptExecutor.executeScript(cmd,1)
			copyVersionLogsIntoDir(realPath, versionFilePath, executionInstance?.id, exectionDeviceId?.toString())



			if(device?.boxType?.type?.equalsIgnoreCase(BOXTYPE_CLIENT)){
				getDeviceDetails(device,device?.agentMonitorPort,realPath,url)
			}
		}
		catch(Exception ex){
		}
	}
	
	/**
	 * For getting the image name on a particular device
	 * - Accessing the getimagename_cmndline file
	 * - send command through TM ( python getimagename_cmndline.py Device_IP_Address PortNumber )
	 * @param stbName
	 * @return buildName
	 */
	def getBuildName(String stbName){
		String buildName
		JsonObject jsonOutData = new JsonObject()
		Device device = Device.findByStbName(stbName)
		if(device){
			try{
				File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//getimagename_cmndline.py").file
				println layoutFolder
				def absolutePath = layoutFolder.absolutePath
				String[] cmd = [
					PYTHON_COMMAND,
					absolutePath,
					device.stbIp,
					device.stbPort
				]
				ScriptExecutor scriptExecutor = new ScriptExecutor()
				def outputData = scriptExecutor.executeScript(cmd,1)
				if(outputData && !(outputData?.toString()?.contains("METHOD_NOT_FOUND") || outputData?.toString()?.contains("AGENT_NOT_FOUND") )){
					buildName = outputData.toString()?.trim()
				}
				else{
					buildName =  "Image name not available"
					
				}
			}catch(Exception e ){
				println  "ERROR "+ e.getMessage()
				buildName =  "Image name not available"
				
			}
		}else{
			buildName =  "Image name not available"
		}
		return buildName
	}
	
	
	/**
	 * Method to call the script executor to execute the script
	 * @param executionData
	 * @return
	 */
	public String executeScriptFile(final String executionData) {
		new ScriptExecutor().execute( getCommand( executionData ),1)
	}

	/**
	 * Method to execute the script
	 * @param scriptGroupInstance
	 * @param scriptInstance
	 * @param deviceInstance
	 * @param url
	 * @return
	 */

	def String executeScript(final String executionName, final ExecutionDevice executionDevice, final def scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark, final String isSystemDiagnostics,final String isLogReqd,final String uniqueExecutionName,final String isMultiple, def category) {
		String htmlData = ""
		Date startTime = new Date()
		String scriptData = convertScriptFromHTMLToPython(scriptInstance.scriptContent)

		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

		//		Script scriptInstance1 = Script.findById(scriptInstance.id,[lock: true])
		//		scriptInstance1.status = Status.ALLOCATED
		//		scriptInstance1.save(flush:true)

		Device deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])

		def executionInstance = Execution.findByName(executionName,[lock: true])
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution

		Date executionStartDt = new Date()
		def execStartTime =  executionStartDt.getTime()
		def executionResult
		ExecutionResult.withTransaction { resultstatus ->
			try {
				executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance1.stbName
				executionResult.dateOfExecution = new Date()
				executionResult.category = category
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}
		def executionResultId = executionResult?.id
		def mocaDeviceList = Device.findAllByStbIpAndMacIdIsNotNull(deviceInstance1?.stbIp)
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

		String gatewayIp = deviceInstance1?.gatewayIp
		String logFilePath = realPath?.toString()+"/logs/logs/"


		def sFile = ScriptFile.findByScriptNameAndModuleName(scriptInstance?.name,scriptInstance?.primitiveTest?.module?.name)
		scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES +logFilePath+SINGLE_QUOTES + COMMA_SEPERATOR +
				executionId  + COMMA_SEPERATOR + executionDevice?.id + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.agentMonitorPort + COMMA_SEPERATOR + deviceInstance1?.statusPort + COMMA_SEPERATOR +
				sFile?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR + SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
				SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR)// + gatewayIp + COMMA_SEPERATOR)


		scriptData	 = scriptData + "\nprint \"SCRIPTEND#!@~\";"

		Date date = new Date()
		String newFile = FILE_STARTS_WITH+date.getTime().toString()+PYTHON_EXTENSION

		File file = new File(filePath, newFile)
		boolean isFileCreated = file.createNewFile()
		if(isFileCreated) {
			file.setExecutable(true, false )
		}
		PrintWriter fileNewPrintWriter = file.newPrintWriter()
		fileNewPrintWriter.print( scriptData )
		fileNewPrintWriter.flush()
		fileNewPrintWriter.close()
		String outData = executeScripts( file.getPath() , execTime,executionName)

		//def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
		def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"

		//new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
		logTransfer(deviceInstance,logTransferFilePath,logTransferFileName, realPath, executionId,executionDevice?.id,executionResultId,url  )

		file.delete()
		// TFTP transfer --->>>
		def logPath = "${realPath}/logs//${executionId}//${executionDevice?.id}//${executionResultId}//"
		copyLogsIntoDir(realPath,logPath ,executionId,executionDevice?.id, executionResultId)
		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}
		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()
		def timeDifference = ( execEndTime - execStartTime  ) / 1000;
		String timeDiff =  String.valueOf(timeDifference)
		def resultArray = Execution.executeQuery("select a.executionTime from Execution a where a.name = :exName",[exName: executionName])
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
			println singleScriptExecTime
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
		

		if(ExecutionService.abortList.contains(executionInstance?.id?.toString())){
			resetAgent(deviceInstance,TRUE)
		}else if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
			}
			updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
			Thread.sleep(4000)
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				"true"
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
			Thread.sleep(4000)
		}else if(htmlData.contains("Pre-Condition not met")){
			if(htmlData.contains(KEY_SCRIPTEND)){
				htmlData = htmlData.replaceAll(KEY_SCRIPTEND,"")
			}
			updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
		}
		else{
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
				String outputData = htmlData
				updateExecutionResults(outputData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
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
						"true"
					]
					ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
					def resetExecutionData = scriptExecutor.executeScript(cmd,1)
					callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
					htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
					updateExecutionResultsTimeOut(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
					Thread.sleep(4000)
				}else{
					try {
						updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
						Thread.sleep(4000)
						File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
						def absolutePath = layoutFolder.absolutePath
						String[] cmd = [
							PYTHON_COMMAND,
							absolutePath,
							deviceInstance?.stbIp,
							deviceInstance?.agentMonitorPort,
							"false"
						]
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						def resetExecutionData = scriptExecutor.executeScript(cmd,1)
						callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
						Thread.sleep(4000)
					} catch (Exception e) {
						e.printStackTrace()
					}

				}
			}
		}
		String performanceFilePath
		String performanceFileName
		String diagnosticsFilePath
		if(isBenchMark.equals("true") || isSystemDiagnostics.equals("true")){
			//new File("${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			performanceFileName = "${executionId}_${executionDevice?.id}_${executionResultId}"
			performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}//"
			diagnosticsFilePath = "${realPath}//logs//stblogs//${executionId}//${executionDevice?.id}//${executionResultId}//"
		}
		def tmUrl = updateTMUrl(url,deviceInstance)
		if(isBenchMark.equals("true")){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath

			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				//deviceInstance?.logTransferPort,
				deviceInstance?.agentMonitorPort,
				"PerformanceBenchMarking",
				performanceFileName
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,1)
			copyPerformanceLogIntoDir(realPath, performanceFilePath,executionId,executionDevice?.id, executionResultId)
		}
		if(isSystemDiagnostics.equals("true")){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				//deviceInstance?.logTransferPort,
				deviceInstance?.agentMonitorPort,
				"PerformanceSystemDiagnostics",
				performanceFileName
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
			htmlData += scriptExecutor.executeScript(cmd,1)
			copyPerformanceLogIntoDir(realPath, performanceFilePath,executionId,executionDevice?.id, executionResultId)
			
			initiateDiagnosticsTest(deviceInstance, performanceFileName, tmUrl,uniqueExecutionName)
			copyLogFileIntoDir(realPath, diagnosticsFilePath, executionId,executionDevice?.id, executionResultId,DEVICE_DIAGNOSTICS_LOG)
		}
		//def logTransferFileName1 = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDevice?.id.toString()}"
		def logTransferFileName1 = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
		def logTransferFilePath1 = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"

		//new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
		logTransfer1(deviceInstance,logTransferFilePath1,logTransferFileName1 ,realPath, executionId,executionDevice?.id, executionResultId,url)
		if(isLogReqd?.toString()?.equals("true")){
			
		transferSTBLog(scriptInstance?.primitiveTest?.module?.name, deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId,realPath,url)
		}
		Date endTime = new Date()
		try {
			def totalTimeTaken = (endTime?.getTime() - startTime?.getTime()) / 1000
	//		totalTimeTaken = totalTimeTaken?.round(2)
			updateExecutionTime(totalTimeTaken?.toString(), executionResultId)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return htmlData
	}

			/**
			 * The function for getting the cumulative time for execution  in seconds
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
				 println "in convert"
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
	 * Function For Tranfer the performance related file using tftp
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */

	def copyPerformanceLogIntoDir(def realPath, def logTransferFilePath  , def executionId, def executionDeviceId , def executionResultId){
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
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}

	/**
	 * Function for transfer the open sourse logs from "tftp server
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyLogsIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId ){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(!(file?.toString()?.contains("version.txt") || file.toString()?.contains("benchmark.log") || file.toString()?.contains("memused.log") || file.toString()?.contains("cpu.log") || file?.toString()?.contains("AgentConsoleLog.log"))){
						def logFileName =  file?.getName()?.split("_")
						if (file?.isFile() && logFileName.length >= 3 ) {
							if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString()) && executionResultId?.toString()?.equals(logFileName[2]?.toString())){
								String fileName = file.getName()
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
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}


	/**
	 * To copy   the stb files in to perticular dir using tftp
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyStbLogsIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId ){
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
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}



	/**
	 * Function for version.txt file transfer
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */

	def copyVersionLogsIntoDir(def realPath, def logTransferFilePath,  def executionId , def executionDeviceId){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(file?.toString().contains("version.txt")){
						def logFileName =  file.getName().split("_")
						if(logFileName?.length > 0){
							if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString())){
								def  versionFileName = logFileName[1]+"_"+logFileName.last()
								new File(logTransferFilePath?.toString()).mkdirs()
								File logTransferPath  = new File(logTransferFilePath)
								if(file.exists()){
									boolean fileMoved = file.renameTo(new File(logTransferPath, versionFileName));
								}
							}
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}


	/**
	 * Method to execute tcl script in job
	 * @param executionName
	 * @param executionDevice
	 * @param scriptInstance
	 * @param deviceInstance
	 * @param url
	 * @param filePath
	 * @param realPath
	 * @param isBenchMark
	 * @param isSystemDiagnostics
	 * @param isLogReqd
	 * @param uniqueExecutionName
	 * @param isMultiple
	 * @return
	 */

	def executeTclScript(final String executionName, final ExecutionDevice executionDevice, final def scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark, final String isSystemDiagnostics,final String isLogReqd,final String uniqueExecutionName,final String isMultiple, def category,  final def combainedTcl) {
		Date startTime = new Date()
		String htmlData = ""
		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES
		def executionInstance = Execution.findByName(executionName)
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution
		def resultArray = Execution.executeQuery("select a.executionTime from Execution a where a.name = :exName",[exName: executionName])
		def totalTimeArray = Execution.executeQuery("select a.realExecutionTime from Execution a where a.name = :exName",[exName: executionName])
		def executionResultId

		def executionResult
		def newScriptName
		if(combainedTcl?.scriptName){
			newScriptName=combainedTcl?.scriptName
		}else{
			newScriptName=scriptInstance?.scriptName
		}

		ExecutionResult.withTransaction { resultstatus ->
			try {
				executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script =newScriptName
				executionResult.device = deviceInstance.stbName
				executionResult.dateOfExecution = new Date()
				executionResult.category = category
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}


		if(executionResult == null){
			//def newScriptName
			try {
				if(combainedTcl?.scriptName){
					newScriptName=combainedTcl?.scriptName
				}else{
					newScriptName=scriptInstance?.scriptName
				}

				def sql = new Sql(dataSource)
				sql.execute("insert into execution_result(version,execution_id,execution_device_id,script,device,date_of_execution,status,category) values(?,?,?,?,?,?,?,?)",
						[1,executionInstance?.id, executionDevice?.id, newScriptName?.toString(),  deviceInstance.stbName, startTime, UNDEFINED_STATUS, category])
				def result = ExecutionResult.findByExecution(executionInstance)
			} catch (Exception e) {
				e.printStackTrace()
				println e.message
			}

			def resultArray1 = ExecutionResult.executeQuery("select a.id from ExecutionResult a where a.execution = :exId and a.script = :scriptname and device = :devName ",[exId: executionInstance, scriptname: newScriptName?.toString(), devName: deviceInstance?.stbName.toString()])
			if(resultArray1[0]){
				executionResultId = resultArray1[0]
			}
		}else{
			executionResultId = executionResult?.id
		}
		int counter = 1
		def sFile = ScriptFile.findByScriptName(scriptInstance?.scriptName)

		Date executionStartDt = new Date()
		def executionStartTime =  executionStartDt.getTime()

		//setting execution time as 12 minutes
		int execTime = 12

		def  scriptDir = grailsApplication.parentContext.getResource("fileStore"+FILE_SEPARATOR+FileStorePath.RDKTCL.value()).file?.absolutePath
		def tclFilePath = scriptDir+FILE_SEPARATOR+sFile.scriptName+".tcl"
		def configFilePath = scriptDir+FILE_SEPARATOR+"Config_" + deviceInstance?.stbName+".txt"
		String scriptData = readScriptContent(tclFilePath)
		scriptData = convertScriptFromHTMLToPython(scriptData)

		//Required only for TDK TCL execution
		//scriptData = scriptData.replace('$ClassPath $Class' , '$ClassPath $Class '+executionResultId+' ' )
		scriptData = scriptData.replace('java -cp $ClassPath $Class ' , 'java -cp $ClassPath $Class '+executionResultId+' ' )

		Date date = new Date()
		String newFile = FILE_STARTS_WITH+date.getTime().toString()+TCL_EXTENSION
		File file = new File(filePath, newFile)
		boolean isFileCreated = file.createNewFile()
		if(isFileCreated) {
			file.setExecutable(true, false )
		}
		PrintWriter fileNewPrintWriter = file.newPrintWriter();
		fileNewPrintWriter.print( scriptData )
		fileNewPrintWriter.flush()
		fileNewPrintWriter.close()

		String outData
		outData = executeTclScriptCommand(file.getPath(), configFilePath, execTime, uniqueExecutionName , scriptInstance.scriptName, scriptDir,combainedTcl.scriptName )

		//outData = executionService?.executeTclScript(tclFilePath, configFilePath, execTime, uniqueExecutionName , scriptInstance.scriptName, scriptDir )
		file.delete()

		def logPath = "${realPath}/logs//${executionId}//${executionDevice?.id}//${executionResultId}//"
		copyLogsIntoDir(realPath,logPath, executionId,executionDevice?.id, executionResultId)

		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}

		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()
		def timeDifference = ( execEndTime - executionStartTime  ) / 1000;

		String timeDiff =  String.valueOf(timeDifference)
		String singleScriptExecTime = String.valueOf(timeDifference)

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
		
		if(ExecutionService.abortList.contains(executionInstance?.id?.toString())){
			resetAgent(deviceInstance,TRUE)
		}else if(Utility.isFail(htmlData) ){
			def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
			def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"
			//new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			logTransfer(deviceInstance,logTransferFilePath,logTransferFileName,realPath, executionId,executionDevice?.id, executionResultId,url)
			if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
				transferSTBLog("tcl", deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId,url)
			}
			updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
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
		}
		else if((timeDifference >= execTime) && (execTime != 0))	{
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
			callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
			htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
			updateExecutionResultsTimeOut(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
			Thread.sleep(10000)
		}
		else{
			String outputData = htmlData
			//	executionService.updateExecutionResults(outputData, executionResultId,  executionId, executionDevice?.id, timeDiff, singleScriptExecTime)
			updateTclExecutionResults( [execId: executionId,  resultData: 'SUCCESS',  execResult:executionResultId,
				expectedResult:null,  resultStatus :'SUCCESS', testCaseName : scriptInstance?.scriptName,  execDevice:executionDevice?.id, statusData:'SUCCESS',
				outputData:outputData, timeDiff:timeDiff, singleScriptExecTime:singleScriptExecTime ])

		}
		if(!ExecutionService.abortList.contains(executionInstance?.id?.toString())){
			String performanceFilePath
			String diagnosticsFilePath
			String performanceFileName
			if(isBenchMark.equals(TRUE) || isSystemDiagnostics.equals(TRUE)){
				new File("${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
				performanceFileName = "${executionId}_${executionDevice?.id}_${executionResultId}"
				performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}//"
				diagnosticsFilePath = "${realPath}//logs//stblogs//${executionId}//${executionDevice?.id}//${executionResultId}//"
			}
			def tmUrl = updateTMUrl(url,deviceInstance)
			if(isBenchMark.equals(TRUE)){
				File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
				def absolutePath = layoutFolder.absolutePath

				String[] cmd = [
					PYTHON_COMMAND,
					absolutePath,
					deviceInstance?.stbIp,
					deviceInstance?.stbPort,
					deviceInstance?.agentMonitorPort,
					KEY_PERFORMANCE_BM,
					performanceFileName
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
					KEY_PERFORMANCE_SD,
					performanceFileName
				]
				ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
				htmlData += scriptExecutor.executeScript(cmd,10)
				copyPerformanceLogIntoDir(realPath, performanceFilePath, executionId,executionDevice?.id, executionResultId)
				
				initiateDiagnosticsTest(deviceInstance, performanceFileName, tmUrl,uniqueExecutionName)
				copyLogFileIntoDir(realPath, diagnosticsFilePath, executionId,executionDevice?.id, executionResultId,DEVICE_DIAGNOSTICS_LOG)
			}

			def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
			def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"
			//logTransfer(deviceInstance,logTransferFilePath,logTransferFileName ,realPath, executionId,executionDevice?.id, executionResultId,url)

			logTransfer(deviceInstance,logTransferFilePath,logTransferFileName,realPath,executionId,executionDevice?.id, executionResultId,url)
			if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
				transferSTBLog('tcl', deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId,url)
			}
		}
		Date endTime = new Date()
		try {
			def totalTimeTaken = (endTime?.getTime() - startTime?.getTime()) / 1000
	//		totalTimeTaken = totalTimeTaken?.round(2)
			updateExecutionTime(totalTimeTaken?.toString(), executionResultId)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return htmlData
	}
	/**
	 * Converts the script that is given in textarea to
	 * python format
	 * @param script
	 * @return
	 */
	def convertScriptFromHTMLToPython(final String script){
		def afterspan =removeAllSpan(script)
		def afterBr = afterspan.replaceAll(HTML_REPLACEBR, KEY_ENTERNEW_LINE)
		afterBr = afterBr.replaceAll(HTML_LESSTHAN,LESSTHAN);
		afterBr = afterBr.replaceAll(HTML_GREATERTHAN, GREATERTHAN)
		return afterBr;
	}

	/**
	 * Function for fetching tcl script content  
	 * @param filename
	 * @return
	 */

	def readScriptContent(String filename){
		File file = new File(filename)
		String scriptContent = ""
		if(file.exists()){
			String s = ""
			List line = file.readLines()
			int indx = 0
			while(indx < line.size()){
				String lineData = line.get(indx)
				scriptContent = scriptContent + lineData+"\n"
				indx++
			}
		}else{
			println " file Not present "
		}
		return scriptContent
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
			callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Removes all span from the script
	 * @param script
	 * @return
	 */
	def removeAllSpan(String script) {
		Matcher m = Pattern.compile(HTML_PATTERN).matcher(script)
		while(m.find()){
			String match = m.group(1);
			script =script.replace(match, "");
		}
		String afterspan =script.replaceAll(HTML_PATTERN_AFTERSPAN, "")
		return afterspan
	}



	def getConsoleFileTransferScriptName(Device device){
		String scriptName = CONSOLE_FILE_TRANSFER_SCRIPT
		if(InetUtility.isIPv6Address(device?.stbIp)){
			scriptName = CONSOLE_FILE_UPLOAD_SCRIPT
		}else{
			String mechanism = getIPV4LogUploadMechanism()
			if(mechanism?.equals(Constants.REST_MECHANISM)){
				scriptName = CONSOLE_FILE_UPLOAD_SCRIPT
			}

		}
		return scriptName
	}

	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def logTransfer1(def deviceInstance, def logTransferFilePath, def logTransferFileName, def realPath , def executionId, def executionDeviceId , def executionResultId, def url){
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
				"AgentConsole.log",
				logTransferFileName // File Name
			]

			if(scriptName?.equals(CONSOLE_FILE_UPLOAD_SCRIPT)){
				cmdList.push(url)
			}

			String [] cmd = cmdList.toArray()

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			copyAgentconsoleLogIntoDir(realPath,logTransferFilePath,executionId,executionDeviceId,executionResultId  )
			Thread.sleep(4000)
		}
		catch(Exception e){
		}
	}


	def transferSTBLog(def moduleName , def dev,def execId, def execDeviceId,def execResultId,def realPath,def url){
		try {
			def module
			Module.withTransaction {
				module = Module.findByName(moduleName)
			}

			def destFolder = grailsApplication.parentContext.getResource("//logs//stblogs//execId_logdata.txt").file
			def destPath = destFolder.absolutePath


			def filePath = destPath.replace("execId_logdata.txt", "${execId}//${execDeviceId}//${execResultId}")
			def directoryPath =  "${execId}_${execDeviceId}_${execResultId}"
			def stbFilePath = "${realPath}/logs//stblogs//${execId}//${execDeviceId}//${execResultId}//"
			//def directoryPath = destPath.replace("execId_logdata.txt", "${execId}//${execDeviceId}//${execResultId}")
			//new File(directoryPath).mkdirs()

			module?.logFileNames?.each{ name ->

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
						dev?.agentMonitorPort,
						//dev?.logTransferPort,
						name,
						//directoryPath+"//"+fName
						directoryPath+"_"+fName
					]

					if(scriptName?.equals(FILE_UPLOAD_SCRIPT)){
						url = ExecutionService.updateTMUrl(url,dev)
						cmdList.push(url)
					}
					String [] cmd = cmdList.toArray()
					try {
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						def outputData = scriptExecutor.executeScript(cmd,1)
						copyStbLogsIntoDir(realPath,stbFilePath, execId,execDeviceId,execResultId)

					}catch (Exception e) {
						e.printStackTrace()
					}
				}

			}
		} catch (Exception e) {
		}
	}

	/**
	 * Method to call the script executor to execute the script
	 * @param executionData
	 * @return
	 */
	public String executeScripts(final String executionData, int execTime,String executionName) {

		//		def output = new ScriptExecutor().execute( getCommand( executionData ), execTime)
		def output =  new ScriptExecutor().execute( getCommand( executionData ), execTime,executionName,ExecutionService?.executionProcessMap)
		return output
	}


	public String executeTclScriptCommand(final String tclExecutableFile, final String configFile, int execTime, final String executionName, final String scriptName, final String tclDirPath, final String combainedTclScriptName) {
		String opFile = prepareOutputfile(executionName, scriptName)
		String output = NEW_LINE+getCurrentTime()+NEW_LINE+"Executing script : "+scriptName+NEW_LINE;
		output += "======================================="+NEW_LINE
		def tclFilePath = ""
		def command
		boolean combine = false
		if(combainedTclScriptName){
			combine = true
		}else{
			combine = false
		}
		if(combine &&  combainedTclScriptName && ScriptService?.tclScriptsList?.toString().contains(scriptName?.toString()) && ScriptService?.totalTclScriptList?.toString()?.contains(combainedTclScriptName?.toString())){
			command =  "tclsh $tclExecutableFile $configFile $combainedTclScriptName"
		}else if( !combainedTclScriptName && ScriptService?.tclScriptsList?.toString().contains(scriptName?.toString()) && !ScriptService?.totalTclScriptList?.toString()?.contains(scriptName?.toString())){
			def startScriptName =  scriptName?.toString().split("_to_")
			def firstName
			if(startScriptName?.length > 0 ){
				firstName = startScriptName[0]
				command =  "tclsh $tclExecutableFile $configFile $firstName"
			}
		}else{

			command = "tclsh $tclExecutableFile $configFile"
		}

		output += new ScriptExecutor(opFile).execute( command, execTime,executionName,ExecutionService?.executionProcessMap,tclDirPath)
		return output
	}
	def getCurrentTime(){
		SimpleDateFormat format = new SimpleDateFormat("dd-MMM-yyyy hh:mm:ss")
		String timeString = format.format(new Date())
		return timeString
	}


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
			buffWriter.write(NEW_LINE+getCurrentTime())
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
	 * Method to check whether the agent reset failed. If the agent reset failed it will request to reboot the box.
	 * @param output
	 * @param device
	 * @return
	 */
	def callRebootOnAgentResetFailure(String output,Device device){
		if(output?.contains("Failed to reset agent") || output?.contains("Unable to reach agent")){
			rebootBox(device)
		}
	}

	/**
	 * Method to reboot the box by invoking the python script.
	 * @param deviceInstance
	 * @return
	 */
	def rebootBox(Device deviceInstance ){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callRebootOnCrash.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(10000)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def logTransfer(def deviceInstance, def logTransferFilePath, def logTransferFileName , def realPath , def executionId, def executionDeviceId , def executionResultId , def url){
		String scriptName = getConsoleFileTransferScriptName(deviceInstance)
		File layoutFolder = grailsApplication.parentContext.getResource(scriptName).file
		def absolutePath = layoutFolder.absolutePath
		def cmdList = [
			PYTHON_COMMAND,
			absolutePath,
			deviceInstance?.stbIp,
			deviceInstance?.agentMonitorPort,
			"AgentConsole.log",
			logTransferFileName
			//logTransferFilePath
		]

		if(scriptName?.equals(CONSOLE_FILE_UPLOAD_SCRIPT)){
			cmdList.push(url)
		}

		String [] cmd = cmdList.toArray()


		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		copyAgentconsoleLogIntoDir(realPath,logTransferFilePath,executionId,executionDeviceId,executionResultId  )
		Thread.sleep(4000)
	}

	/**
	 * Copy the device logs file into devicelog directory using TFTP server.
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyDeviceLogIntoDir(def realPath, def logTransferFilePath){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->

					def logFileName =  file.getName().split("_")
					if(logFileName?.length > 0){
						new File(logTransferFilePath?.toString()).mkdirs()
						File logTransferPath  = new File(logTransferFilePath)
						if(file.exists()){
							boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}

	/**
	 *  Function for move the performance realted like bench mark , cpu usage, meminfo and agent console log transfer
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */

	def copyAgentconsoleLogIntoDir(def realPath, def logTransferFilePath , def executionId, def executionDeviceId , def executionResultId){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(file.toString()?.contains("AgentConsoleLog.txt")){
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
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}


	/**
	 * Execute the script
	 * @param executionData
	 * @return
	 */
	public String executeScriptData(final String executionData) {
		new ScriptExecutor().execute( getCommand( executionData ))
	}


	/**
	 * Method to get the python script execution command.
	 * @param command
	 * @return
	 */
	public String getCommand(String command) {
		String actualCommand = ConfigurationHolder.config.python.execution.path +" "+ command
		return actualCommand
	}



	public boolean validateScriptBoxType(final Script scriptInstance, final Device deviceInstance){
		boolean scriptStatus = true
		//if(!(scriptInstance.boxTypes.find { it.id == deviceInstance.boxType.id })){
		//Issue fixed
		if(!(script?.boxTypes?.find { it?.toString()?.equals(deviceInstance1?.boxType?.toString()) })){
			scriptStatus = false
		}
		return scriptStatus
	}

	def getRDKBuildVersion(Device device){

		def outputData
		def absolutePath
		def boxIp = device?.stbIp
		def port = device?.agentMonitorPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callGetRDKVersion.py").file
		absolutePath = layoutFolder.absolutePath

		if(boxIp != null && port != null ){
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				boxIp,
				port
			]

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			outputData = scriptExecutor.executeScript(cmd,1)
		}

		if(outputData){
			outputData = outputData.trim()
		}else{
			outputData = ""
		}

		String rdkVersion = ""
		if(outputData.equals("METHOD_NOT_FOUND") || outputData.equals("AGENT_NOT_FOUND") || outputData.equals("NOT_DEFINED")){
			rdkVersion = "NOT_AVAILABLE"
		}else if(outputData.contains("DOT")){
			rdkVersion = outputData.replace("DOT",".")
		}else if(!outputData.equals("") && !outputData.startsWith("RDK")){
			rdkVersion = "RDK"+outputData.replace("DOT",".")
		}else{
			rdkVersion = outputData
		}

		if(rdkVersion && rdkVersion.contains(" ")){
			rdkVersion.replaceAll(" ", "")
		}

		return rdkVersion
	}

	public boolean validateScriptRDKVersion(final Script scriptInstance, final String rdkVersion){
		boolean scriptStatus = true
		String versionText = rdkVersion
		if(rdkVersion){
			versionText = rdkVersion.trim()
		}
		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
			Script.withTransaction { trns ->
				def scriptInstance1 = Script.findById(scriptInstance?.id)
				if(scriptInstance1?.rdkVersions.size() > 0 && !(scriptInstance1?.rdkVersions?.find {
					it?.buildVersion?.equals(versionText)
				})){
					scriptStatus = false
				}
			}
		}
		return scriptStatus
	}
	public void updateExecutionTime(final String totalTime, final long executionResultId){
		ExecutionResult.executeUpdate("update ExecutionResult c set c.totalExecutionTime = :time where c.id = :execId",
				[time: totalTime, execId: executionResultId])
	}
	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId,
			final String timeDiff, final String singleScriptExecTime){

		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: outputData, newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.executionTime = :newTime where c.id = :execDevId",
				[newTime: timeDiff, execDevId: executionDeviceId.toLong()])
	}
	
	public void updateTotalExecutionTime(final String totalTime, final long executionId){
		Execution.executeUpdate("update Execution c set c.realExecutionTime = :time where c.id = :execId",
				[time: totalTime, execId: executionId])
	}
	/**
	 * Method to update the execution report for each test script execution.
	 * This method will update the ExecutionResult and Execution tables with new execution output.
	 *
	 * @param outputData
	 * @param executionResultId
	 * @param executionId
	 * @param timeDiff
	 */
	public void updateExecutionResultsTimeOut(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId,
			final def timeDiff, final String singleScriptExecTime){

		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: outputData, newStatus: "SCRIPT TIME OUT", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :newStatus , c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newStatus: "FAILURE", newTime: timeDiff,  execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: "FAILURE", execDevId: executionDeviceId.toLong()])

	}

	/**
	 * Method to update the execution report for each test script execution.
	 * This method will update the ExecutionResult and Execution tables with new execution output.
	 *
	 * @param outputData
	 * @param executionResultId
	 * @param executionId
	 * @param timeDiff
	 */
	public void updateExecutionResultsError(final String resultData,final long executionResultId, final long executionId, final long executionDeviceId,
			final String timeDiff, final String singleScriptExecTime){

		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: resultData, newStatus: "FAILURE", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime, c.result = :newStatus where c.id = :execId",
				[newStatus: resultData, newTime: timeDiff, newStatus: "FAILURE", execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: "FAILURE", execDevId: executionDeviceId.toLong()])

	}

	public void saveSkipStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance){
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance.stbName
				executionResult.status = SKIPPED_STATUS
				executionResult.dateOfExecution = new Date()
				executionResult.executionOutput = "Test skipped , Reason :"+scriptInstance.remarks
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}

		try {
			Execution.withTransaction {
				Execution execution = Execution.findById(executionInstance?.id)
				if(!execution.result.equals( FAILURE_STATUS )){
					execution.result = FAILURE_STATUS
					execution.save(flush:true)
				}
			}

			ExecutionDevice.withTransaction {
				ExecutionDevice execDeviceInstance = ExecutionDevice.findById(executionDevice?.id)
				if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
					execDeviceInstance.status = FAILURE_STATUS
					execDeviceInstance.save(flush:true)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	public void updateExecutionStatus(final String status, final long executionId){
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :reslt where c.id = :execId",
				[newStatus: status, reslt: status, execId: executionId.toLong()])
	}

	public void updateExecutionDeviceSkipStatus(final String status, final long executionId){
		ExecutionDevice.withTransaction {
			ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
					[newStat: status, execDevId: executionId])
		}
	}

	/**
	 * Method to save the execution status
	 * @param isAborted
	 * @param exId
	 */
	public void saveExecutionStatus(boolean isAborted, def exId){

		String status = ""
		if(isAborted){
			status = ABORTED_STATUS
		}else{
			status = COMPLETED_STATUS
		}
		try {
			Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus , c.isAborted = :abort where c.id = :execId",
					[newStatus: status, abort: isAborted, execId: exId?.toLong()])

		} catch (Exception e) {
			e.printStackTrace()
		}

	}

	/**
	 * Method to reset the agent status
	 */
	def resetAgent(def deviceInstance){

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
		callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		Thread.sleep(4000)
	}

	def resetAgent(def deviceInstance,def type){

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
		def absolutePath = layoutFolder.absolutePath
		String[] cmd = [
			PYTHON_COMMAND,
			absolutePath,
			deviceInstance?.stbIp,
			deviceInstance?.agentMonitorPort,
			type
		]
		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		Thread.sleep(4000)
	}



	/**
	 * Method to execute the script to transfer box parameters to /logs/devicelogs
	 * @param device
	 * @param logTransferPort
	 * @param realPath
	 * @return
	 */
	def getDeviceDetails(Device device, def logTransferPort, def realPath,def url){
		try {
			String scriptName = getFileTransferScriptName(device)
			File layoutFolder = grailsApplication.parentContext.getResource(scriptName).file
			def absolutePath = layoutFolder.absolutePath
			def filePath = "${realPath}//logs//devicelogs//${device?.stbName}//"
			def cmdList = [
				"python",
				absolutePath,
				device?.stbIp,
				device?.agentMonitorPort,
				"/version.txt",
				"${device?.stbName}"+"_"+"${device?.stbName}.txt"
			]

			if(scriptName?.equals(FILE_UPLOAD_SCRIPT)){
				url = updateTMUrl(url,device)
				cmdList.push(url)
			}

			String [] cmd = cmdList.toArray()

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def outputData = scriptExecutor.executeScript(cmd,1)
			copyDeviceLogIntoDir(realPath,filePath)
			parseAndSaveDeviceDetails(device, filePath)
		}catch(Exception e){
			e.printStackTrace()

		}
	}

	/**
	 * Parse the file which contains box parameters
	 * @param device
	 * @param filePath
	 * @return
	 */
	def parseAndSaveDeviceDetails(Device device, def filePath){

		try {
			File file = new File(filePath+"${device?.stbName}.txt")

			def map = [:]
			def bootargs = false

			def driversloaded = false
			def driversLoaded = ""

			def partitions = false
			def partition = ""

			def mounts = false
			def mount = ""

			file.eachLine { line ->
				if(line.startsWith("{\"paramList\"")){
					JSONObject userJson = JSON.parse(line)
					userJson.each { id, data ->
						data.each{ val ->

							switch ( val.name.toString().trim() ) {

								case "Device.DeviceInfo.Manufacturer":
									map["Manufacturer"] = val.value.toString()

								case "Device.DeviceInfo.ModelName":
									map["ModelName"] = val.value.toString()

								case "Device.DeviceInfo.SerialNumber":
									map["SerialNumber"] = val.value.toString()

								case "Device.DeviceInfo.HardwareVersion":
									map["HardwareVersion"] = val.value.toString()

								case "Device.DeviceInfo.SoftwareVersion":
									map["SoftwareVersion"] = val.value.toString()

								case "Device.DeviceInfo.ProcessorNumberOfEntries":
									map["NumberOfProcessor"] = val.value.toString()

								case "Device.DeviceInfo.Processor.1.Architecture":
									map["Architecture"] = val.value.toString()

								case "Device.DeviceInfo.UpTime":
									map["UpTime"] = val.value.toString()

								case "Device.DeviceInfo.ProcessStatus.ProcessNumberOfEntries":
									map["NumberOfProcessRunning"] = val.value.toString()

								case "Device.Ethernet.InterfaceNumberOfEntries":
									map["NumberOfInterface"] = val.value.toString()

								case "Device.DeviceInfo.MemoryStatus.Total":
									map["TotalMemory"] = val.value.toString()

								case "Device.DeviceInfo.MemoryStatus.Free":
									map["FreeMemory"] = val.value.toString()

								default:
									log.info("Default")
							}
						}
					}
				}

				if(bootargs){
					map["BootArgs"] = line
					bootargs = false
				}

				if(line.startsWith("#Bootagrs START")){
					bootargs = true
				}

				if(line.startsWith("#Driversloaded END")){
					map["Driversloaded"] = driversLoaded
					driversloaded = false
				}

				if(driversloaded){
					driversLoaded = driversLoaded + line + "<br>"
				}

				if(line.startsWith("#Driversloaded")){
					driversloaded = true
				}

				if(line.startsWith("#Partitions END")){
					map["Partitions"] = partition
					partitions = false
				}

				if(partitions){
					partition = partition + line + "<br>"
				}

				if(line.startsWith("#Partitions START")){
					partitions = true
				}

				if(line.startsWith("#mounts END")){
					map["Mount"] = mount
					mounts = false
				}

				if(mounts){
					mount = mount + line + "<br>"
				}

				if(line.startsWith("#mounts START")){
					mounts = true
				}
			}

			def deviceDetailsList = DeviceDetails.findAllByDevice(device)

			if(deviceDetailsList?.size() > 0){
				DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:device])
			}

			DeviceDetails deviceDetails = new DeviceDetails()

			map?.each{ k,v ->
				deviceDetails = new DeviceDetails()
				deviceDetails.device = device
				deviceDetails.deviceParameter = k
				deviceDetails.deviceValue = v
				deviceDetails.save(flush:true)
			}

		} catch (Exception e) {
		}

	}

	public boolean validateScriptRDKVersions(final Map script, final String rdkVersion){
		boolean scriptStatus = true
		String versionText = rdkVersion
		if(rdkVersion){
			versionText = rdkVersion.trim()
		}
		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
			Script.withTransaction { trns ->
				if(script?.rdkVersions?.size() > 0 && !(script?.rdkVersions?.find {
					it?.buildVersion?.equals(versionText)
				})){
					scriptStatus = false
				}
			}
		}
		return scriptStatus
	}

	public boolean validateScriptBoxTypes(final Map script, final Device deviceInstance){
		boolean scriptStatus = true
		Script.withTransaction { trns ->
			def deviceInstance1 = Device.findById(deviceInstance?.id)
			if(!(script?.boxTypes?.find { it?.toString()?.equals(deviceInstance1?.boxType?.toString()) })){
				//if(!(script?.boxTypes?.find { it?.id == deviceInstance1?.boxType?.id })){
				scriptStatus = false
			}
		}
		return scriptStatus
	}



	def getScript(realPath,dirName,fileName, category){
		dirName = dirName?.trim()
		fileName = fileName?.trim()

		def moduleObj = Module.findByNameAndCategory(dirName,category)
		def scriptDirName = Constants.COMPONENT
		if(moduleObj){
			if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
				scriptDirName = Constants.INTEGRATION
			}
		}
		//File file = new File( "${realPath}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
		File file = null
		def fileStorePath = Utility.getFileStorePath(realPath, category,dirName,fileName)
		def primitiveFileStorePath = Utility.getPrimitiveFileStorePath(realPath, category)
		file = new File(fileStorePath+FILE_SEPARATOR+scriptDirName+FILE_SEPARATOR+dirName+FILE_SEPARATOR+fileName+".py")
		Map script = [:]
		if(file.exists()){
			//String s = ""
			StringBuilder s = new StringBuilder()
			List line = file.readLines()
			//int indx = 0
			int indx = line?.findIndexOf {  it.startsWith("'''")}
			String scriptContent = ""
			if(line.get(indx).startsWith("'''"))	{
				indx++
				while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
					//	s = s + line.get(indx)+"\n"
					s.append(line.get(indx)).append('\n')
					indx++
				}
				indx ++
				while(indx < line.size()){
					scriptContent = scriptContent + line.get(indx)+"\n"
					indx++
				}
			}


			String xml = s.toString()
			XmlParser parser = new XmlParser();
			def node = parser.parseText(xml)
			script.put("id", node.id.text())
			script.put("version", node.version.text())
			script.put("name", node.name.text())
			script.put("skip", node.skip.text())
			def nodePrimitiveTestName = node.primitive_test_name.text()
			def primitiveMap = PrimitiveService.primitiveModuleMap
			def moduleName1 = primitiveMap.get(nodePrimitiveTestName)

			def moduleObj1 = Module.findByName(dirName)
			def scriptDirName1 = Constants.COMPONENT
			if(moduleObj1){
				if(moduleObj1?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName1 = Constants.INTEGRATION
				}
			}
			def primitiveTest = getPrimitiveTest(primitiveFileStorePath+FILE_SEPARATOR+scriptDirName1+FILE_SEPARATOR+moduleName1+FILE_SEPARATOR+moduleName1+".xml",nodePrimitiveTestName)
			//def primitiveTest = getPrimitiveTest(realPath+"//fileStore//testscripts//"+scriptDirName1+"//"+moduleName1+"//"+moduleName1+".xml",nodePrimitiveTestName)

			script.put("primitiveTest",primitiveTest)
			def versList = []
			def btList = []
			def testProfileList =[]
			Set btSet = node?.box_types?.box_type?.collect{ it.text() }
			Set versionSet = node?.rdk_versions?.rdk_version?.collect{ it.text() }
			Set testProfileSet =  node?.test_profiles?.test_profile?.collect{ it.text() }
			btSet.each { bt ->
				btList.add(BoxType.findByName(bt))
			}
			versionSet.each { ver ->
				versList.add(RDKVersions.findByBuildVersion(ver))
			}
			testProfileSet?.each{ tProfile ->
				testProfileList?.add(TestProfile?.findByName(tProfile))
			}
			script.put("rdkVersions", versList)
			script.put("boxTypes", btList)
			script.put("status", node?.status?.text())
			script.put("synopsis", node?.synopsis?.text())
			script.put("scriptContent", scriptContent)
			script.put("executionTime", node.execution_time.text())
			script.put("testProfile",testProfileList)
			def testCaseDeatilsMap =[:]
			if(node?.test_cases){
				testCaseDeatilsMap?.put(T_C_ID,node?.test_cases?.test_case_id?.text())
				testCaseDeatilsMap?.put(T_C_OBJ,node?.test_cases?.test_objective?.text())
				testCaseDeatilsMap?.put(T_C_TYPE,node?.test_cases?.test_type?.text())
				testCaseDeatilsMap?.put(T_C_SETUP,node?.test_cases?.test_setup?.text())
				//testCaseDeatilsMap?.put(T_C_STREAM_ID,node?.test_cases?.steam_id?.text())
				testCaseDeatilsMap?.put(T_C_SKIP,node?.test_cases?.skipped?.text())
				testCaseDeatilsMap?.put(T_C_PRE_REQUISITES, node?.test_cases?.pre_requisite?.text())
				testCaseDeatilsMap?.put(T_C_INTERFACE,node?.test_cases?.api_or_interface_used?.text())
				testCaseDeatilsMap?.put(T_C_IOPARAMS, node?.test_cases?.input_parameters?.text())
				testCaseDeatilsMap?.put(T_C_AUTOAPROCH,node?.test_cases?.automation_approch?.text())
				
				if(node?.test_cases?.expected_output){
					testCaseDeatilsMap?.put(T_C_EX_OUTPUT,node?.test_cases?.expected_output?.text())
				}
				else{
					testCaseDeatilsMap?.put(T_C_EX_OUTPUT,node?.test_cases?.except_output?.text())
				}			
				testCaseDeatilsMap?.put(T_C_PRIORITY,node?.test_cases?.priority?.text())
				testCaseDeatilsMap?.put(T_C_TSI, node?.test_cases?.test_stub_interface?.text())
				testCaseDeatilsMap?.put(T_C_SCRIPT,node?.test_cases?.test_script?.text())
				testCaseDeatilsMap?.put(T_C_RELEASE_VERSION,node?.test_cases?.release_version?.text())
				testCaseDeatilsMap?.put(T_C_REMARKS,node?.test_cases?.remarks?.text())
				script?.put(T_C_DETAILS,testCaseDeatilsMap)
			}else{
				testCaseDeatilsMap?.put(T_C_ID,"")
				testCaseDeatilsMap?.put(T_C_OBJ,"")
				testCaseDeatilsMap?.put(T_C_TYPE,"")
				testCaseDeatilsMap?.put(T_C_SETUP,"")
				//testCaseDeatilsMap?.put(T_C_STREAM_ID,"")
				testCaseDeatilsMap?.put(T_C_SKIP,"")
				testCaseDeatilsMap?.put(T_C_PRE_REQUISITES, "")
				testCaseDeatilsMap?.put(T_C_INTERFACE,"")
				testCaseDeatilsMap?.put(T_C_IOPARAMS, "")
				testCaseDeatilsMap?.put(T_C_AUTOAPROCH,"")
				testCaseDeatilsMap?.put(T_C_EX_OUTPUT,"")
				testCaseDeatilsMap?.put(T_C_PRIORITY,"")
				testCaseDeatilsMap?.put(T_C_TSI, "")
				testCaseDeatilsMap?.put(T_C_SCRIPT,"")
				testCaseDeatilsMap?.put(T_C_RELEASE_VERSION,"")
				testCaseDeatilsMap?.put(T_C_REMARKS,"")
				script?.put(T_C_DETAILS,testCaseDeatilsMap)
			}
		}
		return script
	}



	def getPrimitiveTest(def filePath,def primitiveTestName){
		def newFilePath = null
		def testScriptsPath = null
		def categoryFound = false

		if(!(filePath.contains(FileStorePath.RDKV.value()) || filePath.contains(FileStorePath.RDKB.value()))) {
			categoryFound = PrimitiveService.primitiveListMap.get('RDKV')?.contains(primitiveTestName?.trim())
			if(!categoryFound) {
				categoryFound = PrimitiveService.primitiveListMap.get('RDKB')?.contains(primitiveTestName?.trim())
				if(!categoryFound){
					categoryFound = PrimitiveService.primitiveListMap.get('RDKB')?.contains(primitiveTestName)
				}
				if(categoryFound){
					testScriptsPath = FileStorePath.RDKB.value()
				}
			}else{
				testScriptsPath = FileStorePath.RDKV.value()
			}

			if(testScriptsPath != null) {
				def paths = filePath.split('fileStore')
				def file = null
				def fileName = paths[1].split('testscripts')
				file = fileName[1]?fileName[1]:fileName[0]
				newFilePath = paths[0] + 'fileStore' + FILE_SEPARATOR + testScriptsPath + file
			}
		}else{
			newFilePath = filePath
		}

		Map primitiveMap = [:]
		try {
			//File primitiveXml = new File(filePath)
			File primitiveXml = new File(newFilePath)
			//	def local = new XmlParser()
			//	def node = local.parse(primitiveXml)
			def lines = primitiveXml?.readLines()
			int indx = lines?.findIndexOf { it.startsWith("<?xml")}
			String xmlContent =""
			while(indx < lines.size()){
				xmlContent = xmlContent + lines.get(indx)+"\n"
				indx++
			}
			def parser = new XmlParser();
			def node = parser.parseText(xmlContent?.toString())

			node.each{
				it.primitiveTests.each{
					it.primitiveTest.each {
						if("${it.attribute('name')}".equalsIgnoreCase(primitiveTestName)){
							primitiveMap.put("name", "${it.attribute('name')}")
							primitiveMap.put("version",  "${it.attribute('version')}")
							primitiveMap.put("id","${it.attribute('id')}")
							Set paramList = []
							def moduleName = PrimitiveService.primitiveModuleMap.get(primitiveTestName)
							primitiveMap.put("module",Module.findByName(moduleName))
							def fun = Function.findByModuleAndName(Module.findByName(moduleName),it.function.text())
							primitiveMap.put("function",fun)
							it.parameters.each {
								it.parameter.each{
									def pType = ParameterType.findByNameAndFunction("${it.attribute('name')}",fun)
									Map param = [:]
									param.put("parameterType",pType)
									param.put("value", "${it.attribute('value')}")
									paramList.add(param)
								}
								primitiveMap.put("parameters",paramList)
							}
							//				 return primitiveMap
						}else{
							def ss = "${it.attribute('name')}"
							if(ss == primitiveTestName){
							}
						}
					}
				}
			}
		} catch (Exception e) {
			primitiveMap = null
			e.printStackTrace()
		}
		return primitiveMap
	}


	public void savePausedExecutionStatus(def exId){
		try {
			Execution.withSession {
				Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus where c.id = :execId",
						[newStatus: "PAUSED", execId: exId?.toLong()])
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

	}

	public void saveExecutionDeviceStatusData(String status, def exDevId){

		try {
			ExecutionDevice.withSession {
				ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStatus  where c.id = :execId",
						[newStatus: status, execId: exDevId?.toLong()])
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

	}

	public void saveNoScriptAvailableStatus(def executionInstance , def executionDevice , def scriptName , def deviceInstance, String reason, def category){
		try{
			ExecutionResult.withTransaction { resultstatus ->
				try {
					ExecutionResult executionResult = new ExecutionResult()
					executionResult.execution = executionInstance
					executionResult.executionDevice = executionDevice
					executionResult.script = scriptName
					executionResult.device = deviceInstance?.stbName
					executionResult.status = Constants.SKIPPED_STATUS
					executionResult.dateOfExecution = new Date()
					executionResult.category = category
					executionResult.executionOutput = "Test not executed. Reason : "+reason
					if(! executionResult.save(flush:true)) {
						log.error "Error saving executionResult instance : ${executionResult.errors}"
					}
					resultstatus.flush()
				}
				catch(Throwable th) {
					resultstatus.setRollbackOnly()
				}
			}
		}catch(Exception ee){
		}
	}

	def initiateLogTransfer(String executionName, String server, String logAppName, Device device){
		int count = 3
		boolean logTransferInitiated = false

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
	}

	def isTclScriptExists(String realPath, String fileName){
		def isExists = false
		def tcl = getTclFilePath(realPath, fileName)
		if(tcl){
			isExists = true
		}
		isExists
	}

	def getTclFilePath(String realPath, String fileName){
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(fileName+".tcl")
					};
				})
		if(tcl.length == 1){
			return tcl[0]?.absolutePath
		}
		return null
	}

	def getTclDirectory(String realPath) {
		realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
	}

	def isConfigFileExists(def realPath, def deviceName){
		def isExists = false
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(deviceName+".txt")
					};
				})
		if(tcl.length == 1){
			isExists = true
		}
		isExists
	}

	def getConfigFilePath(String realPath, String deviceName){
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(deviceName+".txt")
					};
				})
		if(tcl.length == 1){
			return tcl[0]?.absolutePath
		}
		return null
	}


	/**
	 * Updating the execution results  
	 * 
	 */
	public void updateTclExecutionResults(def params){
		try {
			String actualResult = params.resultData
			if(actualResult){
				ExecutionResult.withTransaction {
					ExecutionResult executionResult = ExecutionResult.findById(params.execResult)
					if(executionResult){
						ExecuteMethodResult executionMethodResult = new ExecuteMethodResult()
						if(params.resultStatus?.equals( STATUS_NONE ) || params.resultStatus == null ){
							executionMethodResult.status = actualResult
						}
						else{
							executionMethodResult.executionResult = executionResult
							executionMethodResult.expectedResult = params.expectedResult
							executionMethodResult.actualResult = actualResult
							executionMethodResult.status = params.resultStatus
						}
						executionMethodResult.functionName = params.testCaseName
						executionMethodResult.category = executionResult?.category
						executionMethodResult.save(flush:true)

						executionResult?.addToExecutemethodresults(executionMethodResult)
						executionResult.executionOutput = params.outputData
						executionResult.executionTime = params.singleScriptExecTime
						executionResult?.save(flush:true)

						Execution execution = Execution.findById(params.execId)
						ExecutionDevice execDeviceInstance = ExecutionDevice.findById(params.execDevice)
						if(!executionResult?.status.equals( FAILURE_STATUS )){
							executionResult?.status = params.resultStatus
							executionResult?.save(flush:true)
							if(!execution.result.equals( FAILURE_STATUS )){
								execution.result = params.resultStatus
								execution.outputData = params.outputData
								execution.executionTime = params.singleScriptExecTime
								execution.save(flush:true)
							}
							if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
								execDeviceInstance?.addToExecutionresults(executionResult)
								execDeviceInstance?.status = params.resultStatus
								execDeviceInstance.executionTime = params.singleScriptExecTime
								execDeviceInstance?.save(flush:true)
							}
						}
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace()
		}
	}
	
	def getIPV4LogUploadMechanism(){
		String mechanism = Constants.TFTP_MECHANISM
		try {
			File configFile = grailsApplication.parentContext.getResource(Constants.TM_CONFIG_FILE).file
			mechanism = getConfigProperty(configFile, Constants.LOG_UPLOAD_IPV4)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return mechanism
	}
	
	public static String getConfigProperty(File configFile, String key) {
		try {
			Properties prop = new Properties();
			if (configFile.exists()) {
				InputStream is = new FileInputStream(configFile);
				prop.load(is);
				String value = prop.getProperty(key);
				if (value != null && !value.isEmpty()) {
					return value;
				}
			}else{
				System.out.println("DBG :::: No Config File !!! ");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * Function for updating the TM ip[ipv6, ipv4] according to the  device selection
	 * @param url
	 * @param device
	 * @return
	 */
	   def updateTMUrl(String url,Device device){
		   try {
			   if(InetUtility.isIPv6Address(device?.stbIp) && device?.category?.equals(Category.RDKV)){
				   File configFile = grailsApplication.parentContext.getResource("/fileStore/tm.config").file
						   String ipV6Address = InetUtility.getIPAddress(configFile, Constants.IPV6_INTERFACE)
						   String ipV4Address = InetUtility.getIPAddress(configFile, Constants.IPV4_INTERFACE)
						   if(ipV4Address &&ipV6Address && !ipV4Address.isEmpty() && !ipV6Address.isEmpty()){
							   url = url.replace(ipV4Address, "[${ipV6Address}]")
						   }
			   }
		   } catch (Exception e) {
			   e.printStackTrace()
		   }
		   return url
	   }
	   
	   /**
	    *to Copy the logs into specified directory
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
		* To initiate the diagnostics test
		*/
	   def initiateDiagnosticsTest(def deviceInstance , def diagFileName , def tmUrl ,def uniqueExecutionName){
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

}
