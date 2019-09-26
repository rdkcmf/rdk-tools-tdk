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
import grails.converters.JSON
import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Calendar

/**
 * Controller class for showing charts 
 * 
 */

class TrendsController {
	def scriptService

	def executionService
	def utilityService
	def executedbService
	
	def index() {
	}

	/**
	 * Redirects to chart.gsp with the last 200 executions of script group
	 * @return
	 */
	def chart() {

		def category = params?.category
		List<String> executionList = null
		List<String> executionTotalList = null
		
		List<String> executionBuildList =[]
		def scripts = []
		if(!category)
			category = RDKV
		scripts = scriptService.getScriptNameFileList(getRealPath(), category)
		
		def sList = scripts?.clone()
		sList?.sort{a,b -> a?.scriptName <=> b?.scriptName}
		//def c = Execution.createCriteria()
		if(RDKV.equals(category.trim())){
			executionList = Execution.executeQuery("select exe.name from Execution exe where exe.category=? and exe.isBenchMarkEnabled=? and exe.isSystemDiagnosticsEnabled=? and exe.scriptGroup is not null",
					[Category.RDKV, true, true])
			executionBuildList = ExecutionDevice.executeQuery("select distinct  exe.buildName from ExecutionDevice exe where exe.category=? and exe.buildName!=? and exe.buildName!=? order by id desc  ",
					[Category.RDKV,"null","Image name not available"])
			
			executionTotalList = Execution.executeQuery("select exe.name from Execution exe where exe.category=? and exe.executionStatus!=? and exe.scriptGroup is not null and exe.name not like '%RERUN%' order by id desc  ",
					[Category.RDKV,INPROGRESS_STATUS])
		}
		else{
			executionList = Execution.executeQuery("select exe.name from Execution exe where exe.category!=? and exe.isBenchMarkEnabled=? and exe.isSystemDiagnosticsEnabled=? and exe.scriptGroup is not null  order by id desc",
					[Category.RDKV, true, true])
			executionTotalList = Execution.executeQuery("select exe.name from Execution exe where exe.category!=? and exe.executionStatus!= ? and exe.scriptGroup is not null",
					[Category.RDKV,INPROGRESS_STATUS])
			executionBuildList = ExecutionDevice.executeQuery("select distinct  exe.buildName from ExecutionDevice exe where exe.category!=? and exe.buildName!=? and exe.buildName!=? order by id desc  ",
					[Category.RDKV,"null","Image name not available"])
		}
		def groups =  utilityService.getGroup()? utilityService.getGroup() : null
		def scriptGrp = ScriptGroup.withCriteria {
			eq('category',Utility.getCategory(category))
			or{
				eq('groups',groups)
				isNull('groups')
			}
			order('name')
		}
		[executionList : executionList, category:category, startIndex:0,endIndex:8, scriptList : sList, scriptGrpList : scriptGrp,executionTotalList :executionTotalList ,executionBuildList :executionBuildList]
	}
	
	/**
	 * Function to get details of the execution result based on buil name and script
	 * @return
	 */
	
	def getBuildScriptChartData(){
		
		try
		{
			def buildName = params?.buildName
			ScriptFile  script = ScriptFile?.findByScriptName(params?.script)
			def executionDeviceList = ExecutionDevice?.findAllByBuildName(buildName)
			int countRes = Integer.parseInt(params?.resultcount)
			int count = 0 
			int fail_represent = 1
			int success_represent = 2
			List<String> executionList = new ArrayList<String>();
			List<Integer> resultList =  new ArrayList<Integer>(); 
			executionDeviceList.each { executionDevice ->
				if(count < countRes)
				{
					Execution execution = executionDevice?.execution
					ExecutionResult executionResult = ExecutionResult?.findByExecutionAndScript(execution, script.scriptName)
					//println executionResult + executionResult?.status
					if(executionResult)
					{
						
						
								if( executionResult?.status == SUCCESS_STATUS )
								{
									
									resultList.add(success_represent)
									executionList.add(execution?.name)
									count ++ 
								}
								if( executionResult?.status == FAILURE_STATUS )
								{
									resultList.add(fail_represent)
									executionList.add(execution?.name)
									count++
								}	
					}
			
				}
			}
			def mapData = [resultList:resultList, executionList: executionList, yCount : SUCCESS_STATUS ]
			render mapData as JSON
		}
		catch(Exception e){
			e.printStackTrace()
		}
	}
	
	/**
	 * Function to get details of the execution result based on build name and script group
	 * @return
	 */
	def showBuildScriptGroupChart(){
	
		try
		{
			def buildName = params?.buildName
			def executionDeviceList = ExecutionDevice?.findAllByBuildName(buildName)
			int countRes = Integer.parseInt(params?.resultcount)
			int count = 0 
			int fail_represent = 1
			int success_represent = 2
			List<String> executionList = new ArrayList<String>();
			List<Integer> resultList =  new ArrayList<Integer>(); 
			def removeExecutionStatus = [ ABORTED_STATUS,PAUSED]
			executionDeviceList.each { executionDevice ->
				if(count < countRes)
				{
					Execution execution = executionDevice?.execution
					
					if(execution?.scriptGroup == params?.scriptGroup && !execution?.name?.matches("(.*)RERUN(.*)")&& !removeExecutionStatus?.contains(execution.executionStatus)  )
					{
						executionList.add(execution?.name)
						count++
						def executionResultList = execution?.executionresults 
						int successCount = 0
						int notAppCount = 0
						int groupSize = executionResultList.size() 
						executionResultList.each { exeResult ->	
							if(exeResult?.status == SUCCESS_STATUS)
								successCount++		
							if(exeResult?.status == NOT_APPLICABLE_STATUS)
								notAppCount++
						}
						int rate = 0
						if(groupSize!=notAppCount)
							rate =successCount*100/(groupSize-notAppCount)
						resultList.add(rate)		
						}
				}
			}
			def mapData = [resultList:resultList, executionList: executionList ]
			render mapData as JSON
		}
		catch(Exception e){
			e.printStackTrace()
		}
	}
	
