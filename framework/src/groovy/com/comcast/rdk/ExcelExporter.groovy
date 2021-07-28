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
import de.andreasschmitt.export.exporter.AbstractExporter
import de.andreasschmitt.export.exporter.Exporter;
import de.andreasschmitt.export.exporter.ExportingException;
import jxl.write.WritableHyperlink;
import jxl.write.WritableSheet
import jxl.write.WritableCell
import jxl.write.biff.CellValue
/**
 * Exporter for excel exporting of consolidated report.
 *
 */
class ExcelExporter extends AbstractExporter {

	@Override
	protected void exportData(OutputStream outputStream, List data, List fields)
	throws ExportingException {
		// TODO Auto-generated method stub

	}

	def exportData(OutputStream outputStream, Map dataMap){
		try {
			def builder = new ExcelBuilder()

			// Enable/Disable header output
			boolean isHeaderEnabled = true
			if(getParameters().containsKey("header.enabled")){
				isHeaderEnabled = getParameters().get("header.enabled")
			}


			def sheetsList = dataMap.keySet()
			builder {
				workbook(outputStream: outputStream){
					sheetsList.each { sheetName ->
						if(sheetName.equals("CoverPage")){
							Map coverPageMap = dataMap.get(sheetName)
							List columnWidthList = [0.05,0.05,0.05,0.05,0.08,0.4,0.15,0.2,0.2,0.2,0.2,0.2,0.4,0.15,0.15,0.15,0.2,0.2,0.2]
							sheet(name: "Summary" ?: "Export", widths: columnWidthList){
								int rowIndex = 0
								//Default format
								format(name: "header"){
									font(name: "arial", bold: true)
								}

								format(name: "titlecell"){
									font(name: "arial", bold: true)
								}
								
								format(name: "cell"){
									font(name: "arial", bold: false)
								}

								
								Set keySet = coverPageMap.keySet()
								if(keySet.size() > 0){
									def key = keySet.first()
									Map resultMap = coverPageMap.get("Details")
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex { field, index ->
										String label = getLabel(field)
										cell(row: rowIndex, column: 5, value: label, format: "header")
										String value = resultMap.get(field)
										cell(row: rowIndex, column: 5 +1, value: value, format: "cell")
										rowIndex ++
									}
									if(coverPageMap.containsKey(Constants.OVERALL_PASS_RATE)){
										int passRate = coverPageMap.get(Constants.OVERALL_PASS_RATE)
										String passRateString = passRate.toString()
										cell(row: rowIndex, column: 5, value: Constants.OVERALL_PASS_PERCENTAGE, format: "header")
										cell(row: rowIndex, column: 5 +1, value: passRateString, format: "cell")
										rowIndex ++
									}
								}
								
								for(int i = 0 ; i < 4 ; i ++ ){
									cell(row: rowIndex, column: 5 +1, value: "", format: "cell")
									rowIndex ++
								}
								
								if(keySet.size() > 0){
									Map resultMap = coverPageMap.get("Total")
									Set kSet = resultMap?.keySet()
									kSet?.eachWithIndex { field, index ->
										String value = getLabel(field)
										cell(row: rowIndex, column: 4+index, value: value, format: "header")
									}
								}
								

								keySet.eachWithIndex {  object, k ->
									if(!object.equals("Details") && !object.equals(Constants.OVERALL_PASS_RATE)){
									Map resultMap = coverPageMap.get(object)
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex {field, i ->
										Object value = resultMap.get(field)//getValue(object, field)
										String formatString = "cell"
										if(i == 1){
											formatString = "titlecell"
										}
										cell(row: k + rowIndex, column: 4+i, value: value , format :formatString)
									}

									}
								}

							}
						}else{
						int rowIndex = 1
							Map tabMap = dataMap.get(sheetName)
							if(tabMap != null){
								List data = tabMap?.get("dataList")
								List fields = tabMap?.get("fieldsList")
								if(data != null && fields != null){
									sheet(name: sheetName ?: "Export", widths: getParameters().get("column.widths")){
										//Default format
										format(name: "header"){
											font(name: "arial", bold: true)
										}

										format(name: "cell"){
											font(name: "arial", bold: false)
										}


										//Create header
										if(isHeaderEnabled){
											fields.eachWithIndex { field, index ->
												String value = getLabel(field)
												cell(row: rowIndex, column: index, value: value, format: "header")
											}

											rowIndex ++ 
										}

										//Rows
										data.eachWithIndex { object, k ->
											fields.eachWithIndex { field, i ->
												Object value = getValue(object, field)
												cell(row: k + rowIndex, column: i, value: value , format :"cell")
											}
										}
									}
								}
							}
						}
					}
					WritableSheet[] workbookSheets = workbook.getSheets()
					workbookSheets.each { eachSheet ->
						String sheetName = eachSheet.getName()
						if(sheetName.equals("Summary")){
							int i = 10
							while(1){
								WritableCell cell = eachSheet.getWritableCell(5,i)
								def contents = cell.getContents()
								if(contents.equals("Total")){
									break;
								}else{
									WritableSheet contentSheet = workbook.getSheet(contents)
									if(contentSheet){
										def link = new WritableHyperlink(5,i,"",contentSheet,0,0)
										link.setDescription(contents);
										eachSheet.addHyperlink(link);
									}
								}
								i++
							}
						}else{
							WritableSheet summarySheet = workbook.getSheet("Summary")
							if(summarySheet){
								eachSheet.mergeCells(0,0,5,0);
								def link = new WritableHyperlink(0,0,"",summarySheet,0,0)
								link.setDescription("Go to Summary");
								eachSheet.addHyperlink(link);
							}
						}
					}
				}
			}

			builder.write()
		}
		catch(Exception e){
			throw new ExportingException("Error during export", e)
		}
	}
	
