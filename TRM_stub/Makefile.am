##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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

AM_CPPFLAGS = -Wall -g -DGCC4_XXX -Wno-format -Wunused -DRDK_BR_2DOT0 ${COPTS} -DNUM_OF_TUNERS=$(MAX_NUM_TUNERS)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/trm \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0 \
              -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include \
              -I${top_srcdir}/TRM_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libtrmstub.la
libtrmstub_la_SOURCES = src/TRMAgent.cpp \
                        src/TRMAgentHelper.cpp

libtrmstub_la_LIBADD = -ltrm 
libtrmstub_la_includedir = ${includedir}
libtrmstub_la_include_HEADERS = ${top_srcdir}/TRM_stub/include/TRMAgentHelper.h \
                                ${top_srcdir}/TRM_stub/include/TRMAgent.h
