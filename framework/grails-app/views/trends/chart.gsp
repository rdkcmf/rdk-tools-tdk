
<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2016 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<%--<!DOCTYPE html>--%>
<%@page import="org.springframework.util.StringUtils"%>
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<%@ page import="com.comcast.rdk.Execution"%>
<%@ page import="com.comcast.rdk.ScriptFile"%>
<%@ page import="com.comcast.rdk.BoxType"%>

<html>
<head>
<meta name="layout" content="main">
<g:set var="entityName"
	value="${message(code: 'ScriptExecution.label', default: 'ScriptExecution')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.jqplot.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shCoreDefault.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shThemejqPlot.min.css')}" />
<title>Trends</title>
<g:javascript library="chart/jquery.jqplot.min" />
<g:javascript library="chart/shCore.min" />
<g:javascript library="chart/shBrushJScript.min" />
<g:javascript library="chart/shBrushXml.min" />
<g:javascript library="chart/jqplot.barRenderer.min" />
<g:javascript library="chart/jqplot.categoryAxisRenderer.min" />
<g:javascript library="chart/jqplot.pointLabels.min" />
<g:javascript library="chart/jqplot.canvasTextRenderer.min" />
<g:javascript library="chart/jqplot.canvasAxisLabelRenderer.min" />
<g:javascript library="chart/jqplot.canvasAxisTickRenderer.min" />
<g:javascript library="jquery.more" />
<g:javascript library="select2" />
<g:javascript library="chartview" />
<g:javascript library="jquery-ui"/>
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'select2.css')}"
	type="text/css" />

<script type="text/javascript">
	$(document).ready(
			function() {
				$("#trendid").addClass("changecolor");
				$("#executionId").select2();
				var defaultValue = "normal";
				$('input[name=typeOption][value=Normal]').prop(
						'checked', true);
				$('input[name=chartOption][value=ScriptBased]').prop(
						'checked', false);
				$('input[name=chartOption][value=BoxTypeBased]').prop(
						'checked', true);
				$('input[name=chartOption][value=NormalExecutionBased]').prop(
						'checked', false);
				$('input[name=BoxOption][value=BoxGroupBased]').prop(
						'checked', true);
				$("#boxgroupbased").show();
				$("#previous").hide();
				$("#boxtypebased").show();
				$("#next").hide();
				$("#home").hide();
				$("#buildscriptgroupsname").select2();
				$("#buildscriptname").select2();
				$("#scriptname").select2();
				$("#normalexecname").select2();
				$("#scriptgroupsname").select2();
				$("#script").select2();
				$("#device").select2();	
				$("#boxgroupbased").select2();
				$("#boxscriptbased").select2();
				$("#buildgroupbased").select2();
				$("#buildscriptbased").select2();
				$("#buildname").select2();

	});


	
</script>
<style>
#script  option { 
	width:250px;}
</style>

