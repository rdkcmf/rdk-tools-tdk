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

var flagMark = false

$(document).ready(function() {
	$.ajaxSetup ({cache: false});
	timedRefresh();	
	deviceStatusRefresh();	
	$("#browser").treeview({
		
		animated:"normal",
		persist: "cookie"
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});	
	
	$('.filedevicebusy').contextMenu('childs_menu', {
		bindings : {			
			'reset_device' : function(node) {
				if (confirm('Make sure no scripts is currently executed in the device. Do you want to reset the device?')) {
					resetDevice(node.id);
				}
			}
		}
	});
	
	
	/*$('.filedevicefree').contextMenu('childs_menu', {
		bindings : {			
			'reset_IpRule' : function(node) {
				if (confirm('Make sure no scripts is currently executed in the device. Are you want to reset the device?')) {
					resetIPRule(node.id);
				}
			}
		}
	});*/
		
	var decider_id = $("#decider").val();
	$("#execid").addClass("changecolor");	

	$("#scripts").select2();

	$(":checkbox").each(function() {
		$('.resultCheckbox').prop('checked', false);
		mark(this);
	});
	
	$('.markAll').prop('checked', false);
	
	$('#repeatId').attr('readonly', false);
	$('#individualRepeatId').attr('readonly', false);
	if(document.getElementById("scheduleBtnID") != null){
		document.getElementById("scheduleBtnID").disabled = false;
	}
		/*
jQuery 1.9+   $('#inputId').prop('readonly', true);
	 */

	/**
	 * Change the boxtype dropdown according to the category selected
	 */
	$("#categoryId").live('change', function(){
		var category_id = $(this).val();
		if(category_id != '') {
			getBoxTypes(category_id);
		}
		else {
			$("#boxTypeId").html('<select><option value="">Please Select</option></select>');
		}
	});
	
});

/**
 * Function to get the box types according to category and fill it in the boxtype dropdown 
 * @param category_id
 */
function getBoxTypes(category_id) {
	var url = $("#url").val();
	if(category_id != '') {
		$.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
			var select = '<select id="boxType" name="boxType"><option value="">Please Select</option>';
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
			}
			select += '</select>';
			$("#boxTypeId").html(''); 
			$("#boxTypeId").html(select); 
		});
	}
	else {
		$("#boxTypeId").html('');
	}
}

function stopExecution(obj){
	if (confirm('Execution will be stopped after finishing the current test case execution.\nDo you want to stop the execution ? ')) {
		$.get('stopExecution', {execid: obj}, function(data) {});
	}
	
}

function isNumberKey(evt)
{
   var charCode = (evt.which) ? evt.which : event.keyCode
   if (charCode > 31 && (charCode < 48 || charCode > 57))
      return false;

   return true;
}

function showSchedule(){
	if($("#scheduletest").prop('checked') == true){		
		$('#scheduleOptionDiv').show();
	}
	else{
		$('#scheduleOptionDiv').hide();
	}
}

function showSuite(){
	
	$('#testSuite').show();
	$('#singletest').hide();
	$('#scriptSpan').hide();
	$('#testSuiteSpan').show();
	checkRepeat();
	scheduleToggle();
}

function showSingle(){
	$('#singletest').show();
	$('#testSuite').hide();
	$('#scriptSpan').show();
	$('#testSuiteSpan').hide();
	checkRepeat();
	scheduleToggle();
}

function jsExecution(){
	var testSuite = document.getElementById("testSuiteRadioThunder");
	var singleTest = document.getElementById("singleTestRadioThunder");
	var thunderJavascriptExecuteButtons = document.getElementById("thunderJavascriptExecuteButtons");
	var thunderPythonExecuteButtons = document.getElementById("thunderPythonExecuteButtons");
	thunderJavascriptExecuteButtons.style.display = "block";
	thunderPythonExecuteButtons.style.display = "none";
	document.getElementById("thunderExecutionType").value = "javascript";
	document.getElementById("category").value = "RDKV_THUNDER"
	if(singleTest.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').show();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}else if(testSuite.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').show();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}
	checkRepeat();
	scheduleToggle();
}

function pythonExecution(){
	var testSuite = document.getElementById("testSuiteRadioThunder");
	var singleTest = document.getElementById("singleTestRadioThunder");
	document.getElementById("thunderExecutionType").value = "rdkservice";
	var thunderJavascriptExecuteButtons = document.getElementById("thunderJavascriptExecuteButtons");
	var thunderPythonExecuteButtons = document.getElementById("thunderPythonExecuteButtons");
	thunderJavascriptExecuteButtons.style.display = "none";
	thunderPythonExecuteButtons.style.display = "block";
	document.getElementById("category").value = "RDKV"
	if(singleTest.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').show();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').hide();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}else if(testSuite.checked){
		$('#testSuiteThunderPython').show();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}
	checkRepeat();
	scheduleToggle();
}

