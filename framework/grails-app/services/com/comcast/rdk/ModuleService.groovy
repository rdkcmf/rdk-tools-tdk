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

import groovy.xml.MarkupBuilder
import groovy.xml.XmlUtil;


import java.io.File;

/**
 * Service class for Module related operations
 * 
 *
 */
class ModuleService {

	def primitiveService

	/**
	 * Deletes functions of the given module
	 * @param moduleInstance      
	 *      
	 **/
	def deleteFunctionandParameters(final Module moduleInstance, def category, def applnPath){
		def functionInstance = Function.findAllByModule(moduleInstance)
		functionInstance.each{ fnInstance ->
			deleteParameters(fnInstance)
			fnInstance.delete(flush: true)
		}

		//TODO In appln we need to move to dynamic file separator
		def fileSeparator=Constants.FILE_SEPARATOR

		//Deletes the component folder and its contents
		if(category){
			if(category == Category.RDKV){
				//ISSUE fix - for rdkv test scripts
				def path=applnPath+fileSeparator+"fileStore"+fileSeparator+"testscriptsRDKV"+fileSeparator+"component"+fileSeparator+moduleInstance.name
				deleteModuleFiles(path, moduleInstance.name)

				//Delete integration folder and its contents 
				path=applnPath+fileSeparator+"fileStore"+fileSeparator+"testscriptsRDKV"+fileSeparator+"integration"+fileSeparator+moduleInstance.name
				deleteModuleFiles(path, moduleInstance.name)
			}
			else if(category == Category.RDKB){
				def path=applnPath+fileSeparator+"fileStore"+fileSeparator+"testscriptsRDKB"+fileSeparator+"component"+fileSeparator+moduleInstance.name
				deleteModuleFiles(path, moduleInstance.name)
				
				path=applnPath+fileSeparator+"fileStore"+fileSeparator+"testscriptsRDKB"+fileSeparator+"integration"+fileSeparator+moduleInstance.name
				deleteModuleFiles(path, moduleInstance.name)
			}
		}
	}

	/**
	 * Deletes parameters of the given function
	 * @param function
	 * @return
	 */
	def deleteParameters(final Function function){
		def parameterList = ParameterType.findAllByFunction(function)
		parameterList?.each { parameters ->
			try{
				def parameterInstanceList = Parameter.findByParameterType(parameters)
				parameterInstanceList?.each { parameterType ->
					parameterType.delete()
				}
				parameters.delete()
			}
			catch(Exception ex){
				//                log.error(parameters.errors)
			}
		}
	}


	/**
	 * Deletes the script files and entries for primitive test 
	 * @param scriptPath Absolute path to script directory
	 * @param module Module name
	 * 
	 */
	def deleteModuleFiles(def scriptPath, def moduleName){

		def  scriptDir=  new File( scriptPath)
		if (scriptDir && scriptDir.exists()){
			/*for (File script : scriptDir.listFiles()){
			 script.delete()
			 }*/
			deleteFilesFromModule(scriptDir)
			scriptDir.delete()

			def primitiveTests=  PrimitiveService.primitiveMap.get(moduleName)
			primitiveTests.each{ pTest->
				//Removes primitive test for the module
				PrimitiveService.primitiveList.remove( pTest )
				//Removes primitive test & module entry
				PrimitiveService.primitiveModuleMap.remove( pTest )
			}
			//Removes module and primitive tests entry
			PrimitiveService.primitiveMap.remove( moduleName )
		}
	}

	/**
	 *  Creates new module if it does not exist in the fileStore
	 * 
	 */
	def createModule(def moduleInstance, def rootPath, def category, def testGroup){
		def created = false
		def testScriptsDir = getTestScriptsFolder(category)
		def testGrp = TestGroup.valueOf(testGroup)
		def directory = null
		if(testGrp == TestGroup.Component){
			directory = rootPath + Constants.FILE_SEPARATOR + "fileStore" +Constants.FILE_SEPARATOR + testScriptsDir + Constants.FILE_SEPARATOR + Constants.COMPONENT + Constants.FILE_SEPARATOR + moduleInstance?.name
		}
		else if(testGrp == TestGroup.E2E){
			directory = rootPath + Constants.FILE_SEPARATOR + "fileStore" +Constants.FILE_SEPARATOR + testScriptsDir + Constants.FILE_SEPARATOR + Constants.INTEGRATION + Constants.FILE_SEPARATOR + moduleInstance?.name
		}
		
		File dir  = new File(directory)
		if(!dir.exists()){
			created = dir.mkdir()
		}
		else if(dir.exists()){
			created = true
		}
		def file = new File(dir.absolutePath + Constants.FILE_SEPARATOR + moduleInstance?.name+".xml")
		if(!file.exists()){
			created = file.createNewFile()
			file.write(createXmlModuleDeclaration(moduleInstance))
		}
		created
	}


