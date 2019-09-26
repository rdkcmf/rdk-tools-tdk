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
dnl                                               -*- Autoconf -*-
dnl Process this file with autoconf to produce a configure script.

dnl AC_PREREQ([2.69])
AC_INIT(tdk, 1.0, praveensnair@tataelxsi.co.in,tdk)
AC_CONFIG_SRCDIR([agent/src/agentmain.cpp])
AM_CONFIG_HEADER(cfg/config.h)
AC_CONFIG_MACRO_DIR([cfg])
AC_CONFIG_AUX_DIR([cfg])
AM_INIT_AUTOMAKE([foreign no-dist-gzip dist-bzip2 subdir-objects 1.9])
LT_INIT

dnl subdirectories.

dnl Checks for programs.
AC_PROG_CXX
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_CPP
AC_PROG_CXXCPP

dnl use pretty build output with automake >= 1.11
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])],
  [AM_DEFAULT_VERBOSITY=1
   AC_SUBST(AM_DEFAULT_VERBOSITY)])


dnl **********************************
dnl checks for dependencies
dnl **********************************
AC_HEADER_STDC

dnl Checks for header files.
AC_CHECK_HEADERS([limits.h memory.h stdlib.h string.h sys/socket.h unistd.h])

dnl Checks for typedefs, structures, and compiler characteristics.
dnl AC_CHECK_HEADER_STDBOOL
AC_TYPE_UINT8_T

dnl Checks for library functions.
AC_FUNC_MALLOC
AC_CHECK_FUNCS([memset strdup strerror])

COPTS="-DDEBUG_LEVEL_TRACE"
AM_CXXFLAGS="$AM_CXXFLAGS -DDEBUG_LEVEL_TRACE"
AGENT_FLAGS=" "
CONFIG_PREFIX="/etc/"
DVRMGR_FLAGS=" "
RDK_VERSION="RDK2DOT0"
TDKINTEGRATION_FLAGS=" "
TDKINTEGRATION_HYBRID_LIBS=" "
MEDIAFRAMEWORK_HYBRID_LIBS=" "
QAM_LIBS=" "
SF_LIBS=" "
TDK_GST_LIBS=" "
HEADLESS=" "
SUBDIR_HYBRID=" "
SUBDIR_CLIENT=" "
SM_STUB_CFLAG_HYBRID=" "

AC_ARG_ENABLE([hybrid],
        AS_HELP_STRING([--enable-hybrid],[enable hybrid build]),
        [
          case "${enableval}" in
             yes) HYBRID=true
                  SUBDIR_HYBRID="TRM_stub DTCP_stub SNMP_stub"
                  AGENT_FLAGS=" -DPORT_FORWARD";;
           no) HYBRID=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-hybrid ]) ;;
           esac
           ],
         [echo "hybrid build is enable"])
AM_CONDITIONAL([HYBRID], [test x$HYBRID = xtrue])

AC_ARG_ENABLE([qemux86hyb],
        AS_HELP_STRING([--enable-qemux86hyb],[enable qemux86hyb build]),
        [
          case "${enableval}" in
             yes) qemux86hyb=true
                  TDKINTEGRATION_HYBRID_LIBS="-ldvrmgr -lqamsrc -ltrm -ltrh" 
                  MEDIAFRAMEWORK_HYBRID_LIBS="";;
           no) qemux86hyb=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-qemux86hyb ]) ;;
           esac
           ],
         [echo "emulator hybrid build is enable"])
AM_CONDITIONAL([QEMUX86HYB], [test x$qemux86hyb = xtrue])

AC_ARG_ENABLE([client],
        AS_HELP_STRING([--enable-client],[enable client build]),
        [
          case "${enableval}" in
             yes) CLIENT=true
                  SUBDIR_CLIENT="TR069_stub NetSrvMgr_stub MocaHal_stub";;
           no) CLIENT=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-client ]) ;;
           esac
           ],
         [echo "client build is enable"])
AM_CONDITIONAL([CLIENT], [test x$CLIENT = xtrue])

AC_ARG_ENABLE([quemux86mc],
        AS_HELP_STRING([--enable-qemux86mc],[enable quemux86mc build]),
        [
          case "${enableval}" in
             yes) QEMUX86MC=true
                  SUBDIR_CLIENT="TR069_stub";;
           no) QEMUX86MC=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-client ]) ;;
           esac
           ],
         [echo "client build is enable"])
AM_CONDITIONAL([QEMUX86MC], [test x$QEMUX86MC = xtrue])

AC_ARG_ENABLE([audiocapturemgr],
         AS_HELP_STRING([--enable-audiocapturemgr],[enable audiocapturemgr (default is no)]),
         [
           case "${enableval}" in
              yes) AUDIOCAPTUREMGR=true
                   AS_IF([test x$HYBRID = xtrue], [SUBDIR_HYBRID+=" AudioCaptureMgr_stub"],
                          [echo box type not specified]) ;;
             no) AUDIOCAPTUREMGR=false ;;
            *) AC_MSG_ERROR([bad value ${enableval} for --enable-audiocapturemgr ]) ;;
             esac
            ],
           [echo "audiocapturemgr component is not enabled"])
