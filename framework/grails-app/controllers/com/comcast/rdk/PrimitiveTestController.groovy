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
import groovy.xml.MarkupBuilder
import groovy.xml.XmlUtil

import org.springframework.dao.DataIntegrityViolationException
import org.springframework.util.StringUtils;

import com.google.gson.JsonObject

class PrimitiveTestController {

	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def primitivetestService

	def primitiveService

	def utilityService

	def index() {
		redirect(action: "list", params: params)
	}

	def list() {
		def primitiveTestListV = primitiveService.getAllPrimitiveTest(getRealPath(),RDKV)
		def primitiveTestListB = primitiveService.getAllPrimitiveTest(getRealPath(), RDKB)
		def primitiveTestList = primitiveService.getAllPrimitiveTest(getRealPath())
		[primitiveTestInstanceList: primitiveTestList, primitiveTestInstanceTotal: primitiveTestList.size()]
	}

	/**
	 * Method to create the filtered script list based on module
	 * @param scriptInstanceList
	 * @return
	 */
	private Map createPrimitiveTestMap(def primitiveTestList ){
		List primitiveList = []
		Map primitiveTestMap = [:]
		primitiveTestList.each { primitiveTest ->
			String moduleName = primitiveTest.getModule().getName();
			List subList = primitiveTestMap.get(moduleName);
			if(subList == null){
				subList = []
				primitiveTestMap.put(moduleName, subList);
			}
			subList.add(primitiveTest)
		}
		return primitiveTestMap
	}

	/**
	 * TODO: Complete java doc
	 * @return
	 * @author subrata
	 */
	def template() {
		def category = params?.category
		def moduleInstanceList = Module.where{
			(groups==null || groups==utilityService.getGroup()) && category==category
		}.sort('name', 'asc')
		[moduleInstanceList : moduleInstanceList, category:category]
	}


	/**
	 * TODO: Complete java doc
	 * @return
	 */
	def getFunctions() {
		if(! params.moduleId) {
			render "No module id found"
			return
		}

		def module = Module.get(params.moduleId as Long)

		if(! module) {
			render "No module found with id : ${params.moduleId}"
			return
		}

		def functions = Function.findAllByModule(module)
		render functions as JSON
	}

	/**
	 * TODO: Compete java doc
	 * @return
	 * 
	 * @author subrata
	 */
	def getParameters1() {
		if(! params.functionId) {
			render "No function id found"
			return
		}

		def function = Function.get(params.functionId as Long)
		if(! function) {
			render "Function not found with id : ${params.functionId}"
		}

		def parameters = []
		def parameterTypes = ParameterType.withCriteria {
			eq ('function', function)
			order('name')
		}

		parameterTypes.each {
			def result = [id: it.id, name: it.name, range: it.rangeVal, type: it.parameterTypeEnum?.toString()]
			parameters += result
		}
		render parameters as JSON
	}

	/**
	 * TODO: Complete java doc
	 * @return
	 * 
	 * @author subrata
	 */
	def create() {
		def primitiveTestMapB = primitiveService.getAllPrimitiveTest(getRealPath(), RDKB)
		def primitiveTestMapA = primitiveService.getAllPrimitiveTest(getRealPath(), RDKV)
		def primitiveTestListB = primitiveService.getPrimitiveList(getRealPath(), RDKB)?.sort()
		def primitiveTestListA = primitiveService.getPrimitiveList(getRealPath(), RDKV)?.sort()
		def primitiveTestMap =  primitiveService.getAllPrimitiveTest(getRealPath())

		[primitiveTestListA : primitiveTestListA, primitiveTestListB : primitiveTestListB, error: params.error, primitiveTestId: params.primitiveTestId,
			primitiveTestCountA : PrimitiveTest.count(),primitiveTestMapA:primitiveTestMapA, primitiveTestMapB:primitiveTestMapB]

	}

	def getRealPath(){
		//request.getRealPath("/")
		request.getSession().getServletContext().getRealPath("/")
	}

	def getPrimitiveFilePath(def moduleName, def category){
		def scriptDirName = primitiveService.getScriptDirName(moduleName)
		def path = getFileScriptsPath(category,moduleName)
		path =  path + FILE_SEPARATOR + scriptDirName + FILE_SEPARATOR + moduleName + FILE_SEPARATOR + moduleName+".xml"
		return path
	}

