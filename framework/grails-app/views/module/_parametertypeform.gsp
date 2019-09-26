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
<%@ page import="com.comcast.rdk.ParameterType" %>
<%@ page import="com.comcast.rdk.Module" %>
<%@ page import="com.comcast.rdk.User" %>
<%@ page import="com.comcast.rdk.Groups" %>
<%@ page import="org.apache.shiro.SecurityUtils" %>

<script type="text/javascript">	
	function onModuleChange() {
	 	var module_id = $("#moduleId").val();
		if(module_id != '') {
			$.get('getFunctions', {moduleId: module_id}, function(data) {
				var select = '<select style="width: 200px" id="function" name="function.id" ><option value="">Please Select</option>';						
				for(var index = 0; index < data.length; index ++ ) {
					select += '<option value="' + data[index].id + '">' + data[index].name + '</option>';
				}						
				select += '</select>';						
				$("#respDiv").html(''); 
				$("#respDiv").html(select); 
			});
		}				
	}		 	
</script>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="parameterType.name.label" default="Parameter Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${parameterTypeInstance?.name}"/>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'parameterTypeEnum', 'error')} required">
	<label for="parameterTypeEnum">
		<g:message code="parameterType.parameterTypeEnum.label" default="Parameter Type Enum" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="parameterTypeEnum" from="${com.comcast.rdk.ParameterTypeEnum?.values()}" keys="${com.comcast.rdk.ParameterTypeEnum.values()*.name()}" required="" value="${parameterTypeInstance?.parameterTypeEnum?.name()}"/>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'rangeVal', 'error')} required">
	<label for="rangeVal">
		<g:message code="parameterType.rangeVal.label" default="Range Val" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="rangeVal" required="" value="${parameterTypeInstance?.rangeVal}"/>
</div>
<g:if test="${category == "RDKB"  }">
<div class="fieldcontain required">
	<label for="defaultVal">
		<g:message code="parameterType.defaultVal.label" default="Default Val" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="defaultVal" required="" />
</div>
</g:if>
<%
	def user = User.findByUsername(SecurityUtils.subject.principal)
	def group = Groups.findById(user.groupName?.id)
%>
<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'rangeVal', 'error')} required">
	<label for="function">
		<g:message code="parameterType.module.label" default="Module" />
		<span class="required-indicator">*</span>
	</label>
	<g:select noSelection="['' : 'Please Select']"  onChange="onModuleChange();" id="moduleId" name="module" from="${modules}" optionKey="id" required="" value="${module?.id}" class="many-to-one"/>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'function', 'error')} required">
	<label for="function">
		<g:message code="parameterType.function.label" default="Function" />
		<span class="required-indicator">*</span>
	</label>
	<span id="respDiv">
	<g:select id="function" name="function.id"  optionKey="id" from="" style="width: 200px"
	noSelection="['' : 'Please Select']" required="" class="many-to-one"/>
	</span>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'function', 'error')} required">
	<label for="function">	
	</label>
	<span class="buttons">
		<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
	</span>
</div>
<g:hiddenField name="category" id="category" value="${category}"/>
