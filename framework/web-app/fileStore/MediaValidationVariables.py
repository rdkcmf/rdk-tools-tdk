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
lightning_video_test_app_url     = lightning_apps_loc + "tdkunifiedplayer/build/index.html?player=VIDEO"
lightning_shaka_test_app_url     = lightning_apps_loc + "tdkunifiedplayer/build/index.html?player=SHAKA"
lightning_uve_test_app_url       = lightning_apps_loc + "tdkunifiedplayer/build/index.html?player=AAMP"
lightning_animation_test_app_url = lightning_apps_loc + "tdkanimations/build/index.html"
lightning_multianimation_test_app_url    = lightning_apps_loc + "tdkmultianimations/build/index.html"
lightning_objects_animation_test_app_url = lightning_apps_loc + "tdkobjectanimations/build/index.html"

#HTML player application url
html_video_test_app_url = lightning_apps_loc + "tdkhtmlplayer.html"

# Test Streams Base URL
# This is the location under webapps directory in TDK Test Manager Machine where the test streams zip is extracted
# If zip is extracted in some other server machine (not in TDK Test Manager Machine), then use the corresponding
# server URL with the directory path of the test streams folder TDK_Clear_Test_Streams_Sunrise
# (or)
# If zip is copied to /opt/apache-tomcat-7.0.96/webapps/ folder in TDK Test Manager Machine and extracted,then
# use the below test streams base URL after updating TM IP
#test_streams_base_path = "http://<TM_IP>/TDK_Clear_Test_Streams_Sunrise/"
test_streams_base_path = ""


#************************************************************************
#         DIFFERENT AV CODEC HLS/DASH URLs FOR CODEC TESTING
#************************************************************************

# Short duration src streams. Streams should be of maximum 15 seconds
#HLS Video URL
video_src_url_short_duration_hls  = test_streams_base_path + "HLS_H264_AAC_15Sec/master.m3u8"
#DASH Video URL
video_src_url_short_duration_dash = test_streams_base_path + "DASH_H264_AAC_15Sec/master.mpd"


# Long duration src streams. Streams should be of minimum 5-10 minutes
#HLS Video URL
video_src_url_hls    = test_streams_base_path + "HLS_H264_AAC/master.m3u8"
video_src_url_4k_hls = test_streams_base_path + "HLS_HEVC_AAC/master.m3u8"
video_src_url_live_hls = ""

#DASH Video URL
video_src_url_dash    = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"
video_src_url_4k_dash = test_streams_base_path + "DASH_HEVC_AAC_4K_Only/atfms_291_dash_tdk_hevc_aac_fmp4_4konly.mpd"
video_src_url_live_dash = ""

#MP4 Video URL
video_src_url_mp4      = test_streams_base_path + "TDK_Asset_Sunrise_MP4.mp4"
video_src_url_mp4_24fps  = test_streams_base_path + "TDK_Asset_Sunrise_24fps.mp4"
video_src_url_mp4_25fps  = test_streams_base_path + "TDK_Asset_Sunrise_25fps.mp4"
video_src_url_mp4_30fps  = test_streams_base_path + "TDK_Asset_Sunrise_30fps.mp4"
video_src_url_mp4_50fps  = test_streams_base_path + "TDK_Asset_Sunrise_50fps.mp4"
video_src_url_mp4_60fps  = test_streams_base_path + "TDK_Asset_Sunrise_60fps.mp4"

#H.264 Codec Video URL
video_src_url_dash_h264 = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"
video_src_url_hls_h264  = test_streams_base_path + "HLS_H264_AAC/master.m3u8"

#H.264 codec video URL with iframe track. Used by UVE AAMP trickplay tests
video_src_url_dash_h264_iframe = ""
video_src_url_hls_h264_iframe  = ""

#HEVC Codec Video URL
video_src_url_hevc = test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"

#H.263 Codec Video URL
video_src_url_h263 = test_streams_base_path + "TDK_Asset_Sunrise_H263_AAC.mov"

#AAC Codec Video URL
video_src_url_aac = test_streams_base_path + "HLS_H264_AAC/master.m3u8"

#VP9 Codec Video URL
# By default VP9_OPUS stream is used, if we need to test with VP9_OGG stream
# then comment VP9_OPUS stream and uncomment VP9_OGG stream urls below
video_src_url_vp9 = test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"
#video_src_url_vp9 = test_streams_base_path + "DASH_VP9_OGG_WebM/master.mpd"

