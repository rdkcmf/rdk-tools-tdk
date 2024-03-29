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

import groovy.xml.MarkupBuilder

import java.text.SimpleDateFormat;
import java.util.List;
import org.apache.commons.lang.StringUtils;

/**
 * Service class of ExecutionController 
 */

class ExecutedbService {

	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication

	/**
	 * Injects the executionService.
	 */
	def executionService
	
	def scriptService

	public static final String SI_NO_LABEL 					= "SI NO:"
	public static final String EXPORT_SCRIPT_LABEL 			= "Script"
	public static final String EXPORT_STATUS_LABEL 			= "Status"
	public static final String EXPORT_TIMETAKEN 			= "Time Taken(min)"
	public static final String EXPORT_DEVICE_LABEL 			= "Device"
	public static final String EXPORT_DEVICE_DETAILS_LABEL 	= "Image Details"
	public static final String EXPORT_LOGDATA_LABEL			= "Log Data"
	public static final String EXPORT_FUNCTION_LABEL 		= "Function: "
	public static final String EXPORT_FUNCTION_STATUS_LABEL = "Function Status: "
	public static final String EXPORT_EXPECTED_RESULT_LABEL = "Expected Result: "
	public static final String EXPORT_ACTUAL_RESULT_LABEL 	= "Actual Result: "
	public static final String EXPORT_IPADDRESS_LABEL 		= "IP Address"
	public static final String EXPORT_EXECUTION_TIME_LABEL 	= "Time taken for execution(min)"
	public static final String EXPORT_COLUMN1_LABEL 		= "C1"
	public static final String EXPORT_COLUMN2_LABEL 		= "C2"
	public static final String EXPORT_SYSTEMDIAGNOSTICS		= "PerformanceData"
	public static final String EXPORT_BENCHMARKING			= "TimeInfo"
	public static final String EXPORT_PERFORMANCE			= "Performance"

	public static final String MARK_ALL_ID1 				= "markAll1"
	public static final String MARK_ALL_ID2 				= "markAll2"
	public static final String UNDEFINED					= "undefined"


