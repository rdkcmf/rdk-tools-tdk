/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
$(document).ready(function() {
	
	$("#browser1").treeview({		
		animated:"normal",
		persist: "cookie"
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});

	$('#addDeviceGrpRDK').contextMenu('root_menu', {
		bindings : {
			'add_devicegrp' : function(node) {
				createDeviceGroup('RDKV');
			},
			'add_devicegrpB' : function(node) {
				createDeviceGroup('RDKB');
	}
		}
	});
	
	$('.file').contextMenu('childs_menu', {
		bindings : {
			'edit_devicegrp' : function(node) {
				showDeviceGroup(node.id);
			},
			'delete_devicegrp' : function(node) {
				if (confirm('Do want to delete this Device?')) {
					deleteDevice(node.id);
				}
			}
		}
	});
	
	$('#deviceConfigFileName').contextMenu('deviceConfigFile_menu', {
		bindings : {
			'delete_deviceConfigFile' : function(node) {
				if (confirm('Are you want to delete this Device Config File?')) {
					deleteDeviceConfigFile(node.innerHTML,document.getElementById("boxType").value,document.getElementById("stbName").value)
				}
			},
			'download_deviceConfigFile' : function(node) {
				downloadDeviceConfigFile(node.innerHTML)
			}
		}
	});
	
	$("#deviceid").addClass("changecolor");
});

function hideUpload(){
	$("#responseDiv").show();
	$("#up_load").hide();
}

function createDeviceGroup(group) {	
	hideUpload();
	$.get('create',{category:group}, function(data) { $("#responseDiv").html(data); });
}

function showDeviceGroup(id) {
	hideUpload();
	$.get('edit', {id: id}, function(data) { $("#responseDiv").html(data); });
}

function deleteDevice(id){
	$.get('deleteDeviceGrp', {id: id}, function(data) { document.location.reload(); });
}

function showFields(){
	var boxType = $("#boxType").find('option:selected').text();
	var boxId = $("#boxType").find('option:selected').val();
	var isThunderEnabled = $("#isThunderEnabled").prop('checked');
	var url = $("#url").val();
	var stbName = document.getElementById('stbName').value
	if(isThunderEnabled){
		$.get('updateConfigDivOnBoxTypeChange', {stbName:stbName,editFlag:$("#editFlag").val(),boxType:boxType,boxId:boxId}, function(data) {
			$("#deviceConfigFile").html(""); 
			$("#deviceConfigFileUpdatedDiv").html(data); 
		});		
	}
	$.get('getBoxType', {id: boxId }, function(data) {
		if((data[0].type == 'gateway' || data[0].type == 'stand-alone-client') && data[0].category==='RDKV' && !isThunderEnabled){
			var xmlhttp;	
			if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
				xmlhttp = new XMLHttpRequest();
			} else {// code for IE6, IE5
				xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
			}
			xmlhttp.onreadystatechange = function() {
				if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					if($("#editFlag").val() == "true"){
						document.getElementById("streamdivEditDevice").innerHTML = xmlhttp.responseText;
					}else{
						document.getElementById("streamdivCreateDevice").innerHTML = xmlhttp.responseText;
					}
				}
			}			
			xmlhttp.open("GET", url+"/deviceGroup/list?t="+Math.random()+"&max=10&offset=0&streamtable=true", true);
			xmlhttp.send();
			$("#recorderId").show();
			if(data[0].type == 'gateway'){
				$("#gatewayId").hide()
				$("#gatewayIdedit").hide();
			}else if(data[0].type == 'stand-alone-client'){
				if($("#editFlag").val() == "true"){
					$("#gatewayId").hide();
					$("#gatewayIdedit").show();	
					$("#recorderId").hide();
				}
				else{
					$("#gatewayId").show();
					$("#gatewayIdedit").hide();		
				}
			}
			$('#deviceTemplate').prop('selectedIndex',0);  
			$("#deviceTemplateDropdown").show();
			
			if($("#editFlag").val() == "true"){
				$("#recorderId").hide();
				$("#recorderIdedit").show();
				$("#streamdivEditDevice").show();
			}else{
				$("#recorderIdedit").hide();
				$("#recorderId").show();
				$("#streamdivCreateDevice").show();
			}
			
		}
		else{
			if($("#editFlag").val() == "true"){
				$("#gatewayId").hide();
				$("#gatewayIdedit").show();	
				$("#streamdivEditDevice").hide();	
				$("#deviceTemplateDropdown").hide();
				$("#recorderIdedit").hide();
				$("#recorderId").hide();
			}
			else{
				$("#recorderId").hide();
				$("#gatewayId").show();
				$("#streamdivCreateDevice").hide();	
				$("#deviceTemplateDropdown").hide();
				$("#gatewayIdedit").hide();		
				$("#recorderIdedit").hide();
			}
		}	
	});		
}

