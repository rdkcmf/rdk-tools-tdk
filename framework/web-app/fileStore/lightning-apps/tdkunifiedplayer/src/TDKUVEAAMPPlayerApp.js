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
import { dispTime, logMsg, logEventMsg, logActionMsg, GetURLParameter, getVideoOperations, getRandomInt, getPosValResult } from './MediaUtility.js'
import { RDKServicesInterface }  from './RDKServicesUtility';

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
      RDKServices : { type: RDKServicesInterface }
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
      logMsg("AAMP Player loaded with video url: " + url)
  }

  initConfig(config) {
      //logMsg("Invoked initConfig with config: " + JSON.stringify(config));
      this.player.initConfig(config);
  }
  setDRMConfig(config) {
      //logMsg("Invoked initConfig with DRMconfig: " + JSON.stringify(config));
      this.player.setDRMConfig(config);
  }
  addCustomHTTPHeader(headerName, headerValue, isLicenseRequest = true) {
      logMsg("AAMP: adding header: " + headerName + "| value: " + headerValue);
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
      this.pos_zero_index_flag = 1
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
  reload() {
      logMsg("Loading Player with new stream...")
      //this.player.detach();
      this.videoURL = this.secondaryURL;
      this.expectedEvents = ["playing"]
      logMsg("Expected Event: " + this.expectedEvents)
      this.load(this.videoURL,this.autoplay);
  }
  playNow(){
    this.playbackRateIndex = this.playbackSpeeds.indexOf(1)
    var rate = this.playbackSpeeds[this.playbackRateIndex]
    this.setPlaybackRate(rate)
  }
  setPlaybackRate(rate, overshoot = 0) {
      this.expectedEvents = ["ratechange"]
      this.expectedRate = rate
      this.observedRates = []
      logMsg("Expected Rate : " + this.expectedRate)
      logMsg("Expected Event: " + this.expectedEvents)
      this.player.setPlaybackRate(rate, overshoot);
  }
  setNegPlaybackRate(rate, overshoot = 0) {
      this.expectedEvents = ["ratechange"]
      this.expectedRates = [ rate, 1 ]
      this.observedRates = []
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
      logMsg("Expected Pos  : [ " + (this.expectedPos - 2) + " - " + (this.expectedPos + 7) + " ]")
      this.seek(this.expectedPos)
  }
  seekbwd(pos){
      this.expectedEvents   = ["seeking","seeked"]
      this.expectedPos = Math.floor(this.getCurrentPosition() - pos )
      logMsg("Expected Event: "   + this.expectedEvents)
      logMsg("Expected Pos  : [ " + (this.expectedPos - 2) + " - " + (this.expectedPos + 7) + " ]")
      this.seek(this.expectedPos)
  }
  getAudioLanguages(){
      var audioTracks = []
      logMsg("Available Audio tracks: " + this.getAvailableAudioTracks())
      audioTracks = JSON.parse(this.getAvailableAudioTracks())
      for (var i = 0; i < audioTracks.length; i++){
          if(audioTracks[i].language != ""){
              this.audioIndexes.push(i);
              this.audioLanguages.push(audioTracks[i].language)
              this.audioLanguagesSelected.push(audioTracks[i].language)
          }else{
              this.errorFlag = 1
              logMsg("[ERROR]:Audio Track language is empty")
          }
      }
      this.actualAudioIndex = this.getAudioTrack()
      logMsg("Audio Languages: "  + this.audioLanguages)
      logMsg("Current Audio Index: " + this.actualAudioIndex)
      if(this.actualAudioIndex < 0){
          this.errorFlag = 1
          logMsg("[ERROR]: Audio language index obtained is invalid")
      }
      if(this.audioLanguages.length){
          logMsg("Current Audio Language: " + this.audioLanguages[this.actualAudioIndex])
          this.audioIndexes.splice(this.actualAudioIndex,1)
          this.audioLanguagesSelected.splice(this.actualAudioIndex,1)
          logMsg("Audio list excluding current language: " + this.audioLanguagesSelected)
      }else{
          this.audioTracksAvailability = 0
          logMsg("[ERROR]: Cannot perform Audio Track change operation")
      }
  }
  changeAudio(){
      this.getAudioLanguages();
      if(this.audioTracksAvailability){
          var index = parseInt(getRandomInt(this.audioLanguagesSelected.length))
          var language = this.audioLanguagesSelected[index]
          this.expectedAudioIndex = this.audioIndexes[index]
          logMsg("Changing audio language to: "+ language)
          logMsg("Expected Audio Track language:" + language)
          logMsg("Expected Audio Track index: " + this.expectedAudioIndex)
          //this.setAudioLanguage(language)
          this.audioChangeFlag = 1
          this.setAudioTrack(this.expectedAudioIndex)
      }
  }
  getTextTracks(){
      var textTracks = []
      logMsg("Available Text tracks: " + this.getAvailableTextTracks())
      textTracks = JSON.parse(this.getAvailableTextTracks())
      for (var i = 0; i < textTracks.length; i++){
          if(textTracks[i].language != ""){
              this.textIndexes.push(i);
              this.textLanguages.push(textTracks[i].language)
              this.textLanguagesSelected.push(textTracks[i].language)
          }else{
              this.errorFlag = 1
              logMsg("[ERROR]:Text Track language is empty")
          }
      }
      this.actualTextIndex = this.getTextTrack()
      logMsg("Text Tracks: "  + this.textLanguages)
      logMsg("Current Text Index: " + this.actualTextIndex)
      if(this.actualTextIndex < 0){
          this.errorFlag = 1
          logMsg("[ERROR]: Text Track index obtained is invalid")
      }
      if(this.textLanguages.length){
          logMsg("Current Text Language: " + this.textLanguages[this.actualTextIndex])
          this.textIndexes.splice(this.actualTextIndex,1)
          this.textLanguagesSelected.splice(this.actualTextIndex,1)
          logMsg("Text list excluding current language: " + this.textLanguagesSelected)
      }else{
          this.textTracksAvailability = 0
          logMsg("[ERROR]: Cannot perform Text Track change operation")
      }
  }
  changeText(){
      this.getTextTracks();
      if(this.textTracksAvailability){
          var index = parseInt(getRandomInt(this.textLanguagesSelected.length))
          var language = this.textLanguagesSelected[index]
          this.expectedTextIndex = this.textIndexes[index]
          logMsg("Changing text language to: "+ language)
          logMsg("Expected Text Track language:" + language)
          logMsg("Expected Text Track index: " + this.expectedTextIndex)
          this.textChangeFlag = 1
          this.setTextTrack(this.expectedTextIndex)
      }
  }
  getVideoBitRates(){
      var videoBitrates = []
      var currentBitrate = 0
      logMsg("Available Video bitrates: " + this.getVideoBitrates())
      videoBitrates = this.getVideoBitrates()
      if (videoBitrates.length != 0){
          currentBitrate = this.getCurrentVideoBitrate()
          logMsg("Current Video bitrate: " + currentBitrate)
	  if (currentBitrate != "" && currentBitrate > 0){
	      for (var i = 0;i < videoBitrates.length; i++){
	         if (videoBitrates[i] != currentBitrate)
	            this.videoBitratesSelected.push(videoBitrates[i])
	      }
	      if(this.videoBitratesSelected.length)
	          logMsg("Video bitrates excluding current bit rate " + this.videoBitratesSelected)
	      else{
		  this.videoBitratesAvailability = 0
		  logMsg("[ERROR]:Video bitrates list excluding current bitrate is empty")
	      }   
          }else{
	      this.videoBitratesAvailability  = 0
              logMsg("[ERROR]:Current Video bitrate is not valid")
          }
       }else{
           this.videoBitratesAvailability = 0
           logMsg("[ERROR]:Available Video bitrates list is empty")
       }
  }
  changeVideoBitrate(){
      this.getVideoBitRates()
      if(this.videoBitratesAvailability){
          this.stop()
	  var index = parseInt(getRandomInt(this.videoBitratesSelected.length))
	  this.expectedVideoBitrate = this.videoBitratesSelected[index]
	  logMsg("Changing bit rate to: "+ this.expectedVideoBitrate)
	  this.VideoBitrateChangeFlag = 1
	  this.loadAAMPPlayer();
	  this.setVideoBitrate(this.expectedVideoBitrate)
      }
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
  setAudioLanguage(language){
      this.player.setAudioLanguage(language)
  }
  getAudioTrack() {
      return this.player.getAudioTrack();
  }
  setAudioTrack(track) {
      this.player.setAudioTrack(track);
  }
  getAvailableTextTracks(){
      return this.player.getAvailableTextTracks()
  }
  getTextTrack() {
      return this.player.getTextTrack();
  }
  setTextTrack(track) {
      this.player.setTextTrack(track);
  }
  setClosedCaptionStatus(enable){
      logMsg("Setting the Closed Caption Status: " + enable)
      this.player.setClosedCaptionStatus(enable)
      //this.setTextTrack(0)
  }
  getVolume(){
      return this.player.getVolume()
  }
  setVolume(volume){
      this.player.setVolume(volume)
  }
  getVideoBitrates() {
     return this.player.getVideoBitrates();
  }
  getCurrentVideoBitrate() {
      return this.player.getCurrentVideoBitrate();
  }
  setVideoBitrate(bitrate) {
      this.player.setVideoBitrate(bitrate);
  }

  // AAMP Event Listerner and Handlers
  addEventListener(eventName, eventHandler) {
     this.player.addEventListener(eventName, eventHandler, null);
     //logMsg("event:"+eventName+" handler registered");
  }
  eventplaybackStarted(){
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
          if (tag.enableCCStatus == "true"){
              tag.setClosedCaptionStatus(true)
          }
          tag.checkAndStartAutoTesting()
          tag.init = 1 //inited
          // Enable video progress position validation after playing event
          tag.pos_val_flag = 1;
          /*tag.progressLogger = setInterval(()=>{
              tag.dispProgressLog()
          },1000);*/
    }
    tag.message2 = "Pos: " + position.toFixed(2) + "/" + duration.toFixed(2)
    tag.dispUIVideoPosition(tag.message2)
    tag.progressEventMsg = "Video Progressing "  + position.toFixed(2) + "/" + duration.toFixed(2)
    logMsg(tag.progressEventMsg)
    if(tag.pos_val_flag == 1){
          var pos = tag.progressEventMsg.split("Video Progressing")[1].trim().split("/")[0]
          tag.pos_list.push(pos)
    }
    // Get the FPS data only when collect fps option is enabled
    if(tag.enable_fps_flag == 1){
        tag.tag("RDKServices").getDiagnosticsInfo();
    }
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
            // Enable video progress pos validation with pos diff 1
            tag.updatePosValidationInfo(1)
            break;
        case tag.playerStates.Paused:
            tag.observedEvents.push("paused")
            tag.checkAndLogEvents("paused","Video Player Paused")
            // Enable video progress pos validation with pos diff 0
            if(tag.pos_zero_index_flag){
              tag.pos_zero_index_flag = 0
              tag.updatePosValidationInfo(0)
            }
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
    //if (tag.rewindFlag == 1){
    tag.observedRates.push(event.speed);
    //}
    tag.observedRate = event.speed;
    var rate_info = "Video Player Rate Change to " + tag.observedRate
    tag.checkAndLogEvents("ratechange",rate_info);
    if (event.speed > 0 ){
        // Enable video progress pos validation with pos diff rate
        // using same rate for 1x,2x,4x
	var rate_index = event.speed
        // providing some buffer for 16x
        if (event.speed == 16)
            rate_index = 10
        tag.updatePosValidationInfo(rate_index)
    }
  }
  eventplaybackCompleted(){
    tag.observedEvents.push("ended")
    tag.handlePlayerEvents("Video PlayBack Completed")
  }
  eventplaybackFailed(event){
    tag.errorFlag = 1
    logMsg("Event Occurred: playbackFailed !!!")
    logMsg("desc : "+ event.description + " code: "+ event.code)
    tag.handlePlayerEvents("Video PlayBack Failed")
  }
  eventplaybackSeeked(event){
      tag.observedEvents.push("seeked")
      tag.observedPos = Math.round(event.position / 1000);
      var dur = tag.getDurationSec()
      var seek_info = "Video Player Seeked " + tag.observedPos + "/" + dur.toFixed(2)
      tag.checkAndLogEvents("seeked",seek_info);
      // Enable video progress pos validation with pos diff 1
      tag.updatePosValidationInfo(1)
  }
  eventbitrateChanged(event) {
    tag.observedEvents.push("bitratechange")
    tag.observedBitrate = event.bitRate;
    var bitrate_info = "Video Player BitRate Change to " + tag.observedBitrate
    tag.checkAndLogEvents("bitratechange",bitrate_info);
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
    logActionMsg(this.message1)
    // Enable video progress pos validation with pos diff 1
    this.updatePosValidationInfo(1)
  }
  dispAudioInfo(){
    this.message1 = "Observed Audio Track Index: " + this.getAudioTrack()
    this.dispUIMessage(this.message1)
    logActionMsg(this.message1)
    // Enable video progress pos validation with pos diff 1
    this.updatePosValidationInfo(1)
  }
  dispTextInfo(){
    this.message1 = "Observed Text Track Index: " + this.getTextTrack()
    this.dispUIMessage(this.message1)
    logActionMsg(this.message1)
    // Enable video progress pos validation with pos diff 1
    this.updatePosValidationInfo(1)
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
    this.addEventListener("bitrateChanged",this.eventbitrateChanged)
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
	    else if (action == "changeurl"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.reload();
                },actionInterval);
            }
	    else if (action == "changeaudio"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.changeAudio();
                },actionInterval);
            }
	    else if (action == "changetext"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.changeText();
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
	    else if (action == "changevideobitrate"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.changeVideoBitrate();
                },actionInterval);
            }
            else if (action == "close"){
                setTimeout(()=> {
                    this.updatePrevPosValidationResult()
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
            this.updatePrevPosValidationResult()
            logMsg("**************** Going to close ****************")
            this.stop()
          },(actionInterval+10000));
      }
      setTimeout(()=> {
        this.dispTestResult()
      },(actionInterval+15000));
      //console.log("\n");
  }



  clearEvents(){
      this.observedEvents = []
      this.expectedEvents = []
      this.updatePrevPosValidationResult()
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
          this.eventFlowFlag = 0
          Status = "FAILURE"
          logMsg("Failure Reason: Expected events not occurred")
      } else{
          if (this.expectedEvents.includes("paused")){
              var currState = this.getCurrentState();
              if (currState == this.playerStates.Paused){
                logMsg("video pause operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video pause operation failure")
                logMsg("Failure Reason: Current player state is not paused")
              }
          }
          else if(this.expectedEvents.includes("seeked")){
              var currTime = parseInt(this.observedPos)
	      var expTime  = parseInt(this.expectedPos)
              if( currTime >= (expTime-2) && currTime <= (expTime+7) ){
                logMsg("video seek operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video seek operation failure")
                logMsg("Failure Reason: Seeked pos is not within expected range")
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
                logMsg("Failure Reason: Current player state is not playing")
              }
          }
          else if(this.expectedEvents.includes("ratechange")){
              if (this.rewindFlag == 1 ){
                  this.rewindFlag = 0;
                  if( ! this.expectedRates.every(e=> this.observedRates.indexOf(e) >= 0)){
                    this.eventFlowFlag = 0
                    Status = "FAILURE"
                    logMsg("video rate change operation failure")
                    logMsg("Failure Reason: Playback rate is not as expected")
                  }else{
                    logMsg("video rate change operation success")
                  }
              }else{
                  if( this.observedRates.includes(this.expectedRate)){
                    logMsg("video rate change operation success")
                  }else{
                    this.eventFlowFlag = 0
                    Status = "FAILURE"
                    logMsg("video rate change operation failure")
                    logMsg("Failure Reason: Playback rate is not as expected")
                  }
             }
          }
	  else if (this.volumeChangeFlag == 1){
              this.volumeChangeFlag = 0
              var currVolume = parseInt(this.getVolume())
              if( currVolume == this.expectedVolume ){
                logMsg("volume change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("volume change operation failure")
                logMsg("Failure Reason: Current volume level is not as expected")
              }
          }
	  else if (this.audioChangeFlag == 1){
              this.audioChangeFlag = 0
              this.dispAudioInfo()
              var currAudioIndex = this.getAudioTrack()
              if( currAudioIndex == this.expectedAudioIndex ){
                logMsg("Audio language change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("Audio language change operation failure")
                logMsg("Failure Reason: Current Audio track index is not as expected")
              }
          }
          else if (this.textChangeFlag == 1){
              this.textChangeFlag = 0
              this.dispTextInfo()
              var currTextIndex = this.getTextTrack()
              if( currTextIndex == this.expectedTextIndex ){
                logMsg("Text Track change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("Text Track change operation failure")
                logMsg("Failure Reason: Current Text track index is not as expected")
              }
          }
          else if (this.audioTracksAvailability == 0 || this.textTracksAvailability == 0){
              Status = "FAILURE"
              logMsg("Failure Reason: Audio/Text tracks list empty")
          }
          else if (this.VideoBitrateChangeFlag == 1){
              this.VideoBitrateChangeFlag = 0
              var currVideoBitrate = this.getCurrentVideoBitrate()
              if( currVideoBitrate == this.expectedVideoBitrate){
                logMsg(" Video bitrate change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("Video bitrate  change operation failure")
                logMsg("Failure Reason: Current Video bitrate is not as expected")                
              }
          }
	  else if (this.videoBitratesAvailability == 0){
	      Status = "FAILURE"
              logMsg("Failure Reason: Unable to select new video bitrate")
          }
      }
      logMsg("Test step status: " + Status)
  }

  updatePosValidationInfo(index){
      if (!this.pos_val_flag){
          this.pos_val_flag  = 1
          this.pos_val_index = index
          logMsg("Video pos index set as "+this.pos_val_index+", Capturing video progress pos values ...");
      }
  }

  updatePrevPosValidationResult(){
      this.pos_val_flag = 0
      this.pos_val_result.push(getPosValResult(this.pos_list,this.pos_val_index))
      this.pos_list = [];
  }

  updateRDKServicesInterface(){
    // Required device IP and Port to communicate with
    // RDK services plugins using ThunderJS
    this.deviceconfig = {
        host: this.deviceIP,
        port: this.devicePort
    };
    this.settings = {
        consumer:this,
        webkitinstance:this.webkitInstance
    };
    this.tag("RDKServices").updateSettings(this.deviceconfig,this.settings);
    this.tag("RDKServices").rdkservicesInterfaceInit();
  }

  dispTestResult(){
    clearInterval(this.progressLogger);
    // Check the average FPS if collect fps option is enabled
    if(this.enable_fps_flag == 1){
        var avgFPS = this.tag("RDKServices").getAverageDiagnosticsInfo()
        if ( Math.round(avgFPS) >= this.expectedFPS )
	    logMsg("Average FPS >= " + this.expectedFPS)
	else{
            this.errorFlag = 1
	    logMsg("Failure Reason: Average FPS < " + this.expectedFPS)
	}
    }
    // diaplay error, events & pos validation results
    logMsg("**************** TEST STATUS ****************")
    if (this.errorFlag == 0)
        logMsg("OVERALL VIDEO PLAYBACK ERROR EVENT STATUS : FALSE")
    else
        logMsg("OVERALL VIDEO PLAYBACK ERROR EVENT STATUS : TRUE")

    var overall_pos_val_status = 1
    if (this.pos_val_result.includes("FAILURE")){
        overall_pos_val_status = 0
        logMsg("OVERALL VIDEO PROGRESS POSITION VALIDATION STATUS : FAILURE")
    }else
        logMsg("OVERALL VIDEO PROGRESS POSITION VALIDATION STATUS : SUCCESS")

    if (this.eventFlowFlag == 1)
        logMsg("OVERALL VIDEO OPERATIONS EVENTS VALIDATION STATUS : SUCCESS")
    else
        logMsg("OVERALL VIDEO OPERATIONS EVENTS VALIDATION STATUS : FAILURE")

    //Generate TEST RESULT based on error, events & pos validation results
    if (this.eventFlowFlag == 1 && this.errorFlag == 0 && overall_pos_val_status == 1)
        logMsg("TEST RESULT: SUCCESS")
    else{
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
    this.secondaryURL = "";
    this.enableCCStatus = false;
    this.audioChangeFlag  = 0
    this.actualAudioIndex = 0;
    this.expectedAudioIndex = 0;
    this.audioIndexes   = []
    this.audioLanguages = []
    this.audioLanguagesSelected = []
    this.audioTracksAvailability = 1
    this.textChangeFlag  = 0
    this.actualTextIndex = 0;
    this.expectedTextIndex = 0;
    this.textIndexes   = []
    this.textLanguages = []
    this.textLanguagesSelected = []
    this.textTracksAvailability = 1
    this.pos_val_flag   = 0
    this.pos_val_index  = 1
    this.pos_list       = []
    this.pos_val_result = []
    this.pos_zero_index_flag = 0
    // Using device local host IP
    this.deviceIP        = "127.0.0.1"
    this.devicePort      = 0
    this.expectedFPS     = 0
    this.webkitInstance  = null
    this.enable_fps_flag = 0
    this.videoBitrates = []
    this.videoBitratesSelected= []
    this.expectedVideoBitrate= 0
    this.videoBitratesAvailability = 1
    this.VideoBitrateChangeFlag = 0
    logMsg("URL Info: " + this.videoURL )

    tag = this;
    this.playerStates= { "Idle":0, "Initializing":1, "Initialized":2, "Preparing":3, "Prepared":4,
                         "Buffering":5, "Paused":6, "Seeking":7 , "Playing":8, "Stopping":9,
                         "Stopped":10, "Complete":11, "Error":12, "Released":13 };
    this.playerStateIDs = Object.values(this.playerStates)


    this.inputs.forEach(item => {
        if(item.split("=")[0] == "drmconfigs"){
            var drm_configs = GetURLParameter("drmconfigs")
            if (drm_configs != ""){
                this.configs = GetURLParameter("drmconfigs").split(",");
	    }
        }
        else if(item.split("=")[0] == "options"){
            this.options = GetURLParameter("options").split(",");
        }
    });

    // check options provided in the url and update video properties
    this.options.forEach(item => {
	if(item.includes("seekInterval")){
         this.seekInterval = parseInt(item.split('(')[1].split(')')[0]);
        }
        else if(item.includes("checkInterval")){
         this.checkInterval = parseInt(item.split('(')[1].split(')')[0])*1000;
        }
        else if(item.includes("secondaryURL")){
         this.secondaryURL = item.split('(')[1].split(')')[0];
        }
        else if(item.includes("enableCC")){
         this.enableCCStatus = item.split('(')[1].split(')')[0];
        }
        else if(item.includes("collectfps")){
         this.enable_fps_flag = 1
         this.webkitInstance = item.split('(')[1].split(')')[0];
        }
        else if(item.includes("deviceport")){
         this.devicePort = parseInt(item.split('(')[1].split(')')[0]);
        }
        else if(item.includes("expectedfps")){
         this.expectedFPS = parseInt(item.split('(')[1].split(')')[0]);
        }
     });
    // check the DRM options provided in the url and update the configs
    this.license_header = "";
    this.preferredDRM   = "";
    this.configs.forEach(item => {
      if(item.includes("headers")){
          this.license_header = String(item.split('(')[1].split(')')[0]);
      }
      else if(item.includes("preferred")){
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

    if(this.enable_fps_flag)
        this.updateRDKServicesInterface()

    this.loadAAMPPlayer();
  }

}



