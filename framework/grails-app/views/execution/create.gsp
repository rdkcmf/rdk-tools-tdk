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
<%--<!DOCTYPE html>--%>
<html>
<head>
<meta name="layout" content="main">
<%@ page import="org.codehaus.groovy.grails.validation.routines.InetAddressValidator" %>
<g:set var="entityName"
	value="${message(code: 'ScriptExecution.label', default: 'ScriptExecution')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.treeview.css')}" />	

<title>Script Execution</title>
<g:javascript library="jquery.cookie" />
<g:javascript library="jquery.treeview.async" />
<g:javascript library="jquery.treeview" />
<g:javascript library="jquery.contextmenu.r2" />
<g:javascript library="execution_resolver" />
<g:javascript library="jquery.dataTables"/>
<g:javascript library="jquery-ui"/>
<g:javascript library="common"/>	
<g:javascript library="jquery.more"/>
<g:javascript library="select2"/>
<link rel="stylesheet" href="${resource(dir:'css',file:'demo_table.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<script type="text/javascript">
//Popup window code
function newPopup(url) {
	popupWindow = window.open(
		url,'popUpWindow','height=700,width=800,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
}

$(function() {

	$.datepicker.setDefaults({		
		changeMonth: true,
		changeYear: true	
		});
	
	 $( "#datepicker" ).datepicker();
	 $( "#todatepicker" ).datepicker();
	 $( "#cleanFromDate" ).datepicker();
	 $( "#cleanToDate" ).datepicker();

});

$(document).ready(function() {

	$(":checkbox").each(function() {
		$('.resultCheckbox').prop('checked', false);
		mark(this);
	});
	
	$('.markAll').prop('checked', false);
	document.getElementById("category").value = 'All';
});

	
</script>
<link rel="stylesheet" href="${resource(dir:'css',file:'select2.css')}" type="text/css" />
</head>
<body>	
	<div>
		<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
		</g:if>
		<g:if test="${error}">
			<ul class="errors" role="alert">
				<li>${error}</li>
			</ul>
		</g:if>
		<br>
		<g:hiddenField id="url" name="url" value="${url}"/>
		<table class="noClass" style="border: 1; border-color: black;">
			<tr>
				<td>
						<div id="deleteMessageDiv"></div>
				</td>
			</tr>
			<tr>
				<td style="width: 20%;" class="treeborder">
				<div id="device_status">
					<div id="root_menu" class="" style="width: 100%; height: 400px; overflow: auto;">
						<div id="device_statusTotal">
						<ul id="browser" class="filetree">
							<li class="" id="root"><span class="folder" id="addconfId">Device</span>
								
								<ul>
										<li><span class="folder" id="">RDK-V</span>
											<ul>
											 <span id="device_statusV">
												<% int deviceStatusCount = 0; %>
												<g:each in="${deviceListV}" var="device">
														<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
														<% deviceStatusCount++; %>
														<div id="tooltip_${name}" class="tooltip"
															title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}    &#013;BoxType : ${device.boxType}    &#013;Status : ${device.deviceStatus}">
															<li id="deviceExecutionList_${deviceStatusCount}"><g:if
																	test="${device.deviceStatus.toString()=="NOT_FOUND" }">
																	<span class="filedevicenotfound" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}' );  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
																	<span class="filedevicefree" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
																	<span class="filedevicebusy" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
																	<span class="filedevicehang" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
																	<span class="filedevicetdkenabled" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="ALLOCATED" }">
																	<span class="filedevicebusy"><a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a></span>
																</g:if></li>
														</div>
													</g:each>
													</span>
											</ul>
										</li>

										<li><span class="folder" id="">RDK-B</span>
											<ul>
												 <span id="device_statusB">
												<% int deviceStatusCount2 = 0; %>
												<g:each in="${deviceListB}" var="device">
														<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
														<% deviceStatusCount2++; %>
														<div id="tooltip_${name}" class="tooltip"
															title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}    &#013;BoxType : ${device.boxType}    &#013;Status : ${device.deviceStatus}">
															<li id="deviceExecutionList_${deviceStatusCount2}">
															<g:if test="${device.deviceStatus.toString()=="NOT_FOUND" }">
																	<span class="filedevicenotfound" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}' );  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
																	<span class="filedevicefree" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
																	<span class="filedevicebusy" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
																	<span class="filedevicehang" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
																	<span class="filedevicetdkenabled" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="ALLOCATED" }">
																	<span class="filedevicebusy"><a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a></span>
																</g:if></li>
														</div>
													</g:each>
													</span>
													</ul>
											</li>
											<li><span class="folder" id="">RDK-C</span>
											<ul>
											 <span id="device_statusC">
												<% int deviceStatusCountRDKC = 0; %>
												<g:each in="${deviceListC}" var="device">
														<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
														<% deviceStatusCountRDKC++; %>
														<div id="tooltip_${name}" class="tooltip"
															title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}    &#013;BoxType : ${device.boxType}    &#013;Status : ${device.deviceStatus}">
															<li id="deviceExecutionList_${deviceStatusCount}"><g:if
																	test="${device.deviceStatus.toString()=="NOT_FOUND" }">
																	<span class="filedevicenotfound" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}' );  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
																	<span class="filedevicefree" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
																	<span class="filedevicebusy" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
																	<span class="filedevicehang" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
																	<span class="filedevicetdkenabled" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="ALLOCATED" }">
																	<span class="filedevicebusy"><a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a></span>
																</g:if></li>
														</div>
													</g:each>
													</span>
											</ul>
										</li>
											
											</ul>
										
								</li>
							</ul>
							</div>
							</div>
					</div>
					<div class="contextMenu" id="enable_menu">
										<ul>
											<li id="enable"  >EnableTDK</li>
	          								<li id="disable" >DisableTDK</li>
	        							</ul>
	      			</div>									
	  		</td> 
				<td style="width: 84%;">	
					<div style="width: 100%; overflow: auto;">
						<g:select name="filter" id="filter" from="${['RDKB','RDKV','RDKC','RDKB_TCL']}" noSelection="['All':'All']" value="${category }" onchange="loadXMLDoc()"/>
							<div style="width: 96%; overflow: auto; text-align: right; vertical-align: top;">
							<script>						
								$(document).bind("keypress", function (e) {    									
									if (e.keyCode == 13) 
									{        									
										$("#searchSubmit").click();
        								return false;
    								}
								});
								</script>

								<g:form controller="execution">
									<g:textField name="searchName" id="searchId" value="" />
								<span class="buttons"><g:submitToRemote
										after="hideExectionHistory();" before="showSpinner();"
										onSuccess="hideSpinner();" class="find" id="searchSubmit"
										action="searchExecutionList" update="searchResultDiv"
										value="Search" /></span>

								<img src="../images/more.png" title="Advanced Search"
									onclick="displayAdvancedSearch();"></img>
								<span id="spinner1" style="display: none;"> <img id="sss"
									src="${resource(dir:'images',file:'spinner.gif')}" />
								</span>
							</g:form>
						</div>
							<div id="advancedSearch" style="display:none;width: 100%; overflow: auto;">
								<g:form controller="execution" >
								<table>															
									<tr>
										<th colspan="6">Search</th>
									</tr>
									<tr>
										<td valign="middle">From</td>
										<td valign="middle"><input type="text" id="datepicker" name="fromDate" />
										</td>
										<td valign="middle">To</td>
										<td valign="middle"><input type="text" id="todatepicker" name="toDate"/>										
										</td>
										<td></td>
										<td valign="middle">
										
										</td>
									</tr>
									<tr>
										<td valign="middle">DeviceName</td>
										<td valign="middle"><g:textField name="deviceName"/></td>
										<td valign="middle">Status</td>
										<td valign="middle">
											<select name="resultStatus" id="resultStatus" style="width: 150px">
												<option value="">--Please Select--</option>
												<option value="UNDEFINED">UNDEFINED</option>
												<option value="SUCCESS">SUCCESS</option>
												<option value="FAILURE">FAILURE</option>
								 			</select>
										</td>	
										<td valign="middle"></td>
										<td valign="middle"></td>
									</tr>
									<tr>
										<td valign="middle">ScriptType</td>
										<td valign="middle">											
								 			<select name="scriptType" id="scriptType" onchange="showScriptTypes();" style="width: 150px">
												<option value="">--Please Select--</option>
												<option value="Script">SINGLE SCRIPT</option>
												<option value="TestSuite">SCRIPTGROUP</option>												
											</select>
										</td>
										<td valign="middle"><span id="scriptLabel" style="display:none;">Script/ScriptGroup</span></td>
										<td valign="middle"><span id="scriptVal" style="display:none;"><g:textField id="scriptValue" name="scriptVal"/></span>									
										</td>
										<td></td>
										<td valign="middle" width="20%">
											<span class="buttons">
												<g:submitToRemote before="displayWaitSpinner();" class="find" action="multisearch" update="searchResultDiv" value="Search" onSuccess="hideWaitSpinner();" />
											</span>
											<img src="../images/less.png" title="Simple Search" onclick="showMinSearch();"></img>
											<span id="spinnr" style="display: none;">											
										              <img id="ss" src="${resource(dir:'images',file:'spinner.gif')}" />
										    </span>													
										</td>
									</tr>
									<tr>
										<td colspan="6"><hr></td>
									</tr>																		
								</table>
								</g:form>
						</div>
						<div id="searchResultDiv" style="width: 100%;overflow: auto;" class="veruthe"></div>
					
						<div id="listscript" style="width: 97%; overflow: auto; ">
							<g:render template="listExecution"/>
						</div>	
					</div>		
					<div id="responseDiv" style="width: 100%; height: 600px; overflow: auto;" class="responseclass"></div>
				</td>
			</tr>
		</table>			 
	</div>
	<div class="contextMenu" id="childs_menu">
		<ul>
			<li id="reset_device">
         		<img src="../images/delete.png" />
         		Reset Device</li>
              	
			<li id="reset_IpRule">
         		<img src="../images/delete.png" />
         		Reset Ip Rule</li>
       	</ul>
	</div>
	<div id="executionLogPopup" style="display: none; overflow: auto; width : 98%; height : 98%;">			
	</div>
	
	<div id="executionStatusPopup" style="display: none; overflow: auto; width : 98%; height : 98%;">			
	</div>

	<div id="cleanupPopup" style="display: none; overflow: auto;">			
		<g:form controller="execution" ><br>
		<table>																	
			<tr>
				<td valign="middle">From</td>
				<td valign="middle"><input type="text" id="cleanFromDate" name="cleanFromDate" />
				</td>
				<td valign="middle">To</td>
				<td valign="middle"><input type="text" id="cleanToDate" name="cleanToDate"/>										
				</td>
				<td></td>
				<td valign="middle">
				<span class="buttons">
					<g:submitToRemote before="showSpinner();" class="delete" action="deleteExecutions" update="searchDelResultDiv" value="Delete" onSuccess="hideSpinnerForDelete();" />
					
					<span id="delspinnr" style="display: none;">											
						<img id="ss" src="${resource(dir:'images',file:'spinner.gif')}" />
					</span>	
					
				</span>										
				</td>
			</tr>
		</table>
		<span id="searchDelResultDiv"></span>
		</g:form>
	</div>
	<div id="combinedExcelPopUp" style="display: none; overflow: auto; width : 98%; height : 98%;" >	
		<div>
			<div>
			   	<div style="position: absolute;left:10px;top:5px;">
					<button style="font-weight: bold;font-size:15px;color:#2989b3;font-style: italic;font-family: Times New Roman;" onclick="helpDivToggle()" >i</button>
				</div>
   			 	<div style="font-size:20px;font-weight: bold;text-align: center;position: relative;">
   			 		Combined Report Generation
   			 	</div>
			</div>
			<div style="height : 20px;">
			</div>
			<div id="helpDiv" style="display: none;font-style: italic;">
	   			 <p>Feature to generate combined report of executions of same device type. 
	   			    Select the From and To Dates, Box Type and Category and click on the button "Filter Executions".
	   			    The filtered executions will be listed below. 
	   			    Select the executions for report generation 
	   			    (Maximum limit is 10 and minimum is 2) and click on 
	   			    the button "Generate Combined Report". 
	   			    The report generated will have combined details of the executions selected. 
	   			 </p>
			</div>
		</div>
		<g:formRemote name="myForm" update="searchFilterResultDiv" method="GET"
						before="validateInputFields();"
              			action="${createLink(controller: 'execution', action: 'filterExecutions')}"
              			url="[controller: 'execution', action: 'filterExecutions']"><br>
		<table>																
			<tr>
				<td valign="middle">From</td>
				<td valign="middle"><input type="text" id="generateFromDate" name="generateFromDate" required/><span class="required-indicator">*</span>
				</td>
				<td valign="middle">To</td>
				<td valign="middle"><input type="text" id="generateToDate" name="generateToDate" required/><span class="required-indicator">*</span>										
				</td>
				<td></td>
				<td valign="middle">
					<span class="buttons"><input type="submit" style="font-weight: bold;" name="filterExecutions" value="Filter Exceutions">
					</span>
				</td>
			</tr>
			<tr>
				<td>Category</td>
				<td>
					<g:select id="categoryId" name="category" from="${['RDKV','RDKB', 'RDKV_THUNDER']}" value="${params?.category}"/>
				</td>
				<td>Box Type</td>
				<td id="boxTypeId">
					<select name="boxType" id = "boxType">
						<option value="">Please Select</option>
					</select>
				</td>
			</tr>
			<tr>
				<td>ScriptType</td>
				<td>											
					<select name="scriptTypeValue" id="scriptTypeField" onchange="showScriptTypesForCombined();" style="width: 150px">
						<option value="">All</option>
						<option value="Script">SINGLE SCRIPT</option>
						<option value="TestSuite">SCRIPTGROUP</option>												
					</select>
				</td>
				<td><span id="scriptLabelId" style="display:none;">Script/ScriptGroup</span></td>
				<td><span id="scriptFieldId" style="display:none;"><g:textField id="scriptValueId" name="scriptValue"/></span>									
				</td>
			</tr>
			<g:hiddenField name = "validate" id = "validate" value = ""/>
		</table>
		</g:formRemote>
		<span id="searchFilterResultDiv" style="width: 100%;overflow: auto;"></span>
	</div>
	<g:hiddenField name = "selectedDevice" id = "selectedDevice" value = ""/>
	<g:hiddenField name = "deviceInstance" id = "deviceInstance" value = "${deviceInstanceTotal}"/>

</body>
</html> 