	/**
	 * Function to create data in xml format for execution result
	 * @param execName
	 * @return
	 */
	def String getExecutionDataInXmlFormat(final String execName){
		Execution executionInstance = Execution.findByName(execName)
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
		xml.executionResult(name: executionInstance?.name.toString(), status: executionInstance?.result.toString()) {
			executionDevice.each{ executionDeviceInstance ->
				device(name:executionDeviceInstance?.device.toString(), deviceIp:executionDeviceInstance?.deviceIp, executiondate:executionInstance?.dateOfExecution, timetakentoexecute:executionInstance?.executionTime, status:executionDeviceInstance?.status) {

					def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionDeviceInstance.executionresults?.size()?.toString())

					Summary(){
						TotalScripts(summaryMap.get("Total Scripts"))
						Executed(summaryMap.get("Executed"))
						Success(summaryMap?.get("SUCCESS"))
						Failure(summaryMap?.get("FAILURE"))
						NotApplicable(summaryMap?.get("N/A"))
						Skipped(summaryMap?.get("SKIPPED"))
						Pending(summaryMap?.get("PENDING"))
						ScriptTimedOut(summaryMap?.get("TIMED OUT"))
						Undefined(summaryMap?.get("UNDEFINED"))
					}

					executionDeviceInstance.executionresults.each{ executionResultInstance ->
						scripts(name:executionResultInstance?.script, status:executionResultInstance?.status, scriptexecutiontime:executionResultInstance?.executionTime){
							executionResultInstance.executemethodresults.each{executionResultMthdsInstance ->
								function(name:executionResultMthdsInstance?.functionName){
									expectedResult(executionResultMthdsInstance?.expectedResult)
									actualResult(executionResultMthdsInstance?.actualResult)
									status(executionResultMthdsInstance?.status)
								}
							}
							logData(executionResultInstance?.executionOutput)
						}

						performance(){
							def benchmarkList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_BENCHMARK)
							TimeInfo(){
								benchmarkList?.each{ bmInstance ->
									Function(APIName:bmInstance?.processName,ExecutionTime:bmInstance?.processValue+"(ms)")
								}
							}
							def systemDiagList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_SYSTEMDIAGNOSTICS)
							PerformanceData{
								systemDiagList?.each{ sdInstance ->
									Process(ProcessName:sdInstance?.processName,ProcessValue:sdInstance?.processValue)
								}
							}
						}
					}
				}
			}
		}
		return writer
	}
	
	/**
	 * Method to check the Execution Instance is available or not
	 *
	 */
	def isValidExecutionAvailable(Execution executionInstance ){
		List executionDeviceList = []
		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		if(executionDeviceList){
			return Constants.SUCCESS_STATUS
		}
		return Constants.FAILURE_STATUS
	}


	/**
	 * Delete the selected execution results
	 * @param selectedRows
	 * @return
	 */
	def deleteSelectedRowOfExecutionResult(def selectedRows, String realPath) {
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		List executionResultList = []
		List executionMethodResultInstanceList = []
		List performanceList = []
		int deleteCount = 0

		for(int i=0;i<selectedRows.size();i++){
			if(selectedRows[i] != UNDEFINED && selectedRows[i] != MARK_ALL_ID1 && selectedRows[i] != MARK_ALL_ID2 ){
				Execution executionInstance = Execution.findById(selectedRows[i].toLong())
				if(!executionInstance?.executionStatus?.equals(INPROGRESS_STATUS) ){
					if( !executionInstance?.executionStatus?.equals(PAUSED)){
				if(executionInstance){

					executionResultList  = ExecutionResult.findAllByExecution(executionInstance)
					executionResultList.each { executionResultInstance ->
						if(executionResultInstance){
							executionMethodResultInstanceList = ExecuteMethodResult.findAllByExecutionResult(executionResultInstance)
							if(executionMethodResultInstanceList){
								executionMethodResultInstanceList.each { executionMethodResultInstance ->
									executionMethodResultInstance.delete(flush:true)
								}
							}
							performanceList = Performance.findAllByExecutionResult(executionResultInstance)
							performanceList.each{ performance ->
								performance.delete(flush:true)
							}
						}
						executionResultInstance.delete(flush:true)
					}

					def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)

					executionDeviceList.each{ executionDeviceInstance ->
						executionDeviceInstance.delete(flush:true)
					}
					
					if(executionInstance?.thirdPartyExecutionDetails){
						executionInstance?.thirdPartyExecutionDetails = null;
						executionInstance?.save();
					}
					
					def thirdPartyExecutionDetailsList = ThirdPartyExecutionDetails.findAllByExecution(executionInstance)
					thirdPartyExecutionDetailsList?.each{ thirdPartyExecution ->
						thirdPartyExecution?.delete(flush:true)
					}

					def execId = executionInstance?.id

					executionInstance.delete(flush:true)
					deleteCount ++
					log.info "Deleted "+executionInstance

					/**
					 * Deletes the log files, crash files 										  
					 */

					String logFilePath = "${realPathFromFile}//logs//"+execId
					def logFiles = new File(logFilePath)
					if(logFiles.exists()){
						logFiles?.deleteDir()
					}
					String crashFilePath = "${realPathFromFile}//logs//crashlogs//"

					new File(crashFilePath).eachFileRecurse { file->
						if((file?.name).startsWith(execId.toString())){
							file?.delete()
						}
					}

					String versionFilePath = "${realPathFromFile}//logs//version//"+execId
					def versionFiles = new File(versionFilePath)
					if(versionFiles.exists()){
						versionFiles?.deleteDir()
					}

					String agentLogFilePath = "${realPathFromFile}//logs//consolelog//"+execId
					def agentLogFiles = new File(agentLogFilePath)
					if(agentLogFiles.exists()){
						agentLogFiles?.deleteDir()
					}
				}
				else{
					log.info "Invalid executionInstance"
				}
				}
				}
			}
		}
		return deleteCount
	}
	
	/**
	 * Function to format execution time
	 */
	def executionTimeFormat ( def executionTime )
	{
		try {
			if(executionTime){
				if(executionTime.contains(".") ){
					int index = executionTime.indexOf(".")
					if((index + 3) < executionTime.length() ){
						executionTime = executionTime?.substring(0, index+3);
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return 	executionTime
	}

	/**
	 * Function to create data in excel format for execution result
	 * @param executionInstance
	 * @param realPath
	 * @return
	 */
	def getDataForExcelExport(Execution executionInstance, String realPath) {
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		List executionDeviceList = []
		List executionResultInstanceList = []
		List executionMethodResultInstanceList = []
		List executionReportData = []
		List dataList = []
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = []
		List benchmarkList = []
		List systemDiagList = []

		columnWidthList = [0.35, 0.5]
		String deviceDetails

		String fileContents = ""
		def deviceName = ""
		def deviceIp = ""
		def executionTime = ""

		String filePath = ""
		def executionDeviceId
		def benchMarkDetails = ""
		def sdDetails = ""

		Map mapDevice = [:]
		Map mapIpAddress = [:]
		Map mapExecutionTime = [:]
		Map deviceDetailsMap = [:]
		Map blankRowMap = [:]

		Map summaryHead = [:]
		Map statusValue = [:]



		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)

		executionDeviceList.each{ executionDeviceInstance ->

			deviceName = executionDeviceInstance?.device
			deviceIp = executionDeviceInstance?.deviceIp
			executionTime = executionDeviceInstance?.executionTime
			executionTime = executionTimeFormat ( executionTime )
			executionDeviceId = executionDeviceInstance?.id
			filePath = "${realPathFromFile}//logs//version//${executionInstance?.id}//${executionDeviceId?.toString()}//${executionDeviceId?.toString()}_version.txt"

			if(filePath){
				File file = new File(filePath)
				if(file.exists()){
					file.eachLine { line ->
						if(!(line.isEmpty())){
							if(!(line.startsWith( LINE_STRING ))){

								fileContents = fileContents + line + HTML_BR
							}
						}
					}
					deviceDetails = fileContents.replace(HTML_BR, NEW_LINE)
				}
				else{
					log.error "No version file found"
				}
			}
			else{
				log.error "Invalid file path"
			}
			
			String image = "Not Available"
			try {
				if(deviceDetails != null && deviceDetails.contains("imagename:")){
					String imagename = "imagename:"
					int indx = deviceDetails.indexOf(imagename)
					int endIndx = deviceDetails.indexOf("\n",indx)
					if(indx >=0 && endIndx > 0){
						indx = indx + imagename.length()
						image = deviceDetails.substring(indx, endIndx)
					}
				}
			} catch (Exception e) {
				e.printStackTrace()
			}

			mapDevice 			= ["C1":EXPORT_DEVICE_LABEL,"C2":deviceName]
			mapIpAddress 		= ["C1":EXPORT_IPADDRESS_LABEL, "C2": deviceIp]
			mapExecutionTime 	= ["C1":EXPORT_EXECUTION_TIME_LABEL,"C2":executionTime]
			deviceDetailsMap    = ["C1":EXPORT_DEVICE_DETAILS_LABEL,"C2":image]
			blankRowMap 		= ["C1":"     ","C2":"     "]
			
			

			dataList.add(blankRowMap)
			dataList.add(mapDevice)
			dataList.add(mapIpAddress)
			dataList.add(mapExecutionTime)
			dataList.add(deviceDetailsMap)
			dataList.add(blankRowMap)

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)//,[sort: "script",order: "asc"])

			def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionResultInstanceList?.size()?.toString())

			mapDevice 			= ["C1":"SUMMARY","C2":"   "]
			dataList.add(mapDevice)

			summaryMap.each{ mapInfo->
				statusValue 	= ["C1": mapInfo.key, "C2": mapInfo.value ]
				dataList.add(statusValue)
			}

			blankRowMap 		= ["C1":"     ","C2":"     "]
			dataList.add(blankRowMap)

			executionResultInstanceList.each{ executionResultInstance ->

				List functionList = []
				List expectedResultList = []
				List actualResultList = []
				List functionStatusList = []

				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String output = executionResultInstance?.executionOutput
				String scriptExecTime = executionResultInstance?.executionTime
				String executionOutput

				if(output){
					executionOutput = output.replace(HTML_BR, NEW_LINE)
					if(executionOutput && executionOutput.length() > 10000){
						executionOutput = executionOutput.substring(0, 10000)
					}
				}

				Map scriptNameMap 	= ["C1":EXPORT_SCRIPT_LABEL,"C2":scriptName]
				Map statusMap 		= ["C1":EXPORT_STATUS_LABEL,"C2":status]
				Map scriptTimeMap 	= ["C1":EXPORT_TIMETAKEN,"C2":scriptExecTime]
				Map logDataMap 		= ["C1":EXPORT_LOGDATA_LABEL,"C2":executionOutput]

				dataList.add(scriptNameMap)
				dataList.add(statusMap)
				dataList.add(scriptTimeMap)
				executionMethodResultInstanceList = ExecuteMethodResult.findAllByExecutionResult(executionResultInstance)
				if(executionMethodResultInstanceList){
					executionMethodResultInstanceList.each{ executionMethodResultInstance ->
						Map executionMethodResultMap = [:]
						def functionName = executionMethodResultInstance?.functionName
						def expectedResult = executionMethodResultInstance?.expectedResult
						def actualResult = executionMethodResultInstance?.actualResult
						def functionStatus = executionMethodResultInstance?.status
						functionList.add(functionName)
						expectedResultList.add(expectedResult)
						actualResultList.add(actualResult)
						functionStatusList.add(functionStatus)
					}
				}

				int functionCount = functionList.size()
				for(int i=0;i<functionCount;i++){

					def functionDetails
					functionDetails = EXPORT_EXPECTED_RESULT_LABEL+expectedResultList[i] + NEW_LINE +
							EXPORT_ACTUAL_RESULT_LABEL+actualResultList[i] + NEW_LINE + EXPORT_FUNCTION_STATUS_LABEL+functionStatusList[i] + NEW_LINE

					Map functionDetailsMap = ["C1":EXPORT_FUNCTION_LABEL+functionList[i],"C2":functionDetails]
					dataList.add(functionDetailsMap)
				}

				dataList.add(logDataMap)
				dataList.add(blankRowMap)

				populateChartData(executionInstance,realPathFromFile)

				benchMarkDetails = ""				
				sdDetails = ""
				
				benchmarkList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_BENCHMARK)
				systemDiagList = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,KEY_SYSTEMDIAGNOSTICS)

				benchmarkList?.each{ bmInstance ->
					benchMarkDetails = benchMarkDetails + bmInstance?.processName + HYPHEN + bmInstance?.processValue +"(ms)" + NEW_LINE
				}

				systemDiagList?.each{ sdInstance ->
					sdDetails = sdDetails + sdInstance?.processName + HYPHEN + sdInstance?.processValue + NEW_LINE
				}
				if(benchmarkList || systemDiagList){
					Map performanceHeadMap = ["C1":EXPORT_PERFORMANCE]
					dataList.add(performanceHeadMap)
					dataList.add(blankRowMap)

					Map benchMarkHeadMap = ["C1":EXPORT_BENCHMARKING,"C2":benchMarkDetails]
					dataList.add(benchMarkHeadMap)

					Map sdHeadMap = ["C1":EXPORT_SYSTEMDIAGNOSTICS,"C2":sdDetails]
					dataList.add(sdHeadMap)
				}
			}
		}
		return dataList
	}
	
	/**
	 * Method to getting execution details as a map for generating comparison report.
	 * @param baseExecution
	 * @param comparisonExecution
	 * @param counter
	 * @param realPath
	 * @return
	 */
	def getExecutionDetailsAsMap(Execution baseExecution,Execution comparisonExecution,def counter,String realPath){
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		Map executionMap = [:]
		List baseExecutionScriptList = []
		def successCount = 0;
		def failureCount = 0;
		def skippedCount = 0;
		def timeoutCount = 0;
		def naCount = 0;
		def pendingCount = 0;
		def executedCount = 0;
		def newFailureCount = 0;
		def newScriptCount = 0;
		def newTimedOutCount = 0;
		int rate = 0;
		def image = "Image name not available"
		def baseExecutionResultList = ExecutionResult.findAllByExecution(baseExecution)
		baseExecutionResultList.each {executionResult ->
			def moduleName
			def scriptName = executionResult?.script
			def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
			moduleName = sMap.get(scriptName)
			if(moduleName){
				baseExecutionScriptList.add(scriptName)
			}
		}
		def comparisonExecutionResultList = ExecutionResult.findAllByExecution(comparisonExecution)
		ExecutionDevice comparisonExecutionDevice = ExecutionDevice.findByExecution(comparisonExecution)
		if(comparisonExecutionDevice?.buildName && !comparisonExecutionDevice?.buildName?.isEmpty() && !comparisonExecutionDevice?.buildName?.equals("Image name not available")){
			image = comparisonExecutionDevice?.buildName
		}else if(realPathFromFile && comparisonExecution?.id && comparisonExecutionDevice?.id){
			String imageNameFromVersionFile = getImageNameFromVersionFile(realPathFromFile,comparisonExecution?.id,comparisonExecutionDevice?.id)
			if(imageNameFromVersionFile != null && !imageNameFromVersionFile.isEmpty()){
				image = imageNameFromVersionFile
			}
		}
		def scriptNameList = []
		executionMap.put("Sl No", counter)
		executionMap.put("Execution Name", comparisonExecution?.name)
		if(comparisonExecution?.script){
			executionMap.put("Test Suite", comparisonExecution?.script)
		}else{
			executionMap.put("Test Suite", comparisonExecution?.scriptGroup)
		}
		executionMap.put("Image Name", image)
		comparisonExecutionResultList.each {executionResult ->
			def moduleName
			def scriptName = executionResult?.script
			def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
			moduleName = sMap.get(scriptName)
			if(moduleName){
				if(!baseExecutionScriptList?.contains(scriptName)){
					newScriptCount++
				}
				def status = executionResult?.status
				executedCount++
				if(Constants.SUCCESS_STATUS.equals(status)){
					successCount++
				}
				else if(Constants.FAILURE_STATUS.equals(status)){
					failureCount++
					if(!baseExecutionScriptList?.contains(scriptName)){
						newFailureCount++
					}
				}
				else if(Constants.SKIPPED_STATUS.equals(status)){
					skippedCount++
				}
				else if(Constants.NOT_APPLICABLE_STATUS.equals(status)){
					naCount++
				}
				else if(Constants.SCRIPT_TIME_OUT.equals(status)){
					timeoutCount++
					if(!baseExecutionScriptList?.contains(scriptName)){
						newTimedOutCount++
					}
				}else if(Constants.PENDING.equals(status)){
					pendingCount++
				}
			}
		}
		executedCount = executedCount - pendingCount
		executionMap.put(Constants.EXECUTED, executedCount)
		executionMap.put(Constants.SUCCESS_STATUS, successCount)
		executionMap.put(Constants.FAILURE_STATUS, failureCount)
		executionMap.put(Constants.SCRIPT_TIME_OUT, timeoutCount)
		executionMap.put(Constants.NOT_APPLICABLE_STATUS, naCount)
		executionMap.put(Constants.SKIPPED_STATUS, skippedCount)
		if(executedCount!=naCount){
			rate =successCount*100/(executedCount-naCount)
		}
		executionMap.put("Pass %", rate)
		executionMap.put("New Failure Script Count", newFailureCount)
		executionMap.put("New Timedout Script Count", newTimedOutCount)
		executionMap.put("New Script Count", newScriptCount)
		return executionMap
	}
	
	/**
	 * Method to generate the data for creating the comparison report in excel format.
	 * @param baseExecutionName
	 * @param comparisonExecutionNames
	 * @param appUrl
	 * @param realPath
	 * @return
	 */
	def getDataForComparisonReportGeneration(String baseExecutionName, List comparisonExecutionNames ,String appUrl, String realPath) {
		Map detailDataMap = [:]
		List allexecutionsList = []
		List totalScriptList = []
		Map summaryLabels = ["Sl No":"", "Execution Name":"", "Test Suite":"","Image Name":"" ,"Executed":"", "SUCCESS":"", "FAILURE":"", "SCRIPT TIME OUT":"", "N/A":"", "SKIPPED":"", "Pass %":"", "New Failure Script Count":"", "New Timedout Script Count":"", "New Script Count":""]
		Map detailsMap = [:]
		Map coverPageMap = [:]
		Map coverPageExecutionMap = [:]
		Execution baseExecution = Execution.findByName(baseExecutionName)
		allexecutionsList.add(baseExecution)
		if(baseExecution){			
			detailsMap.put("Base Execution Name ", baseExecutionName)
			detailsMap.put("Device", baseExecution?.device)
			coverPageMap.put("Details",detailsMap)
			int counter = 1
			//setting the base execution details as the 1st row in cover page
			coverPageExecutionMap = getExecutionDetailsAsMap(baseExecution, baseExecution,counter,realPath)
			coverPageMap.put(baseExecutionName,coverPageExecutionMap)
			//getting the comparison execution details as a map to be displayed in cover page
			for(int i=0;i<comparisonExecutionNames.size();i++){
				coverPageExecutionMap = [:]
				counter ++ 
				Execution comparisonExecution = Execution.findByName(comparisonExecutionNames[i])
				if(comparisonExecution){
					coverPageExecutionMap = getExecutionDetailsAsMap(baseExecution, comparisonExecution,counter,realPath)
					coverPageMap.put(comparisonExecutionNames[i],coverPageExecutionMap)
					allexecutionsList.add(comparisonExecution)
				}
			}
			coverPageMap.put("Labels",summaryLabels)
			detailDataMap.put("CoverPage", coverPageMap)
			//generating the comparison report page 
			allexecutionsList.each {execution ->
				def executionResultList = ExecutionResult.findAllByExecution(execution)
				executionResultList.each {executionResult ->
					if(!totalScriptList.contains(executionResult?.script)){
						totalScriptList.add(executionResult?.script)
					}
				}
			}
			totalScriptList = totalScriptList?totalScriptList?.sort():[]
			//to generate the data map for each script
			int scriptCounter = 1
			List dataList = []
			Map dataMapList = [:]
			List fieldsList = []
			fieldsList.add("Sl No")
			fieldsList.add("Module Name")
			fieldsList.add("Script Name")
			fieldsList.add("Pass %")
			totalScriptList.each {scriptName ->
				int rate = 0
				def successCount = 0;
				def naCount = 0;
				def totalCount = 0;
				Map dataMap = [:]
				def moduleName
				def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
				moduleName = sMap.get(scriptName)
				if(moduleName){
					dataMap.put("Sl No",scriptCounter)
					dataMap.put("Module Name",moduleName)
					dataMap.put("Script Name",scriptName)
					dataMap.put("Pass %","")
					allexecutionsList.each {execution ->
						String executionName = execution?.name
						def executionResult = ExecutionResult.findByExecutionAndScript(execution,scriptName)
						if(!(fieldsList.contains(executionName))){
							fieldsList.add(executionName)
						}
						if(executionResult){
							dataMap.put(executionName,executionResult?.status)
							if(executionResult?.status == SUCCESS_STATUS){
								successCount++
							}
							if(executionResult?.status == NOT_APPLICABLE_STATUS){
								naCount++
							}
							totalCount++
						}else{
							dataMap.put(executionName,"Not Executed")
						}
						
					}
					scriptCounter++
					if(totalCount!=naCount){
						rate =successCount*100/(totalCount-naCount)
					}
					dataMap.put("Pass %",rate.toString())
					dataList.add(dataMap)
				}
			}
			dataMapList.put("dataList",dataList)
			dataMapList.put("fieldsList",fieldsList)
			detailDataMap.put("Comparison Results",dataMapList)
		}
		return detailDataMap
	}
	/**
	 * Method to generate the data for creating the combined report in excel format.
	 */
	def getDataForCombinedExcelReportGeneration(List selectedRowsDefined ,String appUrl, String realPath) {
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		Map moduleNameScriptListMap = [:]
		Map scriptNameExecutionResultIdMap = [:]
		Map executionResultIdScriptNameMap = [:]
		def executionInstance
		List executionNames = []
		List deviceNameList = []
		List deviceIpList = []
		List executionTimeList = []
		def moduleName
		List selectedRows = []
		selectedRowsDefined = selectedRowsDefined.sort();
		for(int i=0;i<selectedRowsDefined.size();i++){
			if (!selectedRows.contains(selectedRowsDefined[i])) {
				selectedRows.add(selectedRowsDefined[i]);
			}
		}
		//For generating a map with key	as module name and value as list of script names of all the execution result id's
		for(int i=0;i<selectedRows.size();i++){
			executionInstance = Execution.findById(selectedRows[i])
			executionNames.add(executionInstance.name)
			def executionTime = executionInstance?.realExecutionTime
			executionTime = executionTimeFormat (executionTime)
			executionTimeList.add(executionTime)
			def executionDeviceInstance = ExecutionDevice.findByExecution(executionInstance)
			if(!deviceNameList.contains(executionDeviceInstance?.device)){
				deviceNameList.add(executionDeviceInstance?.device)
				deviceIpList.add(executionDeviceInstance?.deviceIp)
			}
			def executionResultList = ExecutionResult.findAllByExecution(executionInstance)
			def scriptNameList = []
			executionResultList.each {executionResult ->
				scriptNameList.add(executionResult.script)
				def executionResultId = executionResult.id.toString()
				executionResultIdScriptNameMap.put(executionResult.id, executionResult.script)
			}
			scriptNameList.each {scriptName ->
				def scriptNameListForMap = []
				def scriptFile =  ScriptFile.findByScriptName(scriptName)
				if(scriptFile){
					def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
					moduleName = sMap.get(scriptName)
					if(moduleName){
						def moduleNameFromMap = moduleNameScriptListMap.get(moduleName)
						if(moduleNameScriptListMap.containsKey(moduleName)){
							def scriptPresentList = []
							scriptPresentList = moduleNameScriptListMap.get(moduleName)
							if(scriptPresentList.contains(scriptName)){
								log.info "Script Name already present in map"
							}
							else{
								def scriptNameListFromMap = []
								scriptNameListFromMap = moduleNameScriptListMap.get(moduleName)
								scriptNameListFromMap.add(scriptName)
								moduleNameScriptListMap.put(moduleName, scriptNameListFromMap)
							}
						}
						else{
							scriptNameListForMap.add(scriptName)
							moduleNameScriptListMap.put(moduleName, scriptNameListForMap)
						}
					}
				}
			}
		}
		//For generating a second map with key as script names that is executed in the executions we selected and
		//value as latest execution result id of that script.
		TreeMap<Long, String> executionResultIdScriptNameMapAfterSorting = new TreeMap<Long, String>(executionResultIdScriptNameMap) 
		executionResultIdScriptNameMapAfterSorting.each{
			executionResultId, scriptName ->
			if(scriptNameExecutionResultIdMap.containsKey(scriptName)){
				def idForScript = scriptNameExecutionResultIdMap.get(scriptName)
				def executionResultNew = ExecutionResult.findById(executionResultId)
				def statusOfExecutionResultNew = executionResultNew.status 
				def executionResultOld = ExecutionResult.findById(idForScript)
				def statusOfExecutionResultOld = executionResultOld.status
				if(idForScript < executionResultId){
					if(!statusOfExecutionResultOld.equals(Constants.SUCCESS_STATUS)){
						if(statusOfExecutionResultNew.equals(Constants.SUCCESS_STATUS)){
							scriptNameExecutionResultIdMap.put(scriptName, executionResultId)
						}
					}
				}
			}
			else{
				scriptNameExecutionResultIdMap.put(scriptName, executionResultId)
			}
		}
		//For generating the data required for excel generation from the 2 maps created
			def detailDataMap = [:]
			Map coverPageMap = [:]
			Map detailsMap = [:]
			Map moduleMap = [:]
			List fieldList = ["C1", "C2", "C3", "C4", "C5","C6","C7","C8","C9","C10","C11"]
			def deviceName = ""
			def deviceIp = ""
			def executionTime = ""
			def totalSuccessCount = 0;
			def totalFailureCount = 0;
			def totalSkippedCount = 0;
			def totalTimeoutCount = 0;
			def totalExecutionCount = 0;
			def totalNaCount = 0;
			def totalScriptIssueCount = 0;
			def totalRdkIssueCount = 0;
			def totalEnvIssueCount = 0;
			def totalNewIssueCount = 0;
			def totalInterfaceChangeCount = 0;
			def totalAnalysedCount = 0;
			def totalExecutionTime;
			def executionInstanceForImage;
			int totalPassRate = 0;
			List executionDeviceList = [];
			List executionList = [];
			detailsMap.put("Execution Names ", executionNames)
			detailsMap.put("Device", deviceNameList)
			detailsMap.put("DeviceIP", deviceIpList)
			detailsMap.put("Execution Time (min)", executionTimeList)
			String image = ""
			List imageList = [];
			for(int i=0;i<selectedRows.size();i++){
				executionInstanceForImage = Execution.findById(selectedRows[i])
				if(executionInstanceForImage != null){
					executionList.add(executionInstanceForImage)
				}
			}
			executionList?.each{ executionObjectForImage ->
				def executionDevice = ExecutionDevice.findByExecution(executionObjectForImage)
				if(executionDevice?.buildName && !executionDevice?.buildName?.isEmpty() && !executionDevice?.buildName?.equals("Image name not available")){
					imageList.add(executionDevice?.buildName)
				}else if(realPathFromFile && executionObjectForImage?.id && executionDevice?.id){
					String imageNameFromVersionFile = getImageNameFromVersionFile(realPathFromFile,executionObjectForImage?.id,executionDevice?.id)
					if(imageNameFromVersionFile != null && !imageNameFromVersionFile.isEmpty()){
						imageList.add(imageNameFromVersionFile)
					}
				}
			}
			imageList?.each{ imageInstance ->
				if (!imageInstance.equals(imageList.get(0))){
					if(!imageInstance.equals("NULL")){
						image = image + "  " +imageInstance
					}
				}
				else{
					if(!imageList.get(0).equals("NULL")){
						image = imageList.get(0)
					}
					else{
						image = "Not Available"
					}
				}
			}
			if(image.equals("Not Available")){
				detailsMap.put("Image", image)
			}
			else{
				String replaceString = image.replace('Not Available','');
				detailsMap.put("Image", replaceString)
			}
			coverPageMap.put("Details",detailsMap)
			detailDataMap.put("CoverPage", coverPageMap)
			int counter = 1
			moduleNameScriptListMap.each{ modName, scriptList ->
				def dataList = []
				Map dataMapList = [:]
				moduleMap = [:]
				moduleMap.put("Sl No", counter)
				moduleMap.put("Module", modName)
				def executedScripts = moduleNameScriptListMap.get(modName)
				moduleMap.put("Executed", executedScripts.size())
				totalExecutionCount = totalExecutionCount + executedScripts.size()
				def successCount = 0;
				def failureCount = 0;
				def skippedCount = 0;
				def timeoutCount = 0;
				def naCount = 0;
				def scriptIssueCount = 0;
				def rdkIssueCount = 0;
				def envIssueCount = 0;
				def newIssueCount = 0;
				def interfaceChangeCount = 0;
				def c1Counter = 1;
				executedScripts.each {scriptName ->
					def executionResultId = scriptNameExecutionResultIdMap.get(scriptName)
					def executionResult = ExecutionResult.findById(executionResultId)
					Execution executionForResultAnalysis = executionResult?.execution
					def executionForResultAnalysisId = executionForResultAnalysis?.id
					String executionName = executionForResultAnalysis?.name
					String executionDeviceName = executionForResultAnalysis?.device
					def executionNameAfterSplit = executionName.split(executionDeviceName)
					def repeatRerunFlag = Constants.NO
					if(executionNameAfterSplit[1].contains("_") || executionNameAfterSplit[1].contains("RERUN")){
						repeatRerunFlag = Constants.YES
					}
					def status = executionResult?.status
					if(Constants.SUCCESS_STATUS.equals(status)){
						successCount++
						totalSuccessCount++
					}
					else if(Constants.FAILURE_STATUS.equals(status)){
						failureCount++
						totalFailureCount++
					}
					else if(Constants.SKIPPED_STATUS.equals(status)){
						skippedCount++
						totalSkippedCount++
					}
					else if(Constants.NOT_APPLICABLE_STATUS.equals(status)){
						naCount++
						totalNaCount++
					}
					else if(Constants.SCRIPT_TIME_OUT.equals(status)){
						timeoutCount++
						totalTimeoutCount++
					}
					String executed
					if( Constants.PENDING.equals(status)){
						executed = Constants.NO
					}
					else{
						executed = Constants.YES
					}
					def executionOutput
					String output = executionResult?.executionOutput
					if(output){
						executionOutput = output.replace(HTML_BR, NEW_LINE)
						if(executionOutput && executionOutput.length() > 10000){
							executionOutput = executionOutput.substring(0, 10000)
						}
					}
					def countOfExecutionOutput = executionOutput?.size()
					String executionLogData = executionOutput
					if(countOfExecutionOutput >= 1000 ){
						executionLogData = executionOutput+"\n More data use this link ....... \n " +appUrl+"/execution/getExecutionOutput?execResId="+executionResult?.id
					}
					String ticketNo = ""
					String remarks = ""
					String issueType = ""
					DefectDetails defectDetails = DefectDetails.findByExecutionIdAndScriptName(executionForResultAnalysisId, scriptName)
					if(defectDetails != null)  {
						ticketNo = defectDetails.ticketNumber
						remarks = defectDetails.remarks
						issueType = defectDetails.defectType
						if(defectDetails.defectType.equals(RDK_ISSUE)){
							rdkIssueCount++
							totalRdkIssueCount++
							if(defectDetails.remarks.contains(NEW_ISSUE)){
								newIssueCount++
								totalNewIssueCount++
							}
						}
						else if(defectDetails.defectType.equals(SCRIPT_ISSUE)){
							scriptIssueCount++
							totalScriptIssueCount++
						}
						else if(defectDetails.defectType.equals(ENVIRONMENT_ISSUE)){
							envIssueCount++
							totalEnvIssueCount++
						}
						else if(defectDetails.defectType.equals(INTERFACE_CHANGE)){
							interfaceChangeCount++
							totalInterfaceChangeCount++
						}
					}
					Map dataMap =["C1":c1Counter,"C2":scriptName,"C3":executed,"C4":status,"C5":parseTime(executionResult?.dateOfExecution),"C6":executionLogData,"C7":ticketNo,"C8":issueType,"C9":remarks,"C10":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResult?.id,"C11":repeatRerunFlag]
					dataList.add(dataMap)
					c1Counter ++
					dataMapList.put("counter",c1Counter)
				}
				moduleMap.put(Constants.SUCCESS_STATUS, successCount)
				moduleMap.put(Constants.FAILURE_STATUS, failureCount)
				moduleMap.put(Constants.SCRIPT_TIME_OUT, timeoutCount)
				moduleMap.put(Constants.NOT_APPLICABLE_STATUS, naCount)
				moduleMap.put(Constants.SKIPPED_STATUS, skippedCount)
				if(!newIssueCount) {newIssueCount = 0}
				if(!rdkIssueCount) {rdkIssueCount = 0}
				def existingIssueCount = rdkIssueCount - newIssueCount
				moduleMap.put("Number of failed scripts linked with open defects", rdkIssueCount? rdkIssueCount:0)
				moduleMap.put(SCRIPT_ISSUE, scriptIssueCount?scriptIssueCount:0)
				moduleMap.put("Existing Issue", existingIssueCount)
				moduleMap.put(ENVIRONMENT_ISSUE, envIssueCount? envIssueCount: 0)
				moduleMap.put(NEW_ISSUE, newIssueCount?newIssueCount : 0)
				moduleMap.put(INTERFACE_CHANGE, interfaceChangeCount? interfaceChangeCount : 0)
				moduleMap.put("Remarks","")
				coverPageMap.put(modName,moduleMap)
				counter++
				dataMapList.put("dataList",dataList)
				dataMapList.put("fieldsList",fieldList)
				detailDataMap.put(modName,dataMapList)
			}
			def executedCount = moduleNameScriptListMap.size()
			Map resultMap = [:]
			resultMap.put("Sl No", "")
			resultMap.put("Module", "Total")
			resultMap.put("Executed", totalExecutionCount)
			resultMap.put(Constants.SUCCESS_STATUS, totalSuccessCount)
			resultMap.put(Constants.FAILURE_STATUS, totalFailureCount)
			resultMap.put(Constants.SCRIPT_TIME_OUT, totalTimeoutCount)
			resultMap.put(Constants.NOT_APPLICABLE_STATUS, totalNaCount)
			resultMap.put(Constants.SKIPPED_STATUS, totalSkippedCount)
			if((totalExecutionCount - totalNaCount)!=0){
				totalPassRate = ((totalSuccessCount * 100)/(totalExecutionCount - totalNaCount))
			}
			totalAnalysedCount  = totalNewIssueCount + totalInterfaceChangeCount + totalEnvIssueCount + totalScriptIssueCount + totalRdkIssueCount
			if(totalAnalysedCount > 0){
				resultMap.put("Number of failed scripts linked with open defects", totalRdkIssueCount)
				resultMap.put(SCRIPT_ISSUE, totalScriptIssueCount)
				def totalExistingIssueCount = totalRdkIssueCount - totalNewIssueCount
				resultMap.put("Existing Issue", totalExistingIssueCount)
				resultMap.put(ENVIRONMENT_ISSUE, totalEnvIssueCount)
				resultMap.put(NEW_ISSUE, totalNewIssueCount)
				resultMap.put(INTERFACE_CHANGE,totalInterfaceChangeCount)
				resultMap.put("Remarks","")
			}
			coverPageMap.put("Total", resultMap)
			coverPageMap.put(Constants.OVERALL_PASS_RATE, totalPassRate)
			detailDataMap.each{ page, data ->
				if(!page.equals("CoverPage")){
					def dataMapList = detailDataMap.get(page)
					def counterValue = dataMapList.get("counter")
					dataMapList.remove("counter")
					dataMapList.put("counter",counterValue)
				}
				else{
					
					if(totalAnalysedCount < 1){
						def dataMapList = detailDataMap.get(page)
						moduleNameScriptListMap.each{ modName, scriptList ->
							def moduleList = dataMapList.get(modName)
							moduleList.remove("Number of failed scripts linked with open defects")
							moduleList.remove("Script Issue")
							moduleList.remove("Existing Issue")
							moduleList.remove("Environment Issue")
							moduleList.remove("New Issue")
							moduleList.remove("Interface Change")
							moduleList.remove("Remarks")
						}
					}
				}
			}
			return detailDataMap
	}

	
	/**
	 * Function to get the pmap details for a particular execution result
	 * @param executionInstance
	 * @param executionDevice
	 * @param executionResult
	 * @param realPath
	 * @return
	 */
	def getPmapDetails(Execution executionInstance,ExecutionDevice executionDevice,ExecutionResult executionResult, String realPath,String appUrl){
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		def logPath = "${realPathFromFile}/logs//${executionInstance.id}//${executionDevice.id}//${executionResult.id}//"
		def finalLogparserFileName = ""
		File logDir  = new File(logPath)
		Map pmapFileMap = [:]
		try{
			if(logDir?.exists() &&  logDir?.isDirectory()){
				logDir.eachFile{ file->
					def currentFileName = file?.getName()
					if(file?.getName()?.contains("pmapData")){
						List fileContent = file?.readLines()
						String fileContents = ""
						for (int index = 0; index <= 400; index++) {
							fileContents = fileContents + NEW_LINE+ fileContent[index]
						}
						if(fileContent?.size() > 400){
							fileContents = fileContents + NEW_LINE
							fileContents = fileContents+"\n More data use this link ....... \n " +appUrl+"/execution/showFileContents?fileName="+file?.getName()+"&execId="+executionInstance?.id+"&execDeviceId="+executionDevice?.id+"&execResultId="+executionResult.id
						}
						currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
						pmapFileMap?.put(currentFileName,fileContents)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return pmapFileMap
	}
	
	/**
	 * Method to fetch the list of alerts for a particular executionresult
	 * @param executionResult
	 * @param realPath
	 * @return
	 */
	def getAlertListFrom(ExecutionResult executionResult, String realPath){
		Map alertMapForExecRes = [:]
		try{
			Date fromDate = executionResult.dateOfExecution
			String executionTime = executionResult.totalExecutionTime
			if(executionTime != null && executionTime != ""){
				def device = Device.findByStbName(executionResult?.device)
				String macAddress = ""
				if(device){
					macAddress = device?.serialNo
				}
				Double totalExecutionTime =  Double.parseDouble(executionTime)
				totalExecutionTime = totalExecutionTime * 1000
				long totalExecutionTimeInLong = (long)totalExecutionTime;
				Date toDate = new Date(fromDate.getTime() + totalExecutionTimeInLong);
				def alertListFromService = executionService.fetchAlertData(fromDate,toDate,macAddress,realPath)
				if(!alertListFromService?.isEmpty()){
					alertListFromService.each{ alert ->
						List metricList = []
						def metric =  alert?.get('metric')
						if(alertMapForExecRes.containsKey(metric)){
							metricList = alertMapForExecRes.get(metric)
						}
						metricList?.add(alert)
						alertMapForExecRes.put(metric, metricList)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return alertMapForExecRes
	}
	
	/**
	 * Function to get the lmbench details for a particular execution result
	 * @param executionInstance
	 * @param executionDevice
	 * @param executionResult
	 * @param realPath
	 * @return
	 */
	def getlmbenchDetails(Execution executionInstance,ExecutionDevice executionDevice,ExecutionResult executionResult, String realPath,String appUrl){
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		def logPath = "${realPathFromFile}/logs//${executionInstance.id}//${executionDevice.id}//${executionResult.id}//"
		def finalLogparserFileName = ""
		File logDir  = new File(logPath)
		Map lmbenchFileMap = [:]
		try{
			if(logDir?.exists() &&  logDir?.isDirectory()){
				logDir.eachFile{ file->
					def currentFileName = file?.getName()
					if(file?.getName()?.contains("lmbench")){
						List fileContent = file?.readLines()
						String fileContents = ""
						for (int index = 0; index <= 400; index++) {
							fileContents = fileContents + NEW_LINE+ fileContent[index]
						}
						if(fileContent?.size() > 400){
							fileContents = fileContents + NEW_LINE
							fileContents = fileContents+"\n More data use this link ....... \n " +appUrl+"/execution/showFileContents?fileName="+file?.getName()+"&execId="+executionInstance?.id+"&execDeviceId="+executionDevice?.id+"&execResultId="+executionResult.id
						}
						currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
						lmbenchFileMap?.put(currentFileName,fileContents)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return lmbenchFileMap
	}
	
	/**
	 * Function to get the systemdBootchart details for a particular execution result
	 * @param executionInstance
	 * @param executionDevice
	 * @param executionResult
	 * @param realPath
	 * @return
	 */
	def getsystemdBootchartDetails(Execution executionInstance,ExecutionDevice executionDevice,ExecutionResult executionResult, String realPath,String appUrl){
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		def logPath = "${realPathFromFile}/logs//${executionInstance.id}//${executionDevice.id}//${executionResult.id}//"
		def finalLogparserFileName = ""
		File logDir  = new File(logPath)
		Map systemdBootchartMap = [:]
		try{
			if(logDir?.exists() &&  logDir?.isDirectory()){
				logDir.eachFile{ file->
					def currentFileName = file?.getName()
					if(file?.getName()?.contains("systemdBootchart") && file?.getName()?.contains("svg")){
						String fileContents = ""
						fileContents = fileContents+"\n Use this link ....... \n " +appUrl+"/execution/showSVGContents?fileName="+file?.getName()+"&execId="+executionInstance?.id+"&execDeviceId="+executionDevice?.id+"&execResultId="+executionResult.id
						currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
						systemdBootchartMap?.put(currentFileName,fileContents)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return systemdBootchartMap
	}
	
	/**
	 * Function to get the systemdAnalyze details for a particular execution result
	 * @param executionInstance
	 * @param executionDevice
	 * @param executionResult
	 * @param realPath
	 * @return
	 */
	def getsystemdAnalyzeDetails(Execution executionInstance,ExecutionDevice executionDevice,ExecutionResult executionResult, String realPath,String appUrl){
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		def logPath = "${realPathFromFile}/logs//${executionInstance.id}//${executionDevice.id}//${executionResult.id}//"
		def finalLogparserFileName = ""
		File logDir  = new File(logPath)
		Map systemdAnalyzeMap = [:]
		try{
			if(logDir?.exists() &&  logDir?.isDirectory()){
				logDir.eachFile{ file->
					def currentFileName = file?.getName()
					if(file?.getName()?.contains("systemdAnalyze") && file?.getName()?.contains("svg")){
						String fileContents = ""
						fileContents = fileContents+"\n Use this link ....... \n " +appUrl+"/execution/showSVGContents?fileName="+file?.getName()+"&execId="+executionInstance?.id+"&execDeviceId="+executionDevice?.id+"&execResultId="+executionResult.id
						currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
						systemdAnalyzeMap?.put(currentFileName,fileContents)
					}else if(file?.getName()?.contains("systemdAnalyze") && !(file?.getName()?.contains("svg"))){
						String fileContents = ""
						file.eachLine { line ->
							fileContents = fileContents + NEW_LINE+ line
						}
						currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
						systemdAnalyzeMap?.put(currentFileName,fileContents)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return systemdAnalyzeMap
	}
	
	/**
	 * Function to get the smem details for a particular execution result
	 * @param executionInstance
	 * @param executionDevice
	 * @param executionResult
	 * @param realPath
	 * @return
	 */
	def getSmemDetails(Execution executionInstance,ExecutionDevice executionDevice,ExecutionResult executionResult, String realPath){
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		def logPath = realPathFromFile + "/logs//${executionInstance.id}//${executionDevice.id}//${executionResult.id}//"
		def finalLogparserFileName = ""
		File logDir  = new File(logPath)
		Map smemFileMap = [:]
		try{
			if(logDir?.exists() &&  logDir?.isDirectory()){
				logDir.eachFile{ file->
					def currentFileName = file?.getName()
					if(file?.getName()?.contains("smemData")){
						String fileContents = ""
						file.eachLine { line ->
							fileContents = fileContents + NEW_LINE+ line
						}
						currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
						smemFileMap?.put(currentFileName,fileContents)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return smemFileMap
	}
	/**
	 * Method to generate the data for creating the profiling data report in excel format.
	 */
	def getDataForProfilingMetricsExcelReportGeneration(Execution executionInstance, String realPath,String appUrl) {
		List executionResultList = []
		def detailDataMap = [:]
		def coverPageMap = [:]
		List fieldList = ["C1", "C2", "C3", "C4","C5","C6","C7","C8"]
		ExecutionDevice executionDevice  = ExecutionDevice.findByExecution(executionInstance)
		executionResultList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDevice)
		Map detailsMap = [:]
		String image = ""
		detailsMap.put("Device", executionDevice?.device)
		detailsMap.put("DeviceIP", executionDevice?.deviceIp)
		def executionTime = executionInstance?.realExecutionTime
		executionTime = executionTimeFormat (executionTime)
		detailsMap.put("Execution Time (min)", executionTime)
		if(executionDevice?.buildName){
			image = executionDevice?.buildName
		}else{
			image = "Image name not available"
		}
		detailsMap.put("Image", image)
		coverPageMap.put("Details",detailsMap)
		detailDataMap.put("CoverPage", coverPageMap)
		int scriptCounter = 1
		List scriptList = []
		Map scriptNameSheetNameMap = [:]
		executionResultList.each{ executionResult ->
			def dataList = []
			Map dataMapList = [:]
			String scriptName = executionResult?.script
			String status = executionResult?.status
			def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
			def moduleName = sMap.get(scriptName)
			if(moduleName){
				ScriptFile script = ScriptFile.findByScriptName(scriptName)
				if(script){
					Map scriptContent = scriptService.getScript(realPath, script?.moduleName, script?.scriptName, "RDKV")
					Map testCaseDetails = scriptContent.get("testCaseDetails")
					def testCaseId = testCaseDetails.get("testCaseId")
					if(testCaseId != "" && testCaseId != null){
						Map toolDetailsMap = [:]
						Map profilingDetailsMap = [:]
						List toolNames = []
						List performanceList = Performance.findAllByExecutionResultAndPerformanceType(executionResult,GRAFANA_DATA)
						Map smemDetails = getSmemDetails(executionInstance,executionDevice,executionResult,realPath)
						Map pmapDetails = getPmapDetails(executionInstance,executionDevice,executionResult,realPath,appUrl)
						Map lmbenchDetails = getlmbenchDetails(executionInstance,executionDevice,executionResult,realPath,appUrl)
						Map systemdAnalyzeDetails = getsystemdAnalyzeDetails(executionInstance,executionDevice,executionResult,realPath,appUrl)
						Map systemdBootchartDetails = getsystemdBootchartDetails(executionInstance,executionDevice,executionResult,realPath,appUrl)
						Map alertMap = getAlertListFrom(executionResult,realPath);
						if(!performanceList.isEmpty() || !smemDetails.isEmpty() || !alertMap.isEmpty() || !pmapDetails.isEmpty() || !lmbenchDetails.isEmpty() || !systemdAnalyzeDetails.isEmpty() || !systemdBootchartDetails.isEmpty()){
							//For summary sheet
							Map scriptMap =["C1":scriptCounter,"C2":executionResult?.script,"C3":executionResult?.status,"C4":""]
							coverPageMap.put(executionResult?.script,scriptMap)
							scriptNameSheetNameMap.put(executionResult?.script,testCaseId)
							scriptCounter++
							//For profiling sheets
							String output = executionResult?.executionOutput
							String executionOutput
							if(output){
								executionOutput = output.replace(HTML_BR, NEW_LINE)
								if(executionOutput && executionOutput.length() > 10000){
									executionOutput = executionOutput.substring(0, 10000)
								}
							}
							def countOfExecutionOutput = executionOutput?.size()
							String executionLogData = executionOutput
							if(countOfExecutionOutput >= 1000 ){
								executionLogData = executionOutput+"\n More data use this link ....... \n " +appUrl+"/execution/getExecutionOutput?execResId="+executionResult?.id
							}
							Map scriptDetailsMap = ["C1":executionResult?.script,"C2":executionResult?.status,"C3":executionLogData]
							profilingDetailsMap.put("scriptDetails", scriptDetailsMap)
							if(!performanceList.isEmpty() || !alertMap.isEmpty()){
								Map parameterMap = [:]
								String performanceType = performanceList[0]?.performanceType
								String toolName = ""
								if(performanceType?.equals(GRAFANA_DATA)){
									toolName = "collectd"
								}
								toolNames.add(toolName)
								performanceList.each{ performance ->
									List metricList = []
									if(parameterMap.containsKey(performance?.processName)){
										metricList = parameterMap.get(performance?.processName)
									}
									Map metricMap = [:]
									metricMap.put("Metrics",performance?.processType )
									if(performance?.processValue1){
										def thresholdValue = Integer.parseInt(performance?.processValue1?.trim())
										metricMap.put("Threshold",thresholdValue )
									}else{
										metricMap.put("Threshold","NIL" )
									}
									String processValue = performance?.processValue
									List processValueList = processValue?.split(",")
									processValueList.each{ process ->
										def value = process?.split(":")[1]
										def valueDouble = Double.parseDouble(value)
										metricMap.put(process?.split(":")[0], valueDouble)
									}
									metricList.add(metricMap)
									parameterMap.put(performance?.processName, metricList)
								}
								parameterMap.put("AlertsReceived", alertMap)
								toolDetailsMap.put(toolName, parameterMap)
							}
							
							//for smem
							if(!smemDetails.isEmpty()){
								Map parameterMap = [:]
								String toolName = "smem"
								toolNames.add(toolName)
								toolDetailsMap.put(toolName, smemDetails)
							}
							//for pmap
							if(!pmapDetails.isEmpty()){
								Map parameterMap = [:]
								String toolName = "pmap"
								toolNames.add(toolName)
								toolDetailsMap.put(toolName, pmapDetails)
							}
							//for systemdAnalyze
							if(!systemdAnalyzeDetails.isEmpty()){
								Map parameterMap = [:]
								String toolName = "systemdAnalyze"
								toolNames.add(toolName)
								toolDetailsMap.put(toolName, systemdAnalyzeDetails)
							}
							// for systemdBootchart
							if(!systemdBootchartDetails.isEmpty()){
								Map parameterMap = [:]
								String toolName = "systemdBootchart"
								toolNames.add(toolName)
								toolDetailsMap.put(toolName, systemdBootchartDetails)
							}
							//for lmbench
							if(!lmbenchDetails.isEmpty()){
								Map parameterMap = [:]
								String toolName = "lmbench"
								toolNames.add(toolName)
								toolDetailsMap.put(toolName, lmbenchDetails)
							}
						}
						profilingDetailsMap.put("toolNames", toolNames)
						profilingDetailsMap.put("profilingData", toolDetailsMap)
						profilingDetailsMap.put("fieldsList", fieldList)
						detailDataMap.put(executionResult?.script, profilingDetailsMap)
					}
				}
			}
		}
		detailDataMap.put("scriptNameSheetNameMap", scriptNameSheetNameMap)
		return detailDataMap
	}
	
	/**
	 * Method to generate the data for creating the consolidated report for RDK service
	 * executions in excel format.
	 */
	def getDataForRDKServiceConsolidatedListExcelExport(Execution executionInstance, String realPath,String appUrl) {
		List executionResultList = []
		def detailDataMap = [:]
		def coverPageMap = [:]
		List fieldList = ["C1", "C2", "C3", "C4","C5","C6","C7","C8"]
		ExecutionDevice executionDevice  = ExecutionDevice.findByExecution(executionInstance)
		executionResultList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDevice)
		Map detailsMap = [:]
		String image = ""
		detailsMap.put("Device", executionDevice?.device)
		detailsMap.put("DeviceIP", executionDevice?.deviceIp)
		def executionTime = executionInstance?.realExecutionTime
		executionTime = executionTimeFormat (executionTime)
		detailsMap.put("Execution Time (min)", executionTime)
		image = "Image name not available"
		if(executionDevice?.buildName && !executionDevice?.buildName?.isEmpty() && !executionDevice?.buildName?.equals("Image name not available")){
			image = executionDevice?.buildName
		}else if(realPath && executionInstance?.id && executionDevice?.id){
			String imageNameFromVersionFile = getImageNameFromVersionFile(realPath,executionInstance?.id,executionDevice?.id)
			if(imageNameFromVersionFile != null && !imageNameFromVersionFile.isEmpty()){
				image = imageNameFromVersionFile
			}
		}
		detailsMap.put("Image", image)
		coverPageMap.put("Details",detailsMap)
		detailDataMap.put("CoverPage", coverPageMap)
		int counter = 1
		int totalCount = 0;
		int totalExecutedCount = 0;
		int totalSuccessCount = 0;
		int totalFailureCount = 0;
		int totalNaCount = 0;
		int totalTestCaseCount = 0;
		int totalTestCaseSuccessCount = 0;
		int totalTestCaseNaCount = 0;
		int rate = 0;
		int scriptCounter = 1
		int totalScriptCount = 0
		int totalScriptSuccessCount = 0
		int totalScriptFailureCount = 0
		int totalScriptNaCount = 0
		int totalScriptExecutedCount = 0
		def scriptList = []
		Map scriptMapList = [:]
		executionResultList.each{ executionResult ->
			def dataList = []
			def preRequisiteList = []
			def postRequisiteList = []
			Map dataMapList = [:]
			String executionResultOutput = executionResult?.executionOutput
			String scriptName = executionResult?.script
			def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
			def moduleName = sMap.get(scriptName)
			if(moduleName){
				if(executionResultOutput){
					if(executionResultOutput.contains("Test Execution Name is:") && executionResultOutput.contains("Connected to Server!") && executionResultOutput.contains("PLUGIN NAME :")) {
						String pluginNameSummary = StringUtils.substringBetween(executionResultOutput, "PLUGIN NAME :", "Final Plugin Tests Status:");
						String pluginName = StringUtils.substringBetween(executionResultOutput, "PLUGIN NAME :", "<br/>");
						pluginName = pluginName?.trim()?.toLowerCase()
						//For generating summary of plugin test cases in summary page
						if(pluginNameSummary){
							String totalTests = StringUtils.substringBetween(pluginNameSummary, "TOTAL TESTS    :", "<br/>");
							if(totalTests){
								totalTests = totalTests?.trim()
								totalCount = totalCount + totalTests?.toInteger()
							}else{
								totalTests = 0
							}
							String executedTests = StringUtils.substringBetween(pluginNameSummary, "EXECUTED TESTS :", "<br/>");
							if(executedTests){
								executedTests = executedTests?.trim()
								totalExecutedCount = totalExecutedCount + executedTests?.toInteger()
							}else{
								executedTests = 0
							}
							String passedTests = StringUtils.substringBetween(pluginNameSummary, "PASSED TESTS   :", "<br/>");
							if(passedTests){
								passedTests = passedTests?.trim()
								totalSuccessCount = totalSuccessCount + passedTests?.toInteger()
							}else{
								passedTests = 0
							}
							String failedTests = StringUtils.substringBetween(pluginNameSummary, "FAILED TESTS   :", "<br/>");
							if(failedTests){
								failedTests = failedTests?.trim()
								totalFailureCount = totalFailureCount + failedTests?.toInteger()
							}else{
								failedTests = 0
							}
							String naTests = StringUtils.substringBetween(pluginNameSummary, "N/A TESTS      :", "<br/>");
							if(naTests){
								naTests = naTests?.trim()
								totalNaCount = totalNaCount + naTests?.toInteger()
							}else{
								naTests = 0
							}
							def pluginMap = [:]
							pluginMap.put("Sl No", counter)
							pluginMap.put("Plugins", pluginName)
							pluginMap.put("Script Status", executionResult?.status)
							pluginMap.put("Total Test Case", totalTests?.toInteger())
							pluginMap.put("Executed", executedTests?.toInteger())
							pluginMap.put(Constants.SUCCESS_STATUS, passedTests?.toInteger())
							pluginMap.put(Constants.FAILURE_STATUS, failedTests?.toInteger())
							pluginMap.put(Constants.NOT_APPLICABLE_STATUS, naTests?.toInteger())
							coverPageMap.put(pluginName,pluginMap)
							counter++
						}else{
							int timeoutScriptTestCaseCount = 0
							int timeoutScriptTestCaseExecutedCount = 0
							int timeoutScriptTestCaseSuccessCount = 0
							int timeoutScriptTestCaseFailureCount = 0
							int timeoutScriptTestCaseNaCount = 0
							int timeoutScriptTestCaseDetailsPresentCount = 0
							String pluginTotalTestCase = StringUtils.substringBetween(executionResultOutput, "PLUGIN TOTAL TEST CASES:", "<br/>");
							if(pluginTotalTestCase){
								pluginTotalTestCase = pluginTotalTestCase?.trim()
								timeoutScriptTestCaseCount = pluginTotalTestCase?.toInteger()
								totalCount = totalCount + pluginTotalTestCase?.toInteger()
							}
							List testCaseNameList = StringUtils.substringsBetween(executionResultOutput, "TEST CASE NAME   :", "<br/>")
							if(testCaseNameList){
								testCaseNameList.each{ testCaseName ->
									testCaseName = testCaseName?.toString()?.trim()
									String testCaseDetails = StringUtils.substringBetween(executionResultOutput, testCaseName, "----------##")
									if(testCaseDetails){
										timeoutScriptTestCaseDetailsPresentCount++
										if(!pluginTotalTestCase){
											timeoutScriptTestCaseCount++
											totalCount++
										}
										String testCaseStatus = testCaseDetails.substring(testCaseDetails?.indexOf("[TEST EXECUTION STATUS] :") + 25 , testCaseDetails?.length());
										testCaseStatus = testCaseStatus?.trim()
										if(Constants.SUCCESS_STATUS.equals(testCaseStatus)){
											timeoutScriptTestCaseSuccessCount++
											totalSuccessCount++
										}else if(Constants.FAILURE_STATUS.equals(testCaseStatus)){
											timeoutScriptTestCaseFailureCount++
											totalFailureCount++
										}else if(Constants.NOT_APPLICABLE_STATUS.equals(testCaseStatus)){
											timeoutScriptTestCaseNaCount++
											totalNaCount++
										}
									}
								}
							}
							timeoutScriptTestCaseExecutedCount = timeoutScriptTestCaseDetailsPresentCount - timeoutScriptTestCaseNaCount
							totalExecutedCount = totalExecutedCount + timeoutScriptTestCaseExecutedCount
							def pluginMap = [:]
							pluginMap.put("Sl No", counter)
							pluginMap.put("Plugins", pluginName)
							pluginMap.put("Script Status", executionResult?.status)
							pluginMap.put("Total Test Case", timeoutScriptTestCaseCount)
							pluginMap.put("Executed", timeoutScriptTestCaseExecutedCount)
							pluginMap.put(Constants.SUCCESS_STATUS, timeoutScriptTestCaseSuccessCount)
							pluginMap.put(Constants.FAILURE_STATUS, timeoutScriptTestCaseFailureCount)
							pluginMap.put(Constants.NOT_APPLICABLE_STATUS, timeoutScriptTestCaseNaCount)
							coverPageMap.put(pluginName,pluginMap)
							counter++
						}
						//For getting plugin prerequisites
						int c2Counter = 1
						String preRequisiteBlock = StringUtils.substringBetween(executionResultOutput, "#---------------------------- Plugin Pre-requisite ----------------------------#", "Plugin Pre-requisite Status:")
						if(preRequisiteBlock){
							List preRequisiteNameList = StringUtils.substringsBetween(preRequisiteBlock, "Pre Requisite :", "<br/>")
							if(preRequisiteNameList){
								preRequisiteNameList.each{ preRequisiteName ->
									preRequisiteName = preRequisiteName?.toString()?.trim()
									String preRequisiteDetails = StringUtils.substringBetween(preRequisiteBlock, preRequisiteName, "----------#")
									if(preRequisiteDetails){
										String preRequisiteStatus = preRequisiteDetails.substring(preRequisiteDetails?.indexOf("[Pre-requisite Status] :") + 25 , preRequisiteDetails?.length());
										String preRequisiteOutput = preRequisiteDetails?.replace(HTML_BR, NEW_LINE)
										Map preRequisiteMap =["C1":c2Counter,"C2":preRequisiteName,"C3":preRequisiteStatus,"C4":parseTime(executionResult?.dateOfExecution),"C5":preRequisiteOutput,"C6":"","C7":"","C8":""]
										preRequisiteList.add(preRequisiteMap)
										c2Counter++
									}
								}
							}
						}
						
						//For getting the test cases of each plugin
						List testCaseNameList = StringUtils.substringsBetween(executionResultOutput, "TEST CASE NAME   :", "<br/>")
						int c1Counter = 1
						if(testCaseNameList){
							testCaseNameList.each{ testCaseName ->
								totalTestCaseCount++
								testCaseName = testCaseName?.toString()?.trim()
								String testCaseDetails = StringUtils.substringBetween(executionResultOutput, testCaseName, "----------##")
								if(testCaseDetails){
									String testCaseStatus = testCaseDetails.substring(testCaseDetails?.indexOf("[TEST EXECUTION STATUS] :") + 25 , testCaseDetails?.length());
									testCaseStatus = testCaseStatus?.trim()
									if(Constants.SUCCESS_STATUS.equals(testCaseStatus)){
										totalTestCaseSuccessCount++
									}else if(Constants.NOT_APPLICABLE_STATUS.equals(testCaseStatus)){
										totalTestCaseNaCount++
									}
									String testCaseOutput = testCaseDetails?.replace(HTML_BR, NEW_LINE)
									Map dataMap =["C1":c1Counter,"C2":testCaseName,"C3":testCaseStatus,"C4":parseTime(executionResult?.dateOfExecution),"C5":testCaseOutput,"C6":"","C7":"","C8":""]
									dataList.add(dataMap)
									c1Counter++
								}
							}
						}	
						//For getting plugin post-requisites
						int c3Counter = 1
						String postRequisiteBlock = StringUtils.substringBetween(executionResultOutput, "#---------------------------- Plugin Post-requisite ----------------------------#", "Plugin Post-requisite Status:")
						if(postRequisiteBlock){
							List postRequisiteNameList = StringUtils.substringsBetween(postRequisiteBlock, "Post Requisite :", "<br/>")
							if(postRequisiteNameList){
								postRequisiteNameList.each{ postRequisiteName ->
									postRequisiteName = postRequisiteName?.toString()?.trim()
									String postRequisiteDetails = StringUtils.substringBetween(postRequisiteBlock, postRequisiteName, "----------#")
									if(postRequisiteDetails){
										String postRequisiteStatus = postRequisiteDetails.substring(postRequisiteDetails?.indexOf("[Post-requisite Status] :") + 26 , postRequisiteDetails?.length());
										String postRequisiteOutput = postRequisiteDetails?.replace(HTML_BR, NEW_LINE)
										Map postRequisiteMap =["C1":c3Counter,"C2":postRequisiteName,"C3":postRequisiteStatus,"C4":parseTime(executionResult?.dateOfExecution),"C5":postRequisiteOutput,"C6":"","C7":"","C8":""]
										postRequisiteList.add(postRequisiteMap)
										c3Counter++
									}
								}
							}
						}
						dataMapList.put("dataList",dataList)
						dataMapList.put("preRequisiteList",preRequisiteList)
						dataMapList.put("postRequisiteList",postRequisiteList)
						String logLink = appUrl+"/execution/getExecutionOutput?execResId="+executionResult?.id
						dataMapList.put("logLink",logLink)
						dataMapList.put("fieldsList",fieldList)
						detailDataMap.put(pluginName,dataMapList)
					}else{
						String output = executionResult?.executionOutput
						String scriptStatus = executionResult?.status
						totalScriptCount ++
						if(Constants.SUCCESS_STATUS.equals(scriptStatus)){
							totalScriptSuccessCount++
						}else if(Constants.FAILURE_STATUS.equals(scriptStatus)){
							totalScriptFailureCount++
						}else if(Constants.NOT_APPLICABLE_STATUS.equals(scriptStatus)){
							totalScriptNaCount++
						}
						String executionOutput
						if(output){
							executionOutput = output.replace(HTML_BR, NEW_LINE)
							if(executionOutput && executionOutput.length() > 10000){
								executionOutput = executionOutput.substring(0, 10000)
							}
						}
						def countOfExecutionOutput = executionOutput?.size()
						String executionLogData = executionOutput
						if(countOfExecutionOutput >= 1000 ){
							executionLogData = executionOutput+"\n More data use this link ....... \n " +appUrl+"/execution/getExecutionOutput?execResId="+executionResult?.id
						}
						Map scriptMap =["C1":scriptCounter,"C2":executionResult?.script,"C3":executionResult?.status,"C4":parseTime(executionResult?.dateOfExecution),"C5":executionLogData,"C6":"","C7":"","C8":""]
						scriptList.add(scriptMap)
						scriptCounter++
					}
				}
			}
		}
		if(!scriptList.isEmpty()){
			def pluginMap = [:]
			totalScriptExecutedCount = totalScriptCount - totalScriptNaCount
			pluginMap.put("Sl No", counter)
			pluginMap.put("Plugins", "rdkservices")
			pluginMap.put("Script Status", "FAILURE")
			pluginMap.put("Total Test Case", totalScriptCount)
			pluginMap.put("Executed", totalScriptExecutedCount)
			pluginMap.put(Constants.SUCCESS_STATUS, totalScriptSuccessCount)
			pluginMap.put(Constants.FAILURE_STATUS, totalScriptFailureCount)
			pluginMap.put(Constants.NOT_APPLICABLE_STATUS, totalScriptNaCount)
			coverPageMap.put("rdkservices",pluginMap)
			counter++
		}
		scriptMapList.put("fieldsList",fieldList)
		scriptMapList.put("rdkserviceScripts",scriptList)
		detailDataMap.put("rdkservices",scriptMapList)
		if(totalTestCaseCount!=totalTestCaseNaCount){
			rate =totalTestCaseSuccessCount*100/(totalTestCaseCount-totalTestCaseNaCount)
		}
		Map totalMap = [:]
		totalMap.put("Sl No", "")
		totalMap.put("Plugins", "Total")
		totalMap.put("Script Status", "")
		totalMap.put("Total Test Case", totalCount + totalScriptCount)
		totalMap.put("Executed", totalExecutedCount + totalScriptExecutedCount)
		totalMap.put(Constants.SUCCESS_STATUS, totalSuccessCount + totalScriptSuccessCount)
		totalMap.put(Constants.FAILURE_STATUS, totalFailureCount + totalScriptFailureCount)
		totalMap.put(Constants.NOT_APPLICABLE_STATUS, totalNaCount + totalScriptNaCount)
		coverPageMap.put("Total",totalMap)
		coverPageMap.put(Constants.OVERALL_PASS_RATE, rate)
		return detailDataMap
	}
	/**
	 * Method to get the data for creating the consolidated report in excel format.
	 */
	def getDataForConsolidatedListExcelExport(Execution executionInstance, String realPath,String appUrl) {
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		List executionDeviceList = []
		List executionResultInstanceList = []
		List columnWidthList = []
		columnWidthList = [0.1, 0.3, 0.1, 0.4]
		
		String deviceDetails

		String fileContents = ""
		def deviceName = ""
		def deviceIp = ""
		def executionTime = ""
		int totalCount = 0
		int testCount =0

		String filePath = ""
		def executionDeviceId

		Map summaryHead = [:]
		Map statusValue = [:]
		List fieldList = ["C1", "C2", "C3", "C4", "C5","C6","C7","C8","C9","C10"]

		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def detailDataMap = [:]
		def analysisSummaryMap = getDefectAnalysisDetails(executionInstance)
		executionDeviceList.each{ executionDeviceInstance ->

			deviceName = executionDeviceInstance?.device
			deviceIp = executionDeviceInstance?.deviceIp
			executionTime = executionDeviceInstance?.executionTime
			executionTime = executionTimeFormat ( executionTime )
			executionDeviceId = executionDeviceInstance?.id
			filePath = "${realPathFromFile}//logs//version//${executionInstance?.id}//${executionDeviceId?.toString()}//${executionDeviceId?.toString()}_version.txt"
			if(filePath){
				File file = new File(filePath)
				if(file.exists()){
					file.eachLine { line ->
						if(!(line.isEmpty())){
							if(!(line.startsWith( LINE_STRING ))){
								fileContents = fileContents + line + HTML_BR
							}
						}
					}
					deviceDetails = fileContents.replace(HTML_BR, NEW_LINE)
				}
			}
			Map coverPageMap = [:]
			detailDataMap.put("CoverPage", coverPageMap)
			Map detailsMap = [:]
			coverPageMap.put("Details",detailsMap)
			detailsMap.put("Device", deviceName)
			detailsMap.put("DeviceIP", deviceIp)
			detailsMap.put("Execution Time (min)", executionTime)
			try {
				String image = "Not Available"
				if(deviceDetails != null && deviceDetails.contains("imagename:")){
					String imagename = "imagename:"
					int indx = deviceDetails.indexOf(imagename)
					int endIndx = deviceDetails.indexOf("\n",indx)
					if(indx >=0 && endIndx > 0){
						indx = indx + imagename.length()
						image = deviceDetails.substring(indx, endIndx)
					}
				}
				detailsMap.put("Image", image)
			} catch (Exception e) {
				e.printStackTrace()
			}
			
		

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)//,[sort: "script",order: "asc"])
			def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionResultInstanceList?.size()?.toString())
			
			int counter = 1
			int counter1=1
			Date date = new Date()
			executionResultInstanceList.each{ executionResultInstance ->
				counter1= counter1+1
			
				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String output = executionResultInstance?.executionOutput
				String executionOutput
				String moduleName = ""
				String tabName = ""
				String ticketNo = ""
				String remarks = ""
				String issueType = ""
				DefectDetails defectDetails = DefectDetails.findByExecutionIdAndScriptName(executionInstance?.id, scriptName)
				if(defectDetails != null)  {
					ticketNo = defectDetails.ticketNumber
					remarks = defectDetails.remarks
					issueType = defectDetails.defectType
				}
//				int  execution = executionResultInstance?.script?.count
//				Script.withTransaction {
//					Script scrpt = Script.findByName(scriptName)
//					moduleName = scrpt?.primitiveTest?.module?.name
				
//				}
				
				if(executionResultInstance?.category != Category.RDKB_TCL && executionResultInstance?.category != Category.RDKV_THUNDER){
					def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
					moduleName = sMap.get(scriptName)
				}
				else if(executionResultInstance?.category == Category.RDKB_TCL){
					moduleName = 'tcl'
				}
				else if(executionResultInstance?.category == Category.RDKV_THUNDER){
					moduleName = Constants.THUNDER
					def sMap = scriptService.getScriptNameTabNameMappingThunder(realPath)
					tabName = sMap.get(scriptName)
				}
				
				int i = 0
				
				if(!moduleName.equals("")){	
		//			def scriptObj1 = ScriptFile.findByModuleName(moduleName)
	
					def scriptObj = ScriptFile.findByScriptNameAndModuleName(scriptName,moduleName)
					if(scriptObj){
						def dataList
						Map dataMapList
						if(moduleName == Constants.THUNDER){
							if(tabName!=null){
								dataMapList = detailDataMap.get(tabName)
							}
						}else{
						    dataMapList = detailDataMap.get(moduleName)
						}
							if(dataMapList == null){
								dataMapList = [:]
								if(moduleName == Constants.THUNDER){
									if(tabName!=null){
										detailDataMap.put(tabName,dataMapList)
									}
								}else{
								    detailDataMap.put(moduleName,dataMapList)
								}
								//detailDataMap.put("total", summaryMap.get("Total Scripts"))
							}				
						
						if(dataMapList != null){
							dataList = dataMapList.get("dataList")
							if(dataList == null){
								dataList = []
								dataMapList.put("dataList",dataList)
								dataMapList.put("fieldsList",fieldList)
								counter = 1
						}else{
							counter =  dataMapList.get("counter")
						}
						if(dataList != null){
							if(output){
								executionOutput = output.replace(HTML_BR, NEW_LINE)
								if(executionOutput && executionOutput.length() > 10000){
									executionOutput = executionOutput.substring(0, 10000)
								}
							}
								
							String executed
							if( "PENDING".equals(status)){
								executed = "NO"
							}			
							else{
								executed = "YES"
							}
							/*Map dataMap = ["C1":counter,"C2":scriptName,"C3":status,"C4":executionOutput,"C5":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id,,"C6":parseTime(executionInstance?.dateOfExecution)] 						
							Map dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":parseTime(executionInstance?.dateOfExecution),"C6":appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id,"C7":"","C8":"","C9":"","C10":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]*/
							Map dataMap
							def countOfExecutionOutput = executionOutput?.size()
							//For CGRTS-521 
							String executionLogData = executionOutput
							if(countOfExecutionOutput >= 1000 ){
								executionLogData = executionOutput+"\n More data use this link ....... \n " +appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id
							}
							
							dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":parseTime(executionInstance?.dateOfExecution),"C6":executionLogData,"C7":ticketNo,"C8":issueType,"C9":remarks,"C10":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]
							
							dataList.add(dataMap)
							counter ++
							dataMapList.put("counter",counter)
						}
					}
				}
			}
		}
	}			
		prepareStatusList(detailDataMap, analysisSummaryMap)
		return detailDataMap
	}
	
	/**
	 * Method to parse the time show in execution date in consolidated report.
	 */
	def parseTime(Date date){
		String dateString = ""
		try {
			SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy")
			dateString = sdf.format(date)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return dateString
	}

	/**
	 * Method to populate status list to show in cover page of consolidated report.
	 */
	def prepareStatusList(Map detailDataMap, Map defectDetailsMap){
		try{
		    Set keySet = detailDataMap.keySet();
		    int counter = 1
		    int totalScripts = 0
		    int tSuccess = 0
		    int tFailure = 0
		    int tNa = 0
		    int tSkip = 0
		    int tTimeOut =0
		    int scriptCount = 0;
		    int totalScript = 0
		    int tRate = 0;
		
		    boolean isAnalyzed = false
		    def totalAnalyzedDetailsCount = defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.getAt(ANALYZED)
		    if(totalAnalyzedDetailsCount > 0) {
			    isAnalyzed = true
		    }
		
		    keySet.each { key ->
			    if(!key.equals("CoverPage")){	
				    int success = 0
				    int failure = 0
				    int na = 0
				    int skip = 0
				    int total = 0
				    int timeOut = 0
			
				    Map dataMap = detailDataMap.get(key)
				    List dataList = dataMap.get("dataList")
				    dataList.each { dMap ->
					    if(!dMap.get("C4").equals("PENDING")){
						    total ++
					    }
					
					    if(dMap.get("C4").equals(Constants.SUCCESS_STATUS)){
						    success ++
					    }else if(dMap.get("C4").equals(Constants.FAILURE_STATUS)){
						    failure ++
					    }else if(dMap.get("C4").equals(Constants.NOT_APPLICABLE_STATUS)){
						    na ++
					    }else if(dMap.get("C4").equals(Constants.SKIPPED_STATUS)){
						    skip ++
					    }else if(dMap.get("C4").equals("SCRIPT TIME OUT")){
						    timeOut ++
					    }
					//scriptCount = Integer.parseInt(dMap.get("total"))
					//scriptCount =dMap.get("total")
				    }
				    Map coverPageMap = detailDataMap.get("CoverPage")
				    Map resultMap = [:]
				    resultMap.put("Sl No", counter)
				    resultMap.put("Module", key)
				    //resultMap.put("Total",	scriptCount)
				    resultMap.put("Executed", total)
				    resultMap.put(Constants.SUCCESS_STATUS, success)
				    resultMap.put(Constants.FAILURE_STATUS, failure)
				    resultMap.put("SCRIPT TIME OUT", timeOut)
				    resultMap.put(Constants.NOT_APPLICABLE_STATUS, na)
				    resultMap.put(Constants.SKIPPED_STATUS, skip)
				 
				    if(isAnalyzed) {

					    def rdkIssueCount = defectDetailsMap?.get(MODULE_DATA)?.get(key)?.get(RDK_ISSUE)
					    def newIssueCount = defectDetailsMap?.get(MODULE_DATA)?.get(key)?.get(NEW_ISSUE)
					    def scriptIssueCount =  defectDetailsMap?.get(MODULE_DATA)?.get(key)?.get(SCRIPT_ISSUE)
					    def envIssueCount = defectDetailsMap?.get(MODULE_DATA)?.get(key)?.get(ENVIRONMENT_ISSUE)
					    def interfaceChangeCount = defectDetailsMap?.get(MODULE_DATA)?.get(key)?.get(INTERFACE_CHANGE)
					    if(!newIssueCount) {newIssueCount = 0}
					    if(!rdkIssueCount) {rdkIssueCount = 0}
					    def existingIssueCount = rdkIssueCount - newIssueCount
					    resultMap.put("Number of failed scripts linked with open defects", rdkIssueCount)
					    resultMap.put(SCRIPT_ISSUE, scriptIssueCount?scriptIssueCount:0)
					    resultMap.put("Existing Issue", existingIssueCount)
					    resultMap.put(NEW_ISSUE, newIssueCount)
					    resultMap.put(ENVIRONMENT_ISSUE, envIssueCount? envIssueCount: 0)
					    resultMap.put(INTERFACE_CHANGE, interfaceChangeCount? interfaceChangeCount : 0)
					    resultMap.put("Remarks","")
				    }
				    coverPageMap.put(key, resultMap)
				    counter ++

				    tSuccess += success
				    tFailure += failure
				    tNa += na
				    tSkip += skip
				    totalScripts += total
				    tTimeOut += timeOut
				    //totalScript +=scriptCount
			    }
		    }
		    //scriptCount=Integer.parseInt(resultMap.getAt("total"))
		    Map coverPageMap = detailDataMap.get("CoverPage")
		    Map resultMap = [:]
		
		    resultMap.put("Sl No", "")
		    resultMap.put("Module", "Total")
		    //resultMap.put("Total", 	totalScript)
		    resultMap.put("Executed", totalScripts)
		    resultMap.put(Constants.SUCCESS_STATUS, tSuccess)
		    resultMap.put(Constants.FAILURE_STATUS, tFailure)
		    resultMap.put("SCRIPT TIME OUT", tTimeOut)
		    resultMap.put(Constants.NOT_APPLICABLE_STATUS, tNa)
		    resultMap.put(Constants.SKIPPED_STATUS, tSkip)
		    if((totalScripts - tNa) != 0){
			    tRate = ((tSuccess * 100)/(totalScripts - tNa))
		    }
		
		    if(isAnalyzed) {
			    resultMap.put("Number of failed scripts linked with open defects", defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.get(RDK_ISSUE))
			    resultMap.put(SCRIPT_ISSUE, defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.get(SCRIPT_ISSUE))
			    def existingIssueCount = defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.get(RDK_ISSUE) - defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.get(NEW_ISSUE)
			    resultMap.put("Existing Issue", existingIssueCount)
			    resultMap.put(NEW_ISSUE, defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.get(NEW_ISSUE))
			    resultMap.put(ENVIRONMENT_ISSUE, defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.get(ENVIRONMENT_ISSUE))
			    resultMap.put(INTERFACE_CHANGE, defectDetailsMap?.get(TOTAL_ANALYZED_DATA)?.get(INTERFACE_CHANGE))
			    resultMap.put("Remarks","")
		    }

		    //resultMap.put("New Issue","")
		    //resultMap.put("Environment Issue", "")
		    //resultMap.put("Interface Change","")
	    
		
		    coverPageMap.put("Total", resultMap)
		    coverPageMap.put(Constants.OVERALL_PASS_RATE, tRate)
		    }catch(Exception e){
		        e.printStackTrace()
		    }
	    }
	/**
	 * Function to populate performance data in db if the data is available only as files
	 * @param executionInstance
	 * @param realPath
	 * @return
	 */
	def populateChartData(final Execution executionInstance,final String realPath){
		//	if(!executionInstance?.isPerformanceDone){
		executionService.setPerformance(executionInstance,realPath)
		//	}
	}

	/**
	 * Get the execution status summary of script executed from the results.
	 * @param executionInstance
	 * @param executionDevice
	 * @param scriptCnt
	 * @return
	 */
	def Map getStatusList(final Execution executionInstance, final ExecutionDevice executionDevice, final String scriptCnt){

		def listStatusCount = [:]
		int scriptCount = 0

		if(executionInstance?.scriptGroup || executionInstance?.script.toString().equals("Multiple Scripts") || executionInstance?.scriptGroup.toString().equals("Multiple Scriptgroups")){
			ScriptGroup scriptGrp = null
			if(executionInstance?.scriptGroup!=null && executionInstance?.scriptGroup!="Multiple Scriptgroups"){
				scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
			}
			if(scriptGrp || executionInstance?.script.toString().equals("Multiple Scripts") || executionInstance?.scriptGroup.toString().equals("Multiple Scriptgroups")){

				def successCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SUCCESS")

				def failureCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"FAILURE")

				def skippedCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SKIPPED")

				def naCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"N/A")

				def pendingCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"PENDING")

				def unknownCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"UNDEFINED")

				def timeoutCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SCRIPT TIME OUT")

				if((executionInstance?.scriptCount != 0 ) && (executionInstance?.scriptCount != null)){
					scriptCount = executionInstance?.scriptCount
				}
				else{
					scriptCount = Integer.parseInt(scriptCnt)
				}
				if(executionInstance?.name.toString().contains("_RERUN_")){
					scriptCount = Integer.parseInt(scriptCnt)
				}
				def executedCount = ExecutionResult.countByExecutionDevice(executionDevice)
				executedCount = executedCount - pendingCount 
				
				listStatusCount.put("Total Scripts",scriptCount?.toString())
				listStatusCount.put("Executed",""+executedCount?.toString())
				listStatusCount.put("SUCCESS",successCount?.toString())
				listStatusCount.put("FAILURE",failureCount?.toString())
				listStatusCount.put("N/A",naCount?.toString())
				listStatusCount.put("SKIPPED",skippedCount?.toString())
				listStatusCount.put("PENDING",pendingCount?.toString())
				listStatusCount.put("TIMED OUT",timeoutCount?.toString())
				listStatusCount.put("UNDEFINED",unknownCount?.toString())
			}
		}
		return listStatusCount
	}
	
	/**
	 * Method to populate total, module wise and detailed defect analysis details.
	 */
	def Map getDefectAnalysisDetails(final Execution executionInstance) {
		def defectDetails = DefectDetails.findAllByExecutionId(executionInstance?.id)
		def defectData = [:]
		def moduleData = [:]
		def totalAnalyzedData = [:]
		totalAnalyzedData[RDK_ISSUE] = 0
		totalAnalyzedData[SCRIPT_ISSUE] = 0
		totalAnalyzedData[ENVIRONMENT_ISSUE] = 0
		totalAnalyzedData[NEW_ISSUE] = 0
		totalAnalyzedData[INTERFACE_CHANGE] = 0
		totalAnalyzedData[ANALYZED] = 0
		
		defectDetails?.each {  defectDetail ->
			defectData.put(defectDetail.scriptName, defectDetail.ticketNumber)
			def scriptFile = ScriptFile.findByScriptName(defectDetail.scriptName)
			if(scriptFile != null) {
				def moduleName = scriptFile.moduleName
				if (moduleData[moduleName] == null) {
					moduleData[moduleName] = [:]
				}
				if(defectDetail.defectType.equals(RDK_ISSUE)) {
					def existingCount =  moduleData[moduleName].get(RDK_ISSUE)
					existingCount = existingCount != null ? existingCount : 0
					moduleData[moduleName].put(RDK_ISSUE, (existingCount +1))
					totalAnalyzedData[RDK_ISSUE] = totalAnalyzedData[RDK_ISSUE] + 1
					if(defectDetail.remarks.contains(NEW_ISSUE)) {
						def existingNewIssueCount =  moduleData[moduleName].get(NEW_ISSUE)
						existingNewIssueCount = existingNewIssueCount != null ? existingNewIssueCount : 0
						moduleData[moduleName].put(NEW_ISSUE, (existingNewIssueCount +1))
						totalAnalyzedData[NEW_ISSUE] = totalAnalyzedData[NEW_ISSUE] + 1
					}
				} else if(defectDetail.defectType.equals(SCRIPT_ISSUE)) {
					def existingCount =  moduleData[moduleName].get(SCRIPT_ISSUE)
					existingCount = existingCount != null ? existingCount : 0
					moduleData[moduleName].put(SCRIPT_ISSUE, (existingCount +1))
					totalAnalyzedData[SCRIPT_ISSUE] = totalAnalyzedData[SCRIPT_ISSUE] + 1
				} else if(defectDetail.defectType.equals(ENVIRONMENT_ISSUE)) {
					def existingCount =  moduleData[moduleName].get(ENVIRONMENT_ISSUE)
					existingCount = existingCount != null ? existingCount : 0
					moduleData[moduleName].put(ENVIRONMENT_ISSUE, (existingCount +1))
					totalAnalyzedData[ENVIRONMENT_ISSUE] = totalAnalyzedData[ENVIRONMENT_ISSUE] + 1
				} else if(defectDetail.defectType.equals(INTERFACE_CHANGE)) {
					def existingCount =  moduleData[moduleName].get(INTERFACE_CHANGE)
					existingCount = existingCount != null ? existingCount : 0
					moduleData[moduleName].put(INTERFACE_CHANGE, (existingCount +1))
					totalAnalyzedData[INTERFACE_CHANGE] =  totalAnalyzedData[INTERFACE_CHANGE] + 1
				}
				
				def existingAnalyzedCount =  moduleData[moduleName].get(ANALYZED)
				existingAnalyzedCount = existingAnalyzedCount != null ? existingAnalyzedCount : 0
				moduleData[moduleName].put(ANALYZED, (existingAnalyzedCount +1))
				totalAnalyzedData[ANALYZED] = totalAnalyzedData[ANALYZED]  + 1
			}
		}
		[totalAnalyzedData :totalAnalyzedData, moduleData :moduleData , defectData : defectData]
	}

	def Map getDetailedStatusList(final Execution executionInstance, final ExecutionDevice executionDevice, final String scriptCnt,String realPath){
		def dataMap = prepareDetailMap(executionInstance, KEY_GATEWAYIP)
				def listStatusCount = [:]
				int scriptCount = 0
		
				if(executionInstance?.scriptGroup){
					ScriptGroup scriptGrp = ScriptGroup.findByName(executionInstance?.scriptGroup)
					if(scriptGrp){
		
						def successCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SUCCESS")
		
						def failureCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"FAILURE")
		
						def skippedCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SKIPPED")
		
						def naCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"N/A")
		
						def pendingCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"PENDING")
		
						def unknownCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"UNDEFINED")
		
						def timeoutCount = ExecutionResult.countByExecutionDeviceAndStatus(executionDevice,"SCRIPT TIME OUT")
		
						if((executionInstance?.scriptCount != 0 ) && (executionInstance?.scriptCount != null)){
							scriptCount = executionInstance?.scriptCount
						}
						else{
							scriptCount = Integer.parseInt(scriptCnt)
						}
		
						def executedCount = ExecutionResult.countByExecutionDevice(executionDevice)
						executedCount = executedCount - pendingCount
						
						listStatusCount.put("Total Scripts",scriptCount?.toString())
						listStatusCount.put("Executed",""+executedCount?.toString())
						listStatusCount.put("SUCCESS",successCount?.toString())
						listStatusCount.put("FAILURE",failureCount?.toString())
						listStatusCount.put("N/A",naCount?.toString())
						listStatusCount.put("SKIPPED",skippedCount?.toString())
						listStatusCount.put("PENDING",pendingCount?.toString())
						listStatusCount.put("TIMED OUT",timeoutCount?.toString())
						listStatusCount.put("UNDEFINED",unknownCount?.toString())
					}
				}
				return listStatusCount
			}
	
	def prepareDetailMap(def executionInstance,def realPath){
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def detailDataMap = [:]
		def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
		executionDeviceList.each{ executionDeviceInstance ->
			def executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)
			executionResultInstanceList.each{ executionResultInstance ->
				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				Category category = executionResultInstance?.category 
				if(category == Category.RDKV_THUNDER){
					def moduleName = Constants.THUNDER
					if(moduleName && !moduleName.equals("null") && !moduleName.equals("")){
						def moduleMap = detailDataMap.get(moduleName)
						if(!moduleMap){
							moduleMap = [:]
							detailDataMap.put(moduleName,moduleMap)
						}
						def statusCounter = moduleMap.get(status)
						if(!statusCounter){
							statusCounter = 0
						}
						statusCounter ++
						moduleMap.put(status, statusCounter)
					}
				}
				else if(category != Category.RDKB_TCL){
					def moduleName = sMap.get(scriptName)
					
					if(moduleName && !moduleName.equals("null") && !moduleName.equals("")){
						
						def moduleMap = detailDataMap.get(moduleName)
						if(!moduleMap){
							moduleMap = [:]
							detailDataMap.put(moduleName,moduleMap)
						}
						def statusCounter = moduleMap.get(status)
						if(!statusCounter){
							statusCounter = 0
						}
						statusCounter ++
						moduleMap.put(status, statusCounter)
					}
				}
				else{
					def moduleName = 'tcl'
					
					if(moduleName && !moduleName.equals("null") && !moduleName.equals("")){
						
						def moduleMap = detailDataMap.get(moduleName)
						if(!moduleMap){
							moduleMap = [:]
							detailDataMap.put(moduleName,moduleMap)
						}
						def statusCounter = moduleMap.get(status)
						if(!statusCounter){
							statusCounter = 0
						}
						statusCounter ++
						moduleMap.put(status, statusCounter)
					}
				}
				
			}
		}
		
		
		TreeMap<String, Map> tMap = new TreeMap<String, Map>(detailDataMap)
		return tMap
	}

	/**
	 * Method to get the data for creating the consolidated report in excel format.
	 */
	def getDataForConsolidatedListPerformanceExcelExport(Execution executionInstance, String realPath,String appUrl) {
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		List executionDeviceList = []
		List executionResultInstanceList = []
		List columnWidthList = []
		columnWidthList = [0.1, 0.3, 0.1, 0.4]
		
		String deviceDetails

		String fileContents = ""
		def deviceName = ""
		def deviceIp = ""
		def executionTime = ""
		int totalCount = 0
		int testCount =0

		String filePath = ""
		def executionDeviceId

		Map summaryHead = [:]
		Map statusValue = [:]
		List fieldList = ["C1", "C2", "C3", "C4", "C5","C6","C7","C8","C9","C10","C11"]


		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def defectDetailsMap = getDefectAnalysisDetails(executionInstance)
		def detailDataMap = [:]
		executionDeviceList.each{ executionDeviceInstance ->

			deviceName = executionDeviceInstance?.device
			deviceIp = executionDeviceInstance?.deviceIp
			executionTime = executionDeviceInstance?.executionTime
			executionTime = executionTimeFormat ( executionTime )
			executionDeviceId = executionDeviceInstance?.id
			filePath = "${realPathFromFile}//logs//version//${executionInstance?.id}//${executionDeviceId?.toString()}//${executionDeviceId?.toString()}_version.txt"
			if(filePath){
				File file = new File(filePath)
				if(file.exists()){
					file.eachLine { line ->
						if(!(line.isEmpty())){
							if(!(line.startsWith( LINE_STRING ))){
								fileContents = fileContents + line + HTML_BR
							}
						}
					}
					deviceDetails = fileContents.replace(HTML_BR, NEW_LINE)
				}
				else{
					//println "No version file found"
				}
			}
			else{
				//println "Invalid file path"
			}

			Map coverPageMap = [:]
			detailDataMap.put("CoverPage", coverPageMap)
			Map detailsMap = [:]
			coverPageMap.put("Details",detailsMap)
			detailsMap.put("Device", deviceName)
			detailsMap.put("DeviceIP", deviceIp)
			detailsMap.put("Execution Time (min)", executionTime)
			try {
				String image = "Not Available"
				if(deviceDetails != null && deviceDetails.contains("imagename:")){
					String imagename = "imagename:"
					int indx = deviceDetails.indexOf(imagename)
					int endIndx = deviceDetails.indexOf("\n",indx)
					if(indx >=0 && endIndx > 0){
						indx = indx + imagename.length()
						image = deviceDetails.substring(indx, endIndx)
					}
				}
				detailsMap.put("Image", image)
			} catch (Exception e) {
				e.printStackTrace()
			}
			
		

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)//,[sort: "script",order: "asc"])
			def summaryMap = getStatusList(executionInstance,executionDeviceInstance,executionResultInstanceList?.size()?.toString())
			
			int counter = 1
			int counter1=1
			Date date = new Date()
			executionResultInstanceList.each{ executionResultInstance ->
				counter1= counter1+1
			
				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String output = executionResultInstance?.executionOutput
				String executionOutput
				String moduleName = ""
//				int  execution = executionResultInstance?.script?.count
//				Script.withTransaction {
//					Script scrpt = Script.findByName(scriptName)
//					moduleName = scrpt?.primitiveTest?.module?.name
				
//				}
				
				
				if(executionResultInstance?.category != Category.RDKB_TCL){
					def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
					moduleName = sMap.get(scriptName)
				}else{
					moduleName = "tcl"
				}
				
				int i = 0
				
				if(!moduleName.equals("")){
		//			def scriptObj1 = ScriptFile.findByModuleName(moduleName)
		
	
					def scriptObj = ScriptFile.findByScriptNameAndModuleName(scriptName,moduleName)
					if(scriptObj){
						def dataList
						Map dataMapList = detailDataMap.get(moduleName)
							if(dataMapList == null){
								dataMapList = [:]
								detailDataMap.put(moduleName,dataMapList)
								//detailDataMap.put("total", summaryMap.get("Total Scripts"))
							}
						
						if(dataMapList != null){
							dataList = dataMapList.get("dataList")
							if(dataList == null){
								dataList = []
								dataMapList.put("dataList",dataList)
								dataMapList.put("fieldsList",fieldList)
								counter = 1
						}else{
							counter =  dataMapList.get("counter")
						}
						if(dataList != null){
							
							if(output){
								executionOutput = output.replace(HTML_BR, NEW_LINE)
								if(executionOutput && executionOutput.length() > 10000){
									executionOutput = executionOutput.substring(0, 10000)
								}
							}
								
							String executed
							if( "PENDING".equals(status)){
								executed = "NO"
							}
							else{
								executed = "YES"
							}
							/*Map dataMap = ["C1":counter,"C2":scriptName,"C3":status,"C4":executionOutput,"C5":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id,,"C6":parseTime(executionInstance?.dateOfExecution)]
							Map dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":parseTime(executionInstance?.dateOfExecution),"C6":appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id,"C7":"","C8":"","C9":"","C10":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]*/
							Map dataMap
							def countOfExecutionOutput = executionOutput?.size()
							//For CGRTS-521
							String executionLogData = executionOutput
							if(countOfExecutionOutput >= 1000 ){
								executionLogData = executionOutput+"\n To view full log use this link ....... \r\n  " +appUrl+"/execution/getExecutionOutput?execResId="+executionResultInstance?.id
							}
							
							String exeTime = executionResultInstance?.executionTime
							String realExeTime = executionResultInstance?.totalExecutionTime
							float time1 = 0.0
							float time2 = 0.0
							 try {
								 time1 = Float.parseFloat(exeTime)
								 time1 = time1?.round(2)
								 time2 = Float.parseFloat(realExeTime)
								 time2 = time2?.round(2)
							} catch (Exception e) {
							}
							
							dataMap =["C1":counter,"C2":scriptName,"C3":executed,"C4":status,"C5":time1,"C6":parseTime(executionInstance?.dateOfExecution),"C7":executionLogData,"C8":"","C9":"","C10":"","C11":appUrl+"/execution/getAgentConsoleLog?execResId="+executionResultInstance?.id]
							
							dataList.add(dataMap)
							counter ++
							dataMapList.put("counter",counter)
						}
					}
				}
			}
		}
	}
		prepareStatusList(detailDataMap, defectDetailsMap)
		return detailDataMap
	}
	
	/**
	 * Method to get the data for creating the consolidated report in excel format.
	 */
	def getDataForComparisonExcelExport(def executionList, def executionInstance,String realPath,String appUrl,def fieldList) {

		List executionDeviceList = []
		List executionResultInstanceList = []
		
		String deviceDetails

		String fileContents = ""
		def deviceName = ""
		def deviceIp = ""
		def executionTime = ""
		int totalCount = 0
		int testCount =0

		String filePath = ""
		def executionDeviceId

		Map summaryHead = [:]
		Map statusValue = [:]

		def execIds = executionList?.id
		executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def detailDataMap = [:]
		executionDeviceList.each{ executionDeviceInstance ->

			deviceName = executionDeviceInstance?.device
			deviceIp = executionDeviceInstance?.deviceIp
			executionTime = executionDeviceInstance?.executionTime
			executionTime = executionTimeFormat ( executionTime )
			executionDeviceId = executionDeviceInstance?.id

			executionResultInstanceList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDeviceInstance)//,[sort: "script",order: "asc"])
			
			int counter = 1
			int counter1=1
			Date date = new Date()
			executionResultInstanceList.each{ executionResultInstance ->
				counter1= counter1+1
			
				String scriptName = executionResultInstance?.script
				String status = executionResultInstance?.status
				String moduleName = ""
				
				if(executionResultInstance?.category != Category.RDKB_TCL){
					def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
					moduleName = sMap.get(scriptName)
				}else{
					moduleName = "tcl"
				}
				
				int i = 0
				
				if(!moduleName.equals("")){
		//			def scriptObj1 = ScriptFile.findByModuleName(moduleName)
		
	
					def scriptObj = ScriptFile.findByScriptNameAndModuleName(scriptName,moduleName)
					if(scriptObj){
						def dataList
						Map dataMapList = detailDataMap.get(moduleName)
							if(dataMapList == null){
								dataMapList = [:]
								detailDataMap.put(moduleName,dataMapList)
								//detailDataMap.put("total", summaryMap.get("Total Scripts"))
							}
						
						if(dataMapList != null){
							dataList = dataMapList.get("dataList")
							if(dataList == null){
								dataList = []
								dataMapList.put("dataList",dataList)
								dataMapList.put("fieldsList",fieldList)
								counter = 1
						}else{
							counter =  dataMapList.get("counter")
						}
						if(dataList != null){
								
							Map dataMap
							
							dataMap =["C1":counter,"C2":scriptName,"C3":executionResultInstance?.status]
							int j = 3;
							executionList?.each{ exec ->
								def statusData = getExecutionResultStatus(exec ,scriptName )
								dataMap.put(fieldList.getAt(j), statusData)
								j++
							}
							
							dataList.add(dataMap)
							counter ++
							dataMapList.put("counter",counter)
						}
					}
				}
			}
		}
	}
		return detailDataMap
	}
	
	/**
	 * to get the execution result status
	 */
	def getExecutionResultStatus(def execution , def script){
		ExecutionResult exResult = ExecutionResult.findByExecutionAndScript(execution,script)
		String status = "Nil"
		if(exResult){
			status = exResult?.status
		}
		return status
	}
	
	/**
	 * Method to get image name from version file
	 */
	def getImageNameFromVersionFile(def realPath, def executionId, def executionDeviceId){
		String realPathFromFile = executionService.getRealPathForLogsFromTMConfig()
		if(realPathFromFile?.equals(Constants.NO_LOCATION_SPECIFIED)){
			realPathFromFile = realPath
		}
		String image = ""
		String deviceDetails
		String filePath = ""
		String fileContents = ""
		filePath = "${realPathFromFile}//logs//version//${executionId}//${executionDeviceId}//${executionDeviceId}_version.txt"
		if(filePath){
			File file = new File(filePath)
			if(file.isFile()){
				file.eachLine { line ->
					if(!(line.isEmpty())){
						if(!(line.startsWith( LINE_STRING ))){
							fileContents = fileContents + line + HTML_BR
						}
					}
				}
				deviceDetails = fileContents.replace(HTML_BR, NEW_LINE)
			}
		}
		try {
			if(deviceDetails != null && deviceDetails.contains("imagename:")){
				String imagename = "imagename:"
				int indx = deviceDetails.indexOf(imagename)
				int endIndx = deviceDetails.indexOf("\n",indx)
				if(indx >=0 && endIndx > 0){
					indx = indx + imagename.length()
					image = deviceDetails.substring(indx, endIndx)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return image
	}
}