#VP8 Codec Video URL
video_src_url_vp8 = test_streams_base_path + "TDK_Asset_Sunrise_VP8_Opus.webm"

#Opus Codec Video URL
video_src_url_opus = test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"

#Audio-Only URL. Stream should be of minimum 2-3 minutes
video_src_url_audio = test_streams_base_path  + "DASH_AAC_Audio_Only/master.mpd"

#MPEG-TS Video URL
video_src_url_mpegts = test_streams_base_path + "HLS_H264_AAC/master.m3u8"

#MPEG 1/2 Video URL
video_src_url_mpeg = test_streams_base_path + "TDK_Asset_Sunrise_MPEGAV.mpeg"

#AV1 Codec Video URL
video_src_url_av1 = test_streams_base_path + "TDK_Asset_Sunrise_AV1_Opus.webm"

#AC3 Codec Video URL
video_src_url_ac3 = test_streams_base_path + "DASH_H264_AC3/atfms_291_dash_tdk_avc_ac3_fmp4.mpd"

#EC3 Codec Video URL
video_src_url_ec3 = test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd"

#OGG Video URL
video_src_url_ogg = test_streams_base_path + "DASH_VP9_OGG_WebM/master.mpd"

#Dolby Video URL
video_src_url_dolby = test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd"

#Type of the different codecs video stream. If the url is dash(.mpd), then type is dash. If its a
#hls stream(.m3u8),then type is hls. If the extension is .mp4,.ogg etc mention as mp4,ogg etc.
h263_url_type = "mov"
aac_url_type  = "hls"
vp9_url_type  = "dash"
vp8_url_type  = "webm"
opus_url_type = "dash"
audio_url_type  = "aac"
mpegts_url_type = "hls"
mpeg_url_type = "mpeg"
av1_url_type  = "webm"
ac3_url_type  = "dash"
ec3_url_type  = "dash"
hevc_url_type = "dash"
ogg_url_type  = "dash"
dolby_url_type = "dash"

# direct ogg & webm container streams without ABR (not hls/dash)
video_src_url_direct_ogg  = test_streams_base_path + "TDK_Asset_Sunrise_OGG.webm"
video_src_url_direct_webm = test_streams_base_path + "TDK_Asset_Sunrise_VP9_Opus.webm"

# Different MPD Variant streams
video_src_url_dash_segement_base = ""
video_src_url_dash_segement_list = ""
video_src_url_dash_segement_timeline = ""
video_src_url_dash_segement_template = ""

# Streams with multiple audio languages & subtitle text tracks
video_src_url_multi_audio_tracks = ""
video_src_url_multi_text_tracks  = ""

# Streams with multiple audio codecs
#Video URL with AC3 and AAC codec audio
video_src_url_ac3_aac   = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_AC3_AAC.mp4"
#Video URL with OPUS and AC3 codec audio
video_src_url_opus_ac3  = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_AC3_OPUS.mp4"
#Video URL with OPUS and EAC3 codec audio
video_src_url_opus_eac3 = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_EAC3_OPUS.mp4"
#Video URL with EAC3 and AC3 codec audio
video_src_url_ac3_eac3  = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_EAC3_AC3.mp4"
video_src_url_aac_eac3  = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_EAC3_AAC.mp4"
video_src_url_opus_aac = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_AAC_OPUS.mp4"
video_src_url_opus_vorbis = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_Vorbis_Opus.webm"

# Basic WAV PCM Audio format stream
audio_src_url_wav_pcm = test_streams_base_path + "TDK_Asset_Sunrise_WAV_Audio.wav"


# Invalid stream URL for testing error scenarios
video_src_url_invalid = test_streams_base_path + "test_stream_invalid.mpd"



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
# Default Seek/Jump position value and check interval.
seekfwd_position = 120
seekbwd_position = 80
seekpos_check_interval = 10

# Provided time (seconds) is the duration after how much second, the player should be closed (30 sec to 3mins)
close_interval = 30
audio_close_interval = 30



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
mse_conformance_test_app_url = "https://ytlr-cert.appspot.com/2021/main.html?command=run&test_type=conformance-test"
eme_conformance_test_app_url = "https://ytlr-cert.appspot.com/2021/main.html?command=run&test_type=encryptedmedia-test"


