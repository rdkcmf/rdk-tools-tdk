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
<script type="text/javascript">
$(document).ready(function() {
	var messageValue = document.getElementById("deleteMessage").value
	if(messageValue != null && messageValue != ""){
		alert(messageValue)
	}
});
$('#deviceConfigFileNameUpdated').contextMenu('deviceConfigFile_menuUpdated', {
	bindings : {
		'delete_deviceConfigFileUpdated' : function(node) {
			if (confirm('Are you want to delete this Device Config File?')) {
				deleteDeviceConfigFile(node.innerHTML,document.getElementById("boxType").value,document.getElementById("stbName").value)
			}
		},
		'download_deviceConfigFileUpdated' : function(node) {
			downloadDeviceConfigFile(node.innerHTML)
		}
	}
});
</script>
<g:hiddenField id="deleteMessage" name="deleteMessage" value="${deleteMessage}" />
<label for="deviceConfigFileLabel"> <g:message
		code="device.thunderPort.label" default="Device Config File" /><span
		class="required-indicator">*</span>
</label>
<g:if test="${deleteDiv == 'deleteDiv'}">
	<g:if test="${boxTypeConfigFileExists == true}">
		<a href="#" onclick="showDeviceConfigContent('${finalConfigFile}');" id="deviceConfigFileNameUpdated">${finalConfigFile}</a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
	</g:if>
	<a href="#" onclick="createDeviceConfigFile('${finalConfigFile}',document.getElementById('stbName').value,'${bTypeId}')" id="createDeviceConfigFileUpdated">Create New Device Config File</a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
</g:if>
<g:else>
	<a href="#" onclick="showDeviceConfigContent('${finalConfigFile}');" id="deviceConfigFileNameUpdated">${finalConfigFile}</a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
	<g:if test="${finalDeviceConfigFileType == 'boxTypeName'}">
		<a href="#" onclick="createDeviceConfigFile('${boxTypeConfigFileName}',document.getElementById('stbName').value,'${bTypeId}')" id="createDeviceConfigFileUpdated">Create New Device Config File</a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
	</g:if>
</g:else>
<div class="contextMenu" id="deviceConfigFile_menuUpdated" style="display:none">
	<ul>
	    <li id="delete_deviceConfigFileUpdated"><img src="../images/delete.png" />Delete</li>	
	    <li id="download_deviceConfigFileUpdated"><img src="../images/reorder_down.png" />Download</li>	
	</ul>
</div>
  