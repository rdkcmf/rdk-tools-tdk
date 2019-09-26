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
	
	$("#primitveTestbrowser").treeview({
		animated:"normal",
		persist: "cookie"
		
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});

	$('.folder').contextMenu('root_menu', {
		bindings : {
			'add_propertyV' : function(node) {
				createTestForm('RDKV');
			},
			'add_propertyB' : function(node) {
				createTestForm('RDKB');
			}
		}
	});
	
	
	$('.file').contextMenu('childs_menu', {
		bindings : {
			'edit_test' : function(node) {
				var values = node.id.split("@");
				makeTestEditable(values[0],values[1]);
			},
			'delete_test' : function(node) {
				if (confirm('Are you sure you want to delete this primitive test?')) {
					var values = node.id.split("@")
					removeProperty(values[0], values[1]);
				}
			}
		}
	});
	
	$("#module").live('change', function(){
		var module_id = $(this).val();
		if(module_id != '') {
			getAssociatedFunctions(module_id);
		}
		else {
			$("#functionTd").html('<select style="width: 250px"><option value="">Please Select</option></select>');
		}
		$("#parameterTable").html('');
		$("#buttons").hide();
	});
	$("#primid").addClass("changecolor");
	var decider_id = $("#decider").val();
});

function createTestForm(category) {
	$.get('template',{category:category}, function(data) { $("#responseDiv").html(data); });
}

function createConfigForm() {
	$.get('confTemplate', function(data) { 
		$("#responseDiv").html(data); });
}

function getAssociatedFunctions(module_id) {
	if(module_id != '') {
		$.get('getFunctions', {moduleId: module_id}, function(data) {
			var select = '<select style="width: 250px" id="functionValue" name="functionValue" onchange="getAssociatedParameters()"><option value="">Please Select</option>';
			
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index].id + '">' + data[index].name + '</option>';
			}
			
			select += '</select>';
			
			$("#functionTd").html(''); 
			$("#functionTd").html(select); 
		});
	}
	else {
		$("#functionTd").html('');
		$("#buttons").hide();
		$("#tableheader").hide();
	}
}

function getAssociatedParameters() {
	var function_id = $("#functionValue").val();
	if(function_id != '') {
		$.get('getParameters1', {functionId: function_id}, function(data) {
			var parameter = '';
			var ids = '';
			for(var index = 0; index < data.length; index ++ ) {
				if(index == 0) {
					parameter += '<tr><th>Parameter Name</th><th>Type</th><th>Range</th><th>Value</th></tr>';
				}
				parameter += '<tr><td align="left">&emsp;&emsp;' + data[index].name + '</td><td>' + data[index].type + 
				'</td><td>' + data[index].range + '</td><td align="center"><input type="text" name="value_' + data[index].id + '"></td></tr>';
				ids += data[index].id + ', ';
			}			
			$("#parameterTable").html(''); 
			$("#parameterTable").html(parameter);
			$("#parameterTypeIds").val(ids);
			$("#buttons").show();
			$("#tableheader").show();
		});
	}
	else {
		$("#parameterTable").html('');
		$("#buttons").hide();
		$("#tableheader").hide();
	}
}

function makeTestEditable(id, category) {
	$.get('getEditableTest', {id: id, category:category}, function(data) { $("#responseDiv").html(data); });
}

function makeConfEditable(id) {	
	$.get('getEditableTest', {id: id}, function(data) { 
		$("#responseDiv").html(data); });
}

function removeProperty(id, category){
	$.get('deleteTest', {id: id, category:category}, function(data) {document.location.reload(); });
}



/**
 * Function to check whether primitive test  is saved or not.
 */
function updateTestList(testName){
	var category = document.getElementById('category').value;
	
	$.get('fetchPrimitiveTest', {testName: testName, category:category}, function(data) {
		if(data!=""){
			if($("#isTestExist").val()==""){
				$("#currentPrimitiveTestId").val(data);
				//setTimeout(function(){location.reload();makeTestEditable(data);},1000);
				location.reload();
			}
			$("#isTestExist").val("");
		}
		$("#testMessageDiv").show();
	});
}

/**
 * Function to check whether primitive test with same name exist or not.
 * @param testName
 */
function isTestExist(testName){
	var category = document.getElementById('category').value;
	
	$.get('fetchPrimitiveTest', {testName: testName, category:category}, function(data) {
		if(data!=""){
			$("#isTestExist").val(data);
		}
		$("#testMessageDiv").show();
	});
}


function clearValues(){
	$("#parameterTable").html('');
	$("#buttons").hide();
	$("#tableheader").hide();
}








