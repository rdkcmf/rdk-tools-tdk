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

#Getting Ubuntu 18.04 base image for the container
FROM ubuntu:18.04

#Setting environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_ROOT_USER=root

#TDK TM Pre-requisites installation
RUN apt-get clean && apt-get update && apt-get upgrade -y \
 && apt-get install -y --fix-missing apt-utils \
 curl \
 git \
 mysql-server \
 openjdk-8-jdk \
 python \
 expect \
 python-xlwt \
 python-xlrd \
 python-numpy \
 python-paramiko \
 python-tftpy \
 python-pycurl \
 python-mysqldb \
 python-pip \
 vim \
 net-tools \
 inetutils-ping \
 unzip \
 zip \
 wget \
 sshpass 
RUN python -m pip install selenium
RUN python -m pip install --pre --upgrade websocket-client==0.57.0
RUN pip install requests \
    pexpect \
    urllib3==1.23 \
    pillow
RUN pip install xlutils

#Setting up Mysql database
COPY mysqld.cnf /mnt
RUN /bin/bash -c "/etc/init.d/mysql stop" && sleep 5
RUN /bin/bash -c "cp /mnt/mysqld.cnf /etc/mysql/mysql.conf.d/"
RUN service mysql start && sleep 5 && mysql -u root -proot -e "DROP DATABASE IF EXISTS rdktesttoolproddb; DROP DATABASE IF EXISTS rdktesttoolproddb_temp; drop user IF EXISTS 'rdktesttooluser'@'127.0.0.1'; CREATE DATABASE IF NOT EXISTS rdktesttoolproddb ; CREATE DATABASE IF NOT EXISTS rdktesttoolproddb_temp; CREATE USER 'rdktesttooluser'@'127.0.0.1' identified by '6dktoolus3r!'; grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER ON  rdktesttoolproddb.* TO 'rdktesttooluser'@'127.0.0.1'; grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER ON  rdktesttoolproddb_temp.* TO 'rdktesttooluser'@'127.0.0.1'" && sleep 5
RUN service mysql start && sleep 5 && mysql -u root -proot -e "SELECT User, Host FROM mysql.user;"

#Java8 installation
RUN echo export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 >> ~/.bashrc
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

#Grails 2.4.0 installation
ENV GRAILS_VERSION 2.4.0
RUN wget --no-check-certificate https://github.com/grails/grails-core/releases/download/v$GRAILS_VERSION/grails-$GRAILS_VERSION.zip && \
    unzip grails-$GRAILS_VERSION.zip && \
    rm -rf grails-$GRAILS_VERSION.zip
RUN /bin/bash -c "mv grails-$GRAILS_VERSION /usr/lib/jvm"
RUN ln -s grails-$GRAILS_VERSION grails
ENV GRAILS_HOME /usr/lib/jvm/grails-$GRAILS_VERSION/
ENV PATH $GRAILS_HOME/bin:$PATH
RUN echo export GRAILS_HOME=/usr/lib/jvm/grails-$GRAILS_VERSION >> ~/.bashrc

#Apache Tomcat 7.0.96 installation
RUN wget --no-check-certificate https://archive.apache.org/dist/tomcat/tomcat-7/v7.0.96/bin/apache-tomcat-7.0.96.tar.gz && sleep 5 && tar -xvzf apache-tomcat-7.0.96.tar.gz && sleep 5
RUN /bin/bash -c "mv apache-tomcat-7.0.96 /opt"
COPY tomcat7 /etc/init.d
RUN /bin/bash -c "chmod 777 /etc/init.d/tomcat7"
RUN /bin/bash -c "chmod +x /etc/init.d/tomcat7"

#Creating rdk-test-tool.war file from TDK generic repo
COPY war_creation_generic.py /mnt
ARG tag_name=rdk-next
ENV tag_name=$tag_name
RUN /bin/bash -c "chmod 777 /mnt/war_creation_generic.py"
RUN /bin/bash -c "python /mnt/war_creation_generic.py $tag_name"
RUN sleep 50
RUN /bin/bash -c "cp /mnt/rdk-test-tool.war /opt/apache-tomcat-7.0.96/webapps"
#COPY rdk-test-tool.war /opt/apache-tomcat-7.0.96/webapps/
#COPY rdktestproddbdump.sql /mnt

#Initializing Mysql database with the latest dump from generic repo
RUN service mysql start && sleep 5 && mysql -u root -proot rdktesttoolproddb < /mnt/rdktestproddbdump.sql
RUN service mysql start

#Configuring the shell script to run tomcat and mysql process in the background
COPY run_tomcat_mysql.sh run_tomcat_mysql.sh
RUN /bin/bash -c "chmod 777 run_tomcat_mysql.sh"

#Google Chrome setup
COPY google_chrome_setup.sh google_chrome_setup.sh
RUN /bin/bash -c "chmod +x google_chrome_setup.sh"
RUN /bin/bash -c "./google_chrome_setup.sh"
RUN /bin/bash -c "rm -rf google_chrome_setup.sh"

#SVS setup
COPY svs_setup.sh svs_setup.sh
RUN /bin/bash -c "chmod +x svs_setup.sh"
RUN /bin/bash -c "./svs_setup.sh"
RUN /bin/bash -c "rm -rf svs_setup.sh"

#XConf Simulator setup
#COPY xconf_simulator_setup.sh xconf_simulator_setup.sh
#RUN /bin/bash -c "chmod +x xconf_simulator_setup.sh"
#RUN /bin/bash -c "./xconf_simulator_setup.sh"
#RUN /bin/bash -c "rm -rf xconf_simulator_setup.sh"

#Passing the shell script to CMD
CMD /bin/bash -c "./run_tomcat_mysql.sh"

#Lightning Apps setup
COPY lightning_apps_setup.sh lightning_apps_setup.sh
RUN /bin/bash -c "chmod +x lightning_apps_setup.sh"
RUN /bin/bash -c "./lightning_apps_setup.sh"
RUN /bin/bash -c "rm -rf lightning_apps_setup.sh"