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
<%@ page import="com.comcast.rdk.Device" %>

<g:set var="entityName" value="${message(code: 'device.label', default: 'Device')}" />

	<g:if test= "${deviceInstance}">
	<div id="edit-device" class="content scaffold-edit" role="main">
		<h1>
			Device &nbsp;${deviceInstance?.stbName}
		</h1>

		<g:form method="post" controller="deviceGroup">
			<g:hiddenField name="id" value="${deviceInstance?.id}" />
			<g:hiddenField name="version" value="${deviceInstance?.version}" />
			<input type="hidden" name="url" id="url" value="${url}">
			<fieldset class="form">
				<g:render template="formDevice" />
			</fieldset>
			<div id="streamdiv">
				<g:render template="streamlistedit" />
			</div>
			<br>
			<div style="width: 90%; text-align: center;">
				<g:if test="${flag != 'STATIC'}">
					<span class="buttons"><g:actionSubmit class="save"
							action="updateDevice"
							value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
					<span class="buttons"><g:actionSubmit class="delete"
							action="deviceDelete"
							value="${message(code: 'default.button.delete.label', default: 'Delete')}"
							formnovalidate=""
							onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
					<g:if
						test="${deviceInstance?.category?.toString()?.equals('RDKV')}">
						<span class="buttons"><g:actionSubmit class="download"
								action="downloadRDKVDeviceXml" value="Download" /> </span>
					</g:if>
					<g:if
						test="${deviceInstance?.category?.toString()?.equals('RDKB')}">
						<span class="buttons"><g:actionSubmit class="download"
								action="downloadRDKBDeviceXml" value="Download" /> </span>
					</g:if>
				</g:if>
			</div>
		</g:form>

		<div>
			<g:if test="${category?.toString()?.equals('RDKB')}">
				<div style="padding-left: 33%; padding-top: 2%;" id="toggleOptions">
					<input type="radio" name="configType" value="PythonE2E" checked>Python
					E2E&nbsp;&nbsp; <input type="radio" name="configType"
						value="TCLE2E">TCL E2E
				</div>
				<div style="padding-left: 17%; padding-top: 1%;" id="uploadConfig">
					<g:form enctype="multipart/form-data" name="uploadForm">Upload Configuration file <input
							type="file" name="configFile" id="file" />
						<input type="button" value="UPLOAD" onclick="uploadConfig()" />
					</g:form>
				</div>
				<div style="padding-left: 17%; padding-top: 2%;" id="uploadStatus"></div>
			</g:if>
		</div>
	</div>


</g:if>
	
