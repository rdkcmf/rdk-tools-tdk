<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2016 RDK Management

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
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.DeviceGroup"%>
<%@ page import="com.comcast.rdk.Utility"%>

<script type="text/javascript">
$(document).ready(function() {
	$("#scripts").select2();	
	$("#devices").select2();
	$("#scriptGrp").select2();
	$("#scriptsThunder").select2();
	$("#scriptsThunderPython").select2();
	$("#scriptGrpThunderPython").select2();
	document.getElementById("rdkCertificationDiagnosisId").disabled = true;
	document.getElementById("rdkCertificationPerformanceId").disabled = true;
	document.getElementById("rdkCertificationStbLogTransferId").disabled = true;
});

</script>

<div id="display">
<g:form  method="post">
	<input type="hidden" name="id" id="id" value="${device?.id}">
	<g:hiddenField name="stbname" id="stbname" value="${device?.stbName}" />
	<g:hiddenField name="stbtype" id="stbtype" value="${device?.isThunderEnabled}" />
	<g:hiddenField name="exId" id="exId" value="${device?.id}" />	
	<g:hiddenField name="category" id="category" value="${category}"/>
	<g:hiddenField id="thunderExecutionType" name="thunderExecutionType" value="javascript"/>
	<table>
		<tr>
			<th colspan="2" align="center">Execute script on ${device?.stbName}</th>
		</tr>
		<tr>
			<td>Execution Name</td>
			<td style="vertical-align: middle;">
				<span id="defExcName">
					<g:textField readonly="true" id="defexecName" name="name" required="" value="${device?.stbName}-${datetime}" class="textwidth"/>
					<a href="#"><img style="vertical-align: middle;" src="../images/edit.png" onclick="showEditableExecName();" /></a>
				</span>
				<span id="givenExcName" style="display:none;">
					<g:textField id="newexecName" name="execName" required="" value="${device?.stbName}-${datetime}" class="textwidth"/>
					<a href="#"><img style="vertical-align: middle;" src="../images/undo.png" onclick="showDefaultExecName();"/></a>					
				</span>		
				<a href="#"><img style="vertical-align: middle;" src="../images/refresh.gif" onclick="showDateTime();"/></a>				
			</td>		
		</tr>
		<tr>
			<td style="vertical-align: middle;">Device</td>
			<td style="vertical-align: middle;">
				<select id="devices" name="devices" multiple="true" id="functionValue" onchange="showDateTime();" style="height:200px;width:400px" class="many-to-one selectCombo">
					<g:each in="${devices}" var="deviceInstance">
						<g:if test="${deviceInstance.id == device.id}">
							<option value="${deviceInstance.id}" selected="selected">${deviceInstance.stbName}</option>
						</g:if>
						<g:else>
							<option value="${deviceInstance.id}">${deviceInstance.stbName}</option>
						</g:else>
					</g:each>
				</select>
			</td>		
		</tr>
		<g:if test="${device?.isThunderEnabled == 1}">
			<tr>
				<td>Select Execution Type</td>
				<td>
					<input onclick="jsExecution();" id="javaScriptThunderRadio" type="radio" name="myGroupExecutionTypeThunder" checked="checked" value="JavascriptThunder" />Storm
				    &emsp;<input onclick="pythonExecution();" id="pythonThunderRadio" type="radio" name="myGroupExecutionTypeThunder" value="PythonThunder" />RdkService
				    
				</td>
			</tr>
		</g:if>
		<tr>
			<td>Select Type</td>
			<td>
			    <g:if test="${device?.isThunderEnabled != 1}">
				    <input onclick="showSuite();" id="testSuiteRadio" type="radio" name="myGroup" value="TestSuite" />TestSuite 
				    &emsp;<input onclick="showSingle();" id="singleTestRadio" type="radio" name="myGroup" checked="checked" value="SingleScript" />SingleScript
				</g:if>
				<g:else>
		            <input onclick="showSuiteThunder();" id="testSuiteRadioThunder" type="radio" name="myGroupThunder" value="TestSuite" />TestSuite 
				    &emsp;<input onclick="showSingleThunder();" id="singleTestRadioThunder" type="radio" name="myGroupThunder" checked="checked" value="SingleScript" />SingleScript				    
				</g:else>	
			</td>		
		</tr>	
		<g:if test="${category != 'RDKV' && device?.isThunderEnabled != 1}">
		<tr>
			<td>Select Script Type</td>
			<%--<td>${deviceInstance.id}
				<input onclick="${remoteFunction(action: 'showDevices',params: [category:'RDKB', id:device?.id])}" id="pythonRadio" type="radio" name="" checked="checked" value="TestSuite" />Python 
				&emsp;<input onclick="${remoteFunction(action: 'showDevices',params: [category:'RDKB_TCL', id:device?.id])}" id="tclRadio" type="radio" name="" value="SingleScript" />TCL	
			</td>		
		--%>
			<td>
				<input onclick="pageLoadOnScriptType('RDKB','${device?.id}')" id="pythonRadio" type="radio" name="" checked="checked" value="TestSuite" />Python 
				&emsp;<input onclick="pageLoadOnScriptType('RDKB_TCL','${device?.id}')" id="tclRadio" type="radio" name="" value="SingleScript" />TCL	
			</td>	
		</tr>
		</g:if>
		<tr>
			<td>
			    <div id="testSuiteSpan" style="display: none;">
			        <label>Select TestSuite</label>
			    </div>
			    <div id="scriptSpan">
			        <label>Select Script</label>
			    </div>
			</td>
			<td>
			    <g:if test="${device?.isThunderEnabled != 1}">	
				    <div id="testSuite" style="display: none;">
				        <g:select id="scriptGrp" multiple="true" style="height:200px;width:400px" onchange="showDateTime();" name="scriptGrp"  from="${scriptGrpList}" value="" class="many-to-one selectCombo"/>
				    </div>
				    <div id="singletest" >
				        <g:select id="scripts" multiple="true" style="height:200px;width:400px" onchange="showDateTime();" name="scripts"  from="${scriptList}" value="" class="many-to-one selectCombo"/>
				    </div>
				</g:if>
				<g:else>
					<div id="testSuiteThunder" style="display: none;">
						<g:select id="scriptGrpThunder" onchange="showDateTime();" name="scriptGrpThunder" noSelection="['' : 'Please Select']" from="${scriptGrpList}" optionKey="id" required="" value="" class="many-to-one selectCombo"/>
				    </div>
				    <div id="singletestThunder" >
				        <g:select id="scriptsThunder" name="scriptsThunder" multiple="true" style="height:200px;width:400px" onchange="showDateTime();" name="scriptsThunder"  from="${scriptListStorm}" value="" class="many-to-one selectCombo"/>
				    </div>
				    <div id="testSuiteThunderPython" style="display: none;">
						<g:select id="scriptGrpThunderPython" name="scriptGrpThunderPython" multiple="true" style="height:200px;width:400px" onchange="showDateTime();"  from="${scriptGrpRdkService}" value="" class="many-to-one selectCombo"/>
				    </div>
				    <div id="singletestThunderPython" style="display: none;">
				        <g:select id="scriptsThunderPython" name="scriptsThunderPython" multiple="true" style="height:200px;width:400px" onchange="showDateTime();" from="${sRdkList}" value="" class="many-to-one selectCombo"/>
				    </div>
				</g:else>						
			</td>						
		</tr>	
		<tr>
			<td>Repeat Test Type</td>
			<td>				
				<%--<g:textField size="5" onkeypress="return digitonly(event);" id="repeatId" name="repeatNo" required="" value="1" />&nbsp; times (Not Applicable for scheduling)
				--%>
				<input onclick="showfullRepeat();" id="fullRepeatRadio" type="radio" name="myGroupRepeat" checked="checked" value="fullRepeat" title="Repeat the full execution"/><label title="Repeat the full execution">Full execution</label>
				&emsp;<input onclick="showindividualRepeat();" id="individualRepeatRadio" type="radio" name="myGroupRepeat" value="individualRepeat" title="Repeat each individual script execution"/><label title="Repeat each individual script execution">Individual scripts</label>
				<g:hiddenField id="repeatType" name="repeatType" value="full"/>
			</td>
		</tr>
		<tr>
		    <td></td>
		    <td>
				    <input size="5" id="repeatId" onkeypress="return isNumberKey(event)" type="text" name="repeatNo" required="" value="1">
		            <input size="5" id="individualRepeatId" onkeypress="return isNumberKey(event)" type="text" name="individualRepeatNo" style="display: none;" required="" value="1">&nbsp; times
				    &emsp;&emsp;<g:checkBox id="rerunId" name="rerun" checked="false" />&nbsp;Re-Run on Failure
			</td>
		</tr>
		<g:if test="${device?.isThunderEnabled != 1}">
			<tr>
				<td>Execution Options</td>
				<td><g:checkBox id="benchmarkId" name="benchMarking" checked="false" />&nbsp;Timing Info 
				&emsp;&emsp;<g:checkBox id="systemDiagId" name="systemDiagnostics" checked="false"  />&nbsp;Performance Data
				&emsp;&emsp;<g:checkBox id="transferLogsId" name="transferLogs" checked="false"  />&nbsp;Transfer STB logs
				</td>
			</tr>	
		</g:if>
		<g:else>
			<tr>
				<td>Execution Options</td>
				<td><g:checkBox id="rdkCertificationDiagnosisId" name="rdkCertificationDiagnosis" checked="false"  />&nbsp;Rdk Certification Diagnosis
				&emsp;&emsp;<g:checkBox id="rdkCertificationPerformanceId" name="rdkCertificationPerformance" checked="false"  />&nbsp;Rdk Certification Performance
				&emsp;&emsp;<g:checkBox id="rdkCertificationStbLogTransferId" name="rdkCertificationStbLogTransfer" checked="false"  />&nbsp;Rdk Certification STB Log Transfer
				</td>
			</tr>
		</g:else>
		<tr>
			<td colspan="2" align="center">
			    <g:if test="${device?.isThunderEnabled != 1 }">				
					<g:hiddenField name="pageFlag" value="execute"/>
					<span id="executeBtn" class="buttons"><g:submitToRemote class="save" before="showWaitSpinner();" 
					action="executeScriptMethod" controller="execution" update="resultDiv${device?.id}" value="Execute" 
					onComplete="completed(${device?.id})" onFailure="changeStyles()"  onSuccess="changeStyles()" >
					</g:submitToRemote>&emsp;	
					</span>
					<span id="scheduleBtn" class="buttons">
						<input id="scheduleBtnID" type=button class="save"  onclick="showScheduler(${device?.id}, '${category}');return false;"
						value="Schedule" />	
					</span>
				</g:if>
				<g:else>
					<div id="thunderJavascriptExecuteButtons">
				    	<span id="executeBtnThunder" class="buttons"><g:submitToRemote class="save" before="showWaitSpinnerThunder();" 
                    	action="executeThunderScript" controller="thunder" update="resultDiv${device?.id}" value="Execute" 
                    	onComplete="completedThunder(${device?.id})" onFailure="changeStylesThunder()"  onSuccess="changeStylesThunder()">
                    	</g:submitToRemote></span>&emsp;
				    	<span id="scheduleBtnThunder" class="buttons">
						<input id="scheduleBtnThunderID" type=button class="save"  onclick="showScheduler(${device?.id}, '${category}');return false;"
						value="Schedule" disabled/>
						</span>
					</div>
					<div id="thunderPythonExecuteButtons" style="display: none;">
						<span id="executeBtnPython" class="buttons"><g:submitToRemote class="save" before="showWaitSpinner();" 
						action="executeScriptMethod" controller="execution" update="resultDiv${device?.id}" value="Execute" 
						onComplete="completed(${device?.id})" onFailure="changeStyles()"  onSuccess="changeStyles()" >
						</g:submitToRemote>&emsp;	
						</span>
						<span id="scheduleBtnPython" class="buttons">
						<input id="scheduleBtnPythonID" type=button class="save"  onclick="showSchedulerRdkService(${device?.id}, '${rdkServiceCategory}');return false;"
						value="Schedule"/>	
						</span>
					</div>
				</g:else>
				<div id="popup" style="display: none;">
			              Please wait.....<img id="s" src="${resource(dir:'images',file:'spinner.gif')}" />
			    </div>				
			</td>
		</tr>		
		<tr>		
			<td>Execution Result</td>					
			<td style="width:80%;">
				<div id="resultDiv${device?.id}" style="border-color: #FFAAAA;border-style: solid;
					border-width: 1px;width: 550px;height:215px;overflow:auto;" >
					
				</div>
				<div id="dynamicResultDiv" style="display: none;border-color: #FFAAAA;border-style: solid;
					border-width: 1px;width: 550px;height:215px;overflow:auto;" >
					
				</div>
				<g:hiddenField id="grailsUrl" name="grailsUrl" value="${grailsUrl}"/>
		 	</td>
		</tr>						
	</table>
</g:form>
<div id="scheduleJobPopup" style="display: none; overflow: auto; width : 98%; height : 98%;">	
</div>

</div>