	/**
	 * Adds function to primitive test file
	 * 	
	 * @param params
	 * @param rootPath
	 * @param category
	 * @return
	 */
	def addFunction(def params, def rootPath, def category){
		def writer = null
			def moduleInstance = Module.findById(params?.module?.id)
			def testScriptsDir = getTestScriptsFolder(category)
			def primitiveXml = getPrimitiveTestFilePath(rootPath , moduleInstance, category)
			File primitiveFile = new File(primitiveXml)
			if(!primitiveFile.exists()){
				primitiveFile.createNewFile()
				primitiveFile.write(createXmlModuleDeclaration(moduleInstance))
			}
			def xml = new XmlSlurper().parse(primitiveFile)
		//	XmlParser parser = new XmlParser();
		//	def xml = parser.parseText(primitiveFile)
			def val = xml.module?.primitiveTests?.primitiveTest.find{it.function?.text().equals(params?.name?.trim())}
			if(val == null || "".equals(val?.text()?.trim())){
				xml.module?.primitiveTests*.appendNode({primitiveTest(name:params?.name, id : '' , version :'1'){function(params?.name)}})
				writer = new FileWriter(primitiveFile)
				XmlUtil.serialize(xml, writer)
				primitiveService.addToPrimitiveList(params?.name,  moduleInstance?.name, category.toString())
			}
			else{
				println params?.name+" already exists"
			}
			if(writer != null){
				writer.close()
			}
	}

	/**
	 * Remove function from primitive test file
	 *  
	 * @param params
	 * @param rootPath
	 * @param category
	 * @return
	 */

	def removeFunction(def params, def rootPath, def category, def functionList){
		def writer = null
		try{
			def moduleInstance = Module.findById(params?.moduleid)
			def testScriptsDir = getTestScriptsFolder(category)
			if(moduleInstance){
				def primitiveXml = getPrimitiveTestFilePath(rootPath , moduleInstance, category)
				def primitiveFile = new File(primitiveXml)
				def xml = new XmlSlurper().parse(primitiveFile)
			//	XmlParser parser = new XmlParser();
			//	def xml = parser.parseText(primitiveFile)				
				functionList.each{ functionName ->
					xml.module?.primitiveTests?.primitiveTest?.each{ primTest ->
						def val = primTest.function?.find{it.text()?.trim().equals(functionName?.trim())}
						if(val != null || !"".equals(val?.text()?.trim())){
							val.parent().replaceNode{}
						}
						else{
							println functionName+" does not exist"
						}
						primitiveService.primitiveListMap.get(category)?.removeAll(functionName)
						primitiveService.primitiveMap?.get(moduleInstance?.name)?.remove(functionName)
						primitiveService.primitiveModuleMap.remove(functionName)
					}
				}
				writer = new FileWriter(primitiveFile)
				XmlUtil.serialize(xml, writer)
			}
			else{
				println "No module found"
			}
		}
		catch(Exception e){
			e.printStackTrace()
		}
		finally{
			if(writer != null){
				writer.close()
			}
		}
	}


	/**
	 * Add parameter to primitive file
	 * 
	 * @param params
	 * @param rootPath
	 * @param category
	 * @return
	 */

