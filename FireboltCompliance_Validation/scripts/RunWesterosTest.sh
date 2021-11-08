#!/bin/sh
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
##########################################################################

DISPLAY=$1
TIMEOUT=$2

#Export westeros library
export XDG_RUNTIME_DIR=/tmp
export LD_PRELOAD=/usr/lib/libwesteros_gl.so.0.0.0

#Start Westeros renderer and run it for 30 seconds
timeout 30  westeros --renderer libwesteros_render_embedded.so.0.0.0 --display $DISPLAY --embedded --window-size 1920x1080 &

#Wait for westeros renderer
sleep 3

#Execute Westeros_TDKTestApp
Westeros_TDKTestApp --display $DISPLAY -t=$TIMEOUT
