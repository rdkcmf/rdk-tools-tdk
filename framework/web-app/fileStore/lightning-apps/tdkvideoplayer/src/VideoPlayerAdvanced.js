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
import Hls from 'hls.js'
import 'dashjs/dist/dash.all.min'

export default class VideoPlayerAdvanced extends Lightning.Component {

    _init(){
        console.log("VideoPlayerAdvanced init");
    }

    setConsumer(consumer) {
        VideoPlayer.consumer(consumer)
    }

    updateDimensions(t,r,b,l){
        VideoPlayer.area(t,r,b,l);
        console.log("Video Player Width set to  : " + VideoPlayer.width)
        console.log("Video Player height set to : " + VideoPlayer.height)
    }

    open(url){
        console.log("Video Player Open: " + url)
        VideoPlayer.open(url)
    }

    openHls(url) {
        window.Hls = Hls
        if (!window.Hls) {
            window.Hls = class Hls {
            static isSupported() {
                console.warn('hls-light not included')
                return false
            }
          }
        }
        if (window.Hls.isSupported()) {
            if (!this._hls) this._hls = new window.Hls({ liveDurationInfinity: true })
            this._hls.loadSource(url)
            this._hls.attachMedia(VideoPlayer._videoEl)
            VideoPlayer._videoEl.style.display = 'block'
        }
    }

    openDash(url) {
        this.player = dashjs.MediaPlayer().create()
        VideoPlayer._videoEl.style.display = 'block'
        this.player.initialize(VideoPlayer._videoEl, url, true)
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



