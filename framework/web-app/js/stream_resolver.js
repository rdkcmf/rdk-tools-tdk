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
	
	$("#streambrowser").treeview({
		animated:"normal",
		persist: "cookie"
		
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});

	$('#video').contextMenu('root_menu', {
		bindings : {
			'add_property' : function(node) {
				createStreamDetailsForm();
			}
		}
	});
	
	$('#radio').contextMenu('root_menu', {
		bindings : {
			'add_property' : function(node) {
				createRadioStreamDetailsForm();
			}
		}
	});
	
	
	$('.videofile').contextMenu('childs_menu', {
		bindings : {
			'edit_test' : function(node) {
				showStreamDetails(node.id);
			},
			'delete_test' : function(node) {
				if (confirm('Are you want to delete property?')) {
					removeProperty(node.id);
				}
			}
		}
	});
	
	$('.radiofile').contextMenu('childs_menu', {
		bindings : {
			'edit_test' : function(node) {
				showRadioStreamDetails(node.id);
			},
			'delete_test' : function(node) {
				if (confirm('Are you want to delete property?')) {
					removeRadioProperty(node.id);
				}
			}
		}
	});
	
	
});

function createStreamDetailsForm() {
	$.get('create', function(data) { $("#responseDiv").html(data); });
}


function createRadioStreamDetailsForm() {
	$.get('createRadio', function(data) { $("#responseDiv").html(data); });
}


function showStreamDetails(id) {
	$.get('edit', {id: id}, function(data) { $("#responseDiv").html(data); });
}


function removeProperty(id){
	$.get('deleteStreamDetails', {id: id}, function(data) { document.location.reload(); });
}

function showRadioStreamDetails(id) {
	$.get('editRadio', {id: id}, function(data) { $("#responseDiv").html(data); });
}


function removeRadioProperty(id){
	$.get('deleteRadioStreamDetails', {id: id}, function(data) { document.location.reload(); });
}













