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

# The default browser instance used for launching the video test apps
# webkit_instance can be "WebKitBrowser" or "LightningApp"
webkit_instance = "WebKitBrowser"
# The default browser instance used for launching html video test app
# webkit_instance_html can be "WebKitBrowser" or "HtmlApp"
webkit_instance_html = "HtmlApp"

# If the webkit_instance is "WebKitBrowser", then port must be 9998 for
# thunder builds and 9224 for rdkservice builds. If the webkit_instance
# is "LightningApp", then port must be 10002
webinspect_port=""

# If the webkit_instance_html is "WebKitBrowser", then port must be 9998 for
# thunder builds and 9224 for rdkservice builds. If the webkit_instance_html
# is "HtmlApp", then port must be 10001
webinspect_port_html = ""

# For the animation tests, default  browser instance is "LightningApp". So
# the port value should be 10002
webinspect_port_lightning = ""

#Port used by ThunderJS in lightning app,port must be 9998 for rdkservice builds
thunder_port=""

lightning_apps_loc = ""

#lightning application url
lightning_video_test_app_url     = lightning_apps_loc + "tdkvideoplayer/build/index.html"
lightning_uve_test_app_url       = lightning_apps_loc + "tdkuveplayer/build/index.html"
lightning_animation_test_app_url = lightning_apps_loc + "tdkanimations/build/index.html"
lightning_multianimation_test_app_url    = lightning_apps_loc + "tdkmultianimations/build/index.html"
lightning_objects_animation_test_app_url = lightning_apps_loc + "tdkobjectanimations/build/index.html"

#HTML player application url
html_video_test_app_url = lightning_apps_loc + "tdkhtmlplayer.html"

#HLS Video URL
video_src_url_hls = ""
video_src_url_4k_hls = ""
video_src_url_live_hls = ""
video_src_url_short_duration_hls = ""

#DASH Video URL
video_src_url_dash = ""
video_src_url_4k_dash = ""
video_src_url_live_dash = ""
video_src_url_short_duration_dash = ""

#MP4 Video URL
video_src_url_mp4 = ""
video_src_url_dash_mp4 = ""

#H.264 Codec Video URL
video_src_url_dash_h264 = ""
video_src_url_hls_h264  = ""

#HEVC Codec Video URL
video_src_url_dash_hevc = ""
video_src_url_hls_hevc  = ""

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

#Audio-Only URL
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

#Type of the different codecs video stream. If the url extension is .mpd, then type is dash. If .m3u8, then type is hls
#If the extension is .mp4,.ogg etc mention as mp4,ogg etc.
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
ogg_url_type  = ""
dolby_url_type = ""


# direct ogg & webm container streams
video_src_url_direct_ogg  = ""
video_src_url_direct_webm = ""


# DRM Protected content URLs
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


# Time duration for operations
# Provided time (seconds) is the duration after how much second the operation should take place
# The time interval for any operation should be set with the consideration of time taken to ssh
# and get proc details. Eg. If fetching proc details takes 5 seconds then interval should be
# greater than time taken say 10
pause_interval = 30
play_interval = 10

pause_interval_stress = 10
play_interval_stress  = 10
repeat_count_stress = 15

operation_max_interval = 10

fastfwd_max_interval = 60

# Default jump interval for seek forward or backward operations
seekfwd_interval = 10
seekbwd_interval = 20
seekfwd_check_interval = 3
seekbwd_check_interval = 7

# Provided time (seconds) is the duration after how much second, the player should be closed
close_interval = 180
audio_close_interval = 120

# Min Time duration for the animation operation used by multianimations app (10 to 60 sec)
animation_duration = 60
# No of objects to be animated by objects(rectangles/texts) animation app
objects_count = 500

# Already Existing Sample Animation App URL
sample_animation_test_url = ""
# XPath of the element to expand
element_expand_xpath = ""
# XPath of the element from where actual data to be read from UI
ui_data_xpath = ""

display_variable = ""
#Give the path where the chromedriver executable is available
path_of_browser_executable = ""

#The directory to which CGI server will upload the images,same as given in the CGI script
image_upload_dir = ""
