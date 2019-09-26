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
//the grails servlet version is defined here
grails.servlet.version = "2.5" // Change depending on 
//target container compliance (2.5 or 3.0)
//with the below config we define the location where the class files needs to be generated
grails.project.class.dir = "target/classes"
//the location fore the test classes can be defined with this
grails.project.test.class.dir = "target/test-classes"
//here we configure the location of the test reports 
grails.project.test.reports.dir = "target/test-reports"
// grails project target level version is configured here
grails.project.target.level = 1.6
//grails project source level version is configured here
grails.project.source.level = 1.6
//we can define how war file needs to be created 
//grails.project.war.file = "target/${appName}-${appVersion}.war"


//not required now : to fork the JVM to 
//isolate classpaths
// uncomment (and adjust settings)

//not required now : grails.project.fork = [
//not required now :   run: [maxMemory:1024, minMemory:64, debug:false, maxPerm:256]
//]

//here comes the dependency resolution 
grails.project.dependency.resolution = {
    // this will inherit default dependencies provided by Grails' 
    inherits("global") {
        // specify dependency 
		//exclusions here; 
		//for example, uncomment this 
		//to disable ehcache:
        // excludes 'ehcache'
    }
    log "error" 
	// log level of Ivy resolver, 
	//the log level can be configured it can be  either 
	// any of these 'error', 'warn', 'info', 'debug' or 'verbose'
    checksums true // Whether to verify checksums on resolve
	// whether to do a secondary resolve
    legacyResolve false 
	//on plugin installation, not advised and here for backwards compatibility

	//repositories for resolveing the dependencies are defined here.
    repositories {
        inherits true 
		// this is to decide Whether to inherit 
		//repository definitions from plugins

		//grails plugins dependencies.
        grailsPlugins()
		
		
		//for the grails home dependencies
        grailsHome()
		
		
		//grails central dependencies 
        grailsCentral()
		//dependency for maven local 
        mavenLocal()
		//dependency for maven central
        mavenCentral()

        grailsRepo "https://grails.org/plugins"
		
        // uncomment these (or add new ones) to enable 
		//remote dependency resolution from public Maven repositories
		
		//mavenRepo "http://repository.jboss.com/maven2/"
        //mavenRepo "http://snapshots.repository.codehaus.org"
        
		//these dependencies needs to be uncommented if issue in resolving dependencies.
        //mavenRepo "http://download.java.net/maven/2/"
		//mavenRepo "http://repository.codehaus.org"
       
    }
	
    // here we define the dependencies
    dependencies {
        // specify dependencies here under either 'build', 
		//'compile', 'runtime', 'test' or 'provided' scopes e.g.
		// dependency for the TDKB TCL support
		  compile 'org.apache.httpcomponents:httpclient:4.5.1'
		  // dependency for the TDKB TCL support
		  compile 'org.apache.httpcomponents:httpcore:4.4.1'
		  // dependency for the TDKB TCL support , to execute the TCL thru TDK approach
		  compile 'com.googlecode.json-simple:json-simple:1.1.1'
		  // dependency for gson
		  compile 'com.google.code.gson:gson:1.4'
		  //mysql connector dependency
		  runtime 'mysql:mysql-connector-java:5.1.10'
		   // for excel reader 
		 // runtime ('org.apache.poi:poi:3.7', 'org.apache.poi:poi-ooxml:3.7')
    }

    plugins {
        runtime ":hibernate:$grailsVersion"
		//for the jquery dependency
        runtime ":jquery:1.8.3"
        //compile ":shiro:1.1.4"
		//user management plugin shiro dependency
        compile (":shiro:1.1.4") {
            excludes([name: 'quartz', group: 'org.opensymphony.quartz'])
        }
        //quartz plugin dependency
        compile ":quartz2:2.1.6.2"
        
      //  compile ':jquery-date-time-picker:0.1.0'
        
     //   compile ":executor:0.3"
    //    compile ":quartz:1.0-RC9"
//      runtime ":resources:1.1.6"

        // Uncomment these (or add new ones) to enable additional resources capabilities
        //runtime ":zipped-resources:1.0"
        //runtime ":cached-resources:1.0"
        //runtime ":yui-minify-resources:0.1.5"
		
		//this is to resolve tomcat dependency
        build ":tomcat:$grailsVersion"
		// this to resolve the database migration plugin dependency
        runtime ":database-migration:1.3.2"
		//to resolve the cache dependency
        compile ':cache:1.0.1'
		//export plugin dependency , plugin to export the content to different formats.
		compile ":export:1.5"
		//the mail plugin dependency
		compile ":mail:1.0.1"
    }
}
