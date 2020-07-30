##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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

#To free up the TDK agent ports before start listening
kill $(netstat -tunlp 2>/dev/null | grep 8087 | awk '{print $7}' | tr "/" "\n" | head -n 1)
kill $(netstat -tunlp 2>/dev/null | grep 8088 | awk '{print $7}' | tr "/" "\n" | head -n 1)

