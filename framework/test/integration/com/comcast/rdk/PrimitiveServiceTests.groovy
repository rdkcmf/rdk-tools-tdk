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
package com.comcast.rdk;

import static org.junit.Assert.*;
import org.codehaus.groovy.grails.web.context.ServletContextHolder as SCH


class PrimitiveServiceTests
{
    
    def primitivetestService
    
    def grailsApplication
    
    private void testPopulateModules() {
        
       println grailsApplication.config.modules.xmlfile.location
       String xmlFile =  SCH.servletContext.getRealPath( grailsApplication.config.modules.xmlfile.location );
       
       primitivetestService.parseAndSaveStubXml();
    }
    
    private void testJsonData() {
        primitivetestService.parseAndSaveStubXml();
        PrimitiveTest primitiveTest = new PrimitiveTest()
        primitiveTest.name = " Test 1"
        Module module = Module.findByName("Ocap")
        primitiveTest.module = module
        Function function = Function.findByName("play")
        primitiveTest.function = function
        Parameter parameter1 = new Parameter();
        ParameterType paramType1 = ParameterType.findByName("locator")
        parameter1.value = "3"
        parameter1.parameterType = paramType1
        
        if(!parameter1.save()) {
            println parameter1.errors
        }
        
        Parameter parameter2 = new Parameter();
        ParameterType paramType2 = ParameterType.findByName("frequency")
        parameter2.value = "50"
        parameter2.parameterType = paramType2
        
        if(!parameter2.save()) {
            println parameter2.errors
        }
        
        if(!primitiveTest.save()) {
            println primitiveTest
        }
        else {
            primitiveTest.addToParameters(parameter1)
            primitiveTest.addToParameters(parameter2)
        }
        
        println primitivetestService.getJsonData(primitiveTest)
        
        
        
    }
    
    void testExecute() {
//        primitivetestService.executeScript("print 'test'")
        println grailsApplication.config.EXEC_PATH
    }
    
    

}
