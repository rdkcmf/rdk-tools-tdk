#!/bin/bash
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

#######################################
#
# Build Framework standard script for
#
#RDKTDK Test tool

# use -e to fail on any shell issue
# -e is the requirement from Build Framework
########################################
set -x


# default PATHs - use `man readlink` for more info
# the path to combined build
export RDK_PROJECT_ROOT_PATH=${RDK_PROJECT_ROOT_PATH-`readlink -m ..`}
export COMBINED_ROOT=$RDK_PROJECT_ROOT_PATH
echo "path":$RDK_PROJECT_ROOT_PATH
# path to build script (this script)
export RDK_SCRIPTS_PATH=${RDK_SCRIPTS_PATH-`readlink -m $0 | xargs dirname`}

# path to components sources and target
export RDK_SOURCE_PATH=${RDK_SOURCE_PATH-`readlink -m .`}
export RDK_TARGET_PATH=${RDK_TARGET_PATH-$RDK_SOURCE_PATH}

# fsroot and toolchain (valid for all devices)
export RDK_FSROOT_PATH=${RDK_FSROOT_PATH-`readlink -m $RDK_PROJECT_ROOT_PATH/sdk/fsroot/ramdisk`}
export RDK_TOOLCHAIN_PATH=${RDK_TOOLCHAIN_PATH-`readlink -m $RDK_PROJECT_ROOT_PATH/sdk/toolchain/staging_dir`}

# default component name
export RDK_COMPONENT_NAME=${RDK_COMPONENT_NAME-`basename $RDK_SOURCE_PATH`}

# parse arguments
INITIAL_ARGS=$@

ENABLE_TDK=0
function usage()
{
    set +x
    echo "Usage: `basename $0` [-h|--help] [-v|--verbose] [iaction]"
    echo "    -h    --help                  : this help"
    echo "    -v    --verbose               : verbose output"
    echo
    echo "Supported actions:"
    echo "      configure, clean, build (DEFAULT), rebuild, install"
}

echo "Option received : $1"
# options may be followed by one colon to indicate they have a required argument
if ! GETOPT=$(getopt -n "build.sh" -o hvp: -l help,enable,verbose: -- "$@")
then
    usage
    exit 1
fi

eval set -- "$GETOPT"

while true; do
  case "$1" in
    -h | --help ) usage; exit 0 ;;
    -v | --verbose ) set -x ;;
    --enable ) ENABLE_TDK=0;;
    -- ) shift; break;;
    * ) break;;
  esac
  shift
done

ARGS=$@

#source ${RDK_PROJECT_ROOT_PATH}/build_scripts/setBCMenv.sh

#COMPILER=mipsel-linux-
# component-specific vars
#export PATH=$PATH:$RDK_PROJECT_ROOT_PATH/tools/stbgcc-4.5.3-2.4/bin:$RDK_PROJECT_ROOT_PATH/sdk/toolchain/staging_dir
export TDK_PATH=$RDK_SOURCE_PATH
export RDK_BUILD_DIR=$RDK_SOURCE_PATH/../
export FSROOT=${RDK_FSROOT_PATH}
export TOOLCHAIN_DIR=${RDK_TOOLCHAIN_PATH}
export OPENSOURCE_PATH=$RDK_PROJECT_ROOT_PATH/opensource
#export RDK_PLATFORM_SOC=${RDK_PLATFORM_SOC-broadcom}
#export PLATFORM_SOC=$RDK_PLATFORM_SOC

if [ "x$BUILD_CONFIG" = "xhybrid-legacy" ];then
    export BUILD_CONFIG="hybrid"
fi

