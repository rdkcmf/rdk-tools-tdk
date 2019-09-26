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

dataSource {
    pooled = true
    driverClassName = "com.mysql.jdbc.Driver"
    intialSize = 10
    maxActive = 100
    dialect = 'org.hibernate.dialect.MySQL5InnoDBDialect'
}
hibernate {
    cache.use_second_level_cache = true
    cache.use_query_cache = false
    cache.region.factory_class = 'net.sf.ehcache.hibernate.EhCacheRegionFactory'
}
// environment specific settings
environments {
    development {
        dataSource {
            dbCreate = "update" // one of 'create', 'create-drop','update'
          // url = "jdbc:mysql://127.0.0.1/rdktesttooldb?autoReconnect=true"
            url = "jdbc:mysql://127.0.0.1/rdktesttooldevdb?autoReconnect=true"
            username = "rdkttuser"
            password = "6dkttus3r!"
        }
    }
    test {
        dataSource {
            dbCreate = "create-drop" // one of 'create', 'create-drop','update'
            url = "jdbc:mysql://127.0.0.1/rdktesttooltestdb?autoReconnect=true"
            username = "rdkttuser"
            password = "6dkttus3r!"
        }
    }
    production {
        dataSource {
            dbCreate = "update"
           // url = "jdbc:mysql://127.0.0.1/rdktesttoolproddbm4?autoReconnect=true" // Test DB for Testers - rdk-tdk-test.war
            url = "jdbc:mysql://127.0.0.1/rdktesttoolproddb?autoReconnect=true"
//			url = "jdbc:mysql://127.0.0.1/db1?autoReconnect=true"
            username = "rdktesttooluser"
            password = "6dktoolus3r!"
            pooled = true
            properties {
               maxActive = -1
               minEvictableIdleTimeMillis=1800000
               timeBetweenEvictionRunsMillis=1800000
               numTestsPerEvictionRun=3
               testOnBorrow=true
               testWhileIdle=true
               testOnReturn=true
               validationQuery="SELECT 1"
           }
        }
		
		dataSource_temp {
			dbCreate = "update"
		   // url = "jdbc:mysql://127.0.0.1/rdktesttoolproddbm4?autoReconnect=true" // Test DB for Testers - rdk-tdk-test.war
			url = "jdbc:mysql://127.0.0.1/rdktesttoolproddb_temp?autoReconnect=true"
//			url = "jdbc:mysql://127.0.0.1/tdkdb?autoReconnect=true"
			username = "rdktesttooluser"
			password = "6dktoolus3r!"
			pooled = true
			properties {
			   maxActive = -1
			   minEvictableIdleTimeMillis=1800000
			   timeBetweenEvictionRunsMillis=1800000
			   numTestsPerEvictionRun=3
			   testOnBorrow=true
			   testWhileIdle=true
			   testOnReturn=true
			   validationQuery="SELECT 1"
		   }
		}
    }
}
