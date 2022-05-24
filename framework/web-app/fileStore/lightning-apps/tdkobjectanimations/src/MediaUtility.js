/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2021 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

  let message = "";

  // Method to parse the URL parameters
  export function GetURLParameter(sParam){
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
    }
  }

  // Method to store the app logs and send them to TM
  export function captureAppLogs(msg){
    if (message.length < 300) {
        //console.log("msg_append")
        message = message + "\n" + msg
    }else{
        //console.log("msg_out")
        sendLog(message)
        message = ""+ msg
    }
    return;
  }

  // Method to send the logs to TM
  export function pushAppLogs(msg){
     if(message.length > 0){
          sendLog(message)
          message = "";
     }
     sendLog(msg);
  }

  // Method to send the logs to TM via REST API
  export function sendLog(msg){
    var tmURL = window.location.href.split("fileStore")[0];
    let restURL = tmURL  + 'execution/createFileAndWrite?'
    const execID = GetURLParameter('execID')
    const devID = GetURLParameter('execDevId')
    const resID = GetURLParameter('resultId')
    //console.log("URL: " +restURL)
    fetch(restURL + new URLSearchParams({execId: execID,
                                     execDevId: devID,
                                     resultId: resID,
                                     test: msg
    }))
    .then(response => {
                console.log('Response from Test Manager: '+ JSON.stringify(response))
     })
     .catch(error => {
                console.log('Error while connecting to Test Manager: '+ error)
    });
    return;
  }

  // Method to get Time info
  export function dispTime() {
    var now = new Date();
    var h  = now.getUTCHours()
    var m  = now.getUTCMinutes()
    var s  = now.getUTCSeconds()
    var ms = now.getUTCMilliseconds()
    if (h < 10)
      h = "0" + h
    if (m < 10)
      m = "0" + m
    if (s < 10)
      s = "0" + s
    if (ms < 10)
      ms = "00" + ms
    else if (ms < 100)
      ms = "0" + ms
    return h + ":" + m + ":" + s + ":" + ms;
  }


  // Method to format bytes data
  export function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = 2;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  export function getAverage(dataList){
    var total = 0;
    for(var i = 0; i < dataList.length; i++) {
        total += parseInt(dataList[i]);
    }
    var avg = total / dataList.length;
    return avg.toFixed(2)
  }

  // To log the general messages
  export function logMsg(msg){
    var logging = GetURLParameter("logging")
    var log_msg = "[ " + dispTime() + " ] " + msg
    console.log(log_msg)
    if(logging == "REST_API"){
        if(msg.includes("TEST COMPLETED")){
            pushAppLogs(log_msg)
        }else if(msg.includes("TEST RESULT")){
            pushAppLogs(log_msg)
        }else{
            captureAppLogs(log_msg)
        }
    }
  }

