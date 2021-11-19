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

import { Lightning, Utils } from '@lightningjs/sdk'
import { dispTime, logMsg, logEventMsg, GetURLParameter, getVideoOperations } from './MediaUtility.js'

let tag = null;

export default class App extends Lightning.Component {
  static getFonts() {
    return [{ family: 'Regular', url: Utils.asset('fonts/Roboto-Regular.ttf') }]
  }
  static _template() {
    return {
      TDKLogo: {
        mountX: 0.5,
        mountY: 0.5,
        x: 500,
        y: 60,
        h: 70,
        w: 200,
        src: Utils.asset('images/TDK_logo.png'),
      },
      TDKTitle: {
        mount: 0.5,
        x: 1000,
        y: 60,
        text: {
          text: "TDK Lightning UVE-Player Test App",
          fontFace: 'bold',
          fontSize: 40,
          textColor: 0xffff00ff,
        },
      },
      MsgBox1: {
        x: 100,
        y: 1000,
        w: 800,
        text: {
          fontFace: 'bold',
          fontSize: 30,
          textColor: 0xffff00ff,
        },
      },
      MsgBox2: {
        x: 1200,
        y: 1000,
        w: 500,
        text: {
          fontFace: 'bold',
          fontSize: 30,
          textColor: 0xffff00ff,
        },
      },
    }
 }


  // To display Events & Video position in UI
  dispUIMessage(msg){
      this.tag("MsgBox1").text.text = `Evt: ${msg}`;
  }
  dispUIVideoPosition(msg){
      this.tag("MsgBox2").text.text = `${msg}`;
  }

  // AAMP PlayBack Wrapper Methods
  createAAMPObject(){
      this.player = new AAMPMediaPlayer();
      logMsg("AAMP Player object created !!!")
  }

  load(url,autoplay) {
      this.url = url;
      this.player.load(url,autoplay);
      logMsg("AAMP Player loaded with video url")
  }

  initConfig(config) {
      //logMsg("Invoked initConfig with config: " + JSON.stringify(config));
      this.player.initConfig(config);
  }
  setDRMConfig(config) {
      //logMsg("Invoked initConfig with DRMconfig: " + JSON.stringify(config));
      this.player.setDRMConfig(config);
  }
  addCustomHTTPHeader(headerName, headerValue, isLicenseRequest = false) {
      console.log("AAMP: adding header: " + headerName + "| value: " + headerValue);
      this.player.addCustomHTTPHeader(headerName, headerValue, isLicenseRequest);
  }


  play() {
      this.expectedEvents = ["playing"]
      logMsg("Expected Event: " + this.expectedEvents)
      this.player.play();
  }
  pause() {
      this.expectedEvents = ["paused"]
      logMsg("Expected Event: " + this.expectedEvents)
      this.player.pause();
  }
  mute() {
      this.expectedVolume = 0
      this.volumeChangeFlag = 1
      logMsg("Expected Volume: " + this.expectedVolume)
      this.setVolume(this.expectedVolume);
      this.dispVolumeInfo()
  }
  unmute() {
      this.expectedVolume = 100
      this.volumeChangeFlag = 1
      logMsg("Expected Volume: " + this.expectedVolume)
      this.setVolume(this.expectedVolume);
      this.dispVolumeInfo()
  }
  stop() {
      this.player.stop();
  }
  playNow(){
    this.playbackRateIndex = this.playbackSpeeds.indexOf(1)
    var rate = this.playbackSpeeds[this.playbackRateIndex]
    this.setPlaybackRate(rate)
  }
  setPlaybackRate(rate, overshoot = 0) {
      this.expectedEvents = ["ratechange"]
      this.expectedRate = rate
      logMsg("Expected Rate : " + this.expectedRate)
      logMsg("Expected Event: " + this.expectedEvents)
      this.player.setPlaybackRate(rate, overshoot);
  }
  setNegPlaybackRate(rate, overshoot = 0) {
      this.expectedEvents = ["ratechange"]
      this.expectedRates = [ rate, 1 ]
      this.rewindFlag = 1
      logMsg("Expected Rates: " + this.expectedRates)
      logMsg("Expected Event: " + this.expectedEvents)
      this.player.setPlaybackRate(rate, overshoot);
  }
  seek(timeSec, keepPause = false) {
      this.player.seek(timeSec, keepPause);
  }
  seekfwd(pos){
      this.expectedEvents   = ["seeking","seeked"]
      this.expectedPos = Math.floor(this.getCurrentPosition() + pos )
      logMsg("Expected Event: "   + this.expectedEvents)
      logMsg("Expected Pos  : [ " + this.expectedPos + " - " + (this.expectedPos + 7) + " ]")
      this.seek(this.expectedPos)
  }
  seekbwd(pos){
      this.expectedEvents   = ["seeking","seeked"]
      this.expectedPos = Math.floor(this.getCurrentPosition() - pos )
      logMsg("Expected Event: "   + this.expectedEvents)
      logMsg("Expected Pos  : [ " + this.expectedPos + " - " + (this.expectedPos + 7) + " ]")
      this.seek(this.expectedPos)
  }
  getPlaybackRate() {
     return this.player.getPlaybackRate();
  }
  getCurrentState() {
      return this.player.getCurrentState();
  }

