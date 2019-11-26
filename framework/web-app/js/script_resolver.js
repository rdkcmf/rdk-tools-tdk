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
	
	$("#scriptbrowser").treeview({
		animated:"normal",
		persist: "cookie"
	});
	
	$("#scriptbrowser").bind("contextmenu", function(e) {
		e.preventDefault();
	});
	
	$("#addScriptId").contextMenu('script_root_menu', {
		bindings : {
			'add_scriptV' : function(node) {
				hideSearchoptions();
				createScriptForm('RDKV');
			},
			'add_scriptB' : function(node) {
				hideSearchoptions();
				createScriptForm('RDKB');
			}, 
			'add_scriptTCL' : function(node) {
				hideSearchoptions();
				createTCLScriptForm('RDKB_TCL');
			},			
			'download_script' : function(node){
				downloadScriptList();	
			},
			'upload_rdkv_script' : function(node){
				uploadRDKVScript();	
			},
			'upload_rdkb_script' : function(node){
				uploadRDKBScript();	
			},
			/*'upload_test_case' : function(node){
				uploadTestCase();	
			},*/
		}
	});
	
	$("#scriptTypeV").contextMenu('script_type_menu', {
		bindings : {
			'download_testcase': function(node){
				downloadTestCaseList('RDKV');	
			}
		}
	});
	
	$("#scriptTypeB").contextMenu('script_type_menu', {
		bindings : {
			'download_testcase': function(node){
				downloadTestCaseList('RDKB');	
			}
		}
	});
	
	$('.file').contextMenu('script_childs_menu', {
		bindings : {
			'edit_script' : function(node) {
				var vals = node.id.split('-')
				//editScript(node.id);
				editScript(vals[0], vals[1]);
			},
			'delete_script' : function(node) {
				if (confirm('Are you sure you want to delete this script?')) {
					var vals = node.id.split('-')
					removeScript(vals[0],vals[1]);
				}
			}
		}
	});
	
	var decider_id = $("#decider").val();
	
	$("#scriptgrpbrowser").treeview({
		animated:"normal",
		persist: "cookie",
		collapsed: true
	});
	
	$("#scriptgrpbrowser").bind("contextmenu", function(e) {
		e.preventDefault();
	});
	
	$('#addscriptGrpId').contextMenu('scriptgrp_root_menu', {
		bindings : {
			'add_scriptgrpV' : function(node) {
				hideAllSearchoptions();
				createScriptGrpForm('RDKV');
			},
			'add_scriptgrpB' : function(node) {
				hideAllSearchoptions();
				createScriptGrpForm('RDKB');
			},
			'add_scriptgrpTCL' : function(node) {
				hideUpload();
				hideAllSearchoptions();
				createScriptGrpForm('RDKB_TCL');
			},
			'create_customgrp' : function(node) {
				hideUpload();
				hideAllSearchoptions();
				getSuiteDetails();
			},
			'upload_scriptGroup' : function(node) {	
				showUploadOption();
			},
			'update_scriptgrp' : function(node) {	
				updateScriptGroup();
			},
			
		}
	});
		
	$('.hasChildren').contextMenu('scriptgrp_childs_menu', {
		bindings : {
			'edit_scriptgrp' : function(node) {
				hideSearchoptions();
				editScriptGroup(node.id);
			},
			'delete_scriptgrp' : function(node) {
				if (confirm('Do you want to delete property?')) {
					removeScriptGroup(node.id);
				}
			}
		}
	});

	$("#scriptid").addClass("changecolor");
	
});
/**
 * Function for show Test case doc 
 */
/*function uploadTestCase(){
	$("#responseDiv123").hide();
	$("#up_load").hide();
	$("#up_load_rdkv_script").hide();	
	$("#up_load_rdkb_script").hide();
	$("#list-scriptDetails").hide();
	$("#list-scriptDetails1").hide();
	$("#up_load_tc").show();
}*/

/**
 * Function for display the upload script option through UI
 */

function uploadRDKVScript(){
	$("#responseDiv123").hide();
	$("#up_load").hide();
	$("#up_load_rdkv_script").show();	
	$("#up_load_rdkb_script").hide();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#update_scriptgroup").hide();
}
function uploadRDKBScript(){
	$("#responseDiv123").hide();
	$("#up_load").hide();
	$("#up_load_rdkv_script").hide();
	$("#up_load_rdkb_script").show();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#update_scriptgroup").hide();
	
}

