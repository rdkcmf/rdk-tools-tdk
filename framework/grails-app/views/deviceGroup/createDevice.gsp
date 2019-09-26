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
<%@ page import="com.comcast.rdk.Device" %>
<g:javascript library="devicegrp_resolver" />
<div id="create-device" class="content scaffold-create" role="main">
	<g:set var="entityName"
		value="${category} ${message(code: 'device.label', default: 'Device')}" />
	<h1>
		<g:message code="default.create.label" args="[entityName]" />
	</h1>
	<g:if test="${flash.message}">
		<div class="message" role="status">
			${flash.message}
		</div>
	</g:if>
	<g:hasErrors bean="${deviceInstance}">
		<ul class="errors" role="alert">
			<g:eachError bean="${deviceInstance}" var="error">
				<li
					<g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message
						error="${error}" /></li>
			</g:eachError>
		</ul>
	</g:hasErrors>
	<div id="messageDiv" class="message" style="display: none;"></div>

	<g:form action="saveDevice" controller="deviceGroup"
		enctype="multipart/form-data">
		<input type="hidden" name="url" id="url" value="${url}">
		<fieldset class="form">
			<g:render template="formDevice" model="[category:category]" />
		</fieldset>
		<div id="streamdiv"></div>
		<br>
		<div style="width: 100%; text-align: center;">
			<span id="createDevice" class="buttons"><g:submitToRemote
					name="create" class="save" action="saveDevice"
					controller="deviceGroup" update="messageDiv"
					value="${message(code: 'default.button.create.label', default: 'Create')}"
					before="isDeviceExist(document.getElementById('stbName').value);"
					onSuccess="updateDeviceList(document.getElementById('stbName').value);">
				</g:submitToRemote>&emsp; </span>
		</div>
	</g:form>
	<div>
		<g:if test="${category?.toString()?.equals('RDKB')}">
			<div style="padding-left: 33%; padding-top: 2%;" id="toggleOptions">
				<input type="radio" name="configType" value="PythonE2E" checked>Python
				E2E&nbsp;&nbsp; <input type="radio" name="configType" value="TCLE2E">TCL
				E2E
			</div>
			<div style="padding-left: 17%; padding-top: 1%;" id="uploadConfig">
				<g:form enctype="multipart/form-data" name="uploadForm">Upload Configuration file <input
						type="file" name="configFile" id="file" />
					<input type="button" value="UPLOAD" onclick="uploadConfig()" />
				</g:form>
			</div>
			<div style="padding-left: 17%; padding-top: 2%;" id="uploadStatus"></div>
		</g:if>
	</div>
</div>

