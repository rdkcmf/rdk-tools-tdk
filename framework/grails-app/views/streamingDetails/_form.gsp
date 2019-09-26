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
<%@ page import="com.comcast.rdk.StreamingDetails" %>
<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'streamId', 'error')} required">
	<label for="streamId">
		<g:message code="streamingDetails.streamId.label" default="Stream Id" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="streamId" required="" value="${streamingDetailsInstance?.streamId}" class="textwidth"/>
</div>

<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'channelType', 'error')} required">
	<label for="channelType">
		<g:message code="streamingDetails.channelType.label" default="Channel Type" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="channelType" from="${com.comcast.rdk.ChannelType?.values()}" keys="${com.comcast.rdk.ChannelType.values()*.name()}" required="" value="${streamingDetailsInstance?.channelType?.name()}" class="selectCombo" />
</div>

<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'audioFormat', 'error')} required">
	<label for="audioFormat">
		<g:message code="streamingDetails.audioFormat.label" default="Audio Format" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="audioFormat" from="${com.comcast.rdk.AudioFormat?.values()}" keys="${com.comcast.rdk.AudioFormat.values()*.name()}" required="" value="${streamingDetailsInstance?.audioFormat?.name()}" class="selectCombo" />
</div>

<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'videoFormat', 'error')} required">
	<label for="videoFormat">
		<g:message code="streamingDetails.videoFormat.label" default="Video Format" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="videoFormat" from="${com.comcast.rdk.VideoFormat?.values()}" keys="${com.comcast.rdk.VideoFormat.values()*.name()}" required="" value="${streamingDetailsInstance?.videoFormat?.name()}" class="selectCombo" />
</div>
