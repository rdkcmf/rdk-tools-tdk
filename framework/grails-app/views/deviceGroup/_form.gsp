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
<%@ page import="com.comcast.rdk.Device" %>


<div class="fieldcontain ${hasErrors(bean: deviceGroupsInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="deviceGroups.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${deviceGroupsInstance?.name}" class="textwidth"/>
</div>

<div class="fieldcontain ${hasErrors(bean: deviceGroupsInstance, field: 'devices', 'error')} ">
	<label for="devices">
		<g:message code="deviceGroups.devices.label" default="Devices" />		
	</label>
	<%--<g:select id="devices" style="width: 210px;height: 410px;" name="devices" multiple="true" from="${com.comcast.rdk.Device.list().stbName}" value="" />
	--%>
	<g:hiddenField name="category" value="${category}"/>
	<select id="devices" name="devices" class="selectCombo" multiple="true" style="width: 210px;height: 410px;" >
			<g:each in="${devices}"
				var="device">
				<option value="${device.id}">
					${device.stbName}
				</option>
			</g:each>
	</select>	
</div>