	//@Override
	protected void exportScriptData(OutputStream outputStream)
	throws ExportingException {
		// TODO Auto-generated method stub

	}
	/**
	 * The function generate the  summary and module wise script list page.   
	 * @param outputStream
	 * @param dataMap
	 * @return
	 */
	
	def exportScriptData(OutputStream outputStream, Map dataMap){	
		try{
			def builder = new ExcelBuilder()
			boolean isHeaderEnabled = true
			if(getParameters().containsKey("header.enabled")){
				isHeaderEnabled = getParameters().get("header.enabled")
			}
			def sheetsList = dataMap.keySet()
			builder {
				workbook(outputStream: outputStream){
					sheetsList.each{   sheetName->
						//Summary page information 
						if(sheetName.equals("coverPage")){
							Map coverPageMap = dataMap.get(sheetName)
							List columnWidthList=[0.05,0.05,0.05,0.05,0.05,0.4,0.3,0.3]
							sheet(name: "Summary" ?: "Export", widths: columnWidthList){
								int rowIndex = 0
								//Default format
								format(name: "header"){
									font(name: "arial", bold: true)
								}
								format(name: "titlecell"){
									font(name: "arial", bold: true)
								}
								format(name: "cell"){
									font(name: "arial", bold: false)
								}
								Set keySet = coverPageMap.keySet()
								Map resultMap = coverPageMap.get("Details")
								Set kSet = resultMap.keySet()
								// Headings
								cell(row: rowIndex, column: 5, value: "Module Name", format: "header")
								cell(row: rowIndex, column: 5+1, value: "Category", format: "header")
								cell(row: rowIndex, column: 5+2, value: "Script Count", format: "header")
								rowIndex = 1
								int totalScriptCount = 0 ;
								int totalRDKVScriptCount  = 0 
								int totalRDKBScriptCount  = 0
								int totalTCLScriptCount = 0
								
								// Content 								
								kSet.eachWithIndex { field, index ->
									String label = getLabel(field)
									cell(row: rowIndex, column: 5, value: label, format: "cell")
									def moduleInstance = Module?.findByName(label)								
									String category
									String value = resultMap.get(field)
									
									if(moduleInstance){
										 category = moduleInstance?.category
										 if(category?.toString()?.equals("RDKV")){
											 totalRDKVScriptCount +=  Integer.parseInt(value)																					 
										 }else if (category?.toString()?.equals("RDKB")){
										 	totalRDKBScriptCount += Integer.parseInt(value)	 
										 }
									}else{									
										 category = "RDKB_TCL"
										 totalTCLScriptCount += Integer.parseInt(value)										
									}
									cell(row: rowIndex, column: 5+1, value: category, format: "cell")									
									totalScriptCount += Integer.parseInt(value)
									cell(row: rowIndex, column: 5+2, value: value, format: "cell")
									rowIndex ++
								}								
								// shows the total number of scripts count 							
								rowIndex++
								cell(row: rowIndex, column: 5+1, value: "Total RDKV  Script Count", format: "header")
								cell(row: rowIndex, column: 5+2, value: totalRDKVScriptCount?.toString() , format: "header")
								cell(row: rowIndex+1, column: 5+1, value: "Total RDKB Script Count", format: "header")
								cell(row: rowIndex+1, column: 5+2, value: totalRDKBScriptCount?.toString() , format: "header")
								cell(row: rowIndex+2, column: 5+1, value: "Total TCL Script Count", format: "header")
								cell(row: rowIndex+2, column: 5+2, value: totalTCLScriptCount?.toString() , format: "header")								
								cell(row: rowIndex+4, column: 5+1, value: "TOTAL SCRIPT COUNT", format: "header")
								cell(row: rowIndex+4, column: 5+2, value: totalScriptCount?.toString() , format: "header")
																
							}
						}else{  // Diffrent sheets
							int rowIndex = 1
							if(!sheetName.equals("CoverPage")){
								List columnWidthList=[0.6]
								//module wise script list iteration 
								sheet(name: sheetName ?: "Export", widths:columnWidthList ){
									format(name: "header"){
										font(name: "arial", bold: true)
									}
									format(name: "cell"){
										font(name: "arial", bold: false)
									}
									List data = dataMap?.get(sheetName)
									// shows script list including  scipt name
								//	cell(row: rowIndex, column: 0, value: "Sl No", format: "header")
									cell(row: rowIndex, column: 0, value: "Script Name", format: "header")
									rowIndex = 2	
								//	int scriptCount = 1							
									data?.each { script ->
										//cell(row: rowIndex, column: 0,  value:scriptCount?.toString(), format: "cell")
										cell(row: rowIndex, column: 0, value: script, format: "cell")
										//scriptCount++
										rowIndex++
									}
								}
							}
						}
					}
					WritableSheet[] workbookSheets = workbook.getSheets()
					workbookSheets.each { eachSheet ->
						String sheetName = eachSheet.getName()
						if(sheetName.equals("Summary")){
							int i = 1
							while(1){
								WritableCell cell = eachSheet.getWritableCell(5,i)
								def contents = cell.getContents()
								if(!contents || contents == ""){
									break;
								}else{
									WritableSheet contentSheet = workbook.getSheet(contents)
									if(contentSheet){
										def link = new WritableHyperlink(5,i,"",contentSheet,0,0)
										link.setDescription(contents);
										eachSheet.addHyperlink(link);
									}
								}
								i++
							}
						}else{
							WritableSheet summarySheet = workbook.getSheet("Summary")
							if(summarySheet){
								def link = new WritableHyperlink(0,0,"",summarySheet,0,0)
								link.setDescription("Go to Summary");
								eachSheet.addHyperlink(link);
							}
						}
					}
				}
			}
		builder.write()		
		}catch(Exception e){
			println "ERROR"+e.getMessage()
			e.printStackTrace()
		}
	}
	/**
	 * Function used to export test case data in script 
* @param scriptName 
	 * @param outputStream
	 * @param dataMap
	 * @return
	 */
	def exportTestCaseDoc(String scriptName, OutputStream outputStream, Map dataMap){
		try{
			def builder = new ExcelBuilder()
			boolean isHeaderEnabled = true			
			if(getParameters().containsKey("header.enabled")){
				isHeaderEnabled = getParameters().get("header.enabled")
			}
			builder{
				workbook(outputStream: outputStream){
					List columnWidthList=[0.4,0.3,0.4,0.2,0.2,0.3,0.8,0.6,0.9,0.8,0.2,0.6,0.2,0.3,0.2]
					sheet(name: "TEST_CASE_"+scriptName ?: "Export", widths: columnWidthList){
						
						format(name: "header"){
							font(name: "arial", bold: true)
						}
						format(name: "titlecell"){
							font(name: "arial", bold: true)
						}
						format(name: "cell"){
							font(name: "arial", bold: false)
						}
						int rowIndex = 0
						int coloumnIndex  = 0
						dataMap?.each{ k,v ->
							cell(row: rowIndex, column: coloumnIndex+0, value: k, format: "header")
							cell(row: rowIndex+1, column: coloumnIndex+0, value: v, format: "cell")
							coloumnIndex = coloumnIndex + 1
						}
					}
				}
			}
			builder.write()					
		}catch(Exception e){		
			println " ERROR "+e.printStackTrace()
		}
	}
	/**
	 * Function for exporting the test case doc corresponding to the suite
	 * @param suiteName
	 * @param outputStream
	 * @param dataMap
	 * @param testCaseKeyList
	 * @return
	 */
	def exportScriptGroupTestCase(String suiteName,OutputStream outputStream, Map dataMap , List testCaseKeyList){
		try{
			def builder = new ExcelBuilder()
			boolean isHeaderEnabled = true
			if(getParameters().containsKey("header.enabled")){
				isHeaderEnabled = getParameters().get("header.enabled")
			}
			def sheetsList = dataMap.keySet() // For separate sheet name based on the module wise 
			builder{
				workbook(outputStream: outputStream){
					sheetsList.each{sheetName->
						def testCaseMap = dataMap?.get(sheetName)
						def scriptFileInstance =  ScriptFile?.findByScriptName(sheetName?.toString())
							List columnWidthList=[0.4,0.3,0.4,0.2,0.2,0.3,0.8,0.6,0.9,0.8,0.2,0.6,0.2,0.3,0.2]
						sheet(name: sheetName.toString() ?: "Export", widths: columnWidthList){
							format(name: "header"){
								font(name: "arial", bold: true)
							}
							format(name: "titlecell"){
								font(name: "arial", bold: true)
							}
							format(name: "cell"){
								font(name: "arial", bold: false)
							}
							int rowIndex = 0
							int coloumnIndex  = 0
							def totalValueList = []
							def valueItems = []
							//For separate test case value and key in different list
							if(testCaseMap  !=  []){
								testCaseMap?.each{ testCase->
									testCase?.each{ k,v->
										valueItems?.add(v)
									}
									totalValueList?.add(valueItems)
									valueItems = []
								}
								// Adding the test case header in a sheet
								testCaseKeyList?.each{
									cell(row: rowIndex, column: coloumnIndex+0, value: it, format: "header")
									coloumnIndex = coloumnIndex + 1
								}
								def rawCount = 1
								coloumnIndex = 0
								// Adding the list of test case  value by appending each row
								totalValueList?.each{
									it?.each{
										cell(row: rowIndex+rawCount, column: coloumnIndex+0, value: it, format: "cell")
										coloumnIndex = coloumnIndex + 1
									}
									rawCount = rawCount +1
									coloumnIndex = 0
								}
							}else{							
								testCaseKeyList?.each{
									cell(row: rowIndex, column: coloumnIndex+0, value: it, format: "header")
									coloumnIndex = coloumnIndex + 1									
								}							 	
							}
						}
					}
				}
			}
			builder?.write()
		}catch(Exception e){
			println "ERROR"+ e.getMessage()
			e.printStackTrace()
		}
	}
	/**
	 * Function to export comparison report in excel format
	 * @param outputStream
	 * @param dataMap
	 * @return
	 */
	def exportComparisonData(OutputStream outputStream, Map dataMap){
		try {
			def builder = new ExcelBuilder()

			// Enable/Disable header output
			boolean isHeaderEnabled = true
			if(getParameters().containsKey("header.enabled")){
				isHeaderEnabled = getParameters().get("header.enabled")
			}


			def sheetsList = dataMap.keySet()
			builder {
				workbook(outputStream: outputStream){
					sheetsList.each { sheetName ->
						if(sheetName.equals("CoverPage")){
							Map coverPageMap = dataMap.get(sheetName)
							List columnWidthList = [0.05,0.08,0.6,0.2,0.2,0.15,0.15,0.15,0.2,0.08,0.15,0.15,0.15,0.15,0.2,0.2,0.2]
							sheet(name: "Summary" ?: "Export", widths: columnWidthList){
								int rowIndex = 0
								//Default format
								format(name: "header"){
									font(name: "arial", bold: true)
								}

								format(name: "titlecell"){
									font(name: "arial", bold: true)
								}
								
								format(name: "cell"){
									font(name: "arial", bold: false)
								}

								
								Set keySet = coverPageMap.keySet()
								if(keySet.size() > 0){
									def key = keySet.first()
									Map resultMap = coverPageMap.get("Details")
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex { field, index ->
										String label = getLabel(field)
										cell(row: rowIndex, column: 2, value: label, format: "header")
										String value = resultMap.get(field)
										cell(row: rowIndex, column: 2 +1, value: value, format: "cell")
										rowIndex ++
									}
									if(coverPageMap.containsKey(Constants.OVERALL_PASS_RATE)){
										int passRate = coverPageMap.get(Constants.OVERALL_PASS_RATE)
										String passRateString = passRate.toString()
										cell(row: rowIndex, column: 2, value: Constants.OVERALL_PASS_PERCENTAGE, format: "header")
										cell(row: rowIndex, column: 2 +1, value: passRateString, format: "cell")
										rowIndex ++
									}
								}
								
								for(int i = 0 ; i < 4 ; i ++ ){
									cell(row: rowIndex, column: 5 +1, value: "", format: "cell")
									rowIndex ++
								}
								
								if(keySet.size() > 0){
									Map resultMap = coverPageMap.get("Labels")
									Set kSet = resultMap?.keySet()
									kSet?.eachWithIndex { field, index ->
										String value = getLabel(field)
										cell(row: rowIndex, column: 1+index, value: value, format: "header")
									}
								}
								

								keySet.eachWithIndex {  object, k ->
									if(!object.equals("Details") && !object.equals(Constants.OVERALL_PASS_RATE)){
									Map resultMap = coverPageMap.get(object)
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex {field, i ->
										Object value = resultMap.get(field)//getValue(object, field)
										String formatString = "cell"
										if(i == 1){
											formatString = "titlecell"
										}
										cell(row: k + rowIndex, column: 1+i, value: value , format :formatString)
									}

									}
								}

							}
						}else{
						int rowIndex = 0
							Map tabMap = dataMap.get(sheetName)
							if(tabMap != null){
								List data = tabMap?.get("dataList")
								List fields = tabMap?.get("fieldsList")
								if(data != null && fields != null){
									sheet(name: sheetName ?: "Export", widths: getParameters().get("column.widths")){
										//Default format
										format(name: "header"){
											font(name: "arial", bold: true)
										}

										format(name: "cell"){
											font(name: "arial", bold: false)
										}


										//Create header
										if(isHeaderEnabled){
											fields.eachWithIndex { field, index ->
												String value = getLabel(field)
												cell(row: rowIndex, column: index, value: value, format: "header")
											}

											rowIndex ++
										}

										//Rows
										data.eachWithIndex { object, k ->
											fields.eachWithIndex { field, i ->
												Object value = getValue(object, field)
												cell(row: k + rowIndex, column: i, value: value , format :"cell")
											}
										}
									}
								}
							}
						}
					}
				}
			}

			builder.write()
		}
		catch(Exception e){
			throw new ExportingException("Error during export", e)
		}
	}
	
