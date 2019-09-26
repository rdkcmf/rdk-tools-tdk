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

AUTO_SEARCH_IN_JENKINS='FALSE'
SEARCH_MASTER_IN_JENKINS='TRUE'
FIRMWARELOCATION =
CDN_MOC_SERVER=

#These are helper fields to search for the latest RDK image in jenkins
#Specify the keyword which should be present in image name as 'VALID_KEYWORD'
VALID_KEYWORD=
#Mention a keyword to identify the build names to be avioded
INVALID_KEYWORD=

#test urls
XCONF_OVERRIDE_URL="https://dummy.overrideurl"
XCONF_INVALID_URL="https://xconf.invalidurl"


#If image name is to be read from this file instead of jenkins, add image name here
#image name is to be added in the format JENKINS_JOB=imagename
#JENKINS_JOB and imagename values are to be reffered from version.txt file in the device
#replace - symbol in JENKINS_JOB with _

