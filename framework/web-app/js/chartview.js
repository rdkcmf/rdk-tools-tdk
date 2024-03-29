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
var listTest =[];
var startIndex = 0 ;
var endIndex = 8  ; 
var maxSize = -1;
var previousCount = 0;
var nextCount = 0 ;

$(document).ready(function() {
	/**
	 * Change the boxtype dropdown according to the category selected for base execution
	 */
	$("#categoryIdBaseExec").live('change', function(){
		var category_id = $(this).val();
		if(category_id != '') {
			getBoxTypes(category_id);
		}
		else {
			$("#boxTypeIdBaseExec").html('<select><option value="">Please Select</option></select>');
		}
	});
	
	/**
	 * Change the boxtype dropdown according to the category selected for comparison execution
	 */
	$("#categoryIdComparisonExec").live('change', function(){
		var category_id = $(this).val();
		if(category_id != '') {
			getBoxTypesForComparison(category_id);
		}
		else {
			$("#boxTypeIdComparisonExec").html('<select><option value="">Please Select</option></select>');
		}
	});
	
	/**
	 * Change the script name dropdown according to the execution selected for plotting cpu memory graph
	 */
	$("#rdkServiceExecutionId").live('change', function(){
		var execution_name = $(this).val();
		if(execution_name != '') {
			getScriptsByExecution(execution_name)
		}
		else {
			$("#rdkServiceScriptId").html('<select style="width:300px"><option value="">Please Select</option></select>');
		}
	});
	
	$("#benchMarkPerformanceTypeList").live('change', function(){
		var benchMarkScript = $(this).val();
		if(benchMarkScript != '') {
			getProcessTypeOfScript(benchMarkScript)
		}
		else {
			$("#parameterId").html(''); 
			$("#analyzeExecution").hide();	
			$("#benchmarkData").hide();	
			$("#messageDiv").hide();	
		}
	});
});

/**
 * Function to get the box types according to category and fill it in the boxtype dropdown of base execution
 * @param category_id
 */
function getBoxTypes(category_id) {
	var url = $("#url").val();
	if(category_id != '') {
		$.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
			var select = '<select id="boxTypeBaseExec" name="boxTypeBaseExec"><option value="">Please Select</option>';
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
			}
			select += '</select>';
			$("#boxTypeIdBaseExec").html(''); 
			$("#boxTypeIdBaseExec").html(select); 
		});
	}
	else {
		$("#boxTypeIdBaseExec").html('');
	}
}

/**
 * Function to get the box types according to category and fill it in the boxtype dropdown of comparison executions
 * @param category_id
 */
function getBoxTypesForComparison(category_id) {
	var url = $("#url").val();
	if(category_id != '') {
		$.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
			var select = '<select id="boxTypeComparisonExec" name="boxTypeComparisonExec"><option value="">Please Select</option>';
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
			}
			select += '</select>';
			$("#boxTypeIdComparisonExec").html(''); 
			$("#boxTypeIdComparisonExec").html(select); 
		});
	}
	else {
		$("#boxTypeIdComparisonExec").html('');
	}
}

/**
 * Compare the result by execution name 
 */
function showChart(){	
	var checked_radio1 = $('input:radio[name=ChartType]:checked').val();
	if(checked_radio1 != undefined  ){
		if(checked_radio1 == "BarChart" ){
			$("#previous").hide();
			$("#next").hide();	
			showBarChart();	

		}else if(checked_radio1 == "LineChart" ){
			showLineChart();	 
		}
	}

}
	
/**
 * Compare result by device details 
 */
function showChart1(){	
		
	
	var checked_radio1 = $('input:radio[name=ChartType1]:checked').val();
	if(checked_radio1 != undefined  ){
		if(checked_radio1 == "BarChart" ){
			$("#previous").hide();
			$("#next").hide();	
			$("#previous1").hide();
			$("#next1").hide();	
			showBarChart();	
		}else if(checked_radio1 == "LineChart" ){
			showLineChart();	 
		}
	}
}

/**
 * Function for hide buttons (home,next, previous buttons)  
 */
function hideOptions(){
	$("#previous").hide();
	$("#next").hide();	
	$("#previous1").hide();
	$("#next1").hide();	
	$("#home").hide();
	$("#home1").hide();	
}


/**
 *Function to show status bar chart based module pass %
 */
function showStatusBarChart(data, barColors) {

	$("#showChart").hide();
	$("#hideChart").show();	
	$("#bar-chart").show();

	var plot3 = $.jqplot('bar-chart', [ data ], {
		title : 'Modulewise Pass%',
		seriesColors : barColors,
		seriesDefaults : {
			renderer : $.jqplot.BarRenderer,
			pointLabels : {
				show : true
			},
			rendererOptions : {
				varyBarColor : true,
				barWidth : 15
			}
		},
		axes : {
			xaxis : {
				renderer : $.jqplot.CategoryAxisRenderer,
				labelOptions : {
					fontSize : '10pt'
				},
				tickOptions : {
					angle : -20
				},
				tickRenderer:$.jqplot.CanvasAxisTickRenderer
			},
			yaxis : {
				max : 100,
				min : 0,
				label : 'Pass%',
				labelOptions : {
					fontSize : '10pt',
					angle: -90
				},
				labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
			}
		}
	});
}

/**
 *Function to hide chart
 */
function hideChart(){
	$("#showChart").show();
	$("#hideChart").hide();	
	$("#bar-chart").hide();	
}

/**
 * Function for setting colour for bar
 */

function setColor (resultList )
{
	var colors = [] ;
	var threshold = 1;
	$.each(resultList , function(index, value){
        if(value > threshold)
          colors.push("green");
        else
          colors.push("red");
	});
    return colors
}
/**
 * Function for setting colour for bar
 */
function setGroupColor (resultList )
{
	var colors = [] ;
	$.each(resultList , function(index, value){
        if(value <= 50)
          colors.push("#f63c0a");
        else if(value >50 && value <80 )
          colors.push("#f19e0e");
	   else if(value >=80 && value <100 )
          colors.push("#67e84d");
	   else
		colors.push("#10bf4d");
	});
    return colors
}

/**
 * Function for getting module wise chart based on execution name
 */
function showNormalExecutionChart(){
		
		$( ".chartdivBoxtypeclass" ).empty();
		$(".chartdivclass").empty();
		$(".chartdivScriptclass").empty();
		$( ".chartdivisionclass" ).empty();
		$(".chartdivisionbuildclass").empty();
		$( ".chartdivBuildScriptclass" ).empty();
		var id = $("#normalexecname").val();
		hideOptions();
		if(id == "")
		{ alert ('Please select an Execution Name');}
		else{
			var colors = [] ;
			$.get('showNormalExecutionChart', {executionname : id}, function(data) {	
					if(data.resultList.length  == 0  ){
						alert(" No results to show");
					}else{	
						var labels = ["Result Status"]
						function tooltipContentEditor(str, seriesIndex, pointIndex, plot) {
								return data.image
						}
						colors = setGroupColor( data.resultList  )	;
						plot2 = $.jqplot('chartdivision', [data.resultList ] , {
							title:  "<b>" + " Execution Results of " + id +"</b>",
							seriesColors:colors,
							animate: true,
							animateReplot: true,
							seriesDefaults: {
								renderer:$.jqplot.BarRenderer,
								rendererOptions: {
									barWidth: 25,
									varyBarColor : true,
	
									animation: {
										speed: 2500
									},	
								},
								pointLabels: { show: true }
							},
							axes: {
								xaxis: {
									renderer: $.jqplot.CategoryAxisRenderer,
									label:'Module Name',		                
									ticks: data.moduleName ,
									tickOptions:{
										angle: -20
									},
									tickRenderer:$.jqplot.CanvasAxisTickRenderer
								},
	
								yaxis: {
									labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
									min:0,
									max: 100, 
									numberTicks: 11,
									label:'Pass Percentage'
								}
							},
							highlighter:{
									show:true,
									sizeAdjust:20,
									tooltipContentEditor:tooltipContentEditor
								},

							cursor: {
									show: false
							}
					});
				}
			}	);
		}	
}

function getKeyValueList(mapString) {
	var mapObject = mapString.replace("{", "");
	mapObject = mapObject.replace("}", ""); 
	var listObjects = mapObject.split(",");
	var mapEntry = null;
	var keyValueList = [[]];
	if(listObjects != null && listObjects != undefined) {	
		for(var i=0; i< listObjects.length; i++) {
			mapEntry = listObjects[i].split("=");
			if(mapEntry != null && mapEntry.length == 2) {
                var entry = [mapEntry[0].trim(),parseInt(mapEntry[1])]
                keyValueList[[i][0]] = entry;
			}
		}
	}
	return keyValueList;
}


/*
 * Function for getting the script based success/failure result 
 */