	def getPrimitiveFileDirectory(def moduleName, def category){
		def scriptDirName = primitiveService.getScriptDirName(moduleName)
		return getFileScriptsPath(category,moduleName)+ FILE_SEPARATOR +scriptDirName + FILE_SEPARATOR + moduleName
	}

	/**
	 * TODO: Complete java doc
	 * @return
	 * 
	 * @author subrata
	 */
	def save() {
		def category = params?.category
		def error = ''
		try {
			//def primitiveList = primitiveService.getPrimitiveList(getRealPath(), category)
			def primitiveList = primitiveService.getAllPrimitiveTest(getRealPath(), category)
			if(primitiveService.checkPrimitiveTestExists(params?.testName?.trim())){
				render("Duplicate PrimitiveTest Name not allowed. Try Again")
			}
			else{
				def moduleObj = Module.get(params?.module as Long)
				def fun = Function.get(params?.functionValue as Long)

				def primitiveFile = new File(getPrimitiveFilePath(moduleObj?.getName(), category))

				if(primitiveFile.exists()){
					//def data = primitiveFile.readBytes()
					//def root = new XmlSlurper().parse(primitiveFile)

					def data = primitiveFile.readLines()
					int indx = data?.findIndexOf { it.startsWith("<?xml")}
					String xmlContent =""
					while(indx < data.size()){
						xmlContent = xmlContent + data.get(indx)+"\n"
						indx++
					}
					def parser = new XmlSlurper()
					def root = parser.parseText(xmlContent?.toString())

					def list1 = []
					if(params.parameterTypeIds) {
						params.parameterTypeIds.split(", ").each {
							if(it) {
								def value = params["value_${it}"]
								def parameterType = ParameterType.get(it as Long)
								def pMap = [:]
								pMap.put("parameterType",parameterType?.name)
								pMap.put("value",value ?: '')
								list1.add(pMap)
							}
						}
						def funName = fun?.getName()
						root?.module?.primitiveTests?.appendNode{
							primitiveTest(name :params?.testName?.trim(),id:" ",version: "1"){
								function(fun?.getName())
								parameters{
									list1.each { p ->
										parameter("name":p?.parameterType,"value":p?.value)
									}
								}
							}
						}
					}
					else{

						root?.module?.primitiveTests?.appendNode{
							primitiveTest(name :params?.testName?.trim(),id:'',version:'1'){
								function(fun?.getName())
								parameters()
							}
						}

					}
					//                    }
					try {
						def writer = new FileWriter(primitiveFile)
						XmlUtil.serialize(root, writer)
						if( primitiveService.addToPrimitiveList(params?.testName?.trim(),moduleObj.getName(), category))
						{
							render "PrimitiveTest created successully"
						}
						else
						{
							render "PrimitiveTest not created successully "
						}

					} catch (Exception e) {
						primitiveFile.write(new String(data))
						e.printStackTrace()
					}
					//					render(message(code: 'default.created.message', args: [
					//						message(code: 'primitiveTest.label', default: 'Primitive Test'),
					//						params?.testName
					//					]))
				}else{
					if(moduleObj){
						def list1 = []
						if(params.parameterTypeIds) {
							params.parameterTypeIds.split(", ").each {
								if(it) {
									def value = params["value_${it}"]
									def parameterType = ParameterType.get(it as Long)

									def pMap = [:]
									pMap.put("parameterType",parameterType?.name)
									pMap.put("value",value ?: '')
									list1.add(pMap)
								}
							}
						}
						def funName = fun?.getName()
						try {
							def writer = new StringWriter()
							def xml = new MarkupBuilder(writer)
							xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
							xml.xml(){

								xml.module("name":moduleObj?.name, "testGroup":moduleObj.testGroup){


									xml.primitiveTests(){

										xml.primitiveTest(name : params?.testName?.trim(), id : '' , version :'1' ){
											xml.function(funName)
											if(list1.size()> 0){
												xml.parameters(){
													list1.each { p ->
														xml.parameter("name":p?.parameterType,"value":p?.value)
													}
												}
											}else{
												xml.parameters()
											}
										}
									}
								}
							}
							String dirname = moduleObj?.name
							dirname = dirname?.trim()
							File dir = new File(getPrimitiveFileDirectory(dirname, category))

							if(!dir.exists()){
								dir.mkdirs()
							}

							File file = new File( getPrimitiveFilePath(dirname, category));
							if(!file.exists()){
								file.createNewFile()
							}
							File xmlHeader = new File( "${request.getRealPath('/')}//fileStore//xmlHeader.txt")
							def xmlHeaderContentList = xmlHeader?.readLines()
							String xmlHeaderContent = ""
							xmlHeaderContentList.each {
								xmlHeaderContent += it?.toString()+"\n"
							}

							file.write(xmlHeaderContent+writer.toString())
							//file.write(writer.toString())
							if(primitiveService.addToPrimitiveList(params?.testName?.trim(),moduleObj.getName(), category)){
								render "PrimitiveTest created successully"
							}else{
								render "PrimitiveTest not created successully"
								
							}
													} catch (Exception e) {
							e.printStackTrace()
						}
					}
				}
			}
		}
		catch(Throwable th) {
		}

	}

