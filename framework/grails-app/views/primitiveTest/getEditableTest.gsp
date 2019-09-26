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
<%@ page import="com.comcast.rdk.PrimitiveTest"%>
<%@ page import="com.comcast.rdk.Module"%>
<%@ page import="com.comcast.rdk.ParameterType"%>

<g:form action="update" controller="primitiveTest" method="post">
	<g:set var="ids" value="${paramTypes?.id?.toString()}"/>
	<%--<g:set var="ids" value="${primitiveTest.parameters?.parameterType?.id?.toString()}"/>--%>
	<input type="hidden" name="parameterTypeIds" id="parameterTypeIds" value="${ids?.substring(1, ids?.lastIndexOf(']'))}">
	<input type="hidden" name="id" id="id" value="${primitiveTest?.name}">
	<input type="hidden" name="ptVersion" id="ptVersion" value="${primitiveTest?.version}">
	<input type="hidden" name="functionValue" id="functionValue" value="${primitiveTest?.function?.id}">
	<g:hiddenField name="category" value="${category}" id="category"/>
	<table>
		<tr>
			<th colspan="2" align="center">Edit Primitive Test</th>
		</tr>
		<tr>
			<td>Test Name</td>
			<td>
				<input type="text" name="testName" id="testName" size="37" maxlength="150" value="${primitiveTest.name}" disabled="true">
			</td>
		</tr>
		<tr>
			<td>Select Module</td>
			<td>
				<input type="text" name="module" id="module" size="37" maxlength="150" value="${primitiveTest.module?.name}" disabled="true">
				<%--<g:select from="${Module.list([order: 'asc', sort: 'name'])}" id="module"
					name="module" style="width: 250px" optionKey="id" value="${primitiveTest.module?.id}"/>
			--%>
			</td>
		</tr>
		<tr>
			<td>Select Function</td>
			<td id="functionTd">
				<input type="text" name="functionValue" id="functionValue" size="37" maxlength="150" 
						value="${primitiveTest?.function?.name}" disabled="true">
				<%--<select name="functionValue" id="functionValue" style="width: 250px" onchange="getAssociatedParameters()">
					<g:each in="${functions}" var="function">
						<g:if test="${function.id == primitiveTest.function.id}">
							<option value="${function.id}" selected="selected">${function.name}</option>
						</g:if>
						<g:else>
							<option value="${function.id}">${function.name}</option>
						</g:else>
					</g:each>
				</select>--%>
			</td>
		</tr>
		<tr>
			<td colspan="2" align="center">
				<table id="parameterTable">
					<tr>
						<th>Parameter Name</th>
						<th>Type</th>
						<th>Range</th>
						<th>Value</th>
					</tr>
					<g:each in="${primitiveTest.parameters}" var="parameter">
						<g:if test="${parameter?.parameterType !=null}">
							<tr>
								<td align="left">&emsp;&emsp;${parameter?.parameterType?.name}</td>
								<td>${parameter?.parameterType?.parameterTypeEnum}</td>
								<td>${parameter?.parameterType?.rangeVal}</td>
								<td align="center">
									<input type="text" name="value_${parameter?.parameterType?.id}" value="${parameter?.value}">
								</td>
							</tr>
						</g:if>
					</g:each>
					<g:each in="${newParams}" var="newparam">
						<tr>
							<td align="left">&emsp;&emsp;${newparam?.name}</td>
							<td>${newparam?.parameterTypeEnum}</td>
							<td>${newparam?.rangeVal}</td>
							<td align="center">
								<input type="text" name="value_${newparam?.id}" value="">
							</td>
						</tr>
					</g:each>
				</table>
			</td>
		</tr>
		<tr id="buttons">
			<td colspan="2" align="center">
				<input type="submit" value="Update" id="save">&emsp;
				<input type="reset" value="Cancel" id="cancel" onclick="makeTestEditable('${primitiveTest?.name},${category}')">
			</td>
		</tr>
	</table>
</g:form>