function hideUpload(){
	$("#update_scriptgroup").hide();
}


function downloadScriptList(){	
	var value  = confirm("Do you want to download  consolidated scripts details ?");
	if(value == true){
		$.get('downloadScriptList',{},function(data){
			window.location = "downloadScriptList";
		});
	}
}

function downloadTestCaseList(category){	
	var value  = confirm("Do you want to download  consolidated testcase details ?");
	if(value == true){
		alert("Please wait, Test case document download may take few minutes...");
		window.location = "exportAllTestCases?category="+ category
	}
}

/**
 * function will shows the upload option 
 */
function showUploadOption(){
	$("#responseDiv123").hide();
	$("#up_load").show();
	$("#up_load_rdkv_script").hide();
	$("#up_load_rdkb_script").hide();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#update_scriptgroup").hide();
}

/**
 * function will shows the upload option 
 */
function updateScriptGroup(){
	$("#responseDiv123").hide();
	$("#up_load").hide();
	$("#up_load_rdkv_script").hide();
	$("#up_load_rdkb_script").hide();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#update_scriptgroup").show();
}
/**
 * Function will hide the upload option.
 */

function hideUploadOption(){
	$("#responseDiv123").show();
	$("#up_load").hide();
	$("#up_load_rdkv_script").hide();	
	$("#up_load_rdkb_script").hide();
	$("#update_scriptgroup").hide();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
}

var displayedGroups = [];

/**
 * Method returns script file list on hovering over test suite.
 */
function getScriptsList(val, scriptGroup, scriptInstanceTotal, totalScripts){
	var group = val.id;
	if(displayedGroups.indexOf(group) < 0){
		if(scriptGroup != null && ""!=scriptGroup.trim() && group != null && "" != group.trim()){
			displayedGroups.push(group);
			$.get('getScriptsList', {group: scriptGroup},function(data) {
				var val = JSON.parse(data);
				var displayHtml = "";				
				var scriptGroupCount = 0;				
				for(key in val){					
					var elem = val[key];
					displayHtml= displayHtml+				
						'<li><span  id="' + elem["moduleName"] + '@' + elem["scriptName"] + '"><a href="#" onclick="editScript(' + "'" + elem["moduleName"] + '@' + 
						elem["scriptName"]+ "','"+elem["category"]+ "'); " +
							"highlightTreeElement(" + "'scriptList_', '0', '" + scriptInstanceTotal + "');" +
							"highlightTreeElement('scriptGroupList_', '" + scriptGroupCount + "', '" + totalScripts + "' );"+
							'return false;">'+elem["scriptName"]+'</a></span></li>';
						++scriptGroupCount;
				}
				var displayClass = ".scripts_"+ group;
				$(displayClass).html(displayHtml);
			});
		}
	}
}
/**
 * Add scripts on the script group
 */

function addScripts() {
	var re = document.getElementById("resultElement");
	var selectable = document.getElementById("selectable");
	var sortable = document.getElementById("sortable");
	var scriptElement = document.getElementById("scriptElement");
	var scriptList = scriptElement.innerHTML;

	if (re.value.length > 0) {
		var array = re.value.split(",");
		for (i = 0; i < array.length; i++) {
			var firstChild = document.getElementById("sortable").firstChild;
			scriptList = scriptList + "," + array[i]
			var lie = document.getElementById(array[i]).innerHTML;
			$("#sortable").append(
					'<li id = "sg' + array[i]
							+ 'end" title = '+lie+'class="ui-state-default">' + lie + '</li>');
			$("#" + array[i]).remove()
		}
		refreshElements();
	} else {
		alert("Please select a script to add");
	}

}

/**
 * 
 * Display Script Detail Summary or TestSuite Summary depending on the radio button clicked by user
 */