  getDurationSec() {
      return this.player.getDurationSec();
  }

  getCurrentPosition() {
      return this.player.getCurrentPosition();
  }
  setVideoRect(x, y, w, h) {
      this.player.setVideoRect(x, y, w, h);
  }
  getVideoRectangle() {
     return this.player.getVideoRectangle();
  }
  getAvailableAudioTracks() {
     return this.player.getAvailableAudioTracks();
  }
  getAudioTrack() {
      return this.player.getAudioTrack();
  }
  setAudioTrack(track) {
      this.player.setAudioTrack(track);
  }
  getVolume(){
      return this.player.getVolume()
  }
  setVolume(volume){
      this.player.setVolume(volume)
  }


  // AAMP Event Listerner and Handlers
  addEventListener(eventName, eventHandler) {
     this.player.addEventListener(eventName, eventHandler, null);
     //logMsg("event:"+eventName+" handler registered");
  }
  eventplaybackStarted(){
      // Able to get position info only after a pause.
      tag.player.pause();
      tag.player.play();
      tag.handlePlayerEvents("Video PlayBack Started");
  }
  eventplaybackProgressUpdate(event){
    //logMsg("PlayBack progress update event: " + JSON.stringify(event))
    var duration = (event.endMiliseconds / 1000.0);
    var position = (event.positionMiliseconds / 1000.0);
    if ( tag.init == 0 ){
          var dur = tag.getDurationSec();
          tag.vidDuration = dur.toFixed(2)
          logMsg("******************* VIDEO STARTED PLAYING !!! *******************")
          logMsg("VIDEO AUTOPLAY: " + tag.autoplay)
          logMsg("VIDEO DURATION: " + tag.vidDuration)
          //logMsg("Available Audio tracks: " + tag.getAvailableAudioTracks())
          //logMsg("Current Audio track: " + tag.getAudioTrack())
          tag.checkAndStartAutoTesting()
          tag.init = 1 //inited
          /*tag.progressLogger = setInterval(()=>{
              tag.dispProgressLog()
          },1000);*/
    }
    tag.message2 = "Pos: " + position.toFixed(2) + "/" + duration.toFixed(2)
    tag.dispUIVideoPosition(tag.message2)
    tag.progressEventMsg = "Video Progressing "  + position.toFixed(2) + "/" + duration.toFixed(2)
    logMsg(tag.progressEventMsg)
  }
  eventplaybackStateChanged(event){
    //logMsg("PlayBack state change event: " + JSON.stringify(event))
    switch (event.state) {
        case tag.playerStates.Idle:
            tag.handlePlayerEvents("Video Player Idle")
            break;
        case tag.playerStates.Initializing:
            tag.handlePlayerEvents("Video Player Initializing")
            break;
        case tag.playerStates.Initialized:
            tag.handlePlayerEvents("Video Player Initialized")
            break;
        case tag.playerStates.Error:
            tag.errorFlag = 1
            tag.handlePlayerEvents("Video Player Error")
            break;
        case tag.playerStates.Playing:
            tag.observedEvents.push("playing")
            tag.checkAndLogEvents("playing","Video Player Playing")
            break;
        case tag.playerStates.Paused:
            tag.observedEvents.push("paused")
            tag.checkAndLogEvents("paused","Video Player Paused")
            break;
        case tag.playerStates.Seeking:
            tag.observedEvents.push("seeking")
            tag.checkAndLogEvents("seeking","Video Player Seeking")
            break;
        default:
            tag.handlePlayerStates(event.state);
            break;
    }
  }
  eventplaybackRateChanged(event) {
    tag.observedEvents.push("ratechange")
    if (tag.rewindFlag == 1){
        tag.observedRates.push(event.speed);
    }
    tag.observedRate = event.speed;
    var rate_info = "Video Player Rate Change to " + tag.observedRate
    tag.checkAndLogEvents("ratechange",rate_info);
  }
  eventplaybackCompleted(){
    tag.observedEvents.push("ended")
    tag.handlePlayerEvents("Video PlayBack Completed")
  }
  eventplaybackFailed(){
    tag.errorFlag = 1
    tag.handlePlayerEvents("Video PlayBack Failed")
  }
  eventplaybackSeeked(event){
      tag.observedEvents.push("seeked")
      tag.observedPos = Math.round(event.position / 1000);
      var dur = tag.getDurationSec()
      var seek_info = "Video Player Seeked " + tag.observedPos + "/" + dur.toFixed(2)
      tag.checkAndLogEvents("seeked",seek_info);
  }
  handlePlayerStates(id){
    if (this.playerStateIDs.includes(id)){
       for (var state in this.playerStates){
         if (this.playerStates[state] == id){
            this.handlePlayerEvents("Video Player " + state);
            break;
         }
      }
    }else{
        logMsg("Player State not expected")
    }
  }
  handlePlayerEvents(eventMsg){
      this.message1 = eventMsg
      this.dispUIMessage(this.message1)
      logMsg(this.message1 + " !!!")
  }
  setExpPlayBackEvents(){
    this.expectedEvents = ["ended"]
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Observed Event: " + this.observedEvents)
  }
  dispVolumeInfo(){
    this.message1 = "Video Player Volume Change, volume: " + this.getVolume()
    this.dispUIMessage(this.message1)
    console.log("*****************************************************************\n" +
	        "[ " + dispTime() + " ] " + this.message1 + "\n" +
                "*****************************************************************")
  }