if [ "x"$RDK_PLATFORM_SOC == "xintel" ]; then
	export TOOLCHAIN_DIR=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/bin
        export CROSS_COMPILE=i686-cm-linux-
	export ROOTFS_INCLUDE=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/usr/include/
	if [ "x"$BUILD_CONFIG == "x" ]; then
	  export RDK_VERSION=RDK1DOT3
	elif [ "x"$BUILD_CONFIG == "xhybrid" ]; then
	  export RDK_VERSION=RDK2DOT0
	fi
        export PLATFORM_SDK=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/
	export JSONRPC_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/jsonrpc
        export JSONCPP_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/jsoncpp
        export CURL_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/curl/include
        COMPILER=i686-cm-linux-
	export CROSS_TOOLCHAIN=$TOOLCHAIN_DIR
	export CROSS_COMPILE=$CROSS_TOOLCHAIN/$COMPILER
	export JSONRPC_LIB=jsonrpc
elif [ "x"$RDK_PLATFORM_SOC = "xbroadcom" ]; then
	export WORK_DIR=$RDK_PROJECT_ROOT_PATH/work${RDK_PLATFORM_DEVICE^^}
	source ${RDK_PROJECT_ROOT_PATH}/build_scripts/setBCMenv.sh
        echo $BCMAPP 
	export PLATFORM_SDK=$BCMAPP
	export RDK_VERSION=RDK2DOT0
	COMPILER=mipsel-linux-
	export JSONRPC_PATH=$RDK_PROJECT_ROOT_PATH/opensource/jsonrpc/
	export JSONCPP_PATH=$RDK_PROJECT_ROOT_PATH/opensource/jsoncpp/
        export CROSS_TOOLCHAIN=$TOOLCHAIN_DIR
	export CROSS_COMPILE=$COMPILER
	export ROOTFS_INCLUDE=$PLATFORM_SDK/include/
	if [ "x"$BUILD_CONFIG == "xhybrid" ]; then
                export WORK_DIR=${RDK_PROJECT_ROOT_PATH}/work${RDK_PLATFORM_DEVICE^^}
                export IMAGE_PATH=${RDK_PROJECT_ROOT_PATH}/work${RDK_PLATFORM_DEVICE^^}/rootfs/
                export CURL_PATH=$RDK_PROJECT_ROOT_PATH/opensource/include
		export TOOLCHAIN_DIR=$BCM_TOOLCHAIN/bin/
        else
                export CURL_PATH=$PLATFORM_SDK/include/curl
        fi
	export JSONRPC_LIB=jsonrpc
elif [ "x"$RDK_PLATFORM_SOC = "xstm" ]; then
        export RDK_VERSION=RDK2DOT0
        COMPILER=arm-oe-linux-gnueabi-
        export JSONRPC_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/jsonrpc/
        export JSONCPP_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/jsoncpp/
	export CROSS_TOOLCHAIN=$RDK_PROJECT_ROOT_PATH/sdk/toolchain/staging_dir/sysroots/x86_64-oesdk-linux/usr/bin/arm-oe-linux-gnueabi/
        export CROSS_COMPILE=$CROSS_TOOLCHAIN/$COMPILER
        export PLATFORM_SDK=$RDK_PROJECT_ROOT_PATH/sdk/toolchain/staging_dir/sysroots/cortexa9t2hf-vfp-neon-oe-linux-gnueabi/usr/
        export CURL_PATH=$PLATFORM_SDK/include/curl
	export JSONRPC_LIB=jsonrpc-cpp

fi
#export PLATFORM_SOC=$TDK_PLATFORM
#export TOOLCHAIN_DIR=$RDK_BUILD_PATH/sdk/toolchain/staging_dir
#export CROSS_TOOLCHAIN=$TOOLCHAIN_DIR
#export CROSS_COMPILE=$COMPILER
export CROSSCOMPILE=$CROSS_COMPILE
echo $CROSSCOMPILE
export TDK_LIB_PATH=$TDK_PATH/build/libs
export TDK_BIN_PATH=$TDK_PATH/build/bin

export LIBDIR=$TDK_LIB_PATH
export TARGETDIR=$TDK_BIN_PATH

