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
<%@page import="com.comcast.rdk.Category"%>
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.DeviceTemplate"%>

<div id="uploadBinarypopup"
	style="display: none; overflow: auto; width: 98%; height: 98%;">
	<div id="uploadBinaryDiv" align="center"
		style="border: solid; border-width: 1px; border-color: #CCCCCC; border-spacing: 5px 5px;"
		b>

		<div
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'System IP', 'error')} required">
			<label for="Source IP"> <g:message
					code="device.System IP.label" default="Source IP" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textField name="systemIP" id="systemIP" autocomplete="on"
				onchange="ValidateIPaddress1();" />
		</div>
		<div
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'System Path', 'error')} required">
			<label for="Source Path"> <g:message code="device.Path.label"
					default="Source Path" /> <span class="required-indicator">*</span>
			</label>
			<g:textField name="systemPath" id="systemPath" autocomplete="on" />
		</div>
		<div
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'Username', 'error')} required">
			<label for="Source Username"> <g:message
					code="device.Source Username.label" default="Source Username" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textField name="usernamedata" id="usernamedata" autocomplete="on" />
		</div>
		<div
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'Password', 'error')} required">
			<label for="Source Password"> <g:message
					code="device.Source Password.label" default="Source Password" /> <span
				class="required-indicator">*</span>
			</label>
			<g:passwordField name="password" id="password" autocomplete="on" />
		</div>

		<div
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'System IP', 'error')} required">
			<label for="Destination IP"> <g:message
					code="device.Destination IP.label" default="Destination IP" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textField name="destinationIP" id="destinationIP"
				value="${deviceInstance?.stbIp}" />
		</div>

		<div
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'Boxpath', 'error')} required">
			<label for="Destinaton Path"> <g:message
					code="device.Boxpath.label" default="Destinaton Path" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textField name="boxpath" id="boxpath" autocomplete="on" />
		</div>

		<div align="center"
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'Buttons', 'error')} required">

			<span class="buttons" id="uploadBtnSpan"><input type="button"
				id="upload" value="Upload"
				onclick="uploadBinary(document.getElementById('boxType').value, document.getElementById('stbIp').value, document.getElementById('usernamedata').value, document.getElementById('password').value, document.getElementById('systemPath').value,  document.getElementById('systemIP').value, document.getElementById('boxpath').value, ${id});">
			</span>
		</div>

		<div id="waitingSymbol" style="display: none;">
			Please wait.....<img id="s"
				src="${resource(dir:'images',file:'spinner.gif')}" />
		</div>
		<div id="seperator1" style="height: 10px; width: 130px;"></div>
	</div>

	<div id="seperator2" style="height: 20px; width: 130px;"></div>

	<div id="uploadResultDiv"
		style="border-color: #FFAAAA; border-style: solid; border-width: 1px; width: 100%; height: 215px; overflow: auto; display: none;">
	</div>

</div>

<div id="uploadButton" align="center"
	class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'Upload Buttons', 'error')} required">
	<table>
		<tr>
			<td align="right"><g:if
					test="${uploadBinaryStatus.toString() == "SUCCESS" }">

					<span class="buttons" id="uploadBinarySuccess"> <a
						class="success" id="uploadBinaryLink_" +${id }
						style="cursor: pointer; font: bold; font-size: 12px;"
						onclick="hideLink();">Upload Binary</a>
					</span>
				</g:if> <g:if test="${uploadBinaryStatus.toString() == "FAILURE" }">

					<span class="buttons" id="uploadBinaryFailure"> <a
						class="failure" id="uploadBinaryLink_" +${id }
						style="cursor: pointer; font: bold; font-size: 12px;"
						onclick="hideLink();">Upload Binary</a>
					</span>
				</g:if> <g:if test="${uploadBinaryStatus.toString() == "UNKNOWN" }">

					<span class="buttons" id="uploadBinaryUnknown"> <a
						class="unknown" id="uploadBinaryLink_" +${id }
						style="cursor: pointer; font: bold; font-size: 12px;"
						onclick="hideLink();">Upload Binary</a>
					</span>
				</g:if> <g:if test="${uploadBinaryStatus.toString() == "INPROGRESS" }">

					<div id="uploadBinaryInprogress" align="right">
						Uploading.....<img id="spinner1"
							src="${resource(dir:'images',file:'spinner.gif')}" />
					</div>
				</g:if></td>
		<tr>
	</table>
</div>

<div id="waitingSymbol2" style="display: none;" align="right">
	Uploading.....<img id="spinner2"
		src="${resource(dir:'images',file:'spinner.gif')}" />
