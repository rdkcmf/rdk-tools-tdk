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

#************************************************************************
#         WEBKIT PLUGIN INSTANCE AND PORT CONFIGURATIONS
#************************************************************************

# The default browser instance used for launching the video test apps
# webkit_instance can be "WebKitBrowser" or "LightningApp" plugin
webkit_instance = "WebKitBrowser"
#webkit_instance = "LightningApp"


# The default browser instance used for launching html video test app
# webkit_instance_html can be "WebKitBrowser" or "HtmlApp" plugin
webkit_instance_html = "HtmlApp"
#webkit_instance_html = "WebKitBrowser"


# If the webkit_instance is "WebKitBrowser", then preferable web-inspect
# page port is 9998 for thunder builds and 9224 for rdkservice builds.
# If the webkit_instance is "LightningApp", then preferable port is 10002
webinspect_port = "9224"
#webinspect_port = "10002"


# If the webkit_instance_html is "WebKitBrowser", then preferable web-inspect
# page port is 9998 for thunder builds and 9224 for rdkservice builds.
# If the webkit_instance_html is "HtmlApp", then preferable port is 10001
webinspect_port_html = "10001"
#webinspect_port_html = "9998"


# For the animation tests, default browser instance is "LightningApp". So
# the preferable web-inspect page port value is 10002
webinspect_port_lightning = "10002"


#Port used by ThunderJS in lightning app,port must be 9998 for rdkservice builds
thunder_port=""


#************************************************************************
#                  MVS TEST APPS URLs CONFIGURATIONS
#************************************************************************

# Lightning apps location url
# Eg. lightning_apps_loc = "http://<TM_IP>:8080/rdk-test-tool/fileStore/lightning-apps/"
lightning_apps_loc = ""

#lightning application url
lightning_video_test_app_url     = lightning_apps_loc + "tdkvideoplayer/build/index.html"
lightning_uve_test_app_url       = lightning_apps_loc + "tdkuveaampplayer/build/index.html"
lightning_animation_test_app_url = lightning_apps_loc + "tdkanimations/build/index.html"
lightning_multianimation_test_app_url    = lightning_apps_loc + "tdkmultianimations/build/index.html"
lightning_objects_animation_test_app_url = lightning_apps_loc + "tdkobjectanimations/build/index.html"

#HTML player application url
html_video_test_app_url = lightning_apps_loc + "tdkhtmlplayer.html"


#************************************************************************
#         DIFFERENT AV CODEC HLS/DASH URLs FOR CODEC TESTING
#************************************************************************

# Short duration src streams. Streams should be of maximum 15 seconds
#HLS Video URL
video_src_url_short_duration_hls = ""
#DASH Video URL
video_src_url_short_duration_dash = ""


# Long duration src streams. Streams should be of minimum 5-10 minutes
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
video_src_url_dash_mp4 = ""

#H.264 Codec Video URL
video_src_url_dash_h264 = ""
video_src_url_hls_h264  = ""

#H.264 codec video URL with iframe track. Used by UVE AAMP trickplay tests
video_src_url_dash_h264_iframe = ""
video_src_url_hls_h264_iframe  = ""

#HEVC Codec Video URL
video_src_url_hevc = ""

#H.263 Codec Video URL
video_src_url_h263 = ""

#AAC Codec Video URL
video_src_url_aac = ""

#VP9 Codec Video URL
video_src_url_vp9 = ""

#VP8 Codec Video URL
video_src_url_vp8 = ""

#Opus Codec Video URL
video_src_url_opus = ""

#Audio-Only URL. Stream should be of minimum 2-3 minutes
video_src_url_audio = ""

#MPEG-TS Video URL
video_src_url_mpegts = ""

#MPEG 1/2 Video URL
video_src_url_mpeg = ""

#AV1 Codec Video URL
video_src_url_av1 = ""

#AC3 Codec Video URL
video_src_url_ac3 = ""

#EC3 Codec Video URL
video_src_url_ec3 = ""

#OGG Video URL
video_src_url_ogg = ""

#Dolby Video URL
video_src_url_dolby = ""

#Type of the different codecs video stream. If the url is dash(.mpd), then type is dash. If its a
#hls stream(.m3u8),then type is hls. If the extension is .mp4,.ogg etc mention as mp4,ogg etc.
h263_url_type = ""
aac_url_type  = ""
vp9_url_type = ""
vp8_url_type = ""
opus_url_type = ""
audio_url_type = ""
mpegts_url_type = ""
mpeg_url_type = ""
av1_url_type  = ""
ac3_url_type  = ""
ec3_url_type  = ""
hevc_url_type = ""
ogg_url_type  = ""
dolby_url_type = ""

# direct ogg & webm container streams without ABR (not hls/dash)
video_src_url_direct_ogg  = ""
video_src_url_direct_webm = ""

# Different MPD Variant streams
video_src_url_dash_segement_base = ""
video_src_url_dash_segement_list = ""
video_src_url_dash_segement_timeline = ""
video_src_url_dash_segement_template = ""


#************************************************************************
#                  DRM PROTECTED CONTENT STREAM URLs
#************************************************************************

# Example:
# video_src_url_playready_dash = "http://playready_dash_url.mpd"
# video_src_url_playready_dash_drmconfigs = "com.microsoft.playready[http://license_url]|com.widevine.alpha[http://license_url]|headers[X-AxDRM-Message:header_info]"
# Note: Each drm config must be seperated by "|" and the values must be enclosed within "[" "]" as above.

# PlayReady DRM URLs
video_src_url_playready_dash_aac = ""
video_src_url_playready_dash_aac_drmconfigs = ""

