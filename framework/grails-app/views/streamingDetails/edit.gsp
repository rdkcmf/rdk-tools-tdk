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
<%@ page import="com.comcast.rdk.StreamingDetails" %>
<%@ page import="com.comcast.rdk.RadioStreamingDetails" %>
				
<div id="edit-streamingDetails" class="content scaffold-edit" role="main">
	<g:set var="entityName" value="${message(code: 'streamingDetails.label', default: 'StreamingDetails')}" />
	<h1><g:message code="default.edit.label" args="[entityName]" /></h1>
	<g:if test="${flash.message}">
	<div class="message" role="status">${flash.message}</div>
	</g:if>
	<g:hasErrors bean="${streamingDetailsInstance}">
	<ul class="errors" role="alert">
		<g:eachError bean="${streamingDetailsInstance}" var="error">
		<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
		</g:eachError>
	</ul>
	</g:hasErrors>
	<g:form method="post" >
		<g:hiddenField name="id" value="${streamingDetailsInstance?.id}" />
		<g:hiddenField name="version" value="${streamingDetailsInstance?.version}" />
		<fieldset class="form">
			<g:render template="form"/>
		</fieldset>
		<div style="width : 100%;text-align: center;">
			<span class="buttons">
			<g:actionSubmit class="save" action="update" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
			<span class="buttons"><g:actionSubmit class="delete" action="delete" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
		</div>
	</g:form>
</div>
