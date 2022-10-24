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

#!/usr/bin/python

import os
import sys
import subprocess
import time
#import argparse


try:
    JAVA_VERSION = subprocess.Popen(['java','-version'])
    out = JAVA_VERSION.communicate()
    #version_name=str(sys.argv[0])
    GRAILS_VERSION = subprocess.Popen(['grails','-version'])
    out = GRAILS_VERSION.communicate()
    current_directory = os.getcwd()

    if(os.path.isdir(current_directory+'/FOLDER')):
        subprocess.check_output(['rm','-rf','./FOLDER'])

    subprocess.check_output(['mkdir','-p','FOLDER/B'])
    subprocess.check_output(['mkdir','-p','FOLDER/ADV'])
    subprocess.check_output(['mkdir','-p','FOLDER/C'])
    #version_name
    #if(len(sys.argv)==0): 
    if((len(sys.argv))==1):
    #cloning tdk generic code
        #version=sys.argv[0]
        os.chdir('./FOLDER')
        #version_name = raw_input("Please enter release tag name? ")
        #print("current tag name :".str(version_name))
        clone_tdk_generic = subprocess.Popen(['git','clone','https://code.rdkcentral.com/r/rdk/tools/tdk'])
        out = clone_tdk_generic.communicate()
        #clone_tdk_generic = subprocess.Popen(['git','clone','-b','%s'%version_name,'https://code.rdkcentral.com/r/rdk/tools/tdk'])
    
        #out = clone_tdk_generic.communicate()

        #cloning tdk-b generic code
        os.chdir('./B')
        clone_tdk_b_generic = subprocess.Popen(['git','clone','https://code.rdkcentral.com/r/rdkb/tools/tdkb'])
        out = clone_tdk_b_generic.communicate()
        #clone_tdk_b_generic = subprocess.Popen(['git','clone','-b','%s'%version_name,'https://code.rdkcentral.com/r/rdkb/tools/tdkb'])
        #out = clone_tdk_b_generic.communicate()

        #cloning tdk-c generic code
        os.chdir('../C')
        clone_tdk_c_generic = subprocess.Popen(['git','clone','https://code.rdkcentral.com/r/rdkc/tools/tdkc'])
        out = clone_tdk_c_generic.communicate()
        #clone_tdk_c_generic = subprocess.Popen(['git','clone','-b','%s'%version_name,'https://code.rdkcentral.com/r/rdkc/tools/tdkc'])
        #out = clone_tdk_c_generic.communicate()

        os.chdir('..')
        #subprocess.check_output(['cp','/home/jnode/Rahim/DOcker_test_setup/BuildConfig.groovy','./tdk/framework/grails-app/conf'])
        subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
        subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKC'])
        subprocess.check_output(['cp','-r','./B/tdkb/testscripts/RDKB/component','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
        subprocess.check_output(['cp','-r','./C/tdkc/testscripts/RDKC/component','./tdk/framework/web-app/fileStore/testscriptsRDKC'])
        
        os.chdir('./tdk/framework/')
        clean_out = subprocess.Popen(['grails','clean'])
        out = clean_out.communicate()

        #creating tdk war
        war_out = subprocess.Popen(['grails','prod','war','rdk-test-tool.war'])
        out = war_out.communicate()

        current_directory = os.getcwd()

        ls_tdk_framework = subprocess.Popen(['ls'])
        out = ls_tdk_framework.communicate()

        ls_tdk_mysql_database = subprocess.Popen(['ls','../mysql-database/'])
        out = ls_tdk_mysql_database.communicate()

        subprocess.check_output(['cp','./rdk-test-tool.war','/mnt'])
        subprocess.check_output(['cp','../mysql-database/rdktestproddbdump.sql','/mnt'])

        ls_mnt = subprocess.Popen(['ls','/mnt'])
        out = ls_tdk_mysql_database.communicate()

        print "rdk-test-tool.war annd rdktestproddbdump.sql copied to /mnt"
    elif ((len(sys.argv))==2):
        #version_name=str(sys.argv[1])
        fileName=sys.argv[1]
        if(fileName.startswith('RDKV_')): 
            os.chdir('./FOLDER')
             #version_name = raw_input("Please enter release tag name? ")
            #print("current tag name :".str(version_name))
            clone_tdk_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdk/tools/tdk'])
            out = clone_tdk_generic.communicate()

            #cloning tdk-b generic code
            #os.chdir('./B')
            #clone_tdk_b_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdkb/tools/tdkb'])
            #out = clone_tdk_b_generic.communicate()

            #cloning tdk-c generic code
            #os.chdir('../C')
            #clone_tdk_c_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdkc/tools/tdkc'])
            #out = clone_tdk_c_generic.communicate()

            #os.chdir('..')
            #subprocess.check_output(['cp','/home/jnode/Rahim/DOcker_test_setup/BuildConfig.groovy','./tdk/framework/grails-app/conf'])
            #subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
            #subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKC'])
            #subprocess.check_output(['cp','-r','./B/tdkb/testscripts/RDKB/component','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
            #subprocess.check_output(['cp','-r','./C/tdkc/testscripts/RDKC/component','./tdk/framework/web-app/fileStore/testscriptsRDKC'])

            os.chdir('./tdk/framework/')
            clean_out = subprocess.Popen(['grails','clean'])
            out = clean_out.communicate()

            #creating tdk war
            war_out = subprocess.Popen(['grails','prod','war','rdk-test-tool.war'])
            out = war_out.communicate()

            current_directory = os.getcwd()

            ls_tdk_framework = subprocess.Popen(['ls'])
            out = ls_tdk_framework.communicate()

            ls_tdk_mysql_database = subprocess.Popen(['ls','../mysql-database/'])
            out = ls_tdk_mysql_database.communicate()

            subprocess.check_output(['cp','./rdk-test-tool.war','/mnt'])
            subprocess.check_output(['cp','../mysql-database/rdktestproddbdump.sql','/mnt'])

            ls_mnt = subprocess.Popen(['ls','/mnt'])
            out = ls_tdk_mysql_database.communicate()

            print "rdk-test-tool.war annd rdktestproddbdump.sql copied to /mnt"
        else:
            os.chdir('./FOLDER')
            #version_name = raw_input("Please enter release tag name? ")
            #print("current tag name :".str(version_name))
            clone_tdk_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdk/tools/tdk'])
            out = clone_tdk_generic.communicate()



            #cloning tdk-b generic code
            os.chdir('./B')
            clone_tdk_b_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdkb/tools/tdkb'])
            out = clone_tdk_b_generic.communicate()

            #cloning tdk-c generic code
            os.chdir('../C')
            clone_tdk_c_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdkc/tools/tdkc'])
            out = clone_tdk_c_generic.communicate()

            os.chdir('..')
            subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
            subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKC'])
            subprocess.check_output(['cp','-r','./B/tdkb/testscripts/RDKB/component','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
            subprocess.check_output(['cp','-r','./C/tdkc/testscripts/RDKC/component','./tdk/framework/web-app/fileStore/testscriptsRDKC'])

            os.chdir('./tdk/framework/')
            clean_out = subprocess.Popen(['grails','clean'])
            out = clean_out.communicate()

            #creating tdk war
            war_out = subprocess.Popen(['grails','prod','war','rdk-test-tool.war'])
            out = war_out.communicate()

            current_directory = os.getcwd()

            ls_tdk_framework = subprocess.Popen(['ls'])
            out = ls_tdk_framework.communicate()

            ls_tdk_mysql_database = subprocess.Popen(['ls','../mysql-database/'])
            out = ls_tdk_mysql_database.communicate()
            subprocess.check_output(['cp','./rdk-test-tool.war','/mnt'])
            subprocess.check_output(['cp','../mysql-database/rdktestproddbdump.sql','/mnt'])

            ls_mnt = subprocess.Popen(['ls','/mnt'])
            out = ls_tdk_mysql_database.communicate()
            print "rdk-test-tool.war annd rdktestproddbdump.sql copied to /mnt"
    else:
        filename=sys.argv[2]
        if(filename=="license=advanced") or (filename=="advanced"):
            #cloning tdk generic code
            os.chdir('./FOLDER')
           #clone_tdk_generic = subprocess.Popen(['git','clone','https://code.rdkcentral.com/r/rdk/tools/tdk'])
            clone_tdk_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdk/tools/tdk'])
            out = clone_tdk_generic.communicate()

            #cloning tdk-b generic code
            os.chdir('./B')
           #clone_tdk_b_generic = subprocess.Popen(['git','clone','https://code.rdkcentral.com/r/rdkb/tools/tdkb'])
            clone_tdk_b_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdkb/tools/tdkb'])
            out = clone_tdk_b_generic.communicate()

            #cloning tdk-c generic code
            os.chdir('../C')
           # clone_tdk_c_generic = subprocess.Popen(['git','clone','https://code.rdkcentral.com/r/rdkc/tools/tdkc'])
            clone_tdk_c_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/rdkc/tools/tdkc'])
            out = clone_tdk_c_generic.communicate()
    
            #cloning adv generic code
            os.chdir('../ADV')
           # clone_tdk_adv_generic = subprocess.Popen(['git','clone','https://code.rdkcentral.com/r/tools/tdk-advanced'])
            clone_tdk_adv_generic = subprocess.Popen(['git','clone','-b','%s'%sys.argv[1],'https://code.rdkcentral.com/r/tools/tdk-advanced'])
            out = clone_tdk_adv_generic.communicate()
   
   
            os.chdir('..')
            subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
            subprocess.check_output(['mkdir','./tdk/framework/web-app/fileStore/testscriptsRDKC'])
            subprocess.check_output(['cp','-r','./B/tdkb/testscripts/RDKB/component','./tdk/framework/web-app/fileStore/testscriptsRDKB'])
            subprocess.check_output(['cp','-r','./C/tdkc/testscripts/RDKC/component','./tdk/framework/web-app/fileStore/testscriptsRDKC'])
            subprocess.check_output(['cp','-r','./ADV/tdk-advanced/framework/web-app/fileStore/','./tdk/framework/web-app/'])
            subprocess.check_output(['rm','-rf','./tdk/framework/web-app/fileStore/testscriptsTCL'])
    
    
            os.chdir('./tdk/framework/')
            clean_out = subprocess.Popen(['grails','clean'])
            out = clean_out.communicate()

            #creating tdk war
            war_out = subprocess.Popen(['grails','prod','war','rdk-test-tool.war'])
            out = war_out.communicate()

            current_directory = os.getcwd()

            ls_tdk_framework = subprocess.Popen(['ls'])
            out = ls_tdk_framework.communicate()

            ls_tdk_mysql_database = subprocess.Popen(['ls','../mysql-database/'])
            out = ls_tdk_mysql_database.communicate()

            subprocess.check_output(['cp','./rdk-test-tool.war','/mnt'])
            subprocess.check_output(['cp','../mysql-database/rdktestproddbdump.sql','/mnt'])

            ls_mnt = subprocess.Popen(['ls','/mnt'])
            out = ls_tdk_mysql_database.communicate()

            print "rdk-test-tool.war annd rdktestproddbdump.sql copied to /mnt"
            
        else:
            print "Please mention license tag for Advaned repo contents"
    #   filename = sys.argv[1]
    #   args = dict([arg.split('=', maxsplit=1) for arg in sys.argv[2:]])
    #   print "key value"
except:
    e = sys.exc_info()[1]
    print "Error occured : " + str(e)
    sys.exit()
