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
<%--<!DOCTYPE html>--%>
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
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'select2.css')}"
	type="text/css" />

<script  type="text/javascript">
	$(document).ready(function(){
		var id= $('#id').val();
		$.get('showDetailedData', {id: id}, function(data) {$("#executionDetails").html(data); });	
	}); 
</script>
</head>
<body>
	<g:hiddenField name="id" value="${name}" />
    <div id = "executionDetails" style = "height:90%; width:90%; margin-left:5%;margin-top:20px;"></div>
    <div id="resultAnalysisPopup" style="display: none; overflow: auto; width : 98%; height : 98%;"></div>        
</body>
</html>