function showfullRepeat(){
	var fullRepeatCount = document.getElementById("repeatId");
	var individualRepeatCount = document.getElementById("individualRepeatId");
	fullRepeatCount.style.display = "inline";
	individualRepeatCount.style.display = "none";
	document.getElementById("repeatType").value = "full";
	checkRepeat();
	scheduleToggle();
}

function showindividualRepeat(){
	var fullRepeatCount = document.getElementById("repeatId");
	var individualRepeatCount = document.getElementById("individualRepeatId");
	fullRepeatCount.style.display = "none";
	individualRepeatCount.style.display = "inline";
	document.getElementById("repeatType").value = "individual";
	checkRepeat();
	scheduleToggle();
}

/**
 * Function to display thunder test suites in execution page when the user clicks on a device
 */
function showSuiteThunder(){
	var executionTypePython = document.getElementById("pythonThunderRadio");
	var executionTypeJavascript = document.getElementById("javaScriptThunderRadio");
	if(executionTypePython.checked){
		$('#testSuiteThunderPython').show();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').hide();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}else if(executionTypeJavascript.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#testSuiteThunder').show();
		$('#singletestThunder').hide();
		$('#scriptSpan').hide();
		$('#testSuiteSpan').show();
	}
	checkRepeat();
	scheduleToggle();
}

/**
 * Function to display thunder scripts in execution page when the user clicks on a device
 */
function showSingleThunder(){
	var executionTypePython = document.getElementById("pythonThunderRadio");
	var executionTypeJavascript = document.getElementById("javaScriptThunderRadio");
	if(executionTypePython.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').show();
		$('#singletestThunder').hide();
		$('#testSuiteThunder').hide();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}else if(executionTypeJavascript.checked){
		$('#testSuiteThunderPython').hide();
		$('#singletestThunderPython').hide();
		$('#singletestThunder').show();
		$('#testSuiteThunder').hide();
		$('#scriptSpan').show();
		$('#testSuiteSpan').hide();
	}
	checkRepeat();
	scheduleToggle();
}
function pageLoadOnScriptType(category, id){
	var isTestSuiteRadio = document.getElementById('testSuiteRadio').checked;
	var isSingleTestRadio = document.getElementById('singleTestRadio').checked;
	var isFullRepeatRadio = document.getElementById('fullRepeatRadio').checked;
	var isIndividualRepeatRadio = document.getElementById('individualRepeatRadio').checked;
	$.get('showDevices', {id: id, category: category}, function(data) {
		$("#responseDiv").html(data);
		//alert(data);
		if(category === 'RDKB_TCL'){
			document.getElementById('pythonRadio').checked = false;
			document.getElementById('tclRadio').checked = true;
		}
		else{
			document.getElementById('pythonRadio').checked = true;
			document.getElementById('tclRadio').checked = false;
		}
		if(isTestSuiteRadio){
			document.getElementById('testSuiteRadio').checked = true;
			document.getElementById('singleTestRadio').checked = false;
			showSuite();
		}
		if(isSingleTestRadio){
			document.getElementById('testSuiteRadio').checked = false;
			document.getElementById('singleTestRadio').checked = true;
			showSingle();
		}
		if(isFullRepeatRadio){
			document.getElementById('fullRepeatRadio').checked = true;
			document.getElementById('individualRepeatRadio').checked = false;
			showfullRepeat();
		}
		if(isIndividualRepeatRadio){
			document.getElementById('individualRepeatRadio').checked = true;
			document.getElementById('fullRepeatRadio').checked = false;
			showindividualRepeat();
		}
	});
	
	
//	alert(' isTestSuiteRadio : '+isTestSuiteRadio);
//	alert('isSingleTestRadio : '+isSingleTestRadio);
	//alert(' isPythonRadio : '+isPythonRadio);
	//alert('isTclRadio : '+isTclRadio);
	//$.get('showDevices', {id: id, category: category}, function(data) { $("#responseDiv").html(data); });
	
}

function showOnetimeSchedule(){
	$('#onetimeScheduleDiv').show();
	$('#reccuranceScheduleDiv').hide();
}

function showReccuranceSchedule(){
	$('#reccuranceScheduleDiv').show();
	$('#onetimeScheduleDiv').hide();
}

function showDaily(){
	$('#reccurDaily').show();
	$('#reccurWeekly').hide();
	$('#reccurMonthly').hide();
}