function getScriptBasedChartData() {
	script = $('#scriptname').val();
	boxTypeId = $('#boxType').val();
	var resultcount = 5;
	$('#scriptBasedChart').empty();
	$('#scriptBasedChart').show();
	var statusMap = $('#statusList').val();
	chartData = getKeyValueList(statusMap);	
	if(chartData.length  == 0  ){
		alert("No results to show");
	} else {		
		var labels = ["Result Status"]	
		var plot2 = $.jqplot ('scriptBasedChart', [chartData], 
				        { 
				            seriesDefaults: {
				               // Make this a pie chart.
				               renderer: jQuery.jqplot.PieRenderer, 
				               rendererOptions: {
				                    // Put data labels on the pie slices.
				                    // By default, labels show the percentage of the slice.
				                    showDataLabels: true
				                    
				               }, 
				               seriesColors :["#F24264", "#189327", "#2097FA", "#6D6D64", "#AE93C4", "#C1C6C5", "#835969"]
				                              //FAILURE, SUCCESS, IN_PROGRESS, SKIPPED, PENDING, N/A, SCRIPT_TIME_OUT 
				            }, 
				            legend: { show:true, location: 'e' }
				        }
				    );
	}
}

/**
 * Function for getting Script Group chart based on box type
 */
function showBoxTypeScriptGroupChart(){

		
		$( ".chartdivBoxtypeclass" ).empty();
		$(".chartdivclass").empty();
		$(".chartdivScriptclass").empty();
		$( ".chartdivisionclass" ).empty();
		$(".chartdivisionbuildclass").empty();
		$( ".chartdivBuildScriptclass" ).empty();
		var status = ["Failure", "Success"];
		var id = $("#boxtype").val();
		hideOptions();
		var scriptgroup = $("#scriptgroupsname").val();
		var resultcount = $("#resultGroupCounts").val();	
		if(scriptgroup == null || scriptgroup.length == 0 )
			{ alert ('please select a script group ');}
		else if(id == "")
			{ alert ('Please select a Box Type');}
		else{
			var colors = [] ;
			$.get('showBoxTypeScriptGroupChart', {boxTypeId : id, scriptgroup : scriptgroup, resultCnt : resultcount} , function(data) {	
					if(data.resultList.length  == 0  ){
						alert(" No results to show");
					}else{	
						var labels = ["Result Status"]
						colors = setGroupColor( data.resultList  )	;
						function tooltipContentEditor(str, seriesIndex, pointIndex, plot) {
								return data.imageList[pointIndex]						
						}
						plot2 = $.jqplot('chartdivisions', [data.resultList ] , {
							title: "<b>" + data.resultList.length   +" Execution Results of " + scriptgroup + "</b>"  ,
							seriesColors:colors,
							animate: true,
							animateReplot: true,
							seriesDefaults: {
								renderer:$.jqplot.BarRenderer,
								rendererOptions: {
									barWidth: 25,
									varyBarColor : true,

									animation: {
										speed: 2500
									},	
								},
								pointLabels: { show: true }
							},
							axes: {
								xaxis: {
									renderer: $.jqplot.CategoryAxisRenderer,
									label:'Execution Name',		                
									ticks: data.executionName ,
									tickOptions:{
										angle: -20
									},
									tickRenderer:$.jqplot.CanvasAxisTickRenderer
								},

								yaxis: {
									labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
									min:0,
									max: 100, 
									numberTicks: 11,
									label:'Pass Percentage'
								}
							},
							highlighter:{
									show:true,
									sizeAdjust:20,
									tooltipContentEditor:tooltipContentEditor
								},

							cursor: {
									show: false
							}
						});
					}

			});
		}
}

/**
 * Function for getting Script  chart based on box type
 */
function getBoxTypeScriptChartData()
{
	
	$(".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivisionbuildclass").empty();
	$( ".chartdivBuildScriptclass" ).empty();
	var status = ["Failure", "Success"];
	var id = $("#boxtype").val();
	hideOptions();
	var script = $("#scriptname").val();
	var resultcount = $("#resultCounts").val();	
	if(script == null || script.length == 0 )
		{ alert ('please select a script ');}
	else if(id == "")
		{ alert ('Please select a Box Type');}
	else
	{
		var colors = [] ;
		$.get('getBoxTypeScriptChartData', {boxTypeId : id, script : script, resultCnt : resultcount} , function(data) {	
				if(data.resultList.length  == 0  ){
					alert(" No results to show");
				}else{	
					
					var labels = ["Result Status"]	
					colors = setColor( data.resultList  )
					function tooltipContentEditor(str, seriesIndex, pointIndex, plot) {
								return data.imageList[pointIndex]					
					}
					var plot2 = $.jqplot('chartdivBoxType1', [data.resultList ] , {
						title: "<b>" + data.resultList.length   +" Execution Results of " + script  + "</b>",
						seriesColors:colors,
						animate: true,
						animateReplot: true,
						series:[
								{
									showHighlight: true,
									yaxis: 'yaxis',
									rendererOptions: {
										
										animation: {
											speed: 2500
										},			                   
									}
								}, 
								{
									rendererOptions:{
										animation: {
											speed: 2000
										}
									}
								}
							   ],
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								
								barWidth: 25,
								varyBarColor : true,
								animation: {
									speed: 2500
								}	
							},
							pointLabels: { show: false }
						},

						 axes: {
								xaxis: {
										renderer: $.jqplot.CategoryAxisRenderer,
										label:'Execution Name',	
										min:0,
										ticks: data.executionName,
										tickOptions:{
											angle: -20
										},
										tickRenderer:$.jqplot.CanvasAxisTickRenderer
									},
								
								yaxis: {
										renderer: $.jqplot.CategoryAxisRenderer,
										label:'Status',
										min:0,
										max: data.yCount, 
										numberTicks: 11,
										ticks: status,
										tickRenderer:$.jqplot.CanvasAxisTickRenderer

									}
								},
						highlighter:{
									show:true,
									sizeAdjust:20,
									tooltipContentEditor:tooltipContentEditor
								},

							cursor: {
									show: false
							}	       
					});	
				 

			}
		} );
	}
}

/**
 * Function for getting Script  chart based on device
 */
function showScriptChart()
{	
	
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivisionbuildclass").empty();
	$( ".chartdivBuildScriptclass" ).empty();
	var labels = ["Result Status"];
	var status = ["Failure", "Success"];
	var id = $("#device").val();
	hideOptions();
	var colors = [];
	var script = $("#script").val();
	if(id == "")
		{ alert ('Please select a Device');}

	if(script == "" )
		{ alert ("please select a script ")}
	else{
		var resultcount = $("#resultcount").val();	
		$.get('getScriptChartData', {deviceId : id, script : script, resultCnt : resultcount} , function(data) {	
				if(data.resultList.length  == 0  ){
					alert(" No results to show");
				}else{	
					colors = setColor( data.resultList  )	
					function tooltipContentEditor(str, seriesIndex, pointIndex, plot) {
								return data.imageList[pointIndex]					
					}					
					var plot2 = $.jqplot('chartdivScript1', [data.resultList ] , {
						title: "<b>" + data.resultList.length   +" Execution Results of " + script + "</b>" ,

						seriesColors:colors,
						animate: true,
						animateReplot: true,
						series:[
								{
									showHighlight: true,
									yaxis: 'yaxis',
									rendererOptions: {
										animation: {
											speed: 2500
										},			                   
									}
								}, 
								{
									rendererOptions:{
										animation: {
											speed: 2000
										}
									}
								}
								],
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 25,
								varyBarColor : true,
								animation: {
									speed: 2500
								},	
							},
							pointLabels: { show: false }
						},

						axes: {
								   xaxis: {
										renderer: $.jqplot.CategoryAxisRenderer,
										label:'Execution Name',	
										min:0,
										ticks: data.executionName,
										tickOptions:{
											angle: -20
										},
										tickRenderer:$.jqplot.CanvasAxisTickRenderer
									},
		
									yaxis: {
										renderer: $.jqplot.CategoryAxisRenderer,
										label:'Status',
										min:0,
										max: data.yCount, 
										numberTicks: 11,
										ticks: status,
																		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		
									}
								},
						highlighter:{
									show:true,
									sizeAdjust:20,
									tooltipContentEditor:tooltipContentEditor
							},

						cursor: {
									show: false
								}				       
					});	
					 
				}
		} );
	}
}

/**
 * Function for getting Script  chart based on build name
 */ 
function getBuildScriptChartData()
{	
	
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivisionbuildclass").empty();
	$( ".chartdivBuildScriptclass" ).empty();
	var labels = ["Result Status"];
	var status = ["Failure", "Success"];
	hideOptions();
	var colors = [];
	var script = $("#buildscriptname").val();
	var buildName =  $("#buildname").val();
	if(script == "" )
		{ alert ("please select a script ")}
	if(script == "" )
		{ alert ("please select a build name  ")}
	else{
		var resultcount = $("#resultBuildCount").val();
		$.get('getBuildScriptChartData', {script : script, buildName : buildName, resultcount:resultcount} , function(data) {	
				if(data.resultList.length  == 0  ){
					alert(" No results to show");
				}
				else{	
					colors = setColor( data.resultList  )						
					var plot2 = $.jqplot('chartdivBuild1', [data.resultList ] , {
						title: "<b>" + data.resultList.length   +" Execution Results of " + script + " executed on " + buildName + "</b>" ,

						seriesColors:colors,
						animate: true,
						animateReplot: true,
						series:[
								{
									showHighlight: false,
									yaxis: 'yaxis',
									rendererOptions: {
										animation: {
											speed: 2500
										},			                   
									}
								}, 
								{
									rendererOptions:{
										animation: {
											speed: 2000
										}
									}
								}
								],
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 25,
								varyBarColor : true,
								animation: {
									speed: 2500
								},	
							},
							pointLabels: { show: false }
						},

						axes: {
								   xaxis: {
										renderer: $.jqplot.CategoryAxisRenderer,
										label:'Execution Name',	
										min:0,
										ticks: data.executionList,
										tickOptions:{
											angle: -20
										},
										tickRenderer:$.jqplot.CanvasAxisTickRenderer
									},
		
									yaxis: {
										renderer: $.jqplot.CategoryAxisRenderer,
										label:'Status',
										min:0,
										max: data.yCount, 
										numberTicks: 11,
										ticks: status,
																		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		
									}
								}
							   		       
					});	
					 
				}
		} );
	}
}

