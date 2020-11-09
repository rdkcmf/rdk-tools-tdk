##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
#########################################################################
#!/usr/bin/perl -wT

use strict;
use warnings;
use CGI;
use diagnostics;
use CGI qw(:standard);
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

#The size of the file must be within this value.
$CGI::POST_MAX = 1024 * 5000;

########USER SHOULD CONFIGURE THIS##########
#Give the path where the file should get uploaded
my $path_to_upload = "";

my $query = new CGI;
my $file_to_upload = $query->param("image");
#Your file will get uploaded as UploadedFile.png. 
$file_to_upload = "UploadedFile.png";
my $file = $query->param('POSTDATA');
open ( FILEUPLOAD, ">$path_to_upload/$file_to_upload" ) or die "$!";
binmode FILEUPLOAD;
print FILEUPLOAD $file;
close FILEUPLOAD;