function display(val) {
	if (val.trim() === 'scriptSummary') {
		$("#suiteDetailsSummary").hide();
		$("#scriptDetailsSummary").show();
		$("#list-scriptDetailsV").show();
		$("#scriptTableV").dataTable( {
		    "sPaginationType": "full_numbers",
		    "bRetrieve": true
		});
		$("#list-scriptDetailsB").show();
		$("#scriptTableB").dataTable( {
			"sPaginationType": "full_numbers",
			"bRetrieve": true
		});
		var scriptId = $("#currentScriptId").val();
		if(scriptId!=null && scriptId!=""){
			editScript(scriptId);
		}
		var scriptGroupId = $("#currentScriptGroupId").val();
		if(scriptGroupId){
			editScriptGroup(scriptGroupId);
		}
	} else if (val.trim() === 'suiteSummary') {
		$("#scriptDetailsSummary").hide();
		$("#suiteDetailsSummary").show();
		$("#list-suiteDetailsV").show();
		$("#suitetTableV").dataTable( {
			"sPaginationType": "full_numbers",
			"bRetrieve": true
		});
		$("#list-suiteDetailsB").show();
		$("#suiteTableB").dataTable( {
			"sPaginationType": "full_numbers",
			"bRetrieve": true
		});
		var scriptId = $("#currentScriptId").val();
		if(scriptId!=null && scriptId!=""){
			editScript(scriptId);
		}
		var scriptGroupId = $("#currentScriptGroupId").val();
		if(scriptGroupId){
			editScriptGroup(scriptGroupId);
		}
	} else {}
}

/**
 * Remove scripts from the script group 
 */

function removeScripts(){
	var re = document.getElementById("sgResultElement");
	var selectable = document.getElementById("selectable");
	var sortable = document.getElementById("sortable");
	var scriptElement = document.getElementById("scriptElement");
	var scriptList = scriptElement.innerHTML;
	if(re.value.length > 0){
	var array = re.value.split(",");
	for(i=0 ; i< array.length;i++){
		var idd = array[i];
		var newId = idd.replace("sg","");
			newId = newId.replace("end","");
		var lie = document.getElementById(idd);
		var data = lie.innerHTML;
		var index = data.lastIndexOf("</div>");
		data = data.substring(index + 6, data.length);
			$("#selectable").append('<li id = "'+newId+'" title = '+data+'class="ui-state-default">' + data + '</li>');
			$("#"+array[i]).remove();
	}
	
		refreshElements();
	}else{
		alert("Please select a script to remove");
	}
	
	
}
/**
 * Move up scripts in the script group 
 */

function moveUp() {
	var re = document.getElementById("sgResultElement");
	
	if(re.value.length > 0){
		
	var array = re.value.split(",");
	for (i = 0; i < array.length; i++) {
		var idd = array[i];
		var lie = document.getElementById(idd);
		var indx = $( "li[id*='sgscript-']" ).index( lie );
		var prevEl = $( "li[id*='sgscript-']" ).get(indx-1).id
		if (indx == 0){
			var prevEl = $( "li[id*='sgscript-']" ).get($( "li[id*='sgscript-']" ).length -1 ).id
			$("li[id*='"+prevEl+"']").after($("li[id*='"+idd+"']"));
		}else{
			$("li[id*='"+prevEl+"']").before($("li[id*='"+idd+"']"));
		}
	}
	}else{
		alert("Please select a script to move up");
	}
}


/**
 * Move down scripts in the script group   
 */

function moveDown() {
	var re = document.getElementById("sgResultElement");
	if(re.value.length > 0){
	var array = re.value.split(",");
	for (i = array.length -1 ; i >= 0; i --) {
		var idd = array[i];
		var lie = document.getElementById(idd);
		var indx = $( "li[id*='sgscript-']" ).index( lie );
		var nxtEl = "";
		if ($( "li[id*='sgscript-']" ).length > (indx + 1)){
			nxtEl = $( "li[id*='sgscript-']" ).get(indx+1).id;
			$("li[id*='"+nxtEl+"']").after($("li[id*='"+idd+"']"));
		}else{
			nxtEl = $( "li[id*='sgscript-']" ).get(0).id;
			$("li[id*='"+nxtEl+"']").before($("li[id*='"+idd+"']"));
		}
	}
	}else{
		alert("Please select a script to move down");
	}

}


function refreshElements(){
	
	$( "#selectable" ).selectable({
		 stop: function() {
		 var result = $( "#select-result" ).empty();
		 var data = ""
		 var myArray = [];
		 
		 $( ".ui-selected", this ).each(function() {
		 var index = $( "#selectable li" ).index( this );
		 data = data +"," +(index +1)
		 result.append( " #" + ( index + 1 ) );
		 myArray.push(this.id)
		 });
		 document.getElementById("resultElement").value = myArray;
		 }
		 });

	 $( "#sortable" ).selectable({
		 stop: function() {
		 var result = $( "#select-result" ).empty();
		 var data = ""
		 var myArray = [];
		 
		 $( ".ui-selected", this ).each(function() {
		 var index = $( "#sortable li" ).index( this );
		 data = data +"," +(index +1)
		 result.append( " #" + ( index + 1 ) );
		 myArray.push(this.id)
		 });
		 document.getElementById("sgResultElement").value = myArray;
		 }
		 });
	 
	 document.getElementById("resultElement").value = [];
	 document.getElementById("sgResultElement").value = [];
}

