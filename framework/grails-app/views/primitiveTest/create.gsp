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
<%@ page import="com.comcast.rdk.PrimitiveTest" %>
<%--<!DOCTYPE html>--%>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${message(code: 'primitiveTest.label', default: 'PrimitiveTest')}" />
		<link rel="stylesheet" href="${resource(dir:'css',file:'jquery.treeview.css')}" />
		<title>Primitive Tests Control Panel</title>
	  	<g:javascript library="jquery.cookie"/>
	  	<g:javascript library="jquery.treeview.async"/>
	  	<g:javascript library="jquery.treeview"/>
	  	<g:javascript library="jquery.contextmenu.r2" />
	  	<g:javascript library="test_resolver" />
	  	<g:javascript library="common" />
	  	
	  	<script type="text/javascript">

		$(document).ready(function() {
	
			var primitiveTestId = $("#currentPrimitiveTestId").val();
			if(primitiveTestId){
				makeTestEditable(primitiveTestId, null);
				$("#currentPrimitiveTestId").val("");
			}
		});

	</script>		
	</head>
	<body>
		<a href="#create-primitiveTest" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div id="" class="">
			<h1>Primitive Tests Control Panel</h1>
			<g:if test="${flash.message}">
				<div class="message" role="status">${flash.message}</div>
			</g:if>
			<g:if test="${error}">
				<ul class="errors" role="alert">
					<li>${error}</li>
				</ul>
			</g:if>
			<br>
			<div id="testMessageDiv" class="message" style="display: none;"></div>
			
			<input type="hidden" name="decider" id="decider" value="${params.id}">
			<table class="noClass" style="border: 1; border-color: black;">
				<tr>
					<td>
						<div class="treeborder" style="width: 290px; height: 400px; overflow: auto;">
							<ul id="primitveTestbrowser" class="filetree">
								<li  class="" id="root"><span class="folder">Primitive Tests</span>
									<ul>
										<li><span class="closed">RDK-V</span>
										<ul>
										
										<% int primitiveTestIndex = 0; %>
										<g:each in="${primitiveTestMapA}" var="mapEntry">
										<li class="closed"><span class="folder" id="addTestId">${mapEntry.key}</span>
											<ul id ="module_">
												<g:each in="${mapEntry.value}" var="test">
												<%  primitiveTestIndex++; %>
											<li id="primitiveTestList_${primitiveTestIndex}">
												<span class="file" id="${test}@RDKV">
													<a href="#" onclick="makeTestEditable('${test}','RDKV'); highlightTreeElement('primitiveTestList_', '${primitiveTestIndex}', '${primitiveTestCount}'); return false;">${test}</a>
												</span>
												</li>
												</g:each>
												</ul>
											</li>
											</g:each>
										</ul>
										</li>
										<li><span class="closed">RDK-B</span>
										<ul>
										<% int primitiveTestIndex2 = 0; %>
										<g:each in="${primitiveTestMapB}" var="mapEntry">
										<li class="closed"><span class="folder" id="addTestId">${mapEntry.key}</span>
											<ul id ="module_">
												<g:each in="${mapEntry.value}" var="test">
												<%  primitiveTestIndex++; %>
											<li id="primitiveTestList_${primitiveTestIndex}">
												<span class="file" id="${test}@RDKB">
													<a href="#" onclick="makeTestEditable('${test}','RDKB'); highlightTreeElement('primitiveTestList_', '${primitiveTestIndex}', '${primitiveTestCount}'); return false;">${test}</a>
												</span>
												</li>
												</g:each>
												</ul>
											</li>
											</g:each>
										
										</ul>
										</li>
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
	          		<li id="add_propertyV"><img src="../images/add_new.png" height="15px" width="15px"/>Add New RDK-V Primitive Test </li>
	          		<li id="add_propertyB"><img src="../images/add_new.png" height="15px" width="15px"/>Add New RDK-B Primitive Test</li>
	        	</ul>
	      </div>
			<div class="contextMenu" id="childs_menu">
				<ul>
					<li id="edit_test"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_test">
	          		
	          		<img src="../images/delete.png" />
	          			
	          		Delete</li>
	        	</ul>
	      </div>
		</div>
		<g:hiddenField name="currentPrimitiveTestId" id="currentPrimitiveTestId" value="${primitiveTestId}"/>
		<g:hiddenField name="isTestExist" id="isTestExist" value=""/>
	</body>
</html>
