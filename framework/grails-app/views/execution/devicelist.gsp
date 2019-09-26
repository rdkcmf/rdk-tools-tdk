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
<%@ page import="org.codehaus.groovy.grails.validation.routines.InetAddressValidator"%>

<% int deviceStatusCount = 0; %>

<g:each in="${deviceList}" var="device">
	<% deviceStatusCount++; %>
	<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
	
	
<div id="tooltip_${name}" title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}   &#013;BoxType : ${device.boxType}   &#013;Status : ${device.deviceStatus}">
	<li id="deviceExecutionList_${deviceStatusCount}">
	<g:if test="${device.deviceStatus.toString()=="NOT_FOUND" }">
		<span class="filedevicenotfound" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				    onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
			<span class="filedevicefree" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
			<span class="filedevicebusy" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
			<span class="filedevicehang" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if>		
		 <g:if test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
			<span class="filedevicetdkdisabled" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if>		
		<g:if test="${device.deviceStatus.toString()=="ALLOCATED" }">
			<span class="filedevicebusy" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if>
	</li>
	</div>
</g:each>
