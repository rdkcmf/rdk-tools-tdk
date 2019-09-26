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

//NOTICE: Use this script only if fresh installation of the TDK tool is required

DROP DATABASE IF EXISTS rdktesttoolproddb;
DROP DATABASE IF EXISTS rdktesttoolproddb_temp;
drop user 'rdktesttooluser'@'127.0.0.1';

CREATE DATABASE IF NOT EXISTS rdktesttoolproddb;
CREATE USER 'rdktesttooluser'@'127.0.0.1' identified by '6dktoolus3r!';
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER, lock tables ON rdktesttoolproddb.* TO 'rdktesttooluser'@'127.0.0.1';


CREATE DATABASE IF NOT EXISTS rdktesttoolproddb_temp;
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER, lock tables ON rdktesttoolproddb_temp.* TO 'rdktesttooluser'@'127.0.0.1';
