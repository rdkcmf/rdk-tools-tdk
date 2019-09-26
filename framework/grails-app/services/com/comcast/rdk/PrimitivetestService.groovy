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
package com.comcast.rdk

import static com.comcast.rdk.Constants.*
import groovy.util.slurpersupport.GPathResult
import javax.xml.parsers.ParserConfigurationException;
import org.codehaus.groovy.grails.web.context.ServletContextHolder as SCH;
import org.xml.sax.SAXException;
import com.google.gson.JsonObject;

/**
 * Service class for the PrimitiveTest domain.
 *
 */
class PrimitivetestService {
	static datasource = 'DEFAULT'
    /**
     * Injects the grailsApplication.
     */
    def grailsApplication
  
    /**
     * Throws runtime exception with the specified message.
     * @param msg
     */
    private void abortTransaction(final String msg) {
        throw new RuntimeException(msg);
    }

  
    /**
     * Returns the JSON data corresponding to the PrimitiveData.
     * sample data is 
     * <pre>
     * {"id":1,"jsonrpc":"2.0","method":"play","params":{"locator":"3","frequency":"etre"}}
     * </pre>
     * @param primitiveTest
     * @return
     * @author ajith
     */
    public JsonObject getJsonData(final def primitiveTest, String idValue) {
		
		if(idValue == null){
			idValue = ID_DEFAULT
		}
		
        log.info(" getJsonData ::::::::: "+primitiveTest?.name)        
        JsonObject outData = new JsonObject()
        if(primitiveTest){
//            outData.addProperty(KEY_ID, idValue);
//            outData.addProperty(KEY_JSONRPC, VAL_JSONRPC);
			outData.addProperty(KEY_MODULE, primitiveTest?.module?.name.trim());
            outData.addProperty(KEY_METHOD, primitiveTest?.function?.name.trim());            
			JsonObject paramsObj = new JsonObject()
            Set parameters = primitiveTest?.parameters;
            for ( Map parameter : parameters ) {
                if(parameter?.parameterType?.parameterTypeEnum.getTypeValue().equals("integer") ){
					int val = 0 ;
                    try{
                        val = Integer.parseInt(parameter?.value);
                    }catch (Exception e){
                        log.error("----Exception in converting to integer")
                    }
                    paramsObj.addProperty (parameter?.parameterType.name, val);
                }
				else if(parameter?.parameterType?.parameterTypeEnum.getTypeValue().equals("float") ){
					float floatVal = 0.0 ;
					try{
						floatVal = Float.parseFloat(parameter?.value)
					}catch (Exception e){
						log.error("----Exception in converting to float")
					}
					paramsObj.addProperty (parameter?.parameterType.name, floatVal);
				}
				else if(parameter?.parameterType?.parameterTypeEnum.getTypeValue().equals("double") ){
					double doubleVal = 0.00 ;
					try{
						doubleVal = Double.parseDouble(parameter?.value)
					}catch (Exception e){
						log.error("----Exception in converting to double")
					}
					paramsObj.addProperty (parameter?.parameterType.name, doubleVal);
				}				
                else{
                    paramsObj.addProperty( parameter?.parameterType.name, parameter?.value.trim() );
                }
            }
			if(parameters?.size() > 0){
				outData.add(KEY_PARAMS, paramsObj );
			}
        }
		
        return outData
    }

}
