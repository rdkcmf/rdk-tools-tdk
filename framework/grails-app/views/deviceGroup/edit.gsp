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
<%@ page import="com.comcast.rdk.Device" %>
<!DOCTYPE html>

	<div id="edit-deviceGroups" class="content scaffold-edit" role="main">
	<g:set var="entityName" value="${message(code: 'deviceGroups.label', default: 'DeviceGroups')}" />
		<h1><g:message code="default.edit.label" args="[entityName]" /></h1>
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
		<g:form method="post" >
			<g:hiddenField name="id" value="${deviceGroupsInstance?.id}" />
			<g:hiddenField name="version" value="${deviceGroupsInstance?.version}" />
			<fieldset class="form">
				<div class="fieldcontain ${hasErrors(bean: deviceGroupsInstance, field: 'name', 'error')} required">
					<label for="name">
						<g:message code="deviceGroups.name.label" default="Name" />
						<span class="required-indicator">*</span>
					</label>
					<g:textField name="name" required="" value="${deviceGroupsInstance?.name}" style="width: 200px"/>
				</div>
				
				<div class="fieldcontain ${hasErrors(bean: deviceGroupsInstance, field: 'devices', 'error')} ">
					<label for="devices">
						<g:message code="deviceGroups.devices.label" default="Devices" />		
					</label>		
					<g:select style="width: 210px;height: 410px" name="devices" from="${com.comcast.rdk.Device.findAllByCategory(deviceGroupsInstance?.category).stbName}" value="${deviceGroupsInstance?.devices.stbName}" />			
					<%--<g:select style="width: 140px" name="devices" from="${com.comcast.rdk.Device.list().stbName}" multiple="multiple" size="5" value="${deviceGroupsInstance?.devices*.stbName}" class="many-to-many"/>				
				--%></div>				
			</fieldset>
			<%--<fieldset class="buttons">
				--%>
			<div style="width : 90%;text-align: center;">
				<span class="buttons"><g:actionSubmit class="save" action="update" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
				<span class="buttons"><g:actionSubmit class="delete" action="delete" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
			</div>
			<%--</fieldset>
		--%></g:form>
	</div>
	