/**
 * Function for getting Script  chart based on build name
 */

function showBuildScriptGroupChart()
{	
	
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$( ".chartdivisionclass" ).empty();
	$( ".chartdivBuildScriptclass" ).empty();

	$(".chartdivisionbuildclass").empty();
	var labels = ["Result Status"];
	var status = ["Failure", "Success"];
	
	hideOptions();
	var colors = [];
	var scriptGroup = $("#buildscriptgroupsname").val();
	var buildName =  $("#buildname").val();
	if(scriptGroup == "" )
		{ alert ("please select a script group ")}
	
	else if(buildName == "" )
		{ alert ("please select a build name ")}
	else{
		var resultcount = $("#resultBuildCount").val();
		$.get('showBuildScriptGroupChart', {scriptGroup : scriptGroup, buildName : buildName, resultcount:resultcount} , function(data) {	
				if(data.resultList.length  == 0  ){
					alert(" No results to show");
				}
				else{	
				
				
				
				
					var labels = ["Result Status"]
						colors = setGroupColor( data.resultList  )	;
						
						
						plot2 = $.jqplot('chartdivisionsbuild', [data.resultList ] , {
							title: "<b>" + data.resultList.length   +" Execution Results of " + scriptGroup + "</b>"  ,
							seriesColors:colors,
							animate: true,
							animateReplot: true,
							seriesDefaults: {
								renderer:$.jqplot.BarRenderer,
								rendererOptions: {
									barWidth: 25,
									varyBarColor : true,

									animation: {
										speed: 2500
									},	
								},
								pointLabels: { show: true }
							},
							axes: {
								xaxis: {
									renderer: $.jqplot.CategoryAxisRenderer,
									label:'Execution Name',		                
									ticks: data.executionList ,
									tickOptions:{
										angle: -20
									},
									tickRenderer:$.jqplot.CanvasAxisTickRenderer
								},

								yaxis: {
									labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
									min:0,
									max: 100, 
									numberTicks: 11,
									label:'Pass Percentage'
								}
							}
						});		       
					
					 
				}
		} );
	}
}





/**
 * Plotting the bar chart  on the bases of the script group.
 */

function showBarChart(){	
	
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	var id = $("#devices").val();

	var scriptGroup = $("#scriptGrp").val();

	var resultcount = $("#resultCount").val();

	var ticks = ['1', '2', '3'];
	var labels = ["Success", "Failure", "Not Executed"];
	var labelsBenchMark = ["Execution Time(millisec)"];
	var labelsSd = ["CPU Utilization","Memory Utilization"];
	var labelsCPUSd = ["CPU Average Utilization","CPU Peak Utilization"];
	var labelsMemorySd = ["Memory Available Peak","Memory Used Peak"];
	var labelsMemoryPercSd = ["Memory Used Percentage Peak"];
	var chartType = null;
	var executionIds = $("#executionId").val();
	var executionIdList = null

	var checked_radio = $('input:radio[name=chartOptions]:checked').val();

	if(checked_radio!=undefined)
	{
		if(checked_radio=="DeviceBased"){
			executionIdList = "";
			chartType = $("#chartType").val();
		}
		else{
			executionIdList = executionIds.toString();		
			chartType = $("#chartType1").val();    
		}
	}
	
	// plotting the  graph for Execution Status  
	if(chartType == "ExecutionStatus"){
		hideOptions();
		$.get('getStatusChartData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{

				plot2 = $.jqplot('chartdiv', data.listdate, {
					seriesColors:['green', 'red', 'grey'],
					animate: true,
					animateReplot: true,
					seriesDefaults: {
						renderer:$.jqplot.BarRenderer,
						rendererOptions: {
							barWidth: 10,
							animation: {
								speed: 2500
							},	
						},
						pointLabels: { show: true }
					},
					legend: {
						show: true,
						placement: 'outsideGrid',
						labels: labels,
						location: 'ne',
						rowSpacing: '0px'
					},
					axes: {
						xaxis: {
							renderer: $.jqplot.CategoryAxisRenderer,
							label:'Execution Name',		                
							ticks: data.execName,
							tickOptions:{
								angle: -60
							},
							tickRenderer:$.jqplot.CanvasAxisTickRenderer
						},

						yaxis: {
							labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
							min:0,
							max: data.yCount, 
							numberTicks: 11,
							label:'Script Count'
						}
					}
				});
			}

		});
	}// Plotting  the  bar chart  for timing info 
	else if(chartType == "TimingInfo"){		
		$.get('getStatusBenchMarkData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				plot3 = $.jqplot('chartdiv', [data.benchmark], {
					animate: true,
					animateReplot: true,
					seriesDefaults: {
						renderer:$.jqplot.BarRenderer,
						pointLabels: { show: true },
						rendererOptions: {
							barWidth: 25,
							animation: {
								speed: 2500
							},	
						}
					},
					legend: {
						show: true,
						placement: 'outsideGrid',
						labels: labelsBenchMark,
						location: 'ne',
						rowSpacing: '0px'
					},		     
					axes: {
						xaxis: {
							renderer: $.jqplot.CategoryAxisRenderer,
							label:'Execution Name',
							ticks: data.execName,
							tickOptions:{
								angle: -60
							},
							tickRenderer:$.jqplot.CanvasAxisTickRenderer
						},
						yaxis: {
							labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
							label:'Time in milliseconds'
						}
					}
				});	
			}
		});	
	} //plotting the bar chart for " CPU-Utilization 
	else if(chartType == "CPU_Utilization"){			
		$.get('getStatusSystemDiagnosticsCPUData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				if(data.systemDiag == null || data.systemDiag == ""){
					alert("Performance data is not available with the selected script and device ");
				}
				else{
					plot3 = $.jqplot('chartdiv', data.systemDiag, {
						animate: true,
						animateReplot: true,
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 20,
								animation: {
									speed: 2500
								},	
							},
							pointLabels: { show: true }
						},
						legend: {
							show: true,
							placement: 'outsideGrid',
							labels: labelsCPUSd,
							location: 'ne',
							rowSpacing: '0px'
						},
						axes: {
							xaxis: {
								renderer: $.jqplot.CategoryAxisRenderer,
								label:'Execution Name',
								ticks: data.execName,
								tickOptions:{
									angle: -60
								},
								tickRenderer:$.jqplot.CanvasAxisTickRenderer

							},
							yaxis: {
								labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
								label:'Percentage of Utilization'
							}
						}
					});	 
				}	
			}

		});	//Plotting the graph for Memory_Utilization 
	}else if(chartType == "Memory_Utilization"){			
		$.get('getStatusSystemDiagnosticsPeakMemoryData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				if(data.systemDiag == null || data.systemDiag == ""){
					alert("Performance data is not available with the selected script and device ");
				}
				else{
					plot3 = $.jqplot('chartdiv', data.systemDiag, {
						animate: true,
						animateReplot: true,
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 20,
								animation: {
									speed: 2500
								},	
							},
							pointLabels: { show: true }
						},
						legend: {
							show: true,
							placement: 'outsideGrid',
							labels: labelsMemorySd,
							location: 'ne',
							rowSpacing: '0px'
						},
						axes: {
							xaxis: {
								renderer: $.jqplot.CategoryAxisRenderer,
								label:'Execution Name',
								ticks: data.execName,
								tickOptions:{
									angle: -60
								},
								tickRenderer:$.jqplot.CanvasAxisTickRenderer

							},
							yaxis: {
								labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
								label:'Used Memory(KB)'
							}
						}
					});	 

				}
			}

		});	//Plotting the graph for Memory_Used_Percentage 
	}else if(chartType == "Memory_Used_Percentage"){			
		$.get('getStatusSystemDiagnosticsMemoryPercData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				if(data.systemDiag == null || data.systemDiag == ""){
					alert("Performance data is not available with the selected script and device ");
				}
				else{
					plot3 = $.jqplot('chartdiv', data.systemDiag, {
						animate: true,
						animateReplot: true,
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 20,
								animation: {
								speed: 2500,
								},	
							},
							pointLabels: { show: true }
						},
						legend: {
							show: true,
							placement: 'outsideGrid',
							labels: labelsMemoryPercSd,
							location: 'ne',
							rowSpacing: '0px'
						},
						axes: {
							xaxis: {
								renderer: $.jqplot.CategoryAxisRenderer,
								label:'Execution Name',
								ticks: data.execName,
								tickOptions:{
									angle: -60
								},
								tickRenderer:$.jqplot.CanvasAxisTickRenderer

							},
							yaxis: {
								labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
								label:'Percentage of Utilization'
							}
						}
					});	 

				}
			}
		});	

	}
}
/**
 * Plotting the line chart. 
 */
