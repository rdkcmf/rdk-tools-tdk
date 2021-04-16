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
import com.comcast.rdk.Category
import org.springframework.dao.DataIntegrityViolationException
//import com.sun.xml.internal.bind.v2.schemagen.xmlschema.List;
import grails.converters.JSON
import groovy.xml.MarkupBuilder
import org.apache.shiro.SecurityUtils
import org.apache.shiro.subject.Subject
import groovy.xml.XmlUtil
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream
import javax.xml.namespace.QName;
import groovy.util.slurpersupport.GPathResult;
import groovy.util.slurpersupport.Node;
import groovy.util.slurpersupport.NodeChild ;



import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.List;
import java.util.Properties;
import java.util.regex.Pattern;
/*import com.sun.corba.se.impl.orbutil.graph.Node
import groovy.xml.StreamingMarkupBuilder
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFCell;*/

/**
 * Controller class for Script and ScriptGroup domain.
 * @author sreejasuma
 */

class ScriptGroupController {

	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def utilityService

	def scriptService

	def primitiveService

	def excelExportService

	/**
	 * Injecting scriptgroupService
	 */
	def scriptgroupService
	
	/**
	 * Injecting testCaseService
	 */
	def testCaseService
	
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication
	
	/**
	 * To keep the status of any system test suite update operation
	 */
	public static transient scriptUpdateProgress = false

	public static final String EXPORT_EXCEL_FORMAT 			= "excel"
	public static final String EXPORT_EXCEL_EXTENSION 		= "xls"


	def index() {
		redirect(action: "list", params: params)
	}
	
    /**
    * Show TestSuite Details Summary	
    * @return
    */
	
	def showSuiteSummary() {
		redirect(action: "suiteSummary")
	}
	
	/**
	 * Show TestSuite Summary
	 * @return
	 */
	def suiteSummary() {
		def scriptGroupListB = ScriptGroup.findAllByCategory('RDKB')
		
		def testSuiteMapB =[:]
		scriptGroupListB.each { scriptgrouplistb  ->
			testSuiteMapB.put(scriptgrouplistb.name,scriptgrouplistb.scriptList?.size())
		}

		def scriptGroupListV = ScriptGroup.findAllByCategory('RDKV')
		
		def testSuiteMapV =[:]
		scriptGroupListV.each { scriptgrouplistv  ->
			testSuiteMapV.put(scriptgrouplistv.name,scriptgrouplistv.scriptList?.size())
		}
		
		def scriptGroupListC = ScriptGroup.findAllByCategory('RDKC')
		
		def testSuiteMapC =[:]
		scriptGroupListC.each { scriptgrouplistc  ->
			testSuiteMapC.put(scriptgrouplistc.name,scriptgrouplistc.scriptList?.size())
		}

		def data = [testSuiteMapB:testSuiteMapB,testSuiteMapV:testSuiteMapV,testSuiteMapC:testSuiteMapC]
		render(template:"suiteSummary", model:data)
		return data
	}

	/**
	 * Lists Script and Script Groups in a tree in list.gsp
	 * @return
	 */
	def list = {
		def groupsInstance = utilityService.getGroup()
		def requestGetRealPath = request.getRealPath("/")
		/*def scriptNameList = scriptService.getScriptNameList(requestGetRealPath)
		 def scriptGroupMap = scriptService.getScriptsMap(requestGetRealPath)
		 scriptGroupMap?.keySet()?.sort{a,b -> a <=> b}
		 scriptGroupMap = new TreeMap(scriptGroupMap)
		 def lists = ScriptGroup.executeQuery('select name from ScriptGroup')
		 [scriptGroupInstanceList: lists, scriptGroupInstanceTotal: lists.size(),error: params.error, scriptId: params.scriptId, scriptGroupId:params.scriptGroupId, scriptInstanceTotal: scriptNameList.size(), scriptGroupMap:scriptGroupMap]
		 */

		def scriptNameListV = scriptService?.getScriptNameList(requestGetRealPath,RDKV)
		scriptNameListV = scriptNameListV?scriptNameListV:[]
		def scriptNameListB = scriptService?.getScriptNameList(requestGetRealPath, RDKB)
		scriptNameListB = scriptNameListB?scriptNameListB:[]
		def scriptNameListTCL = scriptService.getTCLNameList(requestGetRealPath)
		scriptNameListTCL = scriptNameListTCL?scriptNameListTCL?.sort():[]
		def scriptNameListThunder = scriptService.getScriptNameFileListStorm()
		scriptNameListThunder = scriptNameListThunder?scriptNameListThunder?.sort():[]
		def scriptNameListC = scriptService?.getScriptNameList(requestGetRealPath, RDKC)
		scriptNameListC = scriptNameListC?scriptNameListC:[]
		
		def scriptGroupMapB = scriptService.getScriptsMap(requestGetRealPath, RDKB)
		scriptGroupMapB = scriptGroupMapB?scriptGroupMapB:[:]
		def scriptGroupMapV = scriptService.getScriptsMap(requestGetRealPath, RDKV)
		scriptGroupMapV = scriptGroupMapV?scriptGroupMapV:[:]
		def scriptGroupMapThunder = scriptService.getScriptMapThunder(requestGetRealPath)
		scriptGroupMapThunder = scriptGroupMapThunder?scriptGroupMapThunder:[:]
		def scriptGroupMapC = scriptService.getScriptsMap(requestGetRealPath, RDKC)
		scriptGroupMapC = scriptGroupMapC?scriptGroupMapC:[:]
		def listsV = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category or category=:rdkserviceCategory order by name",[category:Category.RDKV,rdkserviceCategory:Category.RDKV_RDKSERVICE])
		listsV = listsV?listsV : []
		def listsB = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category order by name",[category:Category.RDKB])
		listsB = listsB?listsB : []
		def listsTCL = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category order by name",[category:Category.RDKB_TCL])
		def listsThunder = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category order by name",[category:Category.RDKV_THUNDER])
		listsThunder = listsThunder?listsThunder?.sort():[]
		def listsC = ScriptGroup.executeQuery("select name from ScriptGroup where category=:category order by name",[category:Category.RDKC])
		listsC = listsC?listsC : []
		def lists = ScriptGroup.executeQuery('select name from ScriptGroup')
		def testGroup = Module.findAll()
		def moduleMap =[:]
		testGroup.each { moduleName  ->
			moduleMap.put(moduleName,moduleName.testGroup)
		}
		/*def scriptGroupListV = ScriptGroup.findAllByCategory('RDKV')
		def testSuiteMapV =[:]
		scriptGroupListV.each { scriptgrouplistv  ->
			testSuiteMapV.put(scriptgrouplistv.name,scriptgrouplistv.scriptList?.size())
		}
		
		def scriptGroupListB = ScriptGroup.findAllByCategory('RDKB')

		def testSuiteMapB =[:]
		scriptGroupListB.each { scriptgrouplistb  ->
			testSuiteMapB.put(scriptgrouplistb.name,scriptgrouplistb.scriptList?.size())
		}
		def scriptGroupListC = ScriptGroup.findAllByCategory('RDKC')
		def testSuiteMapC =[:]
		scriptGroupListC.each { scriptgrouplistC  ->
			testSuiteMapC.put(scriptgrouplistC.name,scriptgrouplistC.scriptList?.size())
		}*/
		listsTCL = listsTCL?listsTCL?.sort():[]
		def totalScriptsThunder = 0
		totalScriptsThunder = scriptNameListThunder?.size() * listsThunder?.size()

		[error: params.error, scriptId: params.scriptId, scriptGroupId:params.scriptGroupId,
			scriptInstanceTotalV: scriptNameListV?.size(),scriptInstanceTotalB: scriptNameListB?.size(),
			scriptGroupMapV:scriptGroupMapV, scriptGroupMapB:scriptGroupMapB, scriptGroupInstanceListV:listsV, scriptGroupInstanceListB:listsB,
			scriptGroupInstanceTotalV: listsV?.size(), scriptGroupInstanceTotalB: listsB?.size(),
			tclScripts:scriptNameListTCL, tclScriptInstanceTotal:scriptNameListTCL?.size(),  scriptGrpTcl :listsTCL, tclScriptSize : listsTCL?.size(), 
			testGroup : moduleMap, scriptNameListThunder:scriptNameListThunder,  scriptGrpThunder :listsThunder,
			thunderScriptInstanceTotal:scriptNameListThunder?.size(),  thunderScriptSize :listsThunder?.size(),
			totalScriptsThunder:totalScriptsThunder, scriptGroupMapThunder : scriptGroupMapThunder,scriptInstanceTotalC: scriptNameListC?.size(),scriptGroupMapC:scriptGroupMapC,
			scriptGroupInstanceListC:listsC, scriptGroupInstanceTotalC: listsC?.size()]
	}



