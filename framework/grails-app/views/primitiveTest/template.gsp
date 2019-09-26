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

<g:form action="save" controller="primitiveTest" method="post">
	<input type="hidden" name="parameterTypeIds" id="parameterTypeIds">
	<g:hiddenField name="category" value="${category}" id="category" />
	<table>
		<tr>
			<th colspan="2" align="center">Create New Primitive Test</th>
		</tr>
		<tr>
			<td>Test Name</td>
			<td>
				<input type="text" name="testName" id="testName" size="37" maxlength="150">
			</td>
		</tr>
		<tr>
			<td>Select Module</td>
			<td>
				<g:select from="${moduleInstanceList}" var="module" noSelection="['' : 'Please Select']" id="module"
					name="module" style="width: 250px" optionKey="id"/>
			</td>
		</tr>
		<tr>
			<td>Select Function</td>
			<td id="functionTd">
				<select style="width: 250px">
					<option value="">Please Select</option>
				</select>
			</td>
		</tr> 
		<tr id="tableheader" style="display: none;">
			<td colspan="2" align="center">
				<table id="parameterTable">
					<tr>
						<th>Parameter Name</th>
						<th>Type</th>
						<th>Range</th>
						<th>Value</th>
					</tr>
				</table>
			</td>
		</tr>
		<tr id="buttons" style="display: none;">
			<td colspan="2" align="center">
			<span id="save">
					<g:submitToRemote action="save" controller="primitiveTest" update="testMessageDiv" 
						value="Save" before= "isTestExist(document.getElementById('testName').value);" 
						onSuccess = "updateTestList(document.getElementById('testName').value);" >
					</g:submitToRemote>	
			</span>&emsp;
			<input type="reset" value="Reset" id="cancel" onclick="clearValues()">				
			</td>
		</tr>
	</table>
</g:form>

