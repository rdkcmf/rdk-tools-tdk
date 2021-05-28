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
<%@page import="com.comcast.rdk.Category"%>
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.DeviceTemplate"%>

<script type="text/javascript">

$(document).ready(function() {

	/* Assign the codemirror to the textarea where configuration file content is displayed */
	var myTextarea = document.getElementById('configAreaEdit')
	var editorForDeviceConfig = CodeMirror.fromTextArea(myTextarea, {
	    lineNumbers: true,
	    mode:  "python"
	});
	editorForDeviceConfig.setSize(null,"100%"); //to resize codemirror
   $('#updateId').click(function(){
    	updateDeviceConfigContent($('#configFileName').val(),editorForDeviceConfig.getValue(),'update',$('#boxTypeConfigFileExists').val(),$('#finalCreateDeviceConfigFileName').val(),'${boxTypeName}','${createConfigFileName}')
    });

   $('#createId').click(function(){
   	updateDeviceConfigContent($('#createDeviceConfigFileName').val(),editorForDeviceConfig.getValue(),'create',$('#boxTypeConfigFileExists').val(),$('#finalCreateDeviceConfigFileName').val(),'${boxTypeName}','${createConfigFileName}')
   });
});

/**
 * Function to toggle the name of the configuration file to be created if no config 
 * files are present for that device
 */
function changeConfigFileName(boxTypeName,deviceName){
	var configFileNameDiv = document.getElementById('createDeviceConfigFileName')
	if(configFileNameDiv.value == boxTypeName){
		configFileNameDiv.value = deviceName
		document.getElementById('finalCreateDeviceConfigFileName').value = "deviceName"
	}else if(configFileNameDiv.value == deviceName){
		configFileNameDiv.value = boxTypeName
		document.getElementById('finalCreateDeviceConfigFileName').value = "boxTypeName"
	}	
}

/**
 * Function to hide and show upload div for device configuration files
 */
function showUploadConfigDetails(editFlagForDeviceConfigForm){
	var uploadDiv = document.getElementById('uploadDevConfigDiv')
	if(uploadDiv.style.display === "none" ){
		$('#deviceConfigFileContent').hide();
		if(editFlagForDeviceConfigForm == "true"){
			$('#updateIdDiv').hide();
		}else{
			$('#createIdDiv').hide();
		}
		uploadDiv.style.display = "block";
	}else{
		$('#deviceConfigFileContent').show();
		if(editFlagForDeviceConfigForm == "true"){
			$('#updateIdDiv').show();
		}else{
			$('#createIdDiv').show();
		}
		uploadDiv.style.display = "none";
	}
}
</script>
<g:form method="post" controller="deviceGroup">
<input type="hidden" name="boxTypeConfigFileExists" id="boxTypeConfigFileExists" value="${boxTypeConfigFileExists}">
<input type="hidden" name="finalCreateDeviceConfigFileName" id="finalCreateDeviceConfigFileName" value="deviceName">
	<g:if test="${editFlagForDeviceConfigForm == 'true'}">
		<div id="deviceConfigFileName" name="deviceConfigFileName" style="margin-left:10px;">Config File Name :
				${fileName }
		</div>
		<div id="uploadConfig" name="uploadConfig" style="float:right"><a href="#" onclick="showUploadConfigDetails('${editFlagForDeviceConfigForm}'); return false;" >Upload Configuration File</a></div>
	</g:if>
	<g:else>
		<div style="margin-left:10px;" >
			<label for="Config File Name"> File Name: <span
				class="required-indicator">*</span>
			</label>
			<input type="text" id="createDeviceConfigFileName" name="createDeviceConfigFileName" style="width:200px;" value="${createConfigFileName}" readonly />&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<g:if test="${boxTypeConfigFileExists == false}">
				<a href="#" onclick="changeConfigFileName('${boxTypeName}','${createConfigFileName}');" id="changeName">Change Name</a>
			</g:if>
			<div id="uploadConfig" name="uploadConfig" style="float:right"><a href="#" onclick="showUploadConfigDetails('${editFlagForDeviceConfigForm}'); return false;" >Upload Configuration File</a></div>
		</div>
	</g:else>
	<input type="hidden" name="configFileName" id="configFileName" value="${fileName}">
	<div id="deviceConfigFileContent" style="margin-left:10px;margin-top:20px;width:99%;border: 0.5px solid #aaa;height:68vh;">
		<textarea id="configAreaEdit" name="configAreaEdit" class="configAreaEdit">${content}</textarea>
	</div>
	<g:if test="${editFlagForDeviceConfigForm == 'true'}">
		<div style="width: 90%; text-align: center;margin-top:20px;">
		<span class="buttons" id="updateIdDiv"><input type="button" id="updateId" style="font-weight: bold;" name="updateDeviceConf" value="Update Config File"></span>
		<span id="updateDivDeviceConfigForm" style="width: 100%;overflow: auto;margin-left:20px;"></span>
		</div>
	</g:if>
	<g:else>
		<div style="width: 90%; text-align: center;margin-top:20px;">
		<span class="buttons" id="createIdDiv"><input type="button" id="createId" style="font-weight: bold;" name="createDeviceConf" value="Create Config File"></span>
		<span id="updateDivDeviceConfigForm" style="width: 100%;overflow: auto;margin-left:20px;"></span>
		</div>
	</g:else>
</g:form>
<div style="padding-left: 17%; padding-top: 1%;display:none;" id="uploadDevConfigDiv">
	<g:form enctype="multipart/form-data" name="uploadDevConfigForm">Upload Configuration file <input
						type="file" name="configFile" id="file" />
		<input type="button" value="Upload" onclick="uploadDeviceConfigFile($('#createDeviceConfigFileName').val(),$('#configFileName').val(),$('#finalCreateDeviceConfigFileName').val(),'${boxTypeName}','${createConfigFileName}','${editFlagForDeviceConfigForm}')" />
	</g:form>
</div>