function showWeekly(){
	$('#reccurDaily').hide();
	$('#reccurWeekly').show();
	$('#reccurMonthly').hide();
}

function showMonthly(){
	$('#reccurDaily').hide();
	$('#reccurWeekly').hide();
	$('#reccurMonthly').show();
}

function showScript(id, category){
	$.get('showDevices', {id: id, category: category}, function(data) { $("#responseDiv").html(data); });
	$.get('updateDeviceStatus', {id: id,category: 'RDKV'}, function(data) {refreshDevices(data,'RDKV');});
	$.get('updateDeviceStatus', {id: id,category: 'RDKB'}, function(data) {refreshDevices(data,  'RDKB');});
	$.get('updateDeviceStatus', {id: id,category: 'RDKC'}, function(data) {refreshDevices(data,  'RDKC');});
	//$.get('updateDeviceStatus', {id: id,category: 'RDKB'}, function(data) {refreshDevices(data,  'RDKB');});
}

function refreshDevices(data, category){
	var conatiner = null
	if("RDKV" === category){
		container = document.getElementById("device_statusV");
	}
	else if("RDKB" === category){
		container = document.getElementById("device_statusB");
	}
	else if("RDKC" === category){
		container = document.getElementById("device_statusC");
	}
	//container = document.getElementById("device_statusTotal");
	container.innerHTML= data;
	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}

/*function refreshDevices(data){
	var container = document.getElementById("device_status");
	container.innerHTML= data;
	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}*/

function resetDevice(id){
	$.get('resetDevice', {id: id}, function(data) { document.location.reload(); });
}


function resetIPRule(id){
	$.get('resetIPRule', {id: id}, function(data) { document.location.reload(); });
}


function changeStyle(){
	$('#resultDiv').css('display','table');
}

