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
		<g:set var="entityName" value="${message(code: 'module.label', default: 'Module')}" />
		<title><g:message code="default.create.label" args="[entityName]" /></title>			
	</head>
	<body>
		<a href="#create-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" params="[category:category]"  href="${createLink(uri: '/module/configuration')}"><g:message code="default.home.label"/></a></li>
				<li><g:link class="list" params="[category:category]" action="list"><g:message code="default.list.label" args="[entityName]" /></g:link></li>
				</ul>
		</div>	
		<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
		</g:if>
		
		<div id="create-parameterType" class="content scaffold-create" role="main">
			<br>
			<br>
		
			<g:set var="entityName2" value="${message(code: 'parameter.label', default: 'Parameter')}" />
			<h1><g:message code="default.create.label" args="[entityName2]" /></h1>			
			<g:hasErrors bean="${parameterTypeInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${parameterTypeInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<g:form action="saveParameter" >
				<fieldset class="form">
					<g:render template="parametertypeform" model="[category:category]"/>
				</fieldset>
				<%-- <fieldset class="buttons">
					<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
				</fieldset> --%>
			</g:form>
		</div>		
		</body>
</html>
		
