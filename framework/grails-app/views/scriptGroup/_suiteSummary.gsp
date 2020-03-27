<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2019 RDK Management

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
<script type='text/javascript'>
$(document).ready(function() {
	$("#list-suiteDetailsV").show();
	$("#suitetTableV").dataTable( {
		"sPaginationType": "full_numbers",
		"bRetrieve": true
	});
	$("#list-suiteDetailsB").show();
	$("#suiteTableB").dataTable( {
		"sPaginationType": "full_numbers",
		"bRetrieve": true
	});
	$("#list-suiteDetailsC").show();
	$("#suiteTableC").dataTable( {
		"sPaginationType": "full_numbers",
		"bRetrieve": true
	});
	var scriptId = $("#currentScriptId").val();
	if(scriptId!=null && scriptId!=""){
		editScript(scriptId);
	}
	var scriptGroupId = $("#currentScriptGroupId").val();
	if(scriptGroupId){
		editScriptGroup(scriptGroupId);
	}
});
</script>
<div style="width: 95%; max-height: 600px; display: none ;"
    id="list-suiteDetailsV" class="content scaffold-list"
    id="suiteDetailsV">
    <table id="suitetTableV" class="display">
        <thead>
            <tr>
                <th colspan="3" align="center" style="width: 50%;"><h1> RDKV TestSuite
                        Details Summary</h1></th>
            </tr>
            <tr align="left">
                <th width="20%">Sl No</th>
                <th width ="60%">TestSuite Name</th>
                <th width ="20%">Script Count</th>
            </tr>
        </thead>
        <br>
        <br>
        <tbody align="left">
            <%int testSuiteCount =0  %>
            <g:each in="${testSuiteMapV}" var=" name">

                <tr class="odd">
                    <%     testSuiteCount++ %>
                    <td>
                        ${testSuiteCount}
                    </td>
                    <td>
                        ${name.key}
                    </td>
                    <td>
                        ${name.value}
                    </td>
                </tr>
                </g:each>
        </tbody>
    </table>
</div>

<div style="width: 95%; max-height: 600px; display: none ;"
    id="list-suiteDetailsB" class="content scaffold-list"
    id="suiteDetailsB">
    <table id="suiteTableB" class="display">
        <thead>
            <tr>
                <th colspan="3" align="center" style="width: 50%;"><h1> RDKB TestSuite
                        Details Summary</h1></th>
            </tr>
            <tr align="left">
                <th width="20%">Sl No</th>
                <th width ="60%">TestSuite Name</th>
                <th width ="20%">Script Count</th>
            </tr>
        </thead>
        <br>
        <br>
        <tbody align="left">
            <%int testSuiteCount1 =0  %>

            <g:each in="${testSuiteMapB}" var=" name">

                <tr class="odd">
                    <%     testSuiteCount1++ %>
                    <td>
                        ${testSuiteCount1}
                    </td>
                    <td>
                        ${name.key}
                    </td>
                    <td>
                        ${name.value}
                    </td>
                    </tr>
                </g:each>
        </tbody>
    </table>
</div>

<div style="width: 95%; max-height: 600px; display: none ;"
    id="list-suiteDetailsC" class="content scaffold-list"
    id="suiteDetailsC">
    <table id="suiteTableC" class="display">
        <thead>
            <tr>
                <th colspan="3" align="center" style="width: 50%;"><h1> RDKC TestSuite
                        Details Summary</h1></th>
            </tr>
            <tr align="left">
                <th width="20%">Sl No</th>
                <th width ="60%">TestSuite Name</th>
                <th width ="20%">Script Count</th>
            </tr>
        </thead>
        <br>
        <br>
        <tbody align="left">
            <%int testSuiteCount2 =0  %>
            <g:each in="${testSuiteMapC}" var=" name">

                <tr class="odd">
                    <%     testSuiteCount2++ %>
                    <td>
                        ${testSuiteCount2}
                    </td>
                    <td>
                        ${name.key}
                    </td>
                    <td>
                        ${name.value}
                    </td>
                </tr>
                </g:each>
        </tbody>
    </table>
</div>