function showLineChart(){
	
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();	
	var id = $("#devices").val();
	var scriptGroup = $("#scriptGrp").val();
	var resultcount = $("#resultCount").val();
	var labels = ["Success", "Failure", "Not Executed"];	
	var chartType = null;
	var executionIds = $("#executionId").val();
	var executionIdList = null
	var type = null 
	var checked_radio = $('input:radio[name=chartOptions]:checked').val();
	if(checked_radio!=undefined){
		if(checked_radio=="DeviceBased"){	    	
			executionIdList = "";
			chartType = $("#chartType").val();     	
		}
		else{
			executionIdList = executionIds.toString();		
			chartType = $("#chartType1").val();   
		}
	}
	if(chartType == "ExecutionStatus"){
		hideOptions();		
		$.get('getStatusChartData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList,startIndex:startIndex,endIndex:endIndex} , function(data) {	
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{						
				var plot2 = $.jqplot('chartdiv', [data.success , data.failure ,data.notFound] , {
					seriesColors:['green', 'red', 'gray '],
					animate: true,
					animateReplot: true,
					series:[
					        {
					        	showHighlight: false,
					        	yaxis: 'yaxis',
					        	rendererOptions: {
					        		animation: {
					        			speed: 2500
					        		},			                   
					           	}
					        }, 
					        {
					        	rendererOptions:{
					        		animation: {
					        			speed: 2000
					        		}
					        	}
					        }
					        ],
					        seriesDefaults: {
					        	rendererOptions: {
					        		lineWidth: 2,
					        		smooth: true,
					        	},
					      	pointLabels: { show: true, 
					      		
					      		}
					        },
					        legend: {
					        	show: true,
					        	placement: 'outsideGrid',
					        	labels: labels ,
					        	location: 'ne',
					        	rowSpacing: '0px'
					        },
					        axes: {
					        	xaxis: {
					        		renderer: $.jqplot.CategoryAxisRenderer,
					        		label:'Execution Name',	
					        		min:0,
					        		ticks: data.execName,
					        		tickOptions:{
					        			angle: -40
					        		},
					        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
					        	},

					        	yaxis: {
					        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
					        		min:0,
					        		max: data.yCount +5, 
					        		numberTicks: 11,
					        		label:'Script Count'
					        	}
					        },
					       /* highlighter: {
					        	show: true,
					        	sizeAdjust: 15,
					            tooltipAxes: 'y',
					        },
					        cursor: {
								show: true,
								 tooltipLocation:'sw', 
							}	*/				       
				});	

			}
		});
	}
	else if(chartType == "TimingInfo"){				
		$.get('getStatusBenchMarkData1', {deviceId : id, scriptGroup : scriptGroup,resultCnt : resultcount, executionIds : executionIdList, startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, matching script name not found ");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{
					maxSize = data.maxSize;
					nextPreviousButtonDisplay();
					timingInfo(data);		
				}
			}
		});	
	}
	else if(chartType == "CPU_Utilization"){		
		$.get('getStatusSystemDiagnosticsCPUData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList, startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, script name list is empty");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{

					if(data.systemDiag == null || data.systemDiag == ""){
						alert("Performance data is not available with the selected script and device ");
					}else if ( data.scripts ==   null || data.scripts == " " ){
						alert(" Performance data is not available becoz scripts are not same ");
					}		
					else{
						maxSize = data.maxSize;	
						nextPreviousButtonDisplay();
						cpuUtilization(data);						
					}
				}
			}
		});	
	}else if(chartType == "Memory_Utilization"){			
		$.get('getStatusSystemDiagnosticsPeakMemoryData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList,startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, script name list is empty");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{
					if(data.systemDiag == null || data.systemDiag == ""){
						alert("Performance data is not available with the selected script and device ");
					}
					else{				
						maxSize = data.maxSize;
						nextPreviousButtonDisplay();
						memeryUtilization(data);
					}
				}
			}
		});	
	}else if(chartType == "Memory_Used_Percentage"){	
		$.get('getStatusSystemDiagnosticsMemoryPercData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList,startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, script name list is empty");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{
					if(data.systemDiag == null || data.systemDiag == ""){
						alert("Performance data is not available with the selected script and device ");
					}
					else{
						maxSize = data.maxSize;
						nextPreviousButtonDisplay();
						newFunMemPers(data);	
					}	
				}
			}
		});
	}	
	$('#chartOptionsDiv').show();
}

/**
 * function used to hide/show the next , previous button based on the datas 
 */
function nextPreviousButtonDisplay(){
	if(startIndex == 0 && endIndex == 8 &&  maxSize < endIndex ){
		$("#previous").hide();
		$("#next").hide();	
		$("#previous1").hide();
		$("#next1").hide();
		$("#home").hide();
		$("#home1").hide();
	}else if( startIndex == 0 &&  maxSize > endIndex){
		$("#previous").hide();
		$("#next").show();	
		$("#previous1").hide();
		$("#next1").show();	
		$("#home").hide();
		$("#home1").hide();
	}				
	else if(maxSize <= endIndex  ){		
		$("#previous").show();
		$("#next").hide();	
		$("#previous1").show();
		$("#next1").hide();	
		$("#home").show();
		$("#home1").show();
	}	
	else {
		$("#previous").show();
		$("#next").show();
		$("#previous1").show();
		$("#next1").show();
		$("#home").show();		
		$("#home1").show();		
	}
}
/**
 * Function display the execution name  based chart 
 */

function showExecutionBased(){
	$("#normalexecutionsbased").hide();
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$("#executionbased").show();	
	$("#devicebased").hide();
	$("#scriptbased").hide();
	$("#boxtypebased").hide();
	$("#boxgroupbased").hide();
	$("#boxscriptbased").hide();
	$("#chartdiv").show();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}
/**
 * Function display the device based chart 
 */

