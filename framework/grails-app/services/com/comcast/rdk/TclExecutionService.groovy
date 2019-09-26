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
import grails.util.Holders
import groovy.sql.Sql

import java.util.Date;
import java.util.concurrent.Callable
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.Future

import org.springframework.util.StringUtils

import com.comcast.rdk.Utility

class TclExecutionService {

	static transactional = false

	public static volatile Object  lock = new Object()

	private static ExecutorService executorService = Executors.newCachedThreadPool()

	def dataSource
	def executionService
	def executescriptService
	def deviceStatusService
	def messageSource
	def logTransferService
	def grailsApplication = Holders.grailsApplication
	def scriptExecutionService
	def scriptService


	def executeTclScripts(def params, def realPath, def applicationUrl){
		boolean aborted = false
		def exId
		def scriptGroupInstance
		def scriptStatus = true
		def scriptVersionStatus = true
		Device deviceInstance //= Device.findById(params?.id, [lock: true])
		String htmlData = ""
		def deviceId
		def executionName
		def scriptType = params?.myGroup
		def deviceList = []
		def deviceName
		boolean allocated = false
		boolean singleScript = false

		ExecutionDevice executionDevice = new ExecutionDevice()
		if(params?.devices instanceof String){
			deviceList << params?.devices
			deviceInstance = Device.findById(params?.devices, [lock: true])
			deviceName = deviceInstance?.stbName
		}
		else{
			(params?.devices).each{ deviceid ->
				deviceList << deviceid
			}
			deviceName = MULTIPLE
		}

		if(params?.execName){
			executionName = params.execName
		}
		else{
			executionName = params?.name
		}

		int repeatCount = 1
		if(params?.repeatNo){
			repeatCount = (params?.repeatNo)?.toInteger()
		}
		def executionInstance = Execution.findByName(executionName)
		StringBuilder output = new StringBuilder();

		if(deviceList.size() > 1){
			output.append("Multiple Device Execution ")
		}

		try{
			def isBenchMark = FALSE
			def isSystemDiagnostics = FALSE
			def isLogReqd = FALSE
			def rerun = FALSE
			if(params?.systemDiagnostics.equals(KEY_ON)){
				isSystemDiagnostics = TRUE
			}
			if(params?.benchMarking.equals(KEY_ON)){
				isBenchMark = TRUE
			}

			if(params?.transferLogs.equals(KEY_ON)){
				isLogReqd = TRUE
			}

			if(params?.rerun.equals(KEY_ON)){
				rerun = TRUE
			}
			def scriptName
			//String url = getApplicationUrl()
			String url = applicationUrl
			String filePath = realPath + FILE_SEPARATOR + "fileStore"
			def execName
			def executionNameForCheck
			def combinedScript  = [:]
			boolean confPresent = true
			Map deviceDetails = [:]
			for(int i = 0; i < repeatCount; i++ ){
				executionNameForCheck = null
				deviceList.each{ device ->
					deviceInstance = Device.findById(device)
					boolean validScript = false
					deviceName = deviceInstance?.stbName
					if(scriptType == SINGLE_SCRIPT){
						def scripts = params?.scripts
						if(scripts instanceof String){
							singleScript = true
							//def scriptInstance1 = getTclBoxDetails(realPath, deviceInstance?.stbName)
							def scriptInstance1 = [:]					
							
							boolean combinedTCL = false
							def combainedTclScript =  scriptService?.combinedTclScriptMap
							combainedTclScript?.each{
								if(it?.value?.toString().contains(scripts?.toString())){
									combinedTCL = true
								}
							}							
							if((scriptService?.totalTclScriptList?.toString()?.contains(scripts?.toString())) && combinedTCL ){
								combainedTclScript?.each{									
									if(it?.value?.toString()?.contains(scripts?.toString())){
										scripts = it.key?.toString()
									}
								}
							}
							def scriptValid = Utility.isTclScriptExists(realPath,  scripts?.toString())
							if(scriptValid) {
								if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){									
										scriptInstance1.put('scriptName',scripts )									
									validScript = true									
								}
								else{
									confPresent = false
									htmlData = "<br>"+deviceName +"  : No Config file is available with name Config_${deviceInstance?.stbName}.txt"
								}

							}else{
								htmlData = "<br>"+deviceName +"  : No TCL Script is available with name ${params?.scripts}"
							}
							
						}
						else{						
							scripts.each { script ->
								def scriptInstance1 = [:]
								boolean combinedTCL = false
								def combainedTclScript =  scriptService?.combinedTclScriptMap
								combainedTclScript?.each{
									if(it?.value?.toString().contains(script?.toString())){
										combinedTCL = true
									}
								}
								if((scriptService?.totalTclScriptList?.toString()?.contains(script?.toString())) && combinedTCL ){
									combainedTclScript?.each{
										if(it?.value?.toString()?.contains(script?.toString())){
											script = it.key?.toString()
										}
									}
								}								
								def scriptValid = Utility.isTclScriptExists(realPath, script)
								if(scriptValid) {
									if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
										scriptInstance1.put('scriptName',script )
										validScript = true
									}else{
										confPresent = false
									}
								/*scriptInstance1.put('scriptName',script )
									 if(scriptInstance1){
									 validScript = true
									 // deepesh to implement validation of boxtypes and rdk version 
									 if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
									 String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
									 if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
									 validScript = true
									 }
									 }
									 }*/	
								}
							}
						}
					}else{
						def scriptGroup = ScriptGroup.findById(params?.scriptGrp,[lock: true])
						//String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
						try{
							
							scriptGroup?.scriptList?.each{ script ->
								//def scriptInstance1 = getTclBoxDetails(realPath, deviceInstance?.stbName)
								if((scriptService?.totalTclScriptList?.toString()?.contains(script?.scriptName?.toString())) || !(scriptService?.tclScriptsList?.toString()?.contains(script?.scriptName?.toString())) ){
									def combainedTclScript =  scriptService?.combinedTclScriptMap
									combainedTclScript?.each{										
										if(it?.value?.toString()?.contains(script?.scriptName?.toString())){
											//def scriptFile = ScriptFile?.findByScriptName(it.key?.toString())
											script = ["scriptName" : it?.key?.toString()]	
										}
									}
								}
								def scriptValid = Utility.isTclScriptExists(realPath, script?.scriptName?.toString())
								if(scriptValid) {
									if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
										//scriptInstance1.put('scriptName',script )
										validScript = true
									}else{
										confPresent = false
									}
								}								
							}
						}catch(Exception e ){
						println " ERROR "+e.getMessage()
							if(e.getMessage() == "return from closure" ){

							}else{
								validScript = false
							}
						}
					}
					if(validScript){
						if(deviceList.size() > 1){
							executionNameForCheck = null
						}
						boolean paused = false
						int pending = 0
						int currentExecutionCount = -1
						Map statusMap = deviceDetails.get(device)
						if(statusMap){
							paused = ((boolean)statusMap.get("isPaused"))
							pending = ((int)statusMap.get("pending"))
							currentExecutionCount = ((int)statusMap.get("currentExecutionCount"))
						}
						String status = ""
						deviceInstance = Device.findById(device)
						try {
							status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)

							//synchronized (ExecutionController.lock) {
							if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
								status = "BUSY"
							}else{
								if((status.equals( Status.FREE.toString() ))){
									if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
										allocated = true
										executionService.deviceAllocatedList.add(deviceInstance?.id)
										//Thread.start{
										Device.withTransaction {
											deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
										}
									}
								}
							}
						}
						catch(Exception eX){
							println eX.message
						}
						if( !paused && (status.equals( Status.FREE.toString() ))){
							if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
								allocated = true
								executionService.deviceAllocatedList.add(deviceInstance?.id)
							}
							deviceInstance = Device.findById(device)
							def executionSaveStatus = true
							def execution = null
							def scripts = null
							deviceId = deviceInstance?.id
							if(scriptType == SINGLE_SCRIPT){
								scripts = params?.scripts
								if(scripts instanceof String){
									//def scriptInstance1 = getTclBoxDetails(realPath, deviceInstance?.stbName)
									// to implement validation of boxtypes and rdk version
									scriptStatus = scriptVersionStatus = true
									/*scriptStatus = executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)
									 String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
									 scriptVersionStatus = executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)*/
									scriptName = scripts
								}
								else{
									scriptName = MULTIPLESCRIPT
								}
							}else{
								scriptGroupInstance = ScriptGroup.findById(params?.scriptGrp,[lock: true])
							}
							if(scriptStatus && scriptVersionStatus){
								if(!executionNameForCheck){
									String exName = executionName
									if(deviceList.size() > 1){
										deviceName = deviceInstance?.stbName
										exName = deviceInstance?.stbName +"-"+executionName
									}
									if(i > 0){
										execName = exName + UNDERSCORE +i
									}
									else{
										execName = exName
									}
									// Test case count include in the multiple scripts executions
									if(scriptName.equals(MULTIPLESCRIPT)){
										def  scriptCount = params?.scripts?.size()
										executionSaveStatus = executionService.saveExecutionDetailsOnMultipleScripts(execName, scriptName, deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun,isLogReqd,scriptCount, "RDKB_TCL", FALSE)
									}else{																											
										executionSaveStatus = executionService.saveExecutionDetails(execName, [scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance, appUrl : url, isBenchMark : isBenchMark, isSystemDiagnostics: isSystemDiagnostics, rerun : rerun, isLogReqd:isLogReqd, category: "RDKB_TCL", rerunOnFailure : FALSE])
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
									try{
										executionDevice = new ExecutionDevice()
										executionDevice.execution = Execution.findByName(execName)
										executionDevice.dateOfExecution = new Date()
										executionDevice.device = deviceInstance?.stbName
										executionDevice.deviceIp = deviceInstance?.stbIp
										executionDevice.status = UNDEFINED_STATUS
										executionDevice.category = Category.RDKB_TCL
										executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
										executionDevice.save(flush:true)
									}
									catch(Exception e){
										e.printStackTrace()
									}
									def scriptId
									if((!(params?.scriptGrp)) && (!(params?.scripts))){
										//render ""
										return
									}
									else{
										executionService.executeVersionTransferScript(realPath, filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
									}
									if(deviceList.size() > 1){
										executeScriptInThread(execName, device, executionDevice, params?.scripts, params?.scriptGrp, executionName,
												filePath, realPath , params?.myGroup, url, isBenchMark, isSystemDiagnostics, params?.rerun, isLogReqd, params?.category)
										htmlData=" <br> " + deviceName+"  :   Execution triggered "
										output.append(htmlData)


									}else{

										htmlData = executescriptsOnDevice(execName, device, executionDevice, params?.scripts, params?.scriptGrp, executionName,
												filePath, realPath, params?.myGroup, url, isBenchMark, isSystemDiagnostics, params?.rerun,isLogReqd, params?.category)
										output.append(htmlData)
										Execution exe = Execution.findByName(execName)
										if(exe){
											def executionList = Execution.findAllByExecutionStatusAndName("PAUSED",execName);
											paused = (executionList.size() > 0)
										}
									}

									if(paused){
										currentExecutionCount = i
										statusMap = deviceDetails.get(device)
										if(statusMap == null){
											statusMap = [:]
											deviceDetails.put(device,statusMap)
										}

										if(statusMap != null){
											statusMap.put("isPaused", true)
											statusMap.put("currentExecutionCount", i)
											statusMap.put("pending", pending)
										}

									}
								}
							}

							/*else{
							 def devcInstance = Device.findById(device)
							 if(!scriptStatus){
							 htmlData ="<br>"+deviceName+"  :  "+ message(code: 'execution.boxtype.nomatch')
							 }else{
							 htmlData ="<br>"+deviceName+ " :  RDK Version supported by the script is not matching with the RDK Version of selected Device "+devcInstance?.stbName+"<br>"
							 }
							 if(executionService.deviceAllocatedList.contains(devcInstance?.id)){
							 executionService.deviceAllocatedList.remove(devcInstance?.id)
							 }
							 output.append(htmlData)
							 }*/
							htmlData = ""
						}else{

							if(paused){
								try {
									pending ++

									statusMap = deviceDetails.get(device)

									if(statusMap != null){
										statusMap.put("pending", pending)
									}

									if(i == repeatCount -1){
										executionService.saveRepeatExecutionDetails(execName, deviceInstance?.stbName,currentExecutionCount, pending, params?.category)
									}

								} catch (Exception e) {
									e.printStackTrace()
								}
							}else{

								if(i > 0){
									def execName1 = executionName + UNDERSCORE +i

									try {

										Execution execution = new Execution()
										execution.name = execName1
										execution.script = scriptName
										execution.device = deviceName
										execution.scriptGroup = scriptGroupInstance?.name
										execution.result = FAILURE_STATUS
										execution.executionStatus = FAILURE_STATUS
										execution.dateOfExecution = new Date()
										execution.category = Utility.getCategory(params?.category)
										execution.groups = executionService.getGroup()
										execution.applicationUrl = url
										execution.isRerunRequired = rerun?.equals("true")
										execution.isBenchMarkEnabled = isBenchMark?.equals("true")
										execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals("true")
										execution.isStbLogRequired = isLogReqd?.equals("true")
										execution.rerunOnFailure= FALSE
										execution.outputData = "Execution failed due to the unavailability of box"
										if(! execution.save(flush:true)) {
											log.error "Error saving Execution instance : ${execution.errors}"
										}
									}
									catch(Exception th) {
										th.printStackTrace()
									}
								}

								htmlData = "<br>"+deviceName+" : Device is not free to execute scripts"
								output.append(htmlData)
							}
						}
					}else{


						if(!confPresent){
							htmlData = "<br>"+deviceName +"  : No Config file is available with name Config_${deviceInstance?.stbName}.txt"
						}
						else if(! singleScript){
							htmlData = "<br>"+deviceName+ "  :  No valid script available to execute."
						}


						output.append(htmlData)
					}
				}
			}
		}finally{
			if(deviceList.size() == 1){
				deviceList.each{ device ->
					def devInstance = Device.findById(device)
					if(allocated && executionService.deviceAllocatedList.contains(devInstance?.id)){
						executionService.deviceAllocatedList.remove(devInstance?.id)
					}
				}

				String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				Thread.start{
					println Thread.currentThread()
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
				}
			}
		}
		htmlData = output.toString()
		//}
		return htmlData
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
	
	
	def executescriptsOnDevice(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun,def isLogReqd, def category) {
		boolean aborted = false
		boolean pause = false
		def scriptInstance
		Device deviceInstance
		Device.withTransaction {
			deviceInstance= Device.findById(device)
		}
		
		ScriptGroup scriptGroupInstance
		StringBuilder output = new StringBuilder();
		def htmlData = ""
		int scriptGrpSize = 0
		int scriptCounter = 0
		def isMultiple = TRUE
		List pendingScripts = []
		try{
			if(groupType == TEST_SUITE){				
				scriptCounter = 0
				boolean skipStatus = false
				boolean notApplicable = false
				List validScriptList = new ArrayList()
				String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
				def tclCombainedScriptMap = [:]				
				ScriptGroup.withTransaction { trans ->
					scriptGroupInstance = ScriptGroup.findById(scriptGrp)
					scriptGroupInstance?.scriptList?.each { script ->
						//def scriptInstance1 = scriptService.getScript(realPath,script?.moduleName, script?.scriptName, category)
						def scriptInstance1 = [:]
						def combainedTclScript =  scriptService?.combinedTclScriptMap
						def newScriptName  = ""
						boolean tclCombained =  false
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(script?.scriptName.toString())){
								tclCombainedScriptMap.put(script?.scriptName,it.key?.toString())								
								newScriptName = it.key?.toString()
								tclCombained = true
							}
						}
						if(tclCombained ){
							newScriptName= newScriptName
						}else{
							newScriptName = script?.scriptName?.toString()
						}
						if(Utility.isTclScriptExists(realPath, newScriptName)){
							if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){		
								if(tclCombained){
									scriptInstance1.put('scriptName',newScriptName)	
								}else{
									scriptInstance1.put('scriptName', script?.scriptName)									
								}
								validScriptList << scriptInstance1
							}
							else{
								String reason = "No config file is available with name : Config_"+deviceInstance?.stbName+".txt"
								executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script?.scriptName, deviceInstance,reason, category)
							}
    //// implement validation of boxtypes and rdk version

							/*if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
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
							 rdkVersionData = scriptInstance1?.rdkVersions
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
							 boxTypeData = scriptInstance1?.boxTypes
							 String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
							 executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance1, deviceInstance,reason, category)
							 }*/
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
				if(validScriptList.size() > 0){
					logTransferService.transferLog(execName, deviceInstance)
				}	
				int index = 0				
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
							if(devStatus.equals(Status.HANG.toString())){
								executescriptService.resetAgent(deviceInstance, TRUE)
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
							def combainedTcl = [:]
							//combainedTcl?.put("scriptName","")
							 if(scriptGroupInstance?.scriptList?.size() ==  validScriptList?.size()){
								 if( !(scriptService?.totalTclScriptList?.toString()?.contains(scriptObj?.scriptName?.toString())) && scriptService?.tclScriptsList?.toString()?.contains(scriptObj?.scriptName?.toString())){
									 combainedTcl?.put("scriptName", scriptGroupInstance?.scriptList[index]?.toString())
								 }else{
								 	combainedTcl?.put("scriptName","")									
								 }
							 }
							 index = index + 1
							
							htmlData = executeScript(execName, executionDevice, scriptObj, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics, executionName, isMultiple,null,isLogReqd, category, combainedTcl)

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
							def newScriptName 
							if(scriptGroupInstance?.scriptList?.size() ==  validScriptList?.size()){								
								if(!(scriptService?.totalTclScriptList?.toString()?.contains(scriptObj?.scriptName?.toString())) && scriptService?.tclScriptsList?.toString()?.contains(scriptObj?.scriptName?.toString())){
									
									newScriptName= scriptGroupInstance?.scriptList[index]?.toString()
									
									
								}else{
									
									newScriptName = scriptObj?.scriptName?.toString()
								}			
							}							
							try {
								pendingScripts.add(newScriptName)
								def execInstance
								Execution.withTransaction {
									def execInstance1 = Execution.findByName(execName)
									execInstance = execInstance1
								}
								def scriptInstanceObj
								scriptInstanceObj = newScriptName
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
										executionResult.script = scriptInstanceObj
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
							index = index + 1

						}
					}
				}

				if(validScriptList.size() > 0){
					logTransferService.closeLogTransfer(execName)
				}

				if(aborted && executionService.abortList.contains(exeId?.toString())){
					executionService.abortList.remove(exeId?.toString())
				}

				if(!aborted && pause && pendingScripts.size() > 0 ){
					def exeInstance = Execution.findByName(execName)
					executionService.savePausedExecutionStatus(exeInstance?.id)
					executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
				}
			}
			else if(groupType == SINGLE_SCRIPT){
				
				if(scripts instanceof String){
					
					def script1 = [:]
					def combinedScript = [:]
					def scriptNameTcl
					boolean tclCombained =  false
					boolean combinedTCL = false
					def combainedTclScript =  scriptService?.combinedTclScriptMap
					combainedTclScript?.each{ 
						if(it?.value?.toString().contains(scripts?.toString())){
							combinedTCL = true 							
						}						
					}
					if((scriptService?.totalTclScriptList?.toString()?.contains(scripts?.toString())) && combinedTCL ){
						scriptNameTcl = scripts						
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(scripts?.toString())){
								scripts = it.key?.toString()								
								tclCombained =true
							}
						}
					}				
					if(Utility.isTclScriptExists(realPath, scripts)){
						if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
							script1.put('scriptName', scripts)
							if(tclCombained){
								combinedScript.put("scriptName",scriptNameTcl)
							}else{
								combinedScript?.put("scriptName","")
							}
						}
					}	
					def startExecutionTime = new Date()
					isMultiple = FALSE
					try { 						
						htmlData = executeScript(execName, executionDevice, script1, deviceInstance, url, filePath, realPath, isBenchMark,
								isSystemDiagnostics,executionName,isMultiple,null,isLogReqd, category, combinedScript )
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
					def tclCombained = false
					boolean combinedTCL = false
					def scriptNameTcl
					def combinedScript = [:]				
					scripts.each { script ->						
						scriptInstance = [:]
						def combainedTclScript =  scriptService?.combinedTclScriptMap						
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(script?.toString())){								
								script = it.key?.toString()
							}
						}						
						if(Utility.isTclScriptExists(realPath, script)){
							if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
								scriptInstance.put('scriptName',script)								
								validScripts << scriptInstance								
							}
							else{
								String reason = "No config file is available with name : Config_"+deviceInstance?.stbName+".txt"
								executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason, category)
							}
	//  to implement validation of boxtypes and rdk version

							/*if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance)){
							 if(executionService.validateScriptRDKVersions(scriptInstance,rdkVersion)){
							 if(scriptInstance?.skip?.toString().equals("true")){
							 skipStatus = true
							 executionService.saveSkipStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance)
							 }else{
							 validScripts << scriptInstance
							 }
							 }else{
							 notApplicable = true
							 String rdkVersionData = ""
							 rdkVersionData = scriptInstance?.rdkVersions
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
							 boxTypeData = scriptInstance?.boxTypes
							 String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
							 executionService.saveNotApplicableStatus(Execution.findByName(execName), executionDevice, scriptInstance, deviceInstance,reason, category)
							 }*/
						}else{
							String reason = "No tcl script is available with name :"+script+".tcl"
							executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), executionDevice, script, deviceInstance,reason, category)
						}
					}
					scriptGrpSize = validScripts?.size()
					Execution ex = Execution.findByName(execName)
					def exeId = ex?.id
					try{
						if((skipStatus || notApplicable)&& scriptGrpSize == 0){
							executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, exeId)
							executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, executionDevice?.id)
						}
					}
					catch(Exception e){
						println e.message
					}
					String devStatus = ""
					int index = 0
					
					validScripts.each{ script ->					
						scriptCounter++
						if(scriptCounter == scriptGrpSize){
							isMultiple = FALSE
						}
						def startExecutionTime = new Date()
						try {							
							aborted = executionService.abortList.contains(exeId?.toString())
							devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
							if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString()))){
								try{	
									def combainedTcl  = [:]							
									if(scripts?.size() ==  validScripts?.size()){										
										if( scripts?.toString()?.contains(script?.scriptName?.toString())){										
											combainedTcl?.put("scriptName","")
										}else{										
											combainedTcl?.put("scriptName", scripts[index])
										}								
									}
									
									index = index + 1									
									htmlData = executeScript(execName, executionDevice, script, deviceInstance, url, filePath, realPath, isBenchMark, isSystemDiagnostics,executionName,isMultiple,null,isLogReqd, Category.RDKB_TCL.toString(), combainedTcl)		
								}catch(Exception e){
									e.printStackTrace()
								}
							}else {
								if(!aborted && devStatus.equals(Status.NOT_FOUND.toString())){
									pause = true
								}
								if(!aborted && pause) {
									def newScriptName
									try {
										if(scripts?.size() ==  validScripts?.size()){
											if( scripts?.toString()?.contains(script?.scriptName?.toString())){
												newScriptName = script?.scriptName?.toString()
											}else{
												newScriptName = scripts[index].toString()
											}
										}
										
										pendingScripts.add(newScriptName)
										def execInstance
										Execution.withTransaction {
											def execInstance1 = Execution.findByName(execName)
											execInstance = execInstance1
										}
										//Script scriptInstanceObj
										//scriptInstanceObj = scriptInstance
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
												executionResult.script = newScriptName
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
									index = index+1
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
				if((executionDeviceObj1) && ((rerun?.toString()?.equals(TRUE) || (rerun?.toString()?.equals("on"))))){
					htmlData = reRunOnFailure(realPath,filePath,execName,executionName,url, category)
					output.append(htmlData)
				}

			}else{
				executescriptService.resetAgent(deviceInstance)
			}
			executescriptService.deleteOutputFile(executionName)
			htmlData = output.toString()

		}
		catch(Exception ex){
		}
		finally{
			if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				executionService.deviceAllocatedList.remove(deviceInstance?.id)
			}

			String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
			Thread.start{
				println Thread.currentThread()
				deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
			}
		}

		return htmlData
	}


	def executeScriptInThread(String execName, String device, ExecutionDevice executionDevice, def scripts, def scriptGrp,
			def executionName, def filePath, def realPath, def groupType, def url, def isBenchMark, def isSystemDiagnostics, def rerun,def isLogReqd, def category){

		Future<String> future =  executorService.submit( {
			executescriptsOnDevice(execName, device, executionDevice, scripts, scriptGrp,
					executionName, filePath, realPath, groupType, url, isBenchMark, isSystemDiagnostics, rerun,isLogReqd, category)} as Callable< String > )

	}

	def String executeScript(final String executionName, final ExecutionDevice executionDevice, final def scriptInstance,
			final Device deviceInstance, final String url, final String filePath, final String realPath, final String isBenchMark,
			final String isSystemDiagnostics,final String uniqueExecutionName,final String isMultiple, def executionResult,def isLogReqd,
			final def category , final def combainedTcl) {
		Date startTime = new Date()
		String htmlData = ""
		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES
		def executionInstance = Execution.findByName(executionName)
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution
		def resultArray = Execution.executeQuery("select a.executionTime from Execution a where a.name = :exName",[exName: executionName])
		def totalTimeArray = Execution.executeQuery("select a.realExecutionTime from Execution a where a.name = :exName",[exName: executionName])
		def executionResultId
		if(executionResult == null){
			def newScriptName
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
		//setting default execution time as 20 minutes 
		int execTime = 20
		try {
			Module module = Module.findByName("tcl")
			int exTime = module?.executionTime
			if(exTime > 0){
				execTime = exTime
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

		/*try {
		 if(scriptInstance?.executionTime instanceof String){
		 execTime = Integer.parseInt(scriptInstance?.executionTime)
		 }else if(scriptInstance?.executionTime instanceof Integer){
		 execTime = scriptInstance?.executionTime?.intValue()
		 }else {
		 execTime = scriptInstance?.executionTime
		 }
		 } catch (Exception e) {
		 e.printStackTrace()
		 }*/
		def  scriptDir = grailsApplication.parentContext.getResource("fileStore"+FILE_SEPARATOR+FileStorePath.RDKTCL.value()).file?.absolutePath
		def tclFilePath = scriptDir+FILE_SEPARATOR+sFile.scriptName+".tcl"
		def configFilePath = scriptDir+FILE_SEPARATOR+"Config_" + deviceInstance?.stbName+".txt"
		String scriptData = readScriptContent(tclFilePath)
		scriptData = executionService.convertScriptFromHTMLToPython(scriptData)
		
		//Required only for TDK TCL execution 
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
		outData = executionService?.executeTclScript(file.getPath(), configFilePath, execTime, uniqueExecutionName , scriptInstance.scriptName, scriptDir,combainedTcl.scriptName )
		//outData = executionService?.executeTclScript(tclFilePath, configFilePath, execTime, uniqueExecutionName , scriptInstance.scriptName, scriptDir )
		file.delete()

		def logPath = "${realPath}/logs//${executionId}//${executionDevice?.id}//${executionResultId}//"
		executescriptService.copyLogsIntoDir(realPath,logPath, executionId,executionDevice?.id, executionResultId)

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
			executescriptService.resetAgent(deviceInstance,TRUE)
		}else if(Utility.isFail(htmlData) ){
			def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
			def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"
			//new File("${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
			executescriptService.logTransfer(deviceInstance,logTransferFilePath,logTransferFileName,realPath, executionId,executionDevice?.id, executionResultId,url)
			if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
				executescriptService.transferSTBLog("tcl", deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId,url)
			}
			executionService.updateExecutionResultsError(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
			Thread.sleep(4000)
			executescriptService.hardResetAgent(deviceInstance)
			if(deviceInstance?.isChild)
			{
				def parentDevice = Device.findByStbIp(deviceInstance?.gatewayIp)
				if(parentDevice != null && parentDevice?.childDevices?.contains(deviceInstance))
				{
					String stat = DeviceStatusUpdater?.fetchDeviceStatus(grailsApplication, parentDevice)
					if(  stat?.equals(Status.BUSY.toString()) || stat?.equals(Status.HANG.toString()) ){
						executescriptService.hardResetAgent(parentDevice)
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
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
			htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
			executionService.updateExecutionResultsTimeOut(htmlData,executionResultId,executionId,executionDevice?.id,timeDiff,singleScriptExecTime)
			Thread.sleep(10000)
		}
		else{
			String outputData = htmlData
			//	executionService.updateExecutionResults(outputData, executionResultId,  executionId, executionDevice?.id, timeDiff, singleScriptExecTime)
			executionService.updateTclExecutionResults( [execId: executionId,  resultData: 'SUCCESS',  execResult:executionResultId,
				expectedResult:null,  resultStatus :'SUCCESS', testCaseName : scriptInstance?.scriptName,  execDevice:executionDevice?.id, statusData:'SUCCESS',
				outputData:outputData, timeDiff:timeDiff, singleScriptExecTime:singleScriptExecTime ])

		}
		if(!executionService.abortList.contains(executionInstance?.id?.toString())){
			String performanceFilePath
			if(isBenchMark.equals(TRUE) || isSystemDiagnostics.equals(TRUE)){
				new File("${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}").mkdirs()
				performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDevice?.id}//${executionResultId}//"
			}

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
					performanceFilePath
				]
				ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
				htmlData += scriptExecutor.executeScript(cmd,1)
				executescriptService.copyPerformanceLogIntoDir(realPath, performanceFilePath, executionId,executionDevice?.id, executionResultId)
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
					performanceFilePath
				]
				ScriptExecutor scriptExecutor = new ScriptExecutor(uniqueExecutionName)
				htmlData += scriptExecutor.executeScript(cmd,10)
				executescriptService.copyPerformanceLogIntoDir(realPath, performanceFilePath, executionId,executionDevice?.id, executionResultId)
			}

			def logTransferFileName = "${executionId}_${executionDevice?.id}_${executionResultId}_AgentConsoleLog.txt"
			def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${executionDevice?.id}//${executionResultId}//"
			executescriptService.logTransfer(deviceInstance,logTransferFilePath,logTransferFileName ,realPath, executionId,executionDevice?.id, executionResultId,url)

			executescriptService.logTransfer(deviceInstance,logTransferFilePath,logTransferFileName,realPath,executionId,executionDevice?.id, executionResultId,url)
			if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
				executescriptService.transferSTBLog('tcl', deviceInstance,""+executionId,""+executionDevice?.id,""+executionResultId)
			}
		}
		Date endTime = new Date()
	try {
			def totalTimeTaken = (endTime?.getTime() - startTime?.getTime()) / 1000
	//		totalTimeTaken = totalTimeTaken?.round(2)
			executionService.updateExecutionTime(totalTimeTaken?.toString(), executionResultId)
		}
		 catch (Exception e) {
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
	
	def reRunOnFailure(final String realPath, final String filePath, final String execName, final String uniqueExecutionName, final String appUrl, final String category){
		try {			
			boolean pause = false
			List pendingScripts = []
			def aborted=false
			Execution executionInstance = Execution.findByName(execName)
			def exeId = executionInstance?.id
			def resultArray = Execution.executeQuery("select a.result from Execution a where a.name = :exName",[exName: execName])
			def result = resultArray[0]
			def newExecName
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
						if(cnt == 0){
							newExecName = execName + RERUN
							scriptName = executionInstance?.script
							def deviceName = deviceInstance?.stbName
							if(executionDeviceList.size() > 1){
								deviceName = MULTIPLE
							}
							//executionSaveStatus = executionService.saveExecutionDetails(newExecName, scriptName, deviceName, scriptGroupInstance,appUrl,"false","false","false","false",category])
							executionSaveStatus = executionService.saveExecutionDetails(newExecName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance,appUrl:appUrl, isBenchMark:"false", isSystemDiagnostics:"false", rerun:"false", isLogReqd:"false",category:category , rerunOnFailure:FALSE])
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
							def executionResultList
							try{
								ExecutionResult.withTransaction {
									executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
								}
							}
							catch(Exception e){
								println e.getMessage()
							}
							def scriptInstance = [:]
							def htmlData

							def resultSize = executionResultList.size()
							int counter = 0
							def isMultiple = TRUE

							// adding log transfer to server for reruns

							if(executionResultList.size() > 0){
								logTransferService.transferLog(newExecName, deviceInstance)
							}
							def executionName = Execution?.findByName(newExecName)
							executionResultList.each{ executionResult ->
								if(!executionResult.status.equals(SKIPPED)){
									//								scriptInstance = Script.findByName(executionResult?.script)
									def scriptFile = ScriptFile.findByScriptName(executionResult?.script)
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
									
									def scriptNameTcl
									boolean tclCombained =  false
									boolean combinedTCL = false
									def combainedTclScript =  scriptService?.combinedTclScriptMap
									combainedTclScript?.each{
										if(it?.value?.toString().contains(executionResult?.script?.toString())){
											combinedTCL = true
											scriptNameTcl = it.key?.toString()
										}
									}
									def combainedTclMap = [:]
									if(combinedTCL ){										
										scriptNameTcl= scriptNameTcl
										combainedTclMap.put("scriptName",executionResult?.script?.toString())
									}else{
										scriptNameTcl = executionResult?.script?.toString()
										combainedTclMap.put("scriptName","")
									}	
									Thread.sleep(6000)
									if(Utility.isTclScriptExists(realPath, scriptNameTcl)){
										scriptInstance.put('scriptName', scriptNameTcl)
										def startExecutionTime = new Date()
										//aborted = executionService.abortList.contains(exeId?.toString())
										aborted = executionService.abortList?.toString().contains(executionName?.id?.toString())
										if(!aborted && !(deviceStatus?.toString().equals(Status.NOT_FOUND.toString()) || deviceStatus?.toString().equals(Status.HANG.toString())) && !pause){
											htmlData = executeScript(newExecName, executionDevice, scriptInstance, deviceInstance, appUrl, filePath, realPath,"false","false",uniqueExecutionName,isMultiple,null,"false", category,combainedTclMap)
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
							try {

								if(executionResultList.size() > 0){
									logTransferService.closeLogTransfer(newExecName)
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
							if(aborted && !pause){
								executionService.saveExecutionStatus(aborted,executionInstance1?.id)
							}
							//Issue fix : For execution status not updated properly
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

	def executeScriptGroup(ScriptGroup scriptGroup, final String boxType,  final String execName, final String execDeviceId,
			Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl, final String imageName,
			final String isBenchMark, final String isSystemDiagnostics, final String rerun, final String isLogReqd, final String category){
		Future<String> future =  executorService.submit( { executeScriptGrp(scriptGroup, boxType, execName, execDeviceId, deviceInstance,
			url, filePath, realPath, callbackUrl, imageName, isBenchMark,isSystemDiagnostics,rerun,isLogReqd, category)} as Callable< String > )

	}

	def executeScriptGrp(ScriptGroup scriptGroup, final String boxType, final String execName, final String execDeviceId,
			Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl, final String imageName,
			final String isBenchMark, final String isSystemDiagnostics, final String rerun, final String isLogReqd, final String category){
		boolean aborted = false
		boolean pause = false
		try{
			List validScripts = new ArrayList()
			boolean skipStatus = false
			boolean notApplicable = false
			//String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
			scriptGroup.scriptList.each { scrpt ->
				//def script = scriptService.getScript(realPath, scrpt?.moduleName, scrpt?.scriptName, category.toString())
				def configFileExists = Utility.isConfigFileExists(realPath, deviceInstance?.stbName)
				if(configFileExists) {
					def script = Utility.isTclScriptExists(realPath, scrpt.scriptName)
					if(script){
						def scriptInstance = [:]
						scriptInstance.put('scriptName', scrpt.scriptName)
						scriptInstance.put('executionTime', TCL_TIMEOUT)
						validScripts << scriptInstance

						/*if(validateBoxTypeOfScripts(script,boxType)){
						 if(executionService.validateScriptRDKVersions(script, rdkVersion)){
						 if(script?.skip?.toString().equals("true")){
						 skipStatus = true
						 executionService.saveSkipStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), script, deviceInstance, category.toString())
						 }else{
						 validScripts << script
						 }
						 }else{
						 notApplicable =true
						 String rdkVersionData = ""
						 rdkVersionData = script?.rdkVersions
						 String reason = "RDK Version mismatch.<br>Device RDK Version : "+rdkVersion+", Script supported RDK Versions :"+rdkVersionData
						 executionService.saveNotApplicableStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), script, deviceInstance,reason, category.toString())
						 }
						 }else{
						 notApplicable = true
						 String boxTypeData = ""
						 String deviceBoxType = ""
						 Device.withTransaction {
						 Device dev = Device.findById(deviceInstance?.id)
						 deviceBoxType = dev?.boxType
						 }
						 boxTypeData = script?.boxTypes
						 String reason = "Box Type mismatch.<br>Device Box Type : "+deviceBoxType+", Script supported Box Types :"+boxTypeData
						 executionService.saveNotApplicableStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), script, deviceInstance,reason, category.toString())
						 }*/
					}else{
						String reason = "No script is available with name :"+scrpt?.scriptName
						executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), scrpt?.scriptName, deviceInstance,reason, category.toString())

					}
				}
				else{
					String reason = "No config file is available with name : Config_"+deviceInstance.stbName+".txt"
					executionService.saveNoScriptAvailableStatus(Execution.findByName(execName), ExecutionDevice.findById(execDeviceId), scrpt?.scriptName, deviceInstance,reason, category.toString())
				}
			}
			int scriptGrpSize = validScripts?.size()

			int scriptCounter = 0
			def isMultiple = "true"

			def executionStartTime = System.currentTimeMillis()

			try {
				saveThirdPartyExecutionDetails(Execution.findByName(execName),execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType, category)
			} catch (Exception e) {
				e.printStackTrace()
			}

			Execution ex = Execution.findByName(execName)
			ExecutionDevice execDevice = ExecutionDevice.findById(execDeviceId)
			if((skipStatus || notApplicable)&& scriptGrpSize == 0){
				if(ex){
					executionService.updateExecutionSkipStatusWithTransaction(FAILURE_STATUS, ex?.id)
					executionService.updateExecutionDeviceSkipStatusWithTransaction(FAILURE_STATUS, execDevice?.id)
				}
			}
			boolean executionStarted = false
			List pendingScripts = []
			int index = 0
			validScripts.each{ scriptInstance ->
				scriptCounter++
				if(scriptCounter == scriptGrpSize){
					isMultiple = "false"
				}
				aborted = ExecutionService.abortList.contains(ex?.id?.toString())
				String devStatus = ""
				if(!pause && !aborted){
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)

						if(devStatus.equals(Status.HANG.toString())){
							executionService.resetAgent(deviceInstance, TRUE)
							Thread.sleep(6000)
							devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						}

					}
					catch(Exception eX){
					}
				}

				if(!aborted && !(devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString()) || devStatus.equals(Status.TDK_DISABLED.toString())) && !pause){
					
					def startExecutionTime = new Date()
					try {
						executionStarted = true
						def combainedTcl = [:]
							//combainedTcl?.put("scriptName","")
							 if(scriptGroup?.scriptList?.size() ==  validScripts?.size()){
								 if( !(scriptService?.totalTclScriptList?.toString()?.contains(scriptInstance?.scriptName?.toString())) && scriptService?.tclScriptsList?.toString()?.contains(scriptInstance?.scriptName?.toString())){
									 combainedTcl?.put("scriptName", scriptGroup?.scriptList[index]?.toString())
								 }else{
								 	combainedTcl?.put("scriptName","")									
								 }
							 }
							 index = index + 1
						def htmlData = executeScripts(execName, execDeviceId, scriptInstance , deviceInstance , url, filePath, realPath, isMultiple, isBenchMark,isSystemDiagnostics,isLogReqd,rerun, category,combainedTcl)
						if(isMultiple.equals("false")){
							Execution.withTransaction {
								Execution executionInstance = Execution.findByName(execName)
								executionInstance.executionStatus = COMPLETED_STATUS
								executionInstance.save(flush:true)
							}
						}
					} catch (Exception e) {
						e.printStackTrace()
					}
					def endExecutionTime = new Date()
					executionTimeCalculation(execName,startExecutionTime,endExecutionTime )
				}else{
					if(!aborted && (devStatus.equals(Status.NOT_FOUND.toString()) || devStatus.equals(Status.HANG.toString()) || devStatus.equals(Status.TDK_DISABLED.toString()))){
						pause = true
					}

					if(!aborted && pause) {
						pendingScripts.add(scriptInstance?.name)

						def execInstance = Execution.findByName(execName,[lock: true])
						Device deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])
						def executionResult
						ExecutionResult.withTransaction { resultstatus ->
							try {
								executionResult = new ExecutionResult()
								executionResult.execution = execInstance
								executionResult.executionDevice = ExecutionDevice.findById(execDeviceId)
								executionResult.script = scriptInstance?.name
								executionResult.device = deviceInstance1?.stbName
								executionResult.execDevice = null
								executionResult.deviceIdString = deviceInstance1?.id?.toString()
								executionResult.status = "PENDING"
								executionResult.dateOfExecution = new Date()
								executionResult.category = category
								executionResult.save(flush:true)
								resultstatus.flush()
							}
							catch(Throwable th) {
								resultstatus.setRollbackOnly()
							}
						}

					}
				}
			}

			if(aborted){
				if(executionService.abortList.contains(ex?.id?.toString())){
					executionService.abortList.remove(ex?.id?.toString())
				}

				Execution.withTransaction {
					Execution executionInstance = Execution.findByName(execName)
					executionInstance.executionStatus = ABORTED_STATUS
					executionInstance.isAborted = true
					executionInstance.save(flush:true)
				}

				executionService.resetAgent(deviceInstance, FALSE)
			}

			if(pause && pendingScripts.size() > 0 ){
				def exeInstance = Execution.findByName(execName)
				executionService.savePausedExecutionStatus(exeInstance?.id)

				ExecutionDevice.withTransaction {
					ExecutionDevice exDevice = ExecutionDevice.findById(execDeviceId)
					exDevice.status = "PAUSED"
					exDevice.save();
				}
			}

			Execution executionInstance1 = Execution.findByName(execName)
			if(!pause){
				executionService.saveExecutionStatus(aborted, executionInstance1?.id)
			}

			if(callbackUrl){
				if(pause){
					saveThirdPartyExecutionDetails(Execution.findByName(execName),execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType, category)
				}else{
					//executeCallBackUrl(execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType,realPath)
				}
			}

			if(!aborted && !pause){
				if((executionInstance1) && (rerun)){
					executescriptService.reRunOnFailure(realPath,filePath,execName,execName,url)
				}
			}

		}
		catch(Exception e){
			e.printStackTrace()
		}
		finally{
			if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				executionService.deviceAllocatedList.remove(deviceInstance?.id)
				String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				Thread.start{
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
				}
			}
		}
	}

	def saveThirdPartyExecutionDetails(final def execution, final def execName, final def url, final def callbackUrl, final def filePath,
			final def executionStartTime, final def imageName, final def boxType, final def category){

		try{
			ThirdPartyExecutionDetails details = null

			ThirdPartyExecutionDetails.withTransaction {
				details = ThirdPartyExecutionDetails.findByExecNameAndExecutionStartTime(execName,executionStartTime)
			}
			if(details == null){
				ThirdPartyExecutionDetails.withTransaction {
					details = new ThirdPartyExecutionDetails()
					details.execution = execution
					details.execName = execName
					details.url = url
					details.callbackUrl = callbackUrl
					details.filePath = filePath
					details.executionStartTime = executionStartTime
					details.imageName = imageName
					details.boxType = boxType
					details.category = category
					details.save(flush:true)
				}
			}
			if(details){
				Execution.withTransaction{
					Execution ex =Execution.findById(execution?.id)
					ex.thirdPartyExecutionDetails = details
					ex.save(flush:true)
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
	}


	def String executeScripts(String executionName, String execDeviceId, def scriptInstance, Device deviceInstance, final String url, final String filePath,
			final String realPath, final String isMultiple, final String isBenchMark,final String  isSystemDiagnostics, final String isLogReqd, final String rerun,
			final String category ,final def combainedTcl) {


		String htmlData = ""
		Date startTime = new Date()
		def deviceInstance1 = Device.findById(deviceInstance.id,[lock: true])

		def executionInstance = Execution.findByName(executionName,[lock: true])
		def executionId = executionInstance?.id
		Date executionDate = executionInstance?.dateOfExecution

		def execStartTime = executionDate?.getTime()

		def executionDeviceInstance = ExecutionDevice.findById(execDeviceId)

		def executionResult
		ExecutionResult.withTransaction { resultstatus ->
			try {
				executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDeviceInstance
				executionResult.script = scriptInstance.scriptName
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

		int counter = 1
		def executionResultId = executionResult?.id

		def sFile
		try {
			sFile = ScriptFile.findByScriptNameAndModuleName(scriptInstance?.scriptName,'tcl')
		} catch (Exception e) {
			e.printStackTrace()
		}

		Date date = new Date()

		Date executionStartDt = new Date()
		def executionStartTime =  executionStartDt.getTime()

		//TODO  correct time used
		int execTime = 12

		def tclFile = Utility.getTclFilePath(realPath, scriptInstance?.scriptName)
		def configFile = Utility.getConfigFilePath(realPath, deviceInstance.stbName)
		String outData = null
		try{
			outData = executionService.executeTclScript(tclFile, configFile, execTime, executionName , scriptInstance.scriptName, Utility.getTclDir(realPath),combainedTcl.scriptName)
		}
		catch(Exception e){
			println e.message
		}
		def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDeviceInstance?.id.toString()}"
		String performanceFilePath
		if(isBenchMark.equals(TRUE) || isSystemDiagnostics.equals(TRUE)){
			new File("${realPath}//logs//performance//${executionId}//${executionDeviceInstance?.id}//${executionResultId}").mkdirs()
			performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDeviceInstance?.id}//${executionResultId}//"
		}

		if(isBenchMark.equals(TRUE)){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath

			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.logTransferPort,
				KEY_PERFORMANCE_BM,
				performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(executionName)
			outData += scriptExecutor.executeScript(cmd,1)
		}
		if(isSystemDiagnostics.equals(TRUE)){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				deviceInstance?.logTransferPort,
				KEY_PERFORMANCE_SD,
				performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(executionName)
			outData += scriptExecutor.executeScript(cmd,10)
		}
		if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
			executescriptService.transferSTBLog('tcl', deviceInstance,""+executionId,""+execDeviceId,""+executionResultId, realPath,url)
		}


		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${execDeviceId}//${executionResultId}//"
		new File("${realPath}/logs//consolelog//${executionId}//${execDeviceId}//${executionResultId}").mkdirs()
		executescriptService.logTransfer(deviceInstance,logTransferFilePath, logTransferFileName,realPath, executionId,execDeviceId, executionResultId,url)


		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}

		String outputData = htmlData

		Date execEndDate = new Date()
		def execEndTime =  execEndDate.getTime()

		def timeDifference = ( execEndTime - executionStartTime  ) / 1000;

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
		
	


		/* if(outputData) {
		 executionService.updateExecutionResults(outputData,executionResultId,executionId, executionDeviceInstance?.id, timeDiff)
		 /* Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
		 [newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])*/
		// }
		if(executionService.abortList.contains(executionInstance?.id?.toString())){
			executionService.resetAgent(deviceInstance,TRUE)
		}	else if(Utility.isFail(htmlData)){
			executescriptService.logTransfer(deviceInstance,logTransferFilePath,logTransferFileName,realPath, executionId,execDeviceId, executionResultId,url)
			if(isLogReqd){
				executescriptService.transferSTBLog('tcl', deviceInstance,""+executionId,""+execDeviceId,""+executionResultId, realPath,url)
			}
			executionService.updateExecutionResultsError(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),singleScriptExecTime)
			Thread.sleep(5000)
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				"true"
			]
			def resetExecutionData
			try {
				ScriptExecutor scriptExecutor = new ScriptExecutor()
				resetExecutionData = scriptExecutor.executeScript(cmd,1)
				executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
			} catch (Exception e) {
				e.printStackTrace()
			}
			Thread.sleep(6000)
		}
		else if((timeDifference >= scriptInstance.executionTime) && (scriptInstance.executionTime != 0))	{
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
			htmlData = htmlData +"\nScript timeout\n"+ resetExecutionData
			executionService.updateExecutionResultsTimeOut(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),singleScriptExecTime)
			Thread.sleep(6000)
			executionService.callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)

		}
		else{
			String outputData1 = htmlData
			executionService.updateExecutionResults(outputData1,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),singleScriptExecTime)
			executionService.updateTclExecutionResults( [execId: executionInstance?.id,  resultData: 'SUCCESS',  execResult:executionResult?.id,
				expectedResult:null,  resultStatus :'SUCCESS', testCaseName : scriptInstance?.scriptName,  execDevice:executionDeviceInstance?.id, statusData:'SUCCESS',
				outputData:outputData, timeDiff:timeDiff, singleScriptExecTime:singleScriptExecTime ])
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


}