	/**
	 * Shows the chart to draw the chart based on the execution status
	 * @return
	 */
	def getStatusChartData(){
		
		def listdate = []
		def cpuMemoryList = []
		List<Execution> executionList

		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int scriptGrpSize
		int maxScriptGroupSize = 0
		if(executionList){
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			
			scriptGrpSize = scriptGroupInstance?.scriptList?.size()
			
			def executionSuccessList = []
			def executionFailureList = []
			def executionUndefinedList = []
			def executionNotExecutedList = []
	
			List<ExecutionResult> executionSuccessResultList
			List<ExecutionResult> executionFailureResultList
			List<ExecutionResult> executionUndefinedResultList
	
			executionList?.each{ execution ->
				
				populateChartData(execution)
				scriptGroupInstance = ScriptGroup.findByName(execution?.scriptGroup)
			
				scriptGrpSize = scriptGroupInstance?.scriptList?.size()
				if(maxScriptGroupSize < scriptGrpSize)
					maxScriptGroupSize = scriptGrpSize
				executionSuccessResultList = ExecutionResult.findAllByExecutionAndStatus(execution,SUCCESS_STATUS)
				executionFailureResultList = ExecutionResult.findAllByExecutionAndStatus(execution,FAILURE_STATUS)
				//executionUndefinedResultList = ExecutionResult.findAllByExecutionAndStatus(execution,UNDEFINED_STATUS)
	
				int unexecutedScripts = scriptGrpSize - (executionSuccessResultList.size() + executionFailureResultList.size())// + executionUndefinedResultList.size())
	
				executionSuccessList.add(executionSuccessResultList.size())
				executionFailureList.add(executionFailureResultList.size())
				//executionUndefinedList.add(executionUndefinedResultList.size())
				executionNotExecutedList.add(unexecutedScripts)
			}
	
			listdate.add(executionSuccessList)
			listdate.add(executionFailureList)
			//listdate.add(executionUndefinedList)
			listdate.add(executionNotExecutedList)
		}
		def mapData = [listdate:listdate, execName: executionList?.name, yCount : maxScriptGroupSize ]
		render mapData as JSON
	}
	
	def populateChartData(final Execution executionInstance){
		//if(!executionInstance?.isPerformanceDone){
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		//}
	}
	/**
	 * Function to get details of the execution result based on execution
	 * @return
	 */
	def showNormalExecutionChart()
	{
		try
		{

			Execution execution = Execution.findByName(params?.executionname)
			ScriptGroup  scriptgroup = ScriptGroup?.findByName(execution?.scriptGroup)
			
			List<String> moduleList = new ArrayList<String>();
			List<Integer> resultList =  new ArrayList<Integer>();
			if(execution?.executionStatus != ABORTED_STATUS && execution?.executionStatus != PAUSED)
			{
				def detailDataMap = executedbService.prepareDetailMap(execution,request.getRealPath('/'))
				detailDataMap?.keySet()?.each { moduleName ->
					Map statusMap = detailDataMap?.get(moduleName)
					moduleList.add(moduleName)
					int pendingCount = 0 
					int successCount = 0
					int notAppCount = 0
					int rate = 0
					int moduleSize = 0
					statusMap?.keySet()?.each { status ->
						moduleSize = moduleSize + statusMap?.get(status)
					}
					if( statusMap?.keySet()?.contains(SUCCESS_STATUS))
						successCount = statusMap?.get(SUCCESS_STATUS)
					if(statusMap?.keySet()?.contains(NOT_APPLICABLE_STATUS))
						notAppCount = statusMap?.get(NOT_APPLICABLE_STATUS)
					if(statusMap?.keySet()?.contains(PENDING))
						pendingCount = statusMap?.get(PENDING)
					if(moduleSize!=notAppCount)
						rate = successCount*100/(moduleSize-notAppCount-pendingCount )
					resultList.add(rate)
				}
			
				
			}			
			def mapData = [moduleName :moduleList , resultList: resultList ]
			render mapData as JSON				
		}				
		catch(Exception e){
			e.printStackTrace()
		}			
				

	}
	