	/**
	 * Function to export consolidated report for RDK service executions in excel format
	 * @param outputStream
	 * @param dataMap
	 * @return
	 */
	def exportRDKServiceData(OutputStream outputStream, Map dataMap){
		try {
			def builder = new ExcelBuilder()
			boolean isHeaderEnabled = true
			if(getParameters().containsKey("header.enabled")){
				isHeaderEnabled = getParameters().get("header.enabled")
			}


			def sheetsList = dataMap.keySet()
			builder {
				workbook(outputStream: outputStream){
					sheetsList.each { sheetName ->
						if(sheetName.equals("CoverPage")){
							Map coverPageMap = dataMap.get(sheetName)
							List columnWidthList = [0.05,0.05,0.05,0.05,0.08,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.15,0.15,0.15,0.15,0.2,0.2,0.2]
							sheet(name: "Summary" ?: "Export", widths: columnWidthList){
								int rowIndex = 0
								//Default format
								format(name: "header"){
									font(name: "arial", bold: true)
								}

								format(name: "titlecell"){
									font(name: "arial", bold: true)
								}
								
								format(name: "cell"){
									font(name: "arial", bold: false)
								}

								
								Set keySet = coverPageMap.keySet()
								if(keySet.size() > 0){
									def key = keySet.first()
									Map resultMap = coverPageMap.get("Details")
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex { field, index ->
										String label = getLabel(field)
										cell(row: rowIndex, column: 5, value: label, format: "header")
										String value = resultMap.get(field)
										cell(row: rowIndex, column: 5 +1, value: value, format: "cell")
										rowIndex ++
									}
									if(coverPageMap.containsKey(Constants.OVERALL_PASS_RATE)){
										int passRate = coverPageMap.get(Constants.OVERALL_PASS_RATE)
										String passRateString = passRate.toString()
										cell(row: rowIndex, column: 5, value: Constants.OVERALL_PASS_PERCENTAGE, format: "header")
										cell(row: rowIndex, column: 5 +1, value: passRateString, format: "cell")
										rowIndex ++
									}
								}
								
								for(int i = 0 ; i < 4 ; i ++ ){
									cell(row: rowIndex, column: 5 +1, value: "", format: "cell")
									rowIndex ++
								}
								
								if(keySet.size() > 0){
									Map resultMap = coverPageMap.get("Total")
									Set kSet = resultMap?.keySet()
									kSet?.eachWithIndex { field, index ->
										String value = getLabel(field)
										cell(row: rowIndex, column: 4+index, value: value, format: "header")
									}
								}
								

								keySet.eachWithIndex {  object, k ->
									if(!object.equals("Details") && !object.equals(Constants.OVERALL_PASS_RATE)){
									Map resultMap = coverPageMap.get(object)
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex {field, i ->
										Object value = resultMap.get(field)//getValue(object, field)
										String formatString = "cell"
										if(i == 1){
											formatString = "titlecell"
										}
										cell(row: k + rowIndex, column: 4+i, value: value , format :formatString)
									}

									}
								}
							}
						}else if(sheetName.equals("rdkservices")){
							int rowIndex = 1
							Map tabMap = dataMap.get(sheetName)
							if(tabMap != null){
								List data = tabMap?.get("rdkserviceScripts")
								List fields = tabMap?.get("fieldsList")
								if(!(data.isEmpty()) && fields != null){
									sheet(name: sheetName ?: "Export", widths: getParameters().get("column.widths")){
										format(name: "header"){
											font(name: "arial", bold: true)
										}

										format(name: "cell"){
											font(name: "arial", bold: false)
										}


										//Create header
										cell(row: rowIndex, column: 0, value: "Sl No", format: "header")
										cell(row: rowIndex, column: 1, value: "Script Name", format: "header")
										cell(row: rowIndex, column: 2, value: "Status", format: "header")
										cell(row: rowIndex, column: 3, value: "Executed On", format: "header")
										cell(row: rowIndex, column: 4, value: "Log Data", format: "header")
										cell(row: rowIndex, column: 5, value: "Jira #", format: "header")
										cell(row: rowIndex, column: 6, value: "Issue Type", format: "header")
										cell(row: rowIndex, column: 7, value: "Remarks", format: "header")
										rowIndex ++

										//Rows
										data.eachWithIndex { object, k ->
											fields.eachWithIndex { field, i ->
												Object value = getValue(object, field)
												cell(row: k + rowIndex, column: i, value: value , format :"cell")
											}
										}
									}
								}
							}
						}else{
						int rowIndex = 1
							Map tabMap = dataMap.get(sheetName)
							if(tabMap != null){
								List data = tabMap?.get("dataList")
								List preRequisiteList = tabMap?.get("preRequisiteList")
								List postRequisiteList = tabMap?.get("postRequisiteList")
								String logLink = tabMap?.get("logLink")
								List fields = tabMap?.get("fieldsList")
								if(data != null && fields != null){
									sheet(name: sheetName ?: "Export", widths: getParameters().get("column.widths")){
										//Default format
										format(name: "header"){
											font(name: "arial", bold: true)
										}

										format(name: "cell"){
											font(name: "arial", bold: false)
										}

										cell(row: rowIndex, column: 0, value: "Sl No", format: "header")
										cell(row: rowIndex, column: 1, value: "Pre-Requisite Name", format: "header")
										cell(row: rowIndex, column: 2, value: "Status", format: "header")
										cell(row: rowIndex, column: 3, value: "Executed On", format: "header")
										cell(row: rowIndex, column: 4, value: "Log Data", format: "header")
										cell(row: rowIndex, column: 5, value: "Jira #", format: "header")
										cell(row: rowIndex, column: 6, value: "Issue Type", format: "header")
										cell(row: rowIndex, column: 7, value: "Remarks", format: "header")
										rowIndex ++
										
										preRequisiteList.eachWithIndex { object, k ->
											fields.eachWithIndex { field, i ->
												Object value = getValue(object, field)
												cell(row: rowIndex, column: i, value: value , format :"cell")
											}
											rowIndex ++
										}
										
										rowIndex ++
										//Create header
										if(!(data.isEmpty())){
											if(isHeaderEnabled){
												fields.eachWithIndex { field, index ->
													String value = getLabel(field)
													cell(row: rowIndex, column: index, value: value, format: "header")
												}
												rowIndex ++
											}
	
											//Rows
											data.eachWithIndex { object, k ->
												fields.eachWithIndex { field, i ->
													Object value = getValue(object, field)
													cell(row: rowIndex, column: i, value: value , format :"cell")
												}
												rowIndex ++
											}
											rowIndex ++
										}
										if(!(postRequisiteList.isEmpty())){
											cell(row: rowIndex, column: 0, value: "Sl No", format: "header")
											cell(row: rowIndex, column: 1, value: "Post-Requisite Name", format: "header")
											cell(row: rowIndex, column: 2, value: "Status", format: "header")
											cell(row: rowIndex, column: 3, value: "Executed On", format: "header")
											cell(row: rowIndex, column: 4, value: "Log Data", format: "header")
											cell(row: rowIndex, column: 5, value: "Jira #", format: "header")
											cell(row: rowIndex, column: 6, value: "Issue Type", format: "header")
											cell(row: rowIndex, column: 7, value: "Remarks", format: "header")
											rowIndex ++
											
											postRequisiteList.eachWithIndex { object, k ->
												fields.eachWithIndex { field, i ->	
													Object value = getValue(object, field)
													cell(row: rowIndex, column: i, value: value , format :"cell")
												}
												rowIndex ++
											}
											rowIndex ++
										}
										rowIndex ++
										cell(row: rowIndex, column: 0, value: "Log Link" , format :"header")
										cell(row: rowIndex, column: 1, value: logLink , format :"cell")
									}
								}
							}
						}
					}
					WritableSheet[] workbookSheets = workbook.getSheets()
					workbookSheets.each { eachSheet ->
						String sheetName = eachSheet.getName()
						if(sheetName.equals("Summary")){
							int i = 10
							while(1){
								WritableCell cell = eachSheet.getWritableCell(5,i)
								def contents = cell.getContents()
								if(contents.equals("Total")){
									break;
								}else{
									WritableSheet contentSheet = workbook.getSheet(contents)
									if(contentSheet){
										def link = new WritableHyperlink(5,i,"",contentSheet,0,0)
										link.setDescription(contents);
										eachSheet.addHyperlink(link);
									}
								}
								i++
							}
						}else{
							WritableSheet summarySheet = workbook.getSheet("Summary")
							if(summarySheet){
								eachSheet.mergeCells(0,0,4,0);
								def link = new WritableHyperlink(0,0,"",summarySheet,0,0)
								link.setDescription("Go to Summary");
								eachSheet.addHyperlink(link);
							}
						}
					}
				}
			}

			builder.write()
		}
		catch(Exception e){
			throw new ExportingException("Error during export", e)
		}
	}
}
