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

######################################################################################################
# DEBUG_LEVEL shall be TRACE/ERROR/LOG                                                               #
# RDK_VERSION shall be RDK1DOT2/RDK1DOT3/RDK2DOT0 based on the RDK version in the target box         #
# RDK_BUILD_DIR is the location where RDK source code is located                                     #
# COMPILER :Specify the compiler excluded gcc,For ex: i686-cm-linux-                                 #
# TARGETDIR :specify the folder where bianries has to be copied                                      #
# LIBDIR :specify the folder where libs has to copied                                                #
# TOOLCHAIN_DIR :Specify the toolchain folder path												     #
######################################################################################################
DEBUG_LEVEL=TRACE
#RDK_BUILD_DIR=
#TOOLCHAIN_DIR=
#COMPILER=
#RDK_VERSION=
#TARGETDIR=
#LIBDIR=
##############################Uncomment the following the following parameters##########################################
#CROSSCOMPILE=$(TOOLCHAIN_DIR)/$(COMPILER)
#RDK_PROJECT_ROOT_PATH=$(RDK_BUILD_DIR)
#JSONRPC_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/jsonrpc
#JSONCPP_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/jsoncpp
#CURL_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/curl/include
#TDK_BIN_PATH=$(TARGETDIR)
##############################Uncomment the following parameters in case of Gateway######################################
#CURL_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/curl/include
#ROOTFS_INCLUDE=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/usr/include/
###############################Uncomment the following parameters in case of client#########################################
#PLATFORM_SDK=(Export the sdk path)
#CURL_PATH=$(PLATFORM_SDK)/include
#ROOTFS_INCLUDE=$(PLATFORM_SDK)/include