AM_CONDITIONAL([AUDIOCAPTUREMGR], [test x$AUDIOCAPTUREMGR = xtrue])

AC_ARG_ENABLE([usbctrl],
         AS_HELP_STRING([--enable-usbctrl],[enable usbctrl (default is no)]),
         [
           case "${enableval}" in
              yes) USBCTRL=true
                   AS_IF([test x$HYBRID = xtrue], [SUBDIR_HYBRID+=" USBCtrl_stub"],
                          [echo box type not specified]) ;;
             no) USBCTRL=false ;;
            *) AC_MSG_ERROR([bad value ${enableval} for --enable-usbctrl ]) ;;
             esac
            ],
           [echo "usbctrl component is not enabled"])
AM_CONDITIONAL([USBCTRL], [test x$USBCTRL = xtrue])

AC_ARG_ENABLE([wifihal],
         AS_HELP_STRING([--enable-wifihal],[enable wifihal (default is no)]),
         [
           case "${enableval}" in
              yes) WIFIHAL=true
                   AS_IF([test x$CLIENT = xtrue], [SUBDIR_CLIENT+=" WIFIHAL_stub"],
                          [echo box type not specified]) ;;
             no) WIFIHAL=false ;;
            *) AC_MSG_ERROR([bad value ${enableval} for --enable-wifihal ]) ;;
             esac
            ],
           [echo "wifihal component is not enabled"])
AM_CONDITIONAL([WIFIHAL], [test x$WIFIHAL = xtrue])

AC_ARG_ENABLE([trace],
              AS_HELP_STRING([--enable-trace],[enable trace (default is no)]),
              [
                      case "${enableval}" in
                 yes) COPTS="$COPTS -DDEBUG_LEVEL_TRACE"
                      echo "DEBUG_LOG_LEVEL : TRACE";;
                 no)  AC_MSG_ERROR([trace is disabled]) ;;
                 *) AC_MSG_ERROR([bad value ${enableval} for --enable-trace]) ;;
                       esac
                  ],
                  )

AC_ARG_ENABLE([log],
              AS_HELP_STRING([--enable-log],[enable log (default is no)]),
              [
                      case "${enableval}" in
                 yes) COPTS="$COPTS -DDEBUG_LEVEL_LOG"
                      echo "DEBUG_LOG_LEVEL : LOG";;
                 no)  AC_MSG_ERROR([log is disabled]) ;;
                 *) AC_MSG_ERROR([bad value ${enableval} for --enable-log]) ;;
                       esac
                  ],
                  )

AC_ARG_ENABLE([errorlog],
              AS_HELP_STRING([--enable-errorlog],[enable errorlog (default is no)]),
              [
                      case "${enableval}" in
                 yes) COPTS="$COPTS -DDEBUG_LEVEL_ERROR"
                      echo "DEBUG_LOG_LEVEL : ERROR";;
                 no)  AC_MSG_ERROR([errorlog is disabled]) ;;
                 *) AC_MSG_ERROR([bad value ${enableval} for --enable-errorlog]) ;;
                       esac
                  ],
                  )

PKG_CHECK_MODULES([XML2], [libxml-2.0 >= 2.7.8])
PKG_CHECK_MODULES([JANSON],[jansson >= 2.4])

AC_SUBST(COPTS)
AC_SUBST(AGENT_FLAGS)
AC_SUBST(DVRMGR_FLAGS)
AC_SUBST(CONFIG_PREFIX)
AC_SUBST(RDK_VERSION)
AC_SUBST(QAM_LIBS)
AC_SUBST(SF_LIBS)
AC_SUBST(TDK_GST_LIBS)
AC_SUBST(SUBDIR_HYBRID)
AC_SUBST(SUBDIR_CLIENT)
AC_SUBST(SM_STUB_CFLAG_HYBRID)
AC_CONFIG_FILES([Makefile
         cfg/Makefile
         agent/Makefile
         IARMBUS_stub/Makefile
         DS_stub/Makefile
         RDKLogger_stub/Makefile
	 NetSrvMgr_stub/Makefile
         TR069_stub/Makefile
         TRM_stub/Makefile
         XUPNP_stub/Makefile
         DTCP_stub/Makefile
         SNMP_stub/Makefile
         MocaHal_stub/Makefile
         Bluetooth_stub/Makefile
	 AudioCaptureMgr_stub/Makefile
	 USBCtrl_stub/Makefile
	 SystemUtil_stub/Makefile
	 WIFIHAL_stub/Makefile])
AC_OUTPUT
