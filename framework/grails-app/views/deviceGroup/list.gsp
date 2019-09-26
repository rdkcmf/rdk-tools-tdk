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
<%@ page import="com.comcast.rdk.DeviceGroup" %>
<!DOCTYPE html>
<html>
<head>
<meta name="layout" content="main">
<g:set var="entityName"
	value="${message(code: 'Configuration.label', default: 'Configuration')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.treeview.css')}" />
<title>Device Group</title>
<g:javascript library="jquery.cookie" />
<g:javascript library="jquery.treeview.async" />
<g:javascript library="jquery.treeview" />
<g:javascript library="jquery.contextmenu.r2" />
<g:javascript library="devicegrp_resolver" />
<g:javascript library="config_resolver" />
<g:javascript library="jquery.dataTables"/>
<g:javascript library="jquery-ui"/>
<g:javascript library="common" />
<link rel="stylesheet" href="${resource(dir:'css',file:'demo_table.css')}" type="text/css" />
	<script type="text/javascript">

	$(document).ready(function() {

		var deviceId = $("#currentDeviceId").val();
		if(deviceId!=null && deviceId!=""){
			$("#responseDiv").html("");
			showDevice(deviceId);
		}else{
			$("#devicetable").dataTable( {
				"sPaginationType": "full_numbers"
			});
			$("#devicetable2").dataTable( {
				"sPaginationType": "full_numbers"
			});
		}

		var deviceGroupId = $("#currentDeviceGroupId").val();
		if(deviceGroupId){
			showDeviceGroup(deviceGroupId);
		}
	});


	</script>
