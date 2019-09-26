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
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<div class="odd">
	<div align="left" class="content scaffold-create">
		<table>
			<tr>
				<td align="right"><g:link action="downloadTestCaseInExcel"
						params="[moduleName:"${moduleName}",category:"${category}",primitiveTest:"${primitiveTest}",name:"${script?.name }"]"> Download Test Case(Excel) </g:link>
						<br>
						<g:link onClick="alert('The test case document download will start soon...');"
								action="downloadModuleTestCaseInExcel" params="[moduleName:"${moduleName}",category:"${category}"]">Download ${moduleName} Test Cases(Excel)</g:link>
				</td>
			</tr>
			<tr>
				<td align="left">
					<h1>
						<g:message code="default.label" default="Test Case Details" />
					</h1>
				</td>
			</tr>
		</table>
	</div>
	<br>
	<g:if test="${testCaseDetails}">
		<div class="fieldcontain  required">
			<label for="testScript"> <g:message code="default.label"
					default="    Test Script 	" /> <span class="required-indicator">*</span>
			</label>

			<g:textField id="testScript" name="testScript" required="true"
				value="${script.name}" size="39" readonly="true"/>
		</div>
		<div class="fieldcontain required">
			<label for="tcId"> <g:message code="default.label"
					default="Test Case ID" /> <span class="required-indicator">*</span>
			</label>
			<g:textField id="tcId" name="tcId" required="true"
				value="${testCaseDetails?.testCaseId}" size="39" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcObjective"> <g:message code="default.label"
					default=" Test Objective	" /> <span class="required-indicator">*</span>
			</label>
			<g:textArea id="tcObjective" name="tcObjective" required="true"
				value="${testCaseDetails?.testObjective}" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcType"> <g:message code="default.label"
					default=" Test Type	" /> <span class="required-indicator">*</span>
			</label>
			<%--<g:textField id="tcType" name="tcType" required="true" value="${testCaseDetails?.testType}" size="39" />
		--%>
			<g:select id="tcType" name="tcType"
				value="${testCaseDetails?.testType}"
				from="${['Positive','Negative']}" keys="" 
				style="width:263px;font-size: 11px" />

		</div>
		<div class="fieldcontain  required">
			<label for="tcSetup"> <g:message code="default.label"
					default=" Supported Box Types		" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textField id="tcSetup" name="tcSetup" required="true"
				value="${testCaseDetails?.testSetup}" size="39" />
		</div>
		
		<div class="fieldcontain  required">
			<label for="tcApi"> <g:message code="default.label"
					default="  API / Interface is used	" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textArea id="tcApi" name="tcApi" required="true"
				value="${testCaseDetails?.interfaceUsed}" />
		</div>

		<div class="fieldcontain  required">
			<label for="tcInputParams"> <g:message code="default.label"
					default="   Input Parameters	" /> <span class="required-indicator">*</span>
			</label>
			<g:textArea id="tcInputParams" name="tcInputParams" required="true"
				value="${testCaseDetails?.inputParameters}" />
		</div>
		<div class="fieldcontain  ">
			<label for="pre-requisits"> <g:message code="default.label"
					default="  Test Prerequisite		" /> <span
				class="required-indicator"></span>
			</label>
			<%--<g:textField id="preRequisits" required="" name="preRequisits"
				value="${testCaseDetails?.preRequisites}" size="39" />
		--%>
			<g:textArea id="preRequisits" name="preRequisits" required="true"
				value="${testCaseDetails?.preRequisites}" />
		</div>
		<div class="fieldcontain required">
			<label for="tcApproch"> <g:message code="default.label"
					default="   Automation Approach 	" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textArea id="tcApproch" name="tcApproch" required="true"
				value="${testCaseDetails?.automationApproch}" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcExpectedOutput"> <g:message
					code="default.label" default="   Expected Output 	" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textArea id="tcExpectedOutput" name="tcExecutionOutput"
				required="true" value="${testCaseDetails?.expectedOutput}" />
		</div>
		<div class="fieldcontain  required">
			<label for="priority"> <g:message code="default.label"
					default="   Priority 	" /> <span class="required-indicator">*</span>
			</label>
			<%--<g:textField id="priority" name="priority" required="" value="${testCaseDetails?.priority}"
				size="39" />
		--%>
			<g:select id="priority" name="priority"
				value="${testCaseDetails?.priority}" required=""
				from="${['High','Medium','Low']}" keys="" 
				style="width:263px;font-size: 11px" />
		</div>
		<div class="fieldcontain  required">
			<label for="testStub"> <g:message code="default.label"
					default="    Test Stub 	" /> <span class="required-indicator">*</span>
			</label>
			<%--<g:textField id="testStub" name="testStub" required="true"
				value="${testCaseDetails?.testStubInterface}" size="39" />
		--%>
			<g:textArea id="testStub" name="testStub" required="true" value="${testCaseDetails?.testStubInterface}" />
		</div>

		<div class="fieldcontain  required">
			<label for="ReleaseVersion"> <g:message code="default.label"
					default="     Update Release Version  	" /> <span
				class="required-indicator"></span>
			</label>
			<g:textField id="ReleaseVersion" required="" name="ReleaseVersion"
				value="${testCaseDetails?.releaseVersion}" size="39" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcSkipped"> <g:message code="default.label"
					default=" Skipped	" /> <span class="required-indicator"></span>
			</label>
			<g:select id="tcSkipped1" name="tcSkipped1"
				value="${testCaseDetails?.tcskip}" required=""
				from="${['No','Yes']}" keys="" 
				style="width:263px;font-size: 11px" />				
			</div>

		<div class="fieldcontain  required">
			<label for="remarks"> <g:message code="default.label"
					default="    Remarks	" /> <span class="required-indicator"></span>
			</label>
			<g:textField id="test_remarks" name="remarks" required=""
				value="${testCaseDetails?.remarks}" size="39" />
		</div>
	</g:if>
	<br> <br>
	<div class="content scaffold-create"></div>
	<div align="right">
		<span class="buttons"> <g:submitButton name="upadte"
				class="update"
				value="${message(code: 'default.button.update.label', default: 'Update')}"
				onclick="updateTestCase('${moduleName}','${category}','${primitiveTest}','${script?.name}');" /></span>
	</div>
</div>
