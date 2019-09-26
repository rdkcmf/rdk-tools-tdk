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

import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;
import static com.comcast.rdk.Constants.FILE_SEPARATOR
import static com.comcast.rdk.Constants.*

import groovy.xml.XmlUtil

/**
 * Service class to handle the primitive xml
 *
 */
class PrimitiveService {

	public static volatile SortedMap primitiveModuleMap = new TreeMap(String.CASE_INSENSITIVE_ORDER);

	public static volatile Set primitiveList = []

	public static volatile Map primitiveListMap = [:]

	public static volatile Map primitiveMap = [:]

	public static volatile Map moduleDirMap = [:]

	public static volatile String realPathString = ""

	def initializePrimitiveTests(def realPath){

		realPathString = realPath

		List primitiveTestList = []

		List dirList = [Constants.COMPONENT, Constants.INTEGRATION]

		[TESTSCRIPTS_RDKB, TESTSCRIPTS_RDKV, TESTSCRIPTS_RDKV_ADV, TESTSCRIPTS_RDKB_ADV].each{ testScriptPath ->
			def primitiveList = []
			if(testScriptPath.equals(TESTSCRIPTS_RDKB) || testScriptPath.equals(TESTSCRIPTS_RDKB_ADV)){
				if(primitiveListMap.get(RDKB)){
					primitiveList = primitiveListMap.get(RDKB)
				}
			}else{
				if(primitiveListMap.get(RDKV)){
					primitiveList = primitiveListMap.get(RDKV)
				}
			}

			dirList.each{ directory ->
				try {
					File scriptsDir = new File( "${realPath}" + Constants.FILE_SEPARATOR + "fileStore" +  Constants.FILE_SEPARATOR + testScriptPath + Constants.FILE_SEPARATOR + directory )
					if(scriptsDir.exists()){
						def modules = scriptsDir.listFiles()
						modules.each { module ->
							File [] files = module.listFiles(new FilenameFilter() {
										@Override
										public boolean accept(File dir, String name) {
											return name.endsWith(module?.name?.toString()?.trim()+".xml");
										}
									});
							def list = []
							files.each { file ->
								try {
									if(testScriptPath.equals(TESTSCRIPTS_RDKB) || testScriptPath.equals(TESTSCRIPTS_RDKB_ADV)){
										moduleDirMap.put(RDKB+"_"+module?.name?.toString()?.trim(), testScriptPath)
									}else{
										moduleDirMap.put(RDKV+"_"+module?.name?.toString()?.trim(), testScriptPath)
									}
									def lines = file?.readLines()
									int indx = lines?.findIndexOf { it.startsWith("<?xml") }
									String xmlComtent =""
									while(indx >=0 && indx < lines.size()){
										xmlComtent = xmlComtent + lines.get(indx)+"\n"
										indx++
									}
									def parser = new XmlParser();
									def node = parser.parseText(xmlComtent?.toString())
									//def node = new XmlParser().parse(file)
									def pList = []
									node.each{
										try {
											it.primitiveTests.each{
												it.primitiveTest.each {
													String pName = "${it.attribute('name')}"
													if(StringUtils.hasText(pName)){
														pName = pName?.trim()
														pList.add(pName)
														primitiveList.add(pName)
														primitiveModuleMap.put(pName,""+module.getName())
													}
												}
											}
										} catch (Exception e) {
											println " Error "+e.getMessage()
											e.printStackTrace()
										}
									}
									primitiveMap.put(""+module.getName(), pList)
								} catch (Exception e) {
									println " Issue with Primitive File "+ file.getName() + " Error "+e.getMessage()
									e.printStackTrace()
								}
							}
						}

					}
				} catch (Exception e) {
					e.printStackTrace()
				}

			}
			if(testScriptPath.equals(TESTSCRIPTS_RDKB) || testScriptPath.equals(TESTSCRIPTS_RDKB_ADV)){
				primitiveListMap.put(RDKB, primitiveList)
			}
			else if(testScriptPath.equals(TESTSCRIPTS_RDKV) || testScriptPath.equals(TESTSCRIPTS_RDKV_ADV)){
				primitiveListMap.put(RDKV, primitiveList)
			}
		}
	}

	def getAllPrimitiveTest(def realPath){
		if(primitiveMap == null || primitiveMap.keySet().size() == 0){
			initializePrimitiveTests(realPath)
		}
		return primitiveMap
	}