function showDeviceBased(){
	$("#normalexecutionsbased").hide();
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$(".chartdivclass").empty();	
	$("#executionbased").hide();	
	$("#devicebased").show();	
	$("#scriptbased").hide();
	$("#boxtypebased").hide();
	$("#boxgroupbased").hide();
	$("#boxscriptbased").hide();
	$("#chartdiv").show();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#resultCategory").show();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * Function to display the divs for plotting cpu memeory graph
 */
function showAnalyzeExecution(){
	$("#normalexecutionsbased").hide();
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$(".chartdivclass").empty();	
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#boxtypebased").hide();
	$("#boxgroupbased").hide();
	$("#boxscriptbased").hide();
	$("#chartdiv").show();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#resultCategory").show();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	
	$('.chartdivAnalyzeExecution').empty(); 
	$("#rdkServiceDiv").hide(); 
	$("#chartdivAnalyzeExecutionDiv3").hide(); 	
	$('#benchMarkPerformanceTypeList').empty()
	$("#benchMarkPerformanceTypeList").append(`<option value="">Please select</option>`);
	
	$.get('getBenchMarkScripts', function(data) {
		var listObject = data.replace("[", "");
		listObject = listObject.replace("]", ""); 
		var listObjects = listObject.split(",");
		var str = ""
	    for (var item of listObjects) {
	    	item = item.replace("'", "");
	    	item = item.replace("'", "");
			$("#benchMarkPerformanceTypeList").append(`<option value="${item}">${item}</option>`);
	    }
	    $("#benchMarkPerformanceTypeListDiv").show();
	});	
}
/**
 * Function display the boxtype based section 
 */

function showBoxTypeBased(){
	$('input[name=BoxOption][value=BoxScriptBased]').prop(
						'checked', false);
	$('input[name=BoxOption][value=BoxGroupBased]').prop(
						'checked', true);
	$("#boxtypebased").show();
	$(".chartdivScriptclass").empty();
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$(".chartdivclass").empty();
	$("#normalexecutionsbased").hide();
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#scriptgroupbased").hide();	
	
	$("#boxgroupbased").show();
	$("#boxscriptbased").hide();
	$("#chartdiv").hide();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#resultCategory").show();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * Function display the script based chart 
 */
function showScriptBased(){
	$("#normalexecutionsbased").hide();
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").show();
	$("#boxtypebased").hide();	
	$("#boxgroupbased").hide();
	$("#boxscriptbased").hide();
	$("#chartdiv").hide();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#resultCategory").show();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * Function to show the showComparisonReport div to generate comparison report
 */
function showComparisonReport(){
	$("#showComparisonReport").show();
	
	$("#normalexecutionsbased").hide();
	$( ".chartdivisionclass" ).empty();
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$(".chartdivScriptclass").empty();
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#scriptgroupbased").hide();	
	$("#boxtypebased").hide();
	$("#boxgroupbased").hide();
	$("#boxscriptbased").hide();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#resultCategory").hide();
	
	$("#categoryLabel").hide();
	$("#categoryId").hide();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
	
}
/**
 * Function display the execution based chart 
 */
function showNormalExecutionBased(){
	$("#normalexecutionsbased").show();
	$( ".chartdivisionclass" ).empty();
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$(".chartdivScriptclass").empty();
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#scriptgroupbased").hide();	
	$("#boxtypebased").hide();
	$("#boxgroupbased").hide();
	$("#boxscriptbased").hide();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#resultCategory").hide();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
	
	var category = $('#category').val();
	$.get('executionsForAnalysis', {category: category}, function(data) {
		var listObject = data.replace("[", "");
		listObject = listObject.replace("]", ""); 
		var listObjects = listObject.split(",");
		var str = ""
	    for (var item of listObjects) {
	    	item = item.replace("'", "");
	    	item = item.replace("'", "");
			str += "<option>" + item + "</option>"
	    }
	    document.getElementById("normalexecname").innerHTML = str;
	});	
			
		
}

/**
 * Function display the script based chart based on boxtype 
 */
function showBoxScriptBased()
{
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	
	$("#normalexecutionsbased").hide();	
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#boxtypebased").show();
	$("#boxscriptbased").show();
	$("#boxgroupbased").hide();
	$("#chartdiv").hide();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}
/**
 * Function display the script based chart based on boxtype 
 */
function showBoxGroupBased()
{
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivclass").empty();	
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$(".chartdivScriptclass").empty();
	$("#executionbased").hide();
	$("#normalexecutionsbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#boxtypebased").show();
	$("#boxgroupbased").show();
	$("#boxscriptbased").hide();
	$("#chartdiv").hide();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * Function display the performance based section 
 */
function showPerformanceBased(){
	$('input[name=chartOptions][value=ExecutionBased]').prop(
						'checked', true);
	$('input[name=chartOptions][value=DeviceBased]').prop(
						'checked', false);
	$("#performance").show();
	$("#chartOptions").val($("#chartOptions option:first").val());
	$( ".chartdivisionclass" ).empty();
	$("#normal").hide();
	$("#normalexecutionsbased").hide();
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivclass").empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$("#scriptbased").hide();
	$("#boxgroupbased").hide();
	$("#executionbased").show();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#boxtypebased").hide();
	$("#boxscriptbased").hide();
	$("#buildnamebased").hide();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();	
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * Function display the normal based section 
 */
function showNormalBased(){
	$('input[name=chartOption][value=ScriptBased]').prop(
						'checked', false);
	$('input[name=chartOption][value=BoxTypeBased]').prop(
						'checked', true);
	$('input[name=chartOption][value=NormalExecutionBased]').prop(
						'checked', false);
	$('input[name=BoxOption][value=BoxScriptBased]').prop(
						'checked', true);
	$('input[name=chartOption][value=BuildNameBased]').prop(
						'checked', false);
	$( ".chartdivisionclass" ).empty();
	$(".chartdivclass").empty();	
	$( ".chartdivBoxtypeclass" ).empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$("#normalexecutionsbased").hide();	
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#boxgroupbased").hide();
	$("#normal").show();
	$("#performance").hide();
	$("#scriptbased").hide();
	$("#boxtypebased").show();
	$("#boxscriptbased").show();
	$("#buildnamebased").show();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").hide();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * Function display the  build name  section 
 */

function showBuildNameBased(category){
	$('input[name=BuildOption][value=BuildScriptBased]').prop(
						'checked', false);
	$('input[name=BuildOption][value=BuildGroupBased]').prop(
						'checked', true);
	$("#boxtypebased").hide();
	$(".chartdivScriptclass").empty();
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$( ".chartdivBuildScriptclass" ).empty();

	$(".chartdivisionbuildclass").empty();
	$(".chartdivclass").empty();
	$("#normalexecutionsbased").hide();
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#scriptgroupbased").hide();	
	$("#boxgroupbased").hide();
	$("#boxscriptbased").hide();
	$("#chartdiv").hide();
	$.ajax({
		type: "get",
		url: 'getExecutionBuildList',
		data: {category: category},
		success: function (data) {
			var parsedData = JSON.parse(data);
			for(index in parsedData){
				addingBuildNames(parsedData[index])
			}
		}
	});
	$("#buildnamebased").show();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").show();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
	
}

/**
 *Function to add execution buildnames to the Buildname list in chart page 
 */
function addingBuildNames(buildName){
	$("#buildname").append(`<option value="${buildName}">${buildName}</option>`);
}

/**
 * Function display the  script  section for build name 
 */
function showBuildScriptBased()
{
	$( ".chartdivBoxtypeclass" ).empty();
	
	$( ".chartdivisionclass" ).empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$( ".chartdivBuildScriptclass" ).empty();
	$(".chartdivclass").empty();
	$("#normalexecutionsbased").hide();	
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#boxtypebased").hide();
	$("#boxscriptbased").hide();
	$("#boxgroupbased").hide();
	$("#chartdiv").hide();
	$("#buildnamebased").show();
	$("#buildscriptbased").show();
	$("#buildgroupbased").hide();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * Function display the script group section for build name 
 */
function showBuildGroupBased()
{
	$( ".chartdivBoxtypeclass" ).empty();
	$( ".chartdivisionclass" ).empty();
	$(".chartdivScriptclass").empty();
	$(".chartdivBuildScriptclass").empty();
	$(".chartdivisionbuildclass").empty();
	$(".chartdivclass").empty();
	$( ".chartdivBuildScriptclass" ).empty();
	$("#normalexecutionsbased").hide();	
	$("#executionbased").hide();	
	$("#devicebased").hide();	
	$("#scriptbased").hide();
	$("#boxtypebased").hide();
	$("#boxscriptbased").hide();
	$("#boxgroupbased").hide();
	$("#chartdiv").hide();
	$("#buildnamebased").show();
	$("#buildscriptbased").hide();
	$("#buildgroupbased").show();
	$("#showComparisonReport").hide();
	$("#categoryLabel").show();
	$("#categoryId").show();
	$("#analyzeExecution").hide();	
	$("#benchmarkData").hide();	
	$("#benchMarkPerformanceTypeListDiv").hide();
	$("#messageDiv").hide();
}

/**
 * This function to show the type of result required
 */
function submitNormalChartType()
{
	var chartType =$("#chartOption").val();
	var category = $("#category").val();
	
	if( chartType == 'Show Results by Box Type')
	{
		showBoxTypeBased();
	}
	else if( chartType == 'Show Results by Device')
	{
		showScriptBased();
	}
	else if( chartType == 'Analyze execution')
	{
		showNormalExecutionBased();
	}
	else if( chartType == 'Comparison Report Download')
	{
		showComparisonReport();
	}
	else if( chartType == 'Show Results by Build Name')
	{
		showBuildNameBased(category);
	}
	
}

/**
 * This function to show the type of result required
 */
function submitPerformanceChartType()
{
	var chartType =$("#chartOptions").val();
	
	if (chartType == 'Compare Results by Execution Name')
	{
		showExecutionBased();
	}
	else if (chartType == 'Compare Results by Device Details')
	{
		showDeviceBased();
	}else if (chartType == 'Analyze RDK Certification Execution')
	{
		showAnalyzeExecution();
	}
	
}

/**
 * This function to show the type of result required
 */
function submitChartCategory()
{
	var typeOption =$("#typeOption").val();
	
	if( typeOption == 'Normal')
	{
		showNormalBased();
	}
	else if( typeOption == 'Performance')
	{
		showPerformanceBased();
	}
	
	
}


function updateValueOnCategoryChange(val){
	$.get('getCategorySpecificList',{category:val}, function(data) { 
		$("#categoricalDisplay").html(data);
	});
}


/**
 * This function plot the line graph for Memory_Utilization 
 */
function memeryUtilization(data){
	plot3 = $.jqplot('chartdiv', data.memoryValuesTest,{
		animate: true,
		animateReplot: true,
		series:[
		        {   
		        	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500
		        		},			                   
		        	}
		        }, 
		        {
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show: true ,
		        		}
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',
		        	labels: data.execName,
		        	location: 'ne',
		        	rowSpacing: '0px'
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script Name',	
		        		min:0,
		        		ticks: data.scripts,	             
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',

		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		        	},

		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Used Memory (KB)'
		        	}
		        },
		        /*highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				} */		          
	});
}
/**
 * Function for  plotting the line chart for  CPU Utilization
 */
function cpuUtilization(data){
	plot3 = $.jqplot('chartdiv', data.cpuValuesTest,{ 
		animate: true,
		animateReplot: true,
		series:[
		        {  	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500,
		        		},			                   
		        	}
		        }, 
		        {	            	
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000,
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show: true,
		        		},
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',		          
		        	labels : data.execName,		            
		        	location: 'ne',
		        	rowSpacing: '10px'
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script  Name',	
		        		min:0,
		        		ticks: data.scripts,	             
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',

		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer

		        	},	
		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,		        	   
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Percentage of Utilization (Peak)'
		        	}
		        },
		       /* highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				}*/
	});		

}
//Function for  plotting the line chart for  Memory Used Persentage 
function newFunMemPers(data){
	plot3 = $.jqplot('chartdiv', data.memoryValuesTest, {
		animate: true,
		animateReplot: true,
		series:[
		        {
		        	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500
		        		},			                   
		           	}
		        }, 
		        {
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {		           
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show:true,
		        		}
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',
		        	labels: data.execName,
		        	location: 'ne',
		        	rowSpacing: '0px'
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script Name',	
		        		min:0,
		        		ticks: data.scripts,	             
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',

		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		        	},

		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Percentage of Utilization(Peak)'
		        	}
		        },
		        /*highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				}*/
	});
}

//Function for  plotting the line chart for Timing info 

function  timingInfo(data ){
	plot3 = $.jqplot('chartdiv', data.benchmark , {
		animate: true,
		animateReplot: true,
		series:[
		        {
		        	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500
		        		},			                   
		        	}
		        }, 
		        {
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show: true,
		        		}
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',
		        	labels: data.execName,
		        	location: 'ne',
		        	rowSpacing: '0px',
		        	showSwatches: true,
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script Name',	
		        		min:0,
		        		ticks: data.scripts,
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',
		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		        	},

		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Execution Time(millisec) ',
		        	}
		        },
		        /*highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				},*/
	});

}
/*
 * Plotting the 8 script for next points. 
 */