  // Creating AAMp Object, registering events & loading URL
  loadAAMPPlayer(){
    this.createAAMPObject();
    this.setPlayerConfig();
    this.registerEvents();
    this.load(this.videoURL,this.autoplay);
  }
  setPlayerConfig(){
     let defaultInitConfig = {
            initialBitrate: 2500000,
            offset: 0,
            networkTimeout: 10,
            preferredAudioLanguage: "en",
            liveOffset: 15,
            progressReportingInterval:1,
            drmConfig: {}
     };
     //var defaultInitConfig = {progressReportingInterval:1};
     this.initConfig(defaultInitConfig);
     if (Object.keys(this.DRMconfig).length != 0){
         this.setDRMConfig(this.DRMconfig);
         if(this.license_header != ""){
             var header_tag = this.license_header.split(":")[0];
             var header_val = this.license_header.split(":")[1];
             this.addCustomHTTPHeader(header_tag,header_val)
         }
     }

  }
  registerEvents(){
    this.addEventListener("playbackStarted",this.eventplaybackStarted)
    this.addEventListener("playbackProgressUpdate",this.eventplaybackProgressUpdate)
    this.addEventListener("playbackStateChanged",this.eventplaybackStateChanged)
    this.addEventListener("playbackCompleted",this.eventplaybackCompleted)
    this.addEventListener("playbackSpeedChanged",this.eventplaybackRateChanged)
    this.addEventListener("playbackFailed",this.eventplaybackFailed)
    this.addEventListener("seeked", this.eventplaybackSeeked)
    logMsg("Event listeners added successfully...")
  }

  // Method to start the auto-testing by setting video operations
  checkAndStartAutoTesting(){
    if (this.autotest == "true")
    {
      var operationsStr = GetURLParameter("operations")
      var operations = getVideoOperations(operationsStr)
      logMsg("********************** STARTING AUTO TEST ***********************")
      this.performOperations(operations)
    }else{
      logMsg("***************** PRESS KEYS TO DO OPERATIONS ********************")
    }
  }

