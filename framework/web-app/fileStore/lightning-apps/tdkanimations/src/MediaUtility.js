/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
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

  // Method to find the type of the video stream
  export function getVideoURLType(url){
      if (url.includes('.mp4') || url.includes('.webm'))
          urlType = "Regular"
      else if (url.includes('.m3u8'))
          urlType = "M3U8"
      else if (url.includes('.mpd'))
          urlType = "MPD"
      logMsg("URL Info: " + url + " - " + urlType)
      return urlType
  }

  // Method to parse the operations from the URL parameter
  export function  getOperations(operationsStr){
      var operations = operationsStr.split(',');
      var repeatpos  = []
      var alloperations = ""
      for (var i = 0; i < operations.length; i++){
          if ( operations[i].includes("repeat") )
            repeatpos.push(i)
      }
      if (repeatpos.length > 0 ){
          var i,j,t,temp
          for (var n = 0; n < repeatpos.length; n++){
              if (n == 0)
                  i = 0
              else
                  i = parseInt(repeatpos[n-1]) + 1
              j = parseInt(repeatpos[n])
              t = parseInt(operations[repeatpos[n]].split("(")[1].split(")")[0]);
              temp = ""
              for (var k = 0; k < t; k++){
                  if (temp != "")
                      temp += ","
                  temp = temp + operations.slice(i,j)
              }
              if (alloperations!= "")
                  alloperations += ","
              alloperations += temp
          }
          temp = ""
          i = parseInt(repeatpos[repeatpos.length - 1])
          j = parseInt(operations.length -1)
          if ( i != j ){
              if ( i+1 != j )
                  temp = temp + operations.slice(i+1,j+1)
              else
                  temp = temp + operations[j]
              alloperations = alloperations + "," + temp
          }
          operations = alloperations.split(",")
      }
      return operations
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
  // To log the Events occured
  export function logEventMsg(msg){
    var logging = GetURLParameter("logging")
    var log_msg = "[ " + dispTime() + " ] " + "Event Occurred: " + msg
    console.log(log_msg)
    if(logging == "REST_API"){
        captureAppLogs(log_msg)
    }
  }

  // To set delay
  export function sleep(ms){
    return new Promise(
      resolve => setTimeout(resolve, ms)
    );
  }

  export async function setDelay(ms){
    await sleep(ms)

  }