	def getAllPrimitiveTest(def realPath, def category){
		if(primitiveMap == null || primitiveMap.keySet().size() == 0){
			initializePrimitiveTests(realPath)
		}
		if(StringUtils.hasText(category)){
			def modules = getModulesListBasedOnCategory(realPath, category)
			def map = [:]
			modules?.each{ module ->
				if(!(module?.toString()?.equals("scriptDb2File.py"))){
					map.put(module, primitiveMap.get(module)?.sort())
				}
			}
			return map
		}
		return primitiveMap
	}

	def getPrimitiveModuleMap(def realPath){
		if(primitiveModuleMap == null || primitiveModuleMap.keySet().size() == 0){
			initializePrimitiveTests(realPath)
		}
		return primitiveModuleMap
	}

	def getPrimitiveList(def realPath){
		if(primitiveList == null || primitiveList.size() == 0){
			initializePrimitiveTests(realPath)
		}
		return primitiveList
	}

	def getPrimitiveList(def realPath, def category){
		primitiveListMap = [:]
		if(primitiveListMap == null || primitiveListMap.size() == 0){
			initializePrimitiveTests(realPath)
		}
		return primitiveListMap.get(category)
	}

	def addToPrimitiveList(def name,def module){
		if(!primitiveMap.containsKey(module)){
			primitiveMap.put(module,[])
		}
		primitiveMap.get(module)?.add(name)
		primitiveModuleMap.put(name, module)
		primitiveList.add(name)
	}

	def addToPrimitiveList(def name,def module, def category){
		if(!primitiveMap.containsKey(module)){
			primitiveMap.put(module,[])
		}
		primitiveMap.get(module)?.add(name)
		primitiveModuleMap.put(name, module)
		if(!primitiveListMap.get(category)){
			primitiveListMap.put(category,[])
		}
		primitiveListMap.get(category)?.add(name)
	}

	def parsePrimitiveXml(def filePath){
		File primitiveXml = new File(filePath)
		def node = new XmlParser().parse(primitiveXml)
		def pList = []
		node.each{
			it.primitiveTests.each{
				it.primitiveTest.each {
					pList.add("${it.attribute('name')}")
				}
			}
		}
		return pList
	}

