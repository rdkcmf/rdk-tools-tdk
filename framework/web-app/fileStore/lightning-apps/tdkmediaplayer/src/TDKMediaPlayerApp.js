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
import { Lightning, Utils, Log, Metrics} from '@lightningjs/sdk'
import MediaPlayerAdvanced from './MediaPlayerAdvanced.js'

export default class App extends Lightning.Component {
  static getFonts() {
    return [{ family: 'Regular', url: Utils.asset('fonts/Roboto-Regular.ttf') }]
  }

  static _template() {
    return {
      TDKLogo: {
        mountX: 0.5,
        mountY: 0.5,
        x: 280,
        y: 50,
        h: 80,
        src: Utils.asset('images/TDK_logo.png'),
      },
      TDKTitle: {
        mount: 0.5,
        x: 750,
        y: 50,
        text: {
          text: "TDK Lightning Player Test App",
          fontFace: 'Regular',
          fontSize: 40,
          textColor: 0xFF1C27bC,
        },
      },
      MsgBox1: {
        x: 200,
        y: 100,
        w: 600,
        text: {
          fontFace: 'Regular',
          fontSize: 25,
          textColor: 0xFF000000,
        },
      },
      MsgBox2: {
        x: 700,
        y: 100,
        w: 500,
        text: {
          fontFace: 'Regular',
          fontSize: 25,
          textColor: 0xFF000000,
        },
      },
      MediaPlayer: { type: MediaPlayerAdvanced,visible: true}
    }
  }

  // Method to check the URL type
  setVideoURL(url){
      this.videoURL = url
      if (url.includes('.mp4') || url.includes('.webm'))
          this.urlType = "Regular"
      else if (url.includes('.m3u8'))
          this.urlType = "M3U8"
      else if (url.includes('.mpd'))
          this.urlType = "MPD"
      this.logMsg("URL Info: " + this.videoURL + " - " + this.urlType)
  }

  // Method to open the video player with the video URL
  loadPlayer(){
      if (this.urlType == "Regular")
          this.tag('MediaPlayer').open(this.videoURL)
      else if (this.urlType == "M3U8")
          this.tag('MediaPlayer').openHls(this.videoURL)
      else if (this.urlType == "MPD"){
          this.tag('MediaPlayer').openDash(this.videoURL)
      }
      this.logMsg("Loaded Media Player")
  }

  // Methods to perform video playback/trickplay
  play(){
    this.expectedEvents = ["play"]
    this.logMsg("Expected Event: " + this.expectedEvents)
    this.tag('MediaPlayer').videoEl.playbackRate = 1
    this.tag('MediaPlayer').doPlay()
  }
  playPause(){
    if (this.tag('MediaPlayer'). isPlaying())
        this.expectedEvents = ["paused"]
    else
        this.expectedEvents = ["play"]
    this.logMsg("Expected Event: " + this.expectedEvents)
    this.tag('MediaPlayer').playPause()
  }
  pause() {
    this.expectedEvents = ["paused"]
    this.logMsg("Expected Event: " + this.expectedEvents)
    this.tag('MediaPlayer').doPause()
  }
  seekfwd(pos,absolute=false){
    this.expectedPos = this.tag('MediaPlayer').videoEl.currentTime + pos
    this.expectedEvents = ["seeking","seeked"]
    this.logMsg("Expected Event: "   + this.expectedEvents)
    this.logMsg("Expected Pos  : [ " + (this.expectedPos).toFixed(2) + " - " + (this.expectedPos + 3).toFixed(2) + " ]")
    this.tag('MediaPlayer').seek(pos,absolute)
  }
  seekbwd(pos,absolute=false){
    this.expectedPos = this.tag('MediaPlayer').videoEl.currentTime - pos
    this.expectedEvents = ["seeking","seeked"]
    this.logMsg("Expected Event: " + this.expectedEvents)
    this.logMsg("Expected Pos  : [ " + (this.expectedPos).toFixed(2) + " - " + (this.expectedPos + 3).toFixed(2) + " ]")
    this.tag('MediaPlayer').seek(-pos,absolute)
  }

  fastfwd() {
    if (this.playbackRateIndex < this.playbackSpeeds.length - 1) {
      this.playbackRateIndex++
    }
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.logMsg("Action: Fast Forward")
    this.expectedRate = this.rate
    this.logMsg("Expected Rate: " + this.expectedRate)
    this.tag('MediaPlayer').videoEl.playbackRate = this.rate
  }

  rewind() {
    if (this.playbackRateIndex > 0) {
      this.playbackRateIndex--
    }
    this.logMsg("Action: Rewind(reduces rate)")
    this.expectedRate = this.rate
    this.logMsg("Expected Rate: " + this.expectedRate)
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.tag('MediaPlayer').videoEl.playbackRate = this.rate
  }
  close(){
    this.logMsg("Closing Media Player...")
    this.tag('MediaPlayer').close()
  }