function showExecutionLog(id){
	$.get('showLog', {id: id}, function(data) { $("#executionLogPopup").html(data); });		
	$("#executionLogPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

function executionStatus(id){	
	$.get('executionStatus', {id: id}, function(data) { $("#executionStatusPopup").html(data); });		
	$("#executionStatusPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

/**
 * RdkService schedule function
 * @param id
 * @param category
 * @returns {Boolean}
 */
function showSchedulerRdkService(id, category){	
	var scriptGroup = $("#scriptGrpThunderPython").val();
	var scripts = $("#scriptsThunderPython").val();
    var deviceList = $("#devices").val();
	var repeatid = $("#repeatId").val();

	 if ($('input[name=myGroupThunder]:checked').val()=='TestSuite'){     	
	    	scripts = "";
	 }
	 else{     	
	    	scriptGroup ="";
	 }

	var reRun = "";
	var benchmark = "false";
	var systemDiag = "false"
	var isLogReqd =" false"
    if ($("#rerunId").prop('checked')==true){     	
    	reRun = "true";
    }
	
	if( (deviceList =="" || deviceList == null ) ){
		alert("Please select Device");
		return false;
	}
	
	if(deviceList.length > 1){	
		alert("Scheduling is not currently allowed for multiple devices");
		return false;
	}
	else{
		id = deviceList.toString();		
	}

	if((scripts=="" || scripts == null )&& scriptGroup == "" ){
		alert("Please select Script/ScriptGroup");
		return false;
	}
	var scriptVals = ""
	if(scripts){
		scriptVals = scripts.toString();
	} 
	var scriptGroupVals = ""
	if(scriptGroup){
		scriptGroupVals = scriptGroup.toString()
	}
	$.get('showSchedular', {deviceId : id, devices : deviceList.toString(), scriptGroup : scriptGroupVals, scripts:scriptVals, repeatId:repeatid, rerun:reRun, systemDiagnostics : systemDiag , benchMarking : benchmark  ,isLogReqd :isLogReqd, category:category }, function(data) { $("#scheduleJobPopup").html(data); });		
	$("#scheduleJobPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	$("#scheduletable").dataTable( {
		"sPaginationType": "full_numbers",
		 "bRetrieve": "true" 
	} );	
}

function showScheduler(id, category){	
	
	var scriptGroup = $("#scriptGrp").val();
	var scripts = $("#scripts").val();
    var deviceList = $("#devices").val();
	var repeatid = $("#repeatId").val();

	 if ($('input[name=myGroup]:checked').val()=='TestSuite'){     	
	    	scripts = "";
	 }
	 else{     	
	    	scriptGroup ="";
	 }

	var reRun = "";
	var benchmark = "false";
	var systemDiag = "false"
	var isLogReqd =" false"
    if ($("#rerunId").prop('checked')==true){     	
    	reRun = "true";
    }
	if ($("#benchmarkId").prop('checked')==true){     	
		benchmark = "true";
	}
	if ($("#systemDiagId").prop('checked')==true){     	
		systemDiag = "true";
	}
	if ($("#transferLogsId").prop('checked')==true){  
		
		isLogReqd = "true";
	}
	
	
	if( (deviceList =="" || deviceList == null ) ){
		alert("Please select Device");
		return false;
	}
	
	if(deviceList.length > 1){	
		alert("Scheduling is not currently allowed for multiple devices");
		return false;
	}
	else{
		id = deviceList.toString();		
	}

	if((scripts=="" || scripts == null )&& scriptGroup == "" ){
		alert("Please select Script/ScriptGroup");
		return false;
	}
	var scriptVals = ""
	if(scripts){
		scriptVals = scripts.toString();
	} 
	var scriptGroupVals = ""
	if(scriptGroup){
		scriptGroupVals = scriptGroup.toString()
	}
	$.get('showSchedular', {deviceId : id, devices : deviceList.toString(), scriptGroup : scriptGroupVals, scripts:scriptVals, repeatId:repeatid, rerun:reRun, systemDiagnostics : systemDiag , benchMarking : benchmark  ,isLogReqd :isLogReqd, category:category }, function(data) { $("#scheduleJobPopup").html(data); });		
	$("#scheduleJobPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	$("#scheduletable").dataTable( {
		"sPaginationType": "full_numbers",
		 "bRetrieve": "true" 
	} );	
}

function showCleanUpPopUp(){
	$("#cleanupPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 600,
	            height: 250	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

function showDateTime(){
	$('#defexecName').val(" ");
	checkDeviceList();
	var stbName
	var deviceList = $("#devices").val();
	 if(deviceList == null){
		 stbName = ""
	 }else if(deviceList.length > 1){	
		 stbName = "multiple"
	 }else{
		 stbName = $('#stbname').val();
	 }
	
	$.get('showDateTime', {}, function(data) { 	
		$('#defexecName').val(stbName+"-"+data[0]);
		$('#newexecName').val(stbName+"-"+data[0]);
	});
	checkRepeat();
	scheduleToggle();
}

function checkDeviceList(){
	 var deviceList = $("#devices").val();
	 if(deviceList != null && deviceList.length > 1){		
		 $("#repeatId").val(1);
		// document.getElementById("repeatId").disabled = true;
		 $('#repeatId').attr('readonly', true);
			
	 }
	 else{
		 $('#repeatId').attr('readonly', false);			
		// document.getElementById("repeatId").disabled = false;
	 }
}

function checkRepeat(){
	 var IndividualRepeat = document.getElementById("individualRepeatRadio");
	 var singleSelectedTdk = document.getElementById("singleTestRadio");
	 var singleSelectedRdkService = document.getElementById("singleTestRadioThunder");
	 var thunderExecutionType = document.getElementById("thunderExecutionType").value;
	 var scriptList = $("#scripts").val();
	 var scriptListRdkService = $("#scriptsThunderPython").val();
	 var isThunderEnabled = document.getElementById("stbtype").value;
	 if((isThunderEnabled != 1 && singleSelectedTdk && singleSelectedTdk.checked && IndividualRepeat.checked && scriptList!= null && scriptList.length <=1) || (thunderExecutionType == "rdkservice" && isThunderEnabled == 1 && singleSelectedRdkService && singleSelectedRdkService.checked && IndividualRepeat.checked && scriptListRdkService != null && scriptListRdkService.length <=1)||(thunderExecutionType == "javascript" && isThunderEnabled == 1)){
		 $("#individualRepeatId").val(1);
		 $('#individualRepeatId').attr('readonly', true);
	 }else{
		 $('#individualRepeatId').attr('readonly', false);
	 }
}

function scheduleToggle(){
	 var isThunderEnabled = document.getElementById("stbtype").value;
	 var IndividualRepeat = document.getElementById("individualRepeatRadio");
	 if(isThunderEnabled != 1){
		 var suiteSelectedTdk = document.getElementById("testSuiteRadio");
		 var scriptGroupListTdk = $("#scriptGrp").val();
		 if((suiteSelectedTdk.checked && scriptGroupListTdk!= null && scriptGroupListTdk.length > 1) || (IndividualRepeat.checked)){ 
			 document.getElementById("scheduleBtnID").disabled = true;
		 }else{
			 document.getElementById("scheduleBtnID").disabled = false;
		 }
	 }else{
		 var thunderExecutionType = document.getElementById("thunderExecutionType").value;
		 if(thunderExecutionType == "rdkservice"){
			 var suiteSelectedRdkservice = document.getElementById("testSuiteRadioThunder");
			 var scriptGroupListRdkservice = $("#scriptGrpThunderPython").val();
			 if((suiteSelectedRdkservice.checked && scriptGroupListRdkservice!= null && scriptGroupListRdkservice.length > 1) || (IndividualRepeat.checked)){ 
				 document.getElementById("scheduleBtnPythonID").disabled = true;
			 }else{
				 document.getElementById("scheduleBtnPythonID").disabled = false;
			 }
		 }
	 }
}

function showEditableExecName(){
	$("#givenExcName").show();
	$("#defExcName").hide();
}

function showDefaultExecName(){
	$("#defExcName").show();
	$("#givenExcName").hide();	
	$('#newexecName').val($('#defexecName').val());
}

function displayWaitSpinner(){		
	$("#spinnr").show();
}

function hideWaitSpinner(){	
	$("#spinnr").hide();
}

function showSpinner(){		
	$("#spinner1").show();
}

function hideSpinner(){	
	$("#spinner1").hide();
}

var repeatTask;

var repeatTaskThunder;

function showWaitSpinner(){	
	$("#popup").show();
	$("#executeBtn").hide();
	$("#executeBtnPython").hide();
	var execId = $('#exId').val();
	var deviceList= $('#devices').val();
	if(deviceList  && deviceList.length > 1 )
	{
		$('#resultDiv'+execId).show();	
		$('#resultDiv'+execId).html('Multiple Device Execution ');
		//$('#dynamicResultDiv').show();
	}
	else
	{	
	$('#resultDiv'+execId).hide();
	$('#dynamicResultDiv').show();
	$('#dynamicResultDiv').html('Starting the script execution...');
	repeatTask = setInterval("updateLog()",5000);
	}
}

/**
 * Function to display the spinner gif for thunder executions
 */
function showWaitSpinnerThunder(){
	$("#popup").show();
	$("#executeBtnThunder").hide();
	
	var execId = $('#exId').val();
	var deviceList= $('#devices').val();
	if(deviceList  && deviceList.length > 1 )
	{
		$('#resultDiv'+execId).show();	
		$('#resultDiv'+execId).html('Multiple Device Execution ');
	}
	else
	{
		$('#resultDiv'+execId).hide();
		$('#dynamicResultDiv').show();
		$('#dynamicResultDiv').html('Starting the script execution...');
		repeatTaskThunder = setInterval("updateLogThunder()",1000);
	}
}

/**
 * Function to update thunder logs in UI
 */
function updateLogThunder(){
	var execName = "";
	execName = $('#defexecName').val();
	var suite = "single"
	var scriptNameArray
	var scriptname = ""
	if ($('input[name=myGroupThunder]:checked').val()=='TestSuiteThunder'){
		suite = "suite"
	}else{
		scriptNameArray = $('#scriptsThunder').val();
		if(scriptNameArray.length > 1){
			suite = "multiple"
		}else{
			scriptname = scriptNameArray[0]
		}
	}
	$.get('readOutputFileDataThunder', {executionName: execName, scriptName: scriptname, suiteName: suite}, function(data) {
		$("#dynamicResultDiv").html(data); 
	});
}

/**
 * Function to show the static result div once execution gets completed
 * @param id
 */
function completedThunder(id) {
	if (repeatTaskThunder) {
		clearInterval(repeatTaskThunder);
	}
	showDateTime();
	var execId = $('#exId').val();
	if (id == execId) {
		$('#resultDiv' + execId).show();
		$('#dynamicResultDiv').hide();
	}
}

/**
 * Function to hide wait spinner and show Execute button once execution is completed
 */
function changeStylesThunder(){
	showDateTime();
	$("#popup").hide();
	$("#executeBtnThunder").show();
}

function showSpinner(){
	$("#delspinnr").show();
}

function hideSpinnerForDelete(){
	$("#delspinnr").hide();
	 $( "#cleanFromDate" ).datepicker();
	 $( "#cleanToDate" ).datepicker();
}

function updateLog(){
	var execName = "";
	if(  $("#defexecName").is(":visible") == true )
	{  
		execName = $('#defexecName').val();
	}
	
	if (  $("#newexecName").is(":visible") == true )
	{  
		execName = $('#newexecName').val();       
	}
	$.get('readOutputFileData', {executionName: execName}, function(data) {
		$("#dynamicResultDiv").html(data); 
	});
}

function completed(id) {
	if (repeatTask) {
		clearInterval(repeatTask);
	}
	showDateTime();
	var execId = $('#exId').val();
	if (id == execId) {
		$('#resultDiv' + execId).show();
		$('#dynamicResultDiv').hide();
	}

}
function changeStyles(){
	showDateTime();
	$("#popup").hide();
	var thunderExecutionType = document.getElementById("thunderExecutionType");
	if(thunderExecutionType.value == "javascript"){
		$("#executeBtn").show();
	}else if(thunderExecutionType.value == "rdkservice"){
		$("#executeBtnPython").show();
	}
}

function baseScheduleTableRemove(){		
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	alert("script/ScriptGroup unScheduled");
}
function baseScheduleTableSave()
{
	alert(" Script/ScriptGroup Scheduled");
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	
}
function baseScheduleTableDelete()
{
	
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	
}

/**
 * Dynamic page refresh call. First time called from the document ready of list
 * page
 */
function timedRefresh() {
	if(flagMark == true){
		$('.markAll').prop('checked', true);
	}
	setTimeout("loadXMLDoc();", 5 * 1000);	
}


/**
 * Ajax call to refresh only the list table when dynamic refresh is enabled
 */

var prevCategory = null;

function loadXMLDoc() {
	var xmlhttp;	
	var url = $("#url").val();
	var paginateOffset = $("#pageOffset").val();
	if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("list-executor").innerHTML = xmlhttp.responseText;
			timedRefresh();			
		}
	} 
	if(paginateOffset != undefined){
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
		var category = document.getElementById("filter").value;
		xmlhttp.open("GET", url+"/execution/create?t=" + Math.random()+"&max=10&offset="+paginateOffset+"&devicetable=true&flagMark="+flagMark+"&category="+category, true);
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
	}
	xmlhttp.send();
}

function categoryChange() {
	
	var xmlhttp;	
	var url = $("#url").val();
	var paginateOffset = $("#pageOffset").val();
	if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("list-executor").innerHTML = xmlhttp.responseText;
			timedRefresh();			
		}
	} 
	if(paginateOffset != undefined){
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
		
		var category = document.getElementById("filter").value;
		var prevCategory = document.getElementById("selectedFilter").value;
		if(prevCategory == null || prevCategory != category){
			paginateOffset = 0;
		}
		xmlhttp.open("GET", url+"/execution/create?t=" + Math.random()+"&max=10&offset="+paginateOffset+"&devicetable=true&flagMark="+flagMark+"&category="+category, true);
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
	}
	xmlhttp.send();
}

