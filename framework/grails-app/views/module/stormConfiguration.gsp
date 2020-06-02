<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2020 RDK Management

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
<%@ page import="com.comcast.rdk.Module" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${category} ${message(code: 'module.label', default: 'Storm JSON RPC Server Configuration')}" />
		<title><g:message code="default.create.label" args="[entityName]" /></title>
		<script type="text/javascript">
		    function nodeRestart(){
			    $.get('nodeRestartAndScriptListRefresh',function(data){
				    var val = JSON.parse(data);
				    if( val == true ){
					    alert(" Storm JSON RPC server Restarted!");
				    }
			    });
		    }
		</script>
	</head>
	<body>
	    <a href="#show-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
	    <div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="<g:createLink params="[category:category]" action="configuration" controller="module"/>"><g:message code="default.home.label"/></a></li>
			</ul>
		</div>
	    <div id="show-module" class="content scaffold-show" role="main">
	        <h1>Storm JSON RPC Server Setings</h1>
	         <div>
	            <table style="width:50%;">
	                <tr>
				        <td>
				            <span id="nodeRestartButton" class="buttons">
                                <input type=button onclick="nodeRestart()" value="Storm JSON RPC Server Restart" />
                            </span>
				        </td>
				        <td>Storm JSON RPC Server restart button for RDKV storm execution</td>
				    </tr>
	            </table>
	        </div>
	</body>
</html>