</head>
<body>
	<div id="chart1"></div>
	<div>
		&emsp;
		<h1>&emsp;&emsp;&emsp;Result Analysis</h1>
		<g:if test="${flash.message}">
			<div class="message" role="status">
				${flash.message}
			</div>
		</g:if>
		<g:if test="${error}">
			<ul class="errors" role="alert">
				<li>
					${error}
				</li>
			</ul>
		</g:if>
		<br>
		<g:hiddenField id="url" name="url" value="${url}"/>
		<g:hiddenField id="finalBaseExecFromDate" name="finalBaseExecFromDate" value=""/>
		<g:hiddenField id="finalBaseExecToDate" name="finalBaseExecToDate" value=""/>
		<g:hiddenField id="finalBaseExecCategory" name="finalBaseExecCategory" value=""/>
		<g:hiddenField id="finalBoxTypeBaseExec" name="finalBoxTypeBaseExec" value=""/>
		<div>
			<table class="noClass" style="border: 1; border-color: black; width:90%;" >
				<tr>
					<td>
						<div style="float: left;" id="categoryLabel">&emsp;&emsp;&emsp;&emsp;Category&emsp;&emsp;&emsp;&emsp;&emsp; &emsp; </div>
						<div style="float: left; margin-left: 20px;" id="categoryId">
							<g:form controller="trends" action="chart">
								<g:select id="category" name="category" from="['RDKV','RDKB']"
									onchange="submit()" value="${category}" />
							</g:form>
						</div>
					</td>
					<td>
						<div id = "normal" >
							<div style="float: left;">&emsp;&emsp;&emsp;&emsp; Result Type</div>
							&emsp;<g:select id = "chartOption" name="chartOption" from="['Show Results by Box Type','Show Results by Device','Show Results by Build Name', 'Analyze execution','Comparison Report Download']"
								onchange="submitNormalChartType();" value="${chartOption}" />
							
						</div>
						<div id = "performance" style="display: none;">
						<div style="float: left;">&emsp;&emsp;&emsp;&emsp;Result Type &emsp; &emsp;</div>
							&emsp;<g:select id = "chartOptions" name="chartOptions" from="['Compare Results by Execution Name','Compare Results by Device Details']"
								onchange="submitPerformanceChartType();" value="${chartOptions}" />
						</div>
					
						
					</td>
					<td >
						<g:if test="${category == "RDKV"}">
						<div id="resultCategory">
							<div style="float: left;">
							Result Category</div>
							&emsp;<g:select id = "typeOption" name="typeOption" from="['Normal','Performance']"
								onchange="submitChartCategory();" value="${typeOption}" />
							<g:hiddenField name="startIndex" value="${startIndex}" />
							<g:hiddenField name="endIndex" value="${endIndex}" />
						</div>
							
						</g:if>
					</td>
					<td></td>
				</tr>
			</table>

		</div>	
                        <br />
			<div id="normalexecutionsbased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black; " >
					<tr >
						<td style="vertical-align: middle;" >
							&emsp;&emsp;&emsp;&emsp;Select the Execution Name				
							&emsp;<g:select id="normalexecname" name="normalexecname" style="height:200px;width:300px" noSelection="['' : 'Please Select']" from="${executionTotalList }" value="" class="many-to-one selectCombo"/>										
							<span onclick="copyExecName();" style="margin-left:5px" title="Copy Execution name"><img alt="copy" src="../images/skin/database_table.png" > </span> &emsp;&emsp;   <input type="button" class=" buttons" value="Show" onclick="showDetails();"/> <br>
							<input id="execNameField" type="text" hidden="true"/>
						</td>
					</tr>
				</table>
				<table>
					<tr>
						<td style="width: 4%;">
						</td>
						<td style="width: 95%;">
							<!--  >div class="chartdivisionclass" id="chartdivision" style="width: 80%; height: 600px;">
							</div-->
						</td>
					</tr>
				</table>
				<div id = "executionDetails" style = "height:90%; width:90%; margin-left:5%"></div>
  	            <div id="resultAnalysisPopup" style="display: none; overflow: auto; width : 98%; height : 98%;"></div>        
			</div>
			<div id="showComparisonReport" style="display: none;">
				<div style="margin-left:50px;">
					<button style="font-weight: bold;font-size:15px;color:#2989b3;font-style: italic;font-family: Times New Roman;" onclick="helpDivToggle()" >i</button>
				</div>
				<p id="helpDivComparison" style="display: none; border-style: ridge;font-style: italic;width:90%;margin-left:50px;padding: 5px 5px 5px 5px;">Comparison report can be used to compare the execution results of a base execution with other 
					executions. For this, user has to select a single Base execution by either pasting the execution name in the 
					input box or selecting the execution by clicking on "Choose" button displayed to its right.
					Then User can select a list of comparison executions either by pasting the list of execution names separated by commas in the 
					text area provided (Min : 1 and Max : 10) or selecting the executions by clicking on "Choose" button displayed to its right.
					After selecting base execution and the comparison executions, click on the button "Generate Comparison Report" to generate the report
				</p>
				<g:form controller="execution" action="comparisonExcelReportGeneration">

					
					<table class="noClass" style="width:50%;margin-left:50px;">
						<tr >
							<td>Base Execution Name</td>
							<td style="width:50%;"><input type="text" id="baseExecutionName" name="baseExecutionName" placeholder="Give one execution name or choose" value="" style="width:90%;" required/><span class="required-indicator">*</span></td>		
							<td style="width:10px;">OR</td>
							<td><input type="button" class=" buttons" value="Choose" onclick="showBaseDetails();"/> <br></td>
						</tr>
						<tr >
							<td>Comparison Execution Names</td>
							<td style="width:50%;"><textarea type="text" id="comparisonExecutionName" name="comparisonExecutionNames" placeholder="Give list of execution names separated by comma (Min : 1 and Max : 10) or choose" style="height: 120px; width:90%;" required/></textarea><span class="required-indicator">*</span></td>		
							<td style="width:10px;vertical-align:middle;">OR</td>
							<td style="vertical-align:middle;"><input type="button" id="comparisonExecutionButton" class=" buttons" value="Choose" onclick="showComparisonDetails();"/> <br></td>
						</tr>
						<tr>
							<td></td>
							<td>
								<div id="comparisonReportDiv">
									<g:link onclick="return comparisonExcelReportGeneration()" id="comparisonReportLink">
										<span class = "buttons"><input type="button" style="font-weight: bold;" id="comparisonReportButton" value="Generate Comparison Report"><img src="../images/excel.png"  title = " Download Comparison Report(Excel)"/></span>
									</g:link>
								</div>
							</td>
						</tr>
					</table>
				</g:form>
			</div>
			<div id="baseExecutionPopUp" style="display: none; overflow: auto; width : 98%; height : 98%;" >	
				<div>
					<div>
		   			 	<div style="font-size:20px;font-weight: bold;text-align: center;position: relative;">
		   			 		Select Base Execution for Comparison Report Generation
		   			 	</div>
					</div>
					<div style="height : 20px;">
					</div>
				</div>
				<g:formRemote name="myBaseForm" update="searchFilterResultDivBase" method="GET"
								before="validateBaseInputFields();"
		              			action="${createLink(controller: 'trends', action: 'filterBaseExecutions')}"
		              			url="[controller: 'trends', action: 'filterBaseExecutions']"><br>
				<table>																
					<tr>
						<td valign="middle">From</td>
						<td valign="middle"><input type="text" id="generateFromDateBaseExec" name="generateFromDateBaseExec" required/><span class="required-indicator">*</span>
						</td>
						<td valign="middle">To</td>
						<td valign="middle"><input type="text" id="generateToDateBaseExec" name="generateToDateBaseExec" required/><span class="required-indicator">*</span>										
						</td>
						<td></td>
						<td valign="middle">
							<span class="buttons"><input type="submit" style="font-weight: bold;" name="filterBaseExecutions" value="Filter Executions">
							</span>
						</td>
					</tr>
					<tr>
						<td>Category</td>
						<td>
							<g:select id="categoryIdBaseExec" name="categoryBaseExec" from="${['RDKV','RDKB','RDKC' ,'RDKV_THUNDER']}" value="${params?.category}" required="required"/><span class="required-indicator">*</span>
						</td>
						<td>Box Type</td>
						<td id="boxTypeIdBaseExec">
							<select name="boxTypeBaseExec" id = "boxTypeBaseExec">
								<option value="">Please Select</option>
							</select>
						</td>
					</tr>
					<tr>
						<td>ScriptType</td>
						<td>											
							<select name="scriptTypeValueBaseExec" id="scriptTypeBase" onchange="showScriptTypesForBaseExec();" style="width: 150px">
								<option value="">All</option>
								<option value="Script">SINGLE SCRIPT</option>
								<option value="TestSuite">SCRIPTGROUP</option>												
							</select>
						</td>
						<td><span id="scriptLabelBaseId" style="display:none;">Script/ScriptGroup</span></td>
						<td><span id="scriptFieldBaseId" style="display:none;"><g:textField id="scriptValueBaseId" name="scriptValueBasicExec"/></span>									
						</td>
					</tr>
					<g:hiddenField name = "validate" id = "validate" value = ""/>
				</table>
				</g:formRemote>
				<span id="searchFilterResultDivBase" style="width: 100%;overflow: auto;"></span>
			</div>
			<div id="comparisonExecutionPopUp" style="display: none; overflow: auto; width : 98%; height : 98%;" >	
				<div>
					<div>
		   			 	<div style="font-size:20px;font-weight: bold;text-align: center;position: relative;">
		   			 		Select Comparison Executions
		   			 	</div>
					</div>
					<div style="height : 20px;">
					</div>
				</div>
				<g:formRemote name="myComparisonForm" update="searchFilterResultDivComparison" method="GET"
								before="validateComparisonInputFields();"
		              			action="${createLink(controller: 'trends', action: 'filterComparisonExecutions')}"
		              			url="[controller: 'trends', action: 'filterComparisonExecutions']"><br>
				<table>																
					<tr>
						<td valign="middle">From</td>
						<td valign="middle"><input type="text" id="generateFromDateComparisonExec" name="generateFromDateComparisonExec" required/><span class="required-indicator">*</span>
						</td>
						<td valign="middle">To</td>
						<td valign="middle"><input type="text" id="generateToDateComparisonExec" name="generateToDateComparisonExec" required/><span class="required-indicator">*</span>										
						</td>
						<td></td>
						<td valign="middle">
							<span class="buttons"><input type="submit" style="font-weight: bold;" name="filterBaseExecutions" value="Filter Executions">
							</span>
						</td>
					</tr>
					<tr>
						<td>Category</td>
						<td>
							<g:select id="categoryIdComparisonExec" name="categoryComparisonExec" from="${['RDKV','RDKB','RDKC' ,'RDKV_THUNDER']}" value="${params?.category}" required="required"/><span class="required-indicator">*</span>
						</td>
						<td>Box Type</td>
						<td id="boxTypeIdComparisonExec">
							<select name="boxTypeComparisonExec" id = "boxTypeComparisonExec">
								<option value="">Please Select</option>
							</select>
						</td>
					</tr>
					<tr>
						<td>ScriptType</td>
						<td>											
							<select name="scriptTypeValueComparisonExec" id="scriptTypeComparison" onchange="showScriptTypesForComparisonExec();" style="width: 150px">
								<option value="">All</option>
								<option value="Script">SINGLE SCRIPT</option>
								<option value="TestSuite">SCRIPTGROUP</option>												
							</select>
						</td>
						<td><span id="scriptLabelComparisonId" style="display:none;">Script/ScriptGroup</span></td>
						<td><span id="scriptFieldComparisonId" style="display:none;"><g:textField id="scriptValueComparisonId" name="scriptValueComparisonExec"/></span>									
						</td>
					</tr>
					<g:hiddenField id="finalBaseExecName" name="finalBaseExecName" value=""/>
					<g:hiddenField name = "validateComparison" id = "validateComparison" value = ""/>
				</table>
				</g:formRemote>
				<span id="searchFilterResultDivComparison" style="width: 100%;overflow: auto;"></span>
			</div>
			<div id="executionbased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black;">
					<tr>
						<td style="vertical-align: top;">&emsp;&emsp;&emsp;&emsp;Select
							Execution Names</td>
						<td id="executionNameList"><g:select id="executionId"
								multiple="true" style="height:200px;width:400px"
								name="execution" from="${executionList}" optionKey="" value=""
								class="many-to-one selectCombo" /></td>

						<td style="vertical-align: top;">Select Field To Compare</td>
						<td><g:select id="chartType1" name="chartType"
								from="${['ExecutionStatus', 'TimingInfo', 'CPU_Utilization','Memory_Utilization','Memory_Used_Percentage']}"
								value="${count}" required="" /></td>
						<td style="vertical-align: top;">Select chart Type</td>
						<td>
							<form>
								<input onclick="showBarChartBased()" type="radio"
									name="ChartType" id="bar" value="BarChart" checked="checked" />Script
								Group Wise <br> <input onclick="showLineChartBased()"
									type="radio" name="ChartType" id="line" value="LineChart" />Script
								Wise
							</form>
						</td>
						<td><g:submitToRemote class=" buttons" value="Compare"
								before="homePage();" onclick="showChart();" /> <br></td>
					</tr>

				</table>
				<table>
					<tr>
						<td align="left" width="60%"><input id="previous"
							type="button" value="Previous " onclick="previousPlot()"
							class="buttons" style="width: 9%" /></td>
						<td align="center" width="40%"><input id="next" type="button"
							value="Next" onclick="nextPlot()" class="buttons"
							style="width: 15%" /></td>
						<!-- my new add  -->
						<td align="right" width="99%" id="home"><img
							src="../images/skin/house.png" onclick="homePage()" height="28"
							width="28" title="First Page " /></td>
					</tr>
				</table>
			</div>
			<div id="devicebased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black;">
					<tr>
						<td style="vertical-align: middle;">Device</td>
						<td><g:select id="devices" name="devices"
								noSelection="['' : 'Please Select']"
								from="${Device?.findAllByCategory(category)}" required=""
								value="" optionKey="id" class="many-to-one selectCombo" /></td>
						<td style="vertical-align: middle;">ScriptGroup</td>
						<td><g:select id="scriptGrp" name="scriptGrp"
								noSelection="['' : 'Please Select']"
								from="${ScriptGroup?.findAllByCategory(category)}" required=""
								optionKey="id" class="many-to-one selectCombo" /></td>
						<td style="vertical-align: middle;">Select Field To Compare</td>
						<td><g:select id="chartType" name="chartType"
								from="${['ExecutionStatus', 'TimingInfo', 'CPU_Utilization','Memory_Utilization','Memory_Used_Percentage']}"
								value="${count}" required="" /></td>
						<td style="vertical-align: middle;">Result No's</td>
						<td><g:select id="resultCount" name="result.count"
								from="${2..10}" value="${count}" style="width:45px;" required="" />
						</td>
						<td style="vertical-align: top;">Select chart</td>
						<td>
							<form>
								<input type="radio" name="ChartType1" id="bar" value="BarChart"
									checked="checked" />Script Group Wise <br> <input
									type="radio" name="ChartType1" id="line" value="LineChart" />Script
								Wise
							</form>
						</td>
						<td><g:submitToRemote class=" buttons" value="Compare"
								onclick="showChart1();" before="homePage()" /> <br></td>
					</tr>
				</table>
				<table>
					<tr>
						<td align="left" width="60%"><input id="previous1"
							type="button" value="Previous " onclick="previousPlot()"
							class="buttons" style="width: 9%; display: none" /></td>
						<td align="center" width="50%"><input id="next1"
							type="button" value="Next" onclick="nextPlot()" class="buttons"
							style="width: 15%; display: none" /></td>
						<td align="right" width="99%" id="home1"><img
							src="../images/skin/house.png" onclick="homePage()" height="28"
							width="28" title="First Page" /></td>
						<script type="text/javascript">
							var elem = document.getElementById("home1");
							elem.style.display = "none";
						</script>
					</tr>
				</table>
				
			</div>
			<div id="buildnamebased" style="display: none;">
				<table class="noClass" style="border: 1; border-color:black ;width:70%;  "   >
					<tr >
						<td style="vertical-align: middle;" >
							&emsp;&emsp;&emsp;&emsp;Build Name  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
							<g:select id="buildname" name="buildname"  noSelection="['' : 'Please Select']" from="" value="" class="many-to-one " />
						</td>
						<td>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<input onclick="showBuildGroupBased();" type="radio" name="BuildOption" value="BuildGroupBased"  checked=true />
							&emsp;&emsp;Show Results by Script Group&emsp;
						</td>
						<td>
							<input onclick="showBuildScriptBased();" type="radio" name="BuildOption" value="BuildScriptBased"/>
							&emsp;&emsp;Show Results by Script&emsp;
							
						</td>		
					</tr>
				</table>
				
			</div>
			<div id="buildscriptbased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black;width:80%;  " >
					<tr >
						<td style="vertical-align: middle;" >
							&emsp;&emsp;&emsp;&emsp;Select Script
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<g:select id="buildscriptname"  style="height:200px;width:400px"  name="buildscriptname" noSelection="['' : 'Please Select']" from="${scriptList}" value="" class="many-to-one selectCombo"/></td>
											
						<td style="vertical-align: middle;">Result No's</td>
						<td><g:select id="resultBuildCount" name="result.count"
								from="${2..10}" value="${count}" style="width:45px;" required="" />
						</td>
						<td >&emsp;&emsp;&emsp;&emsp;<g:submitToRemote class=" buttons" value="Show"
								onclick="getBuildScriptChartData();" before="getBuildScriptChartData();"/> <br></td>
					</tr>
				</table>
				<table>
				<tr>
					<td style="width: 4%;"></td>
					<td style="width: 70%;">
						<div class="chartdivBuildScriptclass" id="chartdivBuild1" style="width: 100%; height: 500px;"></div>
					</td>
					<td style="width: 23%;">
						<div class="chartdivBuildScriptclass" id="chartdivBuild" style="width: 100%; height: 364px;"></div>
					</td>
				</tr>
			</table>
			</div>

			<div id="buildgroupbased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black; width:60%; " >
					<tr >
						<td style="vertical-align: middle;" >&emsp;&emsp;&emsp;&emsp;Select Script Group																		
						&emsp;&emsp;&emsp;<g:select id="buildscriptgroupsname"  name="buildscriptgroupsname" noSelection="['' : 'Please Select']" from="${ scriptGrpList}" value="" class="many-to-one selectCombo"/></td>
						<td style="vertical-align: middle;" >Result No's</td>
						<td><g:select id="resultBuildGrpCount" name="result.count"
								from="${2..10}" value="${count}" style="width:45px;" required="" />
						</td>
						
						<td >&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<g:submitToRemote class=" buttons" value="Show"
								onclick="showBuildScriptGroupChart();" before="showBuildScriptGroupChart();"/> <br></td>
					</tr>
				</table>
				<table>
					<tr><td style="width: 4%;"></td>
						<td style="width: 95%;"><div class="chartdivisionbuildclass" id="chartdivisionsbuild" style="width: 80%; height: 600px;"></div></td>
					<tr>
				</table>
			</div>
			<div id="scriptbased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black; width : 100%" >
					<tr >
						<td style="vertical-align: middle;">&emsp;&emsp;&emsp;&emsp;Device</td>
						<td>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<g:select id="device" name="device" noSelection="['' : 'Please Select']"
								from="${Device?.findAllByCategory(category)}" required=""
								value="" optionKey="id" class="many-to-one selectCombo" /></td>
						<td style="vertical-align: middle;" >Select Script</td>
						<td ><g:select id="script" name="script" noSelection="['' : 'Please Select']"	style="height:200px;width:400px" from="${scriptList}" required="" value="" class="script"  /></td>	
						<td style="vertical-align: middle;" >Result No's</td>
						<td ><g:select id="resultcount" name="result.count" from="${2..10}" value="${count}" style="width:45px;" required="" /></td>
						<td >&emsp;&emsp;&emsp;&emsp;<g:submitToRemote class=" buttons" value="Show"
								onclick="showScriptChart();" before="showScriptChart();"/> <br></td>
					 </tr>
				</table>
				<table>
					<tr>
					<td style="width: 4%;"></td>
					<td style="width: 70%;">
							<div class="chartdivBoxtypeclass" id="chartdivScript1" style="width: 100%; height: 500px;"></div>
						</td><td style="width: 23%;">
							<div class="chartdivBoxtypeclass" id="chartdivScript" style="width: 100%; height: 364px;"></div>
						</td>
					</tr>
				</table>

			
			</div>
			

			<div id="boxtypebased" style="display: none;">
				<table class="noClass" style="border: 1; border-color:black ;width:70%;  "   >
					<tr >
						<td style="vertical-align: middle;" >
							&emsp;&emsp;&emsp;&emsp;Box Type &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
							<g:select id="boxtype" name="boxtype" noSelection="['' : 'Please Select']"	from="${BoxType?.findAllByCategory(category)}" required="" value="" optionKey="id" class="many-to-one " /></td>
						<td>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<input onclick="showBoxGroupBased();" type="radio" name="BoxOption" value="BoxGroupBased" checked=true/>
							&emsp;&emsp;Show Results by Script Group&emsp;
						</td>
						<td>
							<input onclick="showBoxScriptBased();" type="radio" name="BoxOption" value="BoxScriptBased"/>
							&emsp;&emsp;Show Results by Script&emsp;
							
						</td>		
					</tr>
				</table>
			</div>
			<div id="boxscriptbased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black;width:80%;  " >
					<tr >
						<td style="vertical-align: middle;" >
							&emsp;&emsp;&emsp;&emsp;Select Script
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<g:select id="scriptname" style="height:200px;width:400px" name="scriptname" noSelection="['' : 'Please Select']" from="${scriptList}" value="" class="many-to-one selectCombo"/></td>
											
						<td style="vertical-align: middle;" >Result No's</td>
						<td ><g:select id="resultCounts" name="result.count"
								from="${2..10}" value="${count}" style="width:45px;" required="" />
						</td>
						<td >&emsp;&emsp;&emsp;&emsp;<g:submitToRemote class=" buttons" value="Show"
								onclick="showBoxTypeChart();" before="getBoxTypeScriptChartData();"/> <br></td>
					</tr>
				</table>
				<table>
				<tr>
					<td style="width: 4%;"></td>
					<td style="width: 70%;">
						<div class="chartdivScriptclass" id="chartdivBoxType1" style="width: 100%; height: 500px;"></div>
					</td>
					<td style="width: 23%;">
						<div class="chartdivScriptclass" id="chartdivBoxType" style="width: 100%; height: 364px;"></div>
					</td>
				</tr>
			</table>
			</div>

			<div id="boxgroupbased" style="display: none;">
				<table class="noClass" style="border: 1; border-color: black; width:60%; " >
					<tr >
						<td style="vertical-align: middle;" >&emsp;&emsp;&emsp;&emsp;Select Script Group																		
						&emsp;&emsp;&emsp;<g:select id="scriptgroupsname" style="height:200px;width:200px" name="scriptgroupsname" noSelection="['' : 'Please Select']" from="${ scriptGrpList}" value="" class="many-to-one selectCombo"/></td>

						<td style="vertical-align: middle;" >Result No's</td>
						<td ><g:select id="resultGroupCounts" name="result.count"
								from="${2..10}" value="${count}" style="width:45px;" required="" />
						</td>
						<td >&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<g:submitToRemote class=" buttons" value="Show"
								onclick="showBoxTypeScriptGroupChart();" before="showBoxTypeScriptGroupChart();"/> <br></td>
					</tr>
				</table>
				<table>
					<tr><td style="width: 4%;"></td>
						<td style="width: 95%;"><div class="chartdivisionclass" id="chartdivisions" style="width: 80%; height: 600px;"></div></td>
					
				</table>
			</div>
			<div class="chartdivclass" id="chartdiv" style="width: 100%; height: 600px;"></div>
	</div>
	</body>
</html>