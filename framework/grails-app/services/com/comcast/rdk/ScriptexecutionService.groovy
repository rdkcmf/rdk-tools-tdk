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

import com.google.gson.JsonArray
import com.google.gson.JsonObject
import com.google.gson.JsonPrimitive

import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.concurrent.FutureTask
import java.util.regex.Matcher
import java.util.regex.Pattern
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.Executors;
/**
 * Service class for the Asynchronous Execution of Scripts for REST.
 * @author sreejasuma
 */

class ScriptexecutionService {
	
	static datasource = 'DEFAULT'
	
    /**
	 * Injecting executor service.
	 */
	static ExecutorService executorService = Executors.newCachedThreadPool()
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication
	
	def executionService
	
	def scriptService
	
	def deviceStatusService
	
	def executescriptService
	
	/**
	 * Method to save details of execution in Execution Domain
	 * @param execName
	 * @param scriptName
	 * @param deviceName
	 * @param scriptGroupInstance
	 * @return
	 */
	public boolean saveExecutionDetails(final String execName, String scriptName, String deviceName,
			ScriptGroup scriptGroupInstance, String appUrl, final Category category){

		def executionSaveStatus = true
		try{
			int scriptCnt = 0
			if(scriptGroupInstance?.scriptList?.size() > 0){
				scriptCnt = scriptGroupInstance?.scriptList?.size()
			}
			
			Execution execution = new Execution()
			execution.name = execName
			execution.script = scriptName
			execution.device = deviceName
			execution.scriptGroup = scriptGroupInstance?.name
			execution.result = UNDEFINED_STATUS
			execution.executionStatus = INPROGRESS_STATUS
			execution.dateOfExecution = new Date()
			execution.applicationUrl = appUrl
			execution.scriptCount = scriptCnt
			execution.category = category
			if(! execution.save(flush:true)) {
				log.error "Error saving Execution instance : ${execution.errors}"
				executionSaveStatus = false
			}
		}
		catch(Exception th) {
			//th.printStackTrace()
			executionSaveStatus = false
		}
		return executionSaveStatus
	}
	

	def executeScriptGroup(ScriptGroup scriptGroup, final String boxType,  final String execName, final String execDeviceId,
		Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl, final String imageName,
		final String isBenchMark, final String isSystemDiagnostics, final String rerun, final String isLogReqd, final String category){ // issue fix -category type changed in to string
		
		Future<String> future =  executorService.submit( { executeScriptGrp(scriptGroup, boxType, execName, execDeviceId, deviceInstance,
			url, filePath, realPath, callbackUrl, imageName, isBenchMark,isSystemDiagnostics,rerun,isLogReqd, category)} as Callable< String > )
	}
		
	def String getCurlCommand(final String jsonString, final String callbackUrl){
		
		String curlCommand
		try{
			File jenkFile = grailsApplication.parentContext.getResource("//fileStore//jenkinscredential.txt").file
			String valueString
			String jenkUser=""
			String jenkPwd=""
			if(jenkFile.exists()){
			jenkFile.eachLine {
				if (it.startsWith('JENK_USER:')) {
					valueString = it
					valueString = valueString.replaceAll("JENK_USER:", "")
					jenkUser = valueString.trim()
				}
				else if(it.startsWith('JENK_PWD:')){
					valueString = it
					valueString = valueString.replaceAll("JENK_PWD:", "")
					jenkPwd = valueString.trim()
				}
			}
		}
			/*String jsonString = jsonData.toString();
			jsonString = jsonString.replaceAll("\"", "\\\\\"")*/
			
			if(jenkUser && jenkPwd && callbackUrl){
				curlCommand = "curl --fail -X POST --insecure --user ${jenkUser}:${jenkPwd} ${callbackUrl} -F json=\"{\\\"parameter\\\":[{\\\"name\\\":\\\"TDK_DATA\\\",\\\"value\\\":\\\"${jsonString}\\\"}]}\" --verbose"
				//curlCommand = "curl --fail -X POST --insecure --user ${jenkUser}:${jenkPwd} ${callbackUrl} -F json=\"${jsonString}\" --verbose"
			}
		}
		catch(Exception ex){
			ex.printStackTrace()
		}
		return curlCommand
	}
	
	def String getCustomCurlCommand(final String jsonString, final String callbackUrl,final String jfileName){
		
		String curlCommand
		try{
			File jenkFile = grailsApplication.parentContext.getResource("//fileStore//jenkinscredential.txt").file
			String valueString
			try {
				File tempFile = new File(jfileName)
			if(!tempFile.exists()){
				tempFile.createNewFile()
			}
			
			def mjsonString = jsonString
			tempFile.write("${mjsonString}")
			} catch (Exception e) {
				e.printStackTrace()
			}
			
			if(callbackUrl){
				curlCommand = "curl --fail -X POST --insecure ${callbackUrl} -H 'Content-Type: application/json' -d '@${jfileName}' --verbose"
			}
		}
		catch(Exception ex){
			ex.printStackTrace()
		}
		return curlCommand
	}
		
