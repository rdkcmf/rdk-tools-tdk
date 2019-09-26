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
	
	$(".checkbox").each(function() {
		this.checked = false;
	});

});

var count = 0;
function checkBoxClicked(that) {
	if(that.checked){
		count ++;
		document.getElementById("delete").disabled=false;
	}
	else {
		count --;
	}
	if(count <=0){
		document.getElementById("delete").disabled=true;
	}
}

function populateBoxManufacturerField(that){
	$.get('getBoxManufacturer', {id:that.id}, function(data) {		
		document.getElementById("boxManufacturerId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}


function populateBoxTypeField(that){
	$.get('getBoxType', {id:that.id}, function(data) {		
		document.getElementById("boxTypeId").value = that.id;
		document.getElementById("name").value = data[0];
		document.getElementById("typeId").value = data[1];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}

function populateRDKVersionsField(that){
	$.get('getRDKVersions', {id:that.id}, function(data) {		
		document.getElementById("rdkVersionsId").value = that.id;
//		document.getElementById("name").value = data[0];
		document.getElementById("buildVersion").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}

function populateSoCVendorField(that){
	$.get('getSoCVendor', {id:that.id}, function(data) {		
		document.getElementById("soCVendorId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}

function populateScriptTagField(that){
	$.get('getScriptTag', {id:that.id}, function(data) {		
		document.getElementById("scriptTagId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}
function populateGroupField(that){

	$.get('getGroup', {id:that.id}, function(data) {			
		document.getElementById("groupId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}

function onResetClick(){
	$("#updateBtn").hide(); 
	$("#resetBtn").show(); 
	$("#createBtn").show(); 
}

function populateFieldVals(id){
	$.get('populateFields', {id: id}, function(data) {
		$("#userId").val(data[0]); 
		document.getElementById("passwordId").value = "";
		document.getElementById("nameOfUser").value = data[1];
		document.getElementById("email").value = data[2];
		document.getElementById("userName1").value = data[3];
		/*document.getElementById("groupName").value = data[4];*/
		$('#groupName option[value="'+data[4]+'"]"').attr("selected", "selected");		
		if(data[5] == "null"){
		}
		else{
			document.getElementById("passwordId").value = data[5];
		}		
		$('#roleid option[value="'+data[6]+'"]"').attr("selected", "selected");	
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});		
}
function populateTestProfileField(that){
	$.get('getTestProfile', {id:that.id}, function(data) {		
		document.getElementById("testProfileId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}
	
	