/**
 * updateScriptGrp
 */

function updateSG() {
	var sortable = document.getElementById("sortable");

	var dataList = ""
	$( "li[id*='sgscript-']" ).each(function(index) {
		
		var elmnt = $(this).attr('id');
		elmnt = elmnt.replace("sgscript-","");
		
		elmnt = elmnt.replace("end","");
		//if(!(dataList.contains(","+elmnt+","))){
			dataList = dataList +","+ elmnt;
		//}
	});

	var name = document.getElementById("scriptName").value;
	var id = document.getElementById("sgId").value;
	var version = document.getElementById("sgVersion").value;
	
	var name = document.getElementById("scriptName").value;
	if(name == null || name.length == 0 ){
		alert("Please enter script group name ");
	}else if(dataList == "" && dataList.length == 0){
		alert("Please add scripts to the script group");
	}else{
		$.post('updateScriptGrp', {id: id, version:version, idList: dataList, name: name},function(data) {   document.location.reload();  $("#responseDiv123").html(data);  });
	}
}
/**
 *  function for for create script group 
 */
function createSG() {
	var category = document.getElementById("createCategory").value;
	var sortable = document.getElementById("sortable");

	var dataList = ""
	
	$( "li[id*='sgscript-']" ).each(function(index) {
		var elmnt = $(this).attr('id');
		elmnt = elmnt.replace("sgscript-","");
		elmnt = elmnt.replace("end","");
		dataList = dataList +","+ elmnt;
	});

	var name = document.getElementById("scriptName").value;
	if(name == null || name.length == 0 ){
		alert("Please enter script group name ");
	}else if(dataList == "" && dataList.length == 0){
		alert("Please add scripts to the script group");
	}else{ 
		$.get('createScriptGrp', {idList: dataList, name: name, category:category.trim()},function(data) {   document.location.reload();  $("#responseDiv123").html(data); });
	}
}
function createScriptForm(category) {
	checkAnyEditingScript();
	$("#up_load").hide();
	$("#update_scriptgroup").hide();
	$("#up_load_rdkv_script").hide();	
	$("#up_load_rdkb_script").hide();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#responseDiv123").show();
	$.get('createScript', {category:category}, function(data) { $("#responseDiv").html(data); });
}

/** 
 * function for add new tcl script through UI 
 * @param id
 * @param category
 */
function createTCLScriptForm(category) {
	checkAnyEditingScript();
	$("#up_load").hide();
	$("#update_scriptgroup").hide();
	$("#up_load_rdkv_script").hide();	
	$("#up_load_rdkb_script").hide();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#responseDiv123").show();
	$.get('createScript', {category:category}, function(data) { 
		$("#responseDiv").html(data);		
	});
}

function editScript(id , category ) {
	if(category.trim() !== 'RDKB_TCL'){
		hideUploadOption();
		hideSearchoptions();
		checkAnyEditingScript();
		$.get('editScript', {id: id , category : category}, function(data) { $("#responseDiv").html(data); });
	}else{
		editTclScript(id);
	}
}

function editTclScript(scriptName) {
	// Issue fix
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	hideSearchoptions();
	checkAnyEditingScript();
	$.get('tclScriptDisplay', {scriptName: scriptName}, function(data) { 
		$("#responseDiv").html(data); });

}

function checkAnyEditingScript(){
	var scriptName = $("#scriptName").val();
	if(scriptName && scriptName != "undefined"){
		clearLock(scriptName);
	}
}
function showScript(idVal, category) {
	checkAnyEditingScript();
	$.get('editScript', {id: idVal , category : category}, function(data) { $("#responseDiv").html(data); });
}

/*
function removeScript(id){	
	checkAnyEditingScript();
	$("#currentScriptId").val("");
	$.get('deleteScript', {id: id}, function(data) { document.location.reload();  });
}
*/

