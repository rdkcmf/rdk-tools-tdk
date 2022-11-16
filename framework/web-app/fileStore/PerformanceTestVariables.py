##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################

#URL used for testing webkit browser
browser_test_url = ""

#Web inspect port,The port must be 9998 for thunder builds and 9224 for rdkservice builds
webinspect_port = "9224"

#Channel change application URL
channel_change_url = "http://TM-IP/rdk-test-tool/fileStore/lightning-apps/ChannelChangeTest.html?test_duration=168"

#The url used for testing cobalt
cobalt_test_url = ""

# webkit_instance can be "WebKitBrowser" or "LightningApp" or "HtmlApp" plugin
webkit_instance = "LightningApp"

#Video player app URL, sample URL: http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/tdkunifiedplayer/build/index.html?player=VIDEO
lightning_video_test_app_url = ""

#Video URL, either HLS URL or DASH URL
video_src_url = ""

#Type of the video url configured above, give hls for .m3u8 and dash for .mpd
video_src_url_type = ""

#Webinspect port for LightningApp plugin
lightning_app_webinspect_port = "10002"

#Webinspect port for HtmlApp plugin
html_app_webinspect_port = "10001"

#List of Graphical plugins available for test
graphical_plugins_list = ["Cobalt","WebKitBrowser","LightningApp","ResidentApp","HtmlApp"]

#Actual youtube URL should be passed in the below variable
req_graphical_plugins = "Cobalt,deeplink,<Youtube URL video>,13;WebKitBrowser,url,<Google URL>;LightningApp,url,<Youtube URL>"

#URL used to test HtmlApp plugin
html_page_url = "https://vimeo.com/channels/premieres"

#List of processes that can be ignored while checking the zorder
excluded_process_list = ['subtec_s1']

ping_test_destination = "google.com"

#URL used to test encrypted videoplayback
encrypt_test_url = ""

#URL used for Vimeo app
vimeo_test_url="https://widgets.metrological.com/lightning/rdk/d431ce8577be56e82630650bf701c57d#app:com.metrological.app.VimeoRelease"
