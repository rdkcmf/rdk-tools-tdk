/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
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


/**
 * Service class for Thunder scripts
 *
 */
class ThunderScriptService {
	/**
	 * Method to save Thunder Script File
	 * @param fileName
	 */
	def saveThunderScriptFile (final String fileName) {
		ScriptFile.withTransaction {
		   def 	scriptFile  = ScriptFile.findByScriptNameAndCategory(fileName, Category.RDKV_THUNDER)
			if(scriptFile == null) {
				def scriptFile1 = new ScriptFile()
				scriptFile1?.scriptName =fileName?.toString()
				scriptFile1?.category = Category.RDKV_THUNDER
				scriptFile1?.moduleName = Constants.THUNDER
				if(!(scriptFile1.save(flush:true))){
					println("Error while saving thunder script file")
				}
			}
		}
	}
	
	def saveRdkServiceThunderScriptFile(final String fileName, final String folder) {
		ScriptFile.withTransaction {
			def scriptFile  = ScriptFile.findByScriptNameAndCategory(fileName, Category.RDKV_RDKSERVICE)
			 if(scriptFile == null) {
				 def scriptFile1 = new ScriptFile()
				 scriptFile1?.scriptName =fileName?.toString()
				 scriptFile1?.category = Category.RDKV_RDKSERVICE
				 scriptFile1?.moduleName = folder
				 if(!(scriptFile1.save(flush:true))){
					println("Error while saving rdkservice script file")
				 }
			 }
		 }
	}
	
}