	/*to fetch the name of  directory in which primitive xml comes  */
	def getDirectoryName(def primitiveTestName){
		def dirName = ""
		try {
			def moduleName = primitiveModuleMap.get(primitiveTestName)
			if(moduleName){
				def category = getCategory(moduleName)
				if(!category){
					category =findCategory(moduleName)
				}
				dirName = moduleDirMap.get(category+"_"+moduleName)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return dirName
	}

	def deletePrimitiveTest(def realPath,def primitiveTestName){
		def moduleName = primitiveModuleMap.get(primitiveTestName)
		def dirName = getDirectoryName(primitiveTestName)
		primitiveList.removeAll(primitiveTestName)
		primitiveMap?.get(moduleName)?.remove(primitiveTestName)
		primitiveModuleMap.remove(primitiveTestName)
		def moduleObj = Module.findByName(moduleName)
		def scriptDirName = Constants.COMPONENT
		if(moduleObj){
			if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
				scriptDirName = Constants.INTEGRATION
			}
		}
		def category = moduleObj?.category.toString()
		def primitivePath = realPath+ FILE_SEPARATOR + "fileStore" + FILE_SEPARATOR
		if(RDKV.equals(category)){
			if(!dirName){
				dirName = FileStorePath.RDKV.value()
			}
			primitivePath = primitivePath + dirName + FILE_SEPARATOR
		}
		if(RDKB.equals(category)){
			if(!dirName){
				dirName = FileStorePath.RDKB.value()
			}
			primitivePath = primitivePath + dirName + FILE_SEPARATOR
		}
		primitivePath = primitivePath + scriptDirName + FILE_SEPARATOR + moduleName + FILE_SEPARATOR + moduleName+".xml"
		File primitiveFile = new File(primitivePath)
		// The new issue fixed
		def data = primitiveFile.readLines()
		int indx = data?.findIndexOf { it.startsWith("<?xml")}
		String xmlContent =""
		while(indx < data.size()){
			xmlContent = xmlContent + data.get(indx)+"\n"
			indx++
		}
		def parser = new XmlSlurper()
		def root = parser.parseText(xmlContent?.toString())
		//def root = new XmlSlurper().parse(primitiveFile)
		def primitiveNode = root.module.primitiveTests.primitiveTest.find{ it.@name == primitiveTestName }
		primitiveNode.replaceNode{}
		def writer = new FileWriter(primitiveFile)
		XmlUtil.serialize(root, writer)

		return true
	}

	def getScriptDirName(def moduleName){
		def moduleObj = Module.findByName(moduleName)
		def scriptDirName = Constants.COMPONENT
		if(moduleObj){
			if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
				scriptDirName = Constants.INTEGRATION
			}
		}
		return scriptDirName
	}
	def getCategory(def moduleName){
		Module moduleObj = Module.findByName(moduleName)
		return moduleObj?.getCategory()?.toString();
	}
	def getPrimitiveTest(def filePath,def primitiveTestName){
		def newFilePath = null
		def testScriptsPath = null
		def categoryFound = false
		if(!(filePath.contains(FileStorePath.RDKV.value()) || filePath.contains(FileStorePath.RDKB.value()))) {
			categoryFound = primitiveListMap.get(RDKV)?.contains(primitiveTestName?.trim())
			def dirName = getDirectoryName(primitiveTestName)
			if(!categoryFound) {
				categoryFound = primitiveListMap.get(RDKB)?.contains(primitiveTestName?.trim())
				if(!categoryFound){
					categoryFound = primitiveListMap.get(RDKB)?.contains(primitiveTestName)
				}
				if(categoryFound){
					if(!dirName){
						dirName = FileStorePath.RDKB.value()
					}
					testScriptsPath = dirName
				}
			}else{
				if(!dirName){
					dirName = FileStorePath.RDKV.value()
				}
				testScriptsPath = dirName
			}
			if(testScriptsPath != null) {
				try {
					def paths = filePath.split('fileStore')
					def file = null
					if(paths && paths?.length >= INDEX_TWO){
						def fileName = paths[1].split('testscripts')
						if(fileName && fileName?.length >= INDEX_TWO){
							file = fileName[1]?fileName[1]:fileName[0]
							newFilePath = paths[0] + 'fileStore' + FILE_SEPARATOR + testScriptsPath + file
							File primitiveXml = new File(newFilePath)
							if(!primitiveXml?.exists()){
								newFilePath = paths[0] + 'fileStore' + FILE_SEPARATOR + testScriptsPath + file
							}
						}
					}
				} catch (Exception e) {
					println " ERROR "+e.getMessage()
					e.printStackTrace()
				}

			}
		}else{
			newFilePath = filePath
		}

		Map primitiveMap = [:]
		try {
			File primitiveXml = new File(newFilePath)
			//def local = new XmlParser()
			//def node = local.parse(primitiveXml)

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
							def moduleName = primitiveModuleMap.get(primitiveTestName)
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

	def getModulesListBasedOnCategory(def path, def category){
		def modules = []
		def dirList = []
		if(RDKV.equals(category)){
			dirList.add(FileStorePath.RDKV.value())
			dirList.add(FileStorePath.RDKVADVANCED.value())
		}
		else if(RDKB.equals(category)){
			dirList.add(FileStorePath.RDKB.value())
			dirList.add(FileStorePath.RDKBADVANCED.value())
		}

		dirList.each { testScriptsFolder  ->
			def dir = path + FILE_SEPARATOR + "fileStore" + FILE_SEPARATOR + testScriptsFolder
			File f = new File(dir)
			if(f.exists() && f.isDirectory()){
				f.listFiles(new FilenameFilter(){
							boolean accept(File file, String arg1) {
								return file.isDirectory()
							};
						}).each{ file ->
							if(file.isDirectory()){
								modules.addAll(Arrays.asList(file.list()))
							}
						}
			}
		}
		if(!modules.isEmpty()){
			modules.sort()
		}
		modules
	}

	def findCategory(def moduleName){
		def category = null
		def moduleList = getModulesListBasedOnCategory(realPathString,RDKV)
		if(moduleList.contains(moduleName)){
			category = RDKV
		}else {
			moduleList = getModulesListBasedOnCategory(realPathString,RDKB)
			if(moduleList.contains(moduleName)){
				category = RDKB
			}
		}
		return category
	}
	
	def checkPrimitiveTestExists(def primitiveTest){
		boolean exist = false
		def primitiveList = primitiveListMap?.get(RDKV)
		if(!primitiveList?.contains(primitiveTest?.trim())){
			primitiveList = primitiveListMap?.get(RDKB)
			exist = primitiveList?.contains(primitiveTest?.trim())
		}else{
			exist = true
		}
		
		return exist
	}

}