	/**
	 * Function to get details of the execution result based on box type
	 * @return
	 */
	def getBoxTypeScriptChartData()
	{
		try
		{
			BoxType boxType = BoxType.findById(params?.boxTypeId)
			ScriptFile  script = ScriptFile?.findByScriptName(params?.script)
			int countRes = Integer.parseInt(params?.resultCnt)
			int fail_represent = 1
			int success_represent = 2
			int successCount = 0
			int failureCount = 0
			List<String> executionList = new ArrayList<String>();
			List<Integer> resultList =  new ArrayList<Integer>(); 
			def scriptDetails = scriptService.getMinimalScript(getRealPath(),script.moduleName,script.scriptName, script.category.toString())
			def device = Device.findAllByBoxType(boxType)
			device = device.collect { it.toString() }
			def includeStatus = [SUCCESS_STATUS,FAILURE_STATUS]
			if(scriptDetails?.boxTypes?.contains(boxType))
			{
				def executionResultList = ExecutionResult?.findAllByScriptAndDeviceInListAndStatusInList(script.scriptName,device,includeStatus,[max:countRes , offset: 0 ,sort: "id",  order: "desc"])
				executionResultList.each { exeResult ->	
					executionList.add(exeResult?.execution?.name)
					if( exeResult?.status == SUCCESS_STATUS )
					{
						successCount++
						resultList.add(success_represent)
					}
					if( exeResult?.status == FAILURE_STATUS )
					{
						failureCount++
						resultList.add(fail_represent)
					}	
				}
			}
			def mapData = [executionName :executionList , resultList: resultList, yCount : success_represent, successCount:successCount, failureCount:failureCount ]
			render mapData as JSON	
		}
		catch(Exception e){
			e.printStackTrace()
		}
	}
	/**
	 * Function to get details of the execution result based on Script Group 
	 * @return
	 */
	def showBoxTypeScriptGroupChart()
	{
	try
		{
			BoxType boxType = BoxType.findById(params?.boxTypeId)
			ScriptGroup  scriptgroup = ScriptGroup?.findByName(params?.scriptgroup)
			int countRes = Integer.parseInt(params?.resultCnt)
			List<String> executionList = new ArrayList<String>();
			List<Integer> resultList =  new ArrayList<Integer>(); 
			int resultOffset = 0
			def device = Device.findAllByBoxType(boxType)
			device = device.collect { it.toString() }
			def removeExecutionStatus = [ ABORTED_STATUS,PAUSED]
			def executionLists = Execution?.findAllByScriptGroupAndNameNotLikeAndExecutionStatusNotInListAndDeviceInList(params?.scriptgroup,'%RERUN%',removeExecutionStatus,device ,[max: countRes , offset: 0,sort: "id",  order: "desc"])
			executionLists.each { execution->
				executionList.add(execution?.name)
				def executionResultList = execution?.executionresults 
				int successCount = 0
				int notAppCount = 0
				int groupSize = executionResultList.size() 
				executionResultList.each { exeResult ->	
					if(exeResult?.status == SUCCESS_STATUS)
						successCount++		
					if(exeResult?.status == NOT_APPLICABLE_STATUS)
						notAppCount++
				}
				int rate = 0
				if(groupSize!=notAppCount)
					rate =successCount*100/(groupSize-notAppCount)
				resultList.add(rate)		
			}
			def mapData = [executionName :executionList , resultList: resultList ]
			render mapData as JSON	
		}
		catch(Exception e){
			e.printStackTrace()
		}
	
	}

	def getRealPath(){
		return request.getSession().getServletContext().getRealPath("/")
	}

	/**
	 * Function to get details of the execution result based on Script
	 * @return
	 */
	def getScriptChartData()
	{
		try 
		{
			Device deviceInstance = Device.findById(params?.deviceId)
			int countRes = Integer.parseInt(params?.resultCnt )
			List<String> executionList = new ArrayList<String>();
			List<Integer> resultList =  new ArrayList<Integer>();
			int fail_represent = 1
			int success_represent = 2
			int successCount = 0
			int failureCount = 0
			def includeStatus = [SUCCESS_STATUS,FAILURE_STATUS]
			def executionResultList = ExecutionResult?.findAllByDeviceAndStatusInListAndScript(deviceInstance.stbName,includeStatus,params?.script,[max:countRes , offset: 0,sort: "id",  order: "desc"])
			executionResultList.each { exeResult->
				executionList.add(exeResult?.execution.name)
				if( exeResult?.status == SUCCESS_STATUS )
				{
					successCount++
					resultList.add(success_represent)
				}
				if( exeResult?.status == FAILURE_STATUS )
				{
					failureCount++
					resultList.add(fail_represent)
				}
			}
			def mapData = [executionName :executionList , resultList: resultList, yCount : success_represent , successCount:successCount, failureCount:failureCount ]
			render mapData as JSON
		}
		catch(Exception e){
			e.printStackTrace()
		}
	}

	/**
	 * Shows the chart to draw the chart based on the benchmark data
	 * @return
	 */
	def getStatusBenchMarkData(){
				
		def executionList
		def timeList = []
		
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		if(executionList){
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			int scriptGrpSize = scriptGroupInstance?.scriptList?.size()	
			def performanceList = []				
			executionList.each{ execution ->
				populateChartData(execution)
				Double timetotal = 0				
				execution?.executionresults?.each{ execResult ->
					performanceList = Performance.findAllByExecutionResultAndPerformanceType(execResult,"BENCHMARK")
					performanceList.each{ performance ->
						if(performance?.processValue){
							timetotal = timetotal + Double.parseDouble(performance?.processValue)
						}
					}
				}
				timeList.add(timetotal/1000)
			}
		}

		def mapData = [execName: executionList?.name, benchmark : timeList]
		render mapData as JSON
	}