	def addParameter(def params, def rootPath, def category){
		def result = [:]
		def writer = null
		try{
			def moduleInstance = Module.findById(params?.module)
			def testScriptsDir = getTestScriptsFolder(category)
			def primitiveXml = getPrimitiveTestFilePath(rootPath , moduleInstance, category)
			File primitiveFile = new File(primitiveXml)
			def defaultVal = params?.defaultVal
			def functionId = params?.function?.id
			def func = Function.findById(functionId)
			def xml = new XmlSlurper().parse(primitiveFile)
		//	XmlParser parser = new XmlParser();
		//	def xml = parser.parseText(primitiveFile)
			
		    def primaryTest = xml.module.primitiveTests.primitiveTest.find{ primitive  ->
				primitive.@name.equals(func?.name?.trim())
			}
			
			/*xml.module?.primitiveTests?.primitiveTest.find{ primitiveTest ->
				 primitiveTest.name().equals('primitiveTest') && primitiveTest.@name.equals(func?.name)
			}*/
			
			/*slurper.module.primitiveTests.primitiveTest.find{ primitive  ->
				primitive.@name.equals('function4')
			}*/
			if(primaryTest != null && !primaryTest.@name?.text()?.trim()?.equals('')){
				def parameterList = primaryTest?.parameters
				if((parameterList == null || "".equals(parameterList.text()?.trim())) && parameterList.isEmpty()){
					primaryTest.appendNode({ parameters(){ parameter(name:params?.name, value:params?.defaultVal)	}})
					result.success = true
				}
				else{
					if((primaryTest.parameters?.parameter?.find{ it.@name.equals(params?.name)} == null) || (primaryTest.parameters?.parameter?.find{ it.@name.equals(params?.name)}.@name?.text().trim().equals(''))){
						primaryTest.parameters?.appendNode({parameter(name:params?.name, value:params?.defaultVal)})
						result.success = true
					}
					else{
						result.message = "parameter " + params?.name +" already exists"
						result.success = false
					}
				}
				if(result.success){
					writer = new FileWriter(primitiveFile)
					XmlUtil.serialize(xml, writer)
					result.success = true
				}
				
			}else{
				result.message = "No function ${func} found in primitive file"
				result.success = false
			}
		}
		catch(Exception e){
			e.printStackTrace()
			result.message = e.message
			result.success = false
		}
		finally{
			if(writer != null){
				writer.close()
			}
		}
		result
	}

	/**
	 * Remove parameters from primitive file
	 * 
	 * @param params
	 * @param rootPath
	 * @param category
	 * @param paramList
	 * @return
	 */
	def removeParameters(def params, def rootPath, def category, def paramList){
		def writer = null
		try{
			def moduleInstance = Module.findById(params?.moduleid)
			def testScriptsDir = getTestScriptsFolder(category)
			def primitiveXml = getPrimitiveTestFilePath(rootPath , moduleInstance, category)
			File primitiveFile = new File(primitiveXml)
			def xml = new XmlSlurper().parse(primitiveFile)
		//	XmlParser parser = new XmlParser();
		//	def xml = parser.parseText(primitiveFile)
			paramList.each{ param ->
				xml.module?.primitiveTests?.primitiveTest?.each{ primitive ->
					def parameter = primitive?.parameters?.parameter?.find{it.@name.equals(param?.trim())}
					if(parameter != null || !"".equals(parameter?.text()?.trim())){
						parameter.replaceNode{}
					}else{
						println "Parameter " + param + " does not exist"
					}
				}
			}
			writer = new FileWriter(primitiveFile)
			XmlUtil.serialize(xml, writer)
		}
		catch(Exception e){
			println e.getMessage()
			e.printStackTrace()
		}
		finally{
			if(writer != null){
				writer.close()
			}
		}
	}

	private String createXmlModuleDeclaration(def moduleInstance){
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		xml.mkp.xmlDeclaration(version: "1.0", encoding: "UTF-8")
		xml.xml(){
			xml.module("name":moduleInstance?.name, "testGroup":moduleInstance.testGroup){ primitiveTests() }
		}
		return writer.toString()
	}

	private void deleteFilesFromModule(File dir){
		File[] list = dir.listFiles()
		list.each{ file ->
			if(file.isDirectory()){
				deleteFilesFromModule(file)
			}
			else if(file.isFile()){
				file.delete()
			}
		}
	}

	private String getTestScriptsFolder(def category){
		def dir = null
		switch(category){
			case Category.RDKV:
				dir = FileStorePath.RDKV.value()
				break
			case Category.RDKB:
				dir = FileStorePath.RDKB.value()
				break
			default:
				dir = null
				break
		}
		return dir
	}

	private String getPrimitiveTestFilePath(def rootPath , def module, def category){
		return rootPath + Constants.FILE_SEPARATOR + "fileStore" +Constants.FILE_SEPARATOR + getTestScriptsFolder(category) + 	Constants.FILE_SEPARATOR +
				Utility.getModuleParentDirectory(module?.testGroup) + Constants.FILE_SEPARATOR + module?.name + Constants.FILE_SEPARATOR + module?.name+".xml"
	}
}
