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

AM_CPPFLAGS = -DQT_WEBKIT_LIB ${COPTS} -std=c++0x -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/ds \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/ds-hal \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/ds-rpc \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/ir \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs-hal/ \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/mfr \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/power \
              -I${top_srcdir}/DS_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libdevicesettingsstub.la
libdevicesettingsstub_la_SOURCES = src/DeviceSettingsAgent.cpp
libdevicesettingsstub_la_LIBADD = -ldshalcli -lds -lIARMBus 
libdevicesettingsstub_la_includedir = ${includedir}
libdevicesettingsstub_la_include_HEADERS = ./include/DeviceSettingsAgent.h