  //Event Handlers
  $mediaplayerLoadStart(){
    this.message1 = "Media Player Load Start"
    this.dispMessage(this.message1)
    this.logEventMsg(this.message1)
  }
  $mediaplayerLoadedData(){
    this.message1 = "Media Player Loaded Data"
    this.dispMessage(this.message1)
    this.logEventMsg(this.message1)
  }
  $mediaplayerError(){
    this.errorFlag = 1
    this.message1 = "Media Player Error"
    this.dispMessage(this.message1)
    this.logEventMsg(this.message1)
  }
  $mediaplayerEncrypted(){
    this.message1 = "Media Player Encrypted"
    this.dispMessage(this.message1)
    this.logEventMsg(this.message1)
  }

  $mediaplayerProgress({ currentTime, duration }) {
    if ( this.init == 0 ){
        this.logMsg("******************* VIDEO STARTED PLAYING !!! *******************")
        this.logMsg("VIDEO DURATION: " + duration.toFixed(4))
    }
    this.message2 = "Pos: " + currentTime.toFixed(2) + "/" + duration.toFixed(2)
    this.logMsg("Video Progressing: " + currentTime.toFixed(4) + "/" + duration.toFixed(4))
    this.dispVideoPosition(this.message2)

    if ( this.init == 0 ){
        this.checkAndStartAutoTesting()
        this.init = 1 //inited
    }
  }

  $mediaplayerPlaying(){
    this.message1 = "Media Player Playing"
    this.dispMessage(this.message1)
    this.logEventMsg(this.message1)
  }

  $mediaplayerPlay(){
    this.observedEvents.push("play")
    this.message1 = "Media Player Play"
    this.dispMessage(this.message1)
    this.checkAndLogEvents("play",this.message1 + " !!!")
  }

  $mediaplayerPause(){
    this.observedEvents.push("paused")
    this.message1 = "Media Player Paused"
    this.dispMessage(this.message1)
    this.checkAndLogEvents("pause",this.message1 + " !!!")
  }

  $mediaplayerSeeking({ currentTime, duration }) {
    this.observedEvents.push("seeking")
    this.message1 = "Media Player Seeking " + currentTime.toFixed(2) + "/" + duration.toFixed(2)
    this.dispMessage(this.message1)
    this.checkAndLogEvents("seeking",this.message1)
  }

  $mediaplayerSeeked({ currentTime, duration }) {
    this.observedEvents.push("seeked")
    this.message1 = "Media Player Seeked " + currentTime.toFixed(2) + "/" + duration.toFixed(2)
    this.dispMessage(this.message1)
    this.checkAndLogEvents("seeked",this.message1)
  }
  $mediaplayerEnded(){
    this.message1 = "Media Player Ended"
    this.dispMessage(this.message1)
    this.logEventMsg(this.message1)
  }
  $mediaplayerStop(){
    this.message1 = "Media Player Stop"
    this.dispMessage(this.message1)
    this.logEventMsg(this.message1)
  }

  // To display Events & Video position in UI
  dispMessage(msg){
      this.tag("MsgBox1").text.text = `Evt: ${msg}`;
  }
  dispVideoPosition(msg){
      this.tag("MsgBox2").text.text = `${msg}`;
  }


  // To log the Events occured
  logEventMsg(msg){
    console.log("[ " + this.dispTime() + " ] " + "Event Occurred: " + msg )
  }
  logEventFlow(msg){
    console.log("*****************************************************************\n" +
                "Observed Event: " + this.observedEvents    + "\n"  +
                "Event Details : " + "[ " + this.dispTime() + " ] " + msg  + "\n" +
                "*****************************************************************");
  }
  logMsg(msg){
    console.log("[ " + this.dispTime() + " ] " + msg)
  }