/**
 * Function used to check box enabled / Disabled
 * 
 */
function callFunc(select) {
	var option =""	
		$('#root_menu').contextMenu('enable_menu', {
			bindings : {
				'enable' : function(node) {
					option = "enable"
					deviceEnabledStatus(node.id,option,select);
				},
				'disable' : function(node) {
					option = "disable"
					deviceDisabledStatus(node.id,option,select);
				}
			}
		});
}


/**
 * Dynamic page refresh call. First time called from the document ready of list
 * page
 */
function deviceStatusRefresh() {
	
	setTimeout("loadXMLDoc1();", 5 * 1000);	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();	
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}
/**
 * function used to change the box status as disabled 
 * @param id
 * @param option
 * @param select
 */
function deviceDisabledStatus(id,option,select){		
	$.get('getTDKDeviceStatus', {id:id,option:option,select:select}, function(data) {});// {refreshDevices(data);});
}
/**
 * function used to change the box status as enabled 
 * @param id
 * @param option
 * @param select
 */

function deviceEnabledStatus(id,option,select){
	$.get('getTDKDeviceStatus', {id:id,option:option, select:select}, function(data) {}); //{refreshDevices(data);});
}


/**
 * Ajax call to refresh only the list table when dynamic refresh is enabled
 */
function loadXMLDoc1() {
	$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true,category:'RDKV'},function(data,status){
		document.getElementById("device_statusV").innerHTML = "";
		document.getElementById("device_statusV").innerHTML = data;
	});
	$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true,category:'RDKB'},function(data,status){
		document.getElementById("device_statusB").innerHTML = "";
		document.getElementById("device_statusB").innerHTML = data;
	});
	$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true,category:'RDKC'},function(data,status){
		document.getElementById("device_statusC").innerHTML = "";
		document.getElementById("device_statusC").innerHTML = data;
	});
	/*$.get('create',{t:Math.random(),max:10,offset:0,devicestatustable:true},function(data,status){
		//alert(data);
		document.getElementById("device_status").innerHTML = "";
		document.getElementById("device_status").innerHTML = data;
	});*/
	
	deviceStatusRefresh();	
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
	$("#advancedSearch").show();
	$("#minSearch").hide();
	$('.veruthe').empty();
	$('.responseclass').empty();
	$("#listscript").hide();
	$("#scriptValue").val('');	
}

