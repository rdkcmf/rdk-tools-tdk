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
<%@ page import="com.comcast.rdk.RadioStreamingDetails" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${message(code: 'streamingDetails.label', default: 'StreamingDetails')}" />
		<title><g:message code="default.list.label" args="[entityName]" /></title>
		<link rel="stylesheet" href="${resource(dir:'css',file:'jquery.treeview.css')}" />
		<g:javascript library="jquery.cookie"/>
	  	<g:javascript library="jquery.treeview.async"/>
	  	<g:javascript library="jquery.treeview"/>
	  	<g:javascript library="jquery.contextmenu.r2" />
	  	<g:javascript library="stream_resolver" />
	</head>
	<body>		
	<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="${createLink(uri: '/module/configuration')}"><g:message code="default.home.label"/></a></li>
			</ul>
	</div>		
		<div id="list-streamingDetails" class="content scaffold-list" role="main">
			<h1><g:message code="default.list.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			
			<table class="noClass" style="border: 1; border-color: black;">
				<tr>
					<td>
						<div class="" style="width: 200px; height: 400px; overflow: auto;">
							<ul id="streambrowser" class="filetree">
								<li class="" id="root"><span id= "video" class="folder">Streaming Details</span>
									<ul>
										<g:each in="${streamingDetailsInstanceList}" var="stream">
											<li><span  id="video" class="file" id="${stream.id}"><a href="#" onclick="showStreamDetails('${stream.id}'); return false;">${stream.streamId}</a></span></li>
										</g:each>
									</ul>
								</li>
								<li class="" id="root1"><span id ="radio" class="folder">Radio Streaming Details</span>
									<ul>
										<g:each in="${radioStreamingDetails}" var="stream">
											<li><span id="radio" class="file" id="${stream.id}"><a href="#" onclick="showRadioStreamDetails('${stream.id}'); return false;">${stream.streamId}</a></span></li>
										</g:each>
									</ul>
								</li>
							</ul>
						</div>
					</td>
					<td>
						<div id="responseDiv" style="width: 500px; height: 400px; overflow: auto;"></div>
					</td>
				</tr>
			</table>
			<div class="contextMenu" id="root_menu">
				<ul>
	          		<li id="add_property"><img src="../images/add_new.png" height="15px" width="15px"/>Add New Stream Details</li>
	        	</ul>
	        </div>
			<div class="contextMenu" id="childs_menu">
				<ul>
					<li id="edit_test"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_test">	          		
	          		<img src="../images/delete.png" />Delete</li>
	        	</ul>
	        </div>			
		</div>
	</body>
</html>
