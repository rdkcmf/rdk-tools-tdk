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

/**
 * A class that handles the Execution of scripts.
 * @author sreejasuma
 */
class ExecutionController {

	def scriptexecutionService
	/**
	 * Injects quartz scheduler
	 */
	def quartzScheduler
	/**
	 * Injects the executionSerice.
	 */
	def executionService
	/**
	 * Injects the scriptService.
	 */
	def scriptService
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication

	def utilityService

	def exportService   // Export service provided by Export plugin

	def deviceStatusService

	def primitivetestService

	def executedbService

	def executescriptService

	def tclExecutionService
	/**
	 * Injects the excelExportService
	 */
	def excelExportService
	
	/**
	 * Injects the service for downloading logs in Zip format.
	 */
	
	def logZipService

	public static volatile Object  lock = new Object()
	private static int execIdCounter = 0
	public static final String EXPORT_SCRIPT_LABEL 			= "Script"
	public static final String EXPORT_STATUS_LABEL 			= "Status"
	public static final String EXPORT_DEVICE_LABEL 			= "Device"
	public static final String EXPORT_DEVICE_DETAILS_LABEL 	= "Device Details"
	public static final String EXPORT_LOGDATA_LABEL			= "Log Data"
	public static final String EXPORT_FUNCTION_LABEL 		= "Function: "
	public static final String EXPORT_FUNCTION_STATUS_LABEL = "Function Status: "
	public static final String EXPORT_EXPECTED_RESULT_LABEL = "Expected Result: "
	public static final String EXPORT_ACTUAL_RESULT_LABEL 	= "Actual Result: "
	public static final String EXPORT_IPADDRESS_LABEL 		= "IP Address"
	public static final String EXPORT_EXECUTION_TIME_LABEL 	= "Time taken for execution(min)"
	public static final String EXPORT_COLUMN1_LABEL 		= "C1"
	public static final String EXPORT_COLUMN2_LABEL 		= "C2"
	public static final String EXPORT_SHEET_NAME 			= "Execution_Results"
	public static final String EXPORT_FILENAME 				= "ExecutionResults-"
	public static final String COMBINED_EXPORT_FILENAME 	= "CombinedExecutionResults-"
	public static final String EXPORT_COMPARE_FILENAME 		= "ExecutionResultsComparison-"
	public static final String EXPORT_EXCEL_FORMAT 			= "excel"
	public static final String EXPORT_ZIP_FORMAT 			= "zip"
	public static final String EXPORT_EXCEL_EXTENSION 		= "xls"
	public static final String EXPORT_ZIP_EXTENSION 		= "zip"
	public static final String MARK_ALL_ID1 				= "markAll1"
	public static final String MARK_ALL_ID2 				= "markAll2"
	public static final String UNDEFINED					= "undefined"


	def index() {
		redirect(action: "create")
	}

