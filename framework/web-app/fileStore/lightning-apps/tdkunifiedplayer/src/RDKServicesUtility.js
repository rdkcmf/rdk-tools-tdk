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
import { Lightning, Log } from '@lightningjs/sdk';
import { dispTime, logMsg, getAverage } from './MediaUtility.js'
import ThunderJS from "ThunderJS";
let tag;
export class RDKServicesInterface extends Lightning.Component {
  _construct() {
    this.config = {};
    this.settings = {};
    this.diagnosticsInfo = {}
    this.fpsList = []
    this.thunderJS = "";
    logMsg("RDKServicesInterface  _constructer Called")
  }
  _init() {
    logMsg("RDKServicesInterface _init Called");
  }
  rdkservicesInterfaceInit() {
      logMsg("RDKServicesInterface Init")
      logMsg("Host IP:"   + this.config.host);
      logMsg("Host PORT:" + this.config.port);
      logMsg("WEBKIT INSTANCE:" + this.settings.webkitinstance);
      try {
        this.thunderJS = ThunderJS(this.config);
        logMsg("RDKServicesInterface Init Success")
      } catch (err) {
        logMsg(err);
      }
  }
  updateSettings(config={},settings={}){
      this.config = config
      this.settings = settings
      logMsg("Updated settings for RDKServicesInterface")
  }
  getDiagnosticsInfo(){
      if(this.settings.webkitinstance == "LightningApp"){
      this.thunderJS.LightningApp.fps()
      .then((result) => { tag = this
          tag.diagnosticsInfo["fps"] = result
          tag.fpsList.push(result)
      })
      .catch(function(error) {
          console.log(error)
      })
      }else if(this.settings.webkitinstance == "WebKitBrowser"){
      this.thunderJS.WebKitBrowser.fps()
      .then((result) => { tag = this
          tag.diagnosticsInfo["fps"] = result
          tag.fpsList.push(result)
      })
      .catch(function(error) {
          console.log(error)
      })
      }

      logMsg("[DiagnosticInfo]: FPS: "+ this.diagnosticsInfo.fps)
  }
  getAverageDiagnosticsInfo(){
      var avgFPS = getAverage(this.fpsList)
      logMsg("[DiagnosticInfo]: Average FPS: " + avgFPS);
      return avgFPS
  }
}