function nextPlot(){
	if((maxSize != -1 && endIndex <= maxSize) || maxSize == -1){
		startIndex = endIndex ;
		endIndex = startIndex + 8 ;
	}else{
		alert("No more next available");
	}
	nextCount++;
	showLineChart();
}
/*
 * Plotting the 8 script for previous points.
 */
function previousPlot(){
	if(startIndex == 0){
		alert("No more previous available");
	}else{
		endIndex = endIndex - 8 ;
		startIndex = endIndex - 8;
		if(startIndex < 0){
			startIndex = 0;
		}
	}
	previousCount++ ;
	showLineChart();
}


/**
 * Function for shows the home page
 */

function homePage(){	
	startIndex = 0 ;
	endIndex = 8  ; 

	var checked_radio1 = $('input:radio[name=ChartType]:checked').val();
	if(checked_radio1 != undefined ){
		if(checked_radio1 == "BarChart" ){
			showChart1();	
		}else{
			showChart();	
		}
	}

}

/**
 * Method to display the script field based on script type in comparison excel popup
 */
function showScriptTypesForComparisonExec(){
	var choice = $( "#scriptTypeComparison" ).val()
	if((choice == "")){
		$("#scriptLabelComparisonId").hide();
		$("#scriptFieldComparisonId").hide();
		$("#scriptValueComparisonId").val('');
	}
	else{
		$("#scriptLabelComparisonId").show();
		$("#scriptFieldComparisonId").show();
		$("#scriptValueComparisonId").val('');
	}
}

/**
 * Method to display the script field based on script type in base excel popup
 */
function showScriptTypesForBaseExec(){
	var choice = $( "#scriptTypeBase" ).val()
	if((choice == "")){
		$("#scriptLabelBaseId").hide();
		$("#scriptFieldBaseId").hide();
		$("#scriptValueBaseId").val('');
	}
	else{
		$("#scriptLabelBaseId").show();
		$("#scriptFieldBaseId").show();
		$("#scriptValueBaseId").val('');
	}
}

/**
 * Function to toggle the div containing the comparison report feature explanation
 */
function helpDivToggle(){
	  var x = document.getElementById("helpDivComparison");
	  if (x.style.display === "none") {
	    x.style.display = "block";
	  } else {
	    x.style.display = "none";
	  }
}

/**
 * Function to finalize the base execution selection when the confirm button is clicked in the popup
 * @param executionIdList
 */
function baseExecutionSelection(executionIdList) {
	var notChecked = [];
	var baseExecId = "";
	var url = $("#url").val();
	var executionIdArray = JSON.parse(executionIdList);
	for(i=0;i<=executionIdArray.length;i++){
		if ($('#baseExecutionRadio_'+executionIdArray[i]).is(":checked"))
		{
			baseExecId =  executionIdArray[i];
		}
	}
	if (baseExecId == "") {
	    alert("Please select any one execution");
	}
	else{
		$.get(url+'/execution/getExecutionName', {id: baseExecId}, function(data) {
			document.getElementById("baseExecutionName").value = data;
			document.getElementById("finalBaseExecFromDate").value = document.getElementById("generateFromDateBaseExec").value;
			document.getElementById("finalBaseExecToDate").value = document.getElementById("generateToDateBaseExec").value;
			document.getElementById("finalBaseExecCategory").value = document.getElementById("categoryIdBaseExec").value;
			document.getElementById("finalBoxTypeBaseExec").value = document.getElementById("boxTypeBaseExec").value;

			//setting the base execution name in the hidden field to pass it to filterComparisonExecutions function 
			// to exclude the base execution while filtering the comparison executions
			document.getElementById("finalBaseExecName").value = data;
			//closing the current modal
			$.modal.close();
		});
	}
}

/**
 * Function to show the selected base execution in popup
 * @param id
 */
function showSelectedBaseExecution(id){
	document.getElementById("selectedExecution").value = id
	var selectedExecution = id 
	selectedExecution = selectedExecution.split("_")[1]
	var url = $("#url").val();
	$.get(url+'/execution/getExecutionName', {id: selectedExecution}, function(data) {
		document.getElementById("selectedExecution").innerHTML = data
	});
	
}
/**
 * Function to finalize the comparison executions selection when the confirm button is clicked in the popup
 * @param executionIdList
 */
function comparisonExecutionSelection(executionIdList) {
	var notChecked = [];
	var selectedRows = [];
	var checkedRows = "";
	var url = $("#url").val();
	var executionIdArray = JSON.parse(executionIdList);
	for(i=0;i<=executionIdArray.length;i++){
		if ($('#comparisonExecutionsCheckbox_'+executionIdArray[i]).is(":checked"))
		{
			checkedRows =  executionIdArray[i] + "," + checkedRows;
		}
	}
	checkedRows = checkedRows.slice(0, -1)
	selectedRows = checkedRows.split(",")
	if((selectedRows.length > 10) || (checkedRows  == "")){
		alert("Maximum number of executions that can be compared is 10 and minimum number is 1")
		document.getElementById("comparisonExecutionName").value = ""
	}else{
		$.get(url+'/execution/getExecutionNamesAsList', {checkedRows: checkedRows}, function(data) {
			document.getElementById("comparisonExecutionName").value = data;
			//closing the current modal
			$.modal.close();
		});
	}
}

/**
 * Function to validate all input fields in base execution PopUp
 */
function validateBaseInputFields(){
	document.getElementById("validate").value = "";
	var fromDateString = document.getElementById("generateFromDateBaseExec").value;
	var toDateString = document.getElementById("generateToDateBaseExec").value;
	var boxType = document.getElementById("boxTypeBaseExec").value;
	var category = document.getElementById("categoryIdBaseExec").value;
	if (fromDateString == "" || toDateString == "" || boxType == "" || category == "") {
	    alert("From date, To date, Category and Box Type fields are mandatory");
	    document.getElementById("validate").value = "false";
	}
	var today = new Date();
	var fromDate = new Date(fromDateString);
	var toDate = new Date(toDateString);
	if((fromDate > today) || (toDate > today)){
	    alert('Selected date cannot be greater than todays date');
	    document.getElementById("validate").value = "false";
	}
	if(fromDate > toDate){
		alert('From Date cannot be greater than To Date');
		document.getElementById("validate").value = "false";
	}
}


/**
 * Function to validate all input fields in comparison executions PopUp
 */
function validateComparisonInputFields(){
	document.getElementById("validateComparison").value = "";
	var fromDateString = document.getElementById("generateFromDateComparisonExec").value;
	var toDateString = document.getElementById("generateToDateComparisonExec").value;
	var boxType = document.getElementById("boxTypeComparisonExec").value;
	var category = document.getElementById("categoryIdComparisonExec").value;
	if (fromDateString == "" || toDateString == "" || boxType == "" || category == "") {
	    alert("From date, To date, Category and Box Type fields are mandatory");
	    document.getElementById("validateComparison").value = "false";
	}
	var today = new Date();
	var fromDate = new Date(fromDateString);
	var toDate = new Date(toDateString);
	if((fromDate > today) || (toDate > today)){
	    alert('Selected date cannot be greater than todays date');
	    document.getElementById("validateComparison").value = "false";
	}
	if(fromDate > toDate){
		alert('From Date cannot be greater than To Date');
		document.getElementById("validateComparison").value = "false";
	}
}

/**
 * Function to generate modal popup for base execution when choose button is clicked
 */
function showBaseDetails(){
	$("#baseExecutionPopUp").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 1200,
	            height: 450	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	 $( "#generateFromDateBaseExec" ).datepicker();
	 $( "#generateToDateBaseExec" ).datepicker();
	 var today = new Date();
	 var priorDate = new Date();
	 priorDate.setDate(today.getDate() - 30)
	 var ddtoday = String(today.getDate()).padStart(2, '0');
	 var mmtoday = String(today.getMonth() + 1).padStart(2, '0');
	 var yyyytoday = today.getFullYear();
	 today = mmtoday + '/' + ddtoday + '/' + yyyytoday;
	 var ddprior = String(priorDate.getDate()).padStart(2, '0');
	 var mmprior = String(priorDate.getMonth() + 1).padStart(2, '0');
	 var yyyyprior = priorDate.getFullYear();
	 priorDate = mmprior + '/' + ddprior + '/' + yyyyprior;
	 document.getElementById("generateFromDateBaseExec").value = priorDate
	 document.getElementById("generateToDateBaseExec").value = today
	 var category_id = "RDKV"
	 var url = $("#url").val();
	 $.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
		var select = '<select id="boxTypeBaseExec" name="boxTypeBaseExec"><option value="">Please Select</option>';
		for(var index = 0; index < data.length; index ++ ) {
			select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
		}
		select += '</select>';
		$("#boxTypeIdBaseExec").html(''); 
		$("#boxTypeIdBaseExec").html(select); 
	 });
}

/**
 * Function to generate modal popup for comparison execution when choose button is clicked
 */