</div>


<g:if test="${deviceInstance.isChild  == 1}">
	<div
		class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'stbIp', 'error')} required">
		<label for="macId"> <g:message code="device.macId.label"
				default="Mac Id" /> <span class="required-indicator">*</span>
		</label>
		<g:textField id="macId" name="macId" required=""
			value="${deviceInstance?.macId}" class="textwidth" />
	</div>
</g:if>


<div
	class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'stbName', 'error')} required">
	<label for="stbName"> <g:if test="${category != ''}">
			<g:if test="${category=='stb' }">
				<g:message code="device.stbName.label" default="Stb Name" />
			</g:if>
			<g:if test="${category=='modem' }">
				<g:message code="device.stbName.label" default="Gateway Name" />
			</g:if>
		</g:if> <g:if test="${deviceInstance?.category}">
			<g:if test="${deviceInstance.category == Category.RDKV}">
				<g:message code="device.stbName.label" default="Stb Name" />
			</g:if>
			<g:if test="${deviceInstance.category == Category.RDKC}">
				<g:message code="device.stbName.label" default="Camera Name" />
			</g:if>
			<g:if test="${deviceInstance.category == Category.RDKB}">
				<g:message code="device.stbName.label" default="Gateway Name" />
			</g:if>
		</g:if> <span class="required-indicator">*</span>
	</label>
	<g:textField name="stbName" id="stbName" required=""
		value="${deviceInstance?.stbName}" class="textwidth" />
</div>

<g:if test="${deviceInstance.isChild  == 0}">

	<div
		class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'stbIp', 'error')} required">
		<label for="stbIp"> <g:if test="${category != ''}">
				<g:if test="${category=='stb' }">
					<g:message code="device.stbIp.label" default="Stb Ip" />
				</g:if>
				<g:if test="${category=='modem' }">
					<g:message code="device.gateWayIp.label" default="Gateway Ip" />
				</g:if>
			</g:if> <g:if test="${deviceInstance?.category}">
				<g:if test="${deviceInstance.category == Category.RDKV || deviceInstance.category == Category.RDKC}">
					<g:message code="device.stbName.label" default="Stb Ip" />
				</g:if>
				<g:if test="${deviceInstance.category == Category.RDKB}">
					<g:message code="device.stbName.label" default="Gateway Ip" />
				</g:if>
			</g:if> <span class="required-indicator">*</span>
		</label>

		<g:textField id="stbIp" name="stbIp" required=""
			value="${deviceInstance?.stbIp}" class="textwidth" />
	</div>
	<g:if test="${deviceInstance.isChild  == 0}">
		<div
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'serialNo', 'error')} ">
			<label for="serialNo"> <g:message
					code="device.serialNo.label" default="Mac Addr" />
			</label>
			<g:textField name="serialNo" id="serialNo"
				value="${deviceInstance?.serialNo}" class="textwidth" />
		</div>
	</g:if>
	<div
		class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'boxType', 'error')} required">
		<label for="boxType"> <g:message code="device.boxType.label"
				default="Box Type" /> <span class="required-indicator">*</span>
		</label>
		<g:select onchange="javascript:showFields();" id="boxType"
			name="boxType.id" noSelection="['' : 'Please Select']"
			from="${com.comcast.rdk.BoxType.findAllByCategory(category)}"
			optionKey="id" required="" value="${deviceInstance?.boxType?.id}"
			class="many-to-one selectCombo" />
	</div>
	<div class="fieldcontain required" style="display: none;" id="deviceTemplateDropdown">
	<label for="deviceTemplate"> <g:message code="device.boxType.label"
				default="Device Template" /> <span class="required-indicator">*</span>
	</label>
	<g:select onchange="loadDeviceTemplate(this.value,${streamingDetailsInstanceTotal},${radioStreamingDetailsInstanceTotal});" id="deviceTemplate" name="deviceTemplate.id" noSelection="['' : 'Please Select']" from="${DeviceTemplate.list().name}" keys="${DeviceTemplate.list().id}" value="${params?.deviceTemplate}" />
	</div>	
	<div
		class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'boxManufacturer', 'error')} required">
		<label for="boxManufacturer"> <g:message
				code="device.boxManufacturer.label" default="Box Manufacturer" /> <span
			class="required-indicator">*</span>
		</label>
		<g:select id="boxManufacturer" name="boxManufacturer.id"
			noSelection="['' : 'Please Select']"
			from="${com.comcast.rdk.BoxManufacturer.findAllByCategory(category)}"
			optionKey="id" required=""
			value="${deviceInstance?.boxManufacturer?.id}"
			class="many-to-one selectCombo" />
	</div>

	<div
		class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'soCVendor', 'error')} required">
		<label for="boxModel"> <g:message code="device.boxModel.label"
				default="SoC Vendor" /> <span class="required-indicator">*</span>
		</label>
		<g:select id="soCVendor" name="soCVendor.id"
			noSelection="['' : 'Please Select']"
			from="${com.comcast.rdk.SoCVendor.findAllByCategory(category)}"
			optionKey="id" required="" value="${deviceInstance?.soCVendor?.id}"
			class="many-to-one selectCombo" />
	</div>