	def executeScriptGrp(ScriptGroup scriptGroup, final String boxType, final String execName, final String execDeviceId,
		Device deviceInstance, final String url, final String filePath, final String realPath, final String callbackUrl, final String imageName,
		final String isBenchMark, final String isSystemDiagnostics, final String rerun, final String isLogReqd, final String category){ 
		// Issue fix - category type changed as String 
		boolean aborted = false
		boolean pause = false
		try{		
			List validScripts = new ArrayList()
			boolean skipStatus = false
			boolean notApplicable = false
			String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
			scriptGroup.scriptList.each { scrpt ->
				def script = scriptService.getScript(realPath, scrpt?.moduleName, scrpt?.scriptName, category.toString())
				if(script){
				if(validateBoxTypeOfScripts(script,boxType)){
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
				}
				}else{
					String reason = "No script is available with name :"+scrpt?.scriptName+" in module :"+scrpt?.moduleName
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
						/*Thread.start{
							deviceStatusService.updateDeviceStatus(deviceInstance, devStatus)
						}*/
						
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
								def htmlData = executeScripts(execName, execDeviceId, scriptInstance , deviceInstance , url, filePath, realPath, isMultiple, isBenchMark,isSystemDiagnostics,isLogReqd,rerun, category)
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
								if(! executionResult.save(flush:true)) {
	//								log.error "Error saving executionResult instance : ${executionResult.errors}"
								}
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
					executeCallBackUrl(execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType,realPath)
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
			
		def executeCallBackUrl(final def execName, final def url, final def callbackUrl, final def filePath, 
			final def executionStartTime, final def imageName, final def boxType,final def realPath){
		def jfileName
		String curlCommand

		try{
			if(callbackUrl?.contains("jenkins")){
				def newDataString = thirdPartyJsonResult(execName,url,executionStartTime,imageName,boxType,realPath)
				newDataString  = newDataString.replaceAll("\"", "\\\\\\\\\\\\\"")
				curlCommand = getCurlCommand( newDataString , callbackUrl)
			}else{
				jfileName = filePath+"/callBack"+System.currentTimeMillis()+".json"
				curlCommand = getCustomCurlCommand(thirdPartyJsonResult(execName,url,executionStartTime,imageName,boxType,realPath), callbackUrl,jfileName)
			}

			File newFile = new File(filePath, execName+"-curlscript.sh");
			boolean isFileCreated = newFile.createNewFile()
			if(isFileCreated) {
				newFile.setExecutable(true, false )
			}
			if(curlCommand){
				PrintWriter fileNewPrintWriter = newFile.newPrintWriter();
				fileNewPrintWriter.print( curlCommand )
				fileNewPrintWriter.flush()
				fileNewPrintWriter.close()
				def absolutePath = newFile.absolutePath

				if(absolutePath != null){

					String[] cmd = [
						"sh",
						absolutePath
					]
					def outputData
					try {
						ScriptExecutor scriptExecutor = new ScriptExecutor()
						outputData = scriptExecutor.executeScript(cmd)
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
			}
			if(newFile.exists()){
				newFile.delete();
			}
		}finally{
			if(jfileName){
				File jFile = new File(jfileName);
				if(jFile.exists()){
					jFile.delete();
				}
			}
		}
	}
		
		
		def String thirdPartyJsonResult(final String execName, final String appurl, final def executionStartTime,
			final String imageName, final String boxType ,final def realPath){
			JsonArray jsonArray = new JsonArray()
			JsonObject compNode
			JsonObject deviceNode
			JsonObject executionNode
			String appUrl = appurl
			String url
			appUrl = appUrl + "/execution/getDetailedTestResult?execResId="
			Execution executionInstance = Execution.findByName(execName)
			if(executionInstance){
				ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
				def executionResultStatus //= ExecutionResult.findAllByExecutionAndStatusIsNotNull(executionInstance)
				def scriptStatus = null
				def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
				def executionResult //= ExecutionResult.findAllByExecution(executionInstance)
				executionDevice.each{ execDevice ->
					url = ""
					compNode = new JsonObject()
					deviceNode = new JsonObject()
					executionResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
						List<ExecutionResult> execResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
						def componentMap = [:].withDefault {[]}
						def systemMap = [:].withDefault {[]}
						execResult.each{ execResObj ->
							def moduleNameMap = scriptService.getScriptNameModuleNameMapping(realPath)
							def moduleName = moduleNameMap.get(execResObj?.script)
//							def script = scriptService.getScript(realPath, moduleName, execResObj?.script) // TODO realpath
//								Script script = Script.findByName(execResObj?.script)
							Module module = Module.findByName(moduleName)
							if(module){
								if(module?.testGroup?.groupValue?.toString()?.equals("E2E") ){
									List val1 = systemMap.get(moduleName);
									if(!val1){
										val1 = []
										systemMap.put(module.toString(), val1)
									}
									val1.add(execResObj?.id)
								}
								else{
									List val = componentMap.get(module.toString());
									if(!val){
										val = []
										componentMap.put(module.toString(), val)
									}
									val.add(execResObj?.id)
								}
							}
						}
						def statusVal
						def newmap = [:]
						JsonArray compArray = new JsonArray();
						
						componentMap.each{ k, v ->
							JsonObject compObject = new JsonObject();
							
							compObject.addProperty("ModuleName", k.toString())
							def lst = v
							statusVal = SUCCESS_STATUS
							
							JsonArray scriptStatusArray = new JsonArray();
							JsonObject scriptStatusNode
							lst.each{
								url = ""
								scriptStatusNode = new JsonObject()
								ExecutionResult exResult = ExecutionResult.findById(it)
								if(!exResult.status.equals(SUCCESS_STATUS)){
									statusVal = FAILURE_STATUS
								}
								scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
								scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

								/*JsonArray failedFunArray = new JsonArray()
								List fun = []
								JsonPrimitive el = new JsonPrimitive("fun1");
								JsonPrimitive el2 = new JsonPrimitive("fun2");
								failedFunArray.add(el)
								failedFunArray.add(el2)
								scriptStatusNode.add("FailedFunctions", failedFunArray)*/
								url = appUrl + exResult?.id.toString()
								scriptStatusNode.addProperty("LogUrl", url.toString())
								
								scriptStatusArray.add(scriptStatusNode)
								
							}
							newmap[k] = statusVal
							compObject.addProperty("ModuleStatus", statusVal.toString())
							compObject.add("ScriptDetails", scriptStatusArray)
							compArray.add(compObject)
						}
						JsonArray systemArray = new JsonArray();
						systemMap.each{ k, v ->
							JsonObject sysObject = new JsonObject();
							
							sysObject.addProperty("ModuleName", k.toString())
							def lst = v
							statusVal = SUCCESS_STATUS
							
							JsonArray scriptStatusArray = new JsonArray();
							JsonObject scriptStatusNode
							lst.each{
								url = ""
								scriptStatusNode = new JsonObject()
								ExecutionResult exResult = ExecutionResult.findById(it)
								if(!exResult.status.equals(SUCCESS_STATUS)){
									statusVal = FAILURE_STATUS
								}
								scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
								scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							/*	JsonArray failedFunArray = new JsonArray()
								List fun = []
								JsonPrimitive el = new JsonPrimitive("fun1");
								JsonPrimitive el2 = new JsonPrimitive("fun2");
								failedFunArray.add(el)
								failedFunArray.add(el2)
								scriptStatusNode.add("FailedFunctions", failedFunArray)*/
								url = appUrl + exResult?.id.toString()
								scriptStatusNode.addProperty("LogUrl", url.toString())
								
								scriptStatusArray.add(scriptStatusNode)
								
							}
							
							newmap[k] = statusVal
							sysObject.addProperty("ModuleStatus", statusVal.toString())
							sysObject.add("ScriptDetails", scriptStatusArray)
							systemArray.add(sysObject)
						}
						
						def imgName = ""
						if(imageName){
							imgName = imageName
						}

						deviceNode.addProperty("Device",execDevice?.device?.toString())
						def bbType = boxType?.toString()
						if(boxType?.toString()?.equals("Broadband") || boxType?.toString()?.contains("RPI")){
							bbType = "Hybrid-1"
						}
						deviceNode.addProperty("BoxType",bbType)
						deviceNode.addProperty("ImageName",imgName?.toString())
						deviceNode.add("ComponentLevelDetails",compArray)
						deviceNode.add("SystemLevelDetails",systemArray)
						
						jsonArray.add(deviceNode)
					}
					executionNode = new JsonObject()
					executionNode.addProperty("ExecutionName",execName)
					executionNode.add("DEVICES", jsonArray)
				}
			
			JsonObject paramObject = new JsonObject();
			
			JsonArray paramArray = new JsonArray();
			JsonArray dataArray = new JsonArray();
			dataArray.add(executionNode)
			
			String dataString = dataArray.toString();


			//dataString  = dataString.replaceAll("\"", "")
		
			//    	dataString  = dataString.replaceAll("\"", "\\\\\\\\\\\\\"")
		//	return dataString
			
			/*JsonObject tdkObject = new JsonObject();
			tdkObject.addProperty("name", "TDK_DATA")
			tdkObject.addProperty("value", dataString)
			
			paramArray.add(tdkObject);
			
			paramObject.add("parameter", paramArray);
						
			return paramObject*/
			
			def execTime = executionInstance?.executionTime
			
			Double execTme
			
			try {

				execTme = Double.parseDouble(execTime)
				execTme = execTme * 60000

			} catch (Exception e) {
			}
			

			JsonObject tdkObject = new JsonObject();
			tdkObject.addProperty("service", "TDK" )
			tdkObject.addProperty("status", executionInstance?.result?.toString() )
			tdkObject.addProperty("started_at", executionStartTime.toString() )
			tdkObject.addProperty("started_by", "RDKPortal/Jenkins" )
			tdkObject.addProperty("duration", execTme.toString())
			tdkObject.add("result", dataArray )
			String newDataString = tdkObject.toString()
			return newDataString
		}
	
	/**
	 * Method to execute the script
	 * @param scriptGroupInstance
	 * @param scriptInstance
	 * @param deviceInstance
	 * @param url
	 * @return
	 */
	def String executeScripts(String executionName, String execDeviceId, def scriptInstance,
			Device deviceInstance, final String url, final String filePath, final String realPath, final String isMultiple, final String isBenchMark,final String  isSystemDiagnostics, final String isLogReqd, final String rerun, final String category ) {
	
		String htmlData = ""
		Date startTime = new Date()
		String scriptData = convertScriptFromHTMLToPython(scriptInstance.scriptContent)
		 
		String stbIp = STRING_QUOTES + deviceInstance.stbIp + STRING_QUOTES

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
				executionResult.script = scriptInstance.name
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
		
		String gatewayIp = deviceInstance1?.gatewayIp
		
		
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

		
		def executionResultId = executionResult?.id
		
		def sFile 
		try {
			sFile = ScriptFile.findByScriptNameAndModuleName(scriptInstance?.name,scriptInstance?.primitiveTest?.module?.name)
		} catch (Exception e) {
			e.printStackTrace()
		}

		/*scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath +SINGLE_QUOTES + COMMA_SEPERATOR +
			executionId  + COMMA_SEPERATOR + execDeviceId + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.logTransferPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
			sFile?.id + COMMA_SEPERATOR + deviceInstance?.id + COMMA_SEPERATOR+ SINGLE_QUOTES + isBenchMark + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + isSystemDiagnostics + SINGLE_QUOTES + COMMA_SEPERATOR +
			SINGLE_QUOTES + isMultiple + SINGLE_QUOTES + COMMA_SEPERATOR )//+ gatewayIp + COMMA_SEPERATOR)*/
		String logFilePath = realPath?.toString()+"/logs/logs/"
		scriptData = scriptData.replace( REPLACE_TOKEN, METHOD_TOKEN + LEFT_PARANTHESIS + SINGLE_QUOTES + url + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES + realPath + SINGLE_QUOTES + COMMA_SEPERATOR + SINGLE_QUOTES +logFilePath+SINGLE_QUOTES + COMMA_SEPERATOR +
			executionId  + COMMA_SEPERATOR +  execDeviceId + COMMA_SEPERATOR + executionResultId  + REPLACE_BY_TOKEN + deviceInstance?.agentMonitorPort + COMMA_SEPERATOR + deviceInstance?.statusPort + COMMA_SEPERATOR +
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
		
		Date executionStartDt = new Date()
		def executionStartTime =  executionStartDt.getTime()
		
//TODO  correct time used 
		int execTime = 0
		try {
			if(scriptInstance?.executionTime instanceof String){
				execTime = Integer.parseInt(scriptInstance?.executionTime)
			}else {
				execTime = scriptInstance?.executionTime
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		
		String outData = executeScript( file.getPath(), execTime , executionName )
		
		//def logTransferFileName = "${executionId.toString()}${deviceInstance?.id.toString()}${scriptInstance?.id.toString()}${executionDeviceInstance?.id.toString()}"
		def logTransferFileName = "${executionId}_${execDeviceId}_${executionResultId}_AgentConsoleLog.txt"
		String performanceFileName
		String performanceFilePath
		String diagnosticsFilePath
		if(isBenchMark.equals(TRUE) || isSystemDiagnostics.equals(TRUE)){
			//new File("${realPath}//logs//performance//${executionId}//${executionDeviceInstance?.id}//${executionResultId}").mkdirs()
			//performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDeviceInstance?.id}//${executionResultId}//"
			performanceFileName = "${executionId}_${executionDeviceInstance?.id}_${executionResultId}"
			performanceFilePath = "${realPath}//logs//performance//${executionId}//${executionDeviceInstance?.id}//${executionResultId}//"
			diagnosticsFilePath = "${realPath}//logs//stblogs//${executionId}//${executionDeviceInstance?.id}//${executionResultId}//"
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
				//deviceInstance?.logTransferPort,
				deviceInstance?.agentMonitorPort,
				KEY_PERFORMANCE_BM,
				performanceFileName
				//performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(executionName)
			outData += scriptExecutor.executeScript(cmd,1)
			executescriptService.copyPerformanceLogIntoDir(realPath, performanceFilePath,executionId,executionDeviceInstance?.id,executionResultId )
		}
		if(isSystemDiagnostics.equals(TRUE)){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callPerformanceTest.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort,
				//deviceInstance?.logTransferPort,
				deviceInstance?.agentMonitorPort,
				KEY_PERFORMANCE_SD,
				performanceFileName
				//performanceFilePath
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor(executionName)
			outData += scriptExecutor.executeScript(cmd,10)
			executescriptService.copyPerformanceLogIntoDir(realPath, performanceFilePath ,executionId,executionDeviceInstance?.id,executionResultId)
			
			executescriptService.initiateDiagnosticsTest(deviceInstance, performanceFileName, tmUrl,executionName)
			executescriptService.copyLogFileIntoDir(realPath, diagnosticsFilePath, executionId,executionDeviceInstance?.id, executionResultId,DEVICE_DIAGNOSTICS_LOG)
		}
		if(isLogReqd && isLogReqd?.toString().equalsIgnoreCase(TRUE)){
			executescriptService.transferSTBLog(scriptInstance?.primitiveTest?.module?.name, deviceInstance,""+executionId,""+execDeviceId,""+executionResultId,realPath,url)
		}
		
			
		//def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${execDeviceId}//${executionResultId}//"
		//new File("${realPath}/logs//consolelog//${executionId}//${execDeviceId}//${executionResultId}").mkdirs()
		def logTransferFileName1 = "${executionId}_${execDeviceId}_${executionResultId}_AgentConsoleLog.txt"
		def logTransferFilePath = "${realPath}/logs//consolelog//${executionId}//${execDeviceId}//${executionResultId}//"
		executescriptService.logTransfer(deviceInstance,logTransferFilePath,logTransferFileName1, realPath,executionId,execDeviceId,executionResultId,url)

		
		outData?.eachLine { line ->
			htmlData += (line + HTML_BR )
		}
		
		file.delete()			
		//TFTP  New Changes 
		def logPath = "${realPath}/logs//${executionId}//${execDeviceId}//${executionResultId}//"
		executescriptService.copyLogsIntoDir(realPath,logPath, executionId,execDeviceId,executionResultId)
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
		}	else if(htmlData.contains(TDK_ERROR)){
			htmlData = htmlData.replaceAll(TDK_ERROR,"")
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
			}
			executescriptService.logTransfer(deviceInstance,logTransferFilePath,logTransferFileName,realPath, executionId,execDeviceId, executionResultId,url)
			if(isLogReqd){
				executescriptService.transferSTBLog(scriptInstance?.primitiveTest?.module?.name, deviceInstance,""+executionId,""+execDeviceId,""+executionResultId, realPath,url)
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
		else{
			if(htmlData.contains("SCRIPTEND#!@~")){
				htmlData = htmlData.replaceAll("SCRIPTEND#!@~","")
				String outputData1 = htmlData
				executionService.updateExecutionResults(outputData1,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),singleScriptExecTime)
			}
			else{
				if((timeDifference >= scriptInstance.executionTime) && (scriptInstance.executionTime != 0))	{
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
				}else{
					try {
						executionService.updateExecutionResultsError(htmlData,executionResult?.id,executionInstance?.id,executionDeviceInstance?.id,timeDiff.toString(),singleScriptExecTime)
						Thread.sleep(5000)
						File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
						def absolutePath = layoutFolder.absolutePath
						String[] cmd = [
							PYTHON_COMMAND,
							absolutePath,
							deviceInstance?.stbIp,
							deviceInstance?.agentMonitorPort,
							"false"
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
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
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
	 * Method to call the script executor to execute the script
	 * @param executionData
	 * @return
	 */
	public String executeScript(final String executionData, final int executeTime,final String executionName) {
//		new ScriptExecutor().execute( getCommand( executionData ),executeTime)
		new ScriptExecutor().execute( getCommand( executionData ), executeTime,executionName,executionService?.executionProcessMap)
	}
	
	/**
	 * Method to validate script
	 * @param executionData
	 * @return
	 */
	public String validateScript(final String executionData) {
		new ScriptExecutor().validateScript( getCommand( executionData ))
	}
	
	/**
	 * Method to get the python script execution command.
	 * @param command
	 * @return
	 */
	public String getCommand(final String command) {
		String actualCommand = grailsApplication.config.python.execution.path +" "+ command
		return actualCommand
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

	/**
	 * Validates whether the boxtype of device is same as that
	 * of the boxtype specified in the script
	 * @param scriptInstance
	 * @param deviceInstance
	 * @return
	 */
//	public boolean validateScriptBoxType(final Script scriptInstance, final Device deviceInstance){
//		boolean scriptStatus = true
//		if(!(scriptInstance.boxTypes.find { it.id == deviceInstance.boxType.id })){
//			scriptStatus = false
//		}
//		return scriptStatus
//	}
	
	/**
	 * Validates whether the boxtype of device is same as that
	 * of the boxtype specified in the script
	 * @param scriptInstance
	 * @param deviceInstance
	 * @return
	 */
//	public boolean validateBoxTypeOfScript(Script scriptInstance, String boxType){
//		boolean scriptStatus = true
//		def sId = scriptInstance?.id
//		Script.withTransaction {
//			def scriptInstance1 = Script.findById(sId)
//			if(!(scriptInstance1.boxTypes.find { (it.name).equalsIgnoreCase( boxType ) })){
//				scriptStatus = false
//			}
//		}
//		return scriptStatus
//	}
	
	public boolean validateBoxTypeOfScripts(final Map script, String boxType){
		boolean scriptStatus = true
			if(!(script?.boxTypes?.find { (it.name).equalsIgnoreCase( boxType ) })){
				scriptStatus = false
			}
		return scriptStatus
	}
	
	
	/**
	 * Method to execute the versiontransfer.py script stored in filestore folder of webapps
	 *
	 * @param filePath
	 * @param executionName
	 * @param stbIp
	 * @return
	 */
	def executeVersionTransferScript(final String realPath, final String filePath, final String executionName, final String stbIp, final String logTransferPort){
		
		def executionInstance = Execution.findByName(executionName)
		String fileContents = new File(filePath+DOUBLE_FWD_SLASH+VERSIONTRANSFER_FILE).text
		
		fileContents = fileContents.replace(IP_ADDRESS, STRING_QUOTES+stbIp+STRING_QUOTES)
		
		fileContents = fileContents.replace(PORT, logTransferPort)
		
		String versionFilePath = "${realPath}//logs//version//${executionInstance?.id}_version.txt"
		fileContents = fileContents.replace(LOCALFILE, STRING_QUOTES+versionFilePath+STRING_QUOTES)
		
		String versionFile = TEMP_VERSIONFILE_NAME
					   
		File versnFile = new File(filePath, versionFile)
		boolean isVersionFileCreated = versnFile.createNewFile()
		if(isVersionFileCreated) {
			versnFile.setExecutable(true, false )
		}
		PrintWriter versnNewPrintWriter = versnFile.newPrintWriter();
		versnNewPrintWriter.print( fileContents )
		versnNewPrintWriter.flush()
				
		executeScript( versnFile.getPath() )
		versnFile.delete()
	}
	
	def String generateResultBasedOnTestRequest(final String caseId, final String callbackUrl, final String filePath, final String url, final String imageName, final String boxType,final def realPath){
		Execution execution
		def status = ""
		def execName
		if(caseId.startsWith("CI_")){
			execution = Execution.findByName(caseId.trim())
		}
		else{
			execution = Execution.find("from Execution as b where b.result=? and b.name like 'CI%' order by b.id desc",['FAILURE'])			
		}
		if(execution){
			execName = execution?.name
			def executionStartTime = System.currentTimeMillis()
			executeCallBackUrl(execName,url,callbackUrl,filePath,executionStartTime,imageName,boxType,realPath)
			status = "Done"
		}
		return status		
	}
		

	def thirdPartyJsonResultFromController(final String execName, final String appurl,def realPath ){
		JsonArray jsonArray = new JsonArray()
		JsonObject compNode
		JsonObject deviceNode
		JsonObject executionNode
		String appUrl = appurl
		String url
		appUrl = appurl + "/execution/getDetailedTestResult?execResId="
		Execution executionInstance = Execution.findByName(execName)
		if(executionInstance){
			ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
			def executionResultStatus //= ExecutionResult.findAllByExecutionAndStatusIsNotNull(executionInstance)
			def scriptStatus = null
			def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
			def executionResult //= ExecutionResult.findAllByExecution(executionInstance)

			executionDevice.each{ execDevice ->
				url = ""
				compNode = new JsonObject()
				deviceNode = new JsonObject()
				executionResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
		
					List<ExecutionResult> execResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
					def componentMap = [:].withDefault {[]}
					def systemMap = [:].withDefault {[]}
					execResult.each{ execResObj ->
//						Script.withTransaction { scriptRes ->
						def scriptMap = scriptService.getScriptNameModuleNameMapping(realPath)
						def moduleName =scriptMap.get(execResObj?.script)
						Module module= Module.findByName(moduleName)
						def script = scriptService.getScript(realPath,moduleName, execResObj?.script,module?.category?.toString())
							if(module?.testGroup?.groupValue?.toString()?.equals("E2E") ){
								List val1 = systemMap.get(module.toString());
								if(!val1){
									val1 = []
									systemMap.put(module.toString(), val1)
								}
								val1.add(execResObj?.id)
							}
							else{
								List val = componentMap.get(module.toString());
								if(!val){
									val = []
									componentMap.put(module.toString(), val)
								}
								val.add(execResObj?.id)
							}
//						}
					}
					def statusVal
					def newmap = [:]
					JsonArray compArray = new JsonArray();
					
					componentMap.each{ k, v ->
						JsonObject compObject = new JsonObject();
						
						compObject.addProperty("ModuleName", k.toString())
						def lst = v
						statusVal = SUCCESS_STATUS
						
						JsonArray scriptStatusArray = new JsonArray();
						JsonObject scriptStatusNode
						lst.each{
							url = ""
							scriptStatusNode = new JsonObject()
							ExecutionResult exResult = ExecutionResult.findById(it)
							if(!exResult.status.equals(SUCCESS_STATUS)){
								statusVal = FAILURE_STATUS
							}
							scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
							scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							url = appUrl + exResult?.id.toString()
							scriptStatusNode.addProperty("LogUrl", url.toString())
							
							scriptStatusArray.add(scriptStatusNode)
							
						}
						
						newmap[k] = statusVal
						compObject.addProperty("ModuleStatus", statusVal.toString())
						compObject.add("ScriptDetails", scriptStatusArray)
						compArray.add(compObject)
					}
					
					JsonArray systemArray = new JsonArray();
					systemMap.each{ k, v ->
						JsonObject sysObject = new JsonObject();
						
						sysObject.addProperty("ModuleName", k.toString())
						def lst = v
						statusVal = SUCCESS_STATUS
						
						JsonArray scriptStatusArray = new JsonArray();
						JsonObject scriptStatusNode
						lst.each{
							url = ""
							scriptStatusNode = new JsonObject()
							ExecutionResult exResult = ExecutionResult.findById(it)
							if(!exResult.status.equals(SUCCESS_STATUS)){
								statusVal = FAILURE_STATUS
							}
							scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
							scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							url = appUrl + exResult?.id.toString()
							scriptStatusNode.addProperty("LogUrl", url.toString())
							
							scriptStatusArray.add(scriptStatusNode)
							
						}
						
						newmap[k] = statusVal
						sysObject.addProperty("ModuleStatus", statusVal.toString())
						sysObject.add("ScriptDetails", scriptStatusArray)
						systemArray.add(sysObject)
					}

					deviceNode.addProperty("Device",execDevice?.device.toString())
					deviceNode.add("ComponentLevelDetails",compArray)
					deviceNode.add("SystemLevelDetails",systemArray)
					jsonArray.add(deviceNode)
				}
				executionNode = new JsonObject()
				executionNode.addProperty("ExecutionName",execName)
				
				String execStatus
				if(executionInstance?.executionStatus){
					execStatus = executionInstance?.executionStatus
				}
				else{
					execStatus = "IN-PROGRESS"
				}				
				//New changes ------
				if(executionInstance?.scriptGroup){
					executionNode.addProperty("ScriptGroup",executionInstance?.scriptGroup)
				}else if(executionInstance?.script?.toString()?.equals(MULTIPLESCRIPT)){
					executionNode.addProperty("ScriptName",MULTIPLESCRIPT)
				}else{
					executionNode.addProperty("ScriptName",executionInstance?.script)
				}		
								
				executionNode.addProperty("ExecutionStatus",execStatus.toString())
				executionNode.add("DEVICES", jsonArray)
		}
		return executionNode
	}
	def thirdPartyJsonPerformanceResultFromController(final String execName, final String appurl,def realPath ){
		JsonArray jsonArray = new JsonArray()
		JsonObject compNode
		JsonObject deviceNode
		JsonObject executionNode
		String appUrl = appurl
		String url
		appUrl = appurl + "/execution/getDetailedTestResult?execResId="
		Execution executionInstance = Execution.findByName(execName)
		if(executionInstance){
			ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
			def executionResultStatus //= ExecutionResult.findAllByExecutionAndStatusIsNotNull(executionInstance)
			def scriptStatus = null
			def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
			def executionResult //= ExecutionResult.findAllByExecution(executionInstance)

			executionDevice.each{ execDevice ->
				url = ""
				compNode = new JsonObject()
				deviceNode = new JsonObject()
				executionResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
		
					List<ExecutionResult> execResult = ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance, execDevice)
					def componentMap = [:].withDefault {[]}
					def systemMap = [:].withDefault {[]}
					execResult.each{ execResObj ->
//						Script.withTransaction { scriptRes ->
						def scriptMap = scriptService.getScriptNameModuleNameMapping(realPath)
						def moduleName =scriptMap.get(execResObj?.script)
						Module module= Module.findByName(moduleName)
						//Issue fix
						def script = scriptService.getScript(realPath,moduleName, execResObj?.script,scriptGrp?.category?.toString())
							if(module?.testGroup?.groupValue?.toString()?.equals("E2E") ){
								List val1 = systemMap.get(module.toString());
								if(!val1){
									val1 = []
									systemMap.put(module.toString(), val1)
								}
								val1.add(execResObj?.id)
							}
							else{
								List val = componentMap.get(module.toString());
								if(!val){
									val = []
									componentMap.put(module.toString(), val)
								}
								val.add(execResObj?.id)
							}
//						}
					}
					def statusVal
					def newmap = [:]
					JsonArray compArray = new JsonArray();
					
					componentMap.each{ k, v ->
						JsonObject compObject = new JsonObject();
						
						compObject.addProperty("ModuleName", k.toString())
						def lst = v
						statusVal = SUCCESS_STATUS
						
						JsonArray scriptStatusArray = new JsonArray();
						JsonObject scriptStatusNode
						lst.each{
							url = ""
							scriptStatusNode = new JsonObject()
							ExecutionResult exResult = ExecutionResult.findById(it)
							if(!exResult.status.equals(SUCCESS_STATUS)){
								statusVal = FAILURE_STATUS
							}
							scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
							scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							url = appUrl + exResult?.id.toString()
							scriptStatusNode.addProperty("LogUrl", url.toString())
							def benchmarkArray = getBenchMarkJsonArray(exResult)
							scriptStatusNode.add("TimeInfo", benchmarkArray)
							def cpuArray = getPerformanceJsonArray(exResult,Constants.SYSTEMDIAGNOSTICS_CPU)
							scriptStatusNode.add("CPU", cpuArray)
							def memArray = getPerformanceJsonArray(exResult,Constants.SYSTEMDIAGNOSTICS_MEMORY)
							scriptStatusNode.add("Memory", memArray)
							
							scriptStatusArray.add(scriptStatusNode)
							
						}
						
						newmap[k] = statusVal
						compObject.addProperty("ModuleStatus", statusVal.toString())
						compObject.add("ScriptDetails", scriptStatusArray)
						compArray.add(compObject)
					}
					
					JsonArray systemArray = new JsonArray();
					systemMap.each{ k, v ->
						JsonObject sysObject = new JsonObject();
						
						sysObject.addProperty("ModuleName", k.toString())
						def lst = v
						statusVal = SUCCESS_STATUS
						
						JsonArray scriptStatusArray = new JsonArray();
						JsonObject scriptStatusNode
						lst.each{
							url = ""
							scriptStatusNode = new JsonObject()
							ExecutionResult exResult = ExecutionResult.findById(it)
							if(!exResult.status.equals(SUCCESS_STATUS)){
								statusVal = FAILURE_STATUS
							}
							scriptStatusNode.addProperty("ScriptName", exResult.script.toString())
							scriptStatusNode.addProperty("ScriptStatus", exResult.status.toString())

							url = appUrl + exResult?.id.toString()
							scriptStatusNode.addProperty("LogUrl", url.toString())
							
							def benchmarkArray = getBenchMarkJsonArray(exResult)
							scriptStatusNode.add("TimeInfo", benchmarkArray)
							def cpuArray = getPerformanceJsonArray(exResult,Constants.SYSTEMDIAGNOSTICS_CPU)
							scriptStatusNode.add("CPU", cpuArray)
							def memArray = getPerformanceJsonArray(exResult,Constants.SYSTEMDIAGNOSTICS_MEMORY)
							scriptStatusNode.add("Memory", memArray)
							
							scriptStatusArray.add(scriptStatusNode)
							
						}
						
						newmap[k] = statusVal
						sysObject.addProperty("ModuleStatus", statusVal.toString())
						sysObject.add("ScriptDetails", scriptStatusArray)
						systemArray.add(sysObject)
					}

					deviceNode.addProperty("Device",execDevice?.device.toString())
					deviceNode.add("ComponentLevelDetails",compArray)
					deviceNode.add("SystemLevelDetails",systemArray)
					jsonArray.add(deviceNode)
				}
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
				executionNode.add("DEVICES", jsonArray)
		}else{
			executionNode = new JsonObject()
			executionNode.addProperty("status","FAILURE")
			executionNode.addProperty("remarks","no valid execution found with this name "+execName)
		}
		return executionNode
	}
	
	def getBenchMarkJsonArray(def execResult){
		def benchMarkList = Performance.findAllByExecutionResultAndPerformanceType(execResult,"BENCHMARK")
		JsonArray benchmarkArray = new JsonArray();
		if(benchMarkList?.size() > 0){
			benchMarkList?.each {  bMark ->
				JsonObject benchmark = new JsonObject()
				benchmark.addProperty("APIName", bMark?.processName)
				benchmark.addProperty("ExecutionTime", bMark?.processValue)
				benchmarkArray.add(benchmark)
			}
		}
		return benchmarkArray
	}
	
	def getPerformanceJsonArray(def execResult,def perfType){
		def perfList = Performance.findAllByExecutionResultAndPerformanceType(execResult,perfType)
		JsonArray perfArray = new JsonArray();
		if(perfList?.size() > 0){
			perfList?.each {  pData ->
				JsonObject perf = new JsonObject()
				perf.addProperty("ProcessName", pData?.processName)
				perf.addProperty("ProcessValue", pData?.processValue)
				perfArray.add(perf)
			}
		}
		return perfArray
	}
	
}