  performOperations(operations){
      var actionInterval = 0
      var duration = 0, position = 0
      logMsg("Setting up the operations...")
      for (var i = 0; i < operations.length; i++)
      {
          var action = operations[i].split('(')[0];
          if ( action == "seekpos" ){
              duration = parseInt(operations[i].split('(')[1].split(')')[0].split(":")[0]);
              position = parseInt(operations[i].split('(')[1].split(')')[0].split(":")[1]);
          }else{
              duration = parseInt(operations[i].split('(')[1].split(')')[0]);
          }
          if ( action == "playtillend" )
              actionInterval = actionInterval + (this.interval*parseInt(this.vidDuration)) + 60000;
          else
              actionInterval = actionInterval + (this.interval*duration)
          //logMsg("setting " + action + " at " + actionInterval + " th sec")
            if (action == "pause"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.pause()
                },actionInterval);
            }
            else if (action == "play"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.play()
                },actionInterval);
            }
            else if (action == "playtillend"){
                setTimeout(()=> {
                    this.setExpPlayBackEvents()
                },actionInterval);
            }
            else if (action == "playnow"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.playNow()
                },actionInterval);
            }
            else if (action == "mute"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.mute()
                },actionInterval);
            }
            else if (action == "unmute"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.unmute()
                },actionInterval);
            }
	    else if (action == "seekfwd"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.seekfwd(this.seekInterval)
                },actionInterval);
            }
	    else if (action == "seekbwd"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.seekbwd(this.seekInterval)
                },actionInterval);
            }
            else if (action == "fastfwd4x" || action == "fastfwd16x" || action == "fastfwd32x"){
                if (action == "fastfwd32x"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.setPlaybackRate(32)
                },actionInterval);
                }else if (action == "fastfwd4x"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.setPlaybackRate(4)
                },actionInterval);
                }else if (action == "fastfwd16x"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.setPlaybackRate(16)
                },actionInterval);
                }
            }
            else if (action == "rewind4x" || action == "rewind16x" || action == "rewind32x"){
                if (action == "rewind32x"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.setNegPlaybackRate(-32)
                },actionInterval);
                }else if (action == "rewind4x"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.setNegPlaybackRate(-4)
                },actionInterval);
                }else if (action == "rewind16x"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.setNegPlaybackRate(-16)
                },actionInterval);
                }
            }
            else if (action == "close"){
                setTimeout(()=> {
                    logMsg("**************** Going to close ****************")
                    this.stop()
                },actionInterval);
            }
            if (action != "close"){
                setTimeout(()=> {
                    this.updateEventFlowFlag();
                },actionInterval+this.checkInterval);
            }
      }
      if (! operations.find(o=> o.includes("close"))){
          setTimeout(()=> {
            logMsg("**************** Going to close ****************")
            this.stop()
          },(actionInterval+10000));
      }
      setTimeout(()=> {
        this.dispTestResult()
      },(actionInterval+15000));
      console.log("\n");
  }



  clearEvents(){
      this.observedEvents = []
      this.expectedEvents = []
  }
  checkAndLogEvents(checkevent,msg){
    if ( this.expectedEvents.includes(checkevent) ){
        this.message1 = msg
        this.dispUIMessage(this.message1)
        logEventMsg(this.observedEvents,msg)
    }else{
        this.handlePlayerEvents(msg)
    }
  }
  updateEventFlowFlag(){
      var Status = "SUCCESS"
      if( ! this.expectedEvents.every(e=> this.observedEvents.indexOf(e) >= 0)){
	  if (this.volumeChangeFlag == 1){
              this.volumeChangeFlag = 0
              var currVolume = parseInt(this.getVolume())
              if( currVolume == this.expectedVolume ){
                logMsg("volume change  operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("volume change  operation failure")
              }
          }
	  else{
              this.eventFlowFlag = 0
              Status = "FAILURE"
	  }
      } else{
          if (this.expectedEvents.includes("paused")){
              var currState = this.getCurrentState();
              if (currState == this.playerStates.Paused){
                logMsg("video pause operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video pause operation failure")
              }
          }
          else if(this.expectedEvents.includes("seeked")){
              var currTime = parseInt(this.observedPos)
              //var currTime = parseInt(this.getCurrentPosition())
	      var expTime  = parseInt(this.expectedPos)
              if( currTime >= expTime && currTime <= (expTime+7) ){
                logMsg("video seek operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video seek operation failure")
              }
          }
          else if(this.expectedEvents.includes("playing")){
              var currState = this.getCurrentState();
              if (currState == this.playerStates.Playing){
                logMsg("video play operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video play operation failure")
              }
          }
          else if(this.expectedEvents.includes("ratechange")){
              if (this.rewindFlag == 1 ){
                  this.rewindFlag = 0;
                  if( ! this.expectedRates.every(e=> this.observedRates.indexOf(e) >= 0)){
                    this.eventFlowFlag = 0
                    Status = "FAILURE"
                    logMsg("video rate change operation failure")
                  }else{
                    logMsg("video rate change operation success")
                  }
              }else{
                  var currRate = parseInt(this.observedRate)
                  //logMsg("Observed Rate : " + currRate)
                  if( currRate == this.expectedRate && currRate == parseInt(this.getPlaybackRate())){
                    logMsg("video rate change operation success")
                  }else{
                    this.eventFlowFlag = 0
                    Status = "FAILURE"
                    logMsg("video rate change operation failure")
                  }
             }   
          }
      }
      logMsg("Test step status: " + Status)
  }
  dispTestResult(){
    clearInterval(this.progressLogger);
    if (this.eventFlowFlag == 1 && this.errorFlag == 0)
        logMsg("TEST RESULT: SUCCESS")
    else{
        logMsg("eventFlowFlag: " + this.eventFlowFlag + " errorFlag: " + this.errorFlag)
        logMsg("TEST RESULT: FAILURE")
    }
  }
  dispProgressLog(){
    var duration = this.getDurationSec();
    var position = this.getCurrentPosition();
    tag.message2 = "Pos: " + position.toFixed(2) + "/" + duration.toFixed(2)
    tag.dispUIVideoPosition(tag.message2)
    tag.progressEventMsg = "Video Progressing "  + position.toFixed(2) + "/" + duration.toFixed(2)
    logMsg(this.progressEventMsg)
  }


 _init() {
    this.inputs = window.location.search.substring(1).split("&");
    this.videoURL = GetURLParameter("url").replace(/:and:/g,"&").replace(/:eq:/g, "=")
    this.autotest = GetURLParameter("autotest")
    this.autoplay = true
    this.options  = []
    this.configs  = []
    this.DRMconfig= {}
    this.message1 = ""
    this.message2 = ""
    this.player   = null;
    this.init     = 0
    this.interval = 1000
    this.checkInterval= 3000
    this.seekInterval = 10
    this.expectedPos    = 0
    this.observedPos    = 0
    this.expectedRate   = 0
    this.observedRate   = 0
    this.expectedRates  = []
    this.observedRates  = []
    this.vidDuration    = 0
    this.rewindFlag     = 0
    this.errorFlag      = 0
    this.eventFlowFlag  = 1
    this.observedEvents = []
    this.expectedEvents = []
    this.expectedVolume = 0
    this.volumeChangeFlag  = 0
    this.progressEventMsg  = ""
    this.progressLogger    = null
    this.playbackSpeeds = [-64, -32, -16, -4, 1, 4, 16, 32, 64];
    this.playbackRateIndex = this.playbackSpeeds.indexOf(1)
    logMsg("URL Info: " + this.videoURL )

    tag = this;
    this.playerStates= { "Idle":0, "Initializing":1, "Initialized":2, "Preparing":3, "Prepared":4,
                         "Buffering":5, "Paused":6, "Seeking":7 , "Playing":8, "Stopping":9,
                         "Stopped":10, "Complete":11, "Error":12, "Released":13 };
    this.playerStateIDs = Object.values(this.playerStates)


    this.inputs.forEach(item => {
        if(item.split("=")[0] == "drmconfigs"){
            this.configs = GetURLParameter("drmconfigs").split(",");
        }
        else if(item.split("=")[0] == "options"){
            this.options = GetURLParameter("options").split(",");
        }
    });
    this.options.forEach(item => {
	if(item.includes("seekInterval")){
         this.seekInterval = parseInt(item.split('(')[1].split(')')[0]);
        }
        else if(item.includes("checkInterval")){
         this.checkInterval = parseInt(item.split('(')[1].split(')')[0])*1000;
       }
     });
    // check the DRM options provided in the url and update the configs
    this.license_header = "";
    this.preferredDRM   = "";
    this.configs.forEach(item => {
      if(item.includes("headers")){
          this.license_header = String(item.split('(')[1].split(')')[0]);
      }
      else if(item.includes("headers")){
          this.preferredDRM = String(item.split('(')[1].split(')')[0]);
          this.DRMconfig["preferredKeysystem"] = this.preferredDRM;
      }
      else{
          var drm = String(item.split('(')[0]);
          var license_url = String(item.split('(')[1].split(')')[0]);
          license_url = license_url.replace(/:and:/g,"&").replace(/:eq:/g, "=").replace(/:ob:/g,"(").replace(/:cb:/g,")").replace(/:comma:/g,",");
          this.DRMconfig[drm] = license_url;
      }
    });

    this.loadAAMPPlayer();
  }

}