	/**
	 * Shows the chart to draw the chart based on SystemDiagnostics
	 * @return
	 */
	def getStatusSystemDiagnosticsCPUData(){
		
		def executionList
		def cpuMemoryList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
	
			def cpuValues = []
			def cpuPercValues = []
			def performanceSd
			String cpumemValue = ""
			String memValue = ""
			executionList.each{ execution ->
				populateChartData(execution)
				Double cpuTotal = 0
				Double cpuPeak = 0
				int counter = 0
				execution?.executionresults?.each{ execResult ->
					counter ++
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.CPU_AVG)
						if(performanceSd?.processValue){
							def cpuAvg = 0
							try {
								cpuAvg = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							cpuTotal = cpuTotal +  cpuAvg
						}
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.CPU_PEAK)
						if(performanceSd?.processValue){
							def cpuPercentage = 0
							try {
								cpuPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							if(cpuPeak < cpuPercentage){
								cpuPeak = cpuPercentage
							}
						}
						
						
				}
				cpuValues.add(cpuTotal/counter)
				cpuPercValues.add(cpuPeak)
			}	
			cpuMemoryList.add(cpuValues)
			cpuMemoryList.add(cpuPercValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : cpuMemoryList]
		render mapData as JSON
	}

	
	/**
	 * Shows the chart to draw the chart based on SystemDiagnostics
	 * @return
	 */
	def getStatusSystemDiagnosticsPeakMemoryData(){
		def executionList
		def cpuMemoryList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
	
			def memoryValues = []
			def memoryValues2 = []
			def memoryValues3 = []
			def performanceSd
			String cpumemValue = ""
			String memValue = ""
			executionList.each{ execution ->
				populateChartData(execution)
				Double cpuTotal = 0
				Double memoryAvailFirstTotal = 0
				Double memoryUsedPeakTotal = 0
				float memoryPercentagePeakTotal = 0
				int counter = 0
				execution?.executionresults?.each{ execResult ->
					counter ++
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.MEMORY_AVAILABLE_PEAK)
						if(performanceSd?.processValue){
							def memoryPercentage = 0
							try {
								memoryPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							memoryAvailFirstTotal = memoryAvailFirstTotal +  memoryPercentage
						}
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.MEMORY_USED_PEAK)
						if(performanceSd?.processValue){
							def memoryPercentage = 0
							try {
								memoryPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							memoryUsedPeakTotal = memoryUsedPeakTotal +  memoryPercentage
						}
						
				}
				memoryValues.add(memoryAvailFirstTotal/counter)
				memoryValues2.add(memoryUsedPeakTotal/counter)
			}
			cpuMemoryList.add(memoryValues)
			cpuMemoryList.add(memoryValues2)
		}
		def mapData = [execName: executionList?.name, systemDiag : cpuMemoryList]
		render mapData as JSON
	}
	
	/**
	 * Shows the chart to draw the chart based on SystemDiagnostics
	 * @return
	 */
	def getStatusSystemDiagnosticsMemoryPercData(){
		def executionList
		def cpuMemoryList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
	
			def memoryValues = []
			def memoryValues2 = []
			def memoryValues3 = []
			def performanceSd
			String cpumemValue = ""
			String memValue = ""
			executionList.each{ execution ->
				populateChartData(execution)
				Double cpuTotal = 0
				Double memoryPercPeakTotal = 0
				int counter = 0
				execution?.executionresults?.each{ execResult ->
					
						counter++
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,Constants.MEMORY_PERC_PEAK)
						if(performanceSd?.processValue){
							def memoryPercentage = 0
							try {
								memoryPercentage = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							memoryPercPeakTotal = memoryPercPeakTotal +  memoryPercentage
						}
						
						
				}
				memoryValues.add(memoryPercPeakTotal/counter)
			}
			cpuMemoryList.add(memoryValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : cpuMemoryList]
		render mapData as JSON
	}

	/**
	 * Shows the chart to draw the line chart based on the execution status
	 * The chart display like three status - success , failure , Not Found 
	 *  
	 * @return
	 */
	def getStatusChartData1(){	 
		def listdate = []
		def executionSuccessList = []
		def executionFailureList = []
		def executionUndefinedList = []
		def executionNotExecutedList = []	
		def cpuMemoryList = []
		List<Execution> executionList
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int scriptGrpSize
		int totalScriptGroupSize = 0 
		if(executionList){
			List<ExecutionResult> executionSuccessResultList
			List<ExecutionResult> executionFailureResultList
			List<ExecutionResult> executionUndefinedResultList
			executionList?.each{ execution ->
				scriptGrpSize = 0
				
				def scriptGroupName =  ScriptGroup.findByName(execution?.scriptGroup)
				if(  scriptGroupName){
					scriptGrpSize = scriptGroupName?.scriptList.size()	
					if( totalScriptGroupSize < scriptGrpSize ){
						totalScriptGroupSize = scriptGrpSize
					}					
				}
				populateChartData(execution)
				
				executionSuccessResultList = ExecutionResult.findAllByExecutionAndStatus(execution,SUCCESS_STATUS)
				executionFailureResultList = ExecutionResult.findAllByExecutionAndStatus(execution,FAILURE_STATUS)
				int unexecutedScripts = scriptGrpSize - (executionSuccessResultList.size() + executionFailureResultList.size())// + executionUndefinedResultList.size())
				executionSuccessList.add(executionSuccessResultList.size())
				executionFailureList.add(executionFailureResultList.size())
				executionNotExecutedList.add(unexecutedScripts)
			}
			listdate.add(executionSuccessList)
			listdate.add(executionFailureList)
			listdate.add(executionNotExecutedList)
		}
		def mapData = [listdate:listdate, execName: executionList?.name, yCount : totalScriptGroupSize, success : executionSuccessList , failure : executionFailureList , notFound : executionNotExecutedList]
		render mapData as JSON
	}
	
	
	/**
	 * Shows the chart to draw the line chart based on the benchmark data
	 * The  plotting the graph according to the timing info value.
	 * @return
	 */
	def getStatusBenchMarkData1(){	
	
		def executionList 
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int sIndex = 0
		int eIndex = 0
		try {
			sIndex =  Integer.parseInt(params?.startIndex)
			eIndex = Integer.parseInt(params?.endIndex)
		} catch (Exception e) {
			e.printStackTrace()
		}
		Map valueMap = [:]
		List commonScripts = []
		List curList = []
		if(executionList && sIndex >= 0 && eIndex > 0 ){
			List scriptsList = []
			try{
				executionList?.each {  ex ->
					List  slist = []
					def sg = ScriptGroup.findByName(ex?.scriptGroup)
					slist.addAll(sg?.scriptList?.scriptName);
					scriptsList.add(slist);
				}
			}catch(Exception e ){
			
			}
			if(scriptsList?.size() > 0){
				commonScripts = scriptsList?.get(0)
				scriptsList?.each { tList ->
					commonScripts = commonScripts?.intersect(tList);
				}
			}
			def performanceSd
			if(commonScripts?.size() < eIndex){
				eIndex = commonScripts?.size()
			}
			curList = commonScripts?.subList(sIndex,eIndex)
			curList?.each {  scriptName ->
				executionList.each{ execution ->
					def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
					performanceSd = Performance.findByExecutionResultAndPerformanceType(exRes,"BENCHMARK")
					def timingInfo   = 0
					if(performanceSd?.processValue){
						try {
							timingInfo = Double.parseDouble(performanceSd?.processValue)
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					def valueList = valueMap?.get(execution?.name)
					if(valueList == null){
						valueList = []
						valueMap.put(execution?.name, valueList)
					}
					valueList?.add(timingInfo)
				}
			}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , benchmark :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON
	}
	
	/**
	 * Shows the chart to draw the line chart based on the CPU- Utilization  
	 * @return
	 */  
	def getStatusSystemDiagnosticsCPUData1(){
		def executionList
		List  cpuValues1 = []
	if(params?.executionIds){
		executionList = getExecutionLists(params?.executionIds)
	}
	else{
		executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
	}	
	int sIndex = 0
	int eIndex = 0
	try {
		sIndex =  Integer.parseInt(params?.startIndex)
		eIndex = Integer.parseInt(params?.endIndex)
	} catch (Exception e) {
		e.printStackTrace()
	}
	Map valueMap = [:]
	List commonScripts = []
	List curList = []
	if(executionList && sIndex >= 0 && eIndex > 0 ){		
		List scriptsList = []
		try{
		executionList?.each {  ex ->
			List  slist = []
			def sg = ScriptGroup.findByName(ex?.scriptGroup)
			slist.addAll(sg?.scriptList?.scriptName);
			scriptsList.add(slist);
		}
		}catch(Exception e){
		
		} 
		if(scriptsList?.size() > 0){
			commonScripts = scriptsList?.get(0)
			scriptsList?.each { tList ->
				commonScripts = commonScripts?.intersect(tList);
			}
		}		
		def performanceSd
		if(commonScripts?.size() < eIndex){
			eIndex = commonScripts?.size()
		}
		curList = commonScripts?.subList(sIndex,eIndex)
		curList?.each {  scriptName ->
			executionList.each{ execution ->
				def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
				performanceSd = Performance.findByExecutionResultAndProcessName(exRes,Constants.CPU_PEAK)
				def cpuUtilization  = 0
				if(performanceSd?.processValue){
					try {
						cpuUtilization = Double.parseDouble(performanceSd?.processValue)
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
				def valueList = valueMap?.get(execution?.name)
				if(valueList == null){
					valueList = []
					valueMap.put(execution?.name, valueList)
				}
				valueList?.add(cpuUtilization)
				
			}
		}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , cpuValuesTest :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON
	}
	/**
	 * Shows the chart to draw the line chart based on the Memory Utilization 
	 * @return
	 */
	def getStatusSystemDiagnosticsPeakMemoryData1(){		
		def executionList
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		int sIndex = 0
		int eIndex = 0		
		try {
			sIndex =  Integer.parseInt(params?.startIndex)
			eIndex = Integer.parseInt(params?.endIndex)
		} catch (Exception e) {
			e.printStackTrace()
		}		
		Map valueMap = [:]
		List commonScripts = []
		List curList = []
		if(executionList && sIndex >= 0 && eIndex > 0 ){
			
			List scriptsList = []
			try {
			executionList?.each {  ex ->
				List  slist = []
				def sg = ScriptGroup.findByName(ex?.scriptGroup)
				slist.addAll(sg?.scriptList?.scriptName);
				scriptsList.add(slist);
			}
			}catch (Exception e){
			
			}
			if(scriptsList?.size() > 0){
				commonScripts = scriptsList?.get(0)
				scriptsList?.each { tList ->
					commonScripts = commonScripts?.intersect(tList);
				}
			}	
			
			def performanceSd
			if(commonScripts?.size() < eIndex){
				eIndex = commonScripts?.size()
			}			
			curList = commonScripts?.subList(sIndex,eIndex)
			curList?.each {  scriptName ->
				executionList.each{ execution ->
					def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
					performanceSd = Performance.findByExecutionResultAndProcessName(exRes,Constants.MEMORY_USED_PEAK)
					def memoryPercentage = 0
					if(performanceSd?.processValue){
						try {
							memoryPercentage = Double.parseDouble(performanceSd?.processValue)
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					def valueList = valueMap?.get(execution?.name)
					if(valueList == null){
						valueList = []
						valueMap.put(execution?.name, valueList)
					}
					valueList?.add(memoryPercentage)
				}
			}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , memoryValuesTest :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON

	}

	/**
	 * Shows the chart to draw line chart based on the Memory Used Percentage 
	 * @return
	 */
	def getStatusSystemDiagnosticsMemoryPercData1(){
		def executionList
		
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}		
		int sIndex = 0
		int eIndex = 0
		try {
			sIndex =  Integer.parseInt(params?.startIndex)
			eIndex = Integer.parseInt(params?.endIndex)
		} catch (Exception e) {
			e.printStackTrace()
		}		
		Map valueMap = [:]
		List commonScripts = []
		List curList = []
		
		if(executionList && sIndex >= 0 && eIndex > 0 ){
			List scriptsList = []
			try{
			executionList?.each {  ex ->
				List  slist = []
				def sg = ScriptGroup.findByName(ex?.scriptGroup)
				slist.addAll(sg?.scriptList?.scriptName);
				scriptsList.add(slist);
			}
			}catch(Exception  e){
			
			}
			if(scriptsList?.size() > 0){
				commonScripts = scriptsList?.get(0)
				scriptsList?.each { tList ->
					commonScripts = commonScripts?.intersect(tList);
				}
			}	
			if(commonScripts?.size() < eIndex){
				eIndex = commonScripts?.size()
			}
			curList = commonScripts?.subList(sIndex,eIndex)		
			def performanceSd
			curList?.each {  scriptName ->
				executionList.each{ execution ->
					def exRes = ExecutionResult?.findByExecutionAndScript(execution,scriptName)
					performanceSd = Performance.findByExecutionResultAndProcessName(exRes,Constants.MEMORY_PERC_PEAK)
					def memoryPercentage = 0
					if(performanceSd?.processValue){
						try {
							memoryPercentage = Double.parseDouble(performanceSd?.processValue)
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					def valueList = valueMap?.get(execution?.name)
					if(valueList == null){
						valueList = []
						valueMap.put(execution?.name, valueList)
					}
					valueList?.add(memoryPercentage)
				}
			}
		}
		def mapData = [execName: valueMap?.keySet(), systemDiag : valueMap?.values() , scripts :curList , memoryValuesTest :valueMap?.values() ,maxSize : commonScripts?.size()]
		render mapData as JSON
	}

	/**
	 * Shows the chart to draw the chart based on Paging data
	 * @return
	 */
	def getPagingData(){
		
		def executionList
		def systemDiagList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
	
			def pageInValues = []
			def pageOutValues = []
			def performanceSd
		
			executionList.each{ execution ->
				populateChartData(execution)
				Double pageInTotal = 0
				Double pageOutTotal = 0
				execution?.executionresults?.each{ execResult ->
					
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"PAGING : pgpgin/s")
						if(performanceSd?.processValue){
							def pageInVal = 0
							try {
								pageInVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							pageInTotal = pageInTotal +  pageInVal
						}
						
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"PAGING : pgpgout/s")
						if(performanceSd?.processValue){
							def pageOutVal = 0
							try {
								pageOutVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							pageOutTotal = pageOutTotal +  pageOutVal
						}
				}
				pageInValues.add(pageInTotal)
				pageOutValues.add(pageOutTotal)
			}
			systemDiagList.add(pageInValues)
			systemDiagList.add(pageOutValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : systemDiagList]
		render mapData as JSON

	}
	
	/**
	 * Shows the chart to draw the chart based on Swap Data
	 * @return
	 */
	def getSwapData(){

		def executionList
		def systemDiagList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			def swapValues = []
			def performanceSd
	
			executionList.each{ execution ->
				populateChartData(execution)
				Double swapTotal = 0
				Double loadAvgTotal = 0
				execution?.executionresults?.each{ execResult ->											
						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"SWAPING")
						if(performanceSd?.processValue){
							def swapVal = 0
							try {
								swapVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							swapTotal = swapTotal +  swapVal
						}							
				}
				swapValues.add(swapTotal)
			}
			systemDiagList.add(swapValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : systemDiagList]
		render mapData as JSON
	}
/**
 * Plot the graph using the load average data
 * @return
 */
	
	def getLoadAverage(){
		
		def executionList
		def systemDiagList = []
		if(params?.executionIds){
			executionList = getExecutionLists(params?.executionIds)
		}
		else{
			executionList = getExecutionList(params?.scriptGroup,params?.deviceId,params?.resultCnt)
		}
		
		executionList?.intersect(systemDiagList)
		if(executionList){
			
			ScriptGroup scriptGroupInstance = ScriptGroup.findByName(executionList[0]?.scriptGroup)
			def loadAvgValues = []
			def performanceSd
	
			executionList.each{ execution ->
				populateChartData(execution)
				
				Double loadAvgTotal = 0
				execution?.executionresults?.each{ execResult ->

						performanceSd = Performance.findByExecutionResultAndProcessName(execResult,"LOAD AVERAGE")
						if(performanceSd?.processValue){
							def loadAvgVal = 0
							try {
								loadAvgVal = Double.parseDouble(performanceSd?.processValue)
							} catch (Exception e) {
								e.printStackTrace()
							}
							loadAvgTotal = loadAvgTotal +  loadAvgVal
						}
				}
				loadAvgValues.add(loadAvgTotal)
			}
			systemDiagList.add(loadAvgValues)
		}
		def mapData = [execName: executionList?.name, systemDiag : systemDiagList]
				
		render mapData as JSON
	}
	
	/**
	 * Returns execution list
	 * @param scriptGroup
	 * @param deviceId
	 * @param maxRes
	 * @return
	 */
	def List<Execution> getExecutionList(final String scriptGroup, final String deviceId, final String maxRes){
		
		ScriptGroup scriptGroupInstance = ScriptGroup.findById(scriptGroup)
		Device deviceInstance = Device.findById(deviceId)
		int countRes = Integer.parseInt(maxRes)
		//performance data enabled execution names
		def executionNameList = Execution.findAllByIsBenchMarkEnabledAndIsSystemDiagnosticsEnabled('1','1')
		def executionNames=[]
		int executionNameCount = 0
		executionNameList.each { execName ->
			if(executionNameCount < countRes){
				if(execName.scriptGroup.toString().equals(scriptGroupInstance?.toString()) && execName.device.toString().equals(deviceInstance?.toString())){
					executionNames.add(execName)
					executionNameCount++
				}
			}
		}
		/*def c = Execution.createCriteria()
		List<Execution> executionList = c.list {
			and {
				eq("scriptGroup", scriptGroupInstance?.name)
				eq("device", deviceInstance?.stbName)
			}
			order("id", "desc")
			maxResults(countRes)			
		}*/
		return executionNames
	}
	
	/**
	 * Returns execution list based on execution id's
	 * @param executionIds
	 * @return
	 */
	def List<Execution> getExecutionLists(final String executionIds){
		def  executionArray = executionIds.split(",")
		List<Execution> executionList = []
		Execution execution
		//Execution executionInstance = Execution.findById(executionArray[0])
		//def scriptGroup = executionInstance?.scriptGroup
		def counter = 0
		executionArray.each{ executionId ->			
			if(counter < 10){
					execution = Execution.findByName(executionId)	
					if(execution?.scriptGroup){	
					//if(scriptGroup.equals(execution?.scriptGroup)){
						executionList << execution
					//}
					}
			}
			counter++
		}
		return executionList
	}
	
	/**
	 * Displays the failed execution details of the input execution
	 */
	def showDetailedData() {
		redirect(action: "showDetails", params: [id:params?.id])
	}

	/**
	 * Displays the failed execution details of the input execution
	 */
	def showDetails() {
		Execution executionInstance = Execution.findByName(params?.id)
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup

		def executionResultMap = [:]
		def statusResultMap = [:]
		def listStatusCount = [:]

		executionDeviceList.each { executionDevice ->
			ArrayList executionList = new ArrayList(executionDevice.executionresults);
			listStatusCount = executedbService.getStatusList(executionInstance,executionDevice,executionList.size().toString())
			statusResultMap.put(executionDevice, listStatusCount)
		}

		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}

		def analysisData = executedbService.getDefectAnalysisDetails(executionInstance)

		def totalAnalyzedData = analysisData[TOTAL_ANALYZED_DATA]
		def moduleData = analysisData.get(MODULE_DATA)
		def defectData = analysisData.get(DEFECT_DATA)

		def detailDataMap = executedbService.prepareDetailMap(executionInstance,request.getRealPath('/'))

		def tDataMap = [:]
		def  chartModuleDataList = []

		int total = 0
		detailDataMap?.keySet()?.each { module ->
			Map statusMap = detailDataMap?.get(module)
			int tCount = 0
			statusMap?.keySet()?.each { status ->

				def tStatusCounter = tDataMap.get(status)
				def statusCounter = statusMap.get(status)
				if(!tStatusCounter){
					tStatusCounter = 0
				}
				if(!status.equals(PENDING)){
					tCount = tCount + statusCounter
					tStatusCounter = tStatusCounter + statusCounter
					tDataMap.put(status, tStatusCounter)
				}
			}

			int na = 0
			if(statusMap?.keySet().contains(NOT_APPLICABLE_STATUS)){
				na = statusMap?.get(NOT_APPLICABLE_STATUS)
			}

			statusMap.put(EXECUTED, tCount)
			def success = statusMap?.get(SUCCESS)
			if(success){
				int rate = 0
				if(tCount > 0){
					rate = ((success * 100)/(tCount - na))
				}
				statusMap.put(PASS_RATE, rate)
				def statusData = []
				statusData.add("'" + module + "'")
				statusData.add(rate)
			}
			total = total + tCount
			if(moduleData[module] != null) {
				detailDataMap[module].putAll(moduleData[module])
			}
			
			int analyzedRate = 0
			if(statusMap?.get(FAILURE)){
				int failure = statusMap?.get(FAILURE)
				int analyzed = detailDataMap[module]?.get(ANALYZED) ? detailDataMap[module]?.get(ANALYZED): 0
				if(failure > 0){
				    analyzedRate = (analyzed*100)/failure
				}
			}
			statusMap.put(ANALYZED, analyzedRate)
			
		}

		tDataMap.put(EXECUTED, total)
		int rate
		if(tDataMap?.get(SUCCESS)){
			int success = tDataMap?.get(SUCCESS)
			int na = 0
			if(tDataMap?.keySet().contains(NOT_APPLICABLE_STATUS)){
				na = tDataMap?.get(NOT_APPLICABLE_STATUS)
			}
			rate = ((success * 100)/(total - na))
		}

		int analyzedRate = 0
		if(tDataMap?.get(FAILURE)){
			int failure = tDataMap?.get(FAILURE)
			int analyzed = totalAnalyzedData[ANALYZED]
			if(failure > 0){
				analyzedRate = (analyzed*100)/failure
			} 
		}

		tDataMap.put(PASS_RATE, rate)
		tDataMap.putAll(totalAnalyzedData)
		tDataMap.put(ANALYZED, analyzedRate)
		

		def data = [statusResults : statusResultMap, executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList,
			testGroup : testGroup, tDataMap: tDataMap, executionresults:executionResultMap, boxType: device?.boxType, defectData: defectData,
			detailDataMap:detailDataMap, moduleDataMap: moduleData]
		render(template:"showDetails", model:data)
		return data
	}

	/**
	 * Provides defect details history and  script execution status chart for result analysis
	 */
	def resultAnalysis (String execId, String scriptName, String boxTypeId, String execDeviceId, String execResultId, String selectedBoxType, String noOfEntries, String category) {

		Integer maxResultCount = Integer.parseInt(noOfEntries)
		selectedBoxType = selectedBoxType?.trim()
		BoxType boxType = BoxType.findByName(selectedBoxType)
		def allowedDevices = selectedBoxType.equalsIgnoreCase("All") ? Device.list()?.stbName : Device.findAllByBoxType(boxType)?.stbName
		def execResults = []
		if(allowedDevices != null) {
			def execCriteria = ExecutionResult.createCriteria()
			execResults = execCriteria {
				like ("script", scriptName)
				'in' ("device", allowedDevices)
				maxResults(maxResultCount)
				order("id", "desc")
				lt("execution.id", execId.toLong())
			}
		}
		def analysisDetails = []
		def data = [:]
		def remarks = ""
		def defectType = ""
		def ticketNo = ""

		def existingAnalysisData =  DefectDetails.findByExecutionIdAndScriptName(execId, scriptName)
		if(existingAnalysisData != null) {
			remarks = existingAnalysisData.remarks
			defectType = existingAnalysisData.defectType
			ticketNo = existingAnalysisData.ticketNumber
		}
		
		def statusMap = [:]
		statusMap[FAILURE_STATUS] = 0
		statusMap[SUCCESS_STATUS] = 0
		statusMap[INPROGRESS_STATUS] = 0
		statusMap[SKIPPED_STATUS] = 0
		statusMap[PENDING] = 0
		statusMap[NOT_APPLICABLE_STATUS] = 0
		statusMap[SCRIPT_TIME_OUT] = 0
	
		execResults?.each { def result->
			data = [:]
			data.execName = result?.execution?.name
			data.execId = result?.execution?.id
			Device device = Device.findByStbName(result?.device)
			data.boxType = device?.boxType?.name
			data.status = result?.status
			data.executionResultId = result?.id
			data.executionDeviceId = result?.executionDevice?.id 
			if(statusMap[result?.status] == null){
				statusMap[result?.status] = 1
			} else {
			    statusMap[result?.status] = statusMap[result?.status] + 1
			}
			def analysisData =  DefectDetails.findByExecutionIdAndScriptName(result?.execution?.id, scriptName)
			if(analysisData != null) {
				data.ticketNo = analysisData?.ticketNumber
				data.defectType = analysisData?.defectType
				data.remarks = analysisData?.remarks
			}

			analysisDetails.add(data)
		}
		
		def boxCategory = Category.RDKV 
		if(!category) {
			ExecutionDevice execDeviceInstance = ExecutionDevice.findById(execDeviceId)
			if(execDeviceInstance) {
				boxCategory = execDeviceInstance?.category
			}
		} else {
			boxCategory = (category == "RDKV")? Category.RDKV : Category.RDKB
		}
		
		
		def boxTypes = BoxType.findAllByCategory(boxCategory)
		
		[scriptName:scriptName, executionId:execId, boxTypeId:boxTypeId, execHistory :analysisDetails, remarks: remarks, ticketNo:ticketNo,
			defectType:defectType, execDeviceId:execDeviceId, execResultId: execResultId, boxTypes : boxTypes.name, noOfEntries:noOfEntries,
			selectedBoxType:selectedBoxType, statusList:statusMap]
	}

	/**
	 * Gets the execution details corresponding to the given parameters and populates in UI 
	 */
	def getExecutionDetails () {
		redirect(controller:"execution", action: "getExecutionDetails", params: params)
	}

	/**
	 * Saves the defect analysis data corresponding to execution id and script name to database
	 */
	def saveAnalysisData() {
		boolean isSaved = true
		def executionId = Integer.parseInt(params?.executionId)
		DefectDetails defectDetails = DefectDetails.findByExecutionIdAndScriptName(executionId,params?.scriptName)
		if(defectDetails == null){
			defectDetails = new DefectDetails()
		}
		defectDetails.scriptName = params?.scriptName
		defectDetails.ticketNumber = params?.ticketNo
		defectDetails.defectType = params?.defectType
		defectDetails.executionId = executionId
		defectDetails.remarks = params?.remarks
		if(! defectDetails.save(flush:true))
		{
			println defectDetails.errors.allErrors.join(' \n')
			isSaved = false
		}
		Execution execution = Execution.findById(params?.executionId)
		params.id = execution.name
		def data = showDetails()
		return 
	}
	
	/**
	 * Provides option to do the analysis of the execution with input name in a new page
	 */
	def analyze(String name) {
		[name:name]
	}
	
	/**
	 * Displays the executions for analysis based on the input category
	 */
	def executionsForAnalysis(String category) {
		def selectedCategory =  category==RDKV ? Category.RDKV : Category.RDKB
		def completedStatus = COMPLETED_STATUS
		def result = FAILURE_STATUS
		Calendar cal = Calendar.getInstance();
		cal.add(Calendar.DATE, -14);
		String formated = cal.get(Calendar.YEAR) + "-" + (cal.get(Calendar.MONTH) + 1) + "-" + cal.get(Calendar.DATE) + " 00:00:00"
		def executionTotalList = Execution.findAll("from Execution as b where b.category='${selectedCategory}' and b.executionStatus='${completedStatus}' and b.result='${result}' and b.dateOfExecution>'${formated}' and (b.script like '%Multiple%' or b.scriptGroup is not null ) order by id desc")
		render executionTotalList
	}
	
}