function showComparisonDetails(){
	$("#comparisonExecutionPopUp").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 1200,
	            height: 450	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	document.getElementById("generateFromDateComparisonExec").value = document.getElementById("finalBaseExecFromDate").value
	document.getElementById("generateToDateComparisonExec").value = document.getElementById("finalBaseExecToDate").value
	document.getElementById("categoryIdComparisonExec").value = document.getElementById("finalBaseExecCategory").value
	 $( "#generateFromDateComparisonExec" ).datepicker();
	 $( "#generateToDateComparisonExec" ).datepicker();
	var category_id = document.getElementById("finalBaseExecCategory").value
	var finalBoxType = document.getElementById("finalBoxTypeBaseExec").value
	var url = $("#url").val();
	if (category_id == "") {
		document.getElementById("categoryIdComparisonExec").value = "RDKV"
		category_id = "RDKV"
		$.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
			var select = '<select id="boxTypeComparisonExec" name="boxTypeComparisonExec"><option value="">Please Select</option>';
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
			}
			select += '</select>';
			$("#boxTypeIdComparisonExec").html(''); 
			$("#boxTypeIdComparisonExec").html(select); 
		});
	}else{
		 $.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
			var select = '<select id="boxTypeComparisonExec" name="boxTypeComparisonExec"><option value="'+finalBoxType+'">'+ finalBoxType +'</option>';
			for(var index = 0; index < data.length; index ++ ) {
				if(data[index].name != finalBoxType){
					select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
				}
			}
			select += '</select>';
			$("#boxTypeIdComparisonExec").html(''); 
			$("#boxTypeIdComparisonExec").html(select); 
		 });
	}
}
/**
 * Function to generate comparison excel report after base and comparison executions are selected
 * @returns {Boolean}
 */
function comparisonExcelReportGeneration(){
	var baseExecution = document.getElementById("baseExecutionName").value
	var comparisonExecList = document.getElementById("comparisonExecutionName").value
	var url = $("#url").val();
	if(baseExecution == "" || comparisonExecList == ""){
		alert("Base execution and comparison execution fields should not be empty")
	}else{
		$.get(url+'/execution/checkValidMultipleExecutions', {execNames: baseExecution}, function(data) {
			if(data == "valid"){
				$.get(url+'/execution/checkValidMultipleExecutions', {execNames: comparisonExecList}, function(dataList) {
					if(dataList == "valid"){
						alert("Please wait, Report generation may take few minutes...")
						window.open(url+"/execution/comparisonExcelReportGeneration/?comparisonExecutionNames="+comparisonExecList+"&baseExecutionName="+baseExecution,'_self');
					}else{
						alert("Valid Comparison Execution not found to generate report")
					}
				});
			}else {
				alert("Valid Base Execution not found to generate report")
			}
		});
	}
	return false
}
/**
 * Function to show the execution details
 */
function showDetails(){
	id =  $("#normalexecname").val();
	$.get('showDetailedData', {id: id}, function(data) {$("#executionDetails").html(data); });		
}

/**
 * Function to copy the execution name
 */
function copyExecName() {
	var execName = $("#normalexecname").val();
	$('#execNameField').show();
	$('#execNameField').val(execName);
	var execNameField = document.getElementById('execNameField');
	console.log(execNameField);
	execNameField.focus();
	execNameField.select();
	document.execCommand("copy");
    $('#execNameField').hide();
}

/**
 * Function to show the resullt analysis popup
 */
function showResultAnalysis(id, scriptName, boxTypeId, execDeviceId, execResultId) {
	$("#scriptname").val(scriptName);
	$("#boxtype").val(boxTypeId);
	$('#noOfEntries').val('5');
	category = $("#category").val();
    $.get('resultAnalysis', {execId:id, scriptName:scriptName, boxTypeId:boxTypeId,execDeviceId:execDeviceId, execResultId:execResultId, selectedBoxType: 'All',
    	noOfEntries:'5', category: category},
    		function(data) {$("#resultAnalysisPopup").html(data);});
    $("#resultAnalysisPopup").modal({ opacity : 40, overlayCss : {
	  backgroundColor : "#c4c4c4" }, containerCss: {
            width: 1200,
            height: 550
            
        } }, { onClose : function(dialog) {
	  $.modal.close(); } });
}

/**
 * Function to save the defect analysis data
 * @param executionId
 * @param scriptName
 */
function saveData(executionId, scriptName){
	defectType= $('#defectType').val();
	ticketNo = $('#ticketNo').val();
	remarks= $('#remarks').val();
	if((defectType != null && defectType != "") && (ticketNo != null && ticketNo != "")){
	    $.get('saveAnalysisData', {executionId:executionId , scriptName:scriptName , defectType:defectType, ticketNo:ticketNo, remarks:remarks}, 
		    function (data){
		        $("#savedMessage").fadeIn(300).delay(800).fadeOut(400);
	    		$("#executionDetails").html(data); 
	    });
	}
	else{
		alert("Please fill the Defect Type and Ticket Number details")
	}
    		
}

/**
 * Displays the analysis history data based on the dropdown selection
 * @param id
 * @param execDeviceId
 * @param execResultId
 * @param scriptName
 */
function searchData(id, execDeviceId,execResultId, scriptName) {
	noOfEntry = $('#noOfEntries').val();
	if(noOfEntry =="") {
		noOfEntry = '5'
	}
	selectedBoxType = $("#searchBoxType").val();
	if(selectedBoxType == "") {
		selectedBoxType = "All"
	}
	$("#boxtype").val(boxTypeId);
	category = $("#category").val();
    $.get('resultAnalysis', {execId:id, scriptName:scriptName, boxTypeId:boxTypeId, selectedBoxType: selectedBoxType, noOfEntries:noOfEntry, 
    	execDeviceId:execDeviceId, execResultId:execResultId, category: category}, 
    		function(data) {
    	$("#resultAnalysisPopup").html(data);
    });	
}

/**
 * Function to fill the defect details with the defect details of a past execution
 * @param execId
 */
function fillDefectDetails(execId){
	$("#defectType").val(document.getElementById("defectType_"+execId).value);
	$("#ticketNo").val(document.getElementById("ticketNo_"+execId).value);
	$("#remarks").val(document.getElementById("remarks_"+execId).value);
}

/**
 * Function to fetch the Cpu memory data of a script and plot as a graph
 */
function showChartAnalyzeExecution(){
	var rdkServiceExecutionName = $("#rdkServiceExecutionId").val();
	var rdkServiceScript = $("#rdkServiceScript").val();
	$('.chartdivAnalyzeExecution').empty();
	document.getElementById("chartdivAnalyzeExecutionDiv1").style.width = "1200px";
	$("#chartdivAnalyzeExecutionDiv3").show(); 	
	$('#chartdivAnalyzeExecution').show();
	if(rdkServiceScript != "" && rdkServiceExecutionName != ""){
		$.get('getCpuMemoryInfoData', {rdkServiceExecutionName : rdkServiceExecutionName, rdkServiceScript : rdkServiceScript} , function(data) {	
			if((data.cpuLoadList.length  == 0) || (data.memUsageList.length  == 0)){
				alert(" No results to show");
			}else{
				if(data.cpuLoadList.length < 50){
					document.getElementById("chartdivAnalyzeExecutionDiv1").style.width = "1200px";
				}else if(data.cpuLoadList.length >= 50 && data.cpuLoadList.length < 100){
					document.getElementById("chartdivAnalyzeExecutionDiv1").style.width = "1400px";
				}else if(data.cpuLoadList.length >= 100 && data.cpuLoadList.length < 1000){
					var counter = Math.ceil(data.cpuLoadList.length/100)
					var pixelSize = (1500 * counter)+"px";
					document.getElementById("chartdivAnalyzeExecutionDiv1").style.width = pixelSize;
				}else{
					document.getElementById("chartdivAnalyzeExecutionDiv1").style.width = "40000px";
				}
				var plot1 = $.jqplot('chartdivAnalyzeExecution', [data.cpuLoadList,data.memUsageList], {
				      title: "<b> Cpu Load and Memory Usage Chart </b>", 
				      seriesDefaults: { 
				        showMarker:true,
				        //pointLabels: { show:true } 
				      },
				      	axes:{
				    	  	xaxis:{
				            	renderer: $.jqplot.CategoryAxisRenderer,
								label:rdkServiceScript,	
								min:0,
								max:150 ,
								ticks: data.cpuLoadList.length,
								tickOptions:{
									angle: -60,
									fontSize: '8pt'
								},
								tickRenderer:$.jqplot.CanvasAxisTickRenderer
				            },
				            yaxis: {
								label:"cpu_load",
								min:0,
								max:data.yMaxCpuLoad
							},
							y2axis: {
								label:"memory_usage",
								min:0,
								max:data.yMaxMemUsage
							}
				      },
				        series : [{
				            yaxis : 'yaxis',
				            label:"cpu_load"
				        }, {
				            yaxis : 'y2axis',
				            label:"memory_usage"
				        }],
				        highlighter: {
				          show: true,
				          tooltipAxes: 'y'
				        },
					    legend: {
					    	show: true,
					   		placement: 'outsideGrid',
					   		location: 'nw',
					   		labels: ['cpu_load','memory_usage']
					   },
				        highlighter: {
				        	show: true,
					        showTooltip: true,
					        tooltipLocation:'ne',
					        tooltipAxes: 'y',
					        tooltipContentEditor: function (str, seriesIndex, pointIndex, plot) {
					        	var val = plot.data[seriesIndex][pointIndex];
					            var label = plot.series[seriesIndex]["label"]
					            var html = "<div>";
					            html += label;
					            html += "  : ";
					            html += val;
					            return html;
					          }
				        }
				 });
			}
		} );
	}else{
		alert("Execution name and script should not be empty")
	}
}