if [ "$ENABLE_TDK" == 1 ]; then
	if [ -e "${RDK_PROJECT_ROOT_PATH}/tdk/platform/Mediaplayer_stub/mp_conf.sh" ]; then
    		echo "Mediaplayer_stub present"
    		source ${RDK_PROJECT_ROOT_PATH}/tdk/platform/Mediaplayer_stub/mp_conf.sh
	else
    		echo "pri file not present"
	fi
#for sm_stub
        if [ -e "$COMBINED_ROOT/opensource/qt/stage" ];
        then
                export QT_SRC_ROOT=${RDK_PROJECT_ROOT_PATH}/opensource/qt
        else
	        export QT_SRC_ROOT=${RDK_PROJECT_ROOT_PATH}/opensource/src/qt
        fi
        source $QT_SRC_ROOT/apps_helpers.sh
        source $QT_SRC_ROOT/setenv.sh
        PROJECT_CONFIG_SM=()
        if [ ! -d "${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/servicemanager" ]; then
                mkdir ${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/servicemanager
                cp -r ${RDK_PROJECT_ROOT_PATH}/servicemanager/include ${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/servicemanager/
                cp -r ${RDK_PROJECT_ROOT_PATH}/servicemanager/src ${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/servicemanager/
        fi

        cd ${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/
        configureProject servicemanager_tdk.pro ${PROJECT_CONFIG_SM[@]}

fi
TDK_PATH=$TDK_PATH/platform/
# functional modules

function configure()
{
    true #use this function to perform any pre-build configuration
}

function clean()
{
    cd $TDK_PATH
    make clean
    true #use this function to provide instructions to clean workspace
}

function build()
{
    cd $TDK_PATH
    make
    retCode=$?	
    echo "return value :" $retCode
    if [ $retCode -ne 0 ]; then
       echo "BUILDING tdk FAILED"
       exit $retCode
    fi
}

function rebuild()
{
    clean
    build
}

function install()
{
    touch $RDK_PROJECT_ROOT_PATH/tdk_image

    if [ -e "${RDK_PROJECT_ROOT_PATH}/tdk/platform/Mediaplayer_stub/mp_conf.sh" ]; then
        rsync -rplEogDWI --force --exclude=.svn ${RDK_PROJECT_ROOT_PATH}/tdk/cpc/Mediaplayer_stub/libmediaplayerstub.so* ${TDK_LIB_PATH}
    fi
    if [ -e "${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/src/libservicemanagerstub.so" ];then
        rsync -rplEogDWI --force --exclude=.svn ${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/src/libservicemanagerstub.so* ${TDK_LIB_PATH}
    fi
    if [ -e "${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/test/SMEventApp" ];then
        # Installing SMEventApp only for non-rng150 devices due to packaging size constraint
        if [ $RDK_PLATFORM_DEVICE != "rng150" ]; then
            cp ${RDK_PROJECT_ROOT_PATH}/tdk/SM_stub/test/SMEventApp ${TDK_BIN_PATH}
        fi
    fi
    if [ -d "${RDK_PROJECT_ROOT_PATH}/tdk/platform/SM_stub/scripts" ];then
        cp ${RDK_PROJECT_ROOT_PATH}/tdk/platform/SM_stub/scripts/* ${TDK_BIN_PATH}/scripts/
    fi
}



# run the logic

#these args are what left untouched after parse_args
HIT=false
if [ "$ENABLE_TDK" == 1 ]; then
       touch $RDK_PROJECT_ROOT_PATH/build/packager_scripts/enable_tdk   
	for i in "$ARGS"; do
    		case $i in
        		configure)  HIT=true; configure ;;
        		clean)      HIT=true; clean ;;
        		build)      HIT=true; build ;;
        		rebuild)    HIT=true; rebuild ;;
        		install)    HIT=true; install ;;
        		*)
            		#skip unknown
        		;;
    		esac
	done

# if not HIT do build by default
	if ! $HIT; then
  		build
	fi
else
echo "##TDK OPTION is not set to build the TDK##"
echo "##Use --tdk-option="enable" to build the TDK ##"
fi
