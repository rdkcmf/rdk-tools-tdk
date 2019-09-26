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
<%@ page import="com.comcast.rdk.Groups"%>
<!DOCTYPE html>
<html>
<head>
<meta name="layout" content="main">
<g:set var="entityName"
	value="${message(code: 'groups.label', default: 'Groups')}" />
<title><g:message code="default.create.label"
		args="[entityName]" /></title>
<g:javascript library="validations" />
</head>
<body>
	<g:form controller="groups">
		<a href="#create-groups" class="skip" tabindex="-1"><g:message
				code="default.link.skip.label" default="Skip to content&hellip;" /></a>
		<div class="nav" role="navigation">
			<ul>
				<%--<li><a class="home"
					href="${createLink( params:'[category:"category"]',controller:'module', action:'configuration')}"><g:message
							code="default.home.label" /></a></li>
			--%>
			<li><a class="home"
					href='<g:createLink params="[category:category]" action="configuration" controller="module"/>'><g:message
							code="default.home.label" /></a></li>
			</ul>
			
		</div>
		<div id="create-groups" class="content scaffold-create" role="main">
			<h1>
				<g:message code="default.create.label" args="[entityName]" />
			</h1>
			<g:if test="${flash.message}">
				<div class="message" role="status">
					${flash.message}
				</div>
			</g:if>
			<g:hasErrors bean="${groupsInstance}">
				<ul class="errors" role="alert">
					<g:eachError bean="${groupsInstance}" var="error">
						<li
							<g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message
								error="${error}" /></li>
					</g:eachError>
				</ul>
			</g:hasErrors>
			<g:hiddenField name="category" value="${category}"/>
			<fieldset class="form">
				<g:render template="form" />
			</fieldset>
			<g:hiddenField id="groupId" name="id" value="" />
			<div style="width: 80%; text-align: center;">
				<span id="createBtn" class="buttons"><g:actionSubmit
						class="save" id="create" action="save"
						value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
				<span id="updateBtn" style="display: none;" class="buttons"><g:actionSubmit
						class="save" id="update" action="update"
						value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
				<span id="resetBtn" class="buttons"> <input type="reset"
					class="edit" value="Reset" id="cancel" onclick="onResetClick();" />
				</span>
			</div>
		</div>
		<div id="list-groups" class="content scaffold-list" role="main">
			<h1>
				<g:message code="default.list.label" args="[entityName]" />
			</h1>
			
			<table style="width: 70%; align: left;">
				<thead>
					<tr>
						<g:sortableColumn property="name" title="Select" />
						<g:sortableColumn property="name"
							title="${message(code: 'groups.name.label', default: 'Name')}" params="[category:category]" />
					</tr>
				</thead>
				<tbody>
					<% int count = 0; %>
					<g:each in="${groupsInstanceList}" status="i" var="groupsInstance">
						<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
							<g:hiddenField id="listCount" name="listCount" value="${count}" />
							<% count++ %>
							<td style="text-align: center;"><g:checkBox
									name="chkbox${count}" class="checkbox"
									id="${groupsInstance?.id}" value="${false}" checked="false"
									onclick="checkBoxClicked(this)" /> <g:hiddenField id="idas"
									name="id${count}" value="${groupsInstance?.id}" /></td>
							<td style="text-align: center;"><a href='#'
								id="${groupsInstance.id}" onclick="populateGroupField(this);">
									${fieldValue(bean: groupsInstance, field: "name")}
							</a></td>
						</tr>
					</g:each>
				</tbody>
			</table>
			<div class="pagination" style="width: 70%; align: left;">
				<g:paginate total="${groupsInstanceTotal}" />
			</div>
			&nbsp;<span class="buttons"><g:actionSubmit disabled="true" class="delete" id="delete"  action="deleteGroup" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
		</div>
	</g:form>
</body>
</html>
