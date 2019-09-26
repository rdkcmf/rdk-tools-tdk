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
include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     += -c -g -Wall -DGCC4_XXX -Wno-format -Wunused


LDOPTS    +=    -L $(IMAGE_PATH)/usr/local/lib \
		-L $(IMAGE_PATH)/mnt/nfs/bin
	
INCLUDES  +=	-I $(RDK_BUILD_DIR)/devicesettings/ds/include -I $(RDK_BUILD_DIR)/devicesettings/ds -I $(RDK_BUILD_DIR)/logger/include/ -I $(RDK_BUILD_DIR)/devicesettings/hal/include/ -I $(RDK_BUILD_DIR)/iarmbus/core/include -I $(RDK_BUILD_DIR)/iarmbus/core -I$(RDK_BUILD_DIR)/iarmmgrs/generic/ir/include -I $(RDK_BUILD_DIR)/iarmmgrs/generic/mfr/include -I $(RDK_BUILD_DIR)/iarmmgrs/generic/power/include \
 		-I$(PLATFORM_SDK)/include \
	 	-I$(JSONRPC_PATH)/include \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)

#debug log level
ifeq ($(DEBUG_LEVEL),TRACE)
COPTS     += -DDEBUG_LEVEL_TRACE
endif
ifeq ($(DEBUG_LEVEL),LOG)
COPTS     += -DDEBUG_LEVEL_LOG
endif
ifeq ($(DEBUG_LEVEL),ERROR)
COPTS     += -DDEBUG_LEVEL_ERROR
endif

		
INCLUDES  += 	-I./include \
		-I../agent/include 
LDOPTS	  +=	-ldshalcli \
		-lds \
		-lglib-2.0 \
		-llog4c 
LIBOPTS   := -shared
CC	  := g++
LIBDS	  := libdevicesettingsstub.so	

ifeq ($(RDK_VERSION),RDK1DOT2)
LDOPTS    += -llogger
endif
ifeq ($(RDK_VERSION),RDK1DOT3)
LDOPTS    += -lrdklogger
endif


#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBDS)
SOURCES   := $(SRC_DIR)*.cpp

#
# Intermediate files
#
OBJS       =$(OBJDIR)/*.o

#
# Compile source files into intermediate files
#
$(OBJS): $(SOURCES) 
	mkdir -p $(OBJDIR)
	$(CROSSCOMPILE)$(CC) -Wall -std=c++0x $(INCLUDES) -fPIC $(COPTS) $^
	mv *.o $(OBJDIR)


#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	mkdir -p $(LIBDIR)
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBDS) $(LDOPTS)
	rm -rf $(OBJDIR)
	mv $(LIBDS) $(LIBDIR)
#
# Build everything
#
build: $(LIB) 

#
# Clean 
#
clean:
	rm -rf $(OBJDIR)
	rm -rf $(LIB)
