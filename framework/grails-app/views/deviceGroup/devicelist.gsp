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
<g:each in="${deviceInstanceList}" var="device">
	<li>
	<g:if test="${device.deviceStatus.toString()=="FREE" }">
		<span class="filedevicefree" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:if>
	<g:elseif test="${device.deviceStatus.toString()=="NOT_FOUND" }">
		<span class="filedevicenotfound" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:elseif>
	<g:elseif test="${device.deviceStatus.toString()=="BUSY"}">
		<span class="filedevicebusy" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:elseif>
	<g:elseif test="${device.deviceStatus.toString()=="HANG"}">
		<span class="filedevicehang" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:elseif>
	</li>
</g:each>