	/**
	 * Method to get script file list when selecting test suite 
	 */
	def getScriptsList(String group){
		def scripts
		def finalScripts = []
		if(group){
			def scriptGroup =  ScriptGroup.findByName(group)
			scripts = scriptGroup?.scriptList
			scripts.each{
				finalScripts.add(new ScriptFileBean(scriptName:it?.scriptName, id:it?.id, moduleName:it?.moduleName, category:it?.category))
			}
		}
		if(!finalScripts.isEmpty()){
			finalScripts.sort { a, b ->
				a.scriptName <=> b.scriptName

			}
		}
		render  new Gson().toJson(finalScripts)
	}
	/**
	 * Method to create the filtered script list based on module
	 * @param scriptInstanceList
	 * @return
	 */
	private Map getScriptList(){
		List scriptList = []
		Map scriptGroupMap = [:]
		List dirList = [Constants.COMPONENT,Constants.INTEGRATION]
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

					def list = []

					files.each { file ->
						String name = file?.name?.replace(".py", "")
						list.add(name)
					}

					scriptGroupMap.put(module?.name, list)
				}
			}
		}


		return scriptGroupMap
	}



	def getScriptNameFileList(){
		List scriptList = []
		Map scriptGroupMap = [:]
		List dirList = [Constants.COMPONENT,Constants.INTEGRATION]
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
						def sFile = ScriptFile.findByScriptNameAndModuleName(name,module.getName())
						if(sFile == null){
							sFile = new ScriptFile()
							sFile.setModuleName(module?.getName())
							sFile.setScriptName(name)
							sFile.save(flush:true)
						}
						scriptList.add(sFile)
					}

				}
			}
		}

		return scriptList
	}


	/**
	 * Method to create the filtered script list based on module data
	 * @param scriptInstanceList
	 * @return
	 */
	private Map createScriptList(def scriptInstanceList ){
		List scriptList = []
		Map scriptGroupMap = [:]
		scriptInstanceList.each { script ->
			PrimitiveTest primitiveTest = script.getPrimitiveTest()
			if(primitiveTest){
				String moduleName = primitiveTest.getModule().getName();
				List subList = scriptGroupMap.get(moduleName);
				if(subList == null){
					subList = []
					scriptGroupMap.put(moduleName, subList);
				}
				subList.add(script)
			}
		}

		return scriptGroupMap
	}

	/**
	 * Create ScriptGroup
	 * @return
	 */
	def create() {
		def category = params?.category?.trim()
		def scriptNameList = []
		def sList = null
		if(!(Category.RDKB_TCL.toString().equals(category)) && !(Category.RDKV_THUNDER.toString().equals(category)) && !(Category.RDKV_RDKSERVICE.toString().equals(category))){
			scriptNameList = scriptService.getScriptNameFileList(getRealPath(), category)
		}else if(Category.RDKV_THUNDER.toString().equals(category)){
			scriptNameList = scriptService.getScriptFileListStorm()
		}else if(Category.RDKV_RDKSERVICE.toString().equals(category)){
			scriptNameList = scriptService.getScriptFileListRdkService(getRealPath(), category)
		}else{
			//issue fix
			scriptService.totalTclScriptList.each{
				if(it){
					scriptNameList?.add(it)
				}
			}
		}
		sList = scriptNameList.clone()
		sList?.sort{a,b -> a?.scriptName <=> b?.scriptName}
		[scriptGroupInstance: new ScriptGroup(params),scriptInstanceList:sList,category:params?.category]
	}


	/**
	 * Method to create script group.
	 * @return
	 */
	def createScriptGrp(){
		def errorList= []
		def scriptGroupInstance = new ScriptGroup(params)
		scriptGroupInstance.category = Utility.getCategory(params?.category)
		if(ScriptGroup.findByName(params?.name)){
			flash.message = "TestSuite name is already in use. Please use a different name."
			errorList.add("TestSuite name is already in use. Please use a different name.")
			render errorList as JSON
			return
		}
		else if(!(params?.idList)){
			flash.message = "Select scripts to create a test suite."
			errorList.add("Select scripts to create a test suite.")
			render errorList as JSON
			return
		}

		def idList = params?.idList
		idList = idList.replaceAll("sgscript-","")
		idList = idList.replaceAll("end","")

		StringTokenizer st = new StringTokenizer(idList,",")
		while(st.hasMoreTokens()){
			String token = st.nextToken()

			if(token && token.size()>0){
				ScriptFile sctFile = ScriptFile.findById(token)

				if(sctFile && !scriptGroupInstance?.scriptList?.contains(sctFile)){
					scriptGroupInstance.addToScriptList(sctFile)
				}

			}
		}


		scriptGroupInstance.groups = utilityService.getGroup()
		if (!scriptGroupInstance.save(flush: true)) {
			errorList.add("Error in saving script group")
			render errorList as JSON
			render errorList as JSON
			return
		}
		flash.message = message(code: 'default.created.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		])
		errorList.add(message(code: 'default.created.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		]))
		render errorList as JSON
	}

	def updateScriptGrp(){
		def errorList= []
		def scriptGroupInstance = ScriptGroup.get(params.id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			errorList.add(message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			]))
			render errorList as JSON
		}
		try {
			if (params.version != null) {
				def a = scriptGroupInstance.version
				def b = params.version
				long vers1 = 0
				long vers2 = 0
				if( a instanceof String){
					vers1 = Long.parseLong(a)
				}

				if( b instanceof String){
					vers2 = Long.parseLong(b)
				}

				if (vers1 > vers2) {
					scriptGroupInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
							[
								message(code: 'scriptGroup.label', default: 'Test Suite')] as Object[],
							"Another user has updated this ScriptGroup while you were editing")
					render(view: "edit", model: [scriptGroupInstance: scriptGroupInstance])

					errorList.add("Another user has updated this ScriptGroup while you were editing");
					render errorList as JSON
					return
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}


		if(!(params?.idList)){
			flash.message = "Select scripts to update a test suite."
			errorList.add("Select scripts to update a test suite.");
			render errorList as JSON
			return
		}
		scriptGroupInstance.name = params.get("name")
		scriptGroupInstance.scriptList.clear();
		def idList = params?.idList
		idList = idList.replaceAll("sgscript-","")
		idList = idList.replaceAll("end","")
		StringTokenizer st = new StringTokenizer(idList,",")
		while(st.hasMoreTokens()){
			String token = st.nextToken()
			if(token && token.size()>0){
				ScriptFile sctFile = ScriptFile.findById(token)
				if(sctFile && !scriptGroupInstance?.scriptList?.contains(sctFile)){
					scriptGroupInstance.addToScriptList(sctFile)
				}
			}
		}


		if (!scriptGroupInstance.save(flush: true)) {
			flash.message = "TestSuite name is already in use. Please use a different name."
			errorList.add("TestSuite name is already in use. Please use a different name.");
			render errorList as JSON
			return
		}
		flash.message = message(code: 'default.updated.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		])

		errorList.add(message(code: 'default.updated.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		]));
		render errorList as JSON
	}
	/**
	 * Save ScriptGroup
	 * @return
	 */
	def save() {
		//		def scriptGroupInstance = new ScriptGroup(params)
		//        if(ScriptGroup.findByName(params?.name)){
		//            flash.message = "TestSuite name is already in use. Please use a different name."
		//            redirect(action: "list")
		//            return
		//        }
		//        else if(!(params?.scripts) && !(params?.scriptElement)){
		//            flash.message = "Select scripts to create a test suite."
		//            redirect(action: "list")
		//            return
		//        }
		//
		//		if(params?.scriptElement){
		//			def list = params?.scriptElement
		//			list = list.replaceAll("script-","")
		//			println " listt "+list
		//
		//			StringTokenizer st = new StringTokenizer(list,",")
		//			while(st.hasMoreTokens()){
		//				Script sct = Script.findById(st.nextToken())
		//				println " scriptt "+ sct
		//				if(sct){
		//					scriptGroupInstance.addToScriptsList(sct)
		//				}
		//			}
		//		}
		//
		//		scriptGroupInstance.groups = utilityService.getGroup()
		//		if (!scriptGroupInstance.save(flush: true)) {
		//			return
		//		}
		//		flash.message = message(code: 'default.created.message', args: [
		//			message(code: 'scriptGroup.label', default: 'Test Suite'),
		//			scriptGroupInstance.name
		//		])
		redirect(action: "list")
	}

	/**
	 * Show ScriptGroup
	 * @return
	 */
	def show(Long id) {
		def scriptGroupInstance = ScriptGroup.get(id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				id
			])
			redirect(action: "list")
			return
		}

		[scriptGroupInstance: scriptGroupInstance]
	}

	/**
	 * Edit ScriptGroup
	 * @return
	 */
	/*def edit(Long id) {
	 def scriptGroupInstance = ScriptGroup.get(id)
	 if (!scriptGroupInstance) {
	 flash.message = message(code: 'default.not.found.message', args: [
	 message(code: 'scriptGroup.label', default: 'Test Suite'),
	 scriptGroupInstance.name
	 ])
	 redirect(action: "list")
	 return
	 }       
	 def scripts = scriptService.getScriptNameFileList(getRealPath());   
	 def time1 = System.currentTimeMillis()
	 def list4 = scripts.findAll(){
	 !((scriptGroupInstance.scriptList).contains(it))
	 }
	 list4.sort{a,b -> a?.scriptName <=> b?.scriptName}
	 [scripts:list4,scriptNameList:scriptGroupInstance.scriptList,scriptGroupInstance: scriptGroupInstance]
	 }*/

	def edit(String name) {
		def scriptGroupInstance = ScriptGroup.findByName(name)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			redirect(action: "list")
			return
		}
		//def scripts = scriptService.getScriptNameFileList(getRealPath());
		def scripts = null
		if(scriptGroupInstance.category != Category.RDKB_TCL && scriptGroupInstance.category != Category.RDKV_THUNDER && scriptGroupInstance.category != Category.RDKV_RDKSERVICE){
			scripts = scriptService.getScriptNameFileList(getRealPath(), scriptGroupInstance?.category?.toString());
		}
		else if(scriptGroupInstance.category == Category.RDKV_THUNDER){
			scripts = scriptService.getScriptFileListStorm()
		}else if(scriptGroupInstance.category == Category.RDKV_RDKSERVICE){
		    scripts = scriptService.getScriptFileListRdkService(getRealPath(), scriptGroupInstance?.category?.toString())
		}else{
			scripts = scriptService.totalTclScriptList
		}
		def list4 = scripts.findAll(){
			!((scriptGroupInstance.scriptList).contains(it))
		}
		list4.sort{a,b -> a?.scriptName <=> b?.scriptName}

		[scripts:list4,scriptNameList:scriptGroupInstance.scriptList,scriptGroupInstance: scriptGroupInstance , value : params.value]
	}

	/**
	 * Update ScriptGroup
	 * @return
	 */
	def update(Long id, Long version) {
		def scriptGroupInstance = ScriptGroup.get(id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance.name
			])
			redirect(action: "list",params: [scriptGroupId: params.id])
			return
		}

		if (version != null) {
			if (scriptGroupInstance.version > version) {
				scriptGroupInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						[
							message(code: 'scriptGroup.label', default: 'Test Suite')] as Object[],
						"Another user has updated this ScriptGroup while you were editing")
				render(view: "edit", model: [scriptGroupInstance: scriptGroupInstance])
				return
			}
		}

		scriptGroupInstance.properties = params

		if (!scriptGroupInstance.save(flush: true)) {
			flash.message = "TestSuite name is already in use. Please use a different name."
			redirect(action: "list",params: [scriptGroupId: params.id])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [
			message(code: 'scriptGroup.label', default: 'Test Suite'),
			scriptGroupInstance.name
		])
		redirect(action: "list", params: [scriptGroupId: params.id])
	}

	/**
	 * Delete ScriptGroup
	 * @return
	 */
	def deleteScriptGrp() {
		def scriptGroupInstance = ScriptGroup.findById(params?.id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
			return
		}

		try {
			scriptGroupInstance.delete(flush: true)
			flash.message = message(code: 'default.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
		catch (DataIntegrityViolationException e) {
			flash.message = message(code: 'default.not.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
	}

	/**
	 * Delete ScriptGroup
	 * @return
	 */
	def delete() {
		def scriptGroupInstance = ScriptGroup.findById(params?.id)
		if (!scriptGroupInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
			return
		}

		try {
			scriptGroupInstance.delete(flush: true)
			flash.message = message(code: 'default.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
		catch (DataIntegrityViolationException e) {
			flash.message = message(code: 'default.not.deleted.message', args: [
				message(code: 'scriptGroup.label', default: 'Test Suite'),
				scriptGroupInstance?.name
			])
			redirect(action: "list")
		}
	}

	/**
	 * Create Script
	 * @return
	 */
	def createScript() {

		def primitiveTestList
		def uniqueId = "script_"+System.currentTimeMillis()
		def lis
		if(params?.category?.toString().equals(RDKV) || params?.category?.toString().equals(RDKB) || params?.category?.toString().equals(RDKC)){
			scriptService?.addNewTestCaseDetails([:],uniqueId)
			//		def primitiveTestList = PrimitiveTest.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])//PrimitiveTest.list([order: 'asc', sort: 'name'])
			primitiveTestList = primitiveService.getPrimitiveList(getRealPath(), params?.category)
			lis = primitiveTestList.toList()
			Collections.sort(lis)
		}else{
			primitiveTestList = []
			lis = []
		}
		[ primitiveTestList : lis, category: params?.category,uniqueId:uniqueId]
	}



	/**
	 * Method to get the details of the Suite to be created
	 * @return
	 */
	def getSuiteDetails()
	{
		def moduleList = []
		def moduleListRDKV = []
		def moduleListRDKB = []
		def directoryListRDKVThunder = []
		ArrayList<String> scriptGroupList = new ArrayList<String>();
		int moduleListSizeRDKV 
		int moduleListSizeRDKB
		int directoryListSizeRDKVThunder
		
		moduleListRDKV = Module.findAllByCategory(Category.RDKV)
		boolean removed = false
		Iterator<Module> iteratorModule = moduleListRDKV.iterator()
		while(iteratorModule?.hasNext()){
			def obj = iteratorModule.next()
			def objName = obj.name
			def objTestGroup = obj.testGroup
			if(objName.equals(Constants.RDKSERVICES) || (objTestGroup.equals(TestGroup.Certification))){
				iteratorModule.remove()
				removed = true
			}
		}
		moduleListRDKB = Module.findAllByCategory(Category.RDKB)
		directoryListRDKVThunder = scriptService.scriptGroupMapThunder.keySet()
		moduleListRDKB.remove(Module.findByName('tcl'))
		
		scriptGroupList = ScriptGroup.findAll ()
		

		 moduleListSizeRDKV = moduleListRDKV.size()
	
		 moduleListSizeRDKB = moduleListRDKB.size()
		 
		 directoryListSizeRDKVThunder = directoryListRDKVThunder.size()
		 
		[moduleListSizeRDKV:moduleListSizeRDKV,moduleListSizeRDKB :moduleListSizeRDKB ,directoryListSizeRDKVThunder :directoryListSizeRDKVThunder ,moduleListRDKV :moduleListRDKV ,moduleListRDKB :moduleListRDKB ,directoryListRDKVThunder :directoryListRDKVThunder,scriptGroupList:scriptGroupList]
	}
	
    
	def saveCustomGrp()
	{
		def testSuiteName = params.name
		def countVariable = 0
		def moduleInstance
		def moduleSelectList = []
		def directorySelectList = []
		def scriptFileList =[]
		def scriptFileListThunder =[]
		def scriptModuleList
		def dirName
		def fileName
		def script
		
		def errorList = []
		
		
		if(ScriptGroup.findByName(params?.name))
		{
			println "TestSuite name is already in use. Please use a different name."
			flash.message = "TestSuite name is already in use. Please use a different name."
			render("Duplicate Script Name not allowed. Try Again.")
		}
		else if(params?.customCategory == "RDKVTHUNDER"){
			if(params?.listCount)
			{
				for (iterateVariable in params?.listCount)
				{
					countVariable++
					if(params?.("chkbox"+countVariable) == KEY_ON)
					{
						def directoryName = params?.("id"+countVariable)
						if (directoryName)
						{
							directorySelectList?.add(directoryName)
						}
					}
				}
			}
			for (directory in directorySelectList)
			{
				def scriptListForDirectory = scriptService.scriptGroupMapThunder.get(directory)
				scriptListForDirectory.each {scriptValueObj->
					  ScriptFile.withNewSession{scriptFileSession->
						  def scriptFileObject = ScriptFile.findByScriptName(scriptValueObj?.scriptName)
						  if(scriptFileObject){
							  scriptFileListThunder?.add(scriptFileObject)
						  }
						  scriptFileSession.clear()
					  }
                }
			}
			if(scriptFileListThunder.size()== 0)
			{
				flash.message = "No script with given condition. Suite not created"
            }
			else
			{
				ScriptGroup.withSession{session->
					def scriptGroupInstance = new ScriptGroup()
                    scriptGroupInstance.name = testSuiteName
				    scriptGroupInstance.groups = utilityService.getGroup()
				    scriptGroupInstance.category = Constants.RDKV_THUNDER
					for(scrpt in scriptFileListThunder){
						scriptGroupInstance?.addToScriptList(scrpt)
					}
				    if (!scriptGroupInstance.save(flush: true))
				    {
					    flash.message = "Script Not Saved"
				    }
				    else{
					    flash.message = "Test Suite Created Successfully "
				    }
					session.clear()
				}
			}
		}
		else
		{  
			def boxType =  BoxType.findById(params?.boxname)
			def rdkVersions = RDKVersions.findById(params?.RDKVersionsName)
			/* To get the Selected Modules*/
			if(params?.listCount)
			{ 
				for (iterateVariable in params?.listCount)
				{
					countVariable++
					if(params?.("chkbox"+countVariable) == KEY_ON)
					{
	
						def idDb = params?.("id"+countVariable).toLong()			
						moduleInstance = Module.get(idDb)
						if (moduleInstance) 
						{
							moduleSelectList<<moduleInstance
						}
						
					}
					
				}
			
				}
			
			def category = boxType.category.toString()
			if(moduleSelectList.size()== 0)
			{
				flash.message = "No modules Selected"
				
			}
		
			scriptModuleList = scriptService.getScriptsMap(request.getRealPath("/"), category)
				
			scriptModuleList = scriptModuleList?scriptModuleList:[:]
			for (module in moduleSelectList)
			{
				def scriptValue = scriptModuleList.get(module.toString()) 
			
				scriptValue.each {scriptValueObj->
					
					dirName = module.toString()
					fileName = scriptValueObj
		
					script = scriptService.getMinimalScript(getRealPath(),dirName,fileName, category)
					
					//Include long duration scripts only if the check box for long duration is selected			
					if(script?.boxTypes?.contains( boxType) && script?.rdkVersions?.contains(rdkVersions) && (params.longDuration=="on" || !script?.longDuration))
					{
				
								
						scriptFileList<<ScriptFile.findByScriptName(script?.name)				
					
					}
				}
						
			}
			if(scriptFileList.size()== 0)
			{
				flash.message = "No script with given condition. Suite not created"
				render("No script with given condition. Suite not created")
				
				
			}
			else
			{
				ScriptGroup.withTransaction{
					def scriptGroupInstance = new ScriptGroup()
				    scriptGroupInstance.name = testSuiteName
				    scriptGroupInstance.groups = utilityService.getGroup()
				    scriptGroupInstance.category = category
				    scriptGroupInstance.scriptList = scriptFileList
				    if (!scriptGroupInstance.save(flush: true))
				    {
					    flash.message = "Script Not Saved"
					    println "not saved"
				    }
				    else{
					    flash.message = "Test Suite Created Successfully "
				    }
				}
			}
		}
		redirect(action: "list")
	}


	/**
	 * Edit Script
	 * @return
	 */
	def editScript() {
		if(params.id){
			StringTokenizer st = new StringTokenizer(params.id,"@")
			String dirName
			String fileName
			if(st.countTokens() == 2){
				dirName = st.nextToken()
				fileName = st.nextToken()
			}
			def script = scriptService.getScript(getRealPath(),dirName,fileName, params.category?.trim())
			if(script != null){
				if (script.size() > 0){
					[script : script , category : params?.category]
				} else {
				    render "Error : Module information is not available for module : "+dirName
				}
			}else {
				render "Error : No script available with this name : "+fileName +"in module :"+dirName
			}
		}
	}

	/**
	 * Displays the testcase details for the given module
	 * 
	 */

	def viewTestCase(String module, String category) {
		params?.moduleName = module
		params?.category = category
		def totalTestCaseMap = testCaseService?.downloadModuleTestCaseInExcel(params,getRealPath())
		def testCaseList = totalTestCaseMap[module]
		// For handling special characters in the test cases
		testCaseList.each{testCaseMap ->
			testCaseMap.each{k,v ->
				v = v.replace("&", "&#38;");
				testCaseMap.put(k, v)
			}
		}
		[testCaseList:testCaseList]
	}

	/**
	 * Only display tcl script content
	 *  
	 */
	def tclScriptDisplay(){
		// Issue fix :- edit the script using test suite .
		def scriptName = params?.scriptName
		if(scriptName?.toString()?.contains('@')){
			def name  = scriptName?.tokenize('@')
			scriptName = name[1]

		}else{
			scriptName = params?.scriptName
		}
		//def scriptName = params?.scriptName
		//def scriptText = scriptService.getTclScript(getRealPath(), scriptName)
		def scriptText = scriptService.getTclScript(request.getRealPath("/"), scriptName)
		if(scriptText){
			render (view:"editScript", model:[script : scriptText , category : Category.RDKB_TCL.toString(), scriptName:scriptName])
		}else{
			render "Error : No script available with this name : "+scriptName
		}
	}

	def saveTcl() {
		def content =  params.tclText
		def script = params.scriptName
		if(content && script){
			def file = Utility.getTclFilePath(getRealPath(), script)
			try{

				if(file){
					Utility.writeContentToFile(content, file)
					//removeLock(script)
					flash.message = message(code: 'default.updated.message', args: [
						message(code: 'script.label', default: 'Script'),
						params.scriptName])
				}
				else{
					//removeLock(script)
					flash.error = 'File ${script} not found.'
				}
			}
			catch(Exception e){
				e.printStackTrace()
				//removeLock(script)
				flash.error = "Error occured while updating. Please try again."
			}
		}
		else{
			flash.error = "No content/scriptname. Please try again."
		}

		redirect(action: "list")

	}
	def getRealPath(){
		//return request.getRealPath("/")
		return request.getSession().getServletContext().getRealPath("/")
	}


	/**
	 * Delete Script
	 * @return
	 */
	def deleteScript(){

		def isTcl = false
		if(params.id){
			String dirName
			String fileName
			def scriptDirName
			if(params.id?.contains('@')){
				StringTokenizer st = new StringTokenizer(params.id,"@")
				if(st.countTokens() == 2){
					dirName = st.nextToken()
					fileName = st.nextToken()
					scriptDirName = primitiveService.getScriptDirName(dirName)
				}
			}
			else{
				isTcl = true
				dirName = 'tcl'
				fileName = params.id
			}
			Map script = [:]

			File file = null

			def scriptObj = ScriptFile.findByScriptNameAndModuleName(fileName,dirName)


			if (!scriptObj) {
				flash.message = "Script not found"
				render("Not found")
			}else{
				boolean scriptInUse = false
				if(isTcl){
					file = new File(getTestScriptPath(scriptObj?.category.toString(),fileName, dirName)+FILE_SEPARATOR +fileName+".tcl")
					scriptInUse = false // this need to be updated accordingly
					scriptService.deleteScript(scriptObj, scriptObj?.category?.toString())
				}
				else{
					file = new File(getTestScriptPath(scriptObj?.category.toString(),fileName, dirName)+FILE_SEPARATOR + scriptDirName+FILE_SEPARATOR+dirName+FILE_SEPARATOR+fileName+".py")
					def script1 = scriptService.getScript(getRealPath(), dirName, fileName, scriptObj?.category?.toString())
					scriptInUse = scriptgroupService.checkScriptStatus(scriptObj,script1)
					scriptService.deleteScript(scriptObj, scriptObj?.category?.toString())
				}

				if(scriptInUse){
					flash.message = "Can't Delete. Scripts may be used in Script Group"
					render("Exception")
				}
				else{
					try{
						if(!scriptObj.delete(flush: true)){
							println "not deleted"+scriptObj?.errors
						}
					}catch(Exception e){
						println  e.getMessage()
					}
				}
			}

			if(file != null && file.exists()){
				try {
					def fileDelete = file.delete()
					if(fileDelete){
						flash.message = "Deleted the script '${fileName}'"
						render("success")
					}else{
						flash.message = "Failed to delete the script '${fileName}'"
						render("failure")
					}
				} catch (Exception e) {
					e.printStackTrace()
				}
			}else{
				flash.message = "Failed to delete the script '${fileName}'"
				render("failure")
			}
		}
	}

	def getScript(dirName,fileName){
		def scriptDirName = primitiveService.getScriptDirName(dirName)
		File file = new File( "${request.getRealPath('/')}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
		Map script = [:]
		if(file.exists()){
			String s = ""
			List line = file.readLines()
			//	int indx = 0
			int indx = line?.findIndexOf {  it.startsWith("'''")}
			String scriptContent = ""
			if(line.get(indx).startsWith("'''"))	{
				indx++
				while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
					if(!(line.get(indx)?.equals(""))){
						s = s + line.get(indx)+"\n"
					}
					indx++
				}
				indx ++
				while(indx < line.size()){
					scriptContent = scriptContent + line.get(indx)+"\n"
					indx++
				}
			}

			String xml = s
			XmlParser parser = new XmlParser();
			def node = parser.parseText(xml)
			script.put("id", node.id.text())
			script.put("version", node.version.text())
			script.put("name", node.name.text())
			script.put("skip", node.skip.text())
			def nodePrimitiveTestidText = node.primitiveTestid.text()
			def primitiveTst = PrimitiveTest.findById(nodePrimitiveTestidText)
			script.put("primitiveTest",primitiveTst)
			def versList = []
			def btList = []
			def testProfileList =[]
			Set btSet = node?.boxTypes.boxType.collect{ it.text() }
			Set versionSet = node?.rdkVersions.rdkVersion.collect{ it.text() }
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

	/**
	 * Save Script
	 * @return
	 */
	def saveScript() {
		def error = ''
		def scriptList = scriptService.getScriptNameList(params?.category?.toString())
		def scriptListRDKV  = scriptService.getScriptNameList(request.getRealPath("/"),RDKV)
		def scriptListRDKB  = scriptService.getScriptNameList(request.getRealPath("/"),RDKB)
		def scriptListRDKC  = scriptService.getScriptNameList(request.getRealPath("/"),RDKC)
		String dirname
		boolean isAdvanced = false
		def scriptObject = null
		String scriptObjectName = ""
		scriptObject = ScriptFile.findByScriptNameAndCategory(params?.name.trim()?.toString(), params?.category?.toString())
		if(scriptObject){
			scriptObjectName = scriptObject.scriptName
		}
		if((params?.name?.trim()?.toString()) && (!scriptObjectName.equals(params?.name?.trim()?.toString())) && (!(params?.ptest.equals("null"))) && (params.synopsis?.trim())){
			boolean saveScript = false
			def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
			def moduleName = moduleMap.get(params?.ptest)
			def scriptsDirName = primitiveService.getScriptDirName(moduleName)
			//def ptest = primitiveService.getPrimitiveTest(getRealPath()+"//fileStore//testscripts//"+scriptsDirName+"//"+moduleName+"//"+moduleName+".xml", params?.ptest)
			def category = params?.category?.trim()
			def ptest
			def path = getRealPath()+Constants.FILE_SEPARATOR+"fileStore"+Constants.FILE_SEPARATOR
			
			if(RDKV.equals(category)){
				path = path+TESTSCRIPTS_RDKV + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName +Constants.FILE_SEPARATOR + moduleName +XML
				File xmlFile = new File(path)
				if(!xmlFile?.exists()){
					def dirName = primitiveService.getDirectoryName(params?.ptest)
					path = getRealPath()+Constants.FILE_SEPARATOR+"fileStore"+Constants.FILE_SEPARATOR+dirName + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName +Constants.FILE_SEPARATOR + moduleName +XML
					xmlFile = new File(path)
				}
			}
			else if(RDKB.equals(category)){
				path = path + TESTSCRIPTS_RDKB + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName  +Constants.FILE_SEPARATOR+moduleName+XML
				File xmlFile = new File(path)
				if(!xmlFile?.exists()){
					def dirName = primitiveService.getDirectoryName(params?.ptest)
					path = getRealPath()+Constants.FILE_SEPARATOR+"fileStore"+Constants.FILE_SEPARATOR + dirName + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName  +Constants.FILE_SEPARATOR+moduleName+XML
				}
			}
			else if(RDKC.equals(category)){
				path = path + TESTSCRIPTS_RDKC + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName  +Constants.FILE_SEPARATOR+moduleName+XML
				File xmlFile = new File(path)
				if(!xmlFile?.exists()){
					def dirName = primitiveService.getDirectoryName(params?.ptest)
					path = getRealPath()+Constants.FILE_SEPARATOR+"fileStore"+Constants.FILE_SEPARATOR + dirName + Constants.FILE_SEPARATOR + scriptsDirName.toString() + Constants.FILE_SEPARATOR + moduleName  +Constants.FILE_SEPARATOR+moduleName+XML
				}
			}
			ptest = primitiveService.getPrimitiveTest(path, params?.ptest)
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)

			int time = 0
			if(params?.executionTime){
				try {
					time = Integer.parseInt(params?.executionTime)
				} catch (Exception e) {
					e.printStackTrace()
				}
			}

			boolean skipStatus
			if(params?.skipStatus.equals("on")){
				skipStatus = true
			}else{
				skipStatus = false
			}
			boolean longDuration = false
			if(params?.longDuration.equals("on")){
				longDuration = true
			}else{
				longDuration = false
			}
			
			if(params?.advScript.equals("on")){
				isAdvanced = true
			}
			
			Set boxTypes = []
			Set rdkVersions = []
			Set scrptTags = []
			Set testProfileList = []

			try {

				xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
				xml.xml(){
					xml.id("") //TODO add logic for id
					mkp.yield "\r\n  "
					mkp.comment "Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty"
					xml.version(1)
					mkp.yield "\r\n  "
					mkp.comment "Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1"
					xml.name(params?.name?.trim())
					mkp.yield "\r\n  "
					mkp.comment "If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension"
					xml.primitive_test_id(ptest?.id)
					mkp.yield "\r\n  "
					mkp.comment "Do not change primitive_test_id if you are editing an existing script."
					xml.primitive_test_name(ptest?.name)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.primitive_test_version(ptest?.version)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.status(Status.FREE)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.synopsis(params.synopsis?.trim())
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.groups_id(utilityService.getGroup()?.id)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.execution_time(time)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.long_duration(longDuration)
					mkp.yield "\r\n  "
					mkp.comment ""
					xml.advanced_script(isAdvanced)
					mkp.yield "\r\n  "
					mkp.comment "execution_time is the time out time for test execution"
					xml.remarks(params?.remarks?.trim())
					mkp.yield "\r\n  "
					mkp.comment "Reason for skipping the tests if marked to skip"
					xml.skip(skipStatus?.toString())
					mkp.yield "\r\n  "
					mkp.comment ""

					def bTypeList = params.list("boxTypes")
					if(bTypeList instanceof List){
						//bTypeList = bTypeList?.sort()
					}

					xml.box_types(){
						bTypeList.each{ bType ->
							bType = Integer.parseInt(bType)
							def boxType = BoxType.findById(bType)
							boxTypes.add(boxType)
							xml.box_type(boxType?.name)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}

					def rdkVersList = params?.list("rdkVersions")
					if(rdkVersList instanceof List){
						//rdkVersList = rdkVersList?.sort()
					}

					xml.rdk_versions(){
						rdkVersList?.each { vers ->
							def rdkVers = RDKVersions.findById(vers)
							rdkVersions.add(rdkVers)
							xml.rdk_version(rdkVers?.buildVersion)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}

					def testCaseMap  = scriptService?.getNewTestCaseDetails(params?.uniqueId)
					if((testCaseMap != [:]  )){
						xml?.test_cases(){
							xml.test_case_id(testCaseMap.testCaseId)
							xml.test_objective(testCaseMap.testObjective)
							xml.test_type(testCaseMap.testType)
							xml.test_setup(testCaseMap.testSetup)
							//xml.steam_id(testCaseMap.streamId)
							xml.pre_requisite(testCaseMap.preRequisites)
							xml.api_or_interface_used(testCaseMap.interfaceUsed)
							xml.input_parameters(testCaseMap.inputParameters)
							xml.automation_approch(testCaseMap.automationApproch)
							xml.expected_output(testCaseMap.expectedOutput) 
							xml.priority(testCaseMap.priority)
							xml.test_stub_interface(testCaseMap.testStubInterface)
							xml.test_script(testCaseMap.testScript)
							xml.skipped(testCaseMap.tcskip)
							xml.release_version(testCaseMap.releaseVersion)
							xml.remarks(testCaseMap.remarks)
						}
					}else{
						xml?.test_cases(){
							xml.test_case_id("")
							xml.test_objective("")
							xml.test_type("")
							xml.test_setup("")
							//xml.steam_id("")
							xml.pre_requisite("")
							xml.api_or_interface_used("")
							xml.input_parameters("")
							xml.automation_approch("")
							xml.expected_output("")
							xml.priority("")
							xml.test_stub_interface("")
							xml.test_script("")
							xml.skipped("")
							xml.release_version("")
							xml.remarks("")
						}
					}
					
					def scriptTagList = params?.scriptTags
					if(scriptTagList && scriptTagList instanceof List){
						//scriptTagList = scriptTagList?.sort()
					}
					try {
						if(scriptTagList?.size() > 0){
							xml.script_tags(){
								scriptTagList?.each { tag ->
									def sTag = ScriptTag.findById(tag)
									scrptTags.add(sTag)
									xml.script_tag(sTag?.name)
									mkp.yield "\r\n    "
									mkp.comment ""
								}
							}
						}
					} catch (Exception e) {
						println " error "+e.getMessage()
						e.printStackTrace()
					}
	
					if(params?.testProfile)	{
						def  scriptTestProfiles = params?.testProfile
						if(scriptTestProfiles && scriptTestProfiles?.size() >  0){
							xml.test_profiles(){
								scriptTestProfiles?.each{
									def tProfile = TestProfile?.findById(it)
									testProfileList.add(tProfile?.toString())
									xml.test_profile(tProfile)
								}
							}
						}
					}
				}
				




				dirname = ptest?.module?.name
				dirname = dirname?.trim()

				def pathToDir =  "${request.getRealPath('/')}//fileStore"
				
				if(RDKV.equals(category)){
					if(isAdvanced){
						pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKV_ADV
					}else{
						pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKV
					}
				}
				else if(RDKB.equals(category)){
					if(isAdvanced){
						pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKB_ADV
					}else{
						pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKB
					}
				}
				else if(RDKC.equals(category)){
					pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKC
				}
				//File dir = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName+"//"+dirname+"/")
				File dir = new File( pathToDir + Constants.FILE_SEPARATOR + scriptsDirName +  Constants.FILE_SEPARATOR +dirname)
				if(!dir.exists()){
					dir.mkdirs()
				}
				//File file = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName+"//"+dirname+"/"+params?.name?.trim()+".py");
				File file = new File( pathToDir + Constants.FILE_SEPARATOR + scriptsDirName + Constants.FILE_SEPARATOR+dirname+Constants.FILE_SEPARATOR+params?.name?.trim()+".py");
				if(!file.exists()){
					file.createNewFile()
				}
				File pyHeader
				if(isAdvanced){
					pyHeader = new File( "${request.getRealPath('/')}//fileStore//pyRDKMHeader.txt")
				}
				else{
					pyHeader = new File( "${request.getRealPath('/')}//fileStore//pyHeader.txt")
				}

				def pyHeaderContentList = pyHeader?.readLines()
				String pyHeaderContent = ""
				pyHeaderContentList.each {
					pyHeaderContent += it?.toString()+"\n"
				}
				String data =pyHeaderContent+"'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea

				//String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea
				file.write(data)
				saveScript = true
				scriptService?.clearTestCaseDetailsMap(params?.uniqueId)
			} catch (Exception e) {
				//log.error "Error saving Script instance : ${params?.name}"
				render("Error in saving Script. Try Again." )
			}
			if(saveScript){
				def script = ScriptFile.findByScriptNameAndModuleName(params?.name?.trim(),ptest?.module?.name)
				if(script == null){
					script = new ScriptFile()
					script.setScriptName(params?.name?.trim())
					script.setModuleName(ptest?.module?.name)
					if(ptest?.module?.name == Constants.RDKSERVICES || (ptest?.module?.testGroup == TestGroup.Certification)){
						script.category = Utility.getCategory(Category?.RDKV_RDKSERVICE.toString())
					}else{
						script.category = Utility.getCategory(params?.category)
					}
					script.save(flush:true)
				}
				def sObject = new ScriptObject()
				sObject.setBoxTypes(boxTypes)
				sObject.setRdkVersions(rdkVersions)
				sObject.setScriptTags(scrptTags)
				sObject.setName(params?.name?.trim())
				sObject.setModule(ptest?.module?.name)
				sObject.setScriptFile(script)
				sObject.setLongDuration(longDuration)
				sObject?.setTestProfile(testProfileList)
				if((ptest?.module?.name != Constants.RDKSERVICES) && (ptest?.module?.testGroup != TestGroup.Certification)){
					scriptService.updateScript(script, params?.category)
					scriptgroupService.saveToScriptGroups(script,sObject, params?.category)
					scriptgroupService.saveToDefaultGroups(script,sObject, boxTypes, params?.category)
					scriptgroupService.updateScriptsFromScriptTag(script,sObject,[],[], params?.category)
					scriptService?.updateScriptsFromTestProfile(script,sObject, params.category)
					scriptService.createDefaultGroupWithoutOS(sObject,script, params?.category)
					scriptService.updateAdvScriptMap(params?.name?.trim(), dirname, Utility.getCategory(params?.category), isAdvanced)
				}else{
					scriptService.updateScript(script,Category?.RDKV_RDKSERVICE.toString())
					scriptService.updateRdkServiceScriptSuite(ptest?.module?.name,script,Category?.RDKV_RDKSERVICE.toString())
				}
				def sName = params?.name
				render(message(code: 'default.created.message', args: [
					message(code: 'script.label', default: 'Script'),
					sName
				]))

			}
		}
	}


	/**
	 * Update Script
	 * @return
	 */
	def updateScript(Long id, Long version) {
		def scriptList = scriptService.getScriptNameList(request.getRealPath("/"), params?.category)
		def scriptFileList = ScriptFile.findAll()
		String prevScriptName = params?.prevScriptName?.trim()
		String newScriptName = params?.name?.trim()
		if (prevScriptName != newScriptName && scriptFileList?.scriptName?.contains(newScriptName)) {
			flash.message = "Duplicate Script Name not allowed. Try Again."
			redirect(action: "list")
			return
		}else if(params.synopsis?.isEmpty() ){
			flash.message = "Please fill the synopsis field !!!. Try Again."
			redirect(action: "list")
			return
		}
		if (!scriptList?.contains(prevScriptName)) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'script.label', default: 'Script'),
				id
			])
			redirect(action: "list")
			return
		}
		def moduleMap = primitiveService.getPrimitiveModuleMap(params?.ptest)
		def moduleName = moduleMap.get(params?.ptest)
		def scriptsDirName = primitiveService.getScriptDirName(moduleName)
		def category = params?.category?.trim()
		def filePath = null
		String dirname
		if(RDKV.equals(category)){
			filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + TESTSCRIPTS_RDKV + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +XML
			File xmlFile = new File(filePath)
			if(!xmlFile?.exists()){
				def dirName = primitiveService.getDirectoryName(params?.ptest)
				filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + dirName + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +XML
			}
		}
		else if(RDKB.equals(category)){
			filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + TESTSCRIPTS_RDKB + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +XML
			File xmlFile = new File(filePath)
			if(!xmlFile?.exists()){
				def dirName = primitiveService.getDirectoryName(params?.ptest)
				filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + dirName + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +XML
			}
		}else if(RDKC.equals(category)){
			filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + TESTSCRIPTS_RDKC + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +XML
			File xmlFile = new File(filePath)
			if(!xmlFile?.exists()){
				def dirName = primitiveService.getDirectoryName(params?.ptest)
				filePath = getRealPath() + FILE_SEPARATOR + "fileStore"+ FILE_SEPARATOR + dirName + FILE_SEPARATOR + scriptsDirName + FILE_SEPARATOR + moduleName+ FILE_SEPARATOR + moduleName +XML
			}
		}
		//def ptest = primitiveService.getPrimitiveTest(getRealPath()+"/fileStore/testscripts/"+scriptsDirName+"/"+moduleName+"/"+moduleName+".xml", params?.ptest)
		def ptest = primitiveService.getPrimitiveTest(filePath, params?.ptest)
		//		def module = Module.findByName(moduleName)
		def scrpt = scriptService.getScript(getRealPath(),moduleName, params?.prevScriptName, params?.category)
		def oldBoxTypes = scrpt?.boxTypes
		def oldRDKVersions = scrpt?.rdkVersions
		def oldTags = scrpt?.scriptTags
		def oldAdvStatus = scrpt?.advScript
		boolean isLongDuration = scrpt?.longDuration
		boolean isAdvanced = false

		if (params.scriptVersion != null) {

			def a = scrpt.version
			def b = params.scriptVersion
			long vers1 = 0
			long vers2 = 0


			if( a instanceof String){
				vers1 = Long.parseLong(a)
			}

			if( b instanceof String){
				vers2 = Long.parseLong(b)
			}
			if (vers1 > vers2) {
				clearEditLock(params?.name)
				flash.message = "Script changes not saved, another user has updated this Script while you were editing !!!"
				redirect(action: "list")
				return
			}
		}
		boolean saveScript =  false
		boolean longDuration = false
		Set bTypes = []
		Set rdkVers = []
		Set scrptTags = []
		Set testProfileList = []
		//def tProfile

		try {
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)

			def b = params.scriptVersion
			long vers2 = 0
			if( b instanceof String){
				vers2 = Long.parseLong(b)
				vers2 ++
			}

			int time = 0
			if(params?.executionTime){
				try {
					boolean isNumber = Pattern.matches("[0-9]+", params?.executionTime)
					if(isNumber) {
						time = Integer.parseInt(params?.executionTime)
					}
				} catch (Exception e) {
					e.printStackTrace()
				}
			}
			if(params?.longDuration.equals("on")){
				longDuration = true
			}else{
				longDuration = false
			}


			boolean skipStatus
			if(params?.skipStatus.equals("on")){
				skipStatus = true
			}else{
				skipStatus = false
			}
			
			
			if(params?.advScript.equals("on")){
				isAdvanced = true
			}else{
				isAdvanced = false
			}

			def catgry = Utility.getCategory(category)

			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
			xml.xml(){
				xml.id(scrpt?.id)
				mkp.yield "\r\n  "
				mkp.comment "Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty"
				xml.version(vers2)
				mkp.yield "\r\n  "
				mkp.comment "Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1"
				xml.name(newScriptName)
				mkp.yield "\r\n  "
				mkp.comment "If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension"
				xml.primitive_test_id(ptest?.id)
				mkp.yield "\r\n  "
				mkp.comment "Do not change primitive_test_id if you are editing an existing script."
				xml.primitive_test_name(ptest?.name)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.primitive_test_version(ptest?.version)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.status(Status.FREE)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.synopsis(params.synopsis?.trim())
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.groups_id(utilityService.getGroup()?.id)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.execution_time(time)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.long_duration(longDuration)
				mkp.yield "\r\n  "
				mkp.comment ""
				xml.advanced_script(isAdvanced)
				mkp.yield "\r\n  "
				mkp.comment "execution_time is the time out time for test execution"
				xml.remarks(params?.remarks?.trim())
				mkp.yield "\r\n  "
				mkp.comment "Reason for skipping the tests if marked to skip"
				xml.skip(skipStatus?.toString())
				mkp.yield "\r\n  "
				mkp.comment ""

				/*def bTypeList = params?.boxTypes
				 if(bTypeList instanceof List){
				 bTypeList = bTypeList?.sort()
				 }*/
				def bTypeList = params?.list("boxTypes")

				xml.box_types(){
					bTypeList?.each { bt ->
						def btype = BoxType.findById(bt)
						bTypes.add(btype)
						xml.box_type(btype?.name)
						mkp.yield "\r\n    "
						mkp.comment ""
					}
				}

				/*def rdkVersList = params?.rdkVersions
				 if(rdkVersList instanceof List){
				 rdkVersList = rdkVersList?.sort()
				 }*/

				def rdkVersList = params?.list("rdkVersions")
				xml.rdk_versions(){
					rdkVersList?.each { vers ->
						def rdkVer = RDKVersions.findById(vers)
						rdkVers.add(rdkVer)
						xml.rdk_version(rdkVer?.buildVersion)
						mkp.yield "\r\n    "
						mkp.comment ""
					}
				}
				if(scrpt?.testCaseDetails){
					xml?.test_cases(){
						xml.test_case_id(scrpt?.testCaseDetails.testCaseId)
						xml.test_objective(scrpt?.testCaseDetails.testObjective)
						xml.test_type(scrpt?.testCaseDetails.testType)
						xml.test_setup(scrpt?.testCaseDetails.testSetup)
						//xml.steam_id(testCaseMap.streamId)
						xml.pre_requisite(scrpt?.testCaseDetails.preRequisites)
						xml.api_or_interface_used(scrpt?.testCaseDetails.interfaceUsed)
						xml.input_parameters(scrpt?.testCaseDetails.inputParameters)
						xml.automation_approch(scrpt?.testCaseDetails.automationApproch)
						xml.expected_output(scrpt?.testCaseDetails.expectedOutput) 
						xml.priority(scrpt?.testCaseDetails.priority)
						xml.test_stub_interface(scrpt?.testCaseDetails.testStubInterface)
						xml.test_script(scrpt?.testCaseDetails.testScript)
						xml.skipped(scrpt?.testCaseDetails.tcskip)
						xml.release_version(scrpt?.testCaseDetails.releaseVersion)
						xml.remarks(scrpt?.testCaseDetails.remarks)
					}
				}else{
					xml?.test_cases(){
						xml.test_case_id("")
						xml.test_objective("")
						xml.test_type("")
						xml.test_setup("")
						//xml.steam_id("")
						xml.pre_requisite("")
						xml.api_or_interface_used("")
						xml.input_parameters("")
						xml.automation_approch("")
						xml.expected_output("")
						xml.priority("")
						xml.test_stub_interface("")
						xml.test_script("")
						xml.skipped("")
						xml.release_version("")
						xml.remarks("")
					}
				}
				def scriptTagList = params?.scriptTags
				/*if(scriptTagList instanceof List){
				 scriptTagList = scriptTagList?.sort()
				 }*/
				try {
					xml.script_tags(){
						scriptTagList?.each { tag ->
							def sTag = ScriptTag.findById(tag)
							scrptTags.add(sTag)
							xml.script_tag(sTag?.name)
							mkp.yield "\r\n    "
							mkp.comment ""
						}
					}
				} catch (Exception e) {
					println " error "+e.getMessage()
					e.printStackTrace()
				}
				if(params?.testProfile)	{
					def  scriptTestProfiles = params?.testProfile
					if(scriptTestProfiles && scriptTestProfiles?.size() >  0){
						xml.test_profiles(){
							scriptTestProfiles?.each{
								def tProfile = TestProfile?.findById(it)
								testProfileList.add(tProfile?.toString())
								xml.test_profile(tProfile)
							}
						}
					}
				}
				
			}
			dirname = ptest?.module?.name
			dirname = dirname?.trim()
			isAdvanced = isAdvanced || (!oldAdvStatus && Utility.isAdvancedScript(params?.prevScriptName, dirname))
			def scriptsDirName1 = primitiveService.getScriptDirName(moduleName)
			def testScriptPath = getTestScriptPath(catgry,isAdvanced)
			File dir = new File( testScriptPath+FILE_SEPARATOR+scriptsDirName1+FILE_SEPARATOR+dirname+"/")
			if(!dir.exists()){
				dir.mkdirs()
			}
			File file = new File( testScriptPath+FILE_SEPARATOR+scriptsDirName1+FILE_SEPARATOR+dirname+FILE_SEPARATOR+newScriptName+".py");
			boolean checkOldFile = false
			
			try {
				if(!oldAdvStatus?.equals(isAdvanced)){
					def oldPath = getTestScriptPath(catgry,oldAdvStatus)
					File oldFile = new File( oldPath+FILE_SEPARATOR+scriptsDirName1+FILE_SEPARATOR+dirname+FILE_SEPARATOR+newScriptName+".py")
					if(oldFile?.exists()){
						oldFile?.renameTo(file)
					}
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
			
			if(!file.exists()){
				file.createNewFile()
			}

			def headerFile
			if(isAdvanced){
				headerFile = "pyRDKMHeader.txt"
			}else{
				headerFile = "pyHeader.txt"
			}
			File pyHeader = new File( "${request.getRealPath('/')}//fileStore//${headerFile}")
			def pyHeaderContentList = pyHeader?.readLines()
			String pyHeaderContent = ""
			pyHeaderContentList.each {
				pyHeaderContent += it?.toString()+"\n"
			}
			String data =pyHeaderContent+"'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea

			//String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+params?.scriptArea
			file.write(data)
			if(params?.prevScriptName != params?.name && prevScriptName != newScriptName){
				//File file1 = new File( "${request.getRealPath('/')}//fileStore//testscripts/"+scriptsDirName1+"/"+dirname+"/"+params?.prevScriptName?.trim()+".py");
				File file1 = new File( testScriptPath+FILE_SEPARATOR+scriptsDirName1+FILE_SEPARATOR+dirname+FILE_SEPARATOR+prevScriptName+".py");
				if(file1.exists() ){
					file1.delete()
				}
			}
			saveScript = true
		} catch (Exception e) {
			e.printStackTrace()
		}

		def boxTypes = bTypes?.toList()
		def boxTypesList = []
		//		scriptInstance.name = params.name
		//		scriptInstance.scriptContent = params.scriptArea
		//		scriptInstance.synopsis = params.synopsis
		//		scriptInstance.remarks = params?.remarks
		//
		//		if(params?.skipStatus.equals("on")){
		//			scriptInstance.skip = true
		//		}else{
		//		scriptInstance.skip = false
		//		}
		//		scriptInstance.primitiveTest = PrimitiveTest.findById(params.ptest)
		//		scriptInstance.executionTime = Integer.parseInt(params?.executionTime)
		//
		//		if (!scriptInstance.save(flush: true)) {
		//			log.error "Error saving Script instance : ${scriptInstance.errors}"
		//			return
		//		}
		//
		//		if(boxTypes){
		//			boxTypesList = scriptgroupService.createBoxTypeList(boxTypes)
		//			scriptgroupService.removeScriptsFromBoxSuites(scriptInstance)
		//			scriptgroupService.saveToDefaultGroup(scriptInstance, boxTypesList)
		//		}
		//
		//		scriptInstance.properties = params
		//
		//		scriptgroupService.updateScriptsFromRDKVersionBoxTypeTestSuites(scriptInstance)
		if(prevScriptName != newScriptName ){
			def sFile = ScriptFile.findByScriptName(params?.prevScriptName)
			sFile.scriptName = params?.name
			sFile.save()
			scriptService.updateScriptNameChange(params?.prevScriptName,sFile, params?.category)
		}

		clearEditLock(params?.name)
		if(!saveScript){
			log.error "Error saving Script instance : ${params.name}"
			return
		}else{
			def script = ScriptFile.findByScriptNameAndModuleName(newScriptName,ptest?.module?.name)
			if(script == null){
				script = new ScriptFile()
				script.setScriptName(newScriptName)
				script.setModuleName(ptest?.module?.name)
				if((ptest?.module?.name == Constants.RDKSERVICES) || (ptest?.module?.testGroup == TestGroup.Certification)){
					script.category = Utility.getCategory(Category?.RDKV_RDKSERVICE.toString())
				}else{
					script.category = Utility.getCategory(params?.category)
				}
				script.save(flush:true)
			}

			def sObject = new ScriptObject()
			sObject.setBoxTypes(bTypes)
			sObject.setRdkVersions(rdkVers)
			sObject.setName(newScriptName)
			sObject.setModule(ptest?.module?.name)
			sObject.setScriptFile(script)
			sObject.setScriptTags(scrptTags)
			sObject.setLongDuration(longDuration)
			sObject.setTestProfile(testProfileList)
			if((ptest?.module?.name != Constants.RDKSERVICES) && (ptest?.module?.testGroup != TestGroup.Certification)){
				if(boxTypes){
					scriptgroupService.removeScriptsFromBoxScriptGroup(script,boxTypes,oldBoxTypes)
					if(isLongDuration != longDuration){
						scriptgroupService.updateScriptGroup(script,sObject, params?.category)
					}
				}
			
				scriptgroupService.saveToScriptGroups(script,sObject, params?.category)
				scriptgroupService.saveToDefaultGroups(script,sObject, bTypes,  params?.category)
				scriptgroupService.updateScriptsFromRDKVersionBoxTypeTestSuites1(script, sObject, params?.category)
				scriptgroupService.updateScriptsFromRDKVersionBoxTypeTestGroup(script,sObject,oldRDKVersions,oldBoxTypes)
				scriptgroupService.updateScriptsFromScriptTag(script,sObject,oldTags,oldBoxTypes ,params?.category)
				scriptService?.updateScriptsFromTestProfile(script,sObject, params.category)
				flash.message = message(code: 'default.updated.message', args: [
					message(code: 'script.label', default: 'Script'),
					params.name
				])
				scriptService.updateAdvScriptMap(newScriptName, dirname, Utility.getCategory(params?.category), isAdvanced)
			}
		}
		def newid= params?.id
		if(params?.id?.contains("@")){
			newid = params?.id?.split("@")[0]+"@"+params?.name
		}
		redirect(action: "list", params: [scriptId: newid])
	}

	/**
	 * Get Module name, version and testGroup
	 * through ajax call
	 * @return
	 */
	def getModuleName(){
		List moduleDetails = []
		def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def moduleName = moduleMap.get(params?.primId)
		def module = Module.findByName(moduleName)
		moduleDetails.add(module.name.toString().trim() )
		moduleDetails.add(module.rdkVersion.toLowerCase().trim() )
		moduleDetails.add( module.testGroup.toString().trim() )
		moduleDetails.add(module.executionTime.toString().trim() )
		render moduleDetails as JSON
	}

	/**
	 * Show streaming details in a popup in script page
	 * @param max
	 * @return
	 */
	def showStreamDetails(){
		def streamingDetailsList = StreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
		def radioStreamingDetails = RadioStreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
		[streamingDetailsInstanceList: streamingDetailsList, radioStreamingDetails:radioStreamingDetails, streamingDetailsInstanceTotal: streamingDetailsList.size()]
		// [streamingDetailsInstanceList: StreamingDetails.list(), streamingDetailsInstanceTotal: StreamingDetails.count()]
	}

	/**
	 * Get the list of scripts based on the scriptName.
	 * @return
	 */
	def searchScript(){
		//        def scripts = Script.findAll("from Script as b where b.name like '%${params?.searchName}%'")
		def category = params?.categoryFilter?.trim()
		def moduleMap = null
		def scriptNameList = []
		def scripts = []
		def searchName = params?.searchName?.trim()
		if(category.equals(RDKB_TCL)){
			scriptNameList = scriptService.getTCLNameList(getRealPath())
			if(searchName){
				if(scriptNameList.contains(searchName)){
					scripts.add(searchName)
				}
			}
			else{
				scripts = scriptNameList
			}

		}
		else{
			scriptNameList = scriptService.getScriptNameList(getRealPath(), category)
			moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
			scriptNameList?.each {
				if(it?.toLowerCase()?.contains(searchName?.toLowerCase())){
					def moduleName = moduleMap.get(it)
					def script = scriptService.getScript(getRealPath(), moduleName, it, category)
					if(script){
						scripts.add(script)
					}
				}
			}
		}
		String value = ""
		if(scripts == null || scripts.empty){
			value = FALSE
		}else{
			value = TRUE
		}

		render(template: "searchList", model: [scriptList : scripts, category: category, value : value])
	}

	/**
	 * Get the list of scripts based on the scriptName, primitiveTest and selected box types.
	 * @return
	 */
	def advsearchScript(){
		def scriptList = scriptgroupService.getAdvancedSearchResult(params?.searchName,params?.primtest,params?.selboxTypes)
		render(template: "searchList", model: [scriptList : scriptList])
	}

	/**
	 * Adds a new scriptGroup based on the selection of scripts from the 
	 * list of scripts obtained after performing a search
	 * @return
	 */
	def addScriptGroupfromSeachList(){

		def category = params?.category
		def selectedScripts = params.findAll { it.value == KEY_ON }
		if(params?.suiteRadioGroup.equals( KEY_EXISTING )){
			ScriptGroup scriptGroup = ScriptGroup.findById(params?.testsuite)
			if(scriptGroup){
				def scriptInstance
				selectedScripts.each{
					def moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
					def moduleName = moduleMap.get(it?.key)
					def script = ScriptFile.findByScriptNameAndModuleName(it.key,moduleName)
					if(script){
						scriptInstance = scriptGroup.scriptList.find { it.id == script?.id }
						if(!scriptInstance){
							scriptGroup.addToScriptList(script)
						}
					}
				}
			}
			flash.message = message(code: 'default.updated.message', args: [message(code: 'scriptGroup.label', default: 'Test Suite'),scriptGroup])
		}
		else{
			def scriptGroupInstance = new ScriptGroup()

			if(ScriptGroup.findByName(params?.newSuiteName)){
				flash.message =  message(code: 'script.add.group')
			}
			else if(!(selectedScripts)){
				flash.message = message(code: 'script.empty.select')
			}
			else{
				scriptGroupInstance.name = params?.newSuiteName
				scriptGroupInstance.category = Utility.getCategory(category)
				selectedScripts.each{
					def moduleMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
					def moduleName = moduleMap.get(it?.key)
					def script = ScriptFile.findByScriptNameAndModuleName(it.key,moduleName)
					if(script){
						scriptGroupInstance.addToScriptList(script)
					}
					flash.message = message(code: 'default.created.message', args: [
						message(code: 'scriptGroup.label', default: 'Test Suite'),
						scriptGroupInstance.name
					])
				}
			}
			if (!scriptGroupInstance.save(flush: true)) {
				flash.message = message(code: 'default.created.message', args: [
					message(code: 'scriptGroup.label', default: 'Test Suite'),
					scriptGroupInstance.name])
			}
		}
		redirect(action: "list")
	}



	/**
	 * Method to check whether script with same name exist or not. If yes returns the id of script
	 * @return
	 */
	def fetchScript(){
		List scriptInstanceList = []
		def scriptMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
		def mName = scriptMap.get(params.scriptName)
		def scriptInstance = scriptService.getScript(getRealPath(), mName, params.scriptName, params?.category)
		//		Script scriptInstance = Script.findByName(params.scriptName)
		if(scriptInstance){
			scriptInstanceList.add(scriptInstance.name)
		}
		render scriptInstanceList as JSON
	}
	
	/**
	 * Function to fetch the script file from database
	 * @return
	 */
	def fetchScriptFromDb(){
		List scriptInstanceList = []
		def scriptInstance = null
		if(params.scriptName){
			scriptInstance = ScriptFile.findByScriptNameAndCategory(params?.scriptName.trim()?.toString(),params?.category?.trim())
			if(scriptInstance){
				scriptInstanceList.add(scriptInstance.scriptName)
			}
		}
		render scriptInstanceList as JSON
	}
	
	def fetchScriptWithScriptName(){

		List scriptInstanceList = []
		def scriptMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
		def mName = scriptMap.get(params.scriptName)
		def scriptInstance = scriptService.getScript(getRealPath(), mName, params.scriptName, params?.category)
		//		Script scriptInstance = Script.findByName(params.scriptName)
		if(scriptInstance){
			scriptInstanceList.add(mName+"@"+scriptInstance.name)
		}
		render scriptInstanceList as JSON
	}



	/**
	 * Method to trigger downloading the script content as python script file in script page.
	 * @return
	 */
	def exportScriptContent(){
		def opFail = false
		if(params?.id){
			if(Category.RDKB_TCL.toString().equals(params?.category?.trim())){
				if(!exportTclScript(params)){
					opFail = true
				}
			}
			else{
				if(!exportScript(params)){
					opFail = true
				}
			}
			if(opFail){
				flash.message = "Download failed. No valid script is available for download."
				redirect(action: "list")
			}
		}else{
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}
	
	/**
	 * Method to trigger downloading the script content as a Javascript file in script page.
	 * @return
	 */
	def exportThunderScriptContent(){
		def opFail = false
		if(params?.id){
			if(!exportScriptThunder(params)){
				opFail = true
			}
			if(opFail){
				flash.message = "Download failed. No valid script is available for download."
				redirect(action: "list")
			}
		}else{
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}
	/**
	 * Method to get the script content from script file for storm scripts.
	 * @param params
	 * @return
	 */
	def exportScriptThunder(def params){
		try{
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_FRAMEWORK_LOCATION = StormExecuter.getConfigProperty(configFile,Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
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
						if(fileName.equals(params?.id)){
							path = fileStorePath + directory + File.separator + params?.id + JAVASCRIPT_EXTENSION
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
			File sFile = new File(path)
			if(sFile.exists()){
				params.format = TEXT
				params.extension = JAVASCRIPT
				String data = new String(sFile.getBytes())
				response.setHeader("Content-Type", "application/octet-stream;")
				response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.id+JAVASCRIPT_EXTENSION+"\"")
				response.outputStream << data.getBytes()
			}else{
				flash.message = "Download failed. No valid script is available for download."
				redirect(action: "list")
			}
		}
		}catch(Exception e){
			e.printStackTrace
		}
	}
	
	/**
	 * Method to trigger downloading of all test cases belongs to the input category
	 */
	def exportAllTestCases() {
		def category  = params?.category ? params?.category : RDKV
		def requestGetRealPath = request.getRealPath("/")
		def scriptGroupMap = scriptService.getScriptsMap(requestGetRealPath, category)
		if(scriptGroupMap.size() > 0) {
			ZipOutputStream zos = new ZipOutputStream(response.outputStream);
			params.format = EXPORT_ZIP_FORMAT
			params.extension = EXPORT_ZIP_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			response.setHeader("Content-Type", "application/zip")
			response.setHeader("Content-disposition", "attachment; filename=Testcases_"+ category +".${params.extension}")
			scriptGroupMap.each { entry->
				def fileName = entry?.key + ".xls"
				zos.putNextEntry(new ZipEntry(fileName))
				try{
					params?.moduleName = entry?.key
					def totalTestCaseMap =testCaseService?.downloadModuleTestCaseInExcel(params,getRealPath())
					excelExportService?.exportTestSuiteTestCase(entry?.key, zos ,totalTestCaseMap, testCaseService?.testCaseKeyMap())
					zos.closeEntry()
				}catch(Exception e){
					println "ERROR "+e.printStackTrace()
				}
			}
			zos.close();
		}
	}

	/**
	 * Method to trigger downloading the script content as python script file from the execution result page.
	 * @return
	 */
	def exportScriptData(){
		if(params?.id){
			if(scriptService.tclScriptsList.toString()?.contains(params?.id?.trim()) ){
				if(!exportTclScript(params)){
					flash.message = "Download failed. No valid script is available for download."
					render "Failed to download Script."
				}
			}
			else if(!exportScript(params)){
				flash.message = "Download failed. No valid script is available for download."
				render "Failed to download Script."
			}
		}else{
			flash.message = "Download failed. No valid script is available for download."
			render "Failed to download Script."
		}
	}


	/**
	 * Method to download the script content as pythoin file.
	 * @param params
	 * @return
	 */
	/*def exportScript(def params){
	 def sMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
	 def category = params?.category
	 def moduleName = sMap.get(params?.id)
	 def scriptDir = primitiveService.getScriptDirName(moduleName)
	 File sFile = new File(getRealPath()+"/fileStore/testscripts/"+scriptDir+"/"+moduleName+"/"+params?.id+".py")
	 if(sFile.exists()){
	 params.format = "text"
	 params.extension = "py"
	 String data = new String(sFile.getBytes())
	 response.setHeader("Content-Type", "application/octet-stream;")
	 response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.id+".py\"")
	 response.setHeader("Content-Length", ""+data.length())
	 response.outputStream << data.getBytes()
	 return true
	 }
	 return false
	 }*/

	def exportScript(def params){
		def sMap = scriptService.getScriptNameModuleNameMapping(getRealPath())
		def category = params?.category
		def moduleName = sMap.get(params?.id)
		def scriptDir = primitiveService.getScriptDirName(moduleName)
		if(category == null){
			category = primitiveService.getCategory(moduleName)
		}
		def path = getTestScriptPath(category,params?.id,moduleName) + FILE_SEPARATOR + scriptDir+ FILE_SEPARATOR +moduleName + FILE_SEPARATOR + params?.id+".py"
		File sFile = new File(path)
		if(sFile.exists()){
			params.format = "text"
			params.extension = "py"
			String data = new String(sFile.getBytes())
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.id+".py\"")
			//response.setHeader("Content-Length", ""+data.length())  // Issue fix parial script download
			response.outputStream << data.getBytes()
		}else {
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}

	/**
	 * Method to download the script content as tcl file.
	 * @param params
	 * @return
	 */
	def exportTclScript(def params){
		def category = params?.category
		def path = Utility.getTclDir(getRealPath())+FILE_SEPARATOR + params?.id+".tcl"
		File sFile = new File(path)
		if(sFile?.exists()){
			params.format = "text"
			params.extension = "tcl"
			String data = new String(sFile.getBytes())
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.id+".tcl\"")
			response.setHeader("Content-Length", ""+data.length())
			response.outputStream << data.getBytes()
		}else {
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}


	/***
	 *  Downloads tcl script
	 */
	def exportTCL(){
		def scriptName = params?.scriptName?.trim()
		def path = getTestScriptPath(Category.RDKB_TCL.toString())
		File file = new File(path + FILE_SEPARATOR + scriptName + ".tcl")
		if(file.exists()){
			params.format = "text"
			params.extension = "tcl"
			String data = new String(file.getBytes())
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ scriptName+".tcl\"")
			response.setHeader("Content-Length", ""+data.length())
			response.outputStream << data.getBytes()
		}else {
			flash.message = "Download failed. No valid script is available for download."
			redirect(action: "list")
		}
	}
	def exportScriptAsXML(){
		//		exportCurrentScript(params,response)

		exportAllPrimitive();
		exportAllScripts();
		//		redirect(action: "list", params: params)
		//		if(params?.id){
		//			Script script = Script.findById(params?.id)
		//
		//			def writer = new StringWriter()
		//			def xml = new MarkupBuilder(writer)
		//			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
		//			xml.xml(){
		//				xml.name(script?.name)
		//				xml.id(script?.id)
		//				xml.version(1)
		//				xml.primitiveTestid(script?.primitiveTest?.id)
		//				xml.primitiveTestName(script?.primitiveTest?.name)
		//				xml.primitiveTestVersion(script?.primitiveTest?.version)
		//				xml.status(script?.status)
		//				xml.synopsis(script?.synopsis?.trim())
		//				xml.groupsid(script?.groups?.id)
		//				xml.execution_time(script?.executionTime)
		//				xml.remarks(script?.remarks?.trim())
		//				xml.skip(script?.skip?.toString())
		//
		//			}
		//			response.setHeader "Content-disposition", "attachment; filename=${script?.name}.py"
		//			response.contentType = 'application/octet-stream;'
		//			response.outputStream << "'''"
		//			response.outputStream << "\n"
		//			response.outputStream << writer.toString()
		//			response.outputStream << "\n"
		//			response.outputStream << "'''"
		//			response.outputStream << "\n"
		//			response.outputStream << script?.scriptContent
		//			response.outputStream.flush()
		//		}
	}
	def exportCurrentScript(params,response){
		if(params?.id){
			Script script = Script.findById(params?.id)

			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
			xml.xml(){
				xml.name(script?.name)
				mkp.comment "If you are adding a new script you can specify the script name."
				xml.id(script?.id)
				xml.version(1)
				xml.primitiveTestid(script?.primitiveTest?.id)
				xml.primitiveTestName(script?.primitiveTest?.name)
				xml.primitiveTestVersion(script?.primitiveTest?.version)
				xml.status(script?.status)
				xml.synopsis(script?.synopsis?.trim())
				xml.groupsid(script?.groups?.id)
				xml.execution_time(script?.executionTime)
				xml.remarks(script?.remarks?.trim())
				xml.skip(script?.skip?.toString())

			}
			response.setHeader "Content-disposition", "attachment; filename=${script?.name}.py"
			response.contentType = 'application/octet-stream;'
			response.outputStream << "'''"
			response.outputStream << "\n"
			response.outputStream << writer.toString()
			response.outputStream << "\n"
			response.outputStream << "'''"
			response.outputStream << "\n"
			response.outputStream << script?.scriptContent
			response.outputStream.flush()
		}
	}


	def exportAllScripts(){
		try {
			def groupsInstance = utilityService.getGroup()
			def scriptInstanceList = Script.findAllByGroupsOrGroupsIsNull(groupsInstance)
			def sMap = createScriptList(scriptInstanceList)

			def mList = Module.findAll()
			mList.each {  modl ->

				def sList = sMap.get(modl?.name)

				sList.each { script ->
					def writer = new StringWriter()
					def xml = new MarkupBuilder(writer)
					xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
					xml.xml(){
						xml.id(script?.id)
						mkp.yield "\r\n  "
						mkp.comment "Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty"
						xml.version(1)
						mkp.yield "\r\n  "
						mkp.comment "Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1"
						xml.name(script?.name)
						mkp.yield "\r\n  "
						mkp.comment "If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension "
						xml.primitive_test_id(script?.primitiveTest?.id)
						mkp.yield "\r\n  "
						mkp.comment "Do not change primitive_test_id if you are editing an existing script."
						xml.primitive_test_name(script?.primitiveTest?.name)
						mkp.yield "\r\n  "
						mkp.comment ""
						xml.primitive_test_version(script?.primitiveTest?.version)
						mkp.yield "\r\n  "
						mkp.comment ""
						xml.status(script?.status)
						mkp.yield "\r\n  "
						mkp.comment ""
						xml.synopsis(script?.synopsis?.trim())
						mkp.yield "\r\n  "
						mkp.comment ""
						xml.groups_id(script?.groups?.id)
						mkp.yield "\r\n  "
						mkp.comment ""
						xml.execution_time(script?.executionTime)
						mkp.yield "\r\n  "
						mkp.comment ""
						xml.long_duration(script?.longDuration)
						mkp.yield "\r\n  "
						mkp.comment "execution_time is the time out time for test execution"
						xml.remarks(script?.remarks?.trim())
						mkp.yield "\r\n  "
						mkp.comment "Reason for skipping the tests if marked to skip"
						xml.skip(script?.skip?.toString())
						mkp.yield "\r\n  "
						mkp.comment ""
						xml.box_types(){
							script.boxTypes.each { bt ->
								xml.box_type(bt.name)
								mkp.yield "\r\n    "
								mkp.comment ""
							}
						}
						xml.rdk_versions(){
							script.rdkVersions.each { vers ->
								xml.rdk_version(vers.buildVersion)
								mkp.yield "\r\n    "
								mkp.comment ""
							}
						}

					}

					String dirname = modl?.name
					dirname = dirname?.trim()
					def scriptsDirName = primitiveService.getScriptDirName(dirname)
					File dir = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/")
					if(dir.exists()){
						dir.mkdirs()
					}

					File file = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/"+script?.name?.trim()+".py");
					if(!file.exists()){
						file.createNewFile()
					}
					String data = "'''"+"\n"+writer.toString() +"\n"+"'''"+"\n"+script?.scriptContent
					file.write(data)
				}

			}
		} catch (Exception e) {
			e.printStackTrace()
		}

	}
	def exportAllPrimitive(){

		try {
			def mList = Module.findAll()
			mList.each {  modl ->


				def writer = new StringWriter()
				def xml = new MarkupBuilder(writer)
				xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
				xml.xml(){

					module("name":modl?.name, "testGroup":modl.testGroup){

						xml.primitiveTests(){
							def pList = PrimitiveTest.findAllByModule(modl)
							if(pList){

								pList.each { primitive ->
									xml.primitiveTest(name : primitive?.name, id : primitive?.id , version :primitive?.version ){
										xml.function(primitive?.function?.name)
										xml.parameters(){
											primitive.parameters.each { param ->
												parameter("name" :param.parameterType.name,"value" :param.value)
											}
										}
									}

								}
							}
						}
					}
				}
				String dirname = modl?.name
				dirname = dirname?.trim()
				def scriptsDirName = primitiveService.getScriptDirName(dirname)
				File dir = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/")

				if(!dir.exists()){
					dir.mkdirs()
				}

				File file = new File( "${request.getRealPath('/')}/fileStore/testscripts/"+scriptsDirName+"/"+dirname+"/"+dirname+XML);
				if(!file.exists()){
					file.createNewFile()
				}
				file.write(writer.toString())
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	def addEditLock(){
		def scriptName = params?.scriptName
		if(ScriptService.scriptLockList.contains(scriptName)){
			ScriptService.scriptLockList.add(params?.scriptName)
			render FALSE as String
			return
		}else{
			ScriptService.scriptLockList.add(params?.scriptName)
		}
		render TRUE as String
	}

	def clearEditLock(def scriptName){
		ScriptService.scriptLockList.remove(scriptName)
	}

	def removeEditLock(){
		ScriptService.scriptLockList.remove(params?.scriptName)
	}

	/**
	 * REST method to retrieve the script list 
	 * @param scriptGroup
	 * @return
	 */
	def getScriptsByScriptGroup(String scriptGroup){
		JsonObject scriptJson = new JsonObject()
		try {
			if(scriptGroup){
				ScriptGroup sg = ScriptGroup.findByName(scriptGroup)
				if(sg){
					JsonArray scriptArray = new JsonArray()
					scriptJson.add(scriptGroup, scriptArray)
					sg?.scriptList?.each { scrpt ->
						JsonObject script = new JsonObject()
						script.addProperty("name", scrpt?.scriptName)
						script.addProperty("module", scrpt?.moduleName)
						scriptArray?.add(script)
					}
				}else{
					scriptJson.addProperty("status", "failure")
					scriptJson.addProperty("remarks", "No script groups found with name "+scriptGroup)
				}
			}else{
				Map sgMap = scriptService?.getScriptsMap(getRealPath())
				sgMap?.keySet().each { key ->
					List sList = sgMap.get(key)
					if(sList){
						JsonArray scriptArray = new JsonArray()
						scriptJson.add(key, scriptArray)
						sList?.each{sname ->
							ScriptFile scrpt = ScriptFile.findByScriptNameAndModuleName(sname,key)
							if(scrpt){
								JsonObject script = new JsonObject()
								script.addProperty("name", scrpt?.scriptName)
								scriptArray?.add(script)
							}
						}
					}
				}
			}
		} catch (Exception e) {
			println " Error getScriptNameList "+e.getMessage()
			e.printStackTrace()
		}
		render scriptJson
	}

	/**
	 * REST method to retrieve the script list
	 * @param moduleName
	 * @return
	 */
	def getScriptsByModule(String moduleName){
		JsonObject scriptJson = new JsonObject()
		try {
			if (moduleName){
				Map sgMap = scriptService?.getScriptsMap(getRealPath())
				List sList = sgMap.get(moduleName)
				if(sgMap){
					JsonArray scriptArray = new JsonArray()
					scriptJson.add(moduleName, scriptArray)
					sList?.each{sname ->
						ScriptFile scrpt = ScriptFile.findByScriptNameAndModuleName(sname,moduleName)
						if(scrpt){
							JsonObject script = new JsonObject()
							script.addProperty("name", scrpt?.scriptName)
							scriptArray?.add(script)
						}
					}
				}else{
					scriptJson.addProperty("status", "failure")
					scriptJson.addProperty("remarks", "no module found with name "+moduleName)
				}
			}else{
				Map sgMap = scriptService?.getScriptsMap(getRealPath())
				sgMap?.keySet().each { key ->
					List sList = sgMap.get(key)
					if(sList){
						JsonArray scriptArray = new JsonArray()
						scriptJson.add(key, scriptArray)
						sList?.each{sname ->
							ScriptFile scrpt = ScriptFile.findByScriptNameAndModuleName(sname,key)
							if(scrpt){
								JsonObject script = new JsonObject()
								script.addProperty("name", scrpt?.scriptName)
								scriptArray?.add(script)
							}
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		render scriptJson
	}

	/**
	 * REST API :  The function implements for get all Script group details  
	 * @return
	 */

	def getAllScriptGroups(){
		JsonObject scriptGrpObj = new JsonObject()
		JsonArray scripts = new JsonArray()
		def scriptCount = 0
		try{
			def scriptGrpList  = ScriptGroup.list()
			scriptGrpList?.each{scriptGrpName ->
				JsonObject scriptGrp = new JsonObject()
				scriptCount = scriptGrpName?.scriptList?.size()
				scriptGrp?.addProperty("name",scriptGrpName.toString())
				scriptGrp?.addProperty("scriptcount",scriptCount.toString())
				scripts.add(scriptGrp)
			}
			scriptGrpObj.add("scriptgroups",scripts)
		}catch(Exception e){
		}

		render scriptGrpObj
	}

	/**
	 * REST API :
	 * function used to delete test suite
	 * @param suiteName
	 * @return
	 */
	def deleteScriptGroup(final String scriptGroup){

		JsonObject scriptGrp = new JsonObject()
		try{
			Subject currentUser = SecurityUtils.getSubject()
			if(currentUser?.hasRole('ADMIN')){
				def scriptGroupInstance = ScriptGroup?.findByName(scriptGroup)
				if(scriptGroupInstance){
					if(scriptGroupInstance?.delete(flush :true)){
						scriptGrp?.addProperty("status", "SUCCESS")
						scriptGrp?.addProperty("remarks","ScriptGroup deleted successfully " )
					}else{
						if(ScriptGroup?.findByName(scriptGroup)){
							scriptGrp?.addProperty("status", "FAILURE")
							scriptGrp?.addProperty("remarks","Error in Deleting ScriptGroup" )
						}else{
							scriptGrp?.addProperty("status", "SUCCESS")
							scriptGrp?.addProperty("remarks","ScriptGroup deleted successfully " )
						}
					}

				}else{
					scriptGrp?.addProperty("status", "FAILURE")
					scriptGrp?.addProperty("remarks","no script group found with name "+ scriptGroup)
				}
			}else{
				scriptGrp?.addProperty("status", "FAILURE")
				if(currentUser?.principal){
					scriptGrp?.addProperty("remarks","current user ${currentUser?.principal} don't have permission to delete script group" )
				}else{
					scriptGrp?.addProperty("remarks","login as admin user to perform this operation" )
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
		render scriptGrp
	}
	
	/**
	 * 
	 * Method to get the test scripts path not considering the advance test scripts.
	 */
	private String getTestScriptPath(def category){
		category = Utility.getCategory(category?.trim())
		return getTestScriptPath(category, false)
	}
	
	/**
	 *
	 * Method to get the test scripts path not considering the advance test scripts.
	 */
	private String getTestScriptPath(def category,boolean isAdvanced){
		def path = null
		switch(category){
			case Category.RDKV:
				if(!isAdvanced){
					path = getRealPath() +  FILESTORE + FILE_SEPARATOR + FileStorePath.RDKV.value()
				}else{
					path = getRealPath() +  FILESTORE + FILE_SEPARATOR + FileStorePath.RDKVADVANCED.value()
				}
				break;
			case Category.RDKB:
				if(!isAdvanced){
					path = getRealPath() +  FILESTORE + FILE_SEPARATOR + FileStorePath.RDKB.value()
				}else{
					path = getRealPath() +  FILESTORE + FILE_SEPARATOR + FileStorePath.RDKBADVANCED.value()
				}
				break;
			case Category.RDKC:
				path = getRealPath() +  FILESTORE + FILE_SEPARATOR + FileStorePath.RDKC.value()
				break;
			case Category.RDKB_TCL:
				path = getRealPath()  + FILESTORE + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
				break;
			case Category.RDKV_RDKSERVICE:
				path = getRealPath()  + FILESTORE + FILE_SEPARATOR + FileStorePath.RDKV_RDKSERVICE.value()
				break;
			default:
				break;
		}
		return path
	}
	
	/**
	 * Method to get the Test Script path considering the Advanced Test scripts also.
	 */
	private String getTestScriptPath(def category,def scriptName , def moduleName){
		category = Utility.getCategory(category?.trim())
		boolean isAdvanced = Utility.isAdvancedScript(scriptName, moduleName)
		return getTestScriptPath(category, isAdvanced)
	}
	/**
	 * REST API :- create a new suite
	 * params : file uploaded through the Curl command
	 * Eg : curl http://localhost:8080/rdk-test-tool/scriptGroup/
	 */

	def createNewScriptGroup(){
		JsonObject scriptGroup = new JsonObject()
		ScriptGroup scriptGroupInstance = new ScriptGroup()
		def fileName
		String xml
		def node
		String  idList
		def category
		boolean valid = false
		if(params?.scriptGroupXml){
			def uploadedFile = request.getFile('scriptGroupXml')
			if(uploadedFile?.originalFilename?.endsWith(XML)){
				fileName = uploadedFile?.originalFilename?.replace(XML,"")
				InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
				def fileContent = reader?.readLines()
				if(ScriptGroup.findByName(fileName.trim())){
					scriptGroup?.addProperty("STATUS","FAILURE")
					scriptGroup.addProperty("Remarks","The test suite name already exists")
				}else{
					if(fileContent){
						try{
							String s = ""
							//int indx = 0
							int indx = fileContent?.findIndexOf { it.startsWith("<?xml")}
							String scriptContent = ""
							if(fileContent.get(indx))	{
								while(indx < fileContent.size()){
									s = s + fileContent.get(indx)+"\n"
									indx++
								}
							}
							xml = s
							XmlParser parser = new XmlParser();
							node = parser.parseText(xml)
							List<String> names = new ArrayList<String>()
							node?.script_group?.scripts?.script_name?.each{
								names.add(it.text())
							}
							category =node?.script_group?.category?.text()?.trim()

							idList =  names
							idList = idList?.replace(SQUARE_BRACKET_OPEN,"")
							idList = idList?.replace(SQUARE_BRACKET_CLOSE,"")
						}catch(Exception e){
							scriptGroup?.addProperty("STATUS","FAILURE")
							scriptGroup.addProperty("Remarks","Invalid xml tags  ")
						}
						if(idList.equals("")){
							scriptGroup?.addProperty("STATUS","FAILURE")
							scriptGroup.addProperty("Remarks"," scripts  name list is empty  ")
						}else if(!category){
							scriptGroup?.addProperty("STATUS","FAILURE")
							scriptGroup.addProperty("Remarks"," Category not empty  ")
						}else if(category && !Utility.getCategory(category)){
							scriptGroup?.addProperty("STATUS","FAILURE")
							scriptGroup.addProperty("Remarks"," Invalid Category  ")

						}
						else{
							try{
								StringTokenizer st = new StringTokenizer(idList,",")
								while(st.hasMoreTokens()){
									String token = st.nextToken()
									if(token && token.size()>0){
										ScriptFile sctFile = ScriptFile.findByScriptName(token?.trim())
										if( sctFile != null  && !scriptGroupInstance?.scriptList?.contains(sctFile)){
											scriptGroupInstance.addToScriptList(sctFile)
											valid = true
										}
									}
								}
								if(valid){
									scriptGroupInstance.name = fileName
									scriptGroupInstance.category = Utility.getCategory(category)
									//scriptGroupInstance.groups = utilityService.getGroup()
									if(scriptGroupInstance.save(flush:true)){
										scriptGroup?.addProperty("STATUS","SUCCESS")
										scriptGroup.addProperty("Remarks","Script group created success fully ")
									}else{
										scriptGroup?.addProperty("STATUS","FAILURE")
										scriptGroup.addProperty("Remarks","Script Group not created  ")
									}
								}else {
									scriptGroup?.addProperty("STATUS","FAILURE")
									scriptGroup.addProperty("Remarks","Script name is not valid   ")
								}
							}catch(Exception e){
								println "ERRORS"+e.getMessage()
								scriptGroup?.addProperty("STATUS","FAILURE")
								scriptGroup.addProperty("Remarks","Invalid xml tags   ")
							}
						}
					}else{
						scriptGroup?.addProperty("STATUS","FAILURE")
						scriptGroup.addProperty("Remarks","File not Exists")
					}
				}
			}else{
				scriptGroup?.addProperty("STATUS","FAILURE")
				scriptGroup.addProperty("Remarks","file not in xml format ")
			}
		}else{
			scriptGroup?.addProperty("STATUS","FAILURE")
			scriptGroup.addProperty("Remarks","No file specified ")
		}
		render scriptGroup
	}
	
	/**
	 * Method to check if script file is present in filestore and delete from db if not present
	 * @param scriptId
	 * @param scriptName
	 * @return
	 */
	def verifyScriptFile(Long scriptId, String scriptName){
		ScriptFile scriptFile
		if(scriptId){
			scriptFile = ScriptFile?.findById(scriptId)
		}else {
			scriptFile = ScriptFile?.findByScriptName(scriptName)
		}
		try {
			def requestGetRealPath = request.getRealPath("/")
			if(scriptFile && getScriptFileObj(requestGetRealPath, scriptFile?.moduleName,scriptFile?.scriptName,scriptFile?.category,scriptFile?.id ) == null){
				def sgList = []
				def scriptGroups = ScriptGroup.where {
					scriptList { id == scriptFile?.id }
				}
				scriptGroups?.each{ scriptGrp ->
					sgList.add(scriptGrp?.id)
				}

				sgList?.each{ sId ->
					def sGroup = ScriptGroup.findById(sId)
					sGroup?.scriptList?.removeAll(scriptFile)
					sGroup?.save()
				}
				scriptFile?.delete()
			}
		} catch (Exception e) {
			println "Error in verifyScriptFile - "+e.getMessage() + " scriptName "+scriptFile?.scriptName+" , id -"+scriptFile?.id
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to check if a script file is present in filestore , otherwise return null
	 * @param realPath
	 * @param dirName
	 * @param fileName
	 * @param category
	 * @param scriptId
	 * @return
	 */
	def getScriptFileObj(realPath,dirName,fileName, def category,scriptId){
		dirName = dirName?.trim()
		fileName = fileName?.trim()
		Map script = [:]
		try {
			def moduleObj = Module.findByName(dirName)
			def scriptDirName = Constants.COMPONENT
			if(moduleObj){
				if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName = Constants.INTEGRATION
				}else if(moduleObj?.testGroup?.groupValue.equals(TestGroup.Certification.groupValue)){
					scriptDirName = Constants.CERTIFICATION
				}
			}
			if(category.toString().equals("RDKV_RDKSERVICE")){
				category = Category.RDKV
			}
			def path = getFileFromPath( realPath, scriptDirName, dirName,  fileName,  category, scriptId)
			File file = new File(path)
			
			if(file.exists()){
				return file;
			}
		} catch (Exception e) {
			script = null
			e.printStackTrace()
		}
		return null;
	}
	
	/**
	 * Method to get the path of a script according to the module , category etc
	 * @param realPath
	 * @param dirName
	 * @param moduleName
	 * @param fileName
	 * @param category
	 * @param scriptId
	 * @return
	 */
	def getFileFromPath(def realPath, def dirName, def moduleName, def fileName, def category, def scriptId){
		def path = new StringBuffer()
		path = path?.append(realPath).append(FILE_SEPARATOR).append(FILESTORE)
		boolean isAdvanced = checkIfAdvanced(scriptId)
		String testDirName = ""
		String extn = ".py"
		switch(category){
			case Category.RDKV:
				testDirName =  FileStorePath.RDKV.value()
				if(isAdvanced){
					testDirName =  FileStorePath.RDKVADVANCED.value()
				}
				break;
			case Category.RDKB:
				testDirName =  FileStorePath.RDKB.value()
				if(isAdvanced){
					testDirName =  FileStorePath.RDKBADVANCED.value()
				}
				break;
			case Category.RDKC:
				testDirName =  FileStorePath.RDKC.value()
				break;
			case Category.RDKB_TCL:
				testDirName = FileStorePath.RDKTCL.value()
				extn = ".tcl"
				break;
			default: break;
		}
		path = path?.append(FILE_SEPARATOR).append(testDirName).append(FILE_SEPARATOR).append(dirName).append(FILE_SEPARATOR).append(moduleName).append(FILE_SEPARATOR).append(fileName).append(extn)
		return path?.toString()
	}
	
	/**
	 * Method to check whether a script is part of advanced scripts.
	 */
	def checkIfAdvanced(scriptId){
		boolean isAdv = false
		try {
			String filePath = ScriptService.scriptsListAdvanced.get(scriptId)
			isAdv = (filePath?.equals(TESTSCRIPTS_RDKV_ADV) || filePath?.equals(TESTSCRIPTS_RDKB_ADV) )
		} catch (Exception e) {
			e.printStackTrace()
		}
		return isAdv
	}
	
	/**
	 * Method to delete duplicate entries of a script from database
	 * @param modules
	 * @return
	 */
	def deleteMultipleScriptFileEntries(String modules){
		List moduleList = []
		moduleList = modules?.split(",")
		moduleList.each{ moduleName ->
			List scriptFileList = ScriptFile?.findAllByModuleName(moduleName)
			def sList = []
			def deletedList = []
			Map scriptNameIdMap = [:]
			scriptFileList.each{ scriptFile ->
				try{
					if(!sList.contains(scriptFile?.scriptName)){
						sList.add(scriptFile?.scriptName)
						scriptNameIdMap.put(scriptFile?.scriptName, scriptFile?.id)
						try {
							def requestGetRealPath = request.getRealPath("/")
							if(scriptFile && getScriptFileObj(requestGetRealPath, scriptFile?.moduleName,scriptFile?.scriptName,scriptFile?.category,scriptFile?.id ) == null){
								def sgList = []
								def scriptGroups = ScriptGroup.where {
									scriptList { id == scriptFile?.id }
								}
								scriptGroups?.each{ scriptGrp ->
									sgList.add(scriptGrp?.id)
								}
								sgList?.each{ sId ->
									def sGroup = ScriptGroup.findById(sId)
									sGroup?.scriptList?.removeAll(scriptFile)
									sGroup?.save()
								}
								scriptFile?.delete()
								deletedList.add(scriptFile?.id)
							}
						} catch (Exception e) {
							println "Error  - "+e.getMessage() + " scriptName "+scriptFile?.scriptName+" , id -"+scriptFile?.id
							e.printStackTrace()
						}
					}else{
						def sgList = []
						def scriptGroups = ScriptGroup.where {
							scriptList { id == scriptFile?.id }
						}
						Long originalScriptId = scriptNameIdMap?.get(scriptFile?.scriptName)
						ScriptFile originalScriptFile
						if(!deletedList?.contains(originalScriptId)){
							originalScriptFile = ScriptFile?.findById(originalScriptId)
						}
						scriptGroups?.each{ scriptGrp ->
							sgList.add(scriptGrp?.id)
						}
						sgList?.each{ sId ->
							def sGroup = ScriptGroup.findById(sId)
							if(!deletedList?.contains(originalScriptId)){
								if(!sGroup?.scriptList?.id?.contains(originalScriptId)){
									def indexOfscriptFile = sGroup?.scriptList?.indexOf(scriptFile)
									sGroup?.scriptList?.set(indexOfscriptFile, originalScriptFile);
								}
							}
							sGroup?.scriptList?.removeAll(scriptFile)
							sGroup?.save()
						}
						scriptFile?.delete()
					}
				}catch (Exception e) {
					println "Error - "+e.getMessage() + " scriptName "+scriptFile?.scriptName+" , id -"+scriptFile?.id
					e.printStackTrace()
				}
			}
		}
		render "deleted duplicates"
	}
	
	/**
	 * Function used to the newly added script automatically add the script list without stop and start the "apache-tomcat" server.
	 * The refresh the script list, while calling the  initializeScriptsData() same as boot process.
	 */

	def scriptListRefresh(){
		def requestGetRealPath = request.getRealPath("/")
		def scriptGroupMap = scriptService.getScriptsMap(requestGetRealPath)
		def refreshStatus = scriptService.scriptListRefresh(realPath ,scriptGroupMap )
		scriptService.initializeThunderScripts(realPath)
		scriptService.initializeRdkServiceScripts(realPath)
		if(refreshStatus){
			flash.message =  "Script lists are same not modified "
		} else {
			flash.message = " Script list refreshment completed successfully "
		}
		redirect( action :"list")

	}
	/**
	 * Function used to implement download script group in .xml file format
	 * @return
	 */	
	def downloadXml(){
		def name = params?.name
		String scriptGroupData = getScriptGroupData(name)
		if(scriptGroupData){
			params.format = "text"
			params.extension = "xml"
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ params?.name+".xml\"")
			response.setHeader("Content-Length", ""+scriptGroupData.length())
			response.outputStream << scriptGroupData.getBytes()
		}else{
			flash.message = "Download failed. Script Group data is not available."
			redirect(action: "list")
		}
	}

	/**
	 * Method used to implement download all the script group xmls as zip format.
	 * @return
	 */
	def downloadXmlGroup(){
		def scriptGroupList = ScriptGroup.list()
		File file = new File("ScriptGroups.zip")
		ZipOutputStream zipFile = new ZipOutputStream(new FileOutputStream(file))
		try{
			scriptGroupList?.each {scriptGroup->
				String scriptGroupData = ""
				def writer = new StringWriter()
				def xml = new MarkupBuilder(writer)
				if(scriptGroup){
					scriptGroupData = getScriptGroupData(scriptGroup.name)
					try{
						xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
						xml.xml(){
							xml.script_group(){
								xml.category(scriptGroup?.category)// for RDKB
								xml.scripts(){
									scriptGroup?.scriptList.each{ scriptName ->
										xml.script_name(scriptName)
									}
			
								}
							}
						}
						scriptGroupData = writer.toString()
					}catch (Exception e){
						log.error "ERROR "+e.getMessage()
						e.printStackTrace()
					}

					zipFile.putNextEntry(new ZipEntry(scriptGroup.name + ".xml"))
					zipFile.write(scriptGroupData.bytes, 0, scriptGroupData.bytes.size())
					zipFile.closeEntry()

				}
			}
			zipFile.close()
		}catch(Exception e){
			println " ERROR "+ e.printStackTrace()
		}
		if(scriptGroupList){
			params.format = EXPORT_ZIP_FORMAT
			params.extension = EXPORT_ZIP_EXTENSION
			response.setHeader("Content-Type", "application/zip")
			response.setHeader("Content-Disposition", "attachment; filename=\"ScriptGroups.zip\"")
			response.outputStream << file.newInputStream()
	
		}else{
			flash.message = "Download failed due to script group information not available."
			redirect(action: "show")
		}
	}
	
	def getScriptGroupData(String name){
		def scriptGrpName  = ScriptGroup.findByName(name)
		String scriptGroupData = ""
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		try{
			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
			xml.xml(){
				xml.script_group(){
					xml.category(scriptGrpName?.category)// for RDKB
					xml.scripts(){
						scriptGrpName?.scriptList.each{ scriptName ->
							xml.script_name(scriptName)
						}

					}
				}
			}
			scriptGroupData = writer.toString()
		}catch (Exception e){
			log.error "ERROR "+e.getMessage()
			e.printStackTrace()
		}
		return scriptGroupData
	}

	/** This function used to uploading the new .xml fill in the test manager
	 * check the  .xml file or not
	 * check same script group is exists or not
	 * content of the file is same as the script group xml or not
	 * script list is empty or not
	 * return
	 */

	def upload() {
		def uploadedFile = request.getFile('file')
		String xmlContent = ""
		def node
		def category
		String s = ""
		String  idList
		int indx = 0
		if(uploadedFile){
			if( uploadedFile?.originalFilename?.endsWith(XML)) {

				String fileName = uploadedFile?.originalFilename?.replace(XML,"")

				if(ScriptGroup.findByName(fileName?.trim())){
					flash.message= "Test Suite with same name already exists ..... "
				}else{
					InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
					def fileContent = reader?.readLines()
					if(fileContent){

						fileContent?.each{ xmlData->
							xmlContent += xmlData +"\n"

						}
						List<String> names = new ArrayList<String>()
						try{

							XmlParser parser = new XmlParser();
							node = parser.parseText(xmlContent)

							node.script_group.scripts.script_name.each{
								names.add(it.text())
							}
							category =node?.script_group?.category?.text()?.trim()
						}
						catch(Exception e){
							log.error "ERROR"+e.getMessage()
							e.printStackTrace()
						}
						try{


							if(names?.size() == 0){
								flash.message ="  Test suite xml doesnot contain valid script  list... "
							}else{
								ScriptGroup scriptGroupInstance = new ScriptGroup()
								names?.each{ token ->
									if(token && token.size()>0){
										ScriptFile sctFile = ScriptFile.findByScriptName(token?.trim())
										if( sctFile != null  && !scriptGroupInstance?.scriptList?.contains(sctFile)){
											scriptGroupInstance.addToScriptList(sctFile)
										}
									}
								}
								scriptGroupInstance.name = fileName.trim()
								scriptGroupInstance.category = Utility.getCategory(category)
								scriptGroupInstance.groups = utilityService.getGroup()

								if (!scriptGroupInstance.save(flush: true)) {
									flash.message = "File not uploaded"
								}else{
									flash.message = "File uploaded  successfully "
								}
							}
						}catch(Exception e ){
							log.error "ERROR "+ e.getMessage()
							flash.message = "XML data is not in correct format"
						}
					}
				}
			} else{
				flash.message="Error, The file extension is not in .xml format"
			}
		}else{
			flash.message="Not a valid file"
		}
		redirect(action:"list")
		return
	}

	/**
	 * Function for saving the current script group script list while clicking the module wise/ random wise sort
	 */
	def scriptGroupListSave(){
		def scriptGroupInstance = ScriptGroup.get(params.id)
		boolean  value = false
		try{
			if(scriptGroupInstance){
				scriptGroupInstance.name = params.get("name")
				scriptGroupInstance.scriptList.clear();
				def idList = params?.idList
				idList = idList.replaceAll("sgscript-","")
				idList = idList.replaceAll("end","")
				StringTokenizer st = new StringTokenizer(idList,",")
				while(st.hasMoreTokens()){
					String token = st.nextToken()
					if(token && token.size()>0){
						ScriptFile sctFile = ScriptFile.findById(token)
						if(sctFile && !scriptGroupInstance?.scriptList?.contains(sctFile)){
							scriptGroupInstance.addToScriptList(sctFile)
						}
					}
				}
				if(!scriptGroupInstance?.save()){
					value = false
				}else{
					value = true
				}
			}
		}catch(Exception e){
			println " ERROR "+ e.getMessage()
			e.printStackTrace()
		}
		render value
	}

	/**
	 * The function used to download the consolidated script list according to module wise.
	 * It display the report like a work book  contains
	 * Summary page  - Include the  number of script count in each module and total number of scripts.
	 * Script list shows corresponding to the module in each page.
	 * @return
	 */
	def downloadScriptList() {
		try{
			def requestGetRealPath = request.getRealPath("/")
			def scriptMap = scriptService.getScriptsMap(requestGetRealPath)
			def tclScriptMap = scriptService?.getTCLNameList(requestGetRealPath)
			def detailDataMap = [:]
			Map coverPageMap = [:]
			Map detailsMap = [:]
			List scriptNameList = []
			Map moduleNameMap = [:]
			def moduleInstance
			//For summary page
			scriptMap.each{ moduleName, scripts ->
				//moduleInstance = Module?.findByName(moduleName)
				//detailsMap.put(moduleName, scripts.size())
				detailsMap.put(moduleName, scripts.size())
			}

			detailsMap.put("TCL_SCRIPT",tclScriptMap?.size() )
			coverPageMap.put("Details", detailsMap)
			detailDataMap.put("coverPage", coverPageMap)
			// For script list display according to the module wise
			scriptMap.each{moduleName,scriptList ->
				scriptNameList = []
				scriptList.each{ scriptName ->
					scriptNameList.add(scriptName)
				}
				detailDataMap.put(moduleName, scriptNameList)
			}
			detailDataMap.put("TCL_SCRIPT",tclScriptMap)
			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = "Consolidated_Script_Details"
			response.setHeader("Content-disposition", "attachment; filename="+fileName +".${params.extension}")
			excelExportService.exportScript(params.format,response.outputStream,detailDataMap)
			log.info "Completed excel export............. "
		}catch(Exception e ){
			println "ERROR"+ e.getMessage()
		}
	}


	/**
	 * Function upload the new script using UI .
	 *
	 */
	def  uploadScript(){
		try{
			def uploadedFile = request.getFile('file')
			if( uploadedFile?.originalFilename?.endsWith(".py")) {
				InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
				def fileContent = reader?.readLines()
				if(fileContent){
					boolean saveScript = false
					boolean testCaseTagValue = false
					String xmlContent = ""
					def node
					int startIndex=0
					int indx = fileContent?.findIndexOf { it.startsWith("'''")}
					String headerContent = ""
					// Parsing Header content
					while(startIndex < indx ){
						headerContent = headerContent+fileContent.get(startIndex)+"\n"
						startIndex++
					}
					int lastIndx = fileContent?.findLastIndexOf { it?.toString()?.equals("'''")}
					// Parsing XML content
					while(indx <= lastIndx ){
						if(!(fileContent.get(indx)?.equals(""))){
							xmlContent = xmlContent + fileContent.get(indx)+"\n"
						}
						indx++
					}
					lastIndx += 1
					String pythonContent = " "
					// Parsing  Python content
					while (lastIndx < fileContent?.size()){
						pythonContent = pythonContent+ fileContent.get(lastIndx)+"\n"
						lastIndx++
					}
					try{
						def scriptXmlText = xmlContent?.replaceAll("'''", "")
						XmlParser parser = new XmlParser();
						node = parser.parseText(scriptXmlText?.trim())
					}catch(Exception e){
						flash.message ="XML data is not in correct format "
					}

					def scriptName  = node?.name?.text()?.trim()
					def primitiveTestName  = node?.primitive_test_name?.text()?.trim()
					def synopsis = node?.synopsis?.text()?.trim()
					def executionTime= node?.execution_time?.text()?.trim()
					def remarks = node?.remarks?.text()?.trim()
					def longDuration = node?.long_duration?.text()?.trim()
					def skip = node?.skip?.text()?.trim()
					def advanced  = node?.advanced_script?.text()?.trim()
					Set boxTypeList = []
					Set rdkVersions = []
					Set scrptTags = []
					Set testProfile = []

					node?.box_types?.box_type?.each{
						def boxType = BoxType?.findByName(it?.text().trim())
						if(boxType){
							boxTypeList?.add(boxType)
						}
					}
					node?.rdk_versions?.rdk_version?.each{
						def rdkVers = RDKVersions.findByBuildVersion(it?.text()?.trim())
						if(rdkVers){
							rdkVersions?.add(rdkVers)
						}
					}
					node?.script_tags?.script_tag?.each{
						def sTag = ScriptTag.findByName(it?.text()?.trim())
						if(sTag){
							scrptTags?.add(sTag)
						}
					}
					node?.test_profiles?.test_profile?.each{
						def tProfile = TestProfile?.findByName(it?.text()?.trim())
						if(tProfile){
							testProfile?.add(tProfile)
						}
					}
					if(node?.test_cases){
						if(node?.test_cases?.test_case_id &&
						node?.test_cases?.test_objective &&
						(node?.test_cases?.test_type?.text()?.toString()?.equals(POSITIVE) || node?.test_cases?.test_type?.text()?.toString()?.equals(NEGATIVE))  &&
						node?.test_cases?.test_setup &&
						node?.test_cases?.skipped &&
						node?.test_cases?.pre_requisite    &&
						node?.test_cases?.api_or_interface_used &&
						node?.test_cases?.input_parameters &&
						node?.test_cases?.automation_approch &&
						node?.test_cases?.except_output &&
						(node?.test_cases?.priority?.text().toString()?.equals(HIGH) || node?.test_cases?.priority?.text().toString()?.equals(LOW) ||  node?.test_cases?.priority?.text().toString()?.equals(MEDIUM))
						&& node?.test_cases?.test_stub_interface && node?.test_cases?.test_script &&
						node?.test_cases?.release_version &&
						node?.test_cases?.remarks &&
						(node?.test_cases?.skipped?.text().toString()?.equals(NO) || node?.test_cases?.skipped?.text().toString()?.equals(YES)) ){
							testCaseTagValue = false
						}
						else if(node?.test_cases?.test_case_id &&
							node?.test_cases?.test_objective &&
							(node?.test_cases?.test_type?.text()?.toString()?.equals(POSITIVE) || node?.test_cases?.test_type?.text()?.toString()?.equals(NEGATIVE))  &&
							node?.test_cases?.test_setup &&
							node?.test_cases?.skipped &&
							node?.test_cases?.pre_requisite    &&
							node?.test_cases?.api_or_interface_used &&
							node?.test_cases?.input_parameters &&
							node?.test_cases?.automation_approch &&
							node?.test_cases?.expected_output &&
							(node?.test_cases?.priority?.text().toString()?.equals(HIGH) || node?.test_cases?.priority?.text().toString()?.equals(LOW) ||  node?.test_cases?.priority?.text().toString()?.equals(MEDIUM))
							&& node?.test_cases?.test_stub_interface && node?.test_cases?.test_script &&
							node?.test_cases?.release_version &&
							node?.test_cases?.remarks &&
							(node?.test_cases?.skipped?.text().toString()?.equals(NO) || node?.test_cases?.skipped?.text().toString()?.equals(YES)) ){
								testCaseTagValue = false
							}
						else{
							testCaseTagValue = true
						}
					}else{
						testCaseTagValue = false
					}
					def scriptList
					String category= ""
					def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
					def moduleName = moduleMap.get(primitiveTestName)
					def moduleInstance =  Module?.findByName(moduleName)
					if(moduleInstance){
						if(params?.category?.toString()?.equals(RDKV)){
							category = RDKV
							scriptList = scriptService.getScriptNameList(getRealPath(), category)
						}else{
							category =RDKB

							scriptList = scriptService.getScriptNameList(getRealPath(), category)
						}
					}
					def scriptsDirName = primitiveService.getScriptDirName(moduleName)
					def ptest = primitiveService.getPrimitiveTest(getRealPath()+"//fileStore//testscripts"+category+"//"+scriptsDirName+"//"+moduleName+"//"+moduleName+XML, primitiveTestName)
					if(!ptest){
						ptest = primitiveService.getPrimitiveTest(getRealPath()+"//fileStore//testscripts"+category+"Advanced"+"//"+scriptsDirName+"//"+moduleName+"//"+moduleName+XML, primitiveTestName)
					}
					if(!scriptName){
						flash.message =" Script name should not be empty "
					}else if(!primitiveTestName){
						flash.message =" Primitive test name should not be empty "
					}else if(!executionTime){
						flash.message =" Execution time  should not be empty "
					}else if(!pythonContent ){
						flash.message= " Python script content should not be empty"
					}else if(!longDuration){
						flash.message= " Long Duaration content should not be empty"
					}else if(!skip){
						flash.message= " Skip content should not be empty"
					}else if(scriptList?.toString()?.contains(scriptName?.trim()?.toString())){
						flash.message =  "Duplicate Script Name not allowed. Try Again."
					}else if (!ptest?.name){
						flash.message =" Primitive test name should be valid "
					} else if(!(longDuration?.toString()?.equals(TRUE) || longDuration?.toString()?.equals(FALSE)) ){
						flash.message =" Long Duration  should be valid "
					}else if(!(skip?.toString()?.equals(TRUE) || skip?.toString()?.equals(FALSE))){
						flash.message =" Skip content  should be valid "
					}else if(!(boxTypeList?.size() >= 0) ){
						flash.message =" Box Types should be valid "
					}else if(!(rdkVersions?.size() >= 0)){
						flash.message =" RDK versions should be valid "
					}else if(!(scrptTags?.size() >= 0)){
						flash.message =" Script tags should be valid "
					}else if(!(testProfile?.size() >= 0)){
						flash.message = "Test profile tags should be valid "
					}else if(testCaseTagValue){
						flash.message =" Test case tags or values should be valid"
					}else{
						try{
							String dirname = ptest?.module?.name
							dirname = dirname?.trim()

							def pathToDir =  "${request.getRealPath('/')}//fileStore"
							if(RDKV.equals(category)){
								if(advanced.equals("true")){
									pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKV_ADV
								}
								else{
									pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKV
								}
							}
							else if(RDKB.equals(category)){
								if(advanced.equals("true")){
									pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKB_ADV
								}
								else{
									pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKB
								}
							}
							File dir = new File( pathToDir + Constants.FILE_SEPARATOR + scriptsDirName +  Constants.FILE_SEPARATOR +dirname)
							if(!dir.exists()){
								dir.mkdirs()
							}
							File file = new File( pathToDir + Constants.FILE_SEPARATOR + scriptsDirName + Constants.FILE_SEPARATOR+dirname+Constants.FILE_SEPARATOR+scriptName?.trim()+".py");
							if(!file.exists()){
								file.createNewFile()
							}
							String data = headerContent+xmlContent.toString() +pythonContent
							file.write(data)
							def script = ScriptFile.findByScriptNameAndModuleName(scriptName?.trim(),ptest?.module?.name)
							if(script == null){
								script = new ScriptFile()
								script.setScriptName(scriptName?.trim())
								script.setModuleName(ptest?.module?.name)
								if(ptest?.module?.name == Constants.RDKSERVICES || (ptest?.module?.testGroup == TestGroup.Certification)){
									script.category = Utility.getCategory(Category?.RDKV_RDKSERVICE.toString())
								}else{
									script.category = Utility.getCategory(category)
								}
								script.save(flush:true)
							}
							if((ptest?.module?.name != Constants.RDKSERVICES) && (ptest?.module?.testGroup != TestGroup.Certification)){
								def scr = ScriptFile.findByScriptNameAndModuleName(scriptName?.trim(),ptest?.module?.name)
								if(RDKV.equals(category)){
									if(advanced.equals("true")){
										ScriptService.scriptsListAdvanced.put(scr?.id, TESTSCRIPTS_RDKV_ADV)
									}
									else{
										ScriptService.scriptsListAdvanced.put(scr?.id, TESTSCRIPTS_RDKV)
									}
								}
								else if(RDKB.equals(category)){
									if(advanced.equals("true")){
										ScriptService.scriptsListAdvanced.put(scr?.id, TESTSCRIPTS_RDKB_ADV)
									}
									else{
										ScriptService.scriptsListAdvanced.put(scr?.id, TESTSCRIPTS_RDKB)
									}
								}
								boolean longDurationTest= false
								if(longDuration.equals("true")){
									longDurationTest = true
								}else{
									longDurationTest = false
								}
								def sObject = new ScriptObject()
								sObject.setBoxTypes(boxTypeList)
								sObject.setRdkVersions(rdkVersions)
								sObject.setScriptTags(scrptTags)
								sObject.setTestProfile(testProfile)
								sObject.setName(scriptName?.trim())
								sObject.setModule(ptest?.module?.name)
								sObject.setScriptFile(script)
								sObject.setLongDuration(longDurationTest)
								scriptService.updateScript(script , category)
								scriptgroupService.saveToScriptGroups(script,sObject, category)
								scriptgroupService.saveToDefaultGroups(script,sObject, boxTypeList,category)
								scriptgroupService.updateScriptsFromScriptTag(script,sObject,[],[],category)
								scriptService.createDefaultGroupWithoutOS(sObject,script, params?.category)
								scriptService?.updateScriptsFromTestProfile(script,sObject,category)
							}else{
								scriptService.updateScript(script,Category?.RDKV_RDKSERVICE.toString())
								scriptService.updateRdkServiceScriptSuite(ptest?.module?.name,script,Category?.RDKV_RDKSERVICE.toString())
							}
							flash.message =" Script uploaded successfully"
						}catch(Exception e){
							flash.message =" Script not uploaded, please try again "
						}
					}
				}else{
					flash.message ="File content is empty"
				}
			}else {
				flash.message="Error, The file extension is not in .py format"
			}
		}catch(Exception e){
			println " Error "+ e.getMessage()
			e.printStackTrace()
		}
		redirect(action:"list")
		return
	}
	/**
	 * Function for suite clean up with not available scripts
	 * @return
	 */

	def verifyScriptGroup(){
		boolean value = true
		try{
			long time1 = System.currentTimeMillis();
			ScriptGroup sg = ScriptGroup?.findByName(params?.name)
			def rPath = getRealPath()
			List removeList = []
			if(sg?.category?.toString()?.equals(RDKB) || sg?.category?.toString()?.equals(RDKV) || sg?.category?.toString()?.equals(RDKC)){
				sg?.scriptList.each { script ->
					Map scriptInstance1 = scriptService.getScript(rPath,script?.moduleName, script?.scriptName, params?.category)
					if(scriptInstance1 == null || scriptInstance1?.keySet()?.size() ==  0){
						removeList.add(script)
					}
				}
			}else if(sg?.category?.toString()?.equals(RDKB_TCL)){
				sg?.scriptList?.each{ tclScript ->
					def content = scriptService?.getTclScript(rPath,tclScript?.toString())
					if(!content){
						removeList.add(tclScript)
					}
				}
			}
			if(removeList?.size() > 0){
				def sGroup = ScriptGroup.findByName(params?.name)
				sGroup.scriptList.removeAll(removeList)
				sGroup.save(flush:true)
				value = true
			}
		}catch(Exception e){
			println " ERRROR "+ e.getMessage()
			value = false
		}
		render  new Gson().toJson(value)
	}
	
	/**
	 * Method to clean the test suites and scripts from database
	 * @return
	 */
	def verifyAllScriptGroups(){
		long time1 = System.currentTimeMillis();
		def sgList = ScriptGroup.findAll()
		def map = [:]
		def removeList = []
		try{
			def scriptListRDKV = scriptService.getScriptNameList(request.getRealPath("/"),RDKV)
			scriptListRDKV = scriptListRDKV?scriptListRDKV:[]
			def scriptListRDKB=  scriptService.getScriptNameList(request.getRealPath("/"),RDKB)
			scriptListRDKB = scriptListRDKB?scriptListRDKB:[]
			def scriptListRDKC=  scriptService.getScriptNameList(request.getRealPath("/"),RDKC)
			scriptListRDKC = scriptListRDKC?scriptListRDKC:[]
			def tclScriptList = scriptService.getTCLNameList(request.getRealPath("/"))
			def scriptgroupscriptfilesize = 0
			def sgNames = []
			sgList?.each { scriptGroup ->
				def rPath = getRealPath()
				scriptGroup?.scriptList?.each{ script->
					if(scriptGroup?.category?.toString().equals(RDKV)){
						if(!(scriptListRDKV?.toString()?.contains(script?.toString()))){
							removeList.add(script)
						}
					}else if(scriptGroup?.category?.toString().equals(RDKV_RDKSERVICE)){
						if(!(scriptListRDKV?.toString()?.contains(script?.toString()))){
							removeList.add(script)
						}
					}else if(scriptGroup?.category?.toString().equals(RDKB)){
						if(!(scriptListRDKB?.toString()?.contains(script?.toString()))){
							removeList.add(script)

						}
					}else if(scriptGroup?.category?.toString().equals(RDKC)){
						if(!(scriptListRDKC?.toString()?.contains(script?.toString()))){
							removeList.add(script)

						}
					}else if(scriptGroup?.category?.toString().equals(RDKB_TCL)){
						if(!(tclScriptList?.toString()?.contains(script?.toString())) && !scriptService?.totalTclScriptList?.contains(script)){
							removeList.add(script)
						}
					}
				}
				def sGroup = ScriptGroup.findByName(scriptGroup?.name)
				def scriptList = sGroup?.scriptList
				def scriptListAfterRemoval = []
				scriptList.each { script ->
					if(!scriptListAfterRemoval?.contains(script) && !removeList?.contains(script)){
						scriptListAfterRemoval?.add(script)
					}
				}
				sGroup.scriptList =  scriptListAfterRemoval
				sGroup.category = Utility.getCategory(scriptGroup?.category?.toString())
				if(!sGroup.save(flush:true)){
					sGroup?.errors.allErrors.each{error->
						println"Error saving test suite  - "+error
					}
				}
				map.put(scriptGroup?.name, removeList)
				removeList = []
				if(scriptGroup?.scriptList?.size() == 0){
					sgNames.add(scriptGroup?.name)
				}
			}	
			sgNames?.each{ sg ->
				def sGroup = ScriptGroup.findByName(sg)
				if(sGroup?.scriptList?.size() == 0){
					sGroup.delete(flush: true)
				}
			}
		}
		catch(Exception e){
			println e.printStackTrace()
			println " ERROR in verifyAllScriptGroups for scriptGroups - "+e.getMessage()
		}
		try{
			def scriptFiles = ScriptFile.findAll();
			def sList = []
			scriptFiles.each { sFile ->
				if(sFile.category != Category.RDKV_THUNDER){
					if(!sList.contains(sFile?.scriptName)){
						sList.add(sFile?.scriptName)
						verifyScriptFile(sFile?.id, sFile?.scriptName)
					}
				}
			}
		}catch(Exception e){
			println e.printStackTrace()
			println " ERROR in verifyAllScriptGroups for scripts >>>"+e.getMessage()
		}
		println "End of verifyAllScriptGroups" + (System.currentTimeMillis() - time1 )
		redirect( action :"list")
	}

	/**
	 * Method to delete all empty test suites
	 * @return
	 */
	def deleteAllEmptyScriptGroups(){
		def deletedList = []
		try {
			def sgList = ScriptGroup.findAll()
			sgList?.each{ sg ->
				if(sg?.scriptList?.size() == 0){
					deletedList.add(sg?.name)
				}
			}
			deletedList?.each{ sg ->
				def sGroup = ScriptGroup.findByName(sg)
				if(sGroup?.scriptList?.size() == 0){
					sGroup.delete(flush: true)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		render deletedList as String
	}
	/**
	 * function for saving the tcl script
	 */
	def saveTclScript(){
		def filePath = getRealPath() + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		String content =  params.scriptArea
		def scriptName = params.name
		def saveScript = ""
		def requestGetRealPath = request.getRealPath("/")
		def  tclScriptList= scriptService?.getTCLNameList(requestGetRealPath)
		if(tclScriptList?.toString()?.contains(scriptName?.trim()?.toString()) &&  scriptName && content){
			flash.message = "Duplicate Script Name not allowed. Try Again"
		}
		else if (scriptName && !content?.trim()?.isEmpty() ){
			File dir = new File( filePath)
			if(!dir.exists()){
				dir.mkdirs()
			}
			File file = new File( filePath+Constants.FILE_SEPARATOR+scriptName?.trim()+".tcl");
			if(!file.exists()){
				file.createNewFile()
			}
			if(file.exists()){
				file.write(content)
				saveScript = TRUE
			}
			def sName = params?.name
			if(saveScript?.equals(TRUE)){
				def script = ScriptFile.findByScriptNameAndModuleName(params?.name?.trim(),'tcl')
				if(script == null){
					script = new ScriptFile()
					script.setScriptName(params?.name?.trim())
					script.setModuleName("tcl")
					script.category = Utility.getCategory(params?.category)
					script?.save(flush:true)
				}
				scriptService.updateScript(script, params?.category)
				updateTclScriptGroup(script, params?.category)
				flash.message = message(code: 'default.created.message', args: [
					message(code: 'script.label', default: 'Script'),
					scriptName])
			}else {
				flash.message = message(code: 'default.not.created.message', args: [
					message(code: 'script.label', default: 'Script'),
					scriptName])
			}
		}else if (!scriptName && content){
			flash.message = "Please enter the script name"
		}else if (content?.trim()?.isEmpty()){
			flash.message = "Script content  empty"
		}
		redirect(action: "list")
	}


	/**
	 * Function for deleting TCL script to UI
	 * @return
	 */
	def deleteTCLScript(){
		boolean isTcl = false
		File file = null
		if(params?.category?.toString()?.equals(RDKB_TCL)){
			isTcl = true
		}
		def dirName = 'tcl'
		def fileName = params.id
		def scriptObj = ScriptFile?.findByScriptNameAndCategory(fileName,Category?.RDKB_TCL)
		if(!scriptObj){
			flash.message = "Script not found"
			render("Not found")
		}else{
			boolean scriptInUse = false
			if(isTcl){
				file = new File(getTestScriptPath(scriptObj?.category.toString())+FILE_SEPARATOR +fileName+".tcl")
				scriptInUse = false
				scriptService.deleteScript(scriptObj, scriptObj?.category?.toString())
				deleteTclScriptFromScriptGroup(scriptObj, params?.category)

			}
			if(scriptInUse){
				flash.message = "Can't Delete. Scripts may be used in Script Group"
				render("Exception")
			}
		}
		if(file != null && file.exists()){
			try {
				def fileDelete = file?.delete()
				if(fileDelete){
					flash.message = "Deleted the script '${fileName}'"
					render("success")
				}else{
					flash.message = "Failed to delete the script '${fileName}'"
					render("failure")
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}else{
			flash.message = "Failed to delete the script '${fileName}'"
			render("failure")
		}
	}

	/**
	 * Update TCL script from script group 
	 */
	def updateTclScriptGroup( final def script  , final def category){
		if(category?.toString()?.equals(RDKB_TCL)){
			try{
				def moduleName = "TCL_SCRIPTS"
				def scriptGrpInstance = ScriptGroup.findByName(moduleName)
				if(scriptGrpInstance == null){
					scriptGrpInstance = new ScriptGroup()
					scriptGrpInstance.name = moduleName
					scriptGrpInstance.scriptList = []
					scriptGrpInstance.category = Utility.getCategory(category)
					scriptGrpInstance?.save()
				}
				if(!scriptGrpInstance?.scriptList?.toString().contains(script?.toString())){
					scriptGrpInstance?.addToScriptList(script)
				}
			}
			catch(Exception e){
				println " ERROR "+e.getMessage()
			}
		}
	}
	/**
	 * delete script from tcl Script group 
	 */
	def deleteTclScriptFromScriptGroup(final def script, final def category){
		if(category?.toString()?.equals(RDKB_TCL)){
			try{
				def suiteName = "TCL_SCRIPTS"
				def scriptGrpInstance = ScriptGroup?.findByNameAndCategory(suiteName,category)
				if(scriptGrpInstance){
					scriptGrpInstance?.scriptList?.each { scriptInstance ->
						if(scriptInstance?.toString()?.equals(script?.toString())){
							//scriptGrpInstance?.removeFromScriptList(scriptInstance)
							scriptGrpInstance.scriptList?.remove(scriptInstance)
						}
					}
				}
			}catch(Exception e){
				e.printStackTrace()
			}
		}
	}
	/**
	 * REST API : for retrives execution time out for given script
	 *    - The following sceanrios validating
	 *    1) script name available or not 
	 *    2)  valid script name or not 
	 *    3) If valid script name returns jsons output like 
	 *     {"ScriptName":"Recorder_RMF_Rec_NotOrphaned_StartedLate_Legacy_2071","ExecutionTimeOut":100}    
	 * @param scriptName
	 * @return
	 */
	def getScriptTimeout(String scriptName){
		JsonObject jsonOutData = new JsonObject()
		try{
			if(scriptName){
				def scriptListRDKV = scriptService.getScriptNameList(request.getRealPath("/"), RDKV)
				def scriptListRDKB = scriptService.getScriptNameList(request.getRealPath("/"), RDKB)
				def scriptNameListTCL = scriptService.getTCLNameList(request.getRealPath("/"))
				def category
				def moduleDirName
				if(scriptListRDKV?.toString()?.contains(scriptName)){
					category = RDKV
				}else if(scriptListRDKB?.toString()?.contains(scriptName)){
					category = RDKB
				}else if(scriptNameListTCL?.toString()?.contains(scriptName)){
					category = RDKB_TCL
				}
				if(category?.toString()?.equals(RDKV) || category?.toString()?.equals(RDKB)){
					def scriptsMaps = scriptService?.getScriptsMap(request.getRealPath("/"),category)
					scriptsMaps?.each{
						if(it?.value?.toString()?.contains(scriptName)){
							moduleDirName = it.key
						}
					}
					if(moduleDirName){
						def script =  scriptService?.getScript(request.getRealPath("/"),moduleDirName ,scriptName , category)
						if(script){
							jsonOutData.addProperty("ScriptName", script.name)
							jsonOutData.addProperty("ExecutionTimeOut",script.executionTime)
						}else{
							jsonOutData.addProperty("Status", "FAILED")
							jsonOutData.addProperty("Remarks", "No script found with name  "+ scriptName)
						}
					}
				}else if(category?.toString()?.equals(RDKB_TCL)){
					def tclScript = scriptService?.getTclScript(request.getRealPath("/"), scriptName)
					if(tclScript){
						jsonOutData.addProperty("Status", "FAILED")
						jsonOutData.addProperty("Remarks", "No  execution time out available in TCL scripts")
					}else{
						jsonOutData.addProperty("Status", "FAILED")
						jsonOutData.addProperty("Remarks", "No script found with name  "+ scriptName)
					}
				}else{
					jsonOutData.addProperty("Status", "FAILED")
					jsonOutData.addProperty("Remarks", "No script found with name  "+ scriptName)
				}
			}else{
				jsonOutData.addProperty("Status", "FAILED")
				jsonOutData.addProperty("Remarks", "No Script Name available" )


			}
		}catch(Exception e){
			println "ERROR "+e.getMessage()
			e.printStackTrace()
		}
		render jsonOutData
	}
	/**
	 * Function for save the new test case document
	 *
	 */
	def editTestCaseDoc(){
		def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def moduleName = moduleMap.get(params?.primitiveTestName)
		def scriptsDirName = primitiveService.getScriptDirName(moduleName)
		def ptest = primitiveService.getPrimitiveTest(getRealPath()+"//fileStore//testscripts//"+scriptsDirName+"//"+moduleName+"//"+moduleName+XML, params?.primitiveTestName)
		def scrpt = scriptService.getScript(getRealPath(),moduleName, params?.name,params?.category)
		def testCaseDetails = scrpt?.testCaseDetails
		render(template: "editTestCase", model: [moduleName:moduleName , primitiveTest:ptest?.name , category:params?.category, script:scrpt,testCaseDetails:testCaseDetails ])
	}

	/**
	 * For updating the test case document
	 * @return
	 */

	def updateTestcaseDetails(){
		boolean value = true
		try{
			def scriptsDirName = primitiveService.getScriptDirName(params?.moduleName)
			def ptest = primitiveService.getPrimitiveTest(getRealPath()+"//fileStore//testscripts//"+scriptsDirName+"//"+params?.moduleName+"//"+params?.moduleName+".xml", params?.primitiveTest)
			def scrpt = scriptService.getScript(getRealPath(),params?.moduleName, params?.script,params?.category)
			String dirname = ptest?.module?.name
			dirname = dirname?.trim()
			def pathToDir =  "${request.getRealPath('/')}//fileStore"
			
			boolean isAdvanced = Utility.isAdvancedScript(params?.script, params?.moduleName)
			if(RDKV.equals(params?.category)){
				if(isAdvanced){
					pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKV_ADV
				}else{
					pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKV
				}
			}
			else if(RDKB.equals(params?.category)){
				if(isAdvanced){
					pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKB_ADV
				}else{
					pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKB
				}
			}
			else if(RDKC.equals(params?.category)){
				pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKC
			}
			
			File file = new File( pathToDir + Constants.FILE_SEPARATOR + scriptsDirName + Constants.FILE_SEPARATOR+dirname+Constants.FILE_SEPARATOR+params?.script+".py");

			if(file?.exists()){
				String s = ""
				List line = file.readLines()
				int indx = line?.findIndexOf {  it.startsWith("'''")}
				String scriptContent = ""
				if(line.get(indx).startsWith("'''"))	{
					indx++
					while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
						s = s + line.get(indx)+"\n"
						indx++
					}
					indx ++
					while(indx < line.size()){
						scriptContent = scriptContent + line.get(indx)+"\n"
						indx++
					}
				}
				def parser = new XmlParser(); //[XML Slurper not validate the node is correct or not]
				def root = parser.parseText(s)

				if(root?.test_cases){
					root?.test_cases?.test_case_id[0].value = params.tcId?.toString()
					root?.test_cases?.test_objective[0].value =  params.tcObjective?.toString()
					root?.test_cases?.test_type[0].value = params.tcType?.toString()
					root?.test_cases?.test_setup[0].value = params.tcSetup
					root?.test_cases?.pre_requisite[0].value = params.preRequisits
					root?.test_cases?.api_or_interface_used[0].value = params.tcApi
					root?.test_cases?.input_parameters[0].value = params.tcInputParams
					root?.test_cases?.automation_approch[0].value =  params.tcApproch
					if(root?.test_cases?.except_output){
						root?.test_cases?.except_output[0].value = params.tcExpectedOutput
					}
					else{
						root?.test_cases?.expected_output[0].value = params.tcExpectedOutput
					}
					root?.test_cases?.priority[0].value = params?.priority
					root?.test_cases?.test_stub_interface[0].value =  params?.testStub
					root?.test_cases?.test_script[0].value =  params?.testScript
					root?.test_cases?.release_version[0].value =  params?.releaseVersion
					root?.test_cases?.skipped[0].value = params?.tcSkip
					root?.test_cases?.remarks[0].value =  params?.remarks
				}else{
					def writer = new StringWriter()
					def xml = new MarkupBuilder(writer)
					xml.test_cases(){
						xml.test_case_id(params.tcId)
						xml.test_objective(params.tcObjective)
						xml.test_type(params.tcType)
						xml.test_setup(params.tcSetup)
						xml.pre_requisite(params.preRequisits)
						xml.api_or_interface_used(params.tcApi)
						xml.input_parameters(params.tcInputParams)
						xml.automation_approch(params.tcApproch)
						xml.expected_output(params.tcExpectedOutput)
						xml.priority(params.priority)
						xml.test_stub_interface(params.testStub)
						xml.test_script(params.testScript)
						xml.skipped(params.tcSkip)
						xml.release_version(params?.releaseVersion)
						xml.remarks(params?.remarks)
					}
					def testCaseNode = new XmlParser().parseText(writer.toString())
					root?.children()?.add(15,testCaseNode ) // Test case append at 15 position of xml header
				}
				String outxml = XmlUtil.serialize( root)
				File pyHeader = new File( "${request.getRealPath('/')}//fileStore//pyHeader.txt")
				def pyHeaderContentList = pyHeader?.readLines()
				String pyHeaderContent = ""
				pyHeaderContentList.each {
					pyHeaderContent += it?.toString()+"\n"
				}
				String data =pyHeaderContent+"'''"+"\n"+outxml.toString() +"\n"+"'''"+"\n"+scrpt?.scriptContent
				file.write(data)
			}
		}catch(Exception e){
			println "Error"+e.printStackTrace()
			value = false
		}
		render  new Gson().toJson(value)
	}
	/**
	 * Function for adding new test case doc in the script XML part
	 */
	def addTestCaseDoc(){
		render(template: "createTestCase", model: [category:params?.category, uniqueId:params?.uniqueId,name:params?.name])
	}

	/**
	 * Function for used adding new testcase in new script
	 */
	def addTestCaseInScript(){
		boolean value = true
		try{
			def	testCaseDeatilsMap = [:]
			testCaseDeatilsMap?.put(T_C_ID,params.tcId)
			testCaseDeatilsMap?.put(T_C_OBJ,params.tcObjective)
			testCaseDeatilsMap?.put(T_C_TYPE,params.tcType)
			testCaseDeatilsMap?.put(T_C_SETUP,params.tcSetup)
			//testCaseDeatilsMap?.put(T_C_STREAM_ID,params.tcStreamId)
			testCaseDeatilsMap?.put(T_C_SKIP,params.tcSkip)
			testCaseDeatilsMap?.put(T_C_PRE_REQUISITES, params.preRequisits)
			testCaseDeatilsMap?.put(T_C_INTERFACE,params.tcApi)
			testCaseDeatilsMap?.put(T_C_IOPARAMS,params.tcInputParams )
			testCaseDeatilsMap?.put(T_C_EX_OUTPUT,params.tcExpectedOutput)
			testCaseDeatilsMap?.put(T_C_PRIORITY,params.priority)
			testCaseDeatilsMap?.put(T_C_TSI, params.testStub)
			testCaseDeatilsMap?.put(T_C_SCRIPT,params.testScript)
			testCaseDeatilsMap?.put(T_C_RELEASE_VERSION,params.releaseVersion)
			testCaseDeatilsMap?.put(T_C_AUTOAPROCH,params.tcApproch)
			testCaseDeatilsMap?.put(T_C_REMARKS,params.remarks)

			scriptService?.addNewTestCaseDetails(testCaseDeatilsMap,params?.uniqueId)
			value = true
		}catch(Exception e){
			value = false
			println "ERROR"+e.getMessage()
		}
		render  new Gson().toJson(value)
	}
	
	/**
	 * Function for downloading test case in excel file
	 */
	def downloadTestCaseInExcel(){
		def testCaseDetails = testCaseService?.downloadTestCaseInExcel(params, getRealPath())
		try{
			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = TESTCASE+params?.name
			response.setHeader("Content-disposition", "attachment; filename="+fileName +".${params.extension}")
			excelExportService?.exportTestCase(params?.name, response.outputStream,testCaseDetails)
		}catch(Exception e){
			println "ERROR "+e.printStackTrace()
		}
	}

	/**
	 * Function for downloading the test case in script group in excel file
	 */
	def downloadScriptGroupTestCase(){
		def scriptGrpInstance = ScriptGroup?.findByName(params?.scriptGrpName)
		try{
			def totalTestCaseMap = testCaseService?.downloadScriptGroupTestCase(params,getRealPath())
			if(totalTestCaseMap != [:]){
				params.format = EXPORT_EXCEL_FORMAT
				params.extension = EXPORT_EXCEL_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				def fileName = scriptGrpInstance?.toString()
				response.setHeader("Content-disposition", "attachment; filename="+fileName +".${params.extension}")
				excelExportService?.exportTestSuiteTestCase(scriptGrpInstance?.toString(),response.outputStream,totalTestCaseMap,testCaseService?.testCaseKeyMap())
			}else{
				flash.message = "No test cases available in ${scriptGrpInstance?.name}  "
				redirect(action:"list")
			}
		}catch(Exception e){
			println "ERROR"+e.getMessage()
			flash.message = "No test cases available in ${scriptGrpInstance?.name}  "
			redirect(action:"list")
		}
	}
	
	
	/**
	 * Function used to downloading total test case doc for module
	 */
	def downloadModuleTestCaseInExcel(){
		try{
			def totalTestCaseMap =testCaseService?.downloadModuleTestCaseInExcel(params,getRealPath())
			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = params?.moduleName?.toString()
			response.setHeader("Content-disposition", "attachment; filename="+fileName +".${params.extension}")
			excelExportService?.exportTestSuiteTestCase(params?.moduleName,response.outputStream,totalTestCaseMap, testCaseService?.testCaseKeyMap())
		}catch(Exception e){
			println "ERROR "+ e.getMessage()
			e.printStackTrace()
		}
	}

	/**
	 * Function for upload test cases as xlsx file and copy the test case content in "scripts" .py files 
	 * @return
	 */
	/*def uploadTestCase(){
		try{
			def file = request?.getFile('file')
			if(file?.originalFilename?.endsWith(".xlsx")) {
				def rowInfoList = []
				def dataList = []
				Workbook workbook = WorkbookFactory.create(file?.getInputStream())
				Sheet sheet = workbook.getSheetAt(0)
				println sheet
				if(sheet){
					int rowStart = 0;
					int rowEnd = sheet?.getLastRowNum() + 1 ;
					for (int rowNum = rowStart; rowNum < rowEnd; rowNum++) {
						XSSFRow row = sheet?.getRow(rowNum);
						def rowData =[:]
						for (XSSFCell c : row) {
							int columnIndex = c.getColumnIndex()
							XSSFCell columnContent = row.getCell(columnIndex);
							rowInfoList.add(columnContent)
						}
						dataList.add(rowInfoList)
						rowInfoList = []
					}
				}
				int totalColumnCount = dataList?.get(0)?.size()
				def headerData = dataList?.get(0)
				def tcMap = [:]
				def totalTcList = []
				dataList?.each { content->					
					if(totalColumnCount ==  content?.size()){
						for(int i = 0 ; i < totalColumnCount ; i++  ){
							if(!(headerData?.get(i)?.equals(content?.get(i)))){
								tcMap?.put(headerData?.get(i),content?.get(i) )
							}
						}
						totalTcList?.add(tcMap)
						tcMap = [:]
					}
				}
				def moduleName = file?.originalFilename?.replaceAll(".xlsx", "")
				println "moduleName----------------------------- "+moduleName
				if(Module?.findByName(moduleName)){
					def scriptName
					def testCaseId
					def testObj
					def testType
					def supportBox
					def testPrerequest
					def rdkInterface
					def inputParams
					def autoApproch
					def expectedOutput
					def testStubInterface
					def skipped
					def releaseVersion
					def remarks
					def priority
					def each = totalTcList?.each{ tc ->
						if(tc != [:] ){
							tc?.each{ k,v ->
								if(k?.toString()?.equals(TC_SCRIPT)){
									scriptName = tc?.get(k)
								}else if(k?.toString()?.equals(TC_ID)){
									testCaseId = tc?.get(k)
								}else if(k?.toString()?.equals(TC_OBJ)){
									testObj=tc?.get(k)
								}else if(k?.toString()?.equals(TC_TYPE)){
									testType=tc?.get(k)
								}else if(k?.toString()?.equals(TC_SETUP)){
									supportBox=tc?.get(k)
								}else if(k?.toString()?.equals(TC_PRE_REQUISITES)){
									testPrerequest=tc?.get(k)
								}else if(k?.toString()?.equals(TC_INTERFACE)){
									rdkInterface=tc?.get(k)
								}else if(k?.toString()?.equals(TC_IOPARAMS)){
									inputParams=tc?.get(k)
								}else if(k?.toString()?.equals(TC_AUTOAPROCH)){
									autoApproch=tc?.get(k)
								}else if(k?.toString()?.equals(TC_EX_OUTPUT)){
									expectedOutput=tc?.get(k)
								}else if(k?.toString()?.equals(TC_TSI)){
									testStubInterface=tc?.get(k)
								}else if(k?.toString()?.equals(TC_PRIORITY)){
									priority=tc?.get(k)
								}else if(k?.toString()?.equals(TC_SKIP)){
									skipped=tc?.get(k)
								}else if(k?.toString()?.equals(TC_RELEASE_VERSION)){
									releaseVersion=tc?.get(k)
								}else if(k?.toString()?.equals(REMARKS)){
									remarks=tc?.get(k)
								}
							}
							println "SCRIPT NAME "+scriptName?.toString()
							println "====================================================================="
							if(scriptName && testCaseId && testObj && testType && supportBox  && rdkInterface &&  inputParams && autoApproch && expectedOutput && priority && testStubInterface ){
								try{
									def scrpt = scriptService.getScript(getRealPath(),moduleName,scriptName?.toString(),RDKV)
									def pathToDir =  "${request.getRealPath('/')}//fileStore"
									if(RDKV.equals(RDKV)){
										pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKV
									}
									def scriptsDirName = primitiveService.getScriptDirName(moduleName)
									//else if(RDKB.equals(RDKB)){
									//pathToDir = pathToDir + Constants.FILE_SEPARATOR + TESTSCRIPTS_RDKB
									//}
									File fileName = new File( pathToDir + Constants.FILE_SEPARATOR +scriptsDirName+Constants.FILE_SEPARATOR+moduleName+Constants.FILE_SEPARATOR+scriptName?.toString()+".py");

									if(fileName?.exists()){

										String s = ""
										List line = fileName?.readLines()
										int indx = line?.findIndexOf {  it.startsWith("'''")}
										String scriptContent = ""
										if(line.get(indx).startsWith("'''"))	{
											indx++
											while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
												s = s + line.get(indx)+"\n"
												indx++
											}
											indx ++
											while(indx < line.size()){
												scriptContent = scriptContent + line.get(indx)+"\n"
												indx++
											}
										}
										def parser = new XmlParser(); //[XML Slurper not validate the node is correct or not]
										def root = parser.parseText(s)
										if(root?.test_cases){
											root?.test_cases?.test_case_id[0].value = testCaseId?.toString()
											root?.test_cases?.test_objective[0].value =  testObj?.toString()
											root?.test_cases?.test_type[0].value = testType?.toString()
											root?.test_cases?.test_setup[0].value = supportBox?.toString()
											root?.test_cases?.pre_requisite[0].value = testPrerequest?.toString()
											root?.test_cases?.api_or_interface_used[0].value = rdkInterface?.toString()
											root?.test_cases?.input_parameters[0].value = inputParams?.toString()
											root?.test_cases?.automation_approch[0].value =  autoApproch?.toString()
											root?.test_cases?.except_output[0].value = expectedOutput?.toString()
											root?.test_cases?.priority[0].value = priority?.toString()
											root?.test_cases?.test_stub_interface[0].value = testStubInterface?.toString()
											root?.test_cases?.test_script[0].value = scriptName?.toString()
											root?.test_cases?.release_version[0].value =  releaseVersion?.toString()
											root?.test_cases?.skipped[0].value = skipped?.toString()
											root?.test_cases?.remarks[0].value =  remarks?.toString()
										}else{

											def writer = new StringWriter()
											def xml = new MarkupBuilder(writer)
											xml.test_cases(){
												xml.test_case_id(testCaseId?.toString())
												xml.test_objective(testObj?.toString())
												xml.test_type(testType?.toString())
												xml.test_setup(supportBox?.toString())
												xml.pre_requisite(testPrerequest?.toString())
												xml.api_or_interface_used(rdkInterface?.toString())
												xml.input_parameters(inputParams?.toString())
												xml.automation_approch(autoApproch?.toString())
												xml.except_output(expectedOutput?.toString())
												xml.priority(priority?.toString())
												xml.test_stub_interface(testStubInterface?.toString())
												xml.test_script(scriptName?.toString())
												xml.skipped(skipped?.toString())
												xml.release_version(releaseVersion?.toString())
												xml.remarks(remarks?.toString())
											}
											def testCaseNode = new XmlParser().parseText(writer.toString())
											root?.children()?.add(15,testCaseNode ) // Test case append at 15 position of xml header
										}
										String outxml
										try{
											outxml = XmlUtil?.serialize(root)
										}catch(Exception e){
											println " error "+e.getMessage()
											e.printStackTrace()
										}
										File pyHeader = new File( "${request.getRealPath('/')}//fileStore//pyHeader.txt")
										def pyHeaderContentList = pyHeader?.readLines()
										String pyHeaderContent = ""
										pyHeaderContentList.each {
											pyHeaderContent += it?.toString()+"\n"
										}
										String data =pyHeaderContent+"'''"+"\n"+outxml.toString() +"\n"+"'''"+"\n"+scrpt?.scriptContent
										fileName.write(data)
										flash.message= "Test Case Doc Updated successfuly "
									}
								}catch(Exception e){
									println "Error"+e.getMessage()
									flash.message= "Issue : Test cases not Updated  "
								}
							}else{
								println " INVALID test case entries------------->>>"
							}
						}
					}
				}else{
					flash.message = "Please test case with valid module name"
				}
			}else{
				flash.message = "Please  upload the .xlsx file"
			}
		}catch(Exception e){
			println "ERROR "+e.getMessage()
		}
		redirect(action:"list")
		return
	}*/
	
	/**
	 * Method to get the module list based on category
	 */
	def getModuleList(){
		def moduleList
		if(params?.category?.equals(Constants.RDKB_TCL)){
			moduleList = ['tcl']
		}else if(params?.category?.equals(Constants.RDKV)){
		 	moduleList = Module.findAll("from Module as b where (b.category='${Category.RDKV}' or b.category='${Category.RDKV_THUNDER}')")
		}else{
			moduleList = Module.findAllByCategory(params?.category)
		}
		render(template:"modulelist", model:[ moduleList : moduleList])
	}
	
	/**
	 * Method to check whether any script update operation is in progress.
	 */
	def getScriptUpdateStatus(){
		render new Gson().toJson(scriptUpdateProgress) 
	}
	
	/**
	 * Method to update the system created test suite based on module.
	 * @return
	 */
	def updateTestSuite(){
		Map status = [:]
		if(!scriptUpdateProgress){
			scriptUpdateProgress = true
			try {
				def module = params.module
				def category = params?.category
				def realPath = request.getRealPath("/")
				if(module instanceof String){
					try {
						module = Long.parseLong(module)
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
				try {
					def moduleName
					Module.withTransaction {
						Module mod = Module.get(module)
						moduleName = mod?.getName()
					}
					scriptService.updateScriptGroups(moduleName,realPath, category)
				} catch (Exception e) {
					e.printStackTrace()
				}finally{
					scriptUpdateProgress = false
				}
			} catch (Exception e1) {
				e1.printStackTrace()
			}
		}
		status.put("status", "update completed")
		render status as JSON
	}
	
	/**
	 * REST API to fetch the test JS files 
	 */
	def getTestJavaScript(String category, String module , String scriptName){

		boolean found = false
		String data = ""
		try {
			Module moduleObj = Module.findByName(module)
			/*currenlty support only video*/
			if(category?.equals(Constants.RDKV)){

				def scriptDirName = Constants.COMPONENT
				if(moduleObj){
					if(moduleObj?.testGroup?.groupValue?.equals(TestGroup.E2E.groupValue)){
						scriptDirName = Constants.INTEGRATION
					}
				}
				def path = getRealPath() +  FILESTORE + FILE_SEPARATOR + FileStorePath.RDKVJS.value()
				path = path + FILE_SEPARATOR + scriptDirName + FILE_SEPARATOR +module + FILE_SEPARATOR + scriptName
				File sFile = new File(path)
				params.format = "text"

				if(sFile.exists()){
					found = true
					params.extension = "js"
					data = new String(sFile.getBytes())
					response.setHeader("Content-Disposition", "attachment; filename=\""+ scriptName+"\"")
				}else{
					data = "Download failed !!! No valid script is available for download."
				}

			}else{
				data = "Download failed !!! Category not supported."
			}

		} catch (Exception e) {
			e.printStackTrace()
		}

		if(!found) {
			/*if requested test js file not available it returns error.txt*/
			params.extension = "txt"
			response.setHeader("Content-Disposition", "attachment; filename=\""+"error.txt\"")
		}
		response.setHeader("Content-Type", "application/octet-stream;")
		response.outputStream << data.getBytes()
	}
	
	def downloadTestSuiteXml(){
		def name = params?.id
		String scriptGroupData = getScriptGroupData(name)
		if(scriptGroupData){
			params.format = "text"
			params.extension = "xml"
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ name +".xml\"")
			response.setHeader("Content-Length", ""+scriptGroupData.length())
			response.outputStream << scriptGroupData.getBytes()
		}else{
			flash.message = "Download failed. Script Group data is not available."
			redirect(action: "list")
		}
	}
	
	def downloadMultiScriptXml(){
		def exName= params?.id
		String scriptGroupData
		Execution exec = Execution.findByName(exName)
		def exResList = ExecutionResult.findAllByExecution(exec)
		if(exResList?.size() > 0){
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			try{
				xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
				xml.xml(){
					xml.script_group(){
						xml.category(exec?.category)// for RDKB
						xml.scripts(){
							exResList?.each{ exRes ->
								xml.script_name(exRes?.script)
							}

						}
					}
				}
				scriptGroupData = writer.toString()
			}catch (Exception e){
				log.error "ERROR "+e.getMessage()
				e.printStackTrace()
			}
		}

		if(scriptGroupData){
			params.format = "text"
			params.extension = "xml"
			response.setHeader("Content-Type", "application/octet-stream;")
			response.setHeader("Content-Disposition", "attachment; filename=\""+ exName+".xml\"")
			response.setHeader("Content-Length", ""+scriptGroupData.length())
			response.outputStream << scriptGroupData.getBytes()
		}else{
			flash.message = "Download failed. Script Group data is not available."
			redirect(action: "list")
		}

	}
	/**
	 * Only display thunder script content
	 *
	 */
	def thunderScriptDisplay(){
		def scriptName = params?.scriptName
		if(scriptName?.toString()?.contains('@')){
			def name  = scriptName?.tokenize('@')
			scriptName = name[1]
		}else{
			scriptName = params?.scriptName
		}
		def scriptMap = scriptService.getThundertScript(scriptName)
		if(scriptMap!=null){
			def scriptText = scriptMap.scriptContent
			render (view:"editScript", model:[script : scriptMap , category : Category.RDKV_THUNDER.toString()])
		}else{
			render "No script available with this name : "+scriptName
		}
	}
}