/**
 * Function to load the contents of device template for filling the ocapId's while creating a device
 */
function loadDeviceTemplate(deviceTemplateId, streamingDetailsInstanceTotal,radioStreamingDetailsInstanceTotal){
	if(deviceTemplateId){
		var url = $("#url").val();
		var fetchDeviceTemplateURL = url+'/deviceTemplate/fetchDeviceTemplate'
		$.get(fetchDeviceTemplateURL, {deviceTemplateInstanceId: deviceTemplateId}, function(data) {
			for(i=1;i<=streamingDetailsInstanceTotal;i++){
				document.getElementById("ocapId_"+i).value = data[i-1]
			}
			for(i=streamingDetailsInstanceTotal+1;i<=data.length;i++){
				var j = i-streamingDetailsInstanceTotal
				document.getElementById("ocapId_R0"+j).value = data[i-1]
			}
		});
	}
	else{
		var totalCount = streamingDetailsInstanceTotal + radioStreamingDetailsInstanceTotal
		for(i=1;i<=streamingDetailsInstanceTotal;i++){
			document.getElementById("ocapId_"+i).value = ""
		}
		for(i=streamingDetailsInstanceTotal+1;i<=totalCount;i++){
			var j = i-streamingDetailsInstanceTotal
			document.getElementById("ocapId_R0"+j).value = ""
		}
	}
}

/**
 * Ajax call to perform binary upload.
 * @param boxType
 * @param boxIp
 * @param username
 * @param password
 * @param systemPath
 */
function uploadBinary(boxType, boxIp, username, password, systemPath, systemIP, boxpath, deviceId){	
	if(boxIp == ""){
		alert("Please enter Destination IP address");
	}
	else if(boxType == ""){
		alert("Please enter Destination Box type");
	}
	else if(systemIP == ""){
		alert("Please enter Source IP");
	}
	else if(systemPath == ""){
		alert("Please enter Source Path");
	}
	else if(username == ""){
		alert("Please enter Source Username");
	}
	else if(password == ""){
		alert("Please enter Source Password");
	}
	else if(boxpath == ""){
		alert("Please enter Destination Path");
	}
	else{
		document.getElementById("uploadResultDiv").innerHTML = "";
		$("#waitingSymbol").show();
		$("#waitingSymbol2").show();
		$("#uploadBtnSpan").hide();
		$("#uploadButton").hide();
		$.get('uploadBinary', {boxType:boxType, boxIp:boxIp, username: username, password: password,  systemPath: systemPath, systemIP:systemIP, boxpath:boxpath}, 
			function(data) {
				
				var uploadResult = document.getElementById('uploadResultDiv');
				uploadResult.innerHTML =  " ";
				
				for ( var i = 0; i < data.length; i++) {
					
					uploadResult.innerHTML = uploadResult.innerHTML + data[i];
					uploadResult.innerHTML = uploadResult.innerHTML + "<br />";
					
				}
				
				$("#waitingSymbol").hide();
				$("#waitingSymbol2").hide();
				$("#uploadBtnSpan").show();
				$("#uploadResultDiv").show();
			//	showDevice(deviceId);
				$("#uploadButton").show();
				
		   });
	}
	
}

/**
 * Function to hide upload binary link
 */
