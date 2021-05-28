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
<%@ page
	import="org.apache.shiro.SecurityUtils;com.comcast.rdk.Category"%>
<!DOCTYPE html>
<html>
<head>
<meta name="layout" content="main" />
<title>RDK Test Suite</title>
<style type="text/css" media="screen"></style>

<link rel="stylesheet" href="${resource(dir:'css',file:'codemirror.css')}" />
<g:javascript library="codemirror"/>
<g:javascript library="python"/>

<g:javascript library="jquery.cookie"/>
<g:javascript library="jquery.treeview.async"/>
<g:javascript library="jquery.treeview"/>
<g:javascript library="jquery.contextmenu.r2" />
<g:javascript library="common" />

<script type="text/javascript">

$(document).ready(function() {
	var currentConfigFile = $("#currentConfigFile").val();
	if(currentConfigFile!=null && currentConfigFile!=""){
		$("#responseDivForConfigFile").html("");
		displayCertificationSuiteConfigFile(currentConfigFile,'update');
	}
});

/**
 * Function to display the certification suite config file contents
 */
function displayCertificationSuiteConfigFile(fileName,createOrUpdate) {
	$("#upload_configFile").hide();
	$("#responseDivForConfigFile").html("");
	$("#responseDivForConfigFile").show();
	$.get('displayCertificationSuiteConfigFile', {fileName: fileName,createOrUpdate:createOrUpdate}, function(data) {
		 $("#responseDivForConfigFile").html(data); 
	});
}
/**
 * Function to hide the config file content and show the upload config div
 */
function hideConfigListPage() {
	$("#responseDivForConfigFile").hide();
	$("#upload_configFile").show();
}
</script>
</head>
<body>
	<div class="nav" role="navigation">
		<ul>
			<li><a class="home" href="<g:createLink action="configuration" controller="module"/>"><g:message code="default.home.label"/></a></li>
			<li><a href="#" onclick="displayCertificationSuiteConfigFile('','create'); return false;" >Create Configuration File</a></li>
			<li><a href="#" onclick="hideConfigListPage(); return false;" >Upload Configuration File</a></li>
		</ul>
	</div>
	<br>
	<g:if test="${flash.message}">
		<div class="message" role="status">${flash.message}</div>
	</g:if>
	<div id="rdkCertificationSuiteConfig" class="">
		<table class="noClass" style="border: 1; border-color: black;">
			<tr>
				<td style="width: 200px;">
					<div class="treeborder" style="width: 100%; height: 400px; overflow: auto;">
						<ul id="" class="filetree">
							<g:each in="${fileNameList}" status="i" var="fileName">
								<li style="height: 20px;">
								<a href="#" onclick="displayCertificationSuiteConfigFile('${fileName}','update'); return false;" >${fileName}</a>
								</li>
							</g:each>
						</ul>
					</div>
				</td>
				<td>
					<div id="responseDivForConfigFile" style="width: 1200px; height: 400px;">
					</div>
					<div class="contextMenu" id="upload_configFile" align="left"
						style="height :290px;display:none; " >
						<br> <br> <br> <br>
						<g:form method="POST" controller="scriptGroup" action="uploadSuiteConfigFile"
							enctype="multipart/form-data" params="[category : category]">
							<br><br><br><br>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<label> <b>Select Config Python File </b>
							</label>
							&emsp;
							<input class="uploadFile" type="file" name="file" />
							&emsp;&emsp;
							<g:actionSubmit class="buttons" style="width : 100px; "
								action="uploadSuiteConfigFile" value="Upload Config File" />
						</g:form>
					</div>
				</td>
			</tr>
		</table>
	</div>
	<g:hiddenField name="currentConfigFile" id="currentConfigFile" value="${currentConfigFileName}"/>
</body>
</html>
