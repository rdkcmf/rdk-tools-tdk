#!/usr/bin/python
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
#  Author : Ajan U. Nair
#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import MySQLdb
import os       
import sys   
import re
import string
from xml.dom.minidom import Text, Element,Document,getDOMImplementation,Comment
from mySQLConfig import *

#-----------------------------------Edit this section  to configure your mysql database connection--------------------
hostName="localhost"
databaseName="rdktesttoolproddb_test"
#databaseName="rdktesttoolproddb_M13_ajjuly15"
#-----------------------------------------------------------------------------------------------------------------
targetFolder="./scriptsDump"




#if not os.path.isdir("./scriptsDump/"):
#	print "Creating new directory - scriptsDump in the working directory"	 
#	os.mkdir("./scriptsDump/")
#else:
#	print ".py files in scriptsDump directory will be overwritten. Do you want to continue? y/n "
#	choice = raw_input().lower();
#	if (choice != 'y'):	
#		sys.exit()
	

def addChildToNodeElement(nodeElement,childName,text,commentText=""):
	txtEle=Text()
	tmpStr=str(text)
	tmpStr=re.sub("[^\x00-\x7F]","|",tmpStr) #Replace non-ascii chars
	txtEle.data=tmpStr
	childEle=Element(childName)
	childEle.appendChild(txtEle)
	nodeElement.appendChild(childEle)
	commentEle=Comment(commentText)
	nodeElement.appendChild(commentEle)


def importScriptsFromDb(option,moduleName,filepath):

	if option=="-all":
		query = "SELECT * FROM script";
	elif option=="-m":
		query = "select * from script where primitive_test_id in ( select id from primitive_test where module_id in (select id from module where name = '"+moduleName+"'))"
	
	cur.execute(query);
	rows = cur.fetchall();
	if len(rows) ==0:
		print "There is no script satisfying the given criteria: "+query
		sys.exit()
	
	for row in rows:
		rootXml=Element('xml')
		addChildToNodeElement(rootXml,'id',row[0],"Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty")
		addChildToNodeElement(rootXml,'version',row[1],"Do not edit version. This will be auto incremented while exporting. If you are adding a new script you can keep the vresion as 1")
		addChildToNodeElement(rootXml,'name',row[2]," If you are adding a new script you can specify the script name.")
		addChildToNodeElement(rootXml,'primitive_test_id',row[3],"Do not change primitive_test_id if you are editing an existing script.")
		cur.execute("SELECT name,version  FROM primitive_test where id = "+str(row[3]))
		primitive = cur.fetchone();
		
		addChildToNodeElement(rootXml,'primitive_test_name',primitive[0])
		addChildToNodeElement(rootXml,'primitive_test_version',primitive[1])
		addChildToNodeElement(rootXml,'status',row[5])
		addChildToNodeElement(rootXml,'synopsis',row[6])
		addChildToNodeElement(rootXml,'groups_id',row[7],"If groups_id = None , it will be defaulted to 2 ")
		addChildToNodeElement(rootXml,'execution_time',row[8],"execution_time is the time out time for test execution")

		if row[11]==b'\x00':
			addChildToNodeElement(rootXml,'long_duration','False')
		else:
			addChildToNodeElement(rootXml,'long_duration','True')

		addChildToNodeElement(rootXml,'remarks',row[9])

		if row[10]==b'\x00':
			addChildToNodeElement(rootXml,'skip','False')
		else:
			addChildToNodeElement(rootXml,'skip','True')
			
		
		
		cur.execute("SELECT * FROM script_box_type where script_box_types_id = "+str(row[0]))
		typesRows = cur.fetchall();

		box_TypesEle=Element('box_types')
		for typesRow in typesRows:
			cur.execute("SELECT * FROM box_type where id = "+str(typesRow[1]))
			typeNameRows = cur.fetchall();
			for typeNameRow in typeNameRows:
				addChildToNodeElement(box_TypesEle,'box_type',typeNameRow[2])
		rootXml.appendChild(box_TypesEle)
		
		cur.execute("SELECT * FROM script_rdkversions where script_rdk_versions_id = "+str(row[0]))
		versionRows = cur.fetchall();

		rdk_versionsEle=Element('rdk_versions')
		for versionRow in versionRows:
			cur.execute("SELECT * FROM rdkversions where id = "+str(versionRow[1]))
			versNameRows = cur.fetchall();
			for versNameRow in versNameRows:
				addChildToNodeElement(rdk_versionsEle,'rdk_version',versNameRow[2])
		rootXml.appendChild(rdk_versionsEle)


		cur.execute("SELECT name FROM module WHERE id =(SELECT module_id FROM primitive_test WHERE id ="+str(row[3])+")")
		moduleName=cur.fetchone()
		print "moduleName="+moduleName[0]
		if not os.path.exists(filepath+"/"+moduleName[0]):
			os.makedirs(filepath+"/"+moduleName[0])
		fileName=row[2]
		fileName=fileName.replace(' ','_') 
		print fileName
		fo = open(filepath+"/"+moduleName[0]+"/"+fileName+".py", "wb")
		print rootXml.toprettyxml()
		fo.write("'''\n");
		fo.write("<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>"+rootXml.toprettyxml(encoding="ASCII"))
		fo.write("'''\n\n");
		fo.write(row[4])#index 4 is for script content
		fo.close()
	conn.commit();
	conn.close();
 
def showUsage():
        print "python scriptDb2File.py [[-all][<foldername>]][[-m <modulename>]]"
        print "scriptDb2File.py will import scripts from database to files.It will create  xml headers for files,which will help export back to the database"
        print "You should edit the databse connection line on top of this script to connect to your databse"

def confirmTheAction(folder):
	print "Do you want to import the scripts from the database:  "+databaseName+" at "+hostName+ " to the folder: "+ folder+ " ?"
	print "This will overwirte existing files in this folder!!!! Do you want to continue? y/n "
	choice = raw_input().lower();
	if (choice != 'y'):
		sys.exit()


conn = MySQLdb.connect (host = hostName, user = username, passwd = password, db = databaseName)
cur = conn.cursor()

if (len(sys.argv)== 2 ):
        if (sys.argv[1] == "-all") and( os.path.exists(targetFolder)):
		confirmTheAction(targetFolder)
                importScriptsFromDb("-all","",targetFolder)
        else :
                if not ( os.path.exists(sys.argv[1])):
                        print sys.argv[1]+" :Invalid file/path"
                        showUsage()
                else:
			confirmTheAction(sys.argv[1])
                        importScriptsFromDb("-all","",sys.argv[1])
elif(len(sys.argv) == 3 ) :
	if sys.argv[1] == "-all" :
		if not( os.path.isdir(sys.argv[2])):
			print sys.argv[2]+" :Invalid folder"
			showUsage()
		else:
			confirmTheAction(sys.argv[2])
			importScriptsFromDb("-all","",sys.argv[2])

	elif  sys.argv[1] == "-m" :
		confirmTheAction(targetFolder)		
		importScriptsFromDb("-m",sys.argv[2],targetFolder)
elif (len(sys.argv) == 4 ) :	
	if sys.argv[1] == "-m" :
                if not( os.path.isdir(sys.argv[3])):
                        print sys.argv[3]+" :Invalid folder"
                        showUsage()
		else:
			confirmTheAction(sys.argv[3])
			importScriptsFromDb("-m",sys.argv[2],sys.argv[3])

else:
	print "Invalid Arguments. More/Less arguments than expected"
	showUsage()