	def deleteTest() {
		def primitiveName = params?.id
		def primitiveList = primitiveService.getPrimitiveList(getRealPath(), params?.category)
		if(!primitiveList.contains(primitiveName)){
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
			redirect(action: "create")
			return
		}

		try {
			if(primitiveService.deletePrimitiveTest(getRealPath(), primitiveName)){
				flash.message = message(code: 'default.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
				render("success")
			}else{
				flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
				render("success")
			}
		}
		catch (DataIntegrityViolationException e) {
			flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), primitiveName])
			render("success")
		}
	}


	/**
	 * TODO: Complete java doc
	 * @return
	 * 
	 * @author subrata
	 */
	def getEditableTest() {
		def primitiveModuleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def module = primitiveModuleMap.get(""+params?.id)
		def category = params?.category?.trim()
		def cat = null
		def param = params?.id?.trim()
		try{
			cat = Utility.getCategory(category)?.toString()
		}
		catch(Exception ex) {
			cat = getCategoryFromMap(param)
		}

		def primitiveTest =primitiveService.getPrimitiveTest(getPrimitiveFilePath(module, cat), params?.id)
		def functions = Function.findAllByModule(primitiveTest?.module)
		def parameterTypes = ParameterType.findAllByFunction(primitiveTest?.function)
		def ids = parameterTypes - (primitiveTest?.parameters?.parameterType)
		[primitiveTest: primitiveTest, functions: functions, paramTypes : parameterTypes, newParams : ids, category : cat]
	}

	/**
	 * Method to get the category of primitive test if missing in the request
	 * 
	 * @param param
	 * @return
	 */
	def getCategoryFromMap(def param){
		def category = null
		[RDKV, RDKB].each{ cat ->
			if(category == null){
				def primList =  primitiveService.primitiveListMap?.get(cat)
				if(primList?.contains(param)){
					category = cat
				}
				else{
					category = null
				}
			}
		}
		category
	}


	/**
	 * TODO: Complete java doc
	 * @param id
	 * @param version
	 * @return
	 * 
	 * @author subrata
	 */
	def update(Long id, Long version) {
		def category = params?.category
		def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def moduleName = moduleMap.get(params?.id)
		def primitiveFilePath = getPrimitiveFilePath(moduleName, category)

		File ff =new File(primitiveFilePath);
		def data = ff.readBytes()
		def error
		long vers1 = 0
		if (params?.ptVersion != null) {
			try {
				def b = params?.ptVersion
				if( b instanceof String){
					vers1 = Long.parseLong(b)
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
		def fun = Function.get(params?.functionValue as Long)
		def primitiveFile = new File(primitiveFilePath)
		if(primitiveFile.exists()){
			def lines = primitiveFile?.readLines()
			int indx = lines?.findIndexOf { it.startsWith("<?xml")}
			String xmlComtent =""
			while(indx < lines.size()){
				xmlComtent = xmlComtent + lines.get(indx)+"\n"
				indx++
			}
			def parser = new XmlParser();
			def root = parser.parseText(xmlComtent)



			def list1 = []
			if(params.parameterTypeIds) {
				params.parameterTypeIds.split(", ").each {
					if(it) {
						def value = params["value_${it}"]
						def parameterType = ParameterType.get(it as Long)

						def pMap = [:]
						pMap.put("parameterType",parameterType?.name)
						pMap.put("value",value ?: '')
						list1.add(pMap)
					}
				}
				def funName = fun?.getName()
				def pNode = root?.module?.primitiveTests?.primitiveTest?.find{ it.@name == params?.id }
				long vers2 = 0

				try {
					vers2 = Long.parseLong((""+pNode?.@version)?.trim())
				} catch (Exception e) {
					e.printStackTrace()
				}
				if(vers2 == vers1){
					vers2 ++

					pNode.replaceNode{
						primitiveTest(name :params?.id,id:" ",version: vers2){
							function(fun.getName())
							parameters(){
								list1.each { p ->
									parameter("name":p?.parameterType,"value":p?.value)
								}
							}
						}
					}

					try {
						OutputStreamWriter out = new OutputStreamWriter(new FileOutputStream(primitiveFile),"UTF-8");
						XmlUtil.serialize(root, out)
						flash.message = message(code: 'default.updated.message', args: [message(code: 'primitiveTest.label', default: 'PrimitiveTest'), params?.id])
					} catch (Exception e) {
						File ff1 =new File(primitiveFilePath);
						ff1.write(new String(data))
						flash.message = "Error in updating the primitive test"
						e.printStackTrace()
					}
				}else{
					flash.message = "Another user has updated this PrimitiveTest while you were editing"
				}

			}
		}else{
			flash.message = "Error in updating the primitive test"
		}

		redirect(action: 'create', params: [primitiveTestId: params.id,error: error])

	}

	
	/**
	 * Method to check whether the string is a float
	 * @param number
	 * @return
	 */
	public static boolean isFloat(String inputString){
		def status = true
		try
		{
			Float.parseFloat(inputString);
		}
		catch(NumberFormatException e)
		{
			status = false
		}
		return status
	}

	
	/**
	 * Method to check whether the string is an integer
	 * @param str
	 * @return
	 */
	public static boolean isInteger(String inputString) {

		def isInteger = true
		int length = inputString?.length();
		if (length > 0) {
			int i = 0;
			if (inputString?.charAt(i) == '-') {
				if (length == 1) {
					isInteger = false;
				}
				i = 1;
			}
			for (; i < length; i++) {
				char c = inputString?.charAt(i);
				if (c <= '/' || c >= ':') {
					isInteger = false;
				}
			}
		}else{
			isInteger = false;
		}
		return isInteger;
	}


	/**
	 * Returns JSON data
	 * @param testName
	 * @param idVal
	 * @return
	 */
	def getJson(final String testName, final String idVal) {
		def scriptDirName
		def primitiveTest
		def moduleMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def mName= moduleMap.get(testName)
		try{
			if(mName){
				scriptDirName = primitiveService.getScriptDirName(mName)
				primitiveTest = primitiveService.getPrimitiveTest(getRealPath()+"/fileStore/testscripts/"+scriptDirName+"/"+mName+"/"+mName+".xml", testName)
			}
		}catch(Exception e){
			println e.getMessage()
		}
		render primitivetestService.getJsonData( primitiveTest, idVal )
	}

	/**
	 * Returns JSON data of stream details based on the
	 * streamId received
	 * @param idVal
	 * @return
	 */
	def getStreamDetails(final String idVal, final String stbIp) {

		Device device = Device.findByStbIpAndIsChild(stbIp?.trim(),STAND_ALONE_DEVICE);
		JsonObject outData = new JsonObject()
		String boxtype = device?.boxType?.type?.toLowerCase()
		String deviceNotFound = "Device not found"
		if(device){
			if(boxtype?.equals( BOXTYPE_CLIENT ) ) {
				String gateway = device?.gatewayIp.toString()
				Device gatewayDevice =  Device.findByStbName(gateway.trim())
				if(gateway) {

					if(idVal?.startsWith("R")){
						RadioStreamingDetails streamingDetails = RadioStreamingDetails.findByStreamId(idVal)
						DeviceRadioStream deviceStream = DeviceRadioStream.findByDeviceAndStream( gatewayDevice, streamingDetails )
						outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
						outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
						outData.addProperty(KEY_CHANNELTYPE, "radio");
						outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
						outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
						outData.addProperty(KEY_AUDIOFORMAT, "N/A");
						outData.addProperty(KEY_VIDEOFORMAT, "N/A");
					}else{
						StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
						DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( gatewayDevice, streamingDetails )
						outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
						outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
						outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType?.toString());
						outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
						outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
						outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat?.toString());
						outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat?.toString());
					}
				}
			}else if(boxtype?.equals( BOXTYPE_STANDALONE_CLIENT )) {
				String gateway = device?.gatewayIp.toString()
				Device gatewayDevice =  Device.findByStbName(gateway.trim())
				if(gateway) {

					if(idVal?.startsWith("R")){
						RadioStreamingDetails streamingDetails = RadioStreamingDetails.findByStreamId(idVal)
						DeviceRadioStream deviceStream = DeviceRadioStream.findByDeviceAndStream( device, streamingDetails )
						outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
						outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
						outData.addProperty(KEY_CHANNELTYPE, "radio");
						outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
						outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
						outData.addProperty(KEY_AUDIOFORMAT, "N/A");
						outData.addProperty(KEY_VIDEOFORMAT, "N/A");
					}else{
						StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
						DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( device, streamingDetails )
						outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
						outData.addProperty(KEY_GATEWAYIP, gatewayDevice?.stbIp?.toString());
						outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType?.toString());
						outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
						outData.addProperty(KEY_RECORDERID, gatewayDevice?.recorderId?.toString());
						outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat?.toString());
						outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat?.toString());
					}
				}


			}else{

				if(idVal?.startsWith("R")){
					RadioStreamingDetails streamingDetails = RadioStreamingDetails.findByStreamId(idVal)
					DeviceRadioStream deviceStream = DeviceRadioStream.findByDeviceAndStream( device, streamingDetails )
					outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
					outData.addProperty(KEY_GATEWAYIP, device?.stbIp?.toString());
					outData.addProperty(KEY_CHANNELTYPE, "radio");
					outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
					outData.addProperty(KEY_RECORDERID, device?.recorderId?.toString());
					outData.addProperty(KEY_AUDIOFORMAT, "N/A");
					outData.addProperty(KEY_VIDEOFORMAT, "N/A");
				}else{
					StreamingDetails streamingDetails = StreamingDetails.findByStreamId(idVal)
					DeviceStream deviceStream = DeviceStream.findByDeviceAndStream( device, streamingDetails )
					outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
					outData.addProperty(KEY_GATEWAYIP, device?.stbIp?.toString());
					outData.addProperty(KEY_CHANNELTYPE, streamingDetails?.channelType?.toString());
					outData.addProperty(KEY_OCAPID, deviceStream?.ocapId?.toString());
					outData.addProperty(KEY_RECORDERID, device?.recorderId?.toString());
					outData.addProperty(KEY_AUDIOFORMAT, streamingDetails?.audioFormat?.toString());
					outData.addProperty(KEY_VIDEOFORMAT, streamingDetails?.videoFormat?.toString());
				}
			}
			render outData
		}else{
			render deviceNotFound
		}
	}


	/**
	 * Method to check whether Primitive Test with same Name exist or not. If yes returns the id of Primitive Test
	 * @return
	 */
	def fetchPrimitiveTest(){

		List primitiveTestInstanceList = []

		def primitiveMap = primitiveService.getPrimitiveModuleMap(getRealPath())
		def moduleName = primitiveMap.get(params?.testName)
		if(moduleName){
			def primitiveTestInstance = primitiveService.getPrimitiveTest(getPrimitiveFilePath(moduleName, params?.category), params?.testName)
			if(primitiveTestInstance){
				primitiveTestInstanceList.add(primitiveTestInstance.name)
			}
		}
		render primitiveTestInstanceList as JSON
	}

	def getFileScriptsPath(def category , def moduleName){
		def path = getRealPath() + FILE_SEPARATOR + "fileStore" + FILE_SEPARATOR
		def dirName
		if(!PrimitiveService.moduleDirMap.containsKey(category+"_"+moduleName)){
			if(RDKV.equals(category)){
				dirName = TESTSCRIPTS_RDKV
			}else if(RDKB.equals(category)){
				dirName = TESTSCRIPTS_RDKB
			}

		}else{
			dirName = PrimitiveService.moduleDirMap.get(category+"_"+moduleName)
		}
		if(RDKV.equals(category) || RDKB.equals(category)){
			path = path + dirName
		}
		path
	}
}
