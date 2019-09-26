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
<%@ page import="com.comcast.rdk.Function" %>
<%@ page import="com.comcast.rdk.Module" %>
<%@ page import="com.comcast.rdk.User" %>
<%@ page import="com.comcast.rdk.Groups" %>
<%@ page import="org.apache.shiro.SecurityUtils" %>

<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="function.name.label" default="Function Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${functionInstance?.name}"/>
</div>
<%
	def user = User.findByUsername(SecurityUtils.subject.principal)
	def group = Groups.findById(user.groupName?.id)
%>
<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'module', 'error')} required">
	<label for="module">
		<g:message code="function.module.label" default="Module" />
		<span class="required-indicator">*</span>
	</label>
	<g:select id="module" name="module.id" from="${modules}" noSelection="['' : 'Please Select']" 
			optionKey="id" required="" value="${functionInstance?.module?.id}" class="many-to-one"/>
</div>

<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'module', 'error')} required">
	<label for="module">		
	</label>
	<span class="buttons">
	<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
	</span>
</div>
<g:hiddenField name="category" id="category" value="${category }"/>
