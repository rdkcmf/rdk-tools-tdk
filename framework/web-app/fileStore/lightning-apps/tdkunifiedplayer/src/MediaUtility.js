/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2022 RDK Management
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


  //Random number generator
  export function getRandomInt(max) {
     return Math.floor(Math.random() * max);
  }


  //Average of given numbers
  export function getAverage(dataList){
    var total = 0;
    for(var i = 0; i < dataList.length; i++) {
        total += parseInt(dataList[i]);
    }
    var avg = total / dataList.length;
    return avg.toFixed(2)
  }


  // Method to perform video progress position validation
  export function getPosValResult(pos_list,pos_index){
    var pos_val_status = "SUCCESS"
    var vid_pos_list = []
    var pos_diff = 0;
    var mismatch = ""
    var pos_mismatch_count = 0
    var pos_mismatch_list = []
    if (pos_list.length > 1){
        if (pos_index != 0){
            // removing video progress pos duplicates
            // for video operations except pause
            pos_list.forEach((pos) => {
                if(! vid_pos_list.includes(parseInt(pos)))
                    vid_pos_list.push(parseInt(pos))
            });
        }else{
            // keeping video progress pos duplicates as such
            // for video pause operation
            pos_list.forEach((pos) => {
                vid_pos_list.push(parseInt(pos))
            });
        }
        if (vid_pos_list.length > 1){
            for (var i = 0; i < vid_pos_list.length -1 ; i++){
                // finding the diff of curr pos and prev pos values
                pos_diff = vid_pos_list[i+1] - vid_pos_list[i]
                if (pos_index != 0){
                    // check whether pos diff is >= to the required diff
                    // for video operations except pause
                    if (!(pos_diff >= pos_index)){
                        pos_mismatch_count += 1
                        mismatch = "Pos:"+vid_pos_list[i+1]+"-"+vid_pos_list[i]+",diff="+pos_diff
                        pos_mismatch_list.push(mismatch)
                    }
		}else{
                    // check whether pos diff is = to the required diff
                    // for video pause operation
                    if (!(pos_diff == pos_index)){
                        pos_mismatch_count += 1
                        mismatch = "Pos:"+vid_pos_list[i+1]+"-"+vid_pos_list[i]+",diff="+pos_diff
                        pos_mismatch_list.push(mismatch)
                    }
                }
            }
            // If the pos diff is not as expected for more than max threshold limit
            // consider pos validation status as failure
            if (pos_mismatch_count > 3){
                logMsg(pos_mismatch_list)
                logMsg("Failure Reason: Video Progress position difference is not as expected")
                pos_val_status = "FAILURE"
            }
        }else{
            pos_val_status = "FAILURE"
        }
    }else{
        pos_val_status = "FAILURE"
    }
    logMsg("Video Progress position validation status: "+pos_val_status)
    return pos_val_status
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
    var inputs = window.location.search.substring(1).split("&");
    var player = GetURLParameter("player")
    var options = []
    inputs.forEach(item => {
        if(item.split("=")[0] == "options"){
          options = GetURLParameter("options").split(",");
        }
    });
    options.forEach(item => {
      if(item.includes("useDashlib")){
         var dashlib = item.split('(')[1].split(')')[0]
         if (dashlib == "yes" || dashlib == "YES")
           player = "DASHJS"
      }
      else if(item.includes("useHlslib")){
         var hlslib = item.split('(')[1].split(')')[0]
         if (hlslib == "yes" || hlslib == "YES")
           player = "HLSJS"
      }
    });
    console.log("[ " + dispTime() + " ] [" + player + "] " + msg)
    //console.log("[ " + dispTime() + " ] " + msg)
  }
  // To log the Events occured
  export function logEventMsg(observedEvents,msg){
    console.log("*****************************************************************\n" +
                "Observed Event: " + observedEvents    + "\n"  +
                "Event Details : " + "[ " + dispTime() + " ] " + msg  + "\n" +
                "*****************************************************************");
  }
  // To log the general API outputs
  export function logActionMsg(msg){
    console.log("*****************************************************************\n" +
                "[ " + dispTime() + " ] " + msg  + "\n" +
                "*****************************************************************");
  }
  // To log the DASHJS Events occured
  export function logDASHEventMsg(e){
      logMsg(e.type)
  }
