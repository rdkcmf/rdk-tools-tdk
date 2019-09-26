/**
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 * Copyright 2016 RDK Management
 *  Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.comcast.rdk

import static com.comcast.rdk.Constants.*

class TestCaseService {
	/**
	 * Inject the primitive Service
	 */
	def primitiveService
	/**
	 * Injects the scriptService
	 */
	def scriptService
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication	
	
	/**
	 * Function for downloading test case in excel file
	 */
	def downloadTestCaseInExcel(def params , realPath){ 
		Map testCaseDetails = [:]
		try{
			def moduleMap = primitiveService.getPrimitiveModuleMap(realPath)
			def moduleName = moduleMap.get(params?.primitiveTest)
			def scriptsDirName = primitiveService.getScriptDirName(moduleName)
			def scrpt = scriptService.getScript(realPath,moduleName, params?.name,params?.category)
			def testCase = scrpt?.testCaseDetails			
			testCaseDetails =  getTestCaseMap(testCase)
		}catch(Exception e){
			println "ERROR "+e.printStackTrace()
		}
		return  testCaseDetails
	}
	
	/**
	 * Function for downloading the test case in script group in excel file
	 */
	def downloadScriptGroupTestCase(def params ,def realPath){
		def totalTestCaseMap = [:]
		def testCaseMap = [:]
		boolean tesCaseValue = false
		try{
			def scriptGrpInstance = ScriptGroup?.findByName(params?.scriptGrpName)
			def moduleTestCaseList = []
			if(scriptGrpInstance){
				scriptGrpInstance?.scriptList?.each{ script->
					def scriptFileInstance  = ScriptFile.findByScriptName(script?.toString())
					def scriptDetails = scriptService.getScript(realPath,scriptFileInstance?.moduleName?.toString(),script?.toString(),params.category)
					def testCase =  scriptDetails?.testCaseDetails
					if(testCase){					
						testCaseMap =  getTestCaseMap(testCase)
					}
					if(totalTestCaseMap.containsKey(scriptFileInstance?.moduleName) ) {
						// append the test cases in same module
						if(testCaseMap?.get(TC_SCRIPT)){
							moduleTestCaseList =  totalTestCaseMap?.get(scriptFileInstance?.moduleName)
							moduleTestCaseList?.add(testCaseMap)
							totalTestCaseMap?.put(scriptFileInstance?.moduleName?.toString(),moduleTestCaseList)
						}
						moduleTestCaseList = []
					}else {	// Add test case with single script details in a module
						if(testCaseMap?.get(TC_SCRIPT)){
							moduleTestCaseList?.add(testCaseMap)
						}
						if(moduleTestCaseList?.size() > 0){ // for avoid blank page
							totalTestCaseMap?.put(scriptFileInstance?.moduleName?.toString(),moduleTestCaseList)
						}
						moduleTestCaseList = []
					}
					testCaseMap = [:]
				}
			}
		}catch(Exception e){
			println "ERROR"+e.getMessage()
		}
		return totalTestCaseMap
	}
	/**
	 * Function used to downloading total test case doc for module
	 */
	def downloadModuleTestCaseInExcel(def params , def realPath){
		def totalTestCaseMap = [:]
		try{
			def testCaseMap = [:]
			def moduleTestCaseList = []			
			def scriptDirName = primitiveService.getScriptDirName(params?.moduleName)
			[TEST_SCRIPTS+params?.category, TEST_SCRIPTS+params?.category+'Advanced'].each{ dirName ->
			def moduleDir =  realPath+Constants.FILE_SEPARATOR+FILESTORE+Constants.FILE_SEPARATOR+dirName+FILE_SEPARATOR+scriptDirName+Constants.FILE_SEPARATOR+params?.moduleName
			def files = scriptService?.getFileList(moduleDir)
			files?.each { file ->
				if(file != null) {
					def scriptDetails = scriptService.getScript(realPath,params?.moduleName,file,params.category)
					def testCase =  scriptDetails?.testCaseDetails
					if(testCase){					
						testCaseMap =  getTestCaseMap(testCase)
						if(testCaseMap?.get(TC_SCRIPT)){
							moduleTestCaseList?.add(testCaseMap)
						}
					}
				}
				testCaseMap = [:]
			}
			}
			if(moduleTestCaseList != [:]){
				totalTestCaseMap?.put(params?.moduleName, moduleTestCaseList)
			}			
		}catch(Exception e){
			println "ERROR "+ e.getMessage()
			e.printStackTrace()
		}
		return totalTestCaseMap
	}		
	/**
	 * Function for return the test case header values
	 * @return
	 */
	def testCaseKeyMap(){
		def testCaseHeaderList = []
		testCaseHeaderList.add(TC_SCRIPT)
		testCaseHeaderList.add(TC_ID)
		testCaseHeaderList.add(TC_OBJ)
		testCaseHeaderList.add(TC_TYPE)
		testCaseHeaderList.add(TC_SETUP)
		testCaseHeaderList.add(TC_PRE_REQUISITES)
		testCaseHeaderList.add(TC_INTERFACE)
		testCaseHeaderList.add(TC_IOPARAMS)
		testCaseHeaderList.add(TC_AUTOAPROCH)
		testCaseHeaderList.add(TC_EX_OUTPUT)
		testCaseHeaderList.add(TC_PRIORITY)
		testCaseHeaderList.add(TC_TSI)
		testCaseHeaderList.add(TC_SKIP)
		testCaseHeaderList.add(TC_RELEASE_VERSION)
		testCaseHeaderList.add(REMARKS)
		return testCaseHeaderList
	}
	
	def getTestCaseMap(def testCase){
		def testCaseMap  = [:]
		if(testCase){
			testCaseMap?.put(TC_SCRIPT,testCase?.testScript)
			testCaseMap?.put(TC_ID,testCase?.testCaseId)
			testCaseMap?.put(TC_OBJ,testCase?.testObjective)
			testCaseMap?.put(TC_TYPE,testCase?.testType)
			testCaseMap?.put(TC_SETUP,testCase?.testSetup)
			testCaseMap?.put(TC_PRE_REQUISITES, testCase?.preRequisites)
			testCaseMap?.put(TC_INTERFACE,testCase?.interfaceUsed)
			testCaseMap?.put(TC_IOPARAMS, testCase?.inputParameters)
			testCaseMap?.put(TC_AUTOAPROCH,testCase?.automationApproch)
			testCaseMap?.put(TC_EX_OUTPUT,testCase?.expectedOutput)
			testCaseMap?.put(TC_PRIORITY,testCase?.priority)
			testCaseMap?.put(TC_TSI,testCase?.testStubInterface)
			testCaseMap?.put(TC_SKIP,testCase?.tcskip)
			testCaseMap?.put(TC_RELEASE_VERSION,testCase?.releaseVersion)
			testCaseMap?.put(REMARKS,testCase?.remarks)
		}
		return testCaseMap
	}
	

}
