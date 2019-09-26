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

import org.springframework.util.StringUtils;

import static com.comcast.rdk.Constants.*;

import com.comcast.rdk.Category

public class Utility{

	public static Category getCategory(def category){
		if(StringUtils.hasText(category)){
			return Category.valueOf(category)
		}
		return null
	}

	public static void writeContentToFile(String content, String fileName){
		
		File fileObj = new File(fileName);
		fileObj?.getParentFile()?.mkdirs();
		
		BufferedWriter writer = new BufferedWriter(new FileWriter(new File(fileName)))
		writer.write(content)
		writer.close()
	}

	public static String getTclDir(final String realPath) {
		return realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value();
	}

	/**
	 * Method to check whether a script is part of advanced scripts.
	 */
	public static boolean isAdvancedScript(def fileName, def moduleName ){
		boolean isAdv = false
		try {
			ScriptFile sFile
			ScriptFile.withTransaction {
				sFile = ScriptFile.findByScriptNameAndModuleName(fileName,moduleName)
			}

			String filePath = ScriptService.scriptsListAdvanced.get(sFile?.id)
			isAdv = (filePath?.equals(TESTSCRIPTS_RDKV_ADV) || filePath?.equals(TESTSCRIPTS_RDKB_ADV) )
		} catch (Exception e) {
			e.printStackTrace()
		}
		return isAdv
	}
	
	/**
	 * Method to get the file store path for a script.
	 */
	public static String getFileStorePath(final String realPath, final Category category,String moduleName, String fileName){
		String path = realPath + FILE_SEPARATOR + FILESTORE + FILE_SEPARATOR
		boolean isAdvanced = isAdvancedScript(fileName, moduleName)
		switch(category){
			case Category.RDKB: 
				if(isAdvanced){
					path = path + FileStorePath.RDKBADVANCED.value()
				}else{
					path = path + FileStorePath.RDKB.value()
				}
				break
			case Category.RDKV : 
				if(isAdvanced){
					path = path + FileStorePath.RDKVADVANCED.value()
				}else{
					path = path + FileStorePath.RDKV.value()
				}
				break
			case Category.RDKB_TCL : 
				path = path + FileStorePath.RDKTCL.value()
				break
			default:break
		}
		return path
	}
	
	public static String getPrimitiveFileStorePath(final String realPath, final Category category){
		String path = realPath + FILE_SEPARATOR + 'fileStore' + FILE_SEPARATOR
		switch(category){
			case Category.RDKB: path = path + FileStorePath.RDKB.value()
				break
			case Category.RDKV : path = path + FileStorePath.RDKV.value()
				break
			case Category.RDKB_TCL : path = path + FileStorePath.RDKTCL.value()
				break
			default:break
		}
		return path
	}
	
	/**
	 * Method evaluates whether the text returned from tcl execution represents failure
	 * 
	 * @param htmlData
	 * @return
	 */
	public static boolean isFail(String htmlData){
		return (htmlData.contains('Test Result : FAILED') ||  !htmlData.contains('Test Result :'))
	}
	
	/***
	 * Checks whether tcl file exists in filestore
	 * 
	 * @param realPath
	 * @param fileName
	 * @return
	 */
	public static boolean isTclScriptExists(String realPath, String fileName){
		def isExists = false
		def tcl = getTclFilePath(realPath, fileName)
		if(tcl){
			isExists = true
		}
		return isExists
	}
	
	
	/***
	 * Gets the tcl file absolute path from filestore
	 * 
	 * @author deepesh.mohan
	 *
	 */
	public static String getTclFilePath(String realPath, String fileName){
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(fileName+".tcl")
					};
				})
		if(tcl?.length == 1){
			return tcl[0]?.absolutePath
		}
		return null
	}
	
	
	/**
	 * Returns the tcl scripts path in filestore
	 * 
	 * @param realPath
	 * @return
	 */
	public static String  getTclDirectory(String realPath) {
		return realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
	}

	/**
	 * Checks whether the COnfiguration file for tcl execution exists in filestore
	 * 
	 * @author deepesh.mohan
	 *
	 */
	public static boolean isConfigFileExists(def realPath, def deviceName){
		def isExists = false
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(deviceName+".txt")
					};
				})
		if(tcl.length == 1){
			isExists = true
		}
		return isExists
	}
	
	/***
	 * Returns config file path from tcl filestore
	 * @author deepesh.mohan
	 *
	 */
	public static String getConfigFilePath(String realPath, String deviceName){
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(deviceName+".txt")
					};
				})
		if(tcl.length == 1){
			return tcl[0]?.absolutePath
		}
		return null
	}
	
	
	public static String getModuleParentDirectory(TestGroup testgroup){
		def dir = null
		if(testgroup){
			switch(testgroup){
				case TestGroup.E2E : dir = Constants.INTEGRATION
					break
				case TestGroup.Component : dir = Constants.COMPONENT
					break
				/*
				 *  not implemented
				 case TestGroup.OpenSource : dir = Constants.COMPONENT
				 break*/
				default : dir = null
					break
			}
		}
		return dir
	}
}