	/**
	 * Method to unschedule a quartz job
	 */
	def unScheduleJob(){
		def countVariable = 0
		def jobDetailInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					jobDetailInstance = JobDetails.get(idDb)
					def triggname = jobDetailInstance?.triggerName
					def jobname = jobDetailInstance?.triggerName
					quartzScheduler.unscheduleJob(triggerKey(triggname));
					quartzScheduler.deleteJob(jobKey(jobname));
					if (jobDetailInstance) {
						jobDetailInstance.delete(flush: true)
					}
				}
			}
		}
		render(template: "scheduleTable", model: [jobDetailList : JobDetails.list()])
	}


	def deleteJob(){
		def jobDetailsInstance = JobDetails.findById(params?.jobId)
		if (jobDetailsInstance) {

			def date = new Date()
			def endDate = jobDetailsInstance?.endDate
			def time
			if(endDate){
				time = date.getTime() - endDate.getTime()
			}
			else{
				time = date.getTime() - jobDetailsInstance?.startDate?.getTime()
			}
			if(time > 0 ){
				jobDetailsInstance.delete(flush: true)
			}
		}
		render(template: "scheduleTable", model: [jobDetailList : JobDetails.list()])
	}

	/**
	 * Method to create a cron tab based on the selection of
	 * schedule type in the gsp page by the user
	 */    
	def createCronScheduleTab(def params) {

		String status = SUCCESS_STATUS
		String cronschedule = ""
		String queryString = ""
		String weekDay = params?.weekDay
		String weekDays = ""
		switch ( params?.reccurGroup ) {
			case KEY_DAILY:
				switch(params?.reccurDaily){
					case KEY_DAILYDAYS:
					if((params?.dailyDaysCount).isEmpty()){
						cronschedule = message(code: 'schedule.novalue.dailydays')
						status = ERROR_STATUS
					}
					else{
						queryString = "Every ${params?.dailyDaysCount} days"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} */${params?.dailyDaysCount} * ?"
					}
					break
					case KEY_DAILYWEEKDAY:
					queryString = "All Weekdays"
					cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * 2-6"
					break
					default:
					cronschedule = message(code: 'schedule.error.dailydays')
					status = ERROR_STATUS
					break
				}
				break

			case KEY_WEEKLY:
				if(weekDay){
					if(weekDay instanceof String){
						queryString = "Weekly on ${weekDay}"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * ${weekDay}"
					}
					else{
						weekDay.each{ it->
							weekDays = weekDays+it+COMMA_SEPERATOR
						}
						weekDays = weekDays.substring( 0, (weekDays.size()-1) )
						queryString = "Weekly on ${weekDays}"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * ${weekDays}"
					}
				}
				else{
					cronschedule = message(code: 'schedule.error.weekly')
					status = ERROR_STATUS
				}
				break

			case KEY_MONTHLY:

				switch(params?.reccurMonthly){
					case KEY_MONTHLYDAYS:
					if((params?.monthlyMonthCount).isEmpty() || (params?.monthlyDaysCount).isEmpty() ){
						cronschedule = message(code: 'schedule.novalue.monthly')
						status = ERROR_STATUS
					}
					else{
						queryString = "Day ${params?.monthlyDaysCount} of every ${params?.monthlyMonthCount} month"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ${params?.monthlyDaysCount} */${params?.monthlyMonthCount} ?"
					}
					break
					case KEY_MONTHLYCOMPLEX:
					if((params?.monthlyMonthCnt).isEmpty()){
						cronschedule = message(code: 'schedule.empty.monthly')
						status = ERROR_STATUS
					}
					else{
						if((params?.daytype).equals( KEY_LASTDAY )){
							queryString = "Last  ${executionService.getDayName(params?.dayName)} of every ${(params?.monthlyMonthCnt)} month"
							cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? */${params?.monthlyMonthCnt} ${params?.dayName}${params?.daytype}"
						}
						else{
							queryString = "${executionService.getOptionName(params?.daytype)} ${executionService.getDayName(params?.dayName)} of every ${params?.monthlyMonthCnt} month"
							cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? */${params?.monthlyMonthCnt} ${params?.dayName}#${params?.daytype}"
						}
					}
					break

					default:
					cronschedule = message(code: 'schedule.error.monthly')
					status = ERROR_STATUS
					break
				}
				break

			default: break
		}
		return [status,cronschedule,queryString]
	}

	/**
	 * Schedule a quartz job
	 * @return
	 */
	def scheduleOneOff() {

		String cronschedule
		String startDateString = (params?.startdate).toString()
		String endDateString = (params?.enddate).toString()
		Date startDate = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(startDateString)
		Date endDate = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(endDateString)
		String status
		String resultString
		String queryString
		String jobName = KEY_JOB+System.currentTimeMillis().toString()
		String triggerName = KEY_TIGGER+System.currentTimeMillis().toString()
		
		List<String> scriptList = new ArrayList<String>()
		String scheduleDate = (params?.testdate).toString()
		java.util.Date date = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(scheduleDate)
		if( Date.getMillisOf( date ) < System.currentTimeMillis() && (params?.scheduleGroup.equals( KEY_ONETIME )) ){
			render message(code: 'schedule.valid.date')
			return
		}
		else if(Date.getMillisOf( startDate ) < System.currentTimeMillis() && (params?.scheduleGroup.equals( KEY_RECCURENCE ))){
			render message(code: 'schedule.valid.startdate')
			return
		}
		else if((endDate < startDate) && (params?.scheduleGroup.equals( KEY_RECCURENCE ))){
			render message(code: 'schedule.valid.startenddate')
			return
		}
		else{

			String[] scriptIdArray = (params?.scriptlist).split(COMMA_SEPERATOR)
			scriptIdArray.each{ scriptid ->
				if(!(scriptid.isEmpty()))
				{
					scriptList.add(scriptid)
				}
			}

			JobDetail job = JobBuilder.newJob(JobSchedulerService.class)
					.withIdentity(jobName).build();

			Trigger trigger
			if(params?.scheduleGroup.equals( KEY_ONETIME )){
				queryString = KEY_ONETIME
				startDate = date
				endDate = null
				trigger = new SimpleTriggerImpl(triggerName, date)
			}
			else if(params?.scheduleGroup.equals( KEY_RECCURENCE )){

				(status, resultString, queryString) = createCronScheduleTab(params)
				if(status.equals(ERROR_STATUS)){
					render resultString
					return
				}
				else{
					cronschedule = resultString
				}

				trigger = newTrigger()
						.withIdentity(triggerName)
						.withSchedule(cronSchedule(cronschedule))
						.startAt(startDate)
						.endAt(endDate)
						.forJob(jobName)
						.build();
			}
			def jobSheduled = JobDetails?.findAllByDeviceAndStartDate( params?.deviceId,startDate)
			//To avoid scheduling if the device already scheduled for that time
			if(jobSheduled)
			{
				render message(code: 'Another test execution is scheduled in this device for the specified time.')
				return	
			}
			else{
				
				try{
					quartzScheduler.scheduleJob(job, trigger)
				}
				catch(Exception qEx){
					render message(code: 'schedule.invalid.dates')
					return
				}
			
				int repeatCount = (params?.repeatCount).toInteger()


				JobDetails jobDetails = new JobDetails()
				jobDetails.jobName = jobName
				jobDetails.triggerName = triggerName
				jobDetails.script = scriptList
				jobDetails.scriptGroup = params?.scriptGroup
				jobDetails.device = params?.deviceId
				jobDetails.deviceGroup = null
				jobDetails.realPath = getRealPath()
				jobDetails.appUrl = getApplicationUrl()
				jobDetails.filePath = "${request.getRealPath('/')}//fileStore"
				jobDetails.queryString = queryString
				jobDetails.startDate = startDate
				jobDetails.endDate = endDate
				jobDetails.oneTimeScheduleDate = date
				jobDetails.isSystemDiagnostics = params?.isSystemDiagnostics
				jobDetails.isBenchMark = params?.isBenchMark
				jobDetails.isStbLogRequired=params?.isStbLogRequired
				jobDetails.rerun = params?.rerun
				jobDetails.repeatCount = repeatCount
				jobDetails.rerunOnFailure= FALSE
				jobDetails.groups = utilityService.getGroup()
				jobDetails.category = Utility.getCategory(params?.category)
				if(!jobDetails.save(flush:true)){
					jobDetails.errors.each{
						println "error : "+it
					}
				}
			}
			def jobDetailList = JobDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
			render(template: "scheduleTable", model: [jobDetailList : jobDetailList])
			return
		}

	}

	/**
	 * Method to display the schedule page with previously scheduled job details
	 * @param max
	 * @return
	 */
	def showSchedular(Integer max){

		params.max = Math.min(max ?: 10, 100)
		def repeatCount = (params?.repeatId)
		def rerun = params?.rerun

		// identifying the category of job

		def category = null
		if(params?.scriptGroup){
			def val = params?.scriptGroup.split(',')
			def scriptGrp = ScriptGroup.findByName(val[0]?.trim())
			category = scriptGrp?.category?.toString()
		}
		if(params?.scripts){
			def val = params?.scripts.split(',')
			def script = ScriptFile.findByScriptName(val[0]?.trim())
			category = script?.category?.toString()
		}
		if(category == null){
			category = params?.category
		}
		[scripts : params?.scripts, devices : params?.devices, device : params?.deviceId, scriptGroup : params?.scriptGroup, jobDetailList : JobDetails.list(),
			jobInstanceTotal : JobDetails.count(), isSystemDiagnostics : params?.systemDiagnostics, isBenchMark : params?.benchMarking, rerun : rerun,
			repeatCount : repeatCount,isStbLogRequired : params?.isLogReqd, category : params?.category]
	}

	/**
	 * Creates the execution page with the listing of devices 
	 * @param max
	 * @return
	 */
	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)

		def groups = utilityService.getGroup()
		def category
		def executionInstanceList
		def executionInstanceListCnt
		def jobDetailList
		def deviceInstanceListV
		def deviceInstanceListB
		def deviceInstanceList

		deviceInstanceListV = Device.findAllByGroupsAndCategory(groups, Category.RDKV,[sort:'stbName',order:'asc'])
		deviceInstanceListB = Device.findAllByGroupsAndCategory(groups, Category.RDKB,[sort:'stbName', order:'asc'])
		category = params?.category
		if(params?.devicestatustable) {
			// This is called from execution-resolver.js loadXmlDoc. This is for automatic page refresh.
			def result1
			if(category){
				if(Category.RDKV.toString().equals(category)){
					deviceInstanceList = deviceInstanceListV
				}
				else if(Category.RDKB.toString().equals(category)){
					deviceInstanceList = deviceInstanceListB
				}

				result1 = [url: getApplicationUrl(), deviceList : deviceInstanceList, deviceInstanceTotal: deviceInstanceList?.size()]
				render view:"devicelist", model:result1
				return
			}
		}
		else if(params?.category && !"All".equals(params?.category)){
			category = Utility.getCategory(params?.category)
			executionInstanceListCnt = Execution.countByGroupsAndCategory(groups, category)
			executionInstanceList = Execution.findAllByGroupsAndCategory(groups, category,[max:params.max, offset:params?.offset,sort:params?.sort,order:params?.order])
			jobDetailList = JobDetails.findAllByGroupsAndCategory(groups, category,[max:params.max, offset:params?.offset])
		}else{
			executionInstanceListCnt = Execution.countByGroups(groups)
			executionInstanceList = Execution.findAllByGroups(groups, [max:params.max, offset:params?.offset,sort:params?.sort,order:params?.order])
			jobDetailList = JobDetails.findAllByGroups(groups, [max:params.max, offset:params?.offset])
		}

		if(params?.devicetable) {
			// This is called from execution-resolver.js loadXmlDoc. This is for automatic page refresh.
			def result = [executionInstanceList : executionInstanceList, executorInstanceTotal: executionInstanceListCnt, category:params?.category]
			render view:"executionhistorytable", model:result
			return
		}
		else{
			try{
				DeviceStatusUpdater.updateDeviceStatus(grailsApplication,deviceStatusService,executescriptService);
			}catch(Exception e){
				e.printStackTrace();
			}
		}

		[url : getApplicationUrl(), deviceListV : deviceInstanceListV, deviceListB : deviceInstanceListB,  error: params.error, executionInstanceList : executionInstanceList, executorInstanceTotal: executionInstanceListCnt,
			jobDetailList : jobDetailList, jobInstanceTotal: jobDetailList.size(), deviceInstanceTotalV: deviceInstanceListV?.size(), deviceInstanceTotalB: deviceInstanceListB?.size(), category : params?.category ]
	}

	/**
	 * Show the device IP and the scripts based on the selection
	 * of device name from the list
	 * @return
	 */
	def showDevices(){
		def category = params?.category?.trim()
		def device = Device.get( params?.id )
		def scripts = []
		def newScripts = []
		if(category?.toString()?.equals('RDKB_TCL') ){
			newScripts = scriptService.getTotalTCLScriptList(getRealPath())
			newScripts?.each { it ->
				if(it){
					scripts?.add(it)
				}  
			}	
		}
		else{
			scripts = scriptService.getScriptNameFileList(getRealPath(), category)
		}
		def sList = scripts?.clone()
		sList?.sort{a,b -> a?.scriptName <=> b?.scriptName}
		def groups =  utilityService.getGroup()? utilityService.getGroup() : null

		def scriptGrp = ScriptGroup.withCriteria {
			eq('category',Utility.getCategory(category))
			or{
				eq('groups',groups)
				isNull('groups')
			}
			order('name')
		}

		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
		Calendar cal = Calendar.getInstance()
		def devices = getDeviceList(category)
		[datetime :  dateFormat.format(cal.getTime()).toString(), device : device, scriptGrpList : scriptGrp, scriptList : sList, category:category, devices:devices]
	}

	def getDeviceList(def category){
		category = Utility.getCategory(category)
		def devices = null
		switch(category){
			case Category.RDKB:
			case Category.RDKB_TCL:
				devices = Device.findAllByCategory(Category.RDKB)
				break
			case Category.RDKV:
				devices = Device.findAllByCategory(Category.RDKV)
				break
			default: break
		}
		devices
	}
	def getScriptList(){
		List scriptList = []
		Map scriptGroupMap = [:]
		List dirList = [
			Constants.COMPONENT,
			Constants.INTEGRATION
		]
		dirList.each{ directory ->
			File scriptsDir = new File( "${request.getRealPath('/')}//fileStore//testscripts//"+directory+"//")
			if(scriptsDir.exists()){
				def modules = scriptsDir.listFiles()
				modules.each { module ->

					File [] files = module.listFiles(new FilenameFilter() {
								@Override
								public boolean accept(File dir, String name) {
									return name.endsWith(".py");
								}
							});


					files.each { file ->
						String name = file?.name?.replace(".py", "")
						scriptList.add(name)
					}

				}
			}
		}

		scriptList.sort();

		return scriptList
	}

	/**
	 * Method to get the current date and time from server
	 * to display in execution name field of execution page
	 * @return
	 */
	def showDateTime(){
		def listdate = []
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
		Calendar cal = Calendar.getInstance()
		listdate << dateFormat.format(cal.getTime()).toString()
		render listdate as JSON
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

	/**
	 * Method to return the real path of the application both windows and linux pc
	 * @return
	 */
	def String getRealPath(){
		/*String osName = System.getProperty(OS_NAME)
		 if(osName?.startsWith(OS_WINDOWS)){
		 String s = request.getSession().getServletContext().getRealPath("/")
		 s = s.replace( '\\', '/' )
		 return s
		 }*/
		return request.getSession().getServletContext().getRealPath(Constants.FILE_SEPARATOR)
	}


	/**
	 * REST interface to support script execution with the parameters passed.
	 * @param stbName
	 * @param boxType
	 * @param suiteName
	 * @return
	 */
	def thirdPartyTest(final String stbName, final String boxType, final String imageName, final String suiteName, final String test_request, final String callbackUrl, final String timeInfo,final String  performance, final String isLogReqd, final String reRunOnFailure ){
		JsonObject jsonOutData = new JsonObject()
		try {
			String htmlData = ""
			String outData = ""
			String  url = getApplicationUrl()
			def execName = ""
			def isBenchMark1 = FALSE
			def isSystemDiagnostics1 = FALSE
			def isLogReqd1 = FALSE
			def rerun1 = FALSE

			if(timeInfo != null ){
				isBenchMark1 = timeInfo
			}
			if(performance != null  ){
				isSystemDiagnostics1 = performance
			}
			if(isLogReqd != null ){
				isLogReqd1  = isLogReqd

			}
			if(reRunOnFailure != null ){
				rerun1 = reRunOnFailure
			}

			String filePath = "${request.getRealPath('/')}//fileStore"
			if(test_request){
				String status = scriptexecutionService.generateResultBasedOnTestRequest(test_request,callbackUrl,filePath, url, imageName, boxType,getRealPath())
				if(status){
					jsonOutData.addProperty("status", "SUCCESS");
					jsonOutData.addProperty("result", "Result will be send with callback url");
				}
				else{
					jsonOutData.addProperty("status", "FAILED");
					jsonOutData.addProperty("result", "Error! Please try again");
				}
			}
			else{

				ScriptGroup scriptGroup = ScriptGroup.findByName(suiteName)
				def scriptStatusFlag
				def scriptVersionFlag
				Device deviceInstance
				def deviceNotExistStatus = ""
				def deviceNotExistCnt = 0
				def deviceList = stbName.split(',')
				def executionNameForCheck
				def validTclScripts = []
				deviceList.each{

					String stbname = it.toString().trim()
					deviceInstance = Device.findByStbName(stbname)
					if(deviceInstance){

						if(deviceInstance?.boxType?.name.equals(boxType.trim())){

							if(scriptGroup){
								def category = scriptGroup?.category
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
								scriptGroup?.scriptList?.each{ scrpt ->
									if(scriptGroup.category != Category.RDKB_TCL){
										def script = scriptService.getScript(getRealPath(), scrpt?.moduleName, scrpt?.scriptName, category?.toString())

										if(script){
											/**
											 * Checks whether atleast one script matches with the box type of device.
											 * If so execution will proceed with that one script
											 */
											if(executionService.validateScriptBoxTypes(script,deviceInstance)){
												scriptStatusFlag = true
												if(executionService.validateScriptRDKVersions(script,rdkVersion)){
													scriptVersionFlag = true
												}
											}
										}
									}
									else{
										def scriptExists = Utility.isTclScriptExists(getRealPath(), scrpt?.scriptName)
										def deviceConfigExists = Utility.isConfigFileExists(getRealPath(), deviceInstance?.stbName)
										if(scriptExists && deviceConfigExists){
											validTclScripts << Boolean.TRUE
										}
									}
								}
								def totalStatus = scriptStatusFlag && scriptVersionFlag
								if(totalStatus || !validTclScripts.isEmpty()){
									String status = ""
									try {
										status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)

										synchronized (lock) {
											if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
												status = "BUSY"
											}else{
												if((status.equals( Status.FREE.toString() ))){
													if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
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
									}
									status = status.trim()
									if((status.equals( Status.FREE.toString() ))){
										if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
											executionService.deviceAllocatedList.add(deviceInstance?.id)
										}
										def scriptname
										def deviceName
										ExecutionDevice executionDevice
										def execution
										def executionSaveStatus = true

										/**
										 * Even if there is multiple devices, the execution instance need to be created only once.
										 * 'executionNameForCheck' is used to bypass the creation of execution instance
										 */
										if(!executionNameForCheck){
											DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
											Calendar cal = Calendar.getInstance()
											deviceName = deviceInstance?.stbName
											execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()

											if(deviceList.size() > 1 ){
												executionNameForCheck = execName
												deviceName = MULTIPLE
											}

											try {
												
												// for saving the execution details includes the performance information
												//executionSaveStatus = executionService.saveExecutionDetails(execName, scriptname, deviceName, scriptGroup,url,isBenchMark1,isSystemDiagnostics1,rerun1,isLogReqd1)
												executionSaveStatus = executionService.saveExecutionDetails(execName,[scriptName:scriptname, deviceName:deviceName, scriptGroupInstance:scriptGroup,
													appUrl:url, isBenchMark:isBenchMark1, isSystemDiagnostics:isSystemDiagnostics1, rerun:rerun1, isLogReqd:isLogReqd1,category:category.toString(), rerunOnFailure:FALSE  ])
												//
												//	executionSaveStatus = scriptexecutionService.saveExecutionDetails(execName, scriptname, deviceName, scriptGroup,url, category)
											} catch (Exception e) {
												executionSaveStatus = false
											}
										}
										if(executionSaveStatus){
											execution = Execution.findByName(execName)
											try{
												executionDevice = new ExecutionDevice()
												executionDevice.execution = execution
												executionDevice.dateOfExecution = new Date()
												executionDevice.device = deviceInstance?.stbName
												executionDevice.boxType = deviceInstance?.boxType?.name
												executionDevice.deviceIp = deviceInstance?.stbIp
												executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
												executionDevice.status = UNDEFINED_STATUS
												executionDevice.category = category
												if(executionDevice.save(flush:true)){
													String getRealPathString  = getRealPath()
													executionService.executeVersionTransferScript(getRealPathString,filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
													//	scriptexecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance,url, filePath, getRealPathString, callbackUrl, imageName, category )
													def rerun = null
													if(rerun1?.equals(TRUE)){
														rerun = "on"
													}
													if(category == Category.RDKB_TCL){
														tclExecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance, url, filePath, getRealPathString, callbackUrl, imageName, isBenchMark1,isSystemDiagnostics1,rerun,isLogReqd1, category?.toString())
													}
													else{
														scriptexecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance, url, filePath, getRealPathString, callbackUrl, imageName, isBenchMark1,isSystemDiagnostics1,rerun,isLogReqd1, category?.toString())
													}
												}
											}
											catch(Exception e){
											}
										}
										else{
											deviceNotExistCnt++
											outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
										}
									}
									else if(status.equals( Status.ALLOCATED.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.NOT_FOUND.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.HANG.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.BUSY.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}else if(status.equals( Status.TDK_DISABLED.toString() )){
										deviceNotExistCnt++
										outData = outData + "TDK is not enabled  in the Device to execute scripts"

									}
									else{
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
								}
								else{
									deviceNotExistCnt++
									if(!scriptStatusFlag){
										outData = outData +" BoxType of Scripts in ScriptGroup is not matching with BoxType of Device ${deviceInstance?.stbName}"
									}else if(!scriptVersionFlag){
										outData = outData +" RDK Version of Scripts in ScriptGroup is not matching with RDK Version of Device ${deviceInstance?.stbName}"
									}
								}
							}
							else{
								deviceNotExistCnt++
								outData = outData + " Script Group does not exist"
							}
						}
						else{
							deviceNotExistCnt++
							outData = outData + " Mismatch between the device ${stbname} and box type ${boxType}"
						}
					}
					else{
						deviceNotExistCnt++
						outData = outData + " - Device ${it} not found"
					}
				}

				if(deviceNotExistCnt < deviceList.size()){
					//  url = url + "/execution/showResult?execName=${execName}&scrGrp=${scriptGroup?.id}"
					url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
					jsonOutData.addProperty("status", "RUNNING"+outData)
					jsonOutData.addProperty("result", url)
				}
				else{
					url = outData
					jsonOutData.addProperty("status", "FAILURE")
					jsonOutData.addProperty("result", url)
				}
			}
		} catch (Exception e) {
		}
		render jsonOutData
	}
	/** 
	 * REST method to retrieve the device status list
	 * @param boxType
	 * @return
	 */
	def getDeviceStatusList(String boxType){
		JsonObject devices = new JsonObject()
		try {
			if(boxType == null){
				def deviceList = Device.list()
				deviceList?.each{ device ->
					//devices.addProperty(device.stbName.toString()+LEFT_PARANTHESIS+device.stbIp.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device.boxType.toString()+RIGHT_PARANTHESIS, device.deviceStatus.toString())
					// ISSUE - FIX: Adding device category to the JSON
					devices.addProperty(device?.stbName.toString()+LEFT_PARANTHESIS+device?.stbIp.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device.boxType.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device?.category?.toString()+RIGHT_PARANTHESIS,device.deviceStatus.toString())
				}
			} else {
				JsonArray devArray = new JsonArray()
				def devList
				BoxType	boxTypeObj = BoxType.findByName(boxType)
				if(boxTypeObj){
					devList = Device.findAllByBoxType(boxTypeObj)
				}
				if(boxType && !boxTypeObj){
					devices.addProperty("status", "failure")
					devices.addProperty("remarks", "no box type found with name "+boxType)
				} else{
					if(devList){
						devList?.each{ dev ->
							JsonObject device = new JsonObject()
							device.addProperty("name", dev?.stbName)
							device.addProperty("boxtype", dev?.boxType?.name)
							//adding category of device - broadband or video
							device.addProperty("category", dev?.category?.toString())
							if(dev?.boxType?.type?.equals("Client")){
								if(dev?.gatewayIp){
									device.addProperty("gateway", dev?.gatewayIp)
								}
								if(dev?.isChild == 1){
									device.addProperty("macid", dev?.macId)
									device.addProperty("mocachild", "true")
								}else{
									device.addProperty("mocachild", "false")
									device.addProperty("ip", dev?.stbIp)
								}
							}else{
								device.addProperty("ip", dev?.stbIp)
							}
							device.addProperty("status", dev?.deviceStatus.toString())
							devArray.add(device)
						}
					}
					devices.add("devices",devArray)
				}
			}
		} catch (Exception e) {

		}
		render devices
	}

	def getDeviceStatus(final String stbName, final String boxType){
		JsonObject device = new JsonObject()
		try {
			if(stbName && boxType)	{
				def deviceInstance = Device.findByStbName(stbName)//,BoxType.findByName(boxType.trim()))
				device.addProperty(deviceInstance.stbName.toString()+LEFT_PARANTHESIS+deviceInstance.stbIp.toString()+RIGHT_PARANTHESIS, deviceInstance.deviceStatus.toString())
			}
		} catch (Exception e) {
		}
		render device
	}

	def getRealtimeDeviceStatus(final String stbName, final String boxType){
		JsonObject device = new JsonObject()
		try {
			def deviceInstance = Device.findByStbName(stbName)
			def status = Status.NOT_FOUND?.toString()
			if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				status = Status.BUSY?.toString()
			}
			else{
				status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
			}

			if(stbName && boxType)	{
				device.addProperty(deviceInstance.stbName.toString()+LEFT_PARANTHESIS+deviceInstance.stbIp.toString()+RIGHT_PARANTHESIS, status)
			}
			if(!deviceInstance?.deviceStatus.equals(status)){
				Thread.start{
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, status)
				}
			}
		} catch (Exception e) {

		}
		render device
	}

	def thirdPartyJsonResult(final String execName, final String appurl ){
		JsonObject executionNode = scriptexecutionService.thirdPartyJsonResultFromController(execName, getApplicationUrl() ,getRealPath())
		render executionNode
	}

	def thirdPartyJsonPerformanceResult(final String execName, final String appurl ){
		Execution executionInstance = Execution.findByName(execName)
		if(executionInstance?.script && executionInstance?.executionStatus?.equals(COMPLETED_STATUS)){
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		}else{
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		}
		JsonObject executionNode = scriptexecutionService.thirdPartyJsonPerformanceResultFromController(execName, getApplicationUrl() ,getRealPath())
		render executionNode
	}


	/**
	 * Execute the script
	 * @return
	 */
	def executeScriptMethod() {
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
		String boxType
		boolean allocated = false
		boolean singleScript = false
		String rerunOnFailure =FALSE

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
		if(!(params?.name)){
			htmlData = message(code: 'execution.name.blank')
		}
		else if(executionInstance){
			htmlData = message(code: 'execution.name.duplicate')
		}
		else if(!(params?.devices)){
			htmlData = message(code: 'execution.nodevice.selected')
		}
		else if(!params?.scriptGrp && !params?.scripts){
			htmlData = message(code: 'execution.noscript.selected')
		}

		else if(deviceInstance?.deviceStatus.toString().equals(Status.BUSY.toString())){
			htmlData =deviceName+ " : "+message(code: 'execution.device.notfree')
		}
		else if(deviceInstance?.deviceStatus.toString().equals(Status.NOT_FOUND.toString())){
			htmlData =deviceName+" : "+ message(code: 'execution.device.notfree')
		}
		else if(deviceInstance?.deviceStatus.toString().equals(Status.HANG.toString())){
			htmlData = deviceName+ " : "+message(code: 'execution.device.notfree')
		}else if(deviceInstance?.deviceStatus.toString().equals(Status.TDK_DISABLED.toString()))	{
			htmlData= deviceName+ " : "+message(code: 'execution.device.notfree')
		}
		else if(repeatCount == 0){
			htmlData = "Give a valid entry in repeat"
		}
		else{
			StringBuilder output = new StringBuilder();

			if(deviceList.size() > 1){
				output.append("Multiple Device Execution ")
			}
			def category = params?.category?.trim()
			if(!"RDKB_TCL".equals(category)){
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
					String url = getApplicationUrl()
					String filePath = "${request.getRealPath('/')}//fileStore"
					def execName
					def executionNameForCheck


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
									def moduleName= scriptService.scriptMapping.get(params?.scripts)
									if(moduleName){
										def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, params?.scripts, params?.category)
										if(scriptInstance1){
											if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
												String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
												if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
													validScript = true
												}else{
													htmlData = "<br>"+deviceName +"  : RDK Version supported by the script is not matching with the RDK Version of selected Device "+deviceInstance?.stbName+"<br>"
												}
											}else{
												htmlData = "<br>"+deviceName +" : "+ message(code: 'execution.boxtype.nomatch')
											}
										}else{
											htmlData = "<br>"+deviceName +"  : No Script is available with name ${params?.scripts} in module ${moduleName}"
										}
									}else{
										htmlData = "<br>"+deviceName +" : No module associated with script ${params?.scripts}"
									}
								}
								else{
									scripts.each { script ->										
										def moduleName= scriptService.scriptMapping.get(script)
										def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, script, params?.category)
										if(scriptInstance1){
											if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
												String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
												if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
													validScript = true
												}
											}
										}
									}

								}
							}else{
								def scriptGroup = ScriptGroup.findById(params?.scriptGrp,[lock: true])
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);								
								try{
									scriptGroup?.scriptList?.each{ script ->

										def scriptInstance1 = scriptService.getMinimalScript(getRealPath(),script?.moduleName, script?.scriptName, params?.category)

										/**
										 * Checks whether atleast one script matches with the box type of device.
										 * If so execution will proceed with that one script
										 */
										if(scriptInstance1 && executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
											if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
												validScript = true
												throw new Exception("return from closure")
											}
										}
									}
								}catch(Exception e ){
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

									synchronized (lock) {
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

								}
								catch(Exception eX){
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
											//							scriptInstance = Script.findById(params?.scripts,[lock: true])
											def moduleName= scriptService.scriptMapping.get(params?.scripts)
											def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, params?.scripts, params?.category)
											//							def scriptInstance1 = executionService.getScript(getRealPath(),"ClosedCaption", scripts)
											scriptStatus = executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)
											String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
											scriptVersionStatus = executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)
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
												executionSaveStatus = executionService.saveExecutionDetailsOnMultipleScripts(execName, scriptName, deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun,isLogReqd,scriptCount, params?.category,rerunOnFailure)
											}else{
												//executionSaveStatus = executionService.saveExecutionDetails(execName, scriptName, deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun,isLogReqd)

												executionSaveStatus = executionService.saveExecutionDetails(execName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance,
													appUrl:url, isBenchMark:isBenchMark, isSystemDiagnostics:isSystemDiagnostics, rerun:rerun, isLogReqd:isLogReqd,category:params?.category , rerunOnFailure:rerunOnFailure])
											}

											//	executionSaveStatus = executionService.saveExecutionDetails(execName, [scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance, url : url, isBenchMark : isBenchMark, isSystemDiagnostics: isSystemDiagnostics,, rerun : rerun, isLogReqd:isLogReqd, category: params?.category])

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
												executionDevice.boxType = deviceInstance?.boxType?.name
												executionDevice.deviceIp = deviceInstance?.stbIp
												executionDevice.status = UNDEFINED_STATUS
												executionDevice.category = Utility.getCategory(params?.category)
												executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
												executionDevice.save(flush:true)
											}
											catch(Exception e){
												e.printStackTrace()
											}
											def scriptId
											if((!(params?.scriptGrp)) && (!(params?.scripts))){
												render ""
												return
											}
											else{
												executionService.executeVersionTransferScript(request.getRealPath('/'),filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
											}
											if(deviceList.size() > 1){
												executescriptService.executeScriptInThread(execName, device, executionDevice, params?.scripts, params?.scriptGrp, executionName,
														filePath, getRealPath(), params?.myGroup, url, isBenchMark, isSystemDiagnostics, params?.rerun,isLogReqd, params?.category)
												htmlData=" <br> " + deviceName+"  :   Execution triggered "
												output.append(htmlData)


											}else{
												htmlData = executescriptService.executescriptsOnDevice(execName, device, executionDevice, params?.scripts, params?.scriptGrp, executionName,
														filePath, getRealPath(), params?.myGroup, url, isBenchMark, isSystemDiagnostics, params?.rerun,isLogReqd, params?.category)
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

									else{
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
									}
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
												execution.isRerunRequired = rerun?.equals(TRUE)
												execution.isBenchMarkEnabled = isBenchMark?.equals(TRUE)
												execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals(TRUE)
												execution.isStbLogRequired = isLogReqd?.equals(TRUE)
												execution.rerunOnFailure = rerunOnFailure?.equals(TRUE)
												execution.outputData = "Execution failed due to the unavailability of box"
												if(! execution.save(flush:true)) {
													log.error "Error saving Execution instance : ${execution.errors}"
												}
											}
											catch(Exception th) {
												th.printStackTrace()
											}
										}

										htmlData = "<br>"+deviceName+" : "+message(code: 'execution.device.notfree')
										output.append(htmlData)
									}
								}
							}else{
								if(!singleScript){
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
							deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
						}

					}
				}
				htmlData = output.toString()
			}
			else{
				htmlData = tclExecutionService.executeTclScripts(params, getRealPath(), getApplicationUrl())
			}
		}
		render htmlData
	}
	/**
	 * show execution result via link 
	 * @return
	 */
	def showExecutionResult(){
		String data = ""
		if(params?.execResult){
			ExecutionResult exResult = ExecutionResult.get(params?.execResult)
			data = exResult?.executionOutput
		}else{
			data = "Log data not available"
		}
		render data
	}


	def showAgentLogFiles(){
		def agentConsoleFileData = executionService.getAgentConsoleLogData( request.getRealPath('/'), params?.execId, params?.execDeviceId,params?.execResId)
		if(agentConsoleFileData.isEmpty()){
			agentConsoleFileData = "Unable to fetch Agent Console Log"
		}
		render(template: "agentConsoleLog", model: [agentConsoleFileData : agentConsoleFileData])
	}
	
	/**
	 * Method to fetch the execution details
	 * @return
	 */
	def getExecutionDetails(){
		def exRes = ExecutionResult.get(params?.execResId)
		render(template: "executionDetails", model: [executionResultInstance : exRes])
	}

	def showLogFiles(){

		def logFileNames = executionService.getLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId, params?.execResId )
		render(template: "logFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, execResId : params?.execResId, logFileNames : logFileNames])
	}

	def showCrashLogFiles(){
		def crashlogFileNames = executionService.getCrashLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId, params?.execResId)
		render(template: "crashLogFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, execResId : params?.execResId, logFileNames : crashlogFileNames])
	}

	/**
	 * Method to display the script execution details in the popup.
	 * @return
	 */
	def showLog(){
		Execution executionInstance = Execution.findById(params?.id)
		//	if(!executionInstance.isPerformanceDone){
		executionService.setPerformance(executionInstance,request.getRealPath('/'))
		//}
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup

		def executionResultMap = [:]
		def statusResultMap = [:]

		def totalStatus = ["ALL"]
		def totalStatusList = ["SUCCESS", "FAILURE", "N/A", "SKIPPED", "PENDING", "TIMED OUT", "UNDEFINED"]
		def listStatusCount = [:]

		executionDeviceList.each { executionDevice ->
			ArrayList executionList = new ArrayList(executionDevice.executionresults);
//			executionResultMap.put(executionDevice, executionList)

			listStatusCount = executedbService.getStatusList(executionInstance,executionDevice,executionList.size().toString())
			totalStatusList.each {
				def status = it;
				def statusCount = listStatusCount.get(status)
				if(status == "TIMED OUT"){
					status = "SCRIPT TIME OUT"
				}
				if(statusCount!= null && Integer.parseInt(statusCount) > 0) {
					if(totalStatus.indexOf(status) == -1) {
						totalStatus.add(status)
					}
				}
			}
			statusResultMap.put(executionDevice, listStatusCount)
		}

		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}
		[statusResults : statusResultMap, executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:executionResultMap , statusList: totalStatus]
	}

	/**
	 * Method to display the script execution details in the popup.
	 * @return
	 */
	def showResult(final String execName,final String scrGrp){
		Execution executionInstance = Execution.findByName(execName)
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup
		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}
		[executionInstance : executionInstance, executionDeviceInstanceList : executionDevice, testGroup : testGroup ]
	}

	/**
	 * Show the log files
	 * @return
	 */
	def showExecutionLog()  {
		try {
			String fileName = params?.id
			int index = fileName.indexOf( UNDERSCORE )
			def executionId = fileName.substring( 0, index )
			String filePath = "${request.getRealPath('/')}//logs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.id

			def file = new File(filePath)
			if(!file?.exists()){
				String name =  params?.id.substring(index+1, params?.id?.length())
				filePath = "${request.getRealPath('/')}//logs//stblogs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+name
				file = new File(filePath)
			}
			response.setContentType("html/text")
			response.setHeader("Content-disposition", "attachment;filename=${file.getName()}")
			response.outputStream << file.newInputStream()
		} catch (FileNotFoundException fnf) {
			response.sendError 404
		}
	}


	/**
	 * Show the log files
	 * @return
	 */
	def showCrashExecutionLog()  {
		try {
			String fileName = params?.id
			int index = fileName.indexOf( UNDERSCORE )
			def executionId = fileName.substring( 0, index )
			String filePath = "${request.getRealPath('/')}//logs//crashlogs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.id
			def file = new File(filePath)
			response.setContentType("html/text")
			response.setHeader("Content-disposition", "attachment;filename=${file.getName()}")
			response.outputStream << file.newInputStream()
		} catch (FileNotFoundException fnf) {
			response.sendError 404
		}
	}

	/**
	 * TO DO : Remove this once the device status checking is done.
	 * Reset the device status to FREE.
	 * Called only when the user is sure that the test execution ended
	 * without giving any result or the device is not reachable
	 * @param id
	 * @return
	 */
	def resetDevice(Long id) {
		def deviceInstance = Device.get(id)
		if (!deviceInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'device.label', default: 'Device'), deviceInstance.stbName])
			redirect(action: "list")
			return
		}
		else{
			Device.withTransaction { status ->
				try {
					deviceInstance.deviceStatus = Status.FREE
					deviceInstance.save(flush:true)
					status.flush()
				}
				catch(Throwable th) {
					status.setRollbackOnly()
				}
			}
		}
	}
	/**
	 * Check device is enable or not
	 * 
	 */


	def resetDeviceStatus(Long id){

		def deviceInstance = Device.get(id)
		if (!deviceInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'device.label', default: 'Device'), deviceInstance.stbName])
			redirect(action: "list")
			return
		}
		else{
			Device.withTransaction { status ->
				try {
					deviceInstance.deviceStatus = Status.TDK_DISABLED
					deviceInstance.save(flush:true)
					status.flush()
				}
				catch(Throwable th) {
					status.setRollbackOnly()
				}
			}
		}
	}


	/**
	 * REST API : To save the load module status
	 * @param executionId
	 * @param resultData
	 * @return
	 */
	def saveLoadModuleStatus(final String execId, final String statusData, final String execDevice, final String execResult){
		//		executescriptService.saveLoadModuleStatus(execId, statusData, execDevice, execResult)

		try {
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
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * REST API : To save the result details
	 * @param executionId
	 * @param resultData
	 * @return
	 */
	def saveResultDetails(final String execId, final String resultData, final String execResult,
			final String expectedResult, final String resultStatus, final String testCaseName, final String execDevice)
	{

		try{
			if(resultData){
				String actualResult = resultData
				if(actualResult){
					ExecutionResult.withTransaction {
						ExecutionResult executionResult = ExecutionResult.findById(execResult)
						if(executionResult){
							ExecuteMethodResult executionMethodResult = new ExecuteMethodResult()
							if(resultStatus?.equals( STATUS_NONE ) || resultStatus == null ){
								executionMethodResult.status = actualResult
							}
							else{
								executionMethodResult.executionResult = executionResult
								executionMethodResult.expectedResult = expectedResult
								executionMethodResult.actualResult = actualResult
								executionMethodResult.status = resultStatus
							}
							executionMethodResult.functionName = testCaseName
							executionMethodResult.category = executionResult?.category
							executionMethodResult.save(flush:true)

							executionResult?.addToExecutemethodresults(executionMethodResult)
							executionResult?.save(flush:true)

							Execution execution = Execution.findById(execId)
							ExecutionDevice execDeviceInstance = ExecutionDevice.findById(execDevice)
							if(!executionResult?.status.equals( FAILURE_STATUS )){
								executionResult?.status = resultStatus
								executionResult?.save(flush:true)
								if(!execution.result.equals( FAILURE_STATUS )){
									execution.result = resultStatus
									execution.save(flush:true)
								}
								if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
									execDeviceInstance?.addToExecutionresults(executionResult)
									execDeviceInstance?.status = resultStatus
									execDeviceInstance?.save(flush:true)
								}
							}
						}
					}
				}
			}
			else{
				Execution.withTransaction {
					Execution execution = Execution.findById(execId)
					if(execution){
						execution.result = FAILURE_STATUS
						execution.save(flush:true)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace()
		}
	}

	/**
	 * Search execution list based on the execution name
	 * @return
	 */
	def searchExecutionList(){
		def executionList = []
		def executions = Execution.findAllByNameLike("%${params?.searchName.trim()}%")
		if(executions?.size() > 0){
			executions.each{ execution ->
				executionList.add(execution)
			}
		}else{
			executions = Execution.findAllByScriptGroupLike("%${params?.searchName.trim()}%")
			if(executions?.size() >0){
				executions.each{ execution ->
					executionList.add(execution)
				}
			}
			executions = Execution.findAllByScriptLike("%${params?.searchName.trim()}%")
			if(executions?.size() >0){
				executions.each{ execution ->
					executionList.add(execution)
				}
			}else{
				String searchString = params?.searchName.trim()
				if(searchString?.equalsIgnoreCase("SUCCESS")){
					searchString = "COMPLETED"
				}
				executions = Execution.findAllByExecutionStatusLike("%${searchString}%")
				if(executions?.size() >0){
					executions.each{ execution ->
						executionList.add(execution)
					}
				}else{
				searchString = searchString?.trim()
				def executionDevices = ExecutionDevice.findAllByBuildNameLike("%${searchString}%")
				if(executionDevices?.size() >0){
					executionDevices.each{ execDev ->
						executionList.add(execDev?.execution)
					}
				}
				}
			}

		}
		render(template: "searchList", model: [executionInstanceList : executionList])
	}

	/**
	 * Search execution list based on different search criterias of
	 * script, device, and execution from and to dates.
	 * @return
	 */
	def multisearch(){
		def executionList = executionService.multisearch( params?.toDate?.trim(), params?.fromDate?.trim(), params?.deviceName?.trim(), params?.resultStatus?.trim(),
				params?.scriptType?.trim(), params?.scriptVal?.trim() )
		render(template: "searchList", model: [executionInstanceList : executionList])
	}


	/**
	 * TO DO : Remove this once the port forwarding is automated via config file during reboot.
	 * It is called during free state
	 * Called only when the user is want to reset all rules.
	 * 
	 * @param id
	 * @return
	 */
	def resetIPRule(Long id) {
		def device = Device.get(id)
		if (!device) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'device.label', default: 'Device'),
				device.stbName
			])
			redirect(action: "list")
			return
		}
		else{
			deviceStatusService.resetIPRule(device)
		}
	}

	/**
	 * Method export the execution details to excel format.
	 * This method will be called upon clicking excel export button in execution page.
	 * The method will parse all the child attributes of the execution object to corresponding maps.
	 * Finally all this data will be pushed to excel sheet at a particular format.
	 * The resulting excel sheet will be available in downloads folder of running browser.
	 * 
	 * @param id - Id of execution object.
	 * 
	 */
	def exportToExcel = {

		if(!params.max) params.max = 100000
		List dataList = []
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList =  [0.35, 0.5]

		Execution executionInstance = Execution.findById(params.id)
		try {
			if(executionInstance){
				dataList = executedbService.getDataForExcelExport(executionInstance, getRealPath())
				fieldMap = ["C1":"     ", "C2":"     "]
				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList ]
			}
			else{
				log.error "Invalid excution instance......"
			}
		} catch (Exception e) {
			println "ee "+e.getMessage()
			e.printStackTrace()
		}

		params.format = EXPORT_EXCEL_FORMAT
		params.extension = EXPORT_EXCEL_EXTENSION
		response.contentType = grailsApplication.config.grails.mime.types[params.format]

		def fileName = executionInstance.name
		fileName = fileName?.replaceAll(" ","_")
		response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ fileName +".${params.extension}")
		exportService.export(params.format, response.outputStream,dataList, null,fieldMap,[:], parameters)
		log.info "Completed excel export............. "

		/*********** csv support***************************/                                //TODO Use this if csv support needed
		def type = params.type
		if(type){
			params.format = "csv"
			response.contentType = 'text/csv'

			def filName = "ExecutionReport-"+ executionInstance.name + ".csv"
			response.setHeader("Content-disposition", "attachment; filename="+filName+";sheetname=MySheet")
			exportService.export(params.format, response.outputStream,dataList, fieldLabels,fieldMap,[:], [:])
		}
	}

	// For CGRTS-521
	def getExecutionOutput(final String execResId){
		ExecutionResult executionResult = ExecutionResult.findById(execResId)
		def data

		if(executionResult){
			data = executionResult?.executionOutput
		}
		render data
	}


	/**
	 * Method to export the consolidated report in excel format.
	 */
	def exportConsolidatedToExcel = {
		if(!params.max) params.max = 100000
		Map dataMap = [:]
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = [0.08,0.4,0.15,0.2,0.15,0.8,0.2,0.2,0.2,0.8]

		Execution executionInstance = Execution.findById(params.id)
		String executionInstanceStatus ;
		executionInstanceStatus =executedbService?.isValidExecutionAvailable(executionInstance)
		if(executionInstanceStatus?.equals(Constants.SUCCESS_STATUS)){

			if(executionInstance){
				dataMap = executedbService.getDataForConsolidatedListExcelExport(executionInstance, getRealPath(),getApplicationUrl())
				fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":"Executed","C4":" Status ", "C5":"Executed On ","C6":"Log Data","C7":"Jira #","C8":"Issue Type","C9":"Remarks","C10":" Agent Console Log"]

				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
			}
			else{
				log.error "Invalid excution instance......"
			}

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = executionInstance.name
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ fileName +".${params.extension}")
			excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
		else{
			redirect(action: "create");
			flash.message= "No valid execution reports are available."
			return
		}

	}
	
	/**
	 * Method used to populate individual execution result
	 */
	def resultSummary = {
		Execution executionInstance = Execution.findById(params?.executionId)
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup

		def executionResultMap = [:]
		def statusResultMap = [:]

		def logData = "Could not find the logs"
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
		[statusResults : statusResultMap, executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:executionResultMap, baseUrl:params?.baseUrl]
	}

	/**
	 * Method to export the consolidated report in zip format.
	 */	
	def exportConsolidatedToZip = {

		String url =  "${request.getRequestURL()}"
		String hostname = url.split("://")[1].split(":")[0];
		String portnumber = url.split("://")[1].split(":")[1].split("/")[0];
		String protocol = url.split("://")[0]
		String appName = url.split("://")[1].split(":")[1].split("/")[1]

		String baseUrl = protocol + "://" +hostname + ":" + portnumber + "/" + appName + "/"
		String idVal = params?.id


		def executionId = idVal.replace("_zip", "")

		def urlNew = (baseUrl + "execution/resultSummary?executionId=" + executionId+"&baseUrl=" +baseUrl).toURL()
		def data = ""

		def result = []
		urlNew.eachLine {
			result << it
		}


		try {
			Execution exec = Execution.get(executionId)
			String fileName = exec?.name
			if(exec){
				ZipOutputStream zipFile = new ZipOutputStream(new FileOutputStream("result"))
				zipFile.putNextEntry(new ZipEntry(fileName + ".html"))
				def buffer = new byte[1024]
				
				for(int i=0; i< result.size(); i++){
					data = result[i] + "\n"
					zipFile.write(data.bytes, 0, data.bytes.size())
				}
				
				zipFile.closeEntry()
				zipFile.close()


				params.format = EXPORT_ZIP_FORMAT
				params.extension = EXPORT_ZIP_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				fileName = fileName?.replaceAll(" ","_")
				def file = new File("result")
				response.setHeader("Content-Type", "application/zip")
				response.setHeader("Content-disposition", "attachment; filename=ExecutionLogs_"+ fileName +".zip")
				response.outputStream << file.newInputStream()
				response.outputStream.flush()
				flash.message = "Exported successfully"
			} else {
				flash.message =  "Couldn't find exceution!!"
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to export the consolidated report in excel format.
	 */
	def exportConsolidatedPerfToExcel = {
		if(!params.max) params.max = 100000
		Map dataMap = [:]
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = [0.08,0.4,0.15,0.2,0.2,0.2,0.8,0.15,0.2,0.2,0.8]

		Execution executionInstance = Execution.findById(params.id)
		String executionInstanceStatus ;
		executionInstanceStatus =executedbService?.isValidExecutionAvailable(executionInstance)
		if(executionInstanceStatus?.equals(Constants.SUCCESS_STATUS)){

			if(executionInstance){
				dataMap = executedbService.getDataForConsolidatedListPerformanceExcelExport(executionInstance, getRealPath(),getApplicationUrl())
				fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":"Executed","C4":" Status ","C5":"Script Execution Time","C6":"Executed On ","C7":"Log Data","C8":"Jira #","C9":"Issue Type","C10":"Remarks","C11":" Agent Console Log"]

				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
			}
			else{
				log.error "Invalid excution instance......"
			}

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = executionInstance.name
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ fileName +".${params.extension}")
			excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
		else{
			redirect(action: "create");
			flash.message= "No valid execution reports are available."
			return
		}

	}
	
	/**
	 * To download the test result comparison report
	 */
	def exportComparisonReport = {
		if(!params.max) params.max = 100000
		Map dataMap = [:]
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = [0.08,0.4,0.2]

		Execution executionInstance = Execution.findById(params.id)
		Execution [] executionList = Execution.findAllByScriptGroupAndNameNotEqualAndExecutionStatusNotEqual(executionInstance.scriptGroup,executionInstance?.name,Constants.ABORTED_STATUS,[max: 5, sort: "id", order: "desc"])
		def nameList = executionList?.name
		def colNameList = ["C4","C5","C6","C7","C8"]
		def fieldList = ["C1","C2","C3"]
		String executionInstanceStatus ;
		executionInstanceStatus =executedbService?.isValidExecutionAvailable(executionInstance)
		if(executionInstanceStatus?.equals(Constants.SUCCESS_STATUS)){

			if(executionInstance){
				int i = 0
				fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":executionInstance?.name]
				nameList?.each{ name ->
					fieldMap.put(colNameList.get(i), name)
					fieldList.add(colNameList.get(i))
					columnWidthList.add(0.2)
					i++
				}
				
				dataMap = executedbService.getDataForComparisonExcelExport(executionList, executionInstance , getRealPath(),getApplicationUrl(),fieldList)
				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
			}
			else{
				log.error "Invalid excution instance......"
			}

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = executionInstance.name
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+EXPORT_COMPARE_FILENAME+ fileName +".${params.extension}")
			excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
		else{
			redirect(action: "create");
			flash.message= "No valid execution reports are available."
			return
		}

		
	}

	/**
	 * Method to perform delete operation for marked results.
	 * This method will be invoked by an ajax call.
	 * It removes all the child objects of given execution instance.
	 * 
	 * @param - Ids of checked execution results.
	 * @return - JSON message
	 * 
	 */
	def deleteExecutioResults = {

		List executionResultList = []
		List executionMethodResultInstanceList = []
		def selectedRows
		List returnMsg = []
		int deleteCount = 0
		String message

		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){

			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
			deleteCount =  executedbService.deleteSelectedRowOfExecutionResult(selectedRows,getRealPath())

			if(deleteCount == 1){
				message = deleteCount+" Result Deleted"
			}
			else if (deleteCount > 1){
				message =  deleteCount+" Results Deleted"
			}
			else{
				message = "Delete failed"
				flash.message="Delete failed due to the pending execution"
			}

			returnMsg.add( message)
			render returnMsg as JSON
		}
		else{
			log.info "Invalid marking of results for deletion"
		}
	}
	
	/**
	 * Method which filters executions based on FromDate, ToDate, boxType, Category and script type
	 */

	def filterExecutions(){
		def validate = params?.validate
		def checker = 0
		String messageDiv = ""
		List executionList =[]
		List executionIdList = []
		SimpleDateFormat myFormat = new SimpleDateFormat("MM/dd/yyyy");
		String dateBeforeString = params?.generateFromDate?.trim()
		String dateAfterString = params?.generateToDate?.trim()
		Date dateBefore = myFormat.parse(dateBeforeString);
		Date dateAfter = myFormat.parse(dateAfterString);
		long difference = dateAfter.getTime() - dateBefore.getTime();
		float daysBetween = (difference / (1000*60*60*24));
		daysBetween=(int)daysBetween;
		if(daysBetween > 30){
			checker = 1;
			messageDiv = "Maximum number of days allowed is 30"
		}
		else{
			String fromDateString = params?.generateFromDate?.trim()
			def fromDateList = fromDateString.split("/")
			def year = fromDateList[2]
			def month = fromDateList[0]
			def day = fromDateList[1]
			String fromDate = year + "-" + month + "-" +day + " 00:00:00"
			String toDateString = params?.generateToDate?.trim()
			def toDateList = toDateString.split("/")
			year = toDateList[2]
			month = toDateList[0]
			day = toDateList[1]
			String toDate = year + "-" + month + "-" +day + " 23:59:59"
			executionList = executionService.filterExecutions( fromDate, toDate, params?.boxType?.trim(), params?.category?.trim(),params?.scriptTypeValue?.trim(),params?.scriptValue?.trim())		
			executionList.each {eachExecution ->
				executionIdList.add(eachExecution.id)
			}
		}
		render(template: "combinedExcelList", model: [executionInstanceList : executionList,executionIdList : executionIdList,checker:checker,messageDiv:messageDiv,validate:validate])
	}	
	
	/**
	 * Method to check whether the selected executions have the same device type. 
	 * The list of all the selected executions is passed as params from the gsp page. This method is invoked 
	 * from the execution_resolver.js
	 */
	def checkValidExecutions(){
		def selectedRows
		def selectedRowsDefined = []
		String sameType
		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){
			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
			if((selectedRows.size() > 10) || (selectedRows.size() < 2)){
				sameType = "overFlow"
			}
			else{
				sameType = "true"
			}
		}
		render sameType
		return
	}
	
	/**
	 * Method to export the combined report of the selected executions in excel format. The selected executions
	 * must of the same device type. This method is called from execution_resolver.js
	 */

	def combinedExcelReportGeneration = {
		def selectedRows
		def selectedRowsDefined = []
		def executionInstance
		def executionDevice
		Map dataMap = [:]
		Map fieldMap = [:]
		Map parameters = [:]
		List fieldLabels = []
		List columnWidthList = [0.08,0.4,0.15,0.2,0.15,0.8,0.2,0.2,0.2,0.8]
		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){
			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
			for(int i=0;i<selectedRows.size();i++){
				if(selectedRows[i] != UNDEFINED){
					selectedRowsDefined.add(selectedRows[i])
				}
			}
			dataMap = executedbService.getDataForCombinedExcelReportGeneration(selectedRowsDefined ,getApplicationUrl())
			//For excel generation
			fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":"Executed","C4":" Status ", "C5":"Executed On ","C6":"Log Data","C7":"Jira #","C8":"Issue Type","C9":"Remarks","C10":" Agent Console Log","C11":"Rerun/Repeat"]
			parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def executionInstanceId = selectedRowsDefined.get(0)
			executionInstance = Execution.findById(executionInstanceId)
			def fileName = ""
			if(executionInstance){
				fileName = executionInstance.name
			}
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+COMBINED_EXPORT_FILENAME+ fileName +".${params.extension}")
			excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
	}
	
	/**
	 * Ajax call to update the isMarked status of execution instance.
	 * This will be called during mark operation of corresponding checkbox of execution results.
	 */
	def updateMarkStatus = {
		int markStatus
		markStatus = Integer.parseInt(params?.markStatus)
		try {
			Execution.withTransaction {
				Execution executionInstance = Execution.findById(params?.id)
				if(executionInstance){
					executionInstance.isMarked = markStatus
					executionInstance.save(flush:true)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Download the execution result details in xml format
	 * @return
	 */
	def writexmldata(){
		String writer = executedbService.getExecutionDataInXmlFormat(params?.execName)
		response.setHeader "Content-disposition", "attachment; filename=${params?.execName}.xml"
		response.contentType = 'text/xml'
		response.outputStream << writer.toString()
		response.outputStream.flush()
	}

	def readOutputFileData(String executionName){
		String output = "";
		try{
			String pathName = Constants.SCRIPT_OUTPUT_FILE_PATH+executionName+Constants.SCRIPT_OUTPUT_FILE_EXTN
			File opFile = grailsApplication.parentContext.getResource(pathName).file
			List opList ;
			if(opFile.exists()){
				opList = opFile.readLines();
			}else{
				opList = []
				String opFolderName = Constants.SCRIPT_OUTPUT_FILE_PATH
				File opFolder = grailsApplication.parentContext.getResource(opFolderName).file
				if(opFolder.exists()){
					File[] files = opFolder.listFiles(new CustomFileNameFilter(executionName));
					for (int i=0; i< files.length;i++) {
						List opList1 = files[i].readLines();
						if(opList1 != null && opList1.size() > 0){
							opList.addAll(opList1);
						}
					}
				}
			}

			for (var in opList) {
				output = output + var
			}
		}catch(Exception e){
		}
		render output as String
	}

	/**
	 * REST Api : Get the detailed result based on a execution Result
	 * @param execResId
	 * @return
	 */
	def getDetailedTestResult(final String execResId){
		JsonObject resultNode = new JsonObject()
		if(execResId){
			ExecutionResult executionResult = ExecutionResult.findById(execResId)
			JsonArray jsonArray = new JsonArray()
			JsonObject functionNode = new JsonObject()

			resultNode.addProperty("ExecutionName",executionResult?.execution?.name.toString())
			resultNode.addProperty("Device",executionResult?.device.toString())
			resultNode.addProperty("Script",executionResult?.script.toString())
			resultNode.addProperty("Status",executionResult?.status.toString())
			executionResult?.executemethodresults.each{ execMethdRslt ->
				functionNode = new JsonObject()
				functionNode.addProperty("FunctionName", execMethdRslt?.functionName.toString())
				functionNode.addProperty("ExpectedResult", execMethdRslt?.expectedResult.toString())
				functionNode.addProperty("ActualResult", execMethdRslt?.actualResult.toString())
				functionNode.addProperty("Status", execMethdRslt?.status.toString())
				jsonArray.add(functionNode)
			}
			resultNode.add("Functions",jsonArray)
			resultNode.addProperty("LogData",executionResult?.executionOutput.toString())
			//agent console link added
			def executionInstance = Execution.findById(executionResult?.execution?.id)
			resultNode.addProperty("agentConsoleLogURL",executionInstance?.applicationUrl+"/execution/getAgentConsoleLog?execResId="+executionResult?.id)
		}
		render resultNode
	}

	def getAgentConsoleLog(final String execResId){

		ExecutionResult executionResult = ExecutionResult.findById(execResId)

		def agentConsoleFileData = "No AgentConsoleLog available"

		if(executionResult){

			try {
				agentConsoleFileData = executionService.getAgentConsoleLogData( request.getRealPath('/'), executionResult?.execution?.id?.toString(), executionResult?.executionDevice?.id?.toString(),executionResult?.id?.toString())
				if(agentConsoleFileData){
					agentConsoleFileData =agentConsoleFileData.trim()
					if(agentConsoleFileData.length() == 0){
						agentConsoleFileData = "No AgentConsoleLog available"
					}
				}else{
					agentConsoleFileData = "No AgentConsoleLog available"
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}else{
			agentConsoleFileData = "No execution result available with the given execResId"
		}
		render agentConsoleFileData
	}

	/**
	 * REST Api : Get the detailed result based on a execution Result
	 * @param execResId
	 * @return
	 */

	def getClientPort(final String deviceIP,final String agentPort){
		JsonObject resultNode = null
		if(deviceIP && agentPort){
			Device device = Device.findByStbIpAndStbPort(deviceIP,agentPort)
			if(device){
				resultNode = new JsonObject()
			//	resultNode.addProperty("logTransferPort",device?.logTransferPort.toString())
				resultNode.addProperty("logTransferPort",device?.agentMonitorPort?.toString())
				resultNode.addProperty("statusPort",device?.statusPort.toString())
			}
		}
		render resultNode
	}
	/**
	 * check the box is enabled/disabled
	 */
	def getTDKDeviceStatus()
	{
		try{
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//setTDKStatus.py").file
			def absolutePath = layoutFolder.absolutePath
			Device device = Device.get(params?.select)
			def option = params?.option
			String[] cmd= [
				"python",
				absolutePath,
				device,
				device?.statusPort,
				option
			]

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def outputData = scriptExecutor.executeScript(cmd,1)
		}

		catch(Exception e){
			println e.getMessage()
			e.printStackTrace()
		}
	}

	/**
	 * method to stop the execution through ui request
	 */
	def stopExecution(){
		Execution execution = Execution.findById(params?.execid)
		def listdate = []
		if(execution?.executionStatus.equals(INPROGRESS_STATUS)){
			def executionId = params?.execid?.toString()
			if(!executionService.abortList.contains(executionId)){
				executionService.abortList.add(executionId)
			}else{
				listdate.add("Request to stop already in progress")
			}
		}else if(execution?.executionStatus.equals("PAUSED")){
			executionService.saveExecutionStatus(true, execution?.id)
		}

		render listdate as JSON
	}


	/**
	 * REST API to request for stopping the test execution 
	 * @param executionName
	 * @return
	 */
	def stopThirdPartyTestExecution(final String executionName){
		JsonObject result = new JsonObject()
		result.addProperty("ExecutionName", executionName)
		try {
			Execution execution = Execution.findByName(executionName)
			if(execution?.executionStatus.equals(INPROGRESS_STATUS)){

				if(execution?.script && !execution?.script?.equals(MULTIPLESCRIPT) ){
					try {

						if(!executionService.abortList.contains(execution?.id?.toString())){
							executionService.abortList.add(execution?.id?.toString())
							result.addProperty("Status", "Requested for abort")
						}else{
							result.addProperty("Status", "Request to stop already in progress")
						}

						if(executionService.executionProcessMap.containsKey(executionName)){
							Process process = executionService.executionProcessMap.get(executionName)
							if(process){
								process.waitForOrKill(1)
								process.destroy()
							}
						}
					} catch (Exception e) {
						println " Execption "+e.getMessage()
						e.printStackTrace()
					}

				}else{
					if(!executionService.abortList.contains(execution?.id?.toString())){
						executionService.abortList.add(execution?.id?.toString())
						result.addProperty("Status", "Requested for abort")
					}else{
						result.addProperty("Status", "Request to stop already in progress")
					}
					if(executionService.executionProcessMap.containsKey(executionName)){
						Process process = executionService.executionProcessMap.get(executionName)
						if(process){
							process.waitForOrKill(1)
							process.destroy()
						}
					}

				}
			}else if(execution?.executionStatus.equals("PAUSED")){
				executionService.saveExecutionStatus(true, execution?.id)
				result.addProperty("Status", "Requested for abort")
			} else{
				if(execution != null){
					result.addProperty("Status", "Error. No execution found in this name in IN-PROGRESS / PAUSED state to stop")
				}else{
					result.addProperty("Status", "Error. No execution found in this name")
				}
			}
			render result
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Method to fetch the device status of the selected device
	 * @return
	 */
	def updateDeviceStatus(){
		def device = Device.get( params?.id )
		try {
			String status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, device)
			deviceStatusService.updateOnlyDeviceStatus(device, status);
			def result1
			def deviceInstanceList = null
			def category = params?.category?.trim()
			if(Category.RDKV.toString().equals(category)){
				deviceInstanceList = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKV, [order: 'asc', sort: 'stbName'])
			}
			else if(Category.RDKB.toString().equals(category)){
				deviceInstanceList = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKB, [order: 'asc', sort: 'stbName'])
			}
			result1 = [url: getApplicationUrl(), deviceList : deviceInstanceList, deviceInstanceTotal: deviceInstanceList?.size()]

			render view:"devicelist", model:result1
		} catch (Exception e) {
		}
	}

	def getDeviceStatusListData(){
		try {
			//def deviceInstanceList = Device.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'stbName'])
			def deviceInstanceListV = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKV, [order: 'asc', sort: 'stbName'])
			def deviceInstanceListB = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKB, [order: 'asc', sort: 'stbName'])
			def result1 = [url: getApplicationUrl(), deviceListV : deviceInstanceListV, deviceListB:deviceInstanceListB, deviceInstanceTotalV: deviceInstanceListV?.size(), deviceInstanceTotalB: deviceInstanceListB?.size()]

			render view:"devicelist", model:result1
		} catch (Exception e) {
		}
	}
	/*
	 * Date based execution History table clean up
	 */

	def deleteExecutions(){

		def deleteCount = 0
		try {

			List<Execution> executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${params?.cleanFromDate}' and '${params?.cleanToDate}' ")
			List executionResultList = []
			List executionMethodResultInstanceList = []
			List performanceList = []
			executionList?.each{ executionInstance ->

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
									executionResultInstance.delete(flush:true)
								}
							}


							if(executionInstance?.thirdPartyExecutionDetails){
								executionInstance?.thirdPartyExecutionDetails = null;
								executionInstance?.save();
							}

							def thirdPartyExecutionDetailsList = ThirdPartyExecutionDetails.findAllByExecution(executionInstance)
							thirdPartyExecutionDetailsList.each{ thirdPartyExecution ->
								thirdPartyExecution.delete(flush:true)
							}

							def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
							executionDeviceList.each{ executionDeviceInstance ->
								executionDeviceInstance.delete(flush:true)
							}

							def execId = executionInstance?.id.toString()
							executionInstance.delete(flush:true)
							deleteCount ++
							log.info "Deleted "+executionInstance
							/**
							 * Deletes the log files, crash files
							 */
							String logFilePath = "${getRealPath()}//logs//"+execId
							def logFiles = new File(logFilePath)
							if(logFiles.exists()){
								logFiles?.deleteDir()
							}
							String crashFilePath = "${getRealPath()}//logs//crashlogs//"

							new File(crashFilePath).eachFileRecurse { file->
								if((file?.name).startsWith(execId)){
									file?.delete()
								}
							}
							String versionFilePath = "${getRealPath()}//logs//version//"+execId
							def versionFiles = new File(versionFilePath)
							if(versionFiles.exists()){
								versionFiles?.deleteDir()
							}

							String agentLogFilePath = "${realPath}//logs//consolelog//"+execId
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


		} catch (Exception e) {
			e.printStackTrace()
		}

		render deleteCount.toString()+" execution entries deleted"
	}

	def pushData(String exName,String moduleType){
		def realPath = getRealPath()
		ThirdPartyExecutionDetails.withTransaction {
			ThirdPartyExecutionDetails  thirdPartyExecutionDetails = ThirdPartyExecutionDetails.findByExecName(exName)
			if(thirdPartyExecutionDetails){
				scriptexecutionService.executeCallBackUrl(thirdPartyExecutionDetails.execName,thirdPartyExecutionDetails.url,thirdPartyExecutionDetails.callbackUrl,thirdPartyExecutionDetails.filePath,thirdPartyExecutionDetails.executionStartTime,thirdPartyExecutionDetails.imageName,thirdPartyExecutionDetails.boxType,realPath)
			}
		}
	}

	/**
	 * REST API for single test execution .
	 * @param stbName - name of the STB configured in Test Manager
	 * @param boxType - boxType of the STB like Hybrid-1, IPClient-3
	 * @param scriptName - Name if the script to be executed
	 * @return - Return JSON with status of REST call
	 */

	def thirdPartySingleTestExecution(final String stbName, final String boxType, final String scriptName , final String executionCount, final String reRunOnFailure, final String timeInfo,final String performance,final String isLogRequired){
		int exeCount = 1
		if(executionCount ){
			try {
				exeCount = Integer.parseInt(executionCount)
			} catch (Exception e) {
				e.printStackTrace()
			}
		}

		String rerun = FALSE
		if(reRunOnFailure && reRunOnFailure?.equals(TRUE)){
			rerun = TRUE
		}

		String time = FALSE
		if(timeInfo && timeInfo?.equals(TRUE)){
			time = TRUE
		}

		String perfo = FALSE
		if(performance && performance?.equals(TRUE)){
			perfo = TRUE
		}

		String isLog = FALSE
		if(isLogRequired && isLogRequired?.equals(TRUE)){
			isLog = TRUE
		}

		singleTestRestExecution(stbName,boxType,scriptName,exeCount,rerun,time,perfo,isLog)
	}

	//	def thirdPartySingleTestExecution(final String stbName, final String boxType, final String scriptName ){
	//		singleTestRestExecution(stbName,boxType,scriptName,1,FALSE,FALSE,FALSE)
	//	}

	def singleTestRestExecution(final String stbName, final String boxType, final String scriptName , final int repeat, final String reRunOnFailure, final String timeInfo,final String performance,final String isLog){
		def deviceInstance = Device.findByStbName(stbName)
		String  url = getApplicationUrl()
		String htmlData = ""
		def execName = ""
		def newExecName = ""
		String filePath = "${request.getRealPath('/')}//fileStore"
		boolean executed = false
		JsonObject jsonOutData = new JsonObject()
		String  sName = scriptName
		int i =0;
		boolean valid = false;
		boolean TCL = false;
		try {
			if(deviceInstance){
				def category = deviceInstance.category
				if(("RDKB".equals(category?.toString()))){
					if((scriptService?.tclScriptsList?.toString()?.contains(scriptName?.trim()))  ){
						TCL = true
					}
					if(!TCL){
					boolean compoundTCL = false
					def combainedTclScript =  scriptService?.combinedTclScriptMap
					combainedTclScript?.each{
						if(it?.value?.toString().contains(scriptName?.toString())){
							compoundTCL = true
						}
					}
					if((scriptService?.totalTclScriptList?.toString()?.contains(scriptName?.toString())) && compoundTCL ){
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(scriptName?.toString())){
								TCL = true
							}
						}
					}
					}
				}
				if(!TCL ){
					def moduleName= scriptService.scriptMapping.get(scriptName)
					if(moduleName){
						def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, scriptName, category.toString())
						if(scriptInstance1){
							//check whether the script is valid for this execution
							if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
								if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
									valid = true
								}else{
									htmlData = "RDK Version supported by the script is not matching with the RDK Version of selected Device "+deviceInstance?.stbName+"<br>"
								}
							}else{
								htmlData = message(code: 'execution.boxtype.nomatch')
							}
						}else{
							htmlData = "No Script is available with name ${scriptName} in module ${moduleName}"
						}
					}else{
						htmlData = "No module associated with script ${scriptName}"
					}

				}else{

					def scriptInstance1 = [:]
					boolean compoundTCL = false
					def combainedTclScript =  scriptService?.combinedTclScriptMap
					combainedTclScript?.each{
						if(it?.value?.toString().contains(sName)){
							compoundTCL = true
						}
					}
					if((scriptService?.totalTclScriptList?.toString()?.contains(sName)) && compoundTCL ){
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(sName)){
								sName = it.key?.toString()
							}
						}
					}
					def scriptValid = Utility.isTclScriptExists(realPath,  sName)
					if(scriptValid) {
						if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
							scriptInstance1.put('scriptName',sName )
							valid = true
						}
						else{
							htmlData = "<br>"+stbName +"  : No Config file is available with name Config_${deviceInstance?.stbName}.txt"
						}

					}else{
						htmlData = "<br>"+stbName +"  : No TCL Script is available with name ${scriptName}"
					}
				}
				String status = ""
				if(valid){
					try {
						status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)

						synchronized (lock) {
							if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
								status = "BUSY"
							}else{
								if(!status.equals( Status.FREE.toString() )){
									status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
								}
								if((status.equals( Status.FREE.toString() ))){
									if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
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
					}
			
				status = status.trim()
				//execute script only if the device is free
				if((status.equals( Status.FREE.toString() ))){
					if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						executionService.deviceAllocatedList.add(deviceInstance?.id)
					}

					def deviceName
					ExecutionDevice executionDevice
					def execution
					def executionSaveStatus = true
					DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
					Calendar cal = Calendar.getInstance()
					deviceName = deviceInstance?.stbName


					execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()
					newExecName = execName
					//execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()

					try {
						//									executionSaveStatus = scriptexecutionService.saveExecutionDetails(execName, scriptName, deviceName, null,url)
						//executionSaveStatus =  executionService.saveExecutionDetails(execName, scriptName, deviceName, null,url,timeInfo,performance,reRunOnFailure,FALSE)
						executionSaveStatus =  executionService.saveExecutionDetails(execName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:null,
							appUrl:url, isBenchMark:timeInfo, isSystemDiagnostics:performance, rerun:reRunOnFailure, isLogReqd:FALSE,category:category?.toString(),rerunOnFailure:FALSE])
					} catch (Exception e) {
						executionSaveStatus = false
					}

					if(executionSaveStatus){
						execution = Execution.findByName(execName)
						try{
							executionDevice = new ExecutionDevice()
							executionDevice.execution = execution
							executionDevice.dateOfExecution = new Date()
							executionDevice.device = deviceInstance?.stbName
							executionDevice.boxType = deviceInstance?.boxType?.name
							executionDevice.deviceIp = deviceInstance?.stbIp
							executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
							executionDevice.status = UNDEFINED_STATUS
							executionDevice.category = category
							if(executionDevice.save(flush:true)){
								String getRealPathString  = getRealPath()
								executionService.executeVersionTransferScript(getRealPathString,filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
								def rerun = null
								if(reRunOnFailure?.equals(TRUE)){
									rerun = "on"
								}

								if(repeat > 1){

								}else{
									if(!TCL ){
										htmlData = executescriptService.executeScriptInThread(execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
												filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,isLog,category?.toString())

										// The Execution is done through only one device
										//											htmlData = executescriptService.executescriptsOnDevice(execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
										//													filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,FALSE)

										executed = true
										println " singleTestRestExecution [stbName="+stbName+"] [scriptName="+scriptName+"]"+" [execName="+execName+"] [Triggered Execution]"
										url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
										jsonOutData.addProperty("status", "RUNNING")
										jsonOutData.addProperty("result", url)

									}else{
										tclExecutionService.executeScriptInThread(execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
												filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,isLog,category?.toString())
										executed = true
										url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
										jsonOutData.addProperty("status", "RUNNING")
										jsonOutData.addProperty("result", url)
									}

								}
							}
						}
						catch(Exception e){
							println " ERROR "+e.getMessage()
						}
					}
					else{
						htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
					}
				}
				else if(status.equals( Status.ALLOCATED.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.NOT_FOUND.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.HANG.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.BUSY.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}else if(status.equals( Status.TDK_DISABLED.toString() )){
					htmlData = htmlData + "TDK is not enabled  in the Device to execute scripts"

				}
				else{
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}

							
				}

			}else{
				htmlData = "No device found with this name "+stbName
			}
		} finally {
			if(!executed){
				println " singleTestRestExecution [stbName="+stbName+"] [scriptName="+scriptName+"] not executed "
				if(deviceInstance){
					if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						executionService.deviceAllocatedList.removeAll(deviceInstance?.id)
					}

					String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					Thread.start{
						deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
					}

					Thread.sleep(1000);

					Device devv = Device.get(deviceInstance?.id)					
						println "**["+ deviceInstance?.stbName+"] ["+  devStatus + "] ["+devv?.deviceStatus+"]"
					if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						println " Device instance is still there in the allocated list :  "+deviceInstance?.stbName + " id "+ deviceInstance?.id
						executionService.deviceAllocatedList.removeAll(deviceInstance?.id)
						println " Again checking the device lock  for "+deviceInstance?.stbName + " status =  "+executionService.deviceAllocatedList.contains(deviceInstance?.id)
					}
				}else{
					htmlData = "No device found with this name "+stbName
				}

					jsonOutData.addProperty("status", "FAILURE")
					jsonOutData.addProperty("result", htmlData)
				
			}
		}
		println " singleTestRestExecution [stbName="+stbName+"] [scriptName="+scriptName+"] [jsonOutData="+jsonOutData+"]"
		render jsonOutData
	}

	def clearDeviceAllocatedList(final String stbName){
		JsonObject result = new JsonObject()
		result.addProperty("stbName", stbName)
		
		def deviceInstance = Device.findByStbName(stbName)
		if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
			executionService.deviceAllocatedList.remove(deviceInstance?.id)
			result.addProperty("status", "cleared device allocation")
		}else{
			result.addProperty("status", "nothing to clear")
		}
		render result
	}

	/**
	 * Method to get the module wise execution status
	 */
	def executionStatus(){

		Execution executionInstance = Execution.findById(params?.id)

		def detailDataMap = executedbService.prepareDetailMap(executionInstance,request.getRealPath('/'))

		def tDataMap = [:]
		def  chartModuleDataList = []
		def barColors = []
		
		int total = 0
		detailDataMap?.keySet()?.each { k ->
			Map mapp = detailDataMap?.get(k)
			int tCount = 0
			mapp?.keySet()?.each { status ->

				def tStatusCounter = tDataMap.get(status)
				def statusCounter = mapp.get(status)
				if(!tStatusCounter){
					tStatusCounter = 0
				}
				if(!status.equals("PENDING")){
					tCount = tCount + statusCounter
					tStatusCounter = tStatusCounter + statusCounter
					tDataMap.put(status, tStatusCounter)
				}
			}
			
			int na = 0
			if(mapp?.keySet().contains("N/A")){
				na = mapp?.get("N/A")
			}
			
			mapp.put("Executed", tCount)
			def success = mapp?.get("SUCCESS")
			if(success){
				int rate = 0
				if(tCount > 0){
					if(mapp?.keySet().contains("N/A")){
						na = mapp?.get("N/A")
					}
					rate = ((success * 100)/(tCount - na))
				}
				mapp.put("passrate",rate)
				def statusData = []
				statusData.add("'"+k+"'")
				statusData.add(rate)
				chartModuleDataList.add(statusData)
				barColors.add("'"+getBarChartColors(rate)+"'")
			}
			total = total + tCount
		}
		
		tDataMap.put("Executed", total)
		int rate
		if(tDataMap?.get("SUCCESS")){
			int success = tDataMap?.get("SUCCESS")
			int na = 0
			if(tDataMap?.keySet().contains("N/A")){
				na = tDataMap?.get("N/A")
			}
			rate = ((success * 100)/(total - na))
		}

		tDataMap.put("passrate",rate)

		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup

		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}

		[statusResults : [:], executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:[:],detailDataMap:detailDataMap,tDataMap:tDataMap,chartModuleDataList:chartModuleDataList,barColors:barColors]

	}

	def File [] getFilesArray(def moduleObj ){
		List fileList = []
		File [] files = moduleObj?.listFiles();
		files?.each { ff ->
			if(ff?.name?.endsWith(".py")){
				fileList.add(ff)
			}
		}
		return files
	}

	/**
	 * Utility method to fetch the module wise script count details 
	 */
	def getScriptsDetails(){

		JsonObject scripts = new JsonObject()

		JsonArray jsonArray = new JsonArray()
		List scriptList = []

		List dirList = [
			Constants.COMPONENT,
			Constants.INTEGRATION
		]
		def start = System.currentTimeMillis()
		int moduleCount = 0;
		int total = 0
		dirList.each{ directory ->
			File scriptsDir = new File( "${realPath}//fileStore//testscripts//"+directory+"//")
			if(scriptsDir.exists()){
				File [] moduleArray = scriptsDir.listFiles()

				Arrays.sort(moduleArray);

				moduleArray.each { moduleObj ->
					moduleCount ++
					JsonObject jsonObj = new JsonObject()
					def start1 =System.currentTimeMillis()
					try {
						List files = getFilesArray(moduleObj)
						total = total + files?.size()
						jsonObj.addProperty(moduleObj?.name, ""+files?.size())
						jsonArray.add(jsonObj)
					}catch (Exception e) {
						println " Error  "+e.getMessage()
						e.printStackTrace()
					}
				}
			}
		}
		scripts.addProperty("modules", moduleCount)
		scripts.addProperty("total", total)
		scripts.add("details", jsonArray)
		String data = ""+scripts?.toString()
		render data
	}
	/**
	 * Function for using the repeat execution option in the show log page based on the  test suite / multiple script excution.
	 * params : -
	 * 		1) ExecutionName
	 * 		2) ScriptGroup
	 * 		3) Device
	 * 		4) Scripts
	 * 		5) BenchMark enabled 
	 * 		6) System Diagnostics enabled  
	 * 		7) Rerun 
	 * @return
	 */
	def repeatExecution(){	
		try{
			int execCnt = 0
			def executionInstance =  Execution.findByName(params?.executionName)			
			def  multipleScript = []
			def execName1 =  executionInstance?.name
			if(!(execName1.toString().contains("RERUN"))){
				int executionCount=0
				int execCount = 0
				int testCount = 0
				def repeatCount
				def newExecutionName
				def executionList = Execution?.findAll()
				if(Execution?.findByName(execName1?.toString())){
					def tempExecName = execName1?.toString()
					def executionDevice = executionInstance?.device	
					if(execName1?.toString()?.contains(executionDevice))
					{
						tempExecName = execName1?.toString()?.substring(executionDevice.length())
					}
					
					if(tempExecName?.contains("_"))
					{
						
						def namePart = execName1?.substring(0,execName1.lastIndexOf("_") )
						executionCount = getExecutionCountFromName(execName1)
						executionCount++
						newExecutionName = namePart + "_"+executionCount
						if(Execution?.findByName(newExecutionName?.toString())){
							def execList = Execution?.findAllByNameLike(namePart+"%", [order: "desc"])
							if(execList && execList?.size() > 0){
								executionCount = getExecutionCountFromName(execList?.get(0)?.name)
								executionCount++
								newExecutionName = namePart+"_"+(executionCount)
							}
						}
					}	
					else{
						newExecutionName = execName1 +"_"+1
						//if(executionList?.toString().contains(newExecutionName?.toString())){
						if(Execution.findByName(newExecutionName.toString())){
							def execList = Execution?.findAllByNameLike(execName1+"_%" , [order: "desc"])
							if(execList && execList?.size() > 0){
								executionCount = getExecutionCountFromName(execList?.get(0)?.name)
								executionCount++
								newExecutionName = execName1 +"_"+executionCount
							}
						}else{
							newExecutionName = newExecutionName
						}
					}
				}
				def executionInstance1 =  Execution.findByName(params?.executionName)
				def deviceInstance = Device?.findByStbName(params.device)
				String execName = newExecutionName
				def executionName =  execName
				def executionNameForCheck
				def isBenchMark = FALSE
				def isSystemDiagnostics = FALSE
				def isLogReqd = FALSE
				def rerun = FALSE
				boolean aborted = false
				def scriptGroupInstance
				if( executionInstance?.isBenchMarkEnabled){
					isBenchMark = TRUE
				}
				if(executionInstance?.isSystemDiagnosticsEnabled){
					isSystemDiagnostics =TRUE
				}
				if(executionInstance?.isStbLogRequired){
					isLogReqd = TRUE
				}
				String url = getApplicationUrl()
				String filePath = "${request.getRealPath('/')}//fileStore"
				boolean validScript = false
				def deviceId
				deviceId = deviceInstance?.id
				String devStatus = ""
				def scriptGroup
				boolean allocated = false
				try {
					devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					synchronized (lock) {
						if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
							devStatus = "BUSY"
						}else{
							if((devStatus.equals( Status.FREE.toString() ))){
								if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
									allocated = true
									executionService.deviceAllocatedList.add(deviceInstance?.id)
									Thread.start{
										deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.FREE.toString())
									}
								}
							}
						}
					}
				}
				catch(Exception eX){
					log.error "Error "+eX.getMessage()
					eX.printStackTrace()
				}
				if(params?.scriptGroup){
					scriptGroupInstance  =  ScriptGroup?.findByName(params?.scriptGroup,[lock: true])
				}
				def scripts = null
				def saveExecutionDetails = true
				if( devStatus.equals( Status.FREE.toString())){
					if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						allocated = true
						executionService.deviceAllocatedList.add(deviceInstance?.id)
					}
					int scriptCnt = 0
					if(scriptGroupInstance?.scriptList?.size() > 0){
						scriptCnt= scriptGroupInstance?.scriptList?.size()
					}
					def executionDevice
					def execResult

					if(params?.script?.toString().equals(MULTIPLESCRIPT)){
						execResult = ExecutionResult?.findAllByExecution(executionInstance)
						int scriptCount  = execResult?.size()
						
						//For multiple script execution
						//saveExecutionDetails = executionService.saveExecutionDetailsOnMultipleScripts(execName?.toString(), MULTIPLESCRIPT, deviceInstance?.toString(), scriptGroupInstance,url?.toString(),isBenchMark?.toString(),isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),scriptCount,)
						saveExecutionDetails= executionService.saveExecutionDetails(execName?.toString(),[scriptName:MULTIPLESCRIPT, deviceName:deviceInstance?.toString(), scriptGroupInstance:scriptGroupInstance,
													appUrl:url?.toString(), isBenchMark:isBenchMark?.toString(), isSystemDiagnostics:isSystemDiagnostics?.toString(), rerun:rerun?.toString(), isLogReqd:isLogReqd?.toString(),category:executionInstance1?.category?.toString(), rerunOnFailure : FALSE])
					}else{						//For test suite execution
						//saveExecutionDetails = executionService.saveExecutionDetails(execName?.toString(), scripts, deviceInstance?.toString(), scriptGroupInstance ,url?.toString(),isBenchMark?.toString(),isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString())
					saveExecutionDetails= executionService.saveExecutionDetails(execName?.toString(),[scriptName:scripts, deviceName:deviceInstance?.toString(), scriptGroupInstance:scriptGroupInstance,
						appUrl:url?.toString(), isBenchMark:isBenchMark?.toString(), isSystemDiagnostics:isSystemDiagnostics?.toString(), rerun:rerun?.toString(), isLogReqd:isLogReqd?.toString(),category:executionInstance1?.category?.toString(), rerunOnFailure:FALSE])
					}
					if(saveExecutionDetails){
						try {
							executionDevice = new ExecutionDevice()
							executionDevice.execution = Execution.findByName(execName)
							executionDevice.dateOfExecution = new Date()
							executionDevice.device = deviceInstance?.stbName
							executionDevice.boxType = deviceInstance?.boxType?.name
							executionDevice.deviceIp = deviceInstance?.stbIp
							executionDevice.status = UNDEFINED_STATUS
							executionDevice.category = Utility.getCategory(deviceInstance?.category?.toString())
							executionDevice.save(flush:true)
						}catch (Exception e ){
							log.error "Error "+e.getMessage()
							e.printStackTrace()
						}
						if(saveExecutionDetails){
							if(params?.scriptGroup){
								scriptGroupInstance  =  ScriptGroup?.findByName(params?.scriptGroup,[lock: true])
							}
							String myGroup = ""
							if(params?.script?.toString()?.equals("Multiple Scripts")){
								myGroup = SINGLE_SCRIPT
								scripts = execResult?.script

							} else{
								myGroup = "TestSuite"

							}							
	if(executionInstance1?.category?.toString().equals(RDKB_TCL)){
								tclExecutionService?.executescriptsOnDevice(execName?.toString(), deviceId?.toString(), executionDevice, scripts, scriptGroupInstance?.id.toString(), executionName?.toString(),
									filePath, getRealPath(),myGroup?.toString(), url?.toString(), isBenchMark?.toString(), isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),executionInstance1?.category?.toString())
							}else{
								executescriptService.executescriptsOnDevice(execName?.toString(), deviceId?.toString(), executionDevice, scripts, scriptGroupInstance?.id.toString(), executionName?.toString(),
									filePath, getRealPath(),myGroup?.toString(), url?.toString(), isBenchMark?.toString(), isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),executionInstance1?.category?.toString())
							}
							/*executescriptService.executescriptsOnDevice(execName?.toString(), deviceId?.toString(), executionDevice, scripts, scriptGroupInstance?.id.toString(), executionName?.toString(),
									filePath, getRealPath(),myGroup?.toString(), url?.toString(), isBenchMark?.toString(), isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),deviceInstance.category?.toString())*/

						}else{
							flash.message =  " Save Execution status is null  "
						}
					}else{
						flash.message = "Execution Details not saved  properly "
					}
				}else {
					flash.message= " Device Status is BUSY  so not possible trigger the execution "
				}
			}else{
				flash.message = " Execution name contains the RERUN"
			}
		} catch(Exception e){
			println "ERROR "+ e.getMessage()
			e.printStackTrace()
		}
		redirect( view:"create")
	}
	
	/**
	 * Function for getting the next repeat count
	 * @return executionCount
	 */
	def getExecutionCountFromName(String execName){
		int executionCount = 0
		if(execName?.toString()?.contains("_")){
			def countPart = execName?.substring(execName.lastIndexOf("_") + 1, execName.length())
			if(countPart){
				try {
					executionCount =Integer.parseInt(countPart)
				} catch (Exception e) {
					e.printStackTrace()
				}
			}
		}
		return executionCount
	}
	
	/**
	 * Function for rerun on failure option in the show log page 
	 * Execute failure scripts according to the test suite which user selection.
	 * @return
	 */

	def rerunOnFailure(){
		try{
			String devStatus = ""
			def deviceInstance
			String url = getApplicationUrl()
			String filePath = "${request.getRealPath('/')}//fileStore"
			def executionInstance = Execution?.findByName(params?.executionName)
			if(params.device){
				deviceInstance = Device.findByStbName(params.device)
				//issue fixing for device status not updated properly 
				//devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				//if(devStatus.equals( Status.FREE.toString())){
				if(deviceInstance?.deviceStatus?.toString()?.equals(Status.FREE.toString())){					
					def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
					def executionResultList
					executionDeviceList.each {  execDeviceInstance ->
						ExecutionResult.withTransaction {
							executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
						}
					}
					boolean value  = false
					executionResultList.each{ executionResultInstance ->
						if(executionResultInstance?.status.equals("FAILURE") || executionResultInstance?.status.equals("SCRIPT TIME OUT")){
							value = true
						}
					}
					if(value ==  true ){
						String uniqueName = executionInstance?.toString()+"12"
						//ISSUE fix
						//executescriptService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() , params?.executionName?.toString(),uniqueName?.toString(), url?.toString(), deviceInstance?.category?.toString() )
						if(!(executionInstance?.category?.toString()?.equals(RDKB_TCL))){
							executescriptService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() , params?.executionName?.toString(),uniqueName?.toString(), url?.toString(), executionInstance?.category?.toString() )
						}else{
							tclExecutionService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() , params?.executionName?.toString(),uniqueName?.toString(), url?.toString(), executionInstance?.category?.toString())
						}
					}else{
						flash.message = "Failue script list not found in the suite"
					}
				}else {
					flash.message =" Device is not free to execute"
				}
			}
		}catch(Exception e){
			println "ERROR "+ e.getMessage()
			e.printStackTrace()
		}
		redirect(view : "create")
	}
	def failureScriptCheck(){
		def executionInstance = Execution?.findByName(params?.executionName)
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def executionResultList
		executionDeviceList.each {  execDeviceInstance ->
			ExecutionResult.withTransaction {
				executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
			}
		}
		boolean value  = false
		executionResultList.each{ executionResultInstance ->
			if(executionResultInstance?.status.equals("FAILURE") || executionResultInstance?.status.equals("SCRIPT TIME OUT")){
				value = true
			}
		}
		render value
	}	
	/**
	 * REST API :- for fetching execution id with execution name , include the following
	 * - Execution Name
	 * - Execution Id
	 * - If Status  failed  display message  like "no executions found with name "
	 *
	 */
	def getExecutionId(final String executionName){
		JsonObject executionObj = new JsonObject()
			if(executionName)	{
				def executionInstance = Execution?.findByName(executionName)
				if(executionInstance){
					executionObj?.addProperty("ExecutionName ",executionInstance?.name)
					executionObj.addProperty("ExecutionId",executionInstance?.id)
				}else{
					executionObj?.addProperty("Status","FAILURE")
					executionObj.addProperty("Remarks ", "no executions found with name "+ executionName)
				}
			}
		render executionObj
	}
	
	/**
	 * REST API :- fetching image name using execution name . It will include the following
	 * - Execution Name
	 * - Execution Device
	 * - Image Name
	 */
	def getImageName(final String executionName){
		JsonObject executionObj = new JsonObject()
		if(executionName){
			def executionInstance = Execution?.findByName(executionName)
			if(executionInstance){
				executionObj?.addProperty("ExecutionName ",executionInstance?.name)
				executionObj.addProperty("DeviceName",executionInstance?.device)
				def device =  ExecutionDevice?.findByExecution(executionInstance)
				def versionFilePath = "${realPath}//logs//version//${executionInstance?.id}//${device.id.toString()}"
				String fileName  = versionFilePath+"//"+device?.id+"_version.txt"
				def file = new File( fileName)
				if(file?.isFile()){
					def  lines = file?.readLines()
					def imageNameDetails
					if(lines?.size() > 0){
						lines?.each{
							if(it?.toString()?.contains("imagename")){
								imageNameDetails = it?.toString()
								imageNameDetails = imageNameDetails.replace("=",":")
							}
						}
						if(imageNameDetails){
							def imageName = imageNameDetails?.split(":")
							if(imageName.size() > 1 && imageName[0]?.toString()?.equals("imagename")){
								executionObj?.addProperty("ImageName",imageName[1])
							}else{
								executionObj?.addProperty("ImageName","Image name not available")
							}
						}else{
							executionObj?.addProperty("ImageName","Image name not available")
						}
					}
				}else{
					executionObj?.addProperty("ImageName","Image name not available")
				}
			}else{
				executionObj?.addProperty("Status","FAILURE")
				executionObj.addProperty("Remarks ", "no executions found with name "+ executionName)
			}
		}
		render executionObj
	}
	
	/**
	 * REST API :- For fetching all execution names greater than the perticular date of execution
	 * - Return execution name
	 * - date of execution
	 * - Execution Status
	 * - Failure status
	 * - All  execution list
	 * @param dateOfExecution
	 * @return
	 */
	def getExecutionList(final String dateOfExecution){
		JsonArray totalExecutionList = new JsonArray()
		if(dateOfExecution){
		try{
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:SS.s");
			Date dateObj = new Date().parse("yyyy-MM-dd hh:mm:SS.s", dateOfExecution)
			def executionList = Execution.withCriteria{
				ge("dateOfExecution", dateObj)
			}
			executionList.each{execution->
				JsonObject executionObj = new JsonObject()
				executionObj.addProperty("ExecutionName",execution?.name?.toString())
				executionObj.addProperty("DateOfExecution",execution?.dateOfExecution?.toString())
				executionObj.addProperty("ExecutionStatus",execution?.executionStatus)
				totalExecutionList.add(executionObj)
			}
		}catch(Exception e){
			JsonObject errorObj =  new JsonObject()
			errorObj.addProperty("Status","FAILURE")
			errorObj.addProperty("Remarks "," Invalid date format ")
			totalExecutionList.add(errorObj)
		}
		}else{
			def executionList = Execution.findAll()
			executionList.each{  execution ->
				JsonObject executionObj = new JsonObject()
				executionObj.addProperty("ExecutionName",execution?.name?.toString())
				executionObj.addProperty("DateOfExecution",execution?.dateOfExecution?.toString())
				executionObj.addProperty("ExecutionStatus",execution?.executionStatus)
				totalExecutionList.add(executionObj)
			}
		}
		render totalExecutionList
	}
	