</g:if>
<g:if
	test="${ (deviceInstance?.boxType?.type?.toLowerCase() != 'gateway')  && (deviceInstance?.category?.toString().equals("RDKV"))}">
	<g:if test="${deviceInstance.isChild  == 0}">
		<div id="gatewayId"
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'gatewayIp', 'error')}">
			<label for="gatewayIp"> <g:message
					code="device.gatewayIp.label" default="Gateway" /> <span
				class="required-indicator">*</span>
			</label>
			<g:select id="gatewayIp" name="gatewayIp"
				noSelection="['' : 'Please Select']" from="${gateways?.stbName}"
				value="${deviceInstance?.gatewayIp}" class="many-to-one selectCombo" />
		</div>
		<g:if test="${deviceInstance.category == Category.RDKV }">
			<div style="display: none;" id="recorderId"
				class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'recorderId', 'error')}">
				<label for="recorderId"> <g:message
						code="device.recorderId.label" default="RecorderId" /> <span
					class="required-indicator">*</span>
				</label>
				<g:textField name="recorderId" value="${deviceInstance?.recorderId}"
					class="textwidth" />
			</div>
		</g:if>
	</g:if>
</g:if>
<g:if test="${ deviceInstance?.category != com.comcast.rdk.Category.RDKB && deviceInstance?.category != com.comcast.rdk.Category.RDKC}">
	<div id="isThunderEnabled"
		class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'isThunderEnabled', 'error')}">
		<label for="isThunderEnabled"> <g:message
				code="device.isThunderEnabled.label" default="Is Thunder Enabled" />
		</label>
		<g:checkBox id="isThunderEnabled" name="thunderEnabled"
			checked="${deviceInstance?.isThunderEnabled == 1}" />
	</div>
</g:if>
<div style="display: none;" id="gatewayIdedit"
	class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'gatewayIp', 'error')}">
	<label for="gatewayIp"> <g:message
			code="device.gatewayIp.label" default="Gateway" /> <span
		class="required-indicator">*</span>
	</label>
	<g:select id="gatewayIpedit" name="gatewayIpedit"
		noSelection="['' : 'Please Select']" from="${gateways?.stbName}"
		value="${deviceInstance?.gatewayIp}" class="many-to-one selectCombo" />
</div>
<g:if
	test="${ deviceInstance?.category != com.comcast.rdk.Category.RDKB }">
	<g:if
		test="${ (deviceInstance?.boxType?.type?.toLowerCase() == 'gateway' || deviceInstance?.boxType?.type?.toLowerCase() == 'stand-alone-client')}">
		<div id="recorderIdedit"
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'recorderId', 'error')}">
			<label for="recorderId"> <g:message
					code="device.recorderId.label" default="RecorderId" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textField name="recorderIdedit"
				value="${deviceInstance?.recorderId}" class="textwidth" />
		</div>
	</g:if>
	<g:else>
		<div style="display: none;" id="recorderIdedit"
			class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'recorderId', 'error')}">

			<label for="recorderId"> <g:message
					code="device.recorderId.label" default="RecorderId" /> <span
				class="required-indicator">*</span>
			</label>
			<g:textField name="recorderIdedit"
				value="${deviceInstance?.recorderId}" class="textwidth" />
		</div>
	</g:else>
</g:if>
<%--<div class="fieldcontain ${hasErrors(bean: deviceInstance, field: 'category', 'error')} required">
		<label for="category">
			<g:message code="device.category.label" default="Category" />
			<span class="required-indicator">*</span>
		</label>
		<g:select id="category" name="category" noSelection="['' : 'Please Select']" from="${com.comcast.rdk.Category.values()}" value="${deviceInstance?.category}" required=""  class="many-to-one selectCombo"/>
	</div>

--%>
<g:hiddenField name="category" value="${category}" />
<g:hiddenField id="editFlag" name="editFlag" value="${editPage}" />
