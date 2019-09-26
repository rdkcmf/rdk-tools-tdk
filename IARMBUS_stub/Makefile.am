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

AM_CPPFLAGS = ${COPTS} -fPIC -DDEBUG_LEVEL_TRACE

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/power/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/ir \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/mfr \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs-hal/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/sysmgr/ \
           -I${top_srcdir}/IARMBUS_stub/include -I${top_srcdir}/agent/include


AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/ \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/ir \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/mfr \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs-hal/ \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/power \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/sysmgr/ \
              -I${top_srcdir}/IARMBUS_stub/include -I${top_srcdir}/agent/include


lib_LTLIBRARIES = libiarmbusstub.la
libiarmbusstub_la_SOURCES = src/IARMBUSStub.cpp
libiarmbusstub_la_LIBADD = -lIARMBus 
libiarmbusstub_la_includedir = ${includedir}
libiarmbusstub_la_include_HEADERS = ${top_srcdir}/IARMBUS_stub/include/IARMBUSAgent.h

bin_PROGRAMS = tst_iarmbus DUMMYMgr gen_single_event gen_multiple_events

tst_iarmbusdir = ${bindir}
tst_iarmbus_SOURCES = src/tst_iarmbus.c
tst_iarmbus_LDADD = -lIARMBus -lz -lglib-2.0
tst_iarmbus_includedir = ${includedir}

DUMMYMgrdir = ${bindir}
DUMMYMgr_SOURCES = src/Test_Event_Mgr.c
DUMMYMgr_LDADD = -lIARMBus -lz -lglib-2.0
DUMMYMgr_includedir = ${includedir}

gen_single_eventdir = ${bindir}
gen_single_event_SOURCES = src/gen_single_event.cpp
gen_single_event_LDADD = -lrt -lIARMBus -lz -lglib-2.0
gen_single_event_includedir = ${includedir}

gen_multiple_eventsdir = ${bindir}
gen_multiple_events_SOURCES = src/gen_multiple_events.cpp
gen_multiple_events_LDADD = -lrt -lIARMBus -lz -lglib-2.0
gen_multiple_events_includedir = ${includedir}