/*function removeScript(id){
	if(id.contains('@')){
		checkAnyEditingScript();
		$("#currentScriptId").val("");
		$.get('deleteScript', {id: id}, function(data) { document.location.reload();  });
	}
	else{
		alert('Script cannot be deleted');
	}
}*/

function removeScript(id, category){
	
	//if(id.contains('@')){
	//if(id.search('@')){
	// issue fix for delete script  
	if(id.includes('@')){
		checkAnyEditingScript();
		$("#currentScriptId").val("");
		$.get('deleteScript', {id: id, category:category}, function(data) { document.location.reload();  });
	}else if(category === 'RDKB_TCL'){
		$.get('deleteTCLScript', {id: id, category:category}, function(data) { document.location.reload();  });
	}
	else{
		alert('Script cannot be deleted');
		//$.get('deleteScript', {id: id, category:category}, function(data) { document.location.reload();  });
		
	}
}


function createScriptGrpForm(category) {	
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#responseDiv123").show()
	checkAnyEditingScript();
	$.get('create', {category:category},function(data) { $("#responseDiv").html(data); });
}

function getSuiteDetails() {	
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#responseDiv123").show()
	
	$.get('getSuiteDetails',function(data) { $("#responseDiv").html(data); });
}

/**
 * Function for module or random wise script group script list sort
 * - Saving the current script group  script list  
 * - value : module / random based on the button selection. 
 * - Shows 'edit' page   
 */
function moduleOrRandomSort(value){
	var dataList = ""
		$( "li[id*='sgscript-']" ).each(function(index) {			
			var elmnt = $(this).attr('id');
			elmnt = elmnt.replace("sgscript-","");			
			elmnt = elmnt.replace("end","");
			//if(!(dataList.contains(","+elmnt+","))){
				dataList = dataList +","+ elmnt;
			//}
		});	
		var name = document.getElementById("scriptName").value;
		var id = document.getElementById("sgId").value;
		var version = document.getElementById("sgVersion").value;
		$.get('scriptGroupListSave', {
			id:id, name:name , idList: dataList ,
		}, function(data) {
			if(data == 'true'){
				var sortValue = ""
				if(value == "module" ){
					sortValue = "modulescriptlist"
				}else{
					sortValue = "randomlist"
				}	
				$.get('edit',{name:name, value :sortValue}, function(data){
					$("#responseDiv").html(data); });
				$.get('getScriptsList', {group: id}, function(data) { $(id).html(data); });
			}else{
			}
		});
}

/**
 *  When clicking the script group diplay details 
 * @param id
 */
function editScriptGroup(id) {
	var value = "normal"
	hideUploadOption();
	hideAllSearchoptions();
	checkAnyEditingScript();
	$.get('edit', {name: id , value : value}, function(data) { $("#responseDiv").html(data); });
	$.get('getScriptsList', {group: id}, function(data) { $(id).html(data); });
}

function updateProgressMessage(){
	alert("Test Suite update in progess...");
}

function updateCompletionMessage(){
	alert("Test Suite update completed.");
}

function exportScripts() {
	$.get('exportScriptAsXML', function(data) { alert("Script exporting is done.");});
}

function removeScriptGroup(id){	
	
	$.get('deleteScriptGrp', {id: id}, function(data) { document.location.reload();  });
}

function clearScriptArea(){
	var scripttextarea = document.getElementById('scriptArea');
	scripttextarea.innerHTML = "";
	document.getElementById("scriptArea").value = scripttextarea.innerHTML.html_entity_decode();	
}

function showStreamDetails(){		
	$.get('showStreamDetails', {}, function(data) { $("#streamDetailsPopup").html(data); });		
	$("#streamDetailsPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 400
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });

	$("#locktable").dataTable( {
		"sPaginationType": "full_numbers"
	} );		
}	

function hideSearchoptions(){
	$("#advancedSearch").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
}

function hideAllSearchoptions(){
	$("#advancedSearch").hide();
	$("#minSearch").hide();
	$('.veruthe').empty();
}

function displayAdvancedSearch(){	
	$("#list-scriptDetailsV").show();
	$("#list-scriptDetailsB").show();
	$("#list-suiteDetailsV").show();
	$("#list-suiteDetailsB").show();
	$("#radioDiv").show();
	$("#advancedSearch").show();
	$("#minSearch").hide();
	$('.veruthe').empty();
	$('.responseclass').empty();
}
	