function showMinSearch(){	
	$("#advancedSearch").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
	$("#listscript").show();
}

function hideExectionHistory(){
	$("#listscript").hide();
}

function showOther(){
	$("#otherBased").show();
	$("#dateBased").hide()
	$('.veruthe').empty();
	
}

function showDateBased(){
	$("#dateBased").show();
	$("#otherBased").hide();
	$('.veruthe').empty();
}

function showScriptTypes(){
	var choice = $( "#scriptType" ).val()
	if((choice == "")){
		$("#scriptLabel").hide();
		$("#scriptVal").hide();
		$("#scriptValue").val('');
	}
	else{
		$("#scriptLabel").show();
		$("#scriptVal").show();
		$("#scriptValue").val('');
	}
}

/**
 * Method to display the script field based on script type in combined excel popup
 */
function showScriptTypesForCombined(){
	var choice = $( "#scriptTypeField" ).val()
	if((choice == "")){
		$("#scriptLabelId").hide();
		$("#scriptFieldId").hide();
		$("#scriptValueId").val('');
	}
	else{
		$("#scriptLabelId").show();
		$("#scriptFieldId").show();
		$("#scriptValueId").val('');
	}
}

function showFulltextDeviceDetails(k){
	$("#fulltext"+k).show();
	$("#firstfourlines"+k).hide();
	$("#showlessdd"+k).show();	
}

