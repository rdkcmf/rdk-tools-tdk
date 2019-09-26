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
<%@page import="com.comcast.rdk.TestGroup"%>
<%@ page import="com.comcast.rdk.Module" %>
	
<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="module.name.label" default="Module Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${moduleInstance?.name}"/> 	
</div>
<g:hiddenField name="category" id="category" value="${category }"/>
<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'testGroup', 'error')} required">
	<label for="testGroup">
		<g:message code="module.testGroup.label" default="Test Group" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="testGroup" from="${com.comcast.rdk.TestGroup?.values()}" keys="${com.comcast.rdk.TestGroup.values()*.name()}" required="" value="${moduleInstance?.testGroup?.name()}"/>
</div>

<%--<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'rdkVersion', 'error')} required">
	<label for="name">
		<g:message code="module.rdkVersion.label" default="RDK Version" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="rdkVersion" required="" value="${moduleInstance?.rdkVersion}"/> 	
</div>

--%><div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'executionTime', 'error')} required">
	<label for="name">
		<g:message code="module.executionTime.label" default="Execution TimeOut" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="executionTime" required="" value="${moduleInstance?.executionTime}"/> 	
</div>

<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'name', 'error')} required">
	<label for="name">
	</label>
	<span class="buttons"><g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
</div>