function showMinSearch(){	
	$("#advancedSearch").hide();
	$("#list-scriptDetailsV").hide();
	$("#list-scriptDetailsB").hide();
	$("#list-suiteDetailsV").hide();
	$("#list-suiteDetailsB").hide();
	$("#radioDiv").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
}

function showExistingSuite(){
	$("#existingSuiteId").show();
	$("#newSuiteId").hide();
}

function showNewSuite(){
	$("#existingSuiteId").hide();
	$("#newSuiteId").show();
}


/**
 * Function to check whether device is saved or not. If yes show edit page.
 */
function updateScriptList(scriptName){
	$.get('fetchScript', {scriptName: scriptName}, function(data) {
		if(data!=""){
			if($("#isScriptExist").val()==""){
				$("#currentScriptId").val(data);
				setTimeout(function(){location.reload();editScript()},1000);
			}
			$("#isScriptExist").val("");
		}
		$("#scriptMessageDiv").show();
	});
}


function updateScriptListWithScriptName(scriptName){
	var category = document.getElementById('category').value.trim()
	$.get('fetchScriptWithScriptName', {scriptName: scriptName,category:category}, function(data) {
		if(data!=""){
			if($("#isScriptExist").val()==""){
				$("#currentScriptId").val(data);
				setTimeout(function(){location.reload();tclScriptDisplay()},1000);
			}
			$("#isScriptExist").val("");
		}
		$("#scriptMessageDiv").show();
	});
}
/**
 * Function to check whether script with same name exist or not.
 * @param scriptName
 */
function isScriptExist(scriptName){
	var category = document.getElementById("category").value;
	var ptest = document.getElementById("ptest").value;
	var synopsis = document.getElementById("synopsis").value;
	synopsis = synopsis.trim()
	if(scriptName){
		$.get('fetchScriptFromDb', {scriptName: scriptName, category:category}, function(data) {
			if(data!=""){
				$("#isScriptExist").val(data);
				alert("Duplicate Script Name not allowed. Try Again.")
			}else if (ptest == "null" || ptest == ""){
				alert("Please select a valid primitive test !!!")
			}else if(synopsis == "" || !synopsis){
				alert("Please fill the synopsis field !!!")
			}else{
				$("#isScriptExist").val("");
				$("#scriptMessageDiv").show();
			}
		});
	}
	else{
		alert("Please fill the name field ")
	}
}


function showSkipRemarks(me){
	if (me.checked) {
		$("#skipRemarks").show();
		$("#skipReason").show();
		$("#skipRemarks123").show();
		$("#skipReason123").show();
		$("#remarks").show();
	} else {
		$("#remarks").val('');
		$("#remarks").hide();
		$("#skipReason").hide();
		$("#skipRemarks").hide();
		$("#skipRemarks123").hide();
		$("#skipReason123").hide();	
	}
	$("#skipReason").val("");
}

function enableEdit(me,scriptName,session){
	
	$("#scriptName").val(scriptName);
	
	$.get('addEditLock', {scriptName: scriptName,session:session}, function(data) {
		if(data){
			if(data == "false"){
				alert("Script is being modified by another user !!!");
				$("#warningMsg").html("Script is being modified by another user !!!");
			}
		}
	});
	
	$("#save").show();
	$("#cancel").show();
	$("#editButton").hide();
}

function enableEditTcl(scriptName){
	
	$.get('addEditLock', {scriptName: scriptName}, function(data) {
		if(data){
			if(data == "false"){
				alert("Script is being modified by another user !!!");
				$("#warningMsg").html("Script is being modified by another user !!!");
			}
		}
	});
	
	$("#saveTcl").show();
	$("#cancelTcl").show();
	$("#editButtonTcl").hide();
	$("#tclText").prop("disabled",false);
}
function disableEdit(me,scriptName){
	$.get('removeEditLock', {scriptName: scriptName}, function(data) {
	});
	
}
function cancelTclEdit(scriptName){
	$("#editButtonTcl").show();
	$("#tclText").prop("disabled",true);
	$("#saveTcl").hide();
	$("#cancelTcl").hide();
	$.get('removeEditLock', {scriptName: scriptName}, function(data) {
	});
}