  dispTime() {
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

  // To check the Events occurred
  checkAndLogEvents(checkevent,msg){
    if ( this.checkEvents.includes(checkevent) ){
        this.logEventFlow(msg)
    }else{
        this.logEventMsg(msg)
    }
  }
  clearObservedEvents(){
      this.observedEvents = []
  }
  updateEventFlowFlag(){
      if (this.checkEvents.includes("ratechange")){
          var currRate = parseInt(this.tag('MediaPlayer').videoEl.playbackRate)
          console.log("*****************************************************************\n" +
                      "[ " + this.dispTime() + " ] " + "Observed Rate: " + currRate + "\n"  +
                      "*****************************************************************");
          if( currRate == this.expectedRate ){
              this.logMsg("video rate change operation success")
              this.logMsg("Test step status: SUCCESS")
          }else{
              this.eventFlowFlag = 0
              this.logMsg("video rate change operation failure")
              this.logMsg("Test step status: FAILURE")
          }
          this.clearObservedEvents();
          return;
      }
      if( ! this.expectedEvents.some(e=> this.observedEvents.indexOf(e) >= 0)){
          this.eventFlowFlag = 0
          this.logMsg("Test step status: FAILURE")
      }
      else{
          if (this.expectedEvents.includes("seeking")){
              var currTime = parseInt(this.tag('MediaPlayer').videoEl.currentTime)
              var expTime  = parseInt(this.expectedPos)
              //console.log("Time: " + currTime + " range: " + expTime + " - " + (expTime+3))
              if ( currTime >= expTime && currTime <= (expTime+3) ){
                  this.logMsg("video seek operation success")
                  this.logMsg("Test step status: SUCCESS")
              }else{
                  this.eventFlowFlag = 0
                  this.logMsg("video seek operation failure")
                  this.logMsg("Test step status: FAILURE")
              }
          }else{
              this.logMsg("Test step status: SUCCESS")
          }
      }
      this.clearObservedEvents();
  }
  dispTestResult(){
    if (this.eventFlowFlag == 1 && this.errorFlag == 0)
        this.logMsg("TEST RESULT: SUCCESS")
    else{
        this.logMsg("eventFlowFlag: " + this.eventFlowFlag + " errorFlag: " + this.errorFlag)
        this.logMsg("TEST RESULT: FAILURE")
    }
  }

  GetURLParameter(sParam)
  {
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

  checkAndStartAutoTesting(){
    if (this.autotest == "true")
    {
      console.log("\n********************** STARTING AUTO TEST ***********************")
      this.performOperation()
    }else{
      console.log("\n***************** PRESS KEYS TO DO OPERATIONS ********************")
    }
  }

  performOperation(){
      var operations = this.GetURLParameter("operations")
      operations = operations.split(',');
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
      var actionInterval = 0
      this.logMsg("Setting up the operations...")
      for (var i = 0; i < operations.length; i++)
      {
          var action   = operations[i].split('(')[0];
          var duration = parseInt(operations[i].split('(')[1].split(')')[0]);
          actionInterval = actionInterval + (this.interval*duration)

            if (action == "pause"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    this.checkEvents = ["pause"]
                    this.pause()
                },actionInterval);
            }
            else if (action == "play"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    this.checkEvents = ["play"]
                    this.play()
                },actionInterval);
            }
            else if (action == "switch"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    if (this.tag('MediaPlayer'). isPlaying())
                        this.checkEvents = ["paused"]
                    else
                        this.checkEvents = ["play"]
                    this.playPause()
                },actionInterval);
            }
            else if (action == "seekfwd"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    this.checkEvents = ["seeking","seeked"]
                    this.seekfwd(this.seekInterval)
                },actionInterval);
            }
            else if (action == "seekbwd"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    this.checkEvents = ["seeking","seeked"]
                    this.seekbwd(this.seekInterval)
                },actionInterval);
            }
            else if (action == "fastfwd"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    this.checkEvents = ["ratechange"]
                    this.fastfwd()
                },actionInterval);
            }
            else if (action == "rewind"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    this.checkEvents = ["ratechange"]
                    this.rewind()
                },actionInterval);
            }
            else if (action == "close"){
                setTimeout(()=> {
                    this.close()
                },actionInterval);
            }
            if (action != "close"){
                setTimeout(()=> {
                    this.updateEventFlowFlag();
                },actionInterval+1000);
            }
      }
      if (! operations.find(o=> o.includes("close"))){
          setTimeout(()=> {
            this.close()
          },(actionInterval+10000));
      }
      setTimeout(()=> {
        this.dispTestResult()
      },(actionInterval+15000));
      console.log("\n");
  }

   // Key press for operations
   // Operations validation steps has to be added
   _handleEnter(){
     this.play()
   }
   _handleShift(){
     this.pause()
   }
   _handleAlt(){
     this.playPause()
   }
   _handleUp(){
     this.seekfwd(this.seekInterval)
   }
   _handleDown(){
     this.seekbwd(this.seekInterval)
   }
   _handleRight(){
     this.fastfwd()
   }
   _handleLeft(){
     this.rewind()
   }



  _init() {

    this.inputs = window.location.search.substring(1);
    this.videoURL = this.GetURLParameter("url")
    this.autotest = this.GetURLParameter("autotest")
    this.urlType  = ""
    this.message1 = ""
    this.message2 = ""
    this.init     = 0
    this.interval = 1000
    this.seekInterval = 100
    this.expectedPos    = 0
    this.expectedRate   = 0
    this.errorFlag      = 0
    this.eventFlowFlag  = 1
    this.observedEvents = []
    this.expectedEvents = []
    this.checkEvents    = []
    this.playbackSpeeds = [1, 2, 4, 16]
    this.playbackRateIndex = this.playbackSpeeds.indexOf(1)

    // Set Media Player Properties
    //this.tag('MediaPlayer').videoEl.setAttribute('crossOrigin', 'anonymous')
    this.tag('MediaPlayer').updateSettings({ consumer: this, videoPos: [150, 120, 1050, 800] })
    this.tag('MediaPlayer').videoEl.autoplay = true
    this.tag('MediaPlayer').videoEl.muted = false
    this.setVideoURL(this.videoURL)
    this.loadPlayer();
    this.tag('MediaPlayer').videoEl.style.visibility = 'visible'
    this.play();

  }

}