</head>
<body>
 
	<a href="#create-primitiveTest" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>	
		<div id="" class="">
			
			<g:if test="${flash.message}">
				<div id="messageDiv" class="message" role="status">${flash.message}</div>
			</g:if>
			<g:if test="${error}">
				<ul class="errors" role="alert">
					<li>${error}</li>
				</ul>
			</g:if>
			
			<g:hasErrors bean="${deviceGroupsInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${deviceGroupsInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<g:hasErrors bean="${deviceGroupsInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${deviceGroupsInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<br>
			<g:hiddenField id="url" name="url" value="${url}"/>
			<input type="hidden" name="decider" id="decider" value="${params.id}">
			
			<span>
			<table class="noClass" style="border: 1; border-color: black;">
				<tr>
					<td style="width: 20%; vertical-align: top;" class="treeborder" >
						<div id="deviceTreeDefault"class="" style="vertical-align: top; max-height: 300px;">
							<ul id="browser2" class="filetree">
								<li id="root"><span class="folder" id="addconfId">Devices</span>
									<ul>
									<div id="deviceTreeDefault"class="" style="overflow: auto;vertical-align: top; max-height: 280px;">
									<li><span class="folder" id="addDeviceRDK">RDK-V</span>
									
									<ul>	
										<%  int stbDeviceCount = 0;
									   		int stbTotalDevices = deviceInstanceSTBTotal * deviceGrpInstanceSTBTotal;
									 	%>
											<g:each in="${deviceInstanceListSTB}" var="parentDevice">
											<g:if test="${parentDevice.isChild == 0}">
												<li class="closed"><span class="file" id="${parentDevice.id}"><a href="#" onclick="showDevice('${parentDevice.id}');  highlightTreeElement('deviceList_', '${stbDeviceCount}', '${deviceInstanceSTBTotal}'); highlightTreeElement('deviceGroupList_', '0', '${stbTotalDevices}'); return false;">${parentDevice.stbName}</a></span>
													<ul>
														<g:each in="${ parentDevice.childDevices}" var="childDevice">
															<% stbDeviceCount++; %>
															<li id="deviceList_${stbDeviceCount}">
																<span class="file" id="${childDevice.id}">
																	<a href="#" onclick="showDevice('${childDevice.id}');  highlightTreeElement('deviceList_', '${stbDeviceCount}', '${deviceInstanceSTBTotal}'); highlightTreeElement('deviceGroupList_', '0', '${stbTotalDevices}'); return false;">${childDevice.stbName}</a>
																</span>
															</li>
													     </g:each>
													</ul>											
												</li>
												 </g:if>
											</g:each>
										</ul>	
										</li>
										<li>
											<span class="folder" id="addDeviceRDKB">RDK-B</span>
											<ul>
											<%  int modemDeviceCount = 0;
									   			int modemTotalDevices = deviceInstanceModemTotal * deviceGrpInstanceModemTotal;
									 		%>
											<g:each in="${deviceInstanceListModem}" var="parentDevice">
											<g:if test="${parentDevice.isChild == 0}">
												<li class="closed"><span class="file" id="${parentDevice.id}"><a href="#" onclick="showDevice('${parentDevice.id}');  highlightTreeElement('deviceList_', '${modemDeviceCount}', '${deviceInstanceModemTotal}'); highlightTreeElement('deviceGroupList_', '0', '${modemTotalDevices}'); return false;">${parentDevice.stbName}</a></span>
													<ul>
														<g:each in="${ parentDevice.childDevices}" var="childDevice">
															<% modemDeviceCount++; %>
															<li id="deviceList_${modemDeviceCount}">
																<span class="file" id="${childDevice.id}">
																	<a href="#" onclick="showDevice('${childDevice.id}');  highlightTreeElement('deviceList_', '${modemDeviceCount}', '${deviceInstanceModemTotal}'); highlightTreeElement('deviceGroupList_', '0', '${modemTotalDevices}'); return false;">${childDevice.stbName}</a>
																</span>
															</li>
													     </g:each>
													</ul>											
												</li>
												 </g:if>
											</g:each>
										</ul>	
										</li>
											</div>
									</ul>
								</li>
							</ul>
						</div>
						<div class="" style="width: 200px; max-height: 400px;vertical-align: top;">
							<ul id="browser1" class="filetree">
								<li class="" id="root1"><span class="folder" id="addDeviceGrpRDK">DeviceGroup</span>
									<ul>
									<% int stbGroupCount = 0; %>
									<div class="" style="max-height: 380px;overflow: auto;vertical-align: top;">
									<li><span class="folder" id="">RDK-V</span>
									<ul>
										<g:each in="${deviceGrpInstanceListSTB}" var="deviceGrp">
											<li class="closed"><span class="hasChildren" id="${deviceGrp.id}"><a href="#" onclick="showDeviceGroup('${deviceGrp.id}'); return false;">${deviceGrp.name}</a></span>
												<ul>
													<g:each in="${deviceGrp.devices}" var="device">
														<% stbGroupCount++; %>
													<li id="deviceGroupList_${stbGroupCount}">
														<span id="${device.id}"><a href="#" onclick="showDevice('${device.id}' , 'STATIC');  highlightTreeElement('deviceList_', '0', '${deviceInstanceSTBTotal}'); highlightTreeElement('deviceGroupList_', '${stbGroupCount}', '${stbTotalDevices}'); return false;">${device.stbName}</a></span>
													</li>
													</g:each>
												</ul>											
											</li>
										</g:each>
										</ul>
										</li>
										<li><span class="folder" id="">RDK-B</span>
										<ul>
											<% int modemGroupCount = 0; %>
											<g:each in="${deviceGrpInstanceListModem}" var="deviceGrp">
											<li class="closed"><span class="hasChildren" id="${deviceGrp.id}"><a href="#" onclick="showDeviceGroup('${deviceGrp.id}'); return false;">${deviceGrp.name}</a></span>
												<ul>
													<g:each in="${deviceGrp.devices}" var="device">
														<% modemGroupCount++; %>
													<li id="deviceGroupList_${modemGroupCount}">
														<span id="${device.id}"><a href="#" onclick="showDevice('${device.id}' , 'STATIC');  highlightTreeElement('deviceList_', '0', '${deviceInstanceModemTotal}'); highlightTreeElement('deviceGroupList_', '${modemGroupCount}', '${totalDevices}'); return false;">${device.stbName}</a></span>
													</li>
													</g:each>
												</ul>											
											</li>
											</g:each>
										</ul>
										</li>
										</div>
									</ul>
								</li>
							</ul>
						</div>
					</td>	
					
					<td>
						<div class="contextMenu" id="up_load" align="center"
							style="width: 950px; height: 900px; display: none">
							<br> <br> <br> <br>
							<g:form method="POST" controller="deviceGroup"
								action="uploadRDKVDevice" enctype="multipart/form-data">
								<label> <b><g:message code="deviceGroup.name.label"
											default="Select the device XML file" /></b>
								</label>
								&emsp;
								<input class="uploadFile" type="file" name="file" />
								&emsp;&emsp;
								<g:actionSubmit class="buttons" style="width : 100px; "
									action="uploadRDKVDevice" value="Upload" />

							</g:form>
						</div>
					</td>	
					<td>
						<div class="contextMenu" id="up_load_rdkb" align="center"
							style="width: 950px; height: 900px; display: none">
							<br> <br> <br> <br>
							<g:form method="POST" controller="deviceGroup"
								action="uploadRDKBDevice" enctype="multipart/form-data">
								<label> <b><g:message code="deviceGroup.name.label"
											default="Select the device XML file" /></b>
								</label>
								&emsp;
								<input class="uploadFile" type="file" name="file" />
								&emsp;&emsp;
								<g:actionSubmit class="buttons" style="width : 100px; "
									action="uploadRDKBDevice" value="Upload" />

							</g:form>
						</div>
					</td>				
			
					<td rowspan="2" style="width: 80%; height: 610px">
						<div id="responseDiv" style="width: 97%; overflow-x: auto;overflow-y:hidden">
						<div style="width: 97%; max-height: 600px" id="list-deviceDetails" class="content scaffold-list">
									<% int deviceCount1 = 0;
									   int deviceCount2 = 0;		
									   int totalDevices1 = deviceInstanceSTBTotal * deviceGrpInstanceSTBTotal;
									   int totalDevices2 = deviceInstanceModemTotal * deviceGrpInstanceModemTotal;
									   int deviceGroupCount1 = 0;
									 %>
						</br></br>
						<%--<div style="padding-bottom: 2%;">
								<h3 style="color: #A24C15;"><center><strong>RDK-V</strong></center></h3>
							</div>
						--%><div>
							<g:link action="downloadAllDevices"  params="[category:'RDKV']" target="_blank"> Download All the RDK-V Device Details </g:link>
							<br/>
							<table id="devicetable" class="display">
								<thead>
									<tr>
										<th colspan="4" align="center" style="width: 50%;"><h1> RDK-V Device
												Summary</h1></th>
									</tr>
									<tr id="deleteVRow" >
										<td colspan="4">
										 <span class="buttons" style="float:right;padding:0px">
										     <input type="submit" class="delete" value="Delete" onClick="deleteDevices('V')"/> 
										 </span> 
										</td>
									</tr>
									<tr align="left">
									    <th width="5">Select</th>
										<th width="45%;">Device Name</th>
										<th width="25%">Device IP</th>
										<th width="25%">Box Type</th>
									</tr>
								</thead>
								<tbody>
									<g:each in="${deviceInstanceListSTB}" var="parentDevice">
								<g:if test="${parentDevice.isChild == 0}">
										<tr>
										    <td><input type="checkbox" name="vDevice"  value="${parentDevice.id}" onClick="onDeviceVselectionChange('${parentDevice.id}')"/> </td> 
											<td>
												<a href="#" onclick="showDevice('${parentDevice.id}');  highlightTreeElement('deviceList_', '${deviceCount1}', '${deviceInstanceTotal}'); highlightTreeElement('deviceGroupList_', '0', '${totalDevices1}'); return false;">${parentDevice.stbName}</a>
											</td>
											<td>
												${parentDevice.stbIp}
											</td>
											<td>
												${parentDevice.boxType}
											</td>
										</tr>
										
										<g:each in="${ parentDevice.childDevices}" var="childDevice">
										
										
										<tr>
										<td><input type="checkbox" name="vDevice"  value="${childDevice.id}" onClick="onDeviceVselectionChange('${childDevice.id}')"/> </td>
											<td>
												<a href="#" onclick="showDevice('${childDevice.id}');  highlightTreeElement('deviceList_', '${deviceCount1}', '${deviceInstanceTotal}'); highlightTreeElement('deviceGroupList_', '0', '${totalDevices1}'); return false;">${childDevice.stbName}</a>
											</td>
											<td>
												${parentDevice.stbIp} (${childDevice.macId})
											</td>
											<td>
												${childDevice.boxType} 
											</td>
										</tr>
										</g:each>
									</g:if>
									</g:each>
								</tbody>
							</table>
							
							<br/>
							<br/>
							</div>
							<%--<div style="padding-bottom: 2%; padding-top:2%;">
								<h3 style="color: #A24C15;"><center><strong>RDK-B</strong></center></h3>
							</div>
							
							--%><div>
							<g:link action="downloadAllDevices"  params="[category:'RDKB']" target="_blank"> Download All the RDK-B Device Details </g:link>
							<br/>
							<table id="devicetable2" class="display">
								<thead>
									<tr>
										<th colspan="4" align="center" style="width: 50%;"><h1> RDK-B Device
												Summary</h1></th>
									</tr>
									<tr id="deleteBRow" >
										<td colspan="4">
										<span class="buttons" style="float:right;padding:0px">
										     <input type="submit" class="delete" value="Delete" onClick="deleteDevices('B')"/> 
										 </span> 
										</td>
									</tr>
									
									<tr align="left">
									    <th width="3%">Select</th>
										<th width="47%">Device Name</th>
										<th width="25%">Device IP</th>
										<th width="25%">Box Type</th>
									</tr>
								</thead>
								<tbody>
									<g:each in="${deviceInstanceListModem}" var="parentDevice">
								<g:if test="${parentDevice.isChild == 0}">
										<tr>
										    <td ><input type="checkbox" name="bDevice" value="${parentDevice.id}"/> </td> 
											<td>
												<a href="#" onclick="showDevice('${parentDevice.id}');  highlightTreeElement('deviceList_', '${deviceCount1}', '${deviceInstanceTotal}'); highlightTreeElement('deviceGroupList_', '0', '${totalDevices2}'); return false;">${parentDevice.stbName}</a>
											</td>
											<td>
												${parentDevice.stbIp}
											</td>
											<td>
												${parentDevice.boxType}
											</td>
										</tr>
										
										<g:each in="${ parentDevice.childDevices}" var="childDevice">
										<tr>
											<td ><input type="checkbox" name="bDevice" value="${childDevice.id}"/> </td> 
											<td>
												<a href="#" onclick="showDevice('${childDevice.id}');  highlightTreeElement('deviceList_', '${deviceCount1}', '${deviceInstanceTotal}'); highlightTreeElement('deviceGroupList_', '0', '${totalDevices2}'); return false;">${childDevice.stbName}</a>
											</td>
											<td>
												${parentDevice.stbIp} (${childDevice.macId})
											</td>
											<td>
												${childDevice.boxType} 
											</td>
										</tr>
										</g:each>
									</g:if>
									</g:each>
								</tbody>
							</table>
							<br/>
							<br/>
							</div>
							
							
						</div>
						</div>
					</td>
				</tr>
			</table>
			</span>
			<div class="contextMenu" id="root_menu">
				<ul>
	          		<li id="add_devicegrp"><img src="../images/add_new.png" height="15px" width="15px"/>Add New RDK-V DeviceGroup</li>
	          		<li id="add_devicegrpB"><img src="../images/add_new.png" height="15px" width="15px"/>Add New RDK-B DeviceGroup</li>
	        	</ul>
	        </div>
			<div class="contextMenu" id="childs_menu">
				<ul>
					<li id="edit_devicegrp"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_devicegrp"><img src="../images/delete.png" />Delete</li>
	          	
	        	</ul>
	      </div>	      
	     
	       <div class="contextMenu" id="root_menu_device">
				<ul>
	          		<li id="add_device"><img src="../images/add_new.png" height="15px" width="15px"/>Add New RDK-V Device</li>
	          		<li id="add_deviceB"><img src="../images/add_new.png" height="15px" width="15px"/>Add New RDK-B Device</li>
	          		<li id="upload_device"><img src="../images/reorder_up.png" height="15px" width="15px" /> Upload RDK-V Device</li>
	          		<li id="upload_device_RDKB"><img src="../images/reorder_up.png" height="15px" width="15px" /> Upload RDK-B Device</li>
	        	</ul>
	        </div>
			<div class="contextMenu" id="childs_menu_device">
				<ul>
					<li id="edit_device"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_device"><img src="../images/delete.png" />Delete</li>
	          		
	        	</ul>
	      </div>
	      
		</div>
		
		<g:hiddenField name="currentDeviceId" id="currentDeviceId" value="${deviceId}"/>
		<g:hiddenField name="currentDeviceGroupId" id="currentDeviceGroupId" value="${deviceGroupId}"/>
		
		<g:hiddenField name="deviceGroupCount" id="deviceGroupCount" value="${deviceInstanceTotal}"/>
		<g:hiddenField name="isDeviceExist" id="isDeviceExist" value=""/>
		

</body>
</html>


