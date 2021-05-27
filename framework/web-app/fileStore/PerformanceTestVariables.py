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

#Channel change application URL, Replace <TM-IP> with Test manager IP in below URL
channel_change_url = "http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/ChannelChangeTest.html?test_duration=168"

#The url used for testing cobalt
cobalt_test_url = ""

#Thunder port for listening to events
thunder_port = "9998"

#Video player app URL, sample URL: http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/tdkvideoplayer/build/index.html
lightning_video_test_app_url = ""

#Video URL, either HLS URL or DASH URL
video_src_url = ""

#Type of the video url configured above, give hls for .m3u8 and dash for .mpd
video_src_url_type = ""

#Amazon video url 
amazon_test_url = ""
