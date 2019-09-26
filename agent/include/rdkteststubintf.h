/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
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

#ifndef __RDK_TEST_STUB_INTF__
#define __RDK_TEST_STUB_INTF__

#include <string>
#include <jsonrpccpp/server.h>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN	
#define OUT
class RDKTestAgent;
/**************************************************************************************
 Description   : This Class provides provides interface for the modules.
 
 **************************************************************************************/
class RDKTestStubInterface
{
    public:

        /* Constructor */
        RDKTestStubInterface(){}

        /* Destructor */
        virtual ~RDKTestStubInterface(){}

        virtual std::string testmodulepre_requisites() = 0;
        virtual bool testmodulepost_requisites() = 0;
        virtual bool initialize(IN const char* szVersion) = 0;
        //virtual bool initialize(IN const char* szVersion, IN TcpSocketServer *ptrAgentObj) = 0;
        //virtual bool cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj) = 0;
        virtual bool cleanup(IN const char* szVersion) = 0;
		
}; /* End of RDKTestStubInterface */

#endif //__RDK_TEST_STUB_INTF__
