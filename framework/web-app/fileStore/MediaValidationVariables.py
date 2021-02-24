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
webinspect_port=""

#Port used by ThunderJS in lightning app,port must be 9998 for rdkservice builds
thunder_port=""

#lightning application url
lightning_video_test_app_url = ""
lightning_animation_test_app_url = ""
lightning_multianimation_test_app_url = ""
lightning_objects_animation_test_app_url = ""

#Video URL
video_src_url = ""

#HLS Video URL
video_src_url_hls = ""
video_src_url_4k_hls = ""
video_src_url_live_hls = ""

#DASH Video URL
video_src_url_dash = ""
video_src_url_4k_dash = ""
video_src_url_live_dash = ""

#MP4 Video URL
video_src_url_mp4 = ""

# Time duration for operations
# Provided time (seconds) is the duration after how much second the operation should take place
pause_interval = 30
play_interval = 10

pause_interval_stress = 5
play_interval_stress  = 5
repeat_count_stress = 15

operation_min_interval = 5
operation_max_interval = 10

fastfwd_max_interval = 60

seekfwd_interval = 10
seekbwd_interval = 20
seekfwd_check_interval = 3
seekbwd_check_interval = 7

# Provided time (seconds) is the duration after how much second, the player should be closed
close_interval = 180

# Min Time duration for the animation operation used by multianimations app (10 to 60 sec)
animation_duration = 60
# No of objects to be animated by objects(rectangles/texts) animation app
objects_count = 500
