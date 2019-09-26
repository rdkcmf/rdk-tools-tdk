<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2019 RDK Management

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
	
<g:javascript library="chart/jquery.jqplot.min" />
<g:javascript library="chart/shCore.min" />
<g:javascript library="chart/shBrushJScript.min" />
<g:javascript library="chart/shBrushXml.min" />
<g:javascript library="chart/jqplot.barRenderer.min" />
<g:javascript library="chart/jqplot.pieRenderer.min" />
<g:javascript library="chart/jqplot.categoryAxisRenderer.min" />
<g:javascript library="chart/jqplot.pointLabels.min" />
<g:javascript library="chart/jqplot.canvasTextRenderer.min" />
<g:javascript library="chart/jqplot.canvasAxisLabelRenderer.min" />
<g:javascript library="chart/jqplot.canvasAxisTickRenderer.min" />
<g:javascript library="jquery.more" />
<g:javascript library="select2" />
<g:javascript library="chartview" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'select2.css')}"
	type="text/css" />
<script type="text/javascript">
$(document).ready(function() {
	getScriptBasedChartData();
});

</script>
<body>
    <div id="analysisDiv" style= "width:100%; height:90px"> 
	<div id="tableDiv" style = "width:93%;  float:left; height:60px; margin-bottom:5px">
	    <h4>Defect Details</h4>
		<table style="border: solid 1px #A7A7A7; margin-bottom:5px; width:100%">
			<tr>
				<th style="width:40%">Script Name</th>
				<th style="width:20%">Defect Type</th>
				<th style="width:20%">Ticket Details</th>
				<th style="width:20%">Remarks</th>
			</tr>
			<tr>
				<g:hiddenField name="boxType" id="boxType" value ="${boxTypeId}"/>
				<g:hiddenField name="executionId" id="executionId" value ="${executionId}"/>
				<g:hiddenField name="statusList" id="statusList" value ="${statusList}"/>
				<td id="scriptName">
					${scriptName}
				</td>
				<td>
                     <g:select id="defectType" name="defectType"  noSelection="['' : 'Please Select']" from="${['RDK Issue', 'Script Issue', 'Environment Issue']}" required="" value="${defectType}" 
                     	class="many-to-one selectCombo"/>										
				</td>
				<td><input type="text" id="ticketNo"  name="ticketNo" value="${ticketNo}" required="" />
				</td>
				<td>
					<input list ="remarksList" name="remarks" id="remarks" value = "${remarks}"/>
					<datalist id="remarksList">
                		<option value="Interface Change"/>
        				<option value="New Issue"/>
   					</datalist>										
				</td>
			</tr>
		</table>
	    </div>
	    <div id = "saveDiv" style="width:7%; float:right; height:60px">
	       <input type="button" value="Save" class="buttons" style="float:right; margin-top:25px"
                onclick="saveData(${executionId},'${scriptName}')"/>
	    </div>
        <div id="msgDiv" style="width:100%; height:20px; float:left; margin-top:5px">
         <div id="savedMessage" style = "display:none"> Data saved successfully </div>
       	

                 
         <g:link controller="execution" action="showExecutionResult" style="margin-right: 20px; float:right" 
         	id="1" params="[execResult:"${execResultId}"]" target = "_blank">Execution Log</g:link>
         <g:link controller="execution" action="showAgentLogFiles" style="margin-right: 20px; float:right"
         	params="[execResId:"${execResultId}", execDeviceId:"${execDeviceId}", execId:"${executionId}"]" target = "_blank"> Agent Console Log</g:link>
         </div>
        
	</div>
	<div id ="execHistoryDiv" style="margin-top:5px" > <h4>Execution History</h4>
	   
		<span>Box type</span>
		<g:select id="searchBoxType" name="searchBoxType"  noSelection="['' : 'All']" from="${boxTypes}" value="${selectedBoxType}" 
                     	class="many-to-one selectCombo" style = "width:100px"/>	
        <span>No:of entries</span>
		<g:select id="noOfEntries" name="noOfEntries"  noSelection="['' : '5']" from="${['5','6','7','8','9','10']}" value="${noOfEntries}" 
                     	class="many-to-one selectCombo" style = "width:100px"/>	
         <input type="button" value="Search" class="buttons"
            onclick="searchData('${executionId}', '${execDeviceId}', '${execResultId}', '${scriptName}', '${selectedboxType}')" style="width: 50px; height: 20px;
             margin-left: 10px; margin-bottom: 5px;"/>
      <g:if test="${execHistory.size() > 0}">
		<table>
			<tr>
				<td style="width: 70%;">
					<div  class="chartdivisionclass" id="scriptBasedChart" style="width:80%; height: 200px;">
						</div>
				</td>
			</tr>				
		</table>
		<table>
			<tr>
				<th>Execution Name</th>
				<th>Box Type</th>
				<th>Status</th>
				<th>Defect Type</th>
				<th>Ticket No</th>
				<th>Remarks</th>
				<th>Execution Log</th>
				<th>Agent Console Log</th>
				<th>Use the defect details</th>
			</tr>
			<g:each in="${execHistory}" status="i" var="row">
				<tr>
					<td>
						${row.execName}
					</td>
					<td>
						${row.boxType}
					</td>
					<td>
						${row.status}
					</td>
					<td>
						${row.defectType}
					</td>
					<td>
						${row.ticketNo}
					</td>
					<td>
						${row.remarks}
					</td>
					<td>
					 	<g:link controller="execution" action="showExecutionResult" style="margin-right: 20px; float:right" 
        				id="1" params="[execResult:"${row.executionResultId}"]" target = "_blank">Execution Log</g:link>
					</td>
					<td>
						<g:link controller="execution" action="showAgentLogFiles" style="margin-right: 20px; float:right"
         				params="[execResId:"${row.executionResultId}", execDeviceId:"${row.executionDeviceId}", execId:"${row.execId}"]" target = "_blank"> Agent Console Log</g:link>
					</td>
					<td style="text-align:center;">
						<g:hiddenField name="defectType" id="defectType_${row.execId}" value ="${row.defectType}"/>
						<g:hiddenField name="ticketNo" id="ticketNo_${row.execId}" value ="${row.ticketNo}"/>
						<g:hiddenField name="remarks" id="remarks_${row.execId}" value ="${row.remarks}"/>
						<g:if test="${(row.defectType != null) || (row.ticketNo != null) || (row.remarks != null)}">
							<g:radio name="radioButton" id="radioButtonId_${row.execId}" onclick="fillDefectDetails('${row.execId}')" value="" title="Auto Fill the defect details"/>
						</g:if>
						<g:else>
							<g:radio name="radioButton" id="radioButtonId_${row.execId}" onclick="fillDefectDetails('${row.execId}')" value="" disabled="true" title="Auto Fill the defect details"/>
						</g:else>
					</td>
				</tr>
			</g:each>
		</table>
    </g:if>
    <g:else> 
         <div style="margin-top: 10px; margin-left:5px"> No data found!! </div>
    </g:else>
    </div>
</body>