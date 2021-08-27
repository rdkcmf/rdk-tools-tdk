##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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

# The webkit plugin instance used for load html page test, it can be either HtmlApp or WebKitBrowser
html_app_instance = "HtmlApp"
# URL used for load html page test
html_page_url = "https://vimeo.com/channels/premieres"

# The webkit plugin instance used for load html page test, it can be either LightningApp or WebKitBrowser
lightning_app_instance = "LightningApp"
# URL used for load lightningApp test
lightning_app_url = "https://widgets.metrological.com/lightning/rdk/d431ce8577be56e82630650bf701c57d#app:com.metrological.app.VimeoRelease"

# Keycode dictionary
navigation_key_dictionary = {"ArrowLeft":37,"ArrowUp":38,"ArrowRight":39,"ArrowDown":40,"OK":13}

# Key sequence for navigate test in resident app UI
navigation_key_sequence = ["ArrowRight","ArrowRight","ArrowLeft","ArrowLeft","ArrowDown","ArrowRight","ArrowLeft","ArrowUp"]

# Youtube video URL used to test video playback, video should have a duration of minimum 10 minutes
cobalt_test_url = ""

# Test time in minutes for Cobalt long duration video playback test
cobalt_test_duration = 720
# Youtube video URL used to test long duration video playback, video should have a duration more than 10 hours
cobalt_long_duration_test_url = ""

# Youtube video URL used to test 4K video playback, video should have a duration of minimum 10 minutes
cobalt_test_url_4k = ""
# Key navigations used to select 4K resolution for a video in Cobalt
key_navigation_for_4k = ['ArrowUp','ArrowUp','ArrowRight','ArrowRight','ArrowRight','OK','OK','ArrowUp','ArrowUp','ArrowUp','ArrowUp','ArrowUp','ArrowUp','ArrowUp','ArrowUp','ArrowDown','ArrowDown','OK']

# Encrypted video URL used to test encrypted video playback, video should have a duration of minimum 10 minutes
cobalt_encrypted_test_url = ""

# Key sequence to launch vimeo application from webstore
app_launch_key_sequence = ["ArrowDown","ArrowRight","OK"]
# key sequence to reach the initial position after app launch
post_app_launch_key_sequence = ["ArrowLeft","ArrowUp"]
