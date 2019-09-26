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
<%@ page import="com.comcast.rdk.DeviceGroup" %>
		
<div id="create-deviceGroups" class="content scaffold-create" role="main">
	<g:set var="entityName" value="${category} ${message(code: 'deviceGroups.label', default: 'DeviceGroups')}" />
	<h1><g:message code="default.create.label" args="[entityName]" /></h1>
	<g:if test="${flash.message}">
	<div class="message" role="status">${flash.message}</div>
	</g:if>
	<g:hasErrors bean="${deviceGroupsInstance}">
	<ul class="errors" role="alert">
		<g:eachError bean="${deviceGroupsInstance}" var="error">
		<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
		</g:eachError>
	</ul>
	</g:hasErrors>
	<g:form action="save" >
		<fieldset class="form">
			<g:render template="form" model="[devices:devices, category:category]"/>
		</fieldset>
		<div style="width:100%;text-align: center;">
			<span class="buttons"><g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
		</div>
		<%--<fieldset class="buttons">			
		</fieldset>--%>
		</g:form>
</div>