function updateTclContents(scriptName){

	var content = document.getElementById('tclText').value;
	if(content){
		if(content.trim() !== ''){
			$.post('saveTcl', {content:content, scriptName:scriptName},function(data){
				$("#tclText").prop("disabled",true);
				$("#editButtonTcl").show();
				$("#saveTcl").hide();
				$("#cancelTcl").hide();
				$("#scriptMessageDiv").html(data);
			});
		}
		else{
			alert('Content cannot be empty');
		}
	}
	else{
		alert('Content cannot be empty');
	}
}

function clearLock(scriptName){
	$.get('removeEditLock', {scriptName: scriptName}, function(data) {
	});
}

function showSkipRemarksLabel(){	
	$("#skipRemarks123").hide();
	$("#skipReason123").hide();
}

function sleepIt(milliseconds) {
	  var start = new Date().getTime();
	  for (var i = 0; i < 1e7; i++) {
	    if ((new Date().getTime() - start) > milliseconds){
	      break;
	    }
	  }
	}


function refreshListStart(){
	alert(" Please wait, script list refresh will take some time.");
} 
function scriptRefreshSuccess(){
	alert("The script list refreshed sucessfully.");
	window.location.reload(); 
}
function scriptRefreshFailure(){
	alert(" Error while refreshig the script list.");
	window.location.reload(); 
	
}
function testSuitesCleanUp(){
	alert(" Please wait, test suites clean up will take some time.");
} 
function testSuitesCleanUpSuccess(){
	alert("The  test suites cleaned sucessfully.");
	window.location.reload(); 
}
function testSuitesCleanUpFailure(){
	alert(" Error while clean up the test suites.");
	window.location.reload(); 
}

/**
 * Function for  Suite clean up with N/A scripts 
 * @param name
 */
function cleanUpTestSuite(name ,  category){	
	$.get('verifyScriptGroup', {name: name, category : category}, function(data) { 
		var val = JSON.parse(data);
		if(val === true){
			alert("Script Group cleaned succesfully ");
			var value = "normal"
				hideUploadOption();
				hideAllSearchoptions();
				checkAnyEditingScript();
				$.get('edit',{name:name, value :value}, function(data){
					$("#responseDiv").html(data); });
				$.get('getScriptsList', {group: id}, function(data) { $(id).html(data); });	 
		}else{
			alert("Error while clean up  the test suite clean up. ");		
		}		
	});	 
}
/**
 * function for  before suite clean up
 */
function cleanUp(){
	alert("Please wait, Suite clean up will take some time. ")
}
/**
 * Function will display pop up for add new test case doccument
 */
function editTestCase(scriptName, primiveTest,category){
	$.get('editTestCaseDoc', {name: scriptName , primitiveTestName : primiveTest, category: category}, function(data) { $("#testCaseDocPopUp").html(data); });		
	$("#testCaseDocPopUp").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            //width: 700,
	            //height: 800
			  	width: ($(window).width() - 500),
			  	height:  ($(window).height() -130)	   
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });		
}

/**
 * Function for update test case doc 
 */
function updateTestCase(moduleName, category, primitiveTest, script){
	var tcId = document.getElementById("tcId").value;
	var tcObjective = document.getElementById("tcObjective").value;
	var tcType = document.getElementById("tcType").value;	
	var tcSetup = document.getElementById("tcSetup").value;
	var tcApi = document.getElementById("tcApi").value;
	var tcInputParams = document.getElementById("tcInputParams").value;
	var preRequisits = document.getElementById("preRequisits").value;
	var tcApproch = document.getElementById("tcApproch").value;
	var tcExpectedOutput = document.getElementById("tcExpectedOutput").value;
	var priority = document.getElementById("priority").value;	
	var testStub = document.getElementById("testStub").value;
	var remarks = document.getElementById("test_remarks").value;
	var releaseVersion = document.getElementById("ReleaseVersion").value;	
	//var tcStreamId = document.getElementById("tcStreamId").value;
	var tcSkip = document.getElementById("tcSkipped1").value;	
	var testScript = document.getElementById("testScript").value;	
	if( tcId && tcObjective && tcType && tcSetup && tcApi && tcInputParams && tcApproch && tcExpectedOutput  && priority && testStub && testScript ){
		$.get('updateTestcaseDetails',{tcId:tcId,tcObjective:tcObjective, tcType:tcType, tcSetup:tcSetup,tcApi:tcApi, tcInputParams:tcInputParams,preRequisits:preRequisits , tcApproch:tcApproch, tcExpectedOutput:tcExpectedOutput , priority:priority, testStub:testStub, remarks:remarks, releaseVersion:releaseVersion ,moduleName:moduleName, primitiveTest:primitiveTest,category:category,script:script,tcSkip:tcSkip,testScript:testScript}, function(data) {
			var val = JSON.parse(data);
			if( val == true ){
				alert(" Test cases updated successfully ");
			}else{
				alert(" Test cases not updated ");
			}
		});
	}else{
		alert(" Test case not updated, Please fill the mandatory fields");	
	}
}

