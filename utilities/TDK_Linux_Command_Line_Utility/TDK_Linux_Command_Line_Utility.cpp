/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2018 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <unistd.h>

using namespace std;

int headerEnd;

//Function to display the available options
static void printOptions (string file)
{
    cout <<"\nMenu \n\n";
    string text;
    int lineno = 1;
    headerEnd=0;
    ifstream ifs(file.c_str());

    if (ifs.is_open())
    {
        while(!ifs.eof()) 
        {
            getline(ifs,text);
            if (text.find("#") != std::string::npos or text.empty())
            {
                headerEnd++;
                continue;
            }
            else
            {
                cout << lineno <<"."<<text << "\n" ;
                lineno++;
            }
        }
    ifs.close();
    }
    else
        cout << "\n\nUnable to open the configuration file\n\n";

    cout <<"99.Unload and Exit\n\n";

    headerEnd--;
    return;
}

//Function to get the user selection from available options
static int getUserSelection (void)
{
    int mychoice = 0;
    cout << "\nEnter a choice : ";
    cin >> mychoice;
    getchar();
    return mychoice;
}

//Function to get the reponse of JSON message
string getStdoutFromCommand(string cmd) 
{
    string data;
    FILE * stream;
    const int max_buffer = 256;
    char buffer[max_buffer];
    cmd.append(" 2>&1");
    
    stream = popen(cmd.c_str(), "r");
    if (stream)
    {
        while (!feof(stream))
        if (fgets(buffer, max_buffer, stream) != NULL)
            data.append(buffer);
        pclose(stream);
    }
    else
    {
        cout << "popen() failure";
    }
return data;
}

//Function to get the stub function name from configuration file
string getStubFunctionName(int lineNo , string file)
{
    ifstream ifs(file.c_str());
    string s;
    lineNo += headerEnd;
    if (ifs.is_open())
    {
        for (int i = 1; i <= lineNo; i++)
            std::getline(ifs, s);
        ifs.close();
    }
    else
        cout << "\n\nUnable to open the configuration file\n\n";
    
    return s;
}

//Function to get string values
string getString (string name)
{
    cin>>name;
    return name;
}

//Main
int main(int argc, char *argv[])
{
    if ( argc <= 2 )
        cout << "\n\nUsage : <binary name> <box ip> <configuration file name> \n\n";

    else if ( argc ==3 )
    {
        int loop = 1, i = 0 , paramType = 0, pos = 0;
        string moduleName,command;
        string stubFnName,stubFunWithParameters,parameters,boxIP,configFile,output;
        boxIP =  argv[1];
        configFile = argv[2];
        cout << "\n\nEnter the module name to load ( Example : Enter \"bluetooth\" to load libbluetoothstub.so.0.0.0 ) : ";
        moduleName = getString(moduleName);

        //JSON message to load a module
        command = "echo '{\"jsonrpc\":\"2.0\",\"id\":\"2\",\"method\":\"loadModule\",\"params\":{\"param1\":\""+moduleName+"\",\"version\":\"2.0\", \"execID\":\"31253\",\"deviceID\":\"568\",\"testcaseID\":\"4664\", \"execDevID\":\"30873\",\"resultID\":\"914855\", \"performanceBenchMarkingEnabled\":\"false\", \"performanceSystemDiagnosisEnabled\":\"false\"}}' | nc "+boxIP+" 8088";
        output = getStdoutFromCommand(command);

        cout << "\n\n" << moduleName << " Load Module Details : " << output << endl;

        do 
        {
            printOptions(configFile);
            i = getUserSelection();
            stubFnName = getStubFunctionName(i,configFile); 
            if ( i == 99 )
                break;
            if ( stubFnName == "" )
            {
                cout <<"\n\nInvalid Menu Choice : Please enter a valid Menu Choice \n\n";
                continue;
            }
            pos = stubFnName.find("=");

            if ( pos <= 1 )
            {
                    //JSON message for stub function which is not needed any parameters as input
                    command = "echo '{\"params\": {\"method\": \""+stubFnName+"\", \"module\": \""+moduleName+"\"}, \"jsonrpc\": \"2.0\", \"id\": \"2\", \"method\": \"executeTestCase\"}' | nc "+boxIP+" 8088";

                    //Executing the JSON message
                    output = getStdoutFromCommand(command);
      
                    cout << "\n\n" << stubFnName << " -- Execution Response : " << output << endl;
            }

            else
            {
                stubFunWithParameters = stubFnName.substr (0,pos-1); 
                parameters = stubFnName.substr (pos+2);

                cout <<"\n\nParameters of stub function " << stubFunWithParameters << " : "<< parameters;

                int count =0;
                int n = parameters.length();
                char char_array[n+1];
                strcpy(char_array, parameters.c_str());
                
                char * pch;
                string params="";
                params.append("{");
                pch = strtok (char_array,",");

                //Loop to frame JSON parameters after reading from configuration file
                while (pch != NULL)
                {
                  string str(pch);
                  string parameterValue;
                  params.append("\""+str+"\": ");
                  pch = strtok (NULL, ","); 
                  string paramType(pch);
                  if (paramType == "string")
                  {
                      cout << "\n\nPlease Enter the value that you want to set for " << str  << ": ";
                      parameterValue = getString(parameterValue);
                      params.append("\""+parameterValue+"\"");
                  }
                  else if (paramType == "integer")
                  {
                      cout << "\n\nPlease Enter the value that you want to set for " << str  << ": ";
                      parameterValue = getString(parameterValue);
                      params.append(parameterValue);
                  }
                  else
                  {
                       cout << "\n\nInvalid parameter option\n";
                  }

                  count ++;
                  pch = strtok (NULL, ",");
                  if (pch != NULL)
                  { 
                      params.append(",");
                  }
                }
                
                params.append("}");

                //JSON message for stub function which needed parameters as input
                command = "echo '{\"jsonrpc\": \"2.0\", \"params\": {\"params\":"+params+", \"method\": \""+stubFunWithParameters+"\", \"module\": \""+moduleName+"\"}, \"id\": \"2\", \"method\": \"executeTestCase\"}' | nc "+boxIP+"  8088";
           
                //Executing the JSON message
                output = getStdoutFromCommand(command);
                cout << "\n\n" << stubFunWithParameters << " -- Execution Response : " << output << endl;
   
            }

        }while(i != 99);
      
        //JSON message to unload a module 
        command = "echo '{\"jsonrpc\":\"2.0\",\"id\":\"2\",\"method\":\"unloadModule\",\"params\":{\"param1\":\""+moduleName+"\",\"version\":\"1.3\",\"ScriptSuiteEnabled\":\"false\"}}' | nc "+boxIP+" 8088";
        output = getStdoutFromCommand(command);

        cout << "\n\n" << moduleName << " Unload Module Details : " << output << endl;
    }

    else
       cout << "\n\nUsage : <binary name> <box ip> <configuration file name> \n\n";

    return 0;
}