video_src_url_playready_dash_h264 = ""
video_src_url_playready_dash_h264_drmconfigs = ""

video_src_url_playready_dash_ac3 = ""
video_src_url_playready_dash_ac3_drmconfigs = ""

video_src_url_playready_dash_ec3 = ""
video_src_url_playready_dash_ec3_drmconfigs = ""

video_src_url_playready_dash_hevc = ""
video_src_url_playready_dash_hevc_drmconfigs = ""

video_src_url_playready_hls_aac = ""
video_src_url_playready_hls_aac_drmconfigs = ""

video_src_url_playready_hls_h264 = ""
video_src_url_playready_hls_h264_drmconfigs = ""

video_src_url_playready_hls_hevc = ""
video_src_url_playready_hls_hevc_drmconfigs = ""

# Widevine DRM URLs
video_src_url_widevine_dash_aac = ""
video_src_url_widevine_dash_aac_drmconfigs = ""

video_src_url_widevine_dash_h264 = ""
video_src_url_widevine_dash_h264_drmconfigs = ""

video_src_url_widevine_dash_ac3 = ""
video_src_url_widevine_dash_ac3_drmconfigs =""

video_src_url_widevine_dash_ec3 = ""
video_src_url_widevine_dash_ec3_drmconfigs =""

video_src_url_widevine_dash_hevc = ""
video_src_url_widevine_dash_hevc_drmconfigs =""

video_src_url_widevine_dash_vp9 = ""
video_src_url_widevine_dash_vp9_drmconfigs = ""

video_src_url_widevine_hls_aac = ""
video_src_url_widevine_hls_aac_drmconfigs = ""

video_src_url_widevine_hls_h264 = ""
video_src_url_widevine_hls_h264_drmconfigs = ""

video_src_url_widevine_hls_hevc = ""
video_src_url_widevine_hls_hevc_drmconfigs = ""

video_src_url_widevine_dash_av1 = ""
video_src_url_widevine_dash_av1_drmconfigs = ""

video_src_url_widevine_dash_opus = ""
video_src_url_widevine_dash_opus_drmconfigs = ""

video_src_url_widevine_dash_vp8 = ""
video_src_url_widevine_dash_vp8_drmconfigs = ""

#Multi-DRM Test streams
video_src_url_multi_drm_dash = ""
video_src_url_multi_drm_dash_pref_playready_drmconfigs = ""
video_src_url_multi_drm_dash_pref_widevine_drmconfigs  = ""


#************************************************************************
#                GENERAL CONFIGURATIONS FOR VIDEO TESTS
#************************************************************************

# Time duration for operations
# Provided time (seconds) is the duration after how much second the operation should take place
# The time interval for any operation should be set with the consideration of time taken to ssh
# and get proc details. Eg. If fetching proc details takes 5 seconds then interval should be
# greater than time taken say 10

# This interval indicates after how much seconds video should be paused in playpause test
pause_interval = 30
# This interval indicates after how much seconds video should start playing in playpause test
play_interval = 10

# This interval indicates after how much seconds video should be paused in playpause stress test
pause_interval_stress = 10
# This interval indicates after how much seconds video should start playing in playpause stress test
play_interval_stress  = 10
# This count indicates after how many times the oprations should repeat in stress tests
repeat_count_stress = 10

# This interval indicates after how much seconds any video operations should take place
operation_max_interval = 10
# This interval indicates max duration for FF operations
fastfwd_max_interval = 60

# Default jump interval for seek forward or backward operations
seekfwd_interval = 10
seekbwd_interval = 20
seekfwd_check_interval = 5
seekbwd_check_interval = 7
# Default check interval for fast forward operations
fastfwd_check_interval = 5

# Provided time (seconds) is the duration after how much second, the player should be closed
close_interval = 180
audio_close_interval = 120



#************************************************************************
#            GENERAL CONFIGURATIONS FOR ANIMATION TESTS
#************************************************************************

# Min Time duration for the animation operation used by multianimations app (10 to 60 sec)
animation_duration = 60
# No of objects to be animated by objects(rectangles/texts) animation app
objects_count = 500

# Already Existing Sample Animation App URL
sample_animation_test_url = ""
# XPath of the html tag element to expand in web-inspect page.User has to manually identify
# the xpath by loading the test url in browser and checking the xpath in inspect page
element_expand_xpath = ""
# XPath of the display fps element from where actual data to be read from UI
ui_data_xpath = ""

# Display parameter for opening browser
display_variable = ""
#Give the path where the chromedriver executable is available
#Eg. path_of_browser_executable = ":/home/testing/webui"
path_of_browser_executable = ""

#The directory to which CGI server will upload the images,same as given in the CGI script
image_upload_dir = ""


#************************************************************************
#            CONFIGURATIONS FOR MSE/EME TESTS
#************************************************************************
#User shall update the URL as per the version required
mse_conformance_test_app_url = "https://ytlr-cert.appspot.com/2021/main.html?test_type=conformance-test"
eme_conformance_test_app_url = "https://ytlr-cert.appspot.com/2021/main.html?test_type=encryptedmedia-test"

#Key codes to navigate and start the test. Values must follow the pattern KeyName:KeyCode seperated by comma
#Key sequence should be updated corresponding to the test URL used by the user
mse_key_sequence = "ArrowLeft:37,ArrowDown:40,ArrowDown:40,ArrowUp:38,ArrowLeft:37,Enter:13"
eme_key_sequence = "ArrowDown:40,ArrowDown:40,ArrowDown:40,ArrowUp:38,ArrowLeft:37,Enter:13"