/**
	 * REST API : for executing multiple script
	 *  Input parameter
	 *  	- scripts : script list
	 *  	- stbName :  device name
	 *  	- reRunOnFailure
	 *  	- timeInfo
	 *  	- performance
	 *  	- isLogRequired
	 */

	def thirdPartyMultipleScriptExecution(final String scripts, final String stbName ,final String reRunOnFailure, final String timeInfo,final String performance,final String isLogRequired ){
		String rerun = FALSE
		if(reRunOnFailure && reRunOnFailure?.equals(TRUE)){
			rerun = TRUE
		}
		String time = FALSE
		if(timeInfo && timeInfo?.equals(TRUE)){
			time = TRUE
		}
		String perfo = FALSE
		if(performance && performance?.equals(TRUE)){
			perfo = TRUE
		}
		String isLog = FALSE
		if(isLogRequired && isLogRequired?.equals(TRUE)){
			isLog = TRUE
		}
		JsonObject jsonOutData = new JsonObject()
		boolean validScript = false
		boolean  scriptStatusFlag = false
		boolean  scriptVersionFlag = false
		String outData = ""
		def executionNameForCheck
		String filePath = "${request.getRealPath('/')}//fileStore"
		String htmlData = ""
		def scriptList  = scripts.tokenize(",")
		def deviceInstance = Device.findByStbName(stbName)
		def newScriptList = []
		boolean executed = false
		boolean valid = false;
		boolean TCL = false;
		def category
		def newCategory
		if(deviceInstance){
			category = deviceInstance.category
			if(scriptList?.size() > 0){
				int i =0;
				String scriptType  = MULTIPLESCRIPT
				def moduleInstance
				scriptList.each { script ->
					
					if(category?.toString()?.equals(RDKB)){
						def scriptName
						if((scriptService?.tclScriptsList?.toString()?.contains(script?.trim()))  ){
							TCL = true
						}
						scriptName = script?.toString()
						boolean compoundTCL = false
						def combainedTclScript =  scriptService?.combinedTclScriptMap
						combainedTclScript?.each{
							if(it?.value?.toString().contains(script)){
								compoundTCL = true
							}
						}
						if((scriptService?.totalTclScriptList?.toString()?.contains(script)) && compoundTCL ){
							combainedTclScript?.each{
								if(it?.value?.toString()?.contains(script)){
									scriptName= script?.toString()
									script = it.key?.toString()
									TCL = true
								}
							}
						}
						if(Utility.isTclScriptExists(realPath,  script)) {
							if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
								if(compoundTCL){
									newScriptList << scriptName
								}else{
									newScriptList << script
								}
								validScript = true
								valid =true
								TCL = true
							}
							else{
								outData = "   No Config file is available with name Config_${deviceInstance?.stbName}.txt"
							}
						}else{
							outData = "   No TCL Script is available with name ${script}"
						}
					}					
					if(TCL?.toString()?.equals(FALSE)){
						def moduleName= scriptService.scriptMapping.get(script)
						if( moduleName){
							moduleInstance= Module?.findByName(moduleName)
							def scriptInstance1 = scriptService?.getScript(getRealPath()?.toString(),moduleInstance?.toString(), script?.toString(), moduleInstance?.category?.toString())
							if(scriptInstance1){
								if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
									scriptStatusFlag = true
									String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
									if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
										scriptVersionFlag = true
										validScript = true
										newScriptList << script
									}
								}
							}
						}
					}
				}
				if(validScript && newScriptList?.size() > 0 ){
					if(!TCL){
						if(scriptStatusFlag && scriptVersionFlag){
							valid = true
						}else {
							valid = false
						}
					}
					if(valid){
						String status = ""
						try {
							status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
							synchronized (lock) {
								if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
									status = "BUSY"
								}else{
									if((status.equals( Status.FREE.toString() ))){
										if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
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
						}
						if((status.equals( Status.FREE.toString() ))){
							try{
								if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
									executionService.deviceAllocatedList.add(deviceInstance?.id)
								}
								//	def newCategory
								if(!TCL){
									newCategory = moduleInstance?.category
								}else{
									newCategory = RDKB_TCL
								}
								
								def execution
								def executionSaveStatus = true
								DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
								Calendar cal = Calendar.getInstance()
								def deviceName = deviceInstance?.stbName
								String  url = getApplicationUrl()
								def execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()
								def newExecName = execName
								if(scriptType.equals(MULTIPLESCRIPT)){
									def  scriptCount = newScriptList?.size()
									executionSaveStatus = executionService.saveExecutionDetailsOnMultipleScripts(execName?.toString(), MULTIPLESCRIPT, deviceName, null,url,time,perfo,rerun,isLog,scriptCount, newCategory?.toString(),FALSE)
								}
								if(executionSaveStatus){
									try{
										execution = Execution.findByName(execName)
										def executionDevice = new ExecutionDevice()
										executionDevice.execution = execution
										executionDevice.dateOfExecution = new Date()
										executionDevice.device = deviceInstance?.stbName
										executionDevice.boxType = deviceInstance?.boxType?.name
										executionDevice.deviceIp = deviceInstance?.stbIp
										executionDevice.status = UNDEFINED_STATUS
										executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
										//executionDevice.category = moduleInstance?.category
										executionDevice.category =Utility.getCategory(newCategory?.toString())
										if(executionDevice.save(flush:true)){
											String getRealPathString  = getRealPath()
											executionService.executeVersionTransferScript(getRealPathString,filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort, url)
											if(!TCL){
												htmlData = executescriptService.executeScriptInThread(execName, ""+deviceInstance?.id, executionDevice, newScriptList, "", execName,
														filePath, getRealPath(), SINGLE_SCRIPT, url, time, perfo, rerun,isLog,newCategory?.toString())
												executed = true
												url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
												jsonOutData.addProperty("Status", "RUNNING")
												jsonOutData.addProperty("Remarks", url)
											}else{
												htmlData = tclExecutionService.executeScriptInThread(execName,""+deviceInstance?.id, executionDevice, newScriptList, "", execName,
														filePath, getRealPath(), SINGLE_SCRIPT, url, time, perfo, rerun,isLog,newCategory?.toString())
												executed = true
												url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
												jsonOutData.addProperty("Status", "RUNNING")
												jsonOutData.addProperty("Remarks", url)

											}
										}
									}catch(Exception e){
										println " ERROR "+e.getMessage()
									}
								}else{
									outData= "Error while saving execution parameters "
								}
							}
							catch(Exception e){
								println " ERROR"+e.getMessage()
							}
						}else if(status.equals( Status.ALLOCATED.toString() )){
							outData = " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
						else if(status.equals( Status.NOT_FOUND.toString() )){

							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
						else if(status.equals( Status.HANG.toString() )){
							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
						else if(status.equals( Status.BUSY.toString() )){
							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"

						}else if(status.equals( Status.TDK_DISABLED.toString() )){

							outData =  "TDK is not enabled  in the Device to execute scripts"
						}
						else{
							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
					}else{
						if(!scriptStatusFlag){
							outData = " BoxType of Scripts in ScriptGroup is not matching with BoxType of Device ${deviceInstance?.stbName}"
						}else if(!scriptVersionFlag){
							outData = " RDK Version of Scripts in ScriptGroup is not matching with RDK Version of Device ${deviceInstance?.stbName}"
						}
					}
				}else{
					if(TCL){
						outData = outData
					}else{
						outData = "No valid script list found for execution  "
					}
				}
			}else{
				outData = " script list empty   "
			}
		}else{
			outData = "No device found with this name "+stbName
		}
		if(!executed){
			jsonOutData.addProperty("Status", "FAILURE")
			jsonOutData.addProperty("Remarks", outData)
		}
		render jsonOutData
	}


	/**
	 * REST API : for getting the image name on a particular device
	 * - Accessing the getimagename_cmndline file
	 * - send command through TM ( python getimagename_cmndline.py Device_IP_Address PortNumber )
	 * @param stbName
	 * @return
	 */
	def getDeviceImageName(String stbName){
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
					jsonOutData.addProperty("Status", "SUCCESS")
					jsonOutData.addProperty("DeviceIp", device?.stbIp)
					jsonOutData?.addProperty("ImageName",outputData.toString()?.trim())
				}
				else{
					jsonOutData.addProperty("Status", "FAILURE")
					jsonOutData?.addProperty("Remarks", "Image name not available")
				}
			}catch(Exception e ){
				println  "ERROR "+ e.getMessage()
				jsonOutData.addProperty("Status", "FAILURE")
				jsonOutData?.addProperty("Remarks", "Image name not available")
			}
		}else{
			jsonOutData.addProperty("Status", "FAILURE")
			jsonOutData.addProperty("Remarks", "No device found with this name "+stbName)
		}
		render jsonOutData
	}
	
		
	/**
	 * REST API : invoked by devices to upload the logs to TM
	 */
	def uploadLogs(String fileName){
		String data = "";
		try {
			if(params?.logFile){
				def uploadedFile = request.getFile("logFile")
				if(uploadedFile){
					InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
					def fileContent = reader?.readLines()
					def logPath = "${realPath}/logs//logs"
					File logFile = new File(logPath+"//${fileName}")
					logFile.write ""
					fileContent?.each { logg ->
						data = data + logg+"\n";
						logFile << logg+"\n"
					}
				}
			}
		}catch(Exception e ){
			println  "uploadLogs ERROR "+ e.getMessage()
		}
		render data;
	}
	
	/**
	 * REST API : invoked by devices to upload the logs to TM which will append if the file exists
	 */
	def securedUploadLogs(String fileName){
		String data = "";
			try {
				String deviceStreams , deviceOcapId
				def node
				if(params?.logFile){
					def uploadedFile = request.getFile("logFile")
					if(uploadedFile){
						InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
						def fileContent = reader?.readLines()
						def logPath = "${realPath}/logs//logs"
						File logFile = new File(logPath+"//${fileName}")
						fileContent?.each { logg ->
							data = data + logg+"\n";
							logFile << logg+"\n"
						}
					}
				}
			}catch(Exception e ){
				println  "uploadLogs ERROR "+ e.getMessage()
			}
			render data;
	}
	
	/**
	 * REST API : Method to get the module wise execution status
	 */
	def getExecutionStatus(String execName){
		def jsonObjMap = [:]
		Execution executionInstance = Execution.findByName(execName)
		if(executionInstance){
		jsonObjMap.put(EXECUTION_NAME, execName)
		def detailDataMap = executedbService.prepareDetailMap(executionInstance,request.getRealPath('/'))
		def tDataMap = [:]
		int total = 0
		detailDataMap?.keySet()?.each { k ->
			Map mapp = detailDataMap?.get(k)
			int tCount = 0
			mapp?.keySet()?.each { status ->
				def tStatusCounter = tDataMap.get(status)
				def statusCounter = mapp.get(status)
				if(!tStatusCounter){
					tStatusCounter = 0
				}
				if(!status.equals(PENDING)){
					tCount = tCount + statusCounter
					tStatusCounter = tStatusCounter + statusCounter
					tDataMap.put(status, tStatusCounter)
				}
			}
			mapp.put(EXECUTED, tCount)
			def success = mapp?.get(SUCCESS)
			if(success){
				int rate = 0
				if(tCount > 0){
					int na = 0
					if(mapp?.keySet().contains(NOT_APPLICABLE_STATUS)){
						na = mapp?.get(NOT_APPLICABLE_STATUS)
					}
					rate = ((success * 100)/(tCount - na))
				}
				mapp.put(PASS_RATE,rate)
			}
			total = total + tCount
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
		tDataMap.put(PASS_RATE,rate)
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		jsonObjMap.put(DEVICE_NAME, executionInstance?.device)
		if(executionInstance?.script){
			jsonObjMap.put(SCRIPT, executionInstance?.script)
		}else if(executionInstance?.scriptGroup){
			jsonObjMap.put(SCRIPT_GROUP, executionInstance?.scriptGroup)
		}
		jsonObjMap.put(EXECUTION_STATUS, executionInstance?.executionStatus)
		jsonObjMap.put(RESULT, executionInstance?.result)
		jsonObjMap.put(DATE, executionInstance?.dateOfExecution?.toString())
		jsonObjMap.put(DATATMAP, tDataMap)
		jsonObjMap.put(DETAIL_DATA_MAP,detailDataMap)
		}else{
			jsonObjMap.put(STATUS,FAILED)
			jsonObjMap.put(REMARKS, "No execution found with this name "+execName)
		}
		render jsonObjMap as JSON
	}
	
	/**
	 * REST API : Method to get the TM IP Address
	 */
	def getTMIPAddress(String type){
		def jsonObjMap = [:]
		String ipAddress = null
		File configFile = grailsApplication.parentContext.getResource("/fileStore/tm.config").file
		if(type?.equals(IPV6_INTERFACE)){
			jsonObjMap.put(STATUS,SUCCESS)
			ipAddress = InetUtility.getIPAddress(configFile, Constants.IPV6_INTERFACE)
		}else if(type?.equals(IPV4_INTERFACE)){
			jsonObjMap.put(STATUS,SUCCESS)
			ipAddress = InetUtility.getIPAddress(configFile, Constants.IPV4_INTERFACE)
		}else{
			jsonObjMap.put(STATUS,FAILED)
			jsonObjMap.put(REMARKS, "Not a supported IP Type "+type)
		}
		if(ipAddress != null){
			jsonObjMap.put("IP",ipAddress)
		}
		jsonObjMap.put("type",type)
		render jsonObjMap as JSON
	}
	
	
	/*To handle the complete log download request*/
	def downloadLogs(){
		String executionId = params?.id
		
		String logType = ALL_LOGS
		if(params?.logType && params?.logType?.equals("FAILURE")){
			logType = FAILURE_LOGS
		}
		try {
			Execution exec = Execution.get(executionId)
			String fileName = exec?.name
			if(exec){
				params.format = EXPORT_ZIP_FORMAT
				params.extension = EXPORT_ZIP_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				fileName = fileName?.replaceAll(" ","_")
				response.setHeader("Content-Type", "application/zip")
				response.setHeader("Content-disposition", "attachment; filename=ExecutionLogs_"+ fileName +".${params.extension}")
				logZipService.zipLogs(getRealPath() , response.outputStream , executionId , logType)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	
	
	/**
	 * Method to define the bar color based on pass %
	 */
	def getBarChartColors(final def passPer){

		def color ="#18c561"
		try {
			int perc = passPer
			if ( perc == 100){
				color = "#10bf4d"
			}else if ( perc >=80 && perc < 100){
				color = "#67e84d"
			}else if ( perc >50 && perc < 80){
				color = "#f19e0e"
			}else if (perc <= 50){
				color = "#f63c0a"
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

		return color
	}
	
}
