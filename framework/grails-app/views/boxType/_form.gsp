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

<%@ page import="com.comcast.rdk.BoxType" %>

<div class="fieldcontain ${hasErrors(bean: boxTypeInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="boxType.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${boxTypeInstance?.name}"/>
</div>

<div class="fieldcontain ${hasErrors(bean: boxTypeInstance, field: 'type', 'error')} required">
	<label for="type">
		<g:message code="boxType.type.label" default="Type" />
		<span class="required-indicator">*</span>
	</label>
	<g:select id="typeId" name="type" from="['Client','Stand-alone-Client','Gateway']" style="width : 150px;"/>
	<%--<g:textField name="type" required="" value="${boxTypeInstance?.type}"/>--%>
</div>
<g:hiddenField name="category" value="${category }"/>