function showMintextDeviceDetails(k){
	$("#fulltext"+k).hide();
	$("#firstfourlines"+k).show();
	$("#showlessdd"+k).hide();	
}


/**
 * Function to perform deletion of marked execution results. This will invoke an
 * ajax method and perform deletion of corresponding execution instance.
 */
function deleteResults() {

	var notChecked = [];
	var checkedRows;
	$(":checkbox").each(function() {
		if (this.checked) {
			checkedRows = checkedRows + "," + this.id;
		} else {
			notChecked.push(this.id);
		}
	});
	if (checkedRows != null && checkedRows != "") {
		
		var result = confirm("Are you sure you want to delete?");
		if (result==true) {
			$.get('deleteExecutioResults', {
				checkedRows : checkedRows
			}, function(data) {
	
				$(":checkbox").each(function() {
					$('.resultCheckbox').prop('checked', false);
	
				});
				$('.markAll').prop('checked', false);
				location.reload();
			});
		}
	}
	else 
	{
		alert("Please select the execution entries")
	}	
}

/**
 * Function to generate combined excel report of selected execution results. The selected executions
 * must be repeat and rerun executions of the original execution.
 */
function combinedExcelReportGeneration(executionIdList) {
	var notChecked = [];
	var checkedRows = "";
	var url = $("#url").val();
	var executionIdArray = JSON.parse(executionIdList);
	for(i=0;i<=executionIdArray.length;i++){
		if ($('#combinedExecutionCheckbox_'+executionIdArray[i]).is(":checked"))
		{
		  checkedRows =  executionIdArray[i] + "," + checkedRows;
		}
	}
	var status 
	if (checkedRows != null && checkedRows != "") {
		var request = new XMLHttpRequest();
		request.open("GET",url+"/execution/checkValidExecutions?checkedRows="+checkedRows, false);
		request.send(null);
		if (request.status === 200) {
			status = request.responseText
		}
		else{
			alert("Some problem occured while processing request")
		}
		if(status == "true"){
			for(i=0;i<=executionIdArray.length;i++){
				$.get('updateMarkStatus', {
					markStatus : 0,
					id : executionIdArray[i]
				}, function(data) {
				});
			}
			alert("Going to generate the report")
			window.open(url+"/execution/combinedExcelReportGeneration/?checkedRows="+checkedRows, '_blank');
			window.focus();
			return false
		}
		else if(status == "overFlow"){
			alert("Maximum number of executions that can be combined is 10 and minimum number is 2")
			return false
		}
	}
	else {
		alert("Please select the execution entries for report generation")
		return false
	}	
}

/**
 * Function to show the combined Excel PopUp
 */
