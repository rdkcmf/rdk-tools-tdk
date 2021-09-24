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
ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -g -Wall -std=c++0x -DGCC4_XXX \
              -fPIC ${COPTS} $(GST_CFLAGS) $(GST_CHECK_CFLAGS) -DUSE_GST1

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0 \
              -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/gstreamer-1.0 \
              -I${top_srcdir}/../agent/include


bin_PROGRAMS = mediapipelinetests

mediapipelinetests_SOURCES = src/MediaPipelineSuite.cpp
mediapipelinetests_LDADD = $(GST_LIBS) $(GST_CHECK_LIBS) $(GLIBS) -ldl -lpthread -lgstreamer-1.0 -lgstcheck-1.0 -lgobject-2.0 -lglib-2.0
