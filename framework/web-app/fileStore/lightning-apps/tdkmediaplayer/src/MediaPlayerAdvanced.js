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
import { Lightning, MediaPlayer, Metrics } from '@lightningjs/sdk'
import Hls from 'hls.js'
import 'dashjs/dist/dash.all.min'


export default class MediaPlayerAdvanced extends MediaPlayer {

    updateSettings(settings = {}) {
        this._consumer = settings.consumer
        if (this._consumer && this._consumer.getMediaplayerSettings) {
            settings = Object.assign(settings, this._consumer.getMediaplayerSettings())
        }
        if (!Lightning.Utils.equalValues(this._stream, settings.stream)) {
            if (settings.stream && settings.stream.keySystem) {
            navigator
             .requestMediaKeySystemAccess(
              settings.stream.keySystem.id,
              settings.stream.keySystem.config
            )
            .then(createdMediaKeys => {
              return this.videoEl.setMediaKeys(createdMediaKeys)
            })
            .then(() => {
              if (settings.stream && settings.stream.src) this.open(settings.stream.src)
            })
            .catch(e => {
              console.error('Failed to set up MediaKeys' + e)
            })
            } else {
              this.close()
            }
            this._stream = settings.stream
        }
        this._setHide(settings.hide)
        this._setVideoArea(settings.videoPos)
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
          this._metrics = Metrics.media(url)
          if (!this._hls) this._hls = new window.Hls({ liveDurationInfinity: true })
            this._hls.loadSource(url)
            this._hls.attachMedia(this.videoEl)
            this.videoEl.style.display = 'block'
            // Uncomment if video to be muted by default
            // this.videoEl.muted = false
        }
    }

    openDash(url) {
        this.player = dashjs.MediaPlayer().create()
        this._metrics = Metrics.media(url)
        // Uncomment if video to be muted by default
        // this.videoEl.muted = false
        this.videoEl.style.display = 'block'
        this.player.initialize(this.videoEl, url, true)
    }

    close() {
        if (this._hls) {
          this._hls.detachMedia()
          this._hls = undefined
        } else if (this.player) {
          this.player.reset()
          this.player = null
        } else {
          this.videoEl.pause()
          this.videoEl.removeAttribute('src')
          this.videoEl.load()
          this._clearSrc()
        }
        this.videoEl.style.display = 'none'
    }

}
