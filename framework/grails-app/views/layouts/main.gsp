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
<%@ page import="org.apache.shiro.SecurityUtils"%>
<%@ page import="com.comcast.rdk.User" %>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<title>RDK Test Suite</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<%--	<link rel="shortcut icon" href="${resource(dir: 'images', file: 'favicon.ico')}" type="image/x-icon">--%>
<link rel="apple-touch-icon"
	href="${resource(dir: 'images', file: 'apple-touch-icon.png')}">
<link rel="apple-touch-icon" sizes="114x114"
	href="${resource(dir: 'images', file: 'apple-touch-icon-retina.png')}">
<link rel="stylesheet" href="${resource(dir: 'css', file: 'main.css')}"
	type="text/css">
<link rel="stylesheet"
	href="${resource(dir: 'css', file: 'mobile.css')}" type="text/css">
<link rel="stylesheet" href="${resource(dir:'css',file:'basic.css')}"
	type="text/css" />

<g:javascript library="jquery-1.6.1.min" />
<g:javascript library="jquery.simplemodal" />

<g:layoutHead />
<%--	<r:layoutResources />--%>

<script type="text/javascript">

function showStreamDetails12(){			
	$("#streamDetailsPopup12").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 500,
	            height: 250
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });		
}	

</script>

</head>
<body>
<%  
    def userInstance
    if(SecurityUtils.subject.principal) {
       userInstance = User.findByUsername(SecurityUtils.subject.principal)
    }
%>	
	<div id="grailsLogo" role="banner">
		<img src="${resource(dir: 'images', file: 'rdk_logo.png')}"
			alt="Grails" />
	</div>
	<div
		style="width: 100%; min-width: 100%; text-align: right; border-bottom: 3px solid #CCCCCC; border-bottom-color: #0CB2DD">
		<g:if test="${SecurityUtils.subject.principal}">
			<span style="color : #A24C15;" > Welcome, ${userInstance.name}</span> &emsp;
			 <a href="" onclick="showStreamDetails12();return false;">Change Password</a>&emsp;
			 <g:link controller="auth" action="signOut" class="customizedLink" style="padding-right:10px;">SignOut</g:link>
		</g:if>		
	</div>
	<hr>
	<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN') || SecurityUtils.getSubject().hasRole('TESTER')  }" >      			      	
	<table id="maintable">
		<tr>
			<td nowrap="nowrap"
				style="position: absolute; min-width: 500px; height: 20px; width: 100%; background-color: #E9F1F1; border-bottom-color: #0CB2DD" >
				<div id="header" align="left">
					<ul>
						<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
						<li><g:link controller="primitiveTest" action="create">
								<span><p id="primid">Primitive Test</p></span>
							</g:link></li>
						</g:if>
						<li><g:link controller="scriptGroup" action="list">
								<span><p id="scriptid">Script</p></span>
							</g:link></li>
						<li><g:link controller="deviceGroup" action="list">
								<span><p id="deviceid">Devices</p></span>
							</g:link></li>
						<li><g:link controller="execution" action="create">
								<span><p id="execid">Execution</p></span>
							</g:link></li>
						<li><g:link controller="trends" action="chart">
								<span><p id="trendid">Result Analysis</p></span>
							</g:link></li>
						<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
						<li><g:link controller="module" action="configuration">
									<span><p id="admid">Configure</p></span>
							</g:link>
						</li>
						</g:if>
					</ul>
				</div>
			</td>
		</tr>
	</table>
	</g:if>
	<br>
		<div id="streamDetailsPopup12" style="display: none; overflow: auto; ">
		
		<g:form controller="user">
			<table>
				<tr>
					<td colspan="2" align="center"><h1>Change Password</h1></td>
				</tr>
				<tr>
					<td>Username :</td>
					<td><g:textField name="username" required=""
							value="${SecurityUtils.subject.principal}" /><g:passwordField name="toEscapeFrmBrowser"  value="" style="display:none;" /></td>
				</tr>
				<tr>
					<td>Old Password :</td>
					<td><g:passwordField name="oldPassword" required="" value="" /></td>
				</tr>
				<tr>
					<td>New Password :</td>
					<td><g:passwordField name="newPassword" required="" value="" /></td>
				</tr>
				<tr>
					<td>Confirm Password:</td>
					<td><g:passwordField name="confirmPassword" required=""
							value="" /></td>
				</tr>
				<tr>
					<td></td>
					<td align="left"><g:submitToRemote class="save"
							action="changePassword" update="resultDiv" value="Reset Password"
							controller="user" /></td>
				</tr>				
			</table>			
		</g:form>
		<span id="resultDiv" style="border: 1px; width:20px;"></span>
	</div>		
	<g:layoutBody />
	<br>
	
	<div class="footer" role="contentinfo"> 
	<div>
		<label> <b> RDK Test Development Kit TM-M103 </b></label>
	</div>
	</div>
	<div id="spinner" class="spinner" style="display: none;">
		<g:message code="spinner.alt" default="Loading&hellip;" />
	</div>
	<%--		<g:javascript library="application"/>--%>
	<%--		<r:layoutResources />--%>
	
</body>
</html>
