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

	$("#browser2").treeview({
		animated:"normal"
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});

	$('#addconfId').contextMenu('root_menu_device', {
		bindings : {
			'add_device' : function(node) {
				createDevice("RDKV");
			},
			'add_deviceB' : function(node) {
				createDevice("RDKB");
			},
			'upload_device':function(node){
				uploadRDKVDevice();
			},
			'upload_device_RDKB':function(node){
				uploadRDKBDevice();
			}
		}
	});
	
	$('.file').contextMenu('childs_menu_device', {
		bindings : {
			'edit_device' : function(node) {
				showDevice(node.id);
			},
			'delete_device' : function(node) {
				if (confirm('Are you want to delete this Device?')) {
					deleteDevice(node.id);
				}
			}
		}
	});
	$("#deviceid").addClass("changecolor");
	var decider_id = $("#decider").val();
	$.selectedVDevices = new Array();
	$.selectedBDevices = new Array();
});



/**
 * Function shows the upload device page option  
 */
function uploadRDKVDevice(){
	$("#responseDiv").hide();
	$("#up_load").show();
}

function uploadRDKBDevice(){
	$("#responseDiv").hide();
	$("#up_load_rdkb").show();
}

/**
 * Function used to delete the selected devices based on type
 */
function deleteDevices(type) {
	var devicesToDelete = [];
	if (type == 'V') {
		devicesToDelete = $.selectedVDevices;
	} else {
		devicesToDelete = $.selectedBDevices;
	}
	
	if (devicesToDelete.length > 0) {
		$.get('deleteDevices', {deviceList: devicesToDelete.join(",")}, function(data) {
       		document.location.reload();
       	});
	} else {
        alert('Please select any device to delete');
    }
}

/**
 * Function used to update the list of selected RDK V devices
 */
function onDeviceVSelectionChange(deviceId, id) {
    if($('#'+ id).prop("checked") == true){
    	$.selectedVDevices.push(deviceId);
    } else {
    	var index =  $.selectedVDevices.indexOf(deviceId);
    	if(index >= 0) {
    		$.selectedVDevices.splice(index, 1);
    	}
    }
}

/**
 * Function used to update the list of selected RDK B devices
 */
function onDeviceBSelectionChange(deviceId, id) {
    if($('#'+ id).prop("checked") == true){
    	$.selectedBDevices.push(deviceId);
    } else {
    	var index =  $.selectedBDevices.indexOf(deviceId);
    	if(index >= 0) {
    		$.selectedBDevices.splice(index, 1);
    	}
    }
}

/**
 * function to upload the  Python TDKB E2E/TCL device config file 
 */
function uploadConfig(){
	var gateway = document.getElementById('stbName').value;
	
	var configType = $('input:radio[name=configType]:checked').val();
	
	var ip = document.getElementById('stbIp').value;
	if((gateway != null) && (ip != null)){
		gateway = gateway.trim();
		ip = ip.trim();
		if((gateway !== '') && (ip !== '')){
			var elem = new FormData(document.forms.namedItem('uploadForm'));
			elem.append('gatewayName', gateway);
			elem.append('ip', ip);
			elem.append('configType', configType);
			 var url="uploadConfiguration";
		     $.ajax({
		         url:url,
		         type:'POST',
		         data:elem,
		         processData: false,  // tell jQuery not to process the data
		         contentType: false ,
		         success:function (response) {
		        	 if(response !== 'Upload failed'){
		        		 $('#uploadForm').hide();
		        		 $('#toggleOptions').hide();
		        		 $('#uploadStatus').text(response).css({'color':'green'});
		        	 }
		        	 else{
		        		 $('#uploadStatus').text(response).css({'color':'red'});
		        	 }
		            }
		         });
		}
		else{
			alert('Gateway Name and ip are mandatory');
		}
	}
	else{
		alert('Gateway Name and ip are mandatory');
	}
	
}


/**
 * function for hide upload device option 
 */
function hideUploadOption(){
	$("#responseDiv").show();
	$("#up_load").hide();
	$("#up_load_rdkb").hide();
}

function createDevice(category) {
	hideUploadOption();
	$.get('createDevice',{category:category}, function(data) { $("#responseDiv").html(data); });
}

function showDevice(id,flag) {
	hideUploadOption();
	$.get('editDevice', {id: id, flag:flag}, function(data) { $("#responseDiv").html(data); });
}


function deleteDevice(id){	
	$.get('deleteDevice', {id: id}, function(data) { document.location.reload(); });
}

function ValidateIPaddress()  
{  
	var inputText = $("#stbIp").val();
	var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;  
	if(inputText.match(ipformat))  
	{  	
		return true;  
	}  
	else  
	{  
		alert("You have entered an invalid IP address!");
		$("#stbIp").val("");
		$("#stbIp").focus();
		return false;  
	}  
}  


function ValidateIPaddress1()  
{  
	
	var inputText = $("#systemIP").val();
	var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;  
	if(inputText.match(ipformat))  
	{  	
		return true;  
	}  
	else  
	{  
		alert("You have entered an invalid IP address!");
		$("#systemIP").val("");
		$("#systemIP").focus();
		return false;  
	}  
} 


