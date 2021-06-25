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

#The port must be 9224 for rdkservice builds and 9998 for thunder builds
webinspect_port = ""

#channel change application url,replace <TM-IP> with Test manager IP in the URL:
channel_change_url = "http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/ChannelChangeTest.html?test_duration=730"

#no of channel changes to perform
max_channel_change_count = 1000

#channel change maximum duration value in minutes
channel_change_duration = 720

####Long duration test details:
#The url used for testing cobalt
cobalt_test_url = ""

#Test duration in minutes till test should be performed, it should be less than the duration of test video
cobalt_test_duration = 720

####Cobalt play and exit test details
#Test duration in minutes till test should be performed
cobalt_play_and_exit_testtime = 1440

#Configure Variable for Reboot stress test:
EthernetInterface ="eth0"
#Count of how many times reboot should happen
repeatCount = 1000

#Give "No" if the validation step is not mandatory
#If "Yes", script will exit whenever a step fails
ValidateUptime = "No"
ValidateInterface = "No"
ValidatePluginStatus = "No"
ValidateControllerUI = "No"
ValidateNoOfPlugins = "No"
#Give the value in seconds to wait for device to come online after reboot.
rebootwaitTime = 150

####Webkit stress test details
#test duration in minutes till webkit stress test should be performed.
stress_test_duration = 600

#Stress test url, this will trigger the redirection of urls in webkit browser
stress_test_url = "https://cdn.metrological.com/static/storm/app_redirect1.html"

#The directed urls will follow the below pattern
expected_url_pattern = "https://cdn.metrological.com/static/storm/app_redirect[1|2].html\?run=\d*&runs=-1&wait=200&requests=20&side=[A|B]"

####Suspend and Resume tests details
#The maximum number of times the test should repeat:
suspend_resume_max_count = 1000

####Random key sending test details
#The URL used to test cobalt to play while sending random keys
cobalt_randomkey_test_url = ""

#The time in minutes till random keys should be sent, this duration should be less than the duration of above configured video.
cobalt_randomkey_test_duration = 600

##Stress test by Setting URLs in loop test details
#maximum number of URL set operation
url_loop_count = 500

#any valid URLs to be launched in webkit
loop_test_url_1 = ""
loop_test_url_2 = ""

##Activate and Deactivate tests details
#maximum number of activate and deactivate operations
activate_deactivate_max_count = 1000

##Screen resolution change test details
#Maximum number of resolution set and get operations
change_resolution_max_count = 400

#The directory to which CGI server will upload the images,same as given in the CGI script
image_upload_dir = ""

#List of resolution which are being used for the test
resolutions_list = [{"w":320,"h":240},{"w":640,"h":480},{"w":1280,"h":720},{"w":1920, "h":1080}]

##Power state toggle test
#maximum number of power state changes required
max_power_state_changes = 1000

##Interface toggle test
#maximum number of network interface changes required
max_interface_changes = 1000

##Bluetooth connect-disconnect test
#maximum number of connect and disconnect operations
connect_disconnect_max_count = 1000

##WebKitBrowser KeyStress test
key_stress_max_count = 100

##MoveTofront and MoveToBack test
moveto_operation_max_count = 1000

##Cobalt trickplay test
#time in minutes till the test should be performed
cobalt_trickplay_duration = 1440

##SSH stress test
ssh_max_count = 30

##Cobalt video search and play test
#name of the video to be searched in Cobalt 
cobalt_search_and_play_video_name = ""

#Maximum number of video searches required
cobalt_search_and_play_max_count = 1000

##Video resize test details
video_resize_max_count = 300

##FPS validation test details
fps_test_duration = 360

##Toggle SSID test details
#maximum number of Wi-Fi SSID changes
max_ssid_changes = 1000

#Switch between plugins test details
#maximum number of switch between plugins needed
switch_plugins_max_count = 1000

#URL used for testing WebKitBrowser
webkit_test_url = "https://www.google.com/"

#Life cycle management test details
#Maximum number of complete lifecycle iterations needed
lifecycle_max_count = 1000
