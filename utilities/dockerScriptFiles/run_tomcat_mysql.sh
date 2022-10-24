##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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

#!/bin/bash

# Start the first process
service mysql start -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start mysql: $status"
  exit $status
fi

#Wait for 10 seconds
echo "Sleeping for 10 seconds"
sleep 10

# Start the second process
/etc/init.d/tomcat7 start -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start tomcat: $status"
  exit $status
fi

while sleep 10; do
  TOMCAT_PID=$(ps aux | grep org.apache.catalina.startup.Bootstrap | grep -v grep | awk '{ print $2 }')
  MYSQL_PID=$(ps aux | grep /usr/sbin/mysqld | grep -v grep | awk '{ print $2 }')
  if 
  [ ! -n "$TOMCAT_PID" ] || 
  [ ! -n "$MYSQL_PID" ]
  then
      echo "One of the processes has already exited."
      echo "Tomcat PID : "$TOMCAT_PID
      echo "Mysql PID : "$MYSQL_PID
  fi
done
