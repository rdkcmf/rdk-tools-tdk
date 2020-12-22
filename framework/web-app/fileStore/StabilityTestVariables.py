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
#The port must be 9998 for thunder builds and 9224 for rdkservice builds
webinspect_port = ""

#channel change application url, sample application:"http://cdn.metrological.com/static/storm/cc_time_v2.html?test_duration=168"
channel_change_url = ""

#no of channel changes to perform
max_channel_change_count = 1000

####Long duration test details:
#The url used for testing cobalt
cobalt_test_url = ""

#test duration in minutes till test should be performed, it should be less than the duration of test video
cobalt_test_duration = 330

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
stress_test_duration = 240

#Stress test url, this will trigger the redirection of urls in webkit browser
stress_test_url = "https://cdn.metrological.com/static/storm/app_redirect1.html"

#The directed urls will follow the below pattern
expected_url_pattern = "https://cdn.metrological.com/static/storm/app_redirect[1|2].html\?run=\d*&runs=-1&wait=200&requests=20&side=[A|B]"

####Suspend and Resume tests details - used for both webkit test and cobalt test
#The maximum number of times the test should repeat:
suspend_resume_max_count = 100

####Random key sending test details
#The URL used to test cobalt to play while sending random keys
cobalt_randomkey_test_url = ""

#The time in minutes till random keys should be sent, this duration should be less than the duration of above configured video.
cobalt_randomkey_test_duration = 60
