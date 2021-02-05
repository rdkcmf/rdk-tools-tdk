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

  // Method to parse the operations from the URL parameter
  export function getVideoOperations(operationsStr){
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


  // To log the general messages
  export function logMsg(msg){
    console.log("[ " + dispTime() + " ] " + msg)
  }
  // To log the Events occured
  export function logEventMsg(observedEvents,msg){
    console.log("*****************************************************************\n" +
                "Observed Event: " + observedEvents    + "\n"  +
                "Event Details : " + "[ " + dispTime() + " ] " + msg  + "\n" +
                "*****************************************************************");
  }


