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
		<br>
		<h1>
			<g:message code="default.label" default="Test Case Details" /> 
		</h1>
	</div>
	<br>
		<div class="fieldcontain  required">
			<label for="testScript"> <g:message code="default.label"
					default="    Test Script 	" /> <span class="required-indicator">*</span>
			</label>
			<g:textField id="newtestScript"  name="testScript" required="true" value="${name}" readonly="true"
				size="38" />
		</div>
		<div class="fieldcontain required">
			<label for="tcId"> <g:message code="default.label"
					default="Test Case ID" /> <span class="required-indicator">*</span>
			</label>
			<g:textField id="newtcId" name="tcId" required="true" value="" size="38" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcObjective"> <g:message code="default.label"
					default=" Test Objective	" /> <span class="required-indicator">*</span>
			</label>
			<g:textArea id="newtcObjective" name="tcObjective" required="true" value="" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcType"> <g:message code="default.label"
					default=" Test Type	" /> <span class="required-indicator">*</span>
			</label>
			<%--<g:textField id="newtcType" name="tcType" required="true" value="" size="38" />
		--%>
		<g:select id="newtcType" name="newtcType" value=""  required=""
          from="${['Positive','Negative']}"
          keys=""   style="width:263px;font-size: 11px;"  />	
		</div>
		<div class="fieldcontain  required">
			<label for="tcSetup"> <g:message code="default.label"
					default=" Supported Box Types	" /> <span class="required-indicator">*</span>
			</label>
			<g:textField id="newtcSetup" name="tcSetup" required="true" value=""
				size="38" />
		</div>
		
		<div class="fieldcontain  required">
			<label for="tcApi"> <g:message code="default.label"
					default="  RDK Interface	" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textArea id="newtcApi" name="tcApi" required="true" value="" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcInputParams"> <g:message code="default.label"
					default="   Input Parameters	" /> <span class="required-indicator">*</span>
			</label>
			<g:textArea id="newtcInputParams" name="tcInputParams" required="true"
				value="" />
		</div>
		<div class="fieldcontain  ">
			<label for="pre-requisits"> <g:message code="default.label"
					default="   Test Pre-requisites		" /> <span class="required-indicator"></span>
			</label>
			<%--<g:textField id="newpreRequisits" name="preRequisits" value="" required="" size="38" />
		--%>
			<g:textArea id="newpreRequisits" name="preRequisits" required="true"
				value="" />
		</div>
		<div class="fieldcontain required">
			<label for="tcApproch"> <g:message code="default.label"
					default="   Automation Approach 	" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textArea id="newtcApproch" name="tcApproch" required="true" value="" />
		</div>
		<div class="fieldcontain  required">
			<label for="tcExecutionOutput"> <g:message
					code="default.label" default="    Expected Output 	" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textArea id="newtcExpectedOutput" name="tcExecutionOutput"
				required="true" value="" />
		</div>
		<div class="fieldcontain  required">
			<label for="priority"> <g:message code="default.label"
					default="   Priority 	" /> <span class="required-indicator">*</span>
			</label>
			<%--<g:textField id="newpriority" name="priority" required="" value=""
				size="38" />
		--%>
		<g:select id="newpriority" name="newpriority" value=""  required=""
          from="${['High','Medium','Low']}"
          keys=""   style="width:263px;font-size: 11px;"   />	
		</div>
		<div class="fieldcontain  required">
			<label for="testStub"> <g:message code="default.label"
					default="    Test Stub 	" /> <span class="required-indicator">*</span>
			</label>
			<%--<g:textField id="newtestStub" name="testStub" required="true" value=""
				size="38" />
		--%>
		<g:textArea id="newtestStub" name="testStub" required="true" value="" />
		</div>
		
		<div class="fieldcontain  required">
			<label for="ReleaseVersion"> <g:message code="default.label"
					default="    Update Release Version 	" /> <span
				class="required-indicator"></span>
			</label>
			<g:textField id="newReleaseVersion" required="" name="ReleaseVersion" value=""
				size="38" />
		</div>
		
		<div class="fieldcontain  required">
			<label for="tcSkipped"> <g:message code="default.label"
					default=" Skipped	" /> <span class="required-indicator"></span>
			</label>
			<%--<g:textField id="newtcSkipped" name="tcStreamId" value=""  required="" size="38" />
		--%>
		<g:select id="newtcSkipped" name="tcSkipped" value=""  required=""
          from="${['No','Yes']}"
          keys=""  style="width:263px;font-size: 11px;"  />          
		</div>	
		<div class="fieldcontain  required">
			<label for="remarks"> <g:message code="default.label"
					default="    Remarks	" /> <span class="required-indicator"></span>
			</label>
			<g:textField id="newtest_remarks" name="remarks" required="" value=""
				size="38" />
		</div>
	<br> <br>	
	<div class="content scaffold-create"></div>
	<div align="right">
		<span class="buttons"> <g:submitButton name=" Update " 
				class="update"
				value="${message(code: 'default.button.update.label', default: 'Update')}"
				onclick="addTestCase('${category}','${uniqueId}');" /></span>
	</div>
</div>
