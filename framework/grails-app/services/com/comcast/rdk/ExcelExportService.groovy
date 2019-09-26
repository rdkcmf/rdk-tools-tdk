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

import java.io.OutputStream;
import java.util.List;
import java.util.Map;

import de.andreasschmitt.export.builder.ExcelBuilder
import de.andreasschmitt.export.exporter.Exporter
import de.andreasschmitt.export.exporter.ExportingException

/**
 * Service to export the excel report.
 *
 */
class ExcelExportService {

	def serviceMethod() {
	}
	
	public void export(String type, OutputStream outputStream, Map dataMap, List fields, Map labels, Map formatters, Map parameters) throws ExportingException {
		ExcelExporter exporter = new ExcelExporter()
//		if(fields){
//			exporter.setExportFields(fields)
//		}
//
		if(labels){
			exporter.setLabels(labels)
		}
//
//		if(formatters){
//			exporter.setFormatters(formatters)
//		}
//
		if(parameters){
			exporter.setParameters(parameters)
		}

		exporter.exportData(outputStream, dataMap)
	}
	
	
	
	
	/**
  	 *  Function used to export the  
	 * @param type
	 * @param outputStream
	 * @param dataMap
	 * @throws ExportingException
	 */
	
	public void exportScript(String type, OutputStream outputStream, Map dataMap)throws ExportingException{
		ExcelExporter exporter = new ExcelExporter()
		exporter.exportScriptData(outputStream, dataMap)	
	}
	/**
	 * Function used to export the test case in a script 
	 * @param scriptName
	 * @param outputStream
	 * @param dataMap
	 * @throws ExportingException
	 */
	public void exportTestCase(String  scriptName , OutputStream outputStream, Map dataMap)throws ExportingException{
		ExcelExporter exporter = new ExcelExporter()
		exporter?.exportTestCaseDoc(scriptName ,outputStream ,dataMap)
		
	}
	/**
	 * Function for export the script group test cases
	 * @param suiteName
	 * @param outputStream
	 * @param dataMap
	 * @param testCaseKeyList
	 * @throws ExportingException
	 */
	public void exportTestSuiteTestCase(String suiteName ,OutputStream outputStream, Map dataMap,List testCaseKeyList)throws ExportingException{
		ExcelExporter exporter = new ExcelExporter()	
		exporter?.exportScriptGroupTestCase(suiteName ,outputStream ,dataMap, testCaseKeyList)
	}
	
	
	
	
	
}
