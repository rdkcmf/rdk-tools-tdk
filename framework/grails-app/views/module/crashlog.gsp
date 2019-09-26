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
<%@ page import="com.comcast.rdk.Module" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${category} ${message(code: 'module.label', default: 'Add Crash LogFile Path')}" />
		<title><g:message code="default.create.label" args="[entityName]" /></title>
		<g:javascript library="jquery.table.addrow" />
		<script type="text/javascript">
			(function($){
				$(document).ready(function(){
					$(".addRow").btnAddRow();
					$(".delRow").btnDelRow();
			});
			})(jQuery);
		</script>
	</head>
	<body>
	<g:form controller="module" action="saveCrashLogs" >
		<a href="#show-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<g:hiddenField name="category" value="${category}"/>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="<g:createLink params="[category:category]" action="configuration" controller="module"/>"><g:message code="default.home.label"/></a></li>
			</ul>
		</div>
		<div id="show-module" class="content scaffold-show" role="main">
		
			<h1>Add Crash LogFile Path</h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>

			<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'logFileNames', 'error')} ">
		<table style="width:50%;">
		<tr>
			<td>Select Module</td>
			<td>&nbsp;&nbsp;
			<g:select id="module" name="module.id" from="${moduleInstanceList}" noSelection="['' : 'Please Select']" 
				optionKey="id" required="" value="" class="many-to-one"
				onchange="${remoteFunction(action:"getFileList",update:"propData", params: " \'moduleid=\' + this.value")}" />
			</td>
		</tr>
		
		<tr>
			<td>
				<g:message code="module.logFileNames.label" default="LogFile Names" />
			</td>
			<td><div id="propData">

			</div>	
				<table  style="width:15%;">
						<tr>	
							<td>
								<g:textField name="logFileNames" value="" type="text" />
							</td>
							<td>
								<img class="addRow"
							        src="${resource(dir:'images/',file:'addRow.png')}"
							        alt="Add" border="0"
							        title="Add" /></td>
						        
							<td>
								<img class="delRow"
							        src="${resource(dir:'images/',file:'removeRow.png')}"
							        alt="Remove" border="0"
							        title="Remove" />
							</td>
						</tr>						
				</table>
			</td>
		</tr>		
	</table>
</div>

		</div>
		
		<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'module', 'error')} required">
	<label for="module">		
	</label>
	<span class="buttons">
	<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
	</span>
</div>
</g:form>
	</body>
</html>


