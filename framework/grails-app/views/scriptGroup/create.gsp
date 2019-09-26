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
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<%@ page import="org.apache.shiro.SecurityUtils"%>
<%@ page import="com.comcast.rdk.User" %>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'demo_table.css')}" type="text/css" />
<g:javascript library="jquery-1.10.2.js"/>
<g:javascript library="jquery-ui"/>
<link rel="stylesheet" href="${resource(dir:'css',file:'style.css')}">
<style>
#sortable {
	list-style-type: none;
	margin: 0;
	padding: 0;
	width: 100%;
	border-style : solid;
	border-width:1px;
	border-color:#B6E8F5;
}

#sortable li {
	margin: 0 1px 1px 1px;
	padding: 0.4em;
	padding-left: 1.5em;
	font-size: 2.5;
	height: 7px;
	overflow: hidden;
}

#sortable li span {
	position: absolute;
	margin-left: -1.3em;
}

#feedback {
	font-size: 1.4em;
}

#selectable .ui-selecting {
	background: #FECA40;
}

#selectable .ui-selected {
	background: #F39814;
	color: white;
}

#selectable {
	list-style-type: none;
	margin: 0;
	padding: 0;
	width: 100%;
	border-style : solid;
	border-width:1px;
	border-color:#B6E8F5;
}

#selectable li {
	margin: 0 1px 1px 1px;
	padding: 0.4em;
	padding-left : 8px
	font-size: 2.5;
	height: 10px;
	overflow: hidden;
}

#sortable li .handle {
	background: #CC6633;
	position: absolute;
	left: 0;
	top: 0;
	bottom: 0;
	padding: 0.4em;
	width: 8px
}

#sortable .ui-selecting {
	background: #FECA40;
}

#sortable .ui-selecting .handle {
	background: #FFFF99;
}

#sortable .ui-selected {
	background: #F39814;
}

#sortable .ui-selected .handle {
	background: #FFFF99;
}

#sortable ul {
	width: 300px;
	list-style: none;
	margin: 0;
	padding: 0;
}

#sortable li {
	background: white;
	position: relative;
	margin: 0 3px 3px 3px;
	list-style: none;
	font-size: 2.5;
	height: 8px;
	overflow: hidden;
}
</style>
<script>
	$(function() {
		 $( "#selectable" ).selectable({
			 stop: function() {
			 var result = $( "#select-result" ).empty();
			 var data = ""
			 var myArray = [];
			 
			 $( ".ui-selected", this ).each(function() {
			 var index = $( "#selectable li" ).index( this );
			 data = data +"," +(index +1)
			 result.append( " #" + ( index + 1 ) );
			 myArray.push(this.id)
			 });
			 document.getElementById("resultElement").value = myArray;
			 }
			 });
		
	});
</script>
</head>
<g:set var="entityName" value="${message(code: 'scriptGroup.label', default: 'TestSuite')}" />
		<a href="#create-scriptGroup" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>		
		<div id="create-scriptGroup" class="content scaffold-create" role="main">
			<h1><g:message code="default.create.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			<g:hasErrors bean="${scriptGroupInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${scriptGroupInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<g:form action="save">
			<input type="hidden" id = "scriptElement" name="scriptElement">
			<input type="hidden" id = "resultElement" name="resultElement">
			<input type="hidden" id = "sgResultElement" name="sgResultElement">
			<br>
			<label for="name">
		<g:message code="scriptGroup.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField id= "scriptName" name="name" required="" value="${scriptGroupInstance?.name}" style="width: 240px"/>
	
			<table name="scripttable">
			<tr>
				<td name="selectabletd" style="width: 45%">
					<div class="selectablediv" name ="selectablediv"> 
					<br>
					<label>All Scripts</label> <br>
					<ul class= "selectable" id="selectable" name ="selectable"  title="selectable" style="max-height : 454px; max-width : 380px; overflow: auto; ">
						<g:each in='${scriptInstanceList}' var="script">
						<% 
							String idScript = script?.id;
 					     %>
							<li id = "script-${idScript}" class="ui-state-default">								
								${script?.scriptName} 
							</li>
						</g:each>
					</ul>
					</div>
				</td>
				<td style="width: 5%">
				<br><br><br><br>
				<input type="image" src= "../images/arrow_right.png" onclick="addScripts();return false;"  title = " Add Scripts" ><br><br>
				<input type="image" src= "../images/arrow_left.png" onclick="removeScripts();return false;"  title = "Remove Scripts">
				</td>
				<td name="sortabletd"style="width: 45%">
				<br>
				<br>				
					<ul name ="sortable" id="sortable" style="min-height : 454px; min-width : 250px; max-height : 350px; max-width : 380px; overflow: auto;">
						<g:if test="${category == 'RDKV' || category == 'RDKB'} ">
							<g:if test="${scriptGroupInstance}">
								<g:each in='${scriptGroupInstance.scriptList}' var="script">
									<li class="ui-state-default" title="${script.scriptName}">
										<g:hiddenField name="test" id="test"
											value="${script.scriptName}" /> ${script.scriptName}
									</li>
								</g:each>
							</g:if>
							<g:else>
								<li class="ui-state-default">No scripts in list</li>
							</g:else>
						</g:if>
						<g:elseif test="${category == "RDKB_TCL"}">
							<g:if test="${scriptGroupInstance}">
								<g:each in='${scriptGroupInstance.scriptList}'
									var="script">
									<li class="ui-state-default" title="${script.scriptName}">
										<g:hiddenField name="test" id="test"
											value="${script.scriptName}" /> ${script.scriptName}
									</li>
								</g:each>
							</g:if>
							<g:else>
								<li class="ui-state-default">No scripts in list</li>
							</g:else>
						</g:elseif>
					</ul>					
				</td>
				<td style="width: 5%">
					<br><br>
					<input type="image" src= "../images/reorder_up.png" onclick="moveUp();return false;"  title  = " Move Up"> <br><br>
					<input type="image" src="../images/reorder_down.png" onclick="moveDown();return false;"  title  = "Move Down">
				</td>
			</tr>
		</table>
		<g:hiddenField name="createCategory"  id="createCategory" value="${category}"/>
			<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
				<div style="width : 100%;text-align: center;">
					<span class="buttons">
						<input type="button" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" onclick="createSG();return false;">
					</span>
				</div>
				</g:if>
			</g:form>
		</div>

