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
<%@ page import="com.comcast.rdk.Module" %>
<%@ page import="com.comcast.rdk.User" %>
<%@ page import="com.comcast.rdk.Groups" %>
<%@ page import="org.apache.shiro.SecurityUtils" %>

<table>
  <tr>
    <th>Select Module</th>
  </tr>
  <tr>
    <td>
    <%
		def user = User.findByUsername(SecurityUtils.subject.principal)
		def group = Groups.findById(user.groupName?.id)
	%>
    	<g:select from="${Module.findAllByGroupsOrGroupsIsNull(group, [order: 'asc', sort: 'name'])}" var="module" noSelection="['' : 'Please Select']" id="module" name="module"/>
    </td>
  </tr>
</table>

