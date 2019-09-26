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
<%@ page import="com.comcast.rdk.User" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${message(code: 'user.label', default: 'User')}" />
		<title><g:message code="default.create.label" args="[entityName]" /></title>
		<g:javascript library="validations"/>
	</head>
	<body>
		<g:form controller="user" >
		<a href="#create-user" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="${createLink(uri: '/module/configuration')}"><g:message code="default.home.label"/></a></li>
			</ul>
		</div>
		<div id="create-user" class="content scaffold-create" role="main">
			<h1><g:message code="default.create.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			<g:hasErrors bean="${userInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${userInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>			
				<fieldset class="form">
					<g:render template="form"/>
					<div class="fieldcontain ${hasErrors(bean: userInstance, field: 'roles', 'error')} ">
					<label for="roles">
						<g:message code="user.roles.label" default="Role" />
						<span class="required-indicator">*</span>		
					</label>
					<%--<g:select id="roleid" name="roles" from="${com.comcast.rdk.Role.list()}" multiple="multiple" style="width:150px;" optionKey="id" size="5" value="${userInstance?.roles*.id}" class="many-to-many"/>
				--%>
				<g:select id="roleid" name="roles" from="${com.comcast.rdk.Role.list()}" required="" style="width:150px;" optionKey="id" value="${userInstance?.roles*.id}" class="many-to-one" />
				</div>
					
				</fieldset>
				<%--<fieldset class="buttons">
					<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
				</fieldset>
				--%>
				<div style="width:85%;text-align: center;">
					<g:hiddenField id="userId" name="id" value=""  />
					<g:if test="${role}">
					<span id="createBtn"  style="display:none;" class="buttons"><g:actionSubmit class="save" id="create" action="save" value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
					<span id="updateBtn"  class="buttons"><g:actionSubmit class="save" id="update" action="update" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>	
					</g:if>	
					<g:else>
					<span id="createBtn"  class="buttons"><g:actionSubmit class="save" id="create" action="save" value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
					<span id="updateBtn" style="display:none;" class="buttons"><g:actionSubmit class="save" id="update" action="update" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>	
					</g:else>				
					<span id="resetBtn"  class="buttons">									
					<input type="reset" class="edit" value="Reset" id="cancel" onclick="onResetClick();"/>
					</span>
				</div>					
		</div>
		<div id="list-user" class="content scaffold-list" role="main">
			<h1><g:message code="default.list.label" args="[entityName]" /></h1>
			
			<table>
				<thead>
					<tr>
						<th></th>
						<g:sortableColumn property="username" title="${message(code: 'user.username.label', default: 'Username')}" />
					
						<g:sortableColumn property="email" title="${message(code: 'user.email.label', default: 'Email')}" />
					
						<g:sortableColumn property="name" title="${message(code: 'user.name.label', default: 'Name')}" />
						
						<th><g:message code="user.groupName.label" default="Group Name" /></th>

						<th><g:message code="user.roles.label" default="Role" /></th>
					</tr>
				</thead>
				<tbody>
				<% int count = 0; %> 
				<g:each in="${userInstanceList}" status="i" var="userInstance">
					<g:hiddenField id="listCount" name="listCount" value="${count}"/>
		    		<% count++ %>
					<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
					
						<td align="center"><g:checkBox class="checkbox" name="chkbox${count}" value="${false}" id="${userInstance?.id}" onclick="checkBoxClicked(this);"/>
		    				<g:hiddenField id="id" name="id${count}" value="${userInstance?.id}" />
		    			</td>
					
						<td align="center"><a href="#" onclick="populateFieldVals(${userInstance?.id});" >${fieldValue(bean: userInstance, field: "username")}</a>
					
						<td align="center">${fieldValue(bean: userInstance, field: "email")}</td>
					
						<td align="center">${fieldValue(bean: userInstance, field: "name")}</td>
						
						<td align="center">${fieldValue(bean: userInstance, field: "groupName")}</td>
						
						<td align="center">${fieldValue(bean: userInstance, field: "roles")}</td>
					
					</tr>
				</g:each>
				</tbody>
			</table>
			<div class="pagination">
				<g:paginate total="${userInstanceTotal}" />
			</div>
			&nbsp;<span class="buttons"><g:actionSubmit disabled="true" class="delete" id="delete"  action="deleteUser" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
		</div>
		</g:form>
	</body>
</html>
