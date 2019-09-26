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
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="layout" content="main" />
  <title>Login</title>
  <g:javascript library="validations" />
  <script type="text/javascript">
	
	function onForgotClick(){		
		$("#forgotPasswordModal").modal({ opacity : 40, overlayCss : {
			  backgroundColor : "#c4c4c4" }, containerCss: {
		            width: 300,
		            height: 100
		            
		        } }, { onClose : function(dialog) {
			  $.modal.close(); } }); 		 
	}
	
	function onRegisterClick(){		
		$("#registerPasswordModal").modal({ opacity : 40, overlayCss : {
			  backgroundColor : "#c4c4c4" }, containerCss: {
		            width: 350,
		            height: 250
		            
		        } }, { onClose : function(dialog) {
			  $.modal.close(); } }); 		 
	}

	function validateee(){		
		return false;
	}
	
	</script>
</head>

<body><br><br><br><br><br><br>
  <g:if test="${flash.message}">
    <div class="message">${flash.message}</div>
  </g:if>
  <g:if test="${flash.error}">
    <div class="errors">${flash.error}</div>
  </g:if>
  <g:form action="signIn">
    <input type="hidden" name="targetUri" value="${targetUri}" />
    <div style="width:40%;margin: 0 auto;align:center;">
    <br><br>
    <table>
      <tbody>
        <tr>
          <td>Username:</td>
          <td><input type="text" name="username" value="${username}" /></td>
        </tr>
        <tr>
          <td>Password:</td>
          <td><input type="password" name="password" value="" /></td>
        </tr>
        <%--<tr>
          <td>Remember me?:</td>
          <td><g:checkBox name="rememberMe" value="${rememberMe}" /></td>
        </tr>
        --%><tr>
          <td />
          <td>&emsp;&emsp;&emsp;&emsp;<input type="submit" value="Sign in" /></td>
        </tr>
        <tr>
        <td />
        <td>
	        <g:link action="registerUser" controller="user" value="RegisterMe" >Register Me</g:link>&nbsp;|
			<a href="#" onclick="onForgotClick()" >Forgot Password</a></td>
        </tr>
      </tbody>
    </table>
    </div>
  </g:form>
  <br><br><br><br><br><br>
  <div id ="forgotPasswordModal" style="display:none;" >
	<g:form action="forgotPassword" >
	Username: 
	<g:textField id = "username" name="username" required="" value=""  placeholder="Username" /><br/><br/>
	<input type="submit" value="Get New Password"/><br/><br/>
	
	</g:form>
  </div>
  <div id ="registerPasswordModal" style="display:none;" >
	<g:form action="registerUser">
		<table>
		<tr>
		<td>
	 	Name        :</td><td><g:textField name="name" required="" value="" /></td>
	 	</tr>
		<tr>
		<td>
	 	Username        :</td><td><g:textField name="username" required="" value="" /></td>
	 	</tr>
	 	<tr>
	 	<td>
		Password    : </td><td><g:passwordField name="passwordHash" required="" value="" /></td>
		</tr>		
		<tr>
		<td>Confirm Password: </td><td><g:passwordField name="confirmPassword" required="" value="" /></td>
		</tr>
		<tr>
		<td>email: </td><td><g:textField id="email" name="email" required="" value=""/></td>
		</tr>
		<tr>
		<tr>		
		<td>Group   : </td><td>
			<g:select id="groupName" name="groupName.id" from="${com.comcast.rdk.Groups.list()}" style="width:150px;" optionKey="id" value="${userInstance?.groupName?.id}" class="many-to-one" noSelection="['null': 'Select One']"/>
		</td>
		</tr>
		<tr>
		<td>
		</td>
		<td align="right">
		<input type="submit" onclick="validateee(); return false;" value="Register Me"/>
		</td>
		</tr>
		</table>
			
	</g:form>
	</div>
  
</body>
</html>
