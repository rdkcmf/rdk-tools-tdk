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
<%@ page
	import="org.apache.shiro.SecurityUtils;com.comcast.rdk.Category"%>
<!DOCTYPE html>
<html>
<head>
<meta name="layout" content="main" />
<title>RDK Test Suite</title>
<style type="text/css" media="screen"></style>
<%--<g:javascript library="jquery-1.6.1.min" />
<g:javascript library="jquery.simplemodal" />
<g:javascript library="config_resolver" />
--%><script type="text/javascript">
window.onload = function(){
	$("#rdkB").hide();
	$("#rdkC").hide();
}

function display(val) {
	if (val.trim() === 'RDKV') {
		$("#rdkB").hide();
		$("#rdkC").hide();
		$("#rdkV").show();
	} else if (val.trim() === 'RDKB') {
		$("#rdkV").hide();
		$("#rdkC").hide();
		$("#rdkB").show();
	}else if (val.trim() === 'RDKC') {
		$("#rdkV").hide();
		$("#rdkB").hide();
		$("#rdkC").show();
	} else {}
}

</script>

</head>
<body>
	<div style="padding: 20px;margin-left:20%;">
		<b style="color: #A24C15;">Choose the configuration Category</b>&nbsp;&nbsp;&nbsp;
		<input type="radio" onclick="display('RDKV')" name="chooseCat" checked="checked" >RDK-V</input> &nbsp;&nbsp;
		<input type="radio" onclick="display('RDKB')" name="chooseCat">RDK-B</input>
		<input type="radio" onclick="display('RDKC')" name="chooseCat">RDK-C</input>
	</div>
	<br>
	<div id="rdkV">
		<div style="float: left; padding-left: 10%; padding-top: 5%;">
			<h2 style="color: #A24C15;">
				<center>RDK-V</center>
			</h2>
		</div>
		<div style="width: 40%; margin: 0 auto; align: center;">
			<!-- RDK_V -->
			<table>
				<tr>
					<td><g:link controller="module" action="list"
							params="[category: com.comcast.rdk.Category.RDKV]">
							<span>Modules</span>
						</g:link></td>
					<td>Configure Information about Component Interface Modules</td>
				</tr>
				<tr>
					<td><g:link controller="module" action="crashlog"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>Link Crash Files</span>
						</g:link></td>
					<td>Link Crash Files to Modules</td>
				</tr>

				<tr>
					<td><g:link controller="module" action="logFileNames"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>Link logs files</span>
						</g:link></td>
					<td>Link Configure STB logs to Module</td>
				</tr>
				<tr>
					<td><g:link controller="streamingDetails" action="list"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>Streaming Details</span>
						</g:link></td>
					<td>Option to add streaming details</td>
				</tr>
				<tr>
					<td><g:link controller="boxManufacturer" action="index"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>Box Manufacturers</span>
						</g:link></td>
					<td>Option to add Box Manufacturers</td>
				</tr>
				<tr>
					<td><g:link controller="boxType" action="index"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>Box Type</span>
						</g:link></td>
					<td>Option to add Box Type</td>
				</tr>
				<tr>
					<td><g:link controller="RDKVersions" action="index"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>RDK Versions</span>
						</g:link></td>
					<td>Option to add RDK Versions</td>
				</tr>
				<tr>
					<td><g:link controller="soCVendor" action="index"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>SoC Vendors</span>
						</g:link></td>
					<td>Option to add SoC Vendors</td>
				</tr>
				<tr>
						<td><g:link controller="ScriptTag" action="index"
								params="[category:com.comcast.rdk.Category.RDKV ]">
								<span>Script Tags</span>
							</g:link></td>
						<td>Option to add Script Tags</td>
					</tr>
					
				<tr>
					<td>
					
						<g:link controller="TestProfile" action="index"
								params="[category:com.comcast.rdk.Category.RDKV ]">
								<span>Test Profile</span>
							</g:link></td>
						<td>Option to add Test profile</td>
						
				</tr>
				<tr>
					<td><g:link controller="deviceTemplate" action="create"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>Templates</span>
						</g:link></td>
					<td>Option to configure device templates</td>
				</tr>
				<tr>
					<td><g:link controller="module" action="stormConfiguration"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>Storm JSON RPC Server</span>
						</g:link></td>
					<td>Option to configure Storm JSON RPC Server</td>
				</tr>
				<tr>
					<td><g:link controller="scriptGroup" action="listCertificationSuiteConfigFiles"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>RDK Certification</span>
						</g:link></td>
					<td>Option to configure Certification Suite files</td>
				</tr>
				<%--<g:if test="${SecurityUtils.subject.principal.equals("admin")}">
					<tr>
						<td><g:link controller="groups" action="index"
								params="[category:com.comcast.rdk.Category.RDKV]">
								<span>Groups</span>
							</g:link></td>
						<td>Option to add Groups</td>
					</tr>
					<tr>
						<td><g:link controller="user" action="index"
								params="[category:com.comcast.rdk.Category.RDKV ]">
								<span>User Management</span>
							</g:link></td>
						<td>Option to manage users</td>
					</tr>
				</g:if>
			--%></table>
		</div>
		</div>

	<div id="rdkB">
			<div style="float: left; padding-left: 10%; padding-top: 5%;">
				<h2 style="color: #A24C15;">
					<center>RDK-B</center>
				</h2>
			</div>
			<div style="width: 40%; margin: 0 auto; align: center;">
				<table>
					<tr>
						<td><g:link controller="module" action="list"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Modules</span>
							</g:link></td>
						<td>Configure Information about Component Interface Modules</td>
					</tr>
					<tr>
						<td><g:link controller="module" action="crashlog"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Link Crash Files</span>
							</g:link></td>
						<td>Link Crash Files to Modules</td>
					</tr>

					<tr>
						<td><g:link controller="module" action="logFileNames"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Link logs files</span>
							</g:link></td>
						<td>Link Configure Broadband logs to Module</td>
					</tr>
					<tr>
						<td><g:link controller="boxManufacturer" action="index"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Box Manufacturers</span>
							</g:link></td>
						<td>Option to add Box Manufacturers</td>
					</tr>
					<tr>
						<td><g:link controller="boxType" action="index"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Box Type</span>
							</g:link></td>
						<td>Option to add Box Type</td>
					</tr>
					<tr>
						<td><g:link controller="RDKVersions" action="index"
								params="[category:com.comcast.rdk.Category.RDKB ]">
								<span>RDK Versions</span>
							</g:link></td>
						<td>Option to add RDK Versions</td>
					</tr>
					<tr>
						<td><g:link controller="soCVendor" action="index"
								params="[category:com.comcast.rdk.Category.RDKB ]">
								<span>SoC Vendors</span>
							</g:link></td>
						<td>Option to add SoC Vendors</td>
					</tr>
					<tr>
						<td><g:link controller="ScriptTag" action="index"
								params="[category:com.comcast.rdk.Category.RDKB ]">
								<span>Script Tags</span>
							</g:link></td>
						<td>Option to add Script Tags</td>
					</tr>
					<tr>
					<td>
							<g:link controller="TestProfile" action="index"
								params="[category:com.comcast.rdk.Category.RDKB ]">
								<span>Test Profile</span>
							</g:link></td>
							<td>Option to add Test profile</td>
					</tr>
						
					<%--<g:if test="${SecurityUtils.subject.principal.equals("admin")}">
						<tr>
							<td><g:link controller="groups" action="index"
									params="[category:com.comcast.rdk.Category.RDKB]">
									<span>Groups</span>
								</g:link></td>
							<td>Option to add Groups</td>
						</tr>
						<tr>
							<td><g:link controller="user" action="index"
									params="[category:com.comcast.rdk.Category.RDKB]">
									<span>User Management</span>
								</g:link></td>
							<td>Option to manage users</td>
						</tr>
					</g:if>
				--%></table>
			</div>
		</div>
	<div id="rdkC">
		<div style="float: left; padding-left: 10%; padding-top: 5%;">
			<h2 style="color: #A24C15;">
				<center>RDK-C</center>
			</h2>
		</div>
		<div style="width: 40%; margin: 0 auto; align: center;">
			<!-- RDK_C -->
			<table>
				<tr>
					<td><g:link controller="module" action="list"
							params="[category: com.comcast.rdk.Category.RDKC]">
							<span>Modules</span>
						</g:link></td>
					<td>Configure Information about Component Interface Modules</td>
				</tr>
				<tr>
					<td><g:link controller="module" action="crashlog"
							params="[category:com.comcast.rdk.Category.RDKC ]">
							<span>Link Crash Files</span>
						</g:link></td>
					<td>Link Crash Files to Modules</td>
				</tr>

				<tr>
					<td><g:link controller="module" action="logFileNames"
							params="[category:com.comcast.rdk.Category.RDKC ]">
							<span>Link logs files</span>
						</g:link></td>
					<td>Link Configure STB logs to Module</td>
				</tr>
				<tr>
					<td><g:link controller="streamingDetails" action="list"
							params="[category:com.comcast.rdk.Category.RDKC]">
							<span>Streaming Details</span>
						</g:link></td>
					<td>Option to add streaming details</td>
				</tr>
				<tr>
					<td><g:link controller="boxManufacturer" action="index"
							params="[category:com.comcast.rdk.Category.RDKC]">
							<span>Box Manufacturers</span>
						</g:link></td>
					<td>Option to add Box Manufacturers</td>
				</tr>
				<tr>
					<td><g:link controller="boxType" action="index"
							params="[category:com.comcast.rdk.Category.RDKC]">
							<span>Box Type</span>
						</g:link></td>
					<td>Option to add Box Type</td>
				</tr>
				<tr>
					<td><g:link controller="RDKVersions" action="index"
							params="[category:com.comcast.rdk.Category.RDKC]">
							<span>RDK Versions</span>
						</g:link></td>
					<td>Option to add RDK Versions</td>
				</tr>
				<tr>
					<td><g:link controller="soCVendor" action="index"
							params="[category:com.comcast.rdk.Category.RDKC ]">
							<span>SoC Vendors</span>
						</g:link></td>
					<td>Option to add SoC Vendors</td>
				</tr>
				<tr>
						<td><g:link controller="ScriptTag" action="index"
								params="[category:com.comcast.rdk.Category.RDKC ]">
								<span>Script Tags</span>
							</g:link></td>
						<td>Option to add Script Tags</td>
					</tr>
					
				<tr>
					<td>
					
						<g:link controller="TestProfile" action="index"
								params="[category:com.comcast.rdk.Category.RDKC ]">
								<span>Test Profile</span>
							</g:link></td>
						<td>Option to add Test profile</td>
						
				</tr>
			</table>
		</div>
	</div>
	<div style="padding-top:40px;">
	
		<g:if test="${SecurityUtils.subject.principal.equals("admin")}">
		<div style="float: left; padding-left: 10%; ">
				<h2 style="color: #A24C15;">
					<center>Common Configuration</center>
				</h2>
			</div>
			<div style="width: 40%; margin: 0 auto; align: center;">
			<table style="max-width: 60%;">
				<tr>
					<td><g:link controller="groups" action="index">
							<span>Groups</span>
						</g:link></td>
					<td>Option to add Groups</td>
				</tr>
				<tr>
					<td><g:link controller="user" action="index">
							<span>User Management</span>
						</g:link></td>
					<td>Option to manage users</td>
				</tr>
			</table>
			</div>
		</g:if>
	</div>
</body>
</html>