function hideLink(){
	
	$("#uploadBinarypopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 600,
	            height: 500
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	
}

function showResult(){
	
	$("#uploadResultDiv").show();
	$("#hideResult").show();
	$("#showResult").hide();
	
}

function hideResult(){
	
	$("#uploadResultDiv").hide();
	$("#hideResult").hide();
	$("#showResult").show();
}


/**
 * Function to check whether device is saved or not. If yes show edit page.
 */
function updateDeviceList(stbName){
	$.get('fetchDevice', {stbName: stbName}, function(data) {
		if(data!=""){
			if($("#isDeviceExist").val()==""){
				$("#currentDeviceId").val(data);
				setTimeout(function(){location.reload();showDevice(data);},1000);
			}
			$("#isDeviceExist").val("");
		}
		$("#messageDiv").show();
	});
}

/**
 * Function to check whether device with same ip address exist or not.
 * @param stbIp
 */
function isDeviceExist(stbName){
	
	$.get('fetchDevice', {stbName: stbName}, function(data) {
		if(data!=""){
			$("#isDeviceExist").val(data);
		}
		$("#messageDiv").show();
	});
}

/**
 * Function to hide/show the port configuration div's while adding or editing a device
 */
function showPortConfigDiv(){
	if(document.getElementById('portConfigureRadio').checked) {
		 $("#deviceConfigurePorts").show();	
	}else{
		$("#deviceConfigurePorts").hide();	
	}
}

/**
 * Function to hide/show the thunder port div's while adding or editing a device
 */
function showThunderPortDiv(){
	var editPage = false
	if($("#editFlag").val() == "true"){
		editPage = true
	}
	if(document.getElementById('isThunderEnabled').checked) {
		var boxType = $("#boxType").find('option:selected').text();
		var boxId = $("#boxType").find('option:selected').val();
		var stbName = document.getElementById('stbName').value
		$("#thunderPortConfigure").show();
		$("#deviceTemplateDropdown").hide();
		$("#deviceConfigFile").show();
		$("#deviceConfigFileUpdatedDiv").show();
		$.get('updateConfigDivOnBoxTypeChange', {stbName:stbName,editFlag:editPage,boxType:boxType,boxId:boxId}, function(data) {
			$("#deviceConfigFile").html(""); 
			$("#deviceConfigFileUpdatedDiv").html(data); 
		});	
		if(editPage){
			$("#recorderIdedit").hide();
			$("#recorderId").hide();
			$("#streamdivEditDevice").hide();
		}else{
			$("#recorderIdedit").hide();
			$("#recorderId").hide();
			$("#streamdivCreateDevice").hide();
		}
	}else{
		$("#thunderPortConfigure").hide();
		$("#deviceConfigFile").hide();
		$("#deviceConfigFileUpdatedDiv").hide();
		var boxId = $("#boxType").find('option:selected').val();
		var url = $("#url").val();
		$.get('getBoxType', {id: boxId }, function(data) {
			if((data[0].type == 'gateway' || data[0].type == 'stand-alone-client') && data[0].category==='RDKV'){
				$('#deviceTemplate').prop('selectedIndex',0);
				$("#deviceTemplateDropdown").show();
				if(editPage){
					if($("#deviceStreamsSize").val() > 0){
						$("#streamdivEditDevice").show();
						$("#recorderIdedit").show();
					}else{
						$("#streamdivEditDevice").show();
						$("#recorderIdedit").show();
						var xmlhttp;	
						if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
							xmlhttp = new XMLHttpRequest();
						} else {// code for IE6, IE5
							xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
						}
						xmlhttp.onreadystatechange = function() {
							if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
								document.getElementById("streamdivEditDevice").innerHTML = xmlhttp.responseText;
							}
						}			
						xmlhttp.open("GET", url+"/deviceGroup/list?t="+Math.random()+"&max=10&offset=0&streamtable=true", true);
						xmlhttp.send();
						$("#recorderId").show();
						if(data[0].type == 'gateway'){
							$("#gatewayId").hide()
							$("#gatewayIdedit").hide();
						}else if(data[0].type == 'stand-alone-client'){
							$("#gatewayId").hide();
							$("#gatewayIdedit").show();	
							$("#recorderId").hide();
						}
						$('#deviceTemplate').prop('selectedIndex',0);  
						$("#deviceTemplateDropdown").show();
						$("#recorderIdedit").hide();
						if($("#editFlag").val() == "true"){
							$("#recorderId").hide();
							$("#recorderIdedit").show();
							$("#streamdivEditDevice").show();
						}
					}
				}else{
					$("#recorderId").show();
					$("#streamdivCreateDevice").show();
				}
			}else{
				$("#deviceTemplateDropdown").hide();
				if(editPage){
					$("#recorderIdedit").hide();
					$("#streamdivEditDevice").hide();
				}else{
					$("#recorderId").hide();
					$("#streamdivCreateDevice").hide();
				}
			}
		});
	}
}

/**
 * Function to display the device/boxtype config file contents in a popup
 * @param fileName
 */