function showCombinedExcelPopUp(){
	$("#combinedExcelPopUp").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 1200,
	            height: 450	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	 $( "#generateFromDate" ).datepicker();
	 $( "#generateToDate" ).datepicker();
	 var today = new Date();
	 var priorDate = new Date();
	 priorDate.setDate(today.getDate() - 30)
	 var ddtoday = String(today.getDate()).padStart(2, '0');
	 var mmtoday = String(today.getMonth() + 1).padStart(2, '0');
	 var yyyytoday = today.getFullYear();
	 today = mmtoday + '/' + ddtoday + '/' + yyyytoday;
	 var ddprior = String(priorDate.getDate()).padStart(2, '0');
	 var mmprior = String(priorDate.getMonth() + 1).padStart(2, '0');
	 var yyyyprior = priorDate.getFullYear();
	 priorDate = mmprior + '/' + ddprior + '/' + yyyyprior;
	 document.getElementById("generateFromDate").value = priorDate
	 document.getElementById("generateToDate").value = today
	 var category_id = "RDKV"
	 var url = $("#url").val();
	 $.get(url+'/boxType/getBoxTypeFromCategory', {category: category_id}, function(data) {
		var select = '<select id="boxType" name="boxType"><option value="">Please Select</option>';
		for(var index = 0; index < data.length; index ++ ) {
			select += '<option value="' + data[index].name + '">' + data[index].name + '</option>';
		}
		select += '</select>';
		$("#boxTypeId").html(''); 
		$("#boxTypeId").html(select); 
	 });
}

/**
 * Function to validate all input fields in combined Excel PopUp
 */
function validateInputFields(){
	document.getElementById("validate").value = "";
	var fromDateString = document.getElementById("generateFromDate").value;
	var toDateString = document.getElementById("generateToDate").value;
	var boxType = document.getElementById("boxType").value;
	var category = document.getElementById("categoryId").value;
	if (fromDateString == "" || toDateString == "" || boxType == "" || category == "") {
	    alert("Please select all the fields");
	    document.getElementById("validate").value = "false";
	}
	var today = new Date();
	var fromDate = new Date(fromDateString);
	var toDate = new Date(toDateString);
	if((fromDate > today) || (toDate > today)){
	    alert('Selected date cannot be greater than todays date');
	    document.getElementById("validate").value = "false";
	}
	if(fromDate > toDate){
		alert('From Date cannot be greater than To Date');
		document.getElementById("validate").value = "false";
	}
}
/**
 * Function to toggle the div containing the combined report feature explanation
 */
function helpDivToggle(){
	  var x = document.getElementById("helpDiv");
	  if (x.style.display === "none") {
	    x.style.display = "block";
	  } else {
	    x.style.display = "none";
	  }
}

/**
 * Function to perform mark all operation in execution page.
 * 
 * @param me
 */
function clickCheckbox(me) {
	

	var $this = $(this);
	if (me.checked) {
		$(":checkbox").each(function() {
			$('.resultCheckbox').prop('checked', true);
			if(this.id != "benchmarkId" && this.id != "rerunId" && this.id != "systemDiagId"){
				mark(this);
			}
		});
		flagMark = true
	} else {
		$(":checkbox").each(function() {
			$('.resultCheckbox').prop('checked', false);
			if(this.id != "benchmarkId" && this.id != "rerunId" && this.id != "systemDiagId"){
			mark(this);
			}
		});
		flagMark = false
	}
}


/**
 * Function to mark individual execution results in execution page.
 * 
 * @param me
 */
function mark(me) {

	if (me.id != 'undefined' && me.id != 'markAll1' && me.id != 'markAll2'
			&& me.id != "" && me.id != null) {
		if (me.checked) {
			$.get('updateMarkStatus', {
				markStatus : 1,
				id : me.id
			}, function(data) {
			});
		} else {
			$.get('updateMarkStatus', {
				markStatus : 0,
				id : me.id
			}, function(data) {
			});
		}
	}	
}

/**
 * Function used to check the current device status is FREE  and available or not
 * @param deviceStatus
 */

function deviceStatusCheck(device,deviceStatus){
	if((deviceStatus != "FREE" && deviceStatus !=  'null')){
		alert("Device is currently not available for execution");
	}else if(device == 'null' ){ 
		 alert("Device name is not configured")
	 }else{
		 executionTriggeredPopUp()		 
	 }
	
}
/**
 * Function check failed scripts available in execution
 * @param executionInstance
 */
function failureScriptCheck(executionName,device,deviceStatus){
	$.get('failureScriptCheck', {
		executionName : executionName,
	}, function(data) {
		if(data == 'false'){
			alert(" No Failed scripts availble for rerun execution");			
		}else{
			deviceStatusCheck(device,deviceStatus)			
		}			
	});
		
}

/**
 * function will shows pop up 
 */
function  executionTriggeredPopUp(){
	alert("Execution Triggered ");	
}



