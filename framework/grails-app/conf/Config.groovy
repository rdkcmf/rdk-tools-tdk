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
import org.codehaus.groovy.grails.io.support.PathMatchingResourcePatternResolver
// locations to search for config files that get merged into the main config;
// config files can be ConfigSlurper scripts, Java properties files, or classes
// in the classpath in ConfigSlurper format

// grails.config.locations = [ "classpath:${appName}-config.properties",
//                             "classpath:${appName}-config.groovy",
//                             "file:${userHome}/.grails/${appName}-config.properties",
//                             "file:${userHome}/.grails/${appName}-config.groovy"]

// if (System.properties["${appName}.config.location"]) {
//    grails.config.locations << "file:" + System.properties["${appName}.config.location"]
// }

grails.project.groupId = appName // change this to alter the default package name and Maven publishing destination
grails.mime.file.extensions = true // enables the parsing of file extensions from URLs into the request format
grails.mime.use.accept.header = false
grails.mime.types = [ html: ['text/html','application/xhtml+xml'],
                      xml: ['text/xml', 'application/xml'],
                      text: 'text-plain',
                      js: 'text/javascript',
                      rss: 'application/rss+xml',
                      atom: 'application/atom+xml',
                      css: 'text/css',
                      csv: 'text/csv',
                      pdf: 'application/pdf',
                      rtf: 'application/rtf',
                      excel: 'application/vnd.ms-excel',
                      ods: 'application/vnd.oasis.opendocument.spreadsheet',
                      all: '*/*',
                      json: ['application/json','text/json'],
                      form: 'application/x-www-form-urlencoded',
                      multipartForm: 'multipart/form-data',
					  jnlp: 'application/x-java-jnlp-file'
                    ]



private ConfigObject getDataSourcesConfig() {		
	Properties dataSourcesProps = new Properties()
	InputStream resourceStream
	try {		
		environments {
			development {
				resourceStream = new PathMatchingResourcePatternResolver().getResource('file:web-app/appConfig/mailConfig.properties').inputStream
			}
			production {
				resourceStream = new PathMatchingResourcePatternResolver().getResource('classpath:mailConfig.properties').inputStream
				}
		}
	   dataSourcesProps.load(resourceStream)
	}
	catch(Exception e){	
	}finally {
		resourceStream?.close()
	}
	ConfigObject configObject
	if(dataSourcesProps){
	 configObject = new ConfigSlurper().parse(dataSourcesProps)
	}
	return configObject	
}


// URL Mapping Cache Max Size, defaults to 5000
//grails.urlmapping.cache.maxsize = 1000

// What URL patterns should be processed by the resources plugin
grails.resources.adhoc.patterns = ['/images/*', '/css/*', '/js/*', '/plugins/*']

// The default codec used to encode data with ${}
grails.views.default.codec = "none" // none, html, base64
grails.views.gsp.encoding = "UTF-8"
grails.converters.encoding = "UTF-8"
// enable Sitemesh preprocessing of GSP pages
grails.views.gsp.sitemesh.preprocess = true
// scaffolding templates configuration
grails.scaffolding.templates.domainSuffix = 'Instance'

// Set to false to use the new Grails 1.2 JSONBuilder in the render method
grails.json.legacy.builder = false
// enabled native2ascii conversion of i18n properties files
grails.enable.native2ascii = true
// packages to include in Spring bean scanning
grails.spring.bean.packages = []
// whether to disable processing of multi part requests
grails.web.disable.multipart=false

// request parameters to mask when logging exceptions
grails.exceptionresolver.params.exclude = ['password']

// configure auto-caching of queries by default (if false you can cache individual queries with 'cache: true')
grails.hibernate.cache.queries = false

environments {
    development {
        grails.config.locations = [ "file:web-app/appConfig/executor.properties" ]
        grails.logging.jul.usebridge = true
        fileStore =  "web-app/fileStore"
    }
    production {
        grails.logging.jul.usebridge = false
        // TODO: grails.serverURL = "http://www.changeme.com"
        grails.config.locations = [ "classpath:${appName}-executor.properties"]
             //"file:/opt/comcast/software/tomcat/current/webapps/${appName}/appConfig/executor.properties" ]        
    	fileStore = "/${appName}/fileStore" 
        //"/rdk-test-tool/fileStore" 
    }
    test{
        grails.config.locations = [ "file:web-app/appConfig/executor.properties" ]
    }
}

modules.xmlfile.location="moduleConfig/StubDescriptor.xml"
boxdetails.xmlfile.location="moduleConfig/BoxDetails.xml"

python.execution.path="python"
//python.execution.path="C:/Python27/python.exe"

// log4j configuration
log4j = {
    // Example of changing the log pattern for the default console appender:      
    
    appenders {
        console name:'stdout', layout:pattern(conversionPattern: '%c{2} %m%n')
    }
    
   /* 
    root {
        info()
    }*/

    error  'org.codehaus.groovy.grails.web.servlet',        // controllers
           'org.codehaus.groovy.grails.web.pages',          // GSP
           'org.codehaus.groovy.grails.web.sitemesh',       // layouts
           'org.codehaus.groovy.grails.web.mapping.filter', // URL mapping
           'org.codehaus.groovy.grails.web.mapping',        // URL mapping
           'org.codehaus.groovy.grails.commons',            // core / classloading
           'org.codehaus.groovy.grails.plugins',            // plugins
           'org.codehaus.groovy.grails.orm.hibernate',      // hibernate integration
           'org.springframework',
           'org.hibernate',
           'net.sf.ehcache.hibernate'

}
//grailsApplication.config.EXEC_PATH

ConfigObject emailConfig = getDataSourcesConfig()

grails.mail.default.from=emailConfig?.get('default_from')
grails.mail.default.to=emailConfig?.get('default_to')

	grails {
		mail {
		  host = emailConfig?.get('host')
		  port = emailConfig?.get('port')
		  username = emailConfig?.get('user_name')
		  password = emailConfig?.get('user_pwd')
		  props = ["mail.smtp.starttls.enable":"true",
					   "mail.smtp.port":emailConfig?.get('port')]
		}
	}
