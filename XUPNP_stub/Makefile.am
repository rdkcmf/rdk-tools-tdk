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

AM_CPPFLAGS = ${COPTS} -std=c++0x -fPIC -DGCC4_XXX -g

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/sysmgr/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/directfb/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/core/include \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/core \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/generic/ir/include \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/generic/sysmgr/include \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/xupnp/generic/include

AM_CXXFLAGS = -I${top_srcdir}/XUPNP_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libxupnpstub.la
libxupnpstub_la_SOURCES = src/xupnpAgent.cpp
libxupnpstub_la_includedir = ${includedir}
libxupnpstub_la_include_HEADERS = ${top_srcdir}/XUPNP_stub/include/xupnpAgent.h
