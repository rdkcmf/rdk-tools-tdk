<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2021 RDK Management

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
<style type="text/css" media="screen"></style>


<script type="text/javascript">
$(document).ready(function() {
	/* Assign the codemirror to the textarea where configuration file content is displayed */
	var myTextarea = document.getElementById('configArea')
	var editor = CodeMirror.fromTextArea(myTextarea, {
	    lineNumbers: true,
	    mode:  "python"
	});
});
</script>
<g:form method="post" controller="scriptGroup">
	<g:if test="${createOrUpdate == 'update'}">
		<div id="certificationSuiteConfigFileName" name="certificationSuiteConfigFileName" style="margin-left:30px;margin-top:20px;">Config File Name :
			${fileName }
		</div>
	</g:if>
	<g:else>
		<div style="margin-left:30px;" >
			<label for="Config File Name"> File Name: <span
				class="required-indicator">*</span>
			</label>
			<input type="text" id="certificationSuiteConfigFileName" name="certificationSuiteConfigFileName"  value="" />
		</div>
	</g:else>
	<input type="hidden" name="configFileName" id="configFileName" value="${fileName}">
	<div id="certificationSuiteConfigFileContent" style="margin-left:30px;margin-top:20px;width:90%;border: 0.5px solid #aaa;">
		<textarea id="configArea" name="configArea" class="configArea">${content}</textarea>
	</div>
	<g:if test="${createOrUpdate == 'update'}">
		<div style="width: 90%; text-align: center;margin-top:20px;">
			<span class="buttons"><g:actionSubmit class="save"
			action="updateCertificationSuiteConfigFile" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
			<span class="buttons"><g:actionSubmit class="download"
			action="downloadSuiteConfigFile" value="Download" /> </span>
		</div>
	</g:if>
	<g:else>
		<div style="width: 90%; text-align: center;margin-top:20px;">
			<span class="buttons"><g:actionSubmit class="save"
			action="saveCertificationSuiteConfigFile" value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
		</div>
	</g:else>
</g:form>