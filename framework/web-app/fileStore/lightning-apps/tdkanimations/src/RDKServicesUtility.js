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

import { Lightning, Log } from '@lightningjs/sdk';
import { dispTime, logMsg, formatBytes, getAverage } from './MediaUtility.js'
import ThunderJS from "ThunderJS";

let tag;
export class RDKServicesInterface extends Lightning.Component {

  _construct() {
    this.config = {};
    this.settings = {};
    this.diagnosticsInfo = {}
    this.cpuList = []
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

  activate(callSign) {
    this.thunderJS.Controller.activate({ callsign: callSign },(err, result) => {
        if (err) {
          logMsg("Failed to activate " + callSign);
        } else {
          logMsg("Successfully activated " + callSign);
        }
    });
  }


  deactivate(callSign) {
    this.thunderJS.Controller.deactivate({ callsign: callSign },(err, result) => {
        if (err) {
          logMsg("Failed to activate " + callSign);
        } else {
          logMsg("Successfully activated " + callSign);
        }
    });
  }


  getDiagnosticsInfo(){
      this.thunderJS.DeviceInfo.systeminfo()
      .then((result) => { tag = this
          tag.settings.consumer.tag(tag.settings.cpuholder).text.text = "CPU : " + result.cpuload
          tag.diagnosticsInfo["cpu"] = result.cpuload
          var mem = formatBytes(result.totalram - result.freeram)
          tag.settings.consumer.tag(tag.settings.memholder).text.text = "MEM Used : " + mem
          tag.diagnosticsInfo["mem"] = mem
          tag.cpuList.push(result.cpuload)
      })
      .catch(function(error) {
          logMsg(error)
      })
      this.thunderJS.LightningApp.fps()
      .then((result) => { tag = this
          tag.settings.consumer.tag(tag.settings.fpsholder).text.text = "FPS : " + result
          tag.diagnosticsInfo["fps"] = result
          tag.fpsList.push(result)
      })
      .catch(function(error) {
          console.log(error)
      })

      logMsg("[DiagnosticInfo]: CPU Load: "     + this.diagnosticsInfo.cpu + " , "
                                 + "FPS: "      + this.diagnosticsInfo.fps + " , "
                                 + "MEM Used: " + this.diagnosticsInfo.mem)

  }

  getAverageDiagnosticsInfo(){
      var avgFPS = getAverage(this.fpsList)
      var avgCPU = getAverage(this.cpuList)
      logMsg("[DiagnosticInfo]: Average FPS: " + avgFPS);
      logMsg("[DiagnosticInfo]: Average Device CPU Load: " + avgCPU);
  }

}