function showDeviceConfigContent(fileName){
	var editFlagForDeviceConfigForm = true
	$.get('editDeviceConfigFile', {fileName: fileName,editFlagForDeviceConfigForm:editFlagForDeviceConfigForm}, function(data) {
		$("#deviceConfigPopup").html(data); 
	});		
	$("#deviceConfigPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
			  	width: ($(window).width() - 50),
			  	height:  ($(window).height() -100)	  
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

/**
 * Function to update device config file
 * @param fileName
 * @param configAreaContent
 * @param updateOrCreate
 * @param boxTypeConfigFileExists
 * @param finalDeviceConfigFileType
 * @param boxType
 * @param stbName
 */
function updateDeviceConfigContent(fileName,configAreaContent,updateOrCreate,boxTypeConfigFileExists,finalDeviceConfigFileType,boxType,stbName){
	$.post('updateDeviceConfigContent', {configFileName: fileName,configAreaEdit:configAreaContent,updateOrCreate:updateOrCreate}, function(data) {
		if(data == "Config File Created"){
			$.get('updateDeviceConfigDiv', {fileName: fileName,finalDeviceConfigFileType:finalDeviceConfigFileType,boxType:boxType,stbName:stbName}, function(result) {
				$("#deviceConfigFile").html(""); 
				$("#deviceConfigFileUpdatedDiv").html(result); 
				alert(data)
				$.modal.close();
			});		
		}else{
			alert(data)
			$.modal.close();
		}
	});
}

/**
 * Function to create device config file
 * @param configfile
 * @param stbName
 * @param boxType
 */
function createDeviceConfigFile(configfile,stbName,boxType){
	$.get('editDeviceConfigFile', {fileName: configfile,stbName:stbName,boxType:boxType}, function(data) {
		$("#deviceConfigPopup").html(data); 
	});		
	$("#deviceConfigPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {	
			  	width: ($(window).width() - 50),
			  	height:  ($(window).height() -100)	  
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

/**
 * Function to donwload device config file
 * @param configFileName
 */
function downloadDeviceConfigFile(configFileName){
	window.location = "downloadDeviceConfigFile?configFileName="+ configFileName
}

/**
 * Function to delete device config file
 * @param configFileName
 * @param boxTypeId
 * @param stbName
 */
function deleteDeviceConfigFile(configFileName,boxTypeId,stbName){
	var url = $("#url").val();
	$.get(url+'/boxType/getBoxType', {id: boxTypeId}, function(data) {
		var boxTypeName = data[0]+'.config'
		if(configFileName == boxTypeName){
			alert("Cannot delete box type config file")
		}else{
			$.get('deleteDeviceConfigFile', {fileName: configFileName,boxType:boxTypeId,stbName:stbName}, function(result) {
				$("#deviceConfigFile").html(""); 
				$("#deviceConfigFileUpdatedDiv").html(""); 
				$("#deviceConfigFileUpdatedDiv").html(result); 
			});
		}
	});
}

/**
 * Function to upload device config file
 * @param createFileName
 * @param fileName
 * @param finalDeviceConfigFileType
 * @param boxType
 * @param stbName
 * @param editFlagForDeviceConfigForm
 */
function uploadDeviceConfigFile(createFileName,fileName,finalDeviceConfigFileType,boxType,stbName,editFlagForDeviceConfigForm){
	var finalFileName
	if(createFileName != "" && createFileName != null){
		finalFileName = createFileName
	}else{
		finalFileName = fileName
	}
	var elem = new FormData(document.forms.namedItem('uploadDevConfigForm'));
	elem.append('finalFileName', finalFileName);
	 var url="uploadDeviceConfiguration";
     $.ajax({
         url:url,
         type:'POST',
         data:elem,
         processData: false,
         contentType: false ,
         success:function (response) {
				if(response == 'File uploaded successfully' && editFlagForDeviceConfigForm == 'true'){
					alert(response)
					$.modal.close();
				}else if(response == 'File uploaded successfully' && editFlagForDeviceConfigForm != 'true'){
					$.get('updateDeviceConfigDiv', {fileName: finalFileName,finalDeviceConfigFileType:finalDeviceConfigFileType,boxType:boxType,stbName:stbName}, function(result) {
						$("#deviceConfigFile").html(""); 
						$("#deviceConfigFileUpdatedDiv").html(result); 
						alert(response)
						$.modal.close();
					});
				}else{
					alert(response)
				}
            }
     });
}
