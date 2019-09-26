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

AM_CPPFLAGS = -g -Wall -std=c++0x -DGCC4_XXX \
	      -DDEBUG_CONF_FILE="\"$(CONFIG_PREFIX)debug.ini\"" \
	      -DSYSTEMD_JOURNAL \
	      -fPIC ${COPTS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${top_srcdir}/SNMP_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libsnmpstub.la
libsnmpstub_la_SOURCES = src/SNMPProtocolAgent.cpp 
libsnmpstub_la_includedir = ${includedir}
libsnmpstub_la_include_HEADERS = ${top_srcdir}/SNMP_stub/include/SNMPProtocolAgent.h