/**
 * Function display the new test case doc in the UI 
 */
function newTestCaseAdd(category,uniqueId){
	var name = document.getElementById("name").value;
	if(name != null && name.length > 0 ){
	$.get('addTestCaseDoc', {category:category,uniqueId:uniqueId,name:name}, function(data) { $("#testCaseDocPopUp").html(data); });		
	$("#testCaseDocPopUp").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            //width: 700,
	            //height: 800
			  	width: ($(window).width() - 500),
			  	height:  ($(window).height() -130)	   
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	}else{
		alert("Please enter a valid script name");
	}
}


/**
 * Function for add new test case doc 
 */
function addTestCase(category,uniqueId){		
	var tcId = document.getElementById("newtcId").value;
	var tcObjective = document.getElementById("newtcObjective").value;
	var tcType = document.getElementById("newtcType").value;
	var tcSetup = document.getElementById("newtcSetup").value;
	var tcApi = document.getElementById("newtcApi").value;
	var tcInputParams = document.getElementById("newtcInputParams").value;
	var preRequisits = document.getElementById("newpreRequisits").value;
	var tcApproch = document.getElementById("newtcApproch").value;
	var tcExpectedOutput = document.getElementById("newtcExpectedOutput").value;
	var priority = document.getElementById("newpriority").value;
	var testStub = document.getElementById("newtestStub").value;
	var remarks = document.getElementById("newtest_remarks").value;
	var releaseVersion = document.getElementById("newReleaseVersion").value;	
	//var tcStreamId = document.getElementById("newtcStreamId").value;
	var tcSkip = document.getElementById("newtcSkipped").value;
	var testScript = document.getElementById("newtestScript").value;
	if( tcId && tcObjective && tcType && tcSetup && tcApi &&  tcInputParams && tcApproch && tcExpectedOutput  && priority && testStub && testScript ){
		$.get('addTestCaseInScript',{tcId:tcId,tcObjective:tcObjective, tcType:tcType, tcSetup:tcSetup,tcApi:tcApi, tcInputParams:tcInputParams,preRequisits:preRequisits , tcApproch:tcApproch, tcExpectedOutput:tcExpectedOutput , priority:priority, testStub:testStub, remarks:remarks, releaseVersion:releaseVersion ,testScript:testScript, tcSkip:tcSkip, category:category,uniqueId:uniqueId}, function(data) {
			var val = JSON.parse(data);
			if( val == true ){
				alert(" Test case added while saving the script");
			}
		});
	}else{		
		alert("Please fill the mandatory fields");
	}
}

/**
 * Function to update the system created script groups based on module.
 */
function updateScriptGroups(){
	var category = document.getElementById("category").value;
	var module = document.getElementById("moduleId").value;
	
	if(category == null || category == ""){
		alert("Please select a category.");
		return;
	}
	
	if(module == null || module == "" ){
		alert("Please select a module.");
		return;
	}
	
	var flag = false;
	$.get('getScriptUpdateStatus', function(data) {
		var val = JSON.parse(data);
		flag = val;
		if( val == true ){
			alert(" Another Test Suite update in progress !!! Please try after sometime.");
		}else{
			alert("Starting Test Suite update... ");
			$.get('updateTestSuite',{category:category,module:module}, function(data) {
				alert("Test Suite update completed !!! ");
			});
		}
	});
	
	}

/**
 * Function used to downloading the test case doc according to the user user choice
 * @param scriptGrpName
 * @param category
 */
function downloadScriptGroupTestCase(scriptGrpName , category){
	var value  = confirm("Do you want to download test case details ?");
	if(value == true){	
		// Ajax call not working  for download the report
		// Specify controller function with params using "window.location" 
		alert("Please wait, Test case document download may take few minutes...");
		window.location = "downloadScriptGroupTestCase?category="+ category+"&scriptGrpName="+scriptGrpName; 
	}	
}