/**
 * Function to get the list of rdkservice executions and fill it in the execution dropdown to plot cpu memory graph 
 */
function showExecutionNames(){
	$('.chartdivAnalyzeExecution').empty();
	$("#rdkServiceDiv").hide(); 	
	$("#chartdivAnalyzeExecutionDiv3").hide(); 	
	var select = '<select style="width:300px" id="rdkServiceScript" name="rdkServiceScript"><option value="">Please Select</option>';
	$("#rdkServiceScriptId").html(''); 
	$("#rdkServiceScriptId").html(select); 
	var category = $("#category").val();
	var fromDate = $("#fromDateFilterExecutions").val();
	var toDate = $("#toDateFilterExecutions").val();
	if(fromDate != "" && toDate != ""){
		var beforeDate = new Date(fromDate); 
		var afterDate = new Date(toDate); 
		var difference_In_Time = afterDate.getTime() - beforeDate.getTime(); 
		var difference_In_Days = difference_In_Time / (1000 * 3600 * 24); 
		if(difference_In_Days > 30){
			alert("Maximum dates that can be selected is 30")
		}else{
			var today = new Date();
			if((beforeDate > today) || (afterDate > today)){
				alert("From or To dates cannot be greater than today's date")
			}else if(beforeDate > afterDate){
				alert("From cannot be greater than To date")
			}else{
			    $.get('filterRDKServiceExecutions', {fromDateParam: fromDate, toDateParam:toDate}, function(data) {
			    	$('#rdkServiceExecutionId').empty()
			    	$("#rdkServiceExecutionId").append(`<option value="">Please select</option>`);
					for(i=0;i<data.length;i++){
						$("#rdkServiceExecutionId").append(`<option value="${data[i]}">${data[i]}</option>`);
					}
			    	$("#rdkServiceDiv").show();
			    });	
			}
		}
	}else{
		alert("Please select From and To dates")
	}
}


/**
 * Function to get the scripts of an execution and fill it in the script list dropdown to plot cpu memory graph
 * @param category_id
 */
function getScriptsByExecution(execution_name) {
	var url = $("#url").val();
	var executionName = execution_name
	if(execution_name != '') {
	    $.get(url+'/execution/getScriptsByExecution', {executionName: executionName}, function(data) {
			var select = '<select style="width:300px" id="rdkServiceScript" name="rdkServiceScript"><option value="">Please Select</option>';
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index] + '">' + data[index] + '</option>';
			}
			select += '</select>';
			$("#rdkServiceScriptId").html(''); 
			$("#rdkServiceScriptId").html(select); 
	    });	
	}
	else {
		$("#rdkServiceScriptId").html('');
	}
}

/**
 * Method to get the processType of the benchmark tool selected 
 * @param benchMarkScript
 */
function getProcessTypeOfScript(benchMarkScript) {
	var url = $("#url").val();
	var benchMarkScrpt = benchMarkScript
	$('.chartdivAnalyzeExecution').empty(); 
	$('.chartdivBenchMarkclass').empty(); 
	if(benchMarkScrpt != '') {
	    $.get('getProcessTypeOfScript', {benchMarkScrpt: benchMarkScrpt}, function(data) {
	    	if(data.processType == "multipleEntries"){
	    		$("#rdkServiceDiv").hide(); 
	    		$("#chartdivAnalyzeExecutionDiv3").hide(); 	
	    		$("#benchmarkData").hide();	
	    		$("#analyzeExecution").show();	
	    		$( "#fromDateFilterExecutions" ).datepicker();
	    		$( "#toDateFilterExecutions" ).datepicker();
	    		 $("#messageDiv").show();
	    		 document.getElementById("messageDiv").innerText = "Plot data values across iterations for a single execution";
	    		 document.getElementById("messageDiv").style.fontSize = "medium";
	    		 var today = new Date();
	    		 var priorDate = new Date();
	    		 priorDate.setDate(today.getDate() - 7)
	    		 var ddtoday = String(today.getDate()).padStart(2, '0');
	    		 var mmtoday = String(today.getMonth() + 1).padStart(2, '0');
	    		 var yyyytoday = today.getFullYear();
	    		 today = mmtoday + '/' + ddtoday + '/' + yyyytoday;
	    		 var ddprior = String(priorDate.getDate()).padStart(2, '0');
	    		 var mmprior = String(priorDate.getMonth() + 1).padStart(2, '0');
	    		 var yyyyprior = priorDate.getFullYear();
	    		 priorDate = mmprior + '/' + ddprior + '/' + yyyyprior;
	    		 document.getElementById("fromDateFilterExecutions").value = priorDate
	    		 document.getElementById("toDateFilterExecutions").value = today
	    	}else if(data.processType == "singleEntry"){
	    		$("#analyzeExecution").hide();	
	    		$("#benchmarkData").show();	
	    		$("#messageDiv").show();
	    		document.getElementById("messageDiv").innerText = "Plot data values across executions";
	    		document.getElementById("messageDiv").style.fontSize = "medium";
	    		var benchMarkPerformance = data.benchMarkPerformance
				var select = '<select style="width: 200px" id="parameterValue" name="parameterValue"><option value="">Please Select</option>';
				select += '<option value="ALL">ALL</option>';
				for(var index = 0; index < benchMarkPerformance.length; index ++ ) {
					select += '<option value="' + benchMarkPerformance[index] + '">' + benchMarkPerformance[index] + '</option>';
				}
				select += '</select>';
				$("#parameterId").html(''); 
				$("#parameterId").html(select); 
	    	}
	    });	
	}
	else {
	}
}

/**
 * Method to return the data map for plotting Hardware performance data in according to the benchmark tool selected
 */
function getBenchMarkChartData(){
	$(".chartdivBenchMarkclass" ).empty();
	var parameterValue = $("#parameterValue").val();
	var resultcount = $("#resultBenchmarkCounts").val();	
	var utilityName = $("#benchMarkPerformanceTypeList").val();	
	if(utilityName == null || utilityName.length == 0 )
	{ alert ('please select a utility value  ');}
	if(parameterValue == null || parameterValue.length == 0 )
	{ alert ('please select a parmeter value  ');}
	else if(resultcount == null || resultcount.length == 0){
		alert ('please give a valid result number  ');
	}else if(parseInt(resultcount) < 2 || parseInt(resultcount) > 100){
		alert ('Maximum allowed range is 2-100');
	}else{
		$.get('getBenchMarkChartData', {utilityName : utilityName, parameterValue : parameterValue, resultcount : resultcount} , function(data) {
			if(parameterValue == "ALL"){
				var series = [];
				for(var i = 0; i < data.parameterKeyList.length; i++){
				    var label = data.parameterKeyList[i];
				    series.push({label:label});
				}				
				var plot1 = $.jqplot('chartdivBenchMark', data.resultList, {
				      title: "<b>" + data.executionName.length   +" Execution Results </b>", 
				      seriesDefaults: { 
				        showMarker:true,
				        //pointLabels: { show:true }, // uncomment this to display value of each point
			            breakOnNull: true
				        
				      },
				      series: series,
				      axes:{
				    	  	xaxis:{
				            	renderer: $.jqplot.CategoryAxisRenderer,
								label:'Execution Name',	
								min:0,
								max:data.yMax ,
								ticks: data.executionName,
								tickOptions:{
									angle: -60,
									fontSize: '8pt'
								},
								tickRenderer:$.jqplot.CanvasAxisTickRenderer
				            },
				            yaxis: {
								label:parameterValue,
								min:0,
								max:data.yMax  
							}
				      },
				      legend: {
				          show: true,
				          placement: 'outsideGrid',
				          labels: data.parameterKeyList
				      },
				      highlighter: {
				    	  show: true,
				          showTooltip: true,
				          tooltipLocation:'ne',
				          tooltipAxes: 'y',
				          tooltipContentEditor: function (str, seriesIndex, pointIndex, plot) {
				              var val = plot.data[seriesIndex][pointIndex][1];
				              var parma = plot.series[seriesIndex]["label"]
				              var execName = plot.options.axes.xaxis.ticks[pointIndex]
				              var html = "<div>Value: ";
				              html += val;
				              html += "  <br>Parameter Name : ";
				              html += parma;
				              html += "  <br>Execution Name : ";
				              html += execName;
				              return html;
				          }
				      },
				      cursor: {
				    	  show: false
				      }
				 });
			}else{
				var plot1 = $.jqplot('chartdivBenchMark', [data.resultList], {
					      title: "<b>" + data.resultList.length   +" Execution Results </b>", 
					      seriesDefaults: { 
					        showMarker:true,
					        pointLabels: { show:true } 
					      },
					      	axes:{
					    	  	xaxis:{
					            	renderer: $.jqplot.CategoryAxisRenderer,
									label:'Execution Name',	
									min:0,
									max:data.yMax ,
									ticks: data.executionName,
									tickOptions:{
										angle: -60,
										fontSize: '8pt'
									},
									tickRenderer:$.jqplot.CanvasAxisTickRenderer
					            },
					            yaxis: {
									label:parameterValue,
									min:0,
									max:data.yMax  
								}
					      }
					 });
			}
		} );
	}
}
