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

import { Lightning, VideoPlayer } from '@lightningjs/sdk'
import { logMsg, logDASHEventMsg } from './MediaUtility.js'
import Hls from 'hls.js'
import 'dashjs/dist/dash.all.min'

export default class VideoPlayerAdvanced extends Lightning.Component {

    _init(){
        logMsg("VideoPlayerAdvanced init");
    }

    setConsumer(consumer) {
        VideoPlayer.consumer(consumer)
    }

    updateDimensions(t,r,b,l){
        VideoPlayer.area(t,r,b,l);
        logMsg("Video Player Width set to  : " + VideoPlayer.width)
        logMsg("Video Player height set to : " + VideoPlayer.height)
    }

    open(url){
        logMsg("Video Player Open: " + url)
        VideoPlayer.open(url)
    }

    openHls(url,config) {
            /*let basic_config = {
            maxBufferLength: 5,
            maxBufferSize: 1*1024*1024,
            enableWorker: false,
            debug: false,
            liveDurationInfinity: true
            }*/
            let basic_config = {liveDurationInfinity: true}
            window.Hls = Hls
            if (!window.Hls) {
              window.Hls = class Hls {
              static isSupported() {
                console.warn('hls-light not included')
                return false
                }
              }
            }
            if (Object.keys(config).length != 0){
                if (config.hasOwnProperty("com.widevine.alpha")){
                    //console.log("Videoplayer (HLSJS): attaching protection data: " + JSON.stringify(config));
                    basic_config.emeEnabled = true;
                    basic_config.widevineLicenseUrl = config["com.widevine.alpha"]
                }
            }
            if (window.Hls.isSupported()) {
              if (!this._hls) this._hls = new window.Hls(basic_config)
              this._hls.attachMedia(VideoPlayer._videoEl)
              this._hls.on(Hls.Events.MEDIA_ATTACHED, function () {
                logMsg("Video and HLSJS are now bound together !!!");
              });
              setTimeout(()=>{
                logMsg("Videoplayer (HLSJS): attaching video source url: " + url);
                this._hls.loadSource(url);
              },1000);
            }
            /*this._hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
              console.log("Manifest loaded, found " + data.levels.length + " quality level.");
            });*/
            //VideoPlayer._videoEl.style.display = 'block'
    }

    openDash(url,config) {
        this.player = dashjs.MediaPlayer().create()
        /*this.player.updateSettings({
            "streaming": {
                    "bufferPruningInterval": 5,
                    "bufferToKeep": 5,
                    "bufferTimeAtTopQuality": 5,
                    "bufferTimeAtTopQualityLongForm": 5,
            }
        });*/
        this.player.updateSettings({'debug':{'logLevel':dashjs.Debug.LOG_LEVEL_NONE }});
        this.player.initialize(VideoPlayer._videoEl, url, true)
        // Registering specific dash.js events
	this.player.on(dashjs.MediaPlayer.events["PLAYBACK_STARTED"],logDASHEventMsg);
	this.player.on(dashjs.MediaPlayer.events["PERIOD_SWITCH_STARTED"],logDASHEventMsg);
	this.player.on(dashjs.MediaPlayer.events["PERIOD_SWITCH_COMPLETED"],logDASHEventMsg);
        if (Object.keys(config).length != 0){
            //console.log("Videoplayer (DASHJS): attaching protection data: " + JSON.stringify(config));
            this.player.setProtectionData(config);
        }
        logMsg("Attaching video source url: " + url);
    }
    reload(url){
        if (this.player) {
          this.player.attachSource(null);
          this.player.attachSource(url);
          logMsg("Attaching video source url: " + url);
        }
    }

    close() {
        if (this._hls) {
          this._hls.detachMedia()
          this._hls = undefined
        } else if (this.player) {
          this.player.reset()
          this.player = null
        } else {
          VideoPlayer.close();
        }
        VideoPlayer._videoEl.style.display = 'none'
